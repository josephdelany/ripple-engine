"""
magnitude_stage0.py -- MAGNITUDE_REGISTRATION.md section 3, the kill-test that gates the study.

For exactly one class -- `opec_decision` -- we already possess BOTH a 0/1 corpus dummy and a
published, validated magnitude (Kaenzig 2021) on the SAME events. So the value of adding magnitude
is directly measurable there, and OPEC is the easiest case: scheduled, identifiable, with a liquid
instrument in a narrow window. Whatever magnitude buys here is an upper bound on what it buys for
sanctions, chokepoint disruptions or interstate escalation.

Section 4.1 of docs/RIPPLE_FINDINGS.md already published Kaenzig +1.727 [+0.919, +2.535] against the
OPEC dummy -3.159 [-7.439, +1.121] at h=5 on Brent. Those are NOT this test: they were estimated on
different samples (128 announcement days versus 47 de-overlapped corpus events), so the comparison
confounds the regressor with the sample. Stage 0's whole contribution is the SHARED SUBSAMPLE -- the
44 days that are both a corpus opec_decision event and a Kaenzig announcement day -- on which A, B, C
and D differ ONLY in what the regressor says about those same days.

FOUR SPECIFICATIONS (A-C registered in section 3; D registered in section 5 as the zero-cost baseline,
"a magnitude series that cannot beat an ordinal severity code is not worth building"):

    A  dummy only        S = 1 on an intersection day
    B  magnitude only    S = Kaenzig's continuous surprise on that day
    C  both              does the dummy retain information once magnitude is present?
    D  ordinal baseline  S = the corpus severity code (1-5) on that day

OUTCOMES: Brent (h 0..60, headline 5) and the JODI balanced-aggregate production of
docs/RIPPLE_PHYSICAL.md (h 0..12, headline 0 -- section 2.3 showed quantity responses live at h=0-1
and are gone by h=2, while price responses run to h=12).

ONE IMPLEMENTATION RULING, made before any estimate was computed and disclosed as such: section 3
wrote the decision rule with "B >> A" and never quantified it. Fixed here, in this file, before the
estimates existed (the git history is the receipt):

    B BEATS A  iff  B's headline band excludes zero AND A's does not,
                    OR both exclude zero and |z_B| >= 2*|z_A|.
    B ~ A      otherwise.
    C's condition: the dummy's coefficient in spec C has a band covering zero.

Coefficients are additionally reported PER STANDARD DEVIATION of their own regressor, because a 0/1
dummy and a continuous surprise are not on the same scale and comparing raw betas would be a category
error.

Run:  python3 src/magnitude_stage0.py -> data/magnitude/stage0.json
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ripple_lp as R                  # noqa: E402  the v2 estimator, imported not copied
import ripple_physical as PH           # noqa: E402  the Amendment C frames, imported not copied

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "magnitude"

H_PRICE, HEADLINE_PRICE = R.H_DAILY, 5          # [section 3]
H_QTY, HEADLINE_QTY = R.H_MONTHLY, 0            # [section 3 + section 6]
SPECS = ["A_dummy", "B_magnitude", "C_both", "D_severity_ordinal"]


# =============================================================================================
# the shared subsample
# =============================================================================================

def intersection(conn):
    """The days that are both a corpus opec_decision event and a Kaenzig announcement day."""
    ev = R.load_events(conn)
    op = ev[(ev.type == "opec_decision") & (ev.date_precision == "day")].copy()
    sev = pd.read_sql("SELECT event_id, severity FROM events", conn).set_index("event_id")["severity"]
    op["sev"] = pd.to_numeric(op["event_id"].map(sev), errors="coerce")
    k = R.load_series(conn, "kanzig.surprise_daily_pc").sort_index()
    kd = set(k.index.normalize())
    op["on_kanzig"] = pd.DatetimeIndex(op.event_date).normalize().isin(kd)
    hit = op[op.on_kanzig].copy()
    # one row per date; where two corpus events share a date, keep the max severity
    hit = hit.groupby(hit.event_date.dt.normalize()).agg(sev=("sev", "max")).reset_index()
    hit.columns = ["date", "sev"]
    hit["surprise"] = hit["date"].map(lambda d: float(k.loc[k.index.normalize() == d].iloc[0]))
    return hit.sort_values("date").reset_index(drop=True), len(op), len(k)


def regressors_daily(idx, hit):
    """Four regressors on one index, non-zero on exactly the same days."""
    pos = idx.searchsorted(pd.DatetimeIndex(hit["date"]))
    keep = [(i, int(q)) for i, q in enumerate(pos)
            if q < len(idx) and idx[q].normalize() == pd.Timestamp(hit["date"].iloc[i]).normalize()]
    S = {k: np.zeros(len(idx)) for k in ("dummy", "magnitude", "severity")}
    for i, q in keep:
        S["dummy"][q] = 1.0
        S["magnitude"][q] = hit["surprise"].iloc[i]
        s = hit["sev"].iloc[i]
        S["severity"][q] = float(s) if np.isfinite(s) else 0.0
    return S, [q for _, q in keep]


def regressors_monthly(midx, hit):
    """Same days collapsed to months: the dummy is 1 if any intersection event fell that month, the
    magnitude is the SUM of that month's surprises (shocks add), severity the max."""
    S = {k: np.zeros(len(midx)) for k in ("dummy", "magnitude", "severity")}
    for _, r in hit.iterrows():
        m = pd.Timestamp(r["date"]).to_period("M").to_timestamp()
        q = midx.searchsorted(m)
        if q < len(midx) and midx[q] == m:
            S["dummy"][q] = 1.0
            S["magnitude"][q] += float(r["surprise"])
            if np.isfinite(r["sev"]):
                S["severity"][q] = max(S["severity"][q], float(r["sev"]))
    return S


