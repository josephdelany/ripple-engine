"""
magnitude_severity_retest.py -- MAGNITUDE_REGISTRATION.md section 5, the pre-registered re-test.

data/edge_battery.json carries `severity_dose_response` as VALIDATED:

    "high-severity (4-5) events ripple harder into oil than low-severity (1-2)"
    amp +5.079 [+1.003, +9.364], n=116 (76 high / 40 low), perm p 0.0303,
    survives FDR q=0.10, FAILS Bonferroni (adj 0.394).

The object is mean |CAR+20| in Brent for severity>=4 minus the same for severity<=2. It compares
EVENTS TO OTHER EVENTS and never to a non-event day -- the same defect on which v2 section 3
retracted five of six `propagation_edges`. A world in which nothing transmits, but severe events
happen in volatile periods, passes it: |CAR| is larger in volatile periods whether or not the event
did anything.

The verdict words were fixed BEFORE this file existed (MAGNITUDE_REGISTRATION.md section 5,
sealed at 8cb9d3d):
    RETAINED     if TRANSMITTING under the ripple discipline
    RETRACTED    if NULL
    INSUFFICIENT if below n = 15 after de-overlapping

TWO TESTS, because substituting an easier object for the published one would not be a re-test:
  A. The claim AS PUBLISHED -- the |CAR+20| high-minus-low difference -- against a VIX+GPR-matched
     placebo difference. The placebo draws pseudo-events matched on each real event's own state
     bucket, so the null it builds is exactly "severe events sit in more volatile states". If the
     matched placebo reproduces the observed gap, the state mix explains it and nothing rippled.
  B. The same events as ordinary ripple cells -- Brent, h=20, high and low dummies estimated
     separately with EHW and Newey-West bands and the registered placebo.

`data/edge_battery.json` is NOT edited here; the status is reported for the owning session to act
on, exactly as RIPPLE_REGISTRATION.md Amendment B did with the six propagation edges.

Run:  python3 src/magnitude_severity_retest.py -> data/magnitude/severity_retest.json
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
import ripple_lp as R           # noqa: E402  -- the v2 estimator, imported not copied

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "magnitude"

HORIZON = 20                      # edge_battery.HORIZON, the horizon the claim was made at
HI, LO = 4, 2                     # severity >= 4 vs severity <= 2, as published
SEV_BAND = {"chokepoint_disruption": 3, "infrastructure_attack": 3, "conflict_escalation": 3,
            "opec_decision": 3, "demand_shock": 3, "sanctions": 2, "policy_response": 2}
PUBLISHED = {"amp": 5.0789, "ci": [1.0029, 9.3643], "n": 116, "n_high": 76, "n_low": 40,
             "perm_p": 0.0303, "survives_fdr": True, "survives_bonferroni": False,
             "bonferroni_adj": 0.3939, "validated": True,
             "source": "data/edge_battery.json amplification[] severity_dose_response"}


# =============================================================================================
# provenance of the severity column (MAGNITUDE_REGISTRATION.md section 5, disclosure 1)
# =============================================================================================

def severity_provenance(conn):
    """Which severity values are analyst judgement and which, if any, were imputed by class?

    MAGNITUDE_REGISTRATION.md section 5 reported that 102 of 313 events sit exactly on the
    deterministic SEV_BAND value that `admit_events.py` assigns to auto-admitted candidates, and
    called that 'an upper bound on how many are class-imputed'. This function establishes what the
    true count is, because an upper bound registered as a Tier 1 defect deserves to be resolved
    rather than repeated."""
    ev = pd.read_sql("SELECT event_id, type, severity FROM events", conn)
    ev["sev"] = pd.to_numeric(ev["severity"], errors="coerce")
    ev["band"] = ev["type"].map(SEV_BAND)
    on_band = ev["sev"] == ev["band"]

    # the auto-admit path leaves two receipts: an admission log, and 'AUTO-ADMIT' in the
    # candidate sheet's rec_reason. Look for both.
    log = ROOT / "data" / "extract" / "admission_log.csv"
    admission_log_exists = log.exists()
    auto_ids, reviewed, approved = set(), set(), set()
    sheet = ROOT / "data" / "candidate_review.csv"
    if sheet.exists():
        import csv
        for r in csv.DictReader(open(sheet, newline="", encoding="utf-8")):
            eid = r.get("event_id")
            if not eid:
                continue
            reviewed.add(eid)
            if "AUTO-ADMIT" in (r.get("rec_reason") or ""):
                auto_ids.add(eid)
            if (r.get("joe_decision") or "").strip() == "approve":
                approved.add(eid)
    ids = set(ev["event_id"])
    return {
        "n_events": int(len(ev)),
        "n_severity_populated": int(ev["sev"].notna().sum()),
        "n_on_class_band": int(on_band.sum()),
        "admission_log_exists": admission_log_exists,
        "n_in_candidate_review_sheet": int(len(ids & reviewed)),
        "n_flagged_AUTO_ADMIT": int(len(ids & auto_ids)),
        "n_joe_approved": int(len(ids & approved)),
        "n_demonstrably_class_imputed": int(len(ids & auto_ids)),
        "off_band_event_ids": sorted(ev.loc[~on_band & ev["sev"].notna(), "event_id"]),
        "finding": (
            "The auto-admit path in src/admit_events.py assigns a deterministic severity by event "
            "type and WOULD put a measured and an inferred value in one column, which is what "
            "INV-5 forbids. It has not run against this corpus: there is no admission_log.csv, no "
            "current event carries an AUTO-ADMIT rec_reason, and every current event found in the "
            "candidate sheet is joe_decision=approve. The 102 events sitting on their class band "
            "are therefore NOT demonstrably imputed -- 3 and 2 are simply the modal severities of a "
            "1-5 ordinal, so a large overlap is what chance predicts. The defect is LATENT (in the "
            "code, waiting for the next run) rather than LIVE (in the data). The live issue is "
            "different and simpler: severity carries no per-value source anywhere, so it is "
            "uniformly analyst judgement -- not mixed, but INFERRED throughout, and it may never be "
            "read as a measured magnitude."),
    }


def clustering_unit_check(ev):
    """The SECOND defect, found while replicating the published n.

    edge_battery._oil_type_frame clusters WITHIN EVENT TYPE, with a comment explaining why: the
    neighbouring test compares chokepoint events against sanctions events, and clustering all types
    together let a chokepoint within 35 days of a sanction be cannibalised. That is the right unit
    for THAT test. `severity_dose_response` inherits the same frame unchanged -- but its grouping
    variable is severity, not type, so two high-severity events of different types ten days apart
    both survive as independent observations. The unit of dependence for a severity comparison is
    the episode, and clustering within type does not de-overlap the severity arms.

    Same class of error as the unit-of-dependence defect found in the grid price arm (a7fbae9):
    an n that counts correlated observations as independent, which narrows every interval."""
    e = ev[ev["date_precision"] == "day"].copy()
    e["sev"] = pd.to_numeric(e["severity"], errors="coerce")
    out = {}
    for lab, m in [("high_sev_ge_4", e.sev >= HI), ("low_sev_le_2", e.sev <= LO)]:
        sub = e[m]
        within_type = 0
        for _, g in sub.groupby("type"):
            within_type += len(R.cluster_first_dates(g["event_date"]))
        out[lab] = {
            "raw": int(len(sub)),
            "clustered_within_type": int(within_type),
            "clustered_within_severity_group": int(len(R.cluster_first_dates(sub["event_date"]))),
        }
    out["note"] = (
        "clustered_within_type is the unit the published claim used; "
        "clustered_within_severity_group is the unit the comparison requires. "
        "The gap is the number of overlapping same-severity episodes counted as independent.")
    return out


# =============================================================================================
# test A -- the claim as published, against a state-matched placebo
# =============================================================================================

def car_mags(y, idx, dates, h=HORIZON):
    """|CAR+h| in per cent: |y[t+h] - y[t-1]| on 100*log Brent, one value per de-overlapped event."""
    out, pos = [], []
    for d in dates:
        q = int(idx.searchsorted(pd.Timestamp(d)))
        if q < 1 or q + h >= len(y):
            continue
        v = y[q + h] - y[q - 1]
        if np.isfinite(v):
            out.append(abs(v)); pos.append(q)
    return np.array(out), pos


def matched_placebo_diff(y, pos_hi, pos_lo, buckets, pool, rng, n_draws=R.N_PLACEBO, h=HORIZON):
    """The null the published test never built: draw a pseudo-event for each real event, matched on
    that event's own (VIX decile, GPR decile) at t-1, and take the same high-minus-low difference.
    Its spread is the gap the STATE MIX alone produces."""
    def pools_for(pos):
        out, fb = [], 0
        for q in pos:
            b = buckets.get(q)
            cand = pool.get(b, []) if b is not None else []
            if len(cand) < 5 and b is not None:
                fb += 1
                cand = [x for k, v in pool.items() if k[0] == b[0] for x in v]
            out.append(np.array(cand, dtype=int))
        return out, fb
    ph, fbh = pools_for(pos_hi)
    pl, fbl = pools_for(pos_lo)
    if any(len(p) == 0 for p in ph + pl):
        ph = [p for p in ph if len(p)]; pl = [p for p in pl if len(p)]
    if not ph or not pl:
        return None
    draws = []
    for _ in range(n_draws):
        a = []          # one index drawn per pseudo-event, used for both ends of the window
        for p in ph:
            q = int(p[rng.integers(0, len(p))])
            if q + h < len(y) and q >= 1:
                a.append(abs(y[q + h] - y[q - 1]))
        b = []
        for p in pl:
            q = int(p[rng.integers(0, len(p))])
            if q + h < len(y) and q >= 1:
                b.append(abs(y[q + h] - y[q - 1]))
        a = [v for v in a if np.isfinite(v)]; b = [v for v in b if np.isfinite(v)]
        if len(a) < R.MIN_N or len(b) < R.MIN_N:
            continue
        draws.append(float(np.mean(a) - np.mean(b)))
    if len(draws) < 100:
        return None
    return np.array(draws), fbh + fbl


def welch(a, b):
    """Difference in means with an unequal-variance (HC1-equivalent) band -- the same object the
    published test reported, so the two are comparable."""
    na, nb = len(a), len(b)
    d = float(np.mean(a) - np.mean(b))
    se = float(np.sqrt(np.var(a, ddof=1) / na + np.var(b, ddof=1) / nb))
    return {"diff": round(d, 4), "se": round(se, 4),
            "lo95": round(d - R.Z95 * se, 4), "hi95": round(d + R.Z95 * se, 4),
            "excludes_zero": bool(abs(d) > R.Z95 * se), "n_a": na, "n_b": nb,
            "mean_a": round(float(np.mean(a)), 4), "mean_b": round(float(np.mean(b)), 4)}


def permutation_p(a, b, rng, n_iter=10000):
    """Label permutation on the pooled events -- the published test's own p, reproduced."""
    obs = float(np.mean(a) - np.mean(b))
    pooled = np.concatenate([a, b]); na = len(a)
    cnt = 0
    for _ in range(n_iter):
        rng.shuffle(pooled)
        if float(np.mean(pooled[:na]) - np.mean(pooled[na:])) >= obs:
            cnt += 1
    return round(cnt / n_iter, 4)