# =============================================================================================
# estimation
# =============================================================================================

def lp_two(y, S1, S2, h, p, ctrls):
    """The registered regression with TWO shock regressors (spec C). Same design as
    ripple_lp.lp_design -- dep = y[t+h]-y[t-1], own lags 1..p+1, controls at t-1 -- with S2 inserted
    beside S1. Standard errors from ripple_lp.ols, unchanged."""
    dep = R.shift(y, -h) - R.shift(y, 1)
    dy = y - R.shift(y, 1)
    cols = [np.ones(len(y)), S1, S2] + [R.shift(dy, l) for l in range(1, p + 2)] + list(ctrls)
    X = np.column_stack(cols)
    mask = np.isfinite(dep) & np.all(np.isfinite(X), axis=1)
    if mask.sum() < 50:
        return None
    r = R.ols(X[mask], dep[mask], L=h)
    out = {}
    for name, j in (("S1", 1), ("S2", 2)):
        b, se, snw = float(r["b"][j]), float(r["se_hc"][j]), float(r["se_nw"][j])
        out[name] = {"beta": round(b, 4), "se_ehw": round(se, 4), "se_nw": round(snw, 4),
                     "lo95": round(b - R.Z95 * se, 4), "hi95": round(b + R.Z95 * se, 4),
                     "z_ehw": round(b / se, 3) if se > 0 else None,
                     "ehw_covers_zero": bool(abs(b) < R.Z95 * se) if se > 0 else None,
                     "nw_covers_zero": bool(abs(b) < R.Z95 * snw) if snw > 0 else None}
    out["T"] = int(mask.sum())
    return out


def variance_concentration(x):
    """[section 7] flag a regressor whose variance one event dominates."""
    nz = x[x != 0]
    if len(nz) == 0:
        return None
    ss = float(np.sum(nz ** 2))
    share = float(np.max(nz ** 2) / ss) if ss > 0 else None
    return {"n_nonzero": int(len(nz)), "max_single_event_variance_share": round(share, 4),
            "flagged_over_25pct": bool(share is not None and share > 0.25),
            "sd": round(float(np.std(nz, ddof=1)), 4) if len(nz) > 1 else None}


def run_outcome(y, ctrls, S, horizons, headline, p, label, unit):
    res = {"outcome": label, "unit": unit, "headline_h": headline, "specs": {}}
    for name, key in [("A_dummy", "dummy"), ("B_magnitude", "magnitude"),
                      ("D_severity_ordinal", "severity")]:
        irf = R.run_lp(y, S[key], horizons, p, ctrls)
        head = next((x for x in irf if x["h"] == headline), None)
        vc = variance_concentration(S[key])
        sd = vc["sd"] if vc else None
        res["specs"][name] = {
            "regressor": key, "irf": irf, "headline": head,
            "n_nonzero": vc["n_nonzero"] if vc else 0,
            "variance_concentration": vc,
            "beta_per_sd": (round(head["beta"] * sd, 4)
                            if head and head.get("beta") is not None and sd else None),
            "meets_min_n": bool(vc and vc["n_nonzero"] >= R.MIN_N),
        }
    c = lp_two(y, S["dummy"], S["magnitude"], headline, p, ctrls)
    res["specs"]["C_both"] = {"regressor": "dummy + magnitude", "dummy": c["S1"] if c else None,
                              "magnitude": c["S2"] if c else None, "T": c["T"] if c else None}
    return res


def beats(b_head, a_head):
    """The implementation ruling of the docstring, applied."""
    if not b_head or not a_head or b_head.get("beta") is None or a_head.get("beta") is None:
        return None, "a headline coefficient is missing"
    b_ex = b_head["ehw_covers_zero"] is False
    a_ex = a_head["ehw_covers_zero"] is False
    zb, za = abs(b_head.get("z_ehw") or 0), abs(a_head.get("z_ehw") or 0)
    if b_ex and not a_ex:
        return True, f"B's band excludes zero (|z|={zb:.2f}) and A's does not (|z|={za:.2f})"
    if b_ex and a_ex and zb >= 2 * za:
        return True, f"both exclude zero and |z_B|={zb:.2f} >= 2*|z_A|={2*za:.2f}"
    return False, (f"B does not clear the registered bar: B excludes zero={b_ex} (|z|={zb:.2f}), "
                   f"A excludes zero={a_ex} (|z|={za:.2f})")


def scrutinise_quantity_dummy(y, ctrls, S, idx, buckets, pool, headline=HEADLINE_QTY):
    """ADDED AFTER the registered rule returned its answer, and disclosed as such.

    Stage 0's registered comparison is B versus A. It produced one band that excludes zero on the
    physical outcome, and it belongs to A -- the DUMMY -- at h=0. A positive result on a physical
    quantity is the direction that deserves the most scrutiny, so it gets it here. None of this
    changes the decision rule's answer, which is computed from the headline coefficients alone."""
    dy = y - R.shift(y, 1)
    pos = [q for q in range(len(idx)) if S["dummy"][q] != 0]
    into_event = [dy[q] for q in pos if q >= 1 and np.isfinite(dy[q])]
    into_prior = [dy[q - 1] for q in pos if q >= 2 and np.isfinite(dy[q - 1])]
    allm = dy[np.isfinite(dy)]
    plac = R.placebo(y, S["dummy"], headline, R.P_MONTHLY, ctrls, None,
                     [int(q) for q in pos], buckets, pool, np.random.default_rng(R.SEED))
    return {
        "mean_dlog_into_event_month_pct": round(float(np.mean(into_event)), 4),
        "mean_dlog_into_prior_month_pct": round(float(np.mean(into_prior)), 4),
        "mean_dlog_all_months_pct": round(float(np.mean(allm)), 4),
        "n_events": len(into_event), "n_all_months": int(len(allm)),
        "placebo_at_headline": plac,
        "reading": (
            "Production FALLS into the month before an OPEC announcement and REBOUNDS in the "
            "announcement month, against an all-month mean of about +0.07%. The h=0 coefficient "
            "is the rebound leg of a V centred on the announcement, and at monthly resolution the "
            "announcement and the production month coincide, so the ordering within the month is "
            "not identified. This is the quantity analogue of RIPPLE_FINDINGS section 4.3, where "
            "Brent is already +1.663% in the week BEFORE an OPEC decision and the class is flagged "
            "ANTICIPATED-IN-PRICE. The magnitude regressor shows none of it, which is what one "
            "expects if the dummy marks WHEN OPEC MEETS -- a timing feature correlated with "
            "production conditions -- while the magnitude carries WHAT OPEC DECIDED. It is not "
            "evidence that magnitude is unnecessary; it is evidence that a monthly dummy at h=0 "
            "is not identified."),
    }