def run_test_a(F, ev, rng, restrict_ids=None, label="all_events"):
    y, idx = F["nodes"]["brent"]["y"], F["idx"]
    e = ev[ev["date_precision"] == "day"].copy()
    e["sev"] = pd.to_numeric(e["severity"], errors="coerce")
    if restrict_ids is not None:
        e = e[e["event_id"].isin(restrict_ids)]
    hi_d = R.cluster_first_dates(e.loc[e.sev >= HI, "event_date"])
    lo_d = R.cluster_first_dates(e.loc[e.sev <= LO, "event_date"])
    a, pos_hi = car_mags(y, idx, hi_d)
    b, pos_lo = car_mags(y, idx, lo_d)
    res = {"sample": label, "n_high": len(a), "n_low": len(b), "horizon": HORIZON,
           "outcome": "|CAR+20| in Brent, per cent"}
    if len(a) < R.MIN_N or len(b) < R.MIN_N:
        res["verdict"] = "INSUFFICIENT"
        res["reason"] = f"n_high={len(a)}, n_low={len(b)}, minimum {R.MIN_N} each"
        return res
    res["welch"] = welch(a, b)
    res["perm_p"] = permutation_p(a.copy(), b.copy(), rng)
    mp = matched_placebo_diff(y, pos_hi, pos_lo, F["_buckets"], F["_pool"], rng)
    if mp is None:
        res["placebo"] = None
        res["verdict"] = "INSUFFICIENT"
        res["reason"] = "state-matched placebo could not be built"
        return res
    draws, fb = mp
    real = res["welch"]["diff"]
    pct = float(np.mean(draws < real) * 100)
    res["placebo"] = {
        "n_draws": int(len(draws)), "percentile": round(pct, 1),
        "pseudo_mean": round(float(np.mean(draws)), 4),
        "pseudo_p2_5": round(float(np.percentile(draws, 2.5)), 4),
        "pseudo_p97_5": round(float(np.percentile(draws, 97.5)), 4),
        "beyond_state": bool(pct < 2.5 or pct > 97.5),
        "buckets_fallback_to_vix_only": int(fb),
        "reads": ("the state-matched placebo reproduces the observed gap: the volatility and "
                  "geopolitical-risk mix of severe events explains it"
                  if not (pct < 2.5 or pct > 97.5) else
                  "the observed gap is outside what the matched state mix produces"),
    }
    transmitting = res["welch"]["excludes_zero"] and res["placebo"]["beyond_state"]
    res["verdict"] = "TRANSMITTING" if transmitting else "NULL"
    res["status"] = {"TRANSMITTING": "RETAINED", "NULL": "RETRACTED",
                     "INSUFFICIENT": "INSUFFICIENT"}[res["verdict"]]
    return res