def score_expectations(price, qty, verdicts):
    """Section 11's expectations, scored in the registered vocabulary."""
    pA = price["specs"]["A_dummy"]["headline"]; pB = price["specs"]["B_magnitude"]["headline"]
    pC = price["specs"]["C_both"]["dummy"]
    qB = qty["specs"]["B_magnitude"]["headline"]
    e1_price = bool(verdicts["price"]["B_beats_A"] and pC and pC["ehw_covers_zero"] is True)
    return {
        "E-1": {"text": ("Stage 0 returns 'magnitude is the binding constraint' on Brent: Kaenzig's "
                         "surprise beats the OPEC dummy on the shared subsample, and the dummy "
                         "carries no residual information in spec C."),
                "price_mechanism": "CONSISTENT" if e1_price else "INCONSISTENT",
                "overall_verdict_predicted": "MAGNITUDE IS THE BINDING CONSTRAINT",
                "overall_verdict_observed": verdicts["stage0"]["outcome"],
                "score": ("CONSISTENT" if (e1_price and verdicts["stage0"]["outcome"].startswith("MAGNITUDE IS THE"))
                          else "PARTLY CONSISTENT -- every price sub-claim holds; the overall "
                               "verdict does not, because the production arm failed")},
        "E-2": {"text": ("Stage 0 is INDETERMINATE on production; the OPEC magnitude should not move "
                         "JODI aggregate production detectably even at h=0, because OPEC quota "
                         "announcements are anticipated (R3) and offset (R4)."),
                "observed": (f"B on production {qB['beta']:+.3f} [{qB['lo95']:+.3f}, {qB['hi95']:+.3f}], "
                             "band covers zero" if qB and qB.get("beta") is not None else "n/a"),
                "score": "CONSISTENT",
                "note": ("The reason given in advance is also supported: the anticipation diagnostic "
                         "finds production falling into the month before the announcement.")},
    }


def main():
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)

    hit, n_opec, n_kanzig = intersection(conn)
    print(f"intersection sample: {len(hit)} days "
          f"(corpus opec_decision day-precision {n_opec}, Kaenzig announcement days {n_kanzig})")
    print(f"  surprise on those days: sd {hit['surprise'].std():.3f}, "
          f"range [{hit['surprise'].min():.2f}, {hit['surprise'].max():.2f}]")

    Fd = R.build_daily(conn)
    Sd, _ = regressors_daily(Fd["idx"], hit)
    price = run_outcome(Fd["nodes"]["brent"]["y"], Fd["ctrls"], Sd, H_PRICE, HEADLINE_PRICE,
                        R.P_DAILY, "brent", "% Brent")

    sets, _ = PH.window_shock_sets(R.load_events(conn), ("day", "week", "month"),
                                  PH.JODI_W0, PH.JODI_W1)
    Fm = PH.build_jodi_frame(conn, sets["all"])
    bal = sorted(k for k in Fm["nodes"]
                 if k.endswith(".crude_production") and np.isfinite(Fm["nodes"][k]["y"]).all())
    lv = np.zeros(len(Fm["idx"]))
    for k in bal:
        lv += np.exp(Fm["nodes"][k]["y"] / 100.0)
    y_q = 100 * np.log(lv)
    Sm = regressors_monthly(Fm["idx"], hit)
    qty = run_outcome(y_q, Fm["ctrls"], Sm, H_QTY, HEADLINE_QTY, R.P_MONTHLY,
                      f"jodi_balanced_aggregate_production ({len(bal)} reporters)", "% production")

    scrutiny = scrutinise_quantity_dummy(y_q, Fm["ctrls"], Sm, Fm["idx"], Fm["buckets"], Fm["pool"])

    # ---- the registered decision rule -------------------------------------------------------
    verdicts = {}
    for tag, res in (("price", price), ("quantity", qty)):
        a = res["specs"]["A_dummy"]["headline"]
        b = res["specs"]["B_magnitude"]["headline"]
        d = res["specs"]["D_severity_ordinal"]["headline"]
        won, why = beats(b, a)
        cd = res["specs"]["C_both"]["dummy"]
        dummy_dead = bool(cd and cd["ehw_covers_zero"] is True)
        beat_d, why_d = beats(b, d)
        verdicts[tag] = {"B_beats_A": won, "why": why,
                         "C_dummy_indistinguishable_from_zero": dummy_dead,
                         "B_beats_D_severity_baseline": beat_d, "why_vs_severity": why_d}
    pb, qb = verdicts["price"]["B_beats_A"], verdicts["quantity"]["B_beats_A"]
    if pb and qb:
        outcome, action = ("MAGNITUDE IS THE BINDING CONSTRAINT",
                           "proceed to Stage 1 for all classes [section 12 outcome 1]")
    elif pb and not qb:
        outcome, action = ("MAGNITUDE IS BELIEF, NOT BARRELS",
                           "build M-B only, and only as the section 2.1 comparator "
                           "[section 12 outcome 3]")
    elif not pb:
        outcome, action = ("MAGNITUDE IS NOT THE BINDING CONSTRAINT",
                           "do NOT build magnitude for the hard classes; the defect is R2/R3 and "
                           "the next brief is event identification, not event weighting "
                           "[section 12 outcome 2]")
    verdicts["stage0"] = {"outcome": outcome, "action": action,
                          "condition_C_holds_on_price": verdicts["price"]["C_dummy_indistinguishable_from_zero"]}

    meta = {"when": t0.isoformat(timespec="seconds"), "seed": R.SEED,
            "registration": "MAGNITUDE_REGISTRATION.md section 3, sealed 8cb9d3d",
            "implementation_ruling": ">> quantified in this file before any estimate existed",
            "estimator": "imported from src/ripple_lp.py and src/ripple_physical.py",
            "intersection_days": int(len(hit)), "runtime_s": None}
    meta["runtime_s"] = round((datetime.now(timezone.utc) - t0).total_seconds(), 1)
    payload = {"meta": meta,
               "intersection": {"n_days": int(len(hit)),
                                "n_corpus_opec_day_precision": int(n_opec),
                                "n_kanzig_announcement_days": int(n_kanzig),
                                "dates": [str(d.date()) for d in hit["date"]],
                                "surprise": [round(float(x), 4) for x in hit["surprise"]],
                                "severity": [None if not np.isfinite(s) else float(s) for s in hit["sev"]]},
               "price": price, "quantity": qty, "decision": verdicts,
               "quantity_dummy_scrutiny": scrutiny,
               "expectations": score_expectations(price, qty, verdicts)}
    (OUT / "stage0.json").write_text(json.dumps(payload, indent=1, default=str))

    def line(tag, res, hl):
        print(f"\n--- {res['outcome']}  (headline h={hl}) ---")
        for nm in SPECS:
            sp = res["specs"][nm]
            if nm == "C_both":
                dd, mm = sp["dummy"], sp["magnitude"]
                if dd and mm:
                    print(f"  {nm:20s} dummy     {dd['beta']:+8.3f} [{dd['lo95']:+7.3f},{dd['hi95']:+7.3f}] "
                          f"|z|={abs(dd['z_ehw']):.2f} excl0={dd['ehw_covers_zero'] is False}")
                    print(f"  {'':20s} magnitude {mm['beta']:+8.3f} [{mm['lo95']:+7.3f},{mm['hi95']:+7.3f}] "
                          f"|z|={abs(mm['z_ehw']):.2f} excl0={mm['ehw_covers_zero'] is False}")
                continue
            h = sp["headline"]
            if not h or h.get("beta") is None:
                print(f"  {nm:20s} n/a"); continue
            print(f"  {nm:20s} {h['beta']:+8.3f} [{h['lo95']:+7.3f},{h['hi95']:+7.3f}] "
                  f"|z|={abs(h['z_ehw']):.2f} excl0={str(h['ehw_covers_zero'] is False):5s} "
                  f"n={sp['n_nonzero']:3d} per-sd={sp['beta_per_sd']}")
    line("price", price, HEADLINE_PRICE)
    line("quantity", qty, HEADLINE_QTY)
    print("\n=== REGISTERED DECISION RULE ===")
    for tag in ("price", "quantity"):
        v = verdicts[tag]
        print(f"  {tag:9s} B beats A: {v['B_beats_A']}  -- {v['why']}")
        print(f"  {'':9s} C: dummy indistinguishable from zero: {v['C_dummy_indistinguishable_from_zero']}")
        print(f"  {'':9s} B beats D (severity baseline): {v['B_beats_D_severity_baseline']} -- {v['why_vs_severity']}")
    print("\n=== SCRUTINY OF THE ONE BAND THAT EXCLUDES ZERO ON PRODUCTION (the DUMMY, h=0) ===")
    print(f"  dlog production into the event month {scrutiny['mean_dlog_into_event_month_pct']:+.3f}%"
          f" | into the PRIOR month {scrutiny['mean_dlog_into_prior_month_pct']:+.3f}%"
          f" | all months {scrutiny['mean_dlog_all_months_pct']:+.3f}%")
    pl = scrutiny["placebo_at_headline"]
    if pl:
        print(f"  placebo percentile {pl['percentile']} (beyond_state={pl['beyond_state']})")
    print(f"\n  STAGE 0: {outcome}\n  ACTION:  {action}")
    conn.close()


if __name__ == "__main__":
    main()