# =============================================================================================
# test B -- the same events as ordinary ripple cells
# =============================================================================================

def run_test_b(F, ev, rng):
    y, idx = F["nodes"]["brent"]["y"], F["idx"]
    e = ev[ev["date_precision"] == "day"].copy()
    e["sev"] = pd.to_numeric(e["severity"], errors="coerce")
    all_dates = list(e["event_date"])
    out = []
    for name, dates in [("severity_high_4_5", R.cluster_first_dates(e.loc[e.sev >= HI, "event_date"])),
                        ("severity_low_1_2", R.cluster_first_dates(e.loc[e.sev <= LO, "event_date"]))]:
        S = R.dummies_for(idx, dates)
        event_pos = [int(q) for q in idx.searchsorted(pd.DatetimeIndex(dates)) if q < len(idx)]
        irf = R.run_lp(y, S, R.H_DAILY, R.P_DAILY, F["ctrls"])
        head = next((r for r in irf if r["h"] == HORIZON), None)
        n_ev = head["n_events"] if head else 0
        plac = None
        if n_ev >= R.MIN_N:
            plac = R.placebo(y, S, HORIZON, R.P_DAILY, F["ctrls"], None, event_pos,
                             F["_buckets"], F["_pool"], rng)
        v, fragile = R.verdict(head, plac, n_ev)
        out.append({"shock": name, "node": "brent", "headline_h": HORIZON, "n_events": n_ev,
                    "irf": irf, "placebo": plac, "verdict": v, "fragile": fragile})
    return out


def main():
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(R.SEED)
    conn = sqlite3.connect(DB)
    ev = pd.read_sql("SELECT event_id, event_date, date_precision, type, severity FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])

    prov = severity_provenance(conn)
    clus = clustering_unit_check(ev)
    print("severity provenance:", {k: v for k, v in prov.items()
                                   if k not in ("finding", "off_band_event_ids")})

    F = R.build_daily(conn)
    # the registered placebo pools, built once on the whole day-precision corpus
    all_dates = list(ev.loc[ev.date_precision == "day", "event_date"])
    idx = F["idx"]
    far = np.ones(len(idx), dtype=bool)
    for d in pd.DatetimeIndex(sorted(set(all_dates))):
        lo = idx.searchsorted(d - pd.Timedelta(days=R.EXCL_DAYS))
        hi = idx.searchsorted(d + pd.Timedelta(days=R.EXCL_DAYS))
        far[lo:hi] = False
    buckets, pool = {}, {}
    for q in range(len(idx)):
        v, g = F["vix_dec"][q], F["gpr_dec"][q]
        if np.isfinite(v) and np.isfinite(g):
            buckets[q] = (int(v), int(g))
            if far[q]:
                pool.setdefault(buckets[q], []).append(q)
    F["_buckets"], F["_pool"] = buckets, pool
    print("placebo pool days:", sum(len(v) for v in pool.values()), "buckets:", len(pool))

    a_all = run_test_a(F, ev, rng, None, "all_events")
    a_off = run_test_a(F, ev, rng, set(prov["off_band_event_ids"]), "off_class_band_only")
    b_rows = run_test_b(F, ev, rng)

    payload = {
        "meta": {"when": t0.isoformat(timespec="seconds"), "seed": R.SEED,
                 "registration": "MAGNITUDE_REGISTRATION.md section 5, sealed 8cb9d3d",
                 "estimator": "imported from src/ripple_lp.py",
                 "edge_battery_json_edited": False,
                 "runtime_s": None},
        "published_claim": PUBLISHED,
        "severity_provenance": prov,
        "clustering_unit_check": clus,
        "test_a_claim_as_published": {"all_events": a_all, "off_class_band_only": a_off},
        "test_b_ripple_cells": b_rows,
        "verdict": a_all.get("status", "INSUFFICIENT"),
    }
    payload["meta"]["runtime_s"] = round((datetime.now(timezone.utc) - t0).total_seconds(), 1)
    (OUT / "severity_retest.json").write_text(json.dumps(payload, indent=1, default=str))

    print("\nclustering unit:", {k: v for k, v in clus.items() if k != "note"})
    print("\n--- TEST A: the claim as published, vs a state-matched placebo ---")
    for k in ("all_events", "off_class_band_only"):
        r = payload["test_a_claim_as_published"][k]
        print(f"  [{k}] n_high={r['n_high']} n_low={r['n_low']} verdict={r['verdict']}")
        if "welch" in r:
            w = r["welch"]
            print(f"     diff {w['diff']:+.3f} [{w['lo95']:+.3f}, {w['hi95']:+.3f}] "
                  f"excl0={w['excludes_zero']}  perm_p={r['perm_p']}")
        if r.get("placebo"):
            p = r["placebo"]
            print(f"     placebo pct {p['percentile']}  pseudo mean {p['pseudo_mean']:+.3f} "
                  f"[{p['pseudo_p2_5']:+.3f}, {p['pseudo_p97_5']:+.3f}]  beyond={p['beyond_state']}")
            print(f"     -> {p['reads']}")
    print("\n--- TEST B: the same events as ripple cells (Brent, h=20) ---")
    for r in b_rows:
        h = next((x for x in r["irf"] if x["h"] == HORIZON), None)
        pp = r["placebo"]["percentile"] if r["placebo"] else "—"
        print(f"  {r['shock']:20s} n={r['n_events']:3d}  beta {h['beta']:+.3f} "
              f"[{h['lo95']:+.3f}, {h['hi95']:+.3f}]  placebo {pp}  {r['verdict']}")
    print(f"\nSTATUS OF severity_dose_response: {payload['verdict']}")
    print("(data/edge_battery.json not edited; reported for the owning session)")
    conn.close()


if __name__ == "__main__":
    main()
