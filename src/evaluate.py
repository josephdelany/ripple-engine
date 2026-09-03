"""
evaluate.py -- the comprehensive self-evaluation (prove the engine is sound, many ways).

Runs standard soundness checks over the ALREADY-COMMITTED artifacts + validated claims, using only
validate.py primitives (numpy; nulls stay nulls; no new modelling). Writes data/evaluation.json +
EVALUATION.md. This is the "an Ergo quant can inspect it" centrepiece:

  1. NEGATIVE CONTROL / PLACEBO -- shuffle the state labels on H1's episodes; the amplification MUST
     collapse to ~0 with a CI spanning zero. If a placebo "passes", the whole gate is suspect.
  2. SURFACE CONSISTENCY -- the same headline number (H1 amp) must be identical across every artifact
     (validation_claims, cross_asset_conditioned, sowhat). No surface may drift from another.
  3. CALIBRATION -- from the resolved gap ledger: reliability by forecast bin (Wilson CIs) + the Murphy
     Brier decomposition (Brier = Reliability - Resolution + Uncertainty) -- the honest read on skill.
  4. POWER / ROBUSTNESS -- each validated claim's n + leave-one-cluster-out sign stability.
  5. MISS-AUDIT -- the worst-scored resolved gaps, with a root-cause bucket (learn from the misses).

Run:  python3 src/evaluate.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np

import validate
import edge_battery
from robustness import assign_clusters   # noqa: F401  (kept for parity with the study modules)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
OUT = DATA / "evaluation.json"
MD = ROOT / "EVALUATION.md"
SEED = 19900802


def _rj(name):
    p = DATA / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


# ---------------------------------------------------------------- 0. the REGISTERED gates
# This module used to answer "is the engine sound?" from its own checks. Two of them were not the
# gates this repository registers, and both said the opposite of the registered answer:
#   * its placebo shuffles H1's VIX state labels and passes if the CI spans zero. The REGISTERED
#     placebo is WALK_FORWARD_PROTOCOL §6, published at summary.json#/placebo, and its null_holds
#     is FALSE. EVALUATION.md said "placebo null (good)" at the repo root while the registered
#     placebo was failing.
#   * its temporal hold-out reported "H1 holds out-of-sample". H1 was DOWNGRADED under the single
#     evidentiary bar (docs/red_team_1.md R7; data/evidentiary_bar.json) -- legs 2 and 3 fail -- and
#     is one of the project's published retractions.
# The verdict now comes from those two files. The module's own checks remain, as DIAGNOSTICS,
# labelled as unregistered and gating nothing. A diagnostic that disagrees with a registered gate
# is a fact about the diagnostic.

def _r(x, nd=4):
    """Round for a document a human reads; None stays None. Never rounds anything that is gated on."""
    return None if x is None else round(float(x), nd)


def registered_gates():
    """The gates this repository actually registers, read from their own published files.
    Never this module's own arithmetic. A missing file is reported as unavailable, never as a pass."""
    out = {}
    try:
        s = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
        pl = s.get("placebo") or {}
        out["placebo"] = {"source": "data/walk_forward/summary.json#/placebo",
                          "registration": "WALK_FORWARD_PROTOCOL.md §6",
                          "run_id": s.get("run_id"), "null_holds": pl.get("null_holds"),
                          "skill": _r(pl.get("skill")), "ci95": [_r(x) for x in (pl.get("ci95") or [])],
                          "dm_p": _r(pl.get("dm_p")),
                          "estimator": pl.get("estimator"), "null_reference": pl.get("null_reference")}
    except Exception as ex:
        out["placebo"] = {"unavailable": f"{type(ex).__name__}: {ex}", "null_holds": None}
    try:
        b = json.loads((ROOT / "data" / "evidentiary_bar.json").read_text())
        h1 = (b.get("adjudicated") or {}).get("H1_vix_oil") or {}
        legs = h1.get("legs") or {}
        out["h1"] = {"source": "data/evidentiary_bar.json#/adjudicated/H1_vix_oil",
                     "registration": "docs/red_team_1.md R7 -- the single evidentiary bar",
                     "bar": b.get("bar"), "legs": legs, "retier": h1.get("retier"),
                     "validated": (all(legs.values()) if legs else None)}
    except Exception as ex:
        out["h1"] = {"unavailable": f"{type(ex).__name__}: {ex}", "validated": None}
    return out


def gate_status(g):
    """(sound, headline) from the REGISTERED gates only."""
    pl, h1 = g.get("placebo", {}), g.get("h1", {})
    nh, val = pl.get("null_holds"), h1.get("validated")
    bits = []
    bits.append("registered placebo (protocol §6): " + (
        "null holds" if nh is True else
        f"NULL DOES NOT HOLD -- skill {pl.get('skill')}, CI {pl.get('ci95')}, DM p {pl.get('dm_p')}"
        if nh is False else f"unavailable ({pl.get('unavailable')})"))
    bits.append("H1 under the single evidentiary bar: " + (
        "validated" if val is True else
        f"NOT VALIDATED -- {h1.get('retier')}, legs {h1.get('legs')}" if val is False
        else f"unavailable ({h1.get('unavailable')})"))
    return (nh is True and val is True), "; ".join(bits)


# ---------------------------------------------------------------- 1. placebo / negative control
def placebo(conn):
    m, s = edge_battery._amp_arrays(conn, "derived.vix_pct", "fred.DCOILBRENTEU", 20)
    if m is None:
        return {"ran": False, "reason": "no H1 arrays"}
    obs = validate._directional_amp(m, s, np.median(s), +1)
    rng = np.random.default_rng(SEED)
    shuffled = []
    for _ in range(5000):
        sp = rng.permutation(s)
        a = validate._directional_amp(m, sp, np.median(sp), +1)
        if np.isfinite(a):
            shuffled.append(a)
    lo, hi = np.percentile(shuffled, [2.5, 97.5])
    null_ok = bool(lo <= 0 <= hi)                      # placebo CI must span zero
    return {"ran": True, "real_amp": round(float(obs), 4),
            "placebo_mean": round(float(np.mean(shuffled)), 4),
            "placebo_ci95": [round(float(lo), 4), round(float(hi), 4)],
            "null_as_expected": null_ok,
            "gates": False,
            "note": "DIAGNOSTIC, NOT A GATE. State labels shuffled on H1's episodes -- an unregistered check on a "
                    "hypothesis that has since been downgraded under the single evidentiary bar. The registered "
                    "placebo is WALK_FORWARD_PROTOCOL §6 (summary.json#/placebo); read that for the verdict. This "
                    "figure passing says nothing about whether the registered placebo passes, and it does not."}


# ---------------------------------------------------------------- 2. surface consistency
def surface_consistency():
    vc = _rj("validation_claims.json")
    h1 = next((h for h in vc.get("hypotheses", []) if h.get("hid") == "H1"), {})
    v_claims = h1.get("amp_pp")
    ca = _rj("cross_asset_conditioned.json")
    v_brent = next((c["amp"] for c in ca.get("map", []) if c.get("label") == "Brent oil"), None)
    sw = _rj("sowhat.json")
    v_sowhat = next((e["strength"] for e in sw.get("validated_propagation", [])
                     if e.get("to") == "Brent oil"), None)
    vals = {"validation_claims": v_claims, "cross_asset_conditioned": round(v_brent, 4) if v_brent else None,
            "sowhat": round(v_sowhat, 4) if v_sowhat else None}
    present = [v for v in vals.values() if v is not None]
    consistent = bool(len(present) >= 2 and max(present) - min(present) < 0.01)
    return {"quantity": "H1 amplification (Brent, pp)", "values": vals, "all_consistent": consistent}


# ---------------------------------------------------------------- 3. calibration (Murphy decomposition)
def calibration(conn):
    rows = conn.execute("SELECT engine_p, outcome FROM gaps WHERE outcome IS NOT NULL "
                        "AND engine_p IS NOT NULL").fetchall()
    if not rows:
        return {"ran": False}
    p = np.array([float(a) for a, _ in rows]); y = np.array([float(b) for _, b in rows])
    n = len(y); obar = y.mean()
    brier = float(np.mean((p - y) ** 2))
    base_brier = float(np.mean((obar - y) ** 2))
    bins = []
    rel = res = 0.0
    for pv in sorted(set(p.tolist())):
        mask = p == pv
        nk = int(mask.sum()); ok = float(y[mask].mean())
        w = validate.wilson_ci(int(y[mask].sum()), nk)
        rel += nk / n * (pv - ok) ** 2
        res += nk / n * (ok - obar) ** 2
        bins.append({"forecast_p": round(pv, 3), "n": nk, "observed": round(ok, 3),
                     "observed_ci95": [w["lo"], w["hi"]]})
    unc = float(obar * (1 - obar))
    return {"ran": True, "n_scored": n, "brier": round(brier, 4), "base_rate_brier": round(base_brier, 4),
            "skill_vs_base": round(base_brier - brier, 4),
            "decomposition": {"reliability": round(rel, 4), "resolution": round(res, 4),
                              "uncertainty": round(unc, 4)},
            "reliability_bins": bins,
            "note": "Brier = Reliability - Resolution + Uncertainty. Lower reliability = better "
                    "calibrated; higher resolution = more discriminating. Overall skill vs base is the "
                    "honest headline."}


# ---------------------------------------------------------------- 4. power / robustness of validated claims
def power(conn):
    claims = []
    # H1 (from the registered study) + the battery's validated edges
    eb = _rj("edge_battery.json")
    validated = [(x["hypothesis"], x["state"], x["asset"], x["sign"])
                 for x in eb.get("amplification", []) if x.get("validated") and x.get("state")]
    specs = [("H1", "derived.vix_pct", "fred.DCOILBRENTEU", "high")] + \
            [(name, st, a, sg) for name, st, a, sg in validated]
    seen = set()
    for name, st, a, sg in specs:
        if name in seen:
            continue
        seen.add(name)
        m, s = edge_battery._amp_arrays(conn, st, a, 20)
        if m is None:
            claims.append({"claim": name, "n": None, "note": "arrays unavailable"}); continue
        sign = +1 if sg == "high" else -1
        rob = edge_battery._leave_one_cluster_out(m, s, sign)
        claims.append({"claim": name, "n": int(len(m)), "robust_leave_one_out": rob.get("robust"),
                       "jackknife_amp_range": [rob.get("min"), rob.get("max")]})
    return {"claims": claims,
            "note": "n = clustered episodes; robust = the amplification keeps its predicted sign when "
                    "any single episode is dropped (not driven by one event)."}


# ---------------------------------------------------------------- 5. miss-audit
def miss_audit(conn):
    rows = conn.execute("SELECT gap_id, subject, engine_call, engine_p, outcome, brier, source_url "
                        "FROM gaps WHERE outcome IS NOT NULL AND brier IS NOT NULL "
                        "ORDER BY brier DESC LIMIT 6").fetchall()
    out = []
    for gid, subj, call, p, outcome, brier, url in rows:
        if call == "turbulent" and outcome == 0:
            cause = "regime_misread (engine saw turbulence; calm realised -- vol mean-reverted / priced-in)"
        elif call == "calm" and outcome == 1:
            cause = "surprise_turbulence (engine saw calm; turbulence realised)"
        else:
            cause = "high-loss but directionally consistent"
        out.append({"gap_id": gid, "subject": (subj or "")[:60], "engine_call": call,
                    "outcome": outcome, "brier": round(float(brier), 3), "root_cause": cause,
                    "source_url": url})
    return out


def run():
    conn = sqlite3.connect(DB)
    pl = placebo(conn)
    sc = surface_consistency()
    cal = calibration(conn)
    pw = power(conn)
    ma = miss_audit(conn)
    n_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    conn.close()
    # V-Q4: fold the temporal hold-out + quarterly calibration receipts in as headline lenses
    # (read from their committed JSON; ADDITIVE -- they never affect framework_sound).
    ho = _rj("holdout.json")
    qc = _rj("calibration_report.json")
    holdout = {"holds_out_of_sample": ho.get("holds_out_of_sample"),
               "oos_2019plus_amp_pp": (ho.get("out_of_sample_2019plus") or {}).get("amp_pp"),
               "in_sample_pre2019_amp_pp": (ho.get("in_sample_pre2019") or {}).get("amp_pp")} if ho else {}
    qcal = {"n": (qc.get("overall") or {}).get("n"), "span": qc.get("span"),
            "brier": (qc.get("overall") or {}).get("brier"),
            "skill_vs_base": (qc.get("overall") or {}).get("skill_vs_base"),
            "n_quarters": qc.get("n_quarters")} if qc.get("ran") else {}

    gates = registered_gates()
    gates_ok, gate_line = gate_status(gates)
    framework_ok = bool(gates_ok and sc.get("all_consistent"))
    report = {"corpus": {"n_events": n_events},
              "registered_gates": gates,
              "placebo": pl, "surface_consistency": sc, "calibration": cal, "power": pw,
              "miss_audit": ma, "temporal_holdout": holdout, "quarterly_calibration": qcal,
              "overall": {"framework_sound": framework_ok,
                          "gates_source": "registered files only: WALK_FORWARD_PROTOCOL §6 placebo and the "
                                          "red_team_1 R7 evidentiary bar. This module's own placebo and hold-out "
                                          "are diagnostics and gate nothing.",
                          "headline": gate_line
                          + f"; surfaces {'consistent' if sc.get('all_consistent') else 'INCONSISTENT (!!)'}"
                          + f"; gap-ledger skill vs base {cal.get('skill_vs_base')}"}}
    OUT.write_text(json.dumps(report, indent=2, default=str))
    _write_md(report)
    return report


def _bar_section():
    """The ONE evidentiary bar (red-team-1, R7), codified so every regeneration re-emits it.
    Per-claim adjudication is the machine receipt data/evidentiary_bar.json + the edge packs."""
    L = ["## 0. The evidentiary bar (governing definition — red-team-1, R7)",
         "",
         "A claim is **`validated`** if and only if **all three** hold:",
         "1. **SAR-standardized effect** — the amplification is computed on BMP (1991) standardized "
         "abnormal returns (each event's CAR divided by its own estimation-window σ·√L), not raw |CAR| "
         "(a volatility quantity that inflates in noisy regimes).",
         "2. **Regime-block-robust CI excluding zero** — the 95% cluster-bootstrap CI on the SAR "
         "amplification excludes zero on the full corpus **and** in every regime-block leave-out "
         "(drop 2008 / 2020 / 2026 / all three).",
         "3. **Permutation-FDR** — the SAR permutation-p survives BH-FDR (q=0.10) across the family.",
         "",
         "Applied retroactively (receipt: `data/evidentiary_bar.json`), this bar **downgrades the "
         "entire prior validated set to SUGGESTIVE**:",
         "",
         "| claim | leg 1 SAR | leg 2 regime-robust | leg 3 FDR | re-tier |",
         "|---|---|---|---|---|",
         "| H1 (VIX→oil) | computed | ✗ (null every cut) | ✗ | **SUGGESTIVE** |",
         "| copper_growth | computed | ✗ (drop-2008 CI incl. 0) | ✓ | **SUGGESTIVE** (closest miss) |",
         "| palladium_supply | computed | ✗ (SAR null) | ✗ | **SUGGESTIVE** |",
         "| hy_credit_stress | computed | ✗ (SAR null) | ✗ | **SUGGESTIVE** |",
         "| severity_dose_response | computed | ✗ (SAR null) | ✗ | **SUGGESTIVE** |",
         "| CC2 (gasoline crack) | n/a (event $/bbl) | ✗ (seasonal+outlier CI incl. 0) | — | **SUGGESTIVE** (R6) |",
         "| CC5 (fertilizer→corn) | N/A (monthly β) | — | — | **SUGGESTIVE** (leg-1 N/A) |",
         "| under_priced_risk (mispricing) | — | — | outside family | **SUGGESTIVE** (declared) |",
         "",
         "**The mispricing edge (attack #15), one honest paragraph.** `under_priced_risk_oos` was "
         "reported *alongside* the battery and explicitly **outside** the amplification FDR family. Under "
         "one bar that is not a shield but a statement of estimand: it is a **forecast-skill** test (does "
         "flagged under-priced risk precede realized turbulence?), not an amplification, so it cannot be "
         "folded into the amplification FDR without mixing estimands. It is small-N (~14) and its "
         "direction is fixed in-sample, so it is **SUGGESTIVE — never `validated`** at this N, reported "
         "with a Wilson CI vs base rate. Its exclusion from the FDR family is disclosed here, plainly, "
         "as a property of being a different test — not a way to protect a survivor.",
         "",
         "*Under this bar the current validated set is **empty**; the honest scorecard is SUGGESTIVE "
         "signals + reported nulls. A published downgrade after adversarial review is the finding.*",
         ""]
    return L


def _status_banner(r):
    """The generator emits its own status. Before 2026-09-03 this file asserted "placebo null (good)"
    and "H1 holds out-of-sample" at the repo root while the registered placebo was failing and H1 had
    been downgraded; a banner was added by hand and would have been erased by the next regeneration.
    A machine-generated file has to carry its own verdict, or it lies again on the next pipeline pass."""
    g = r.get("registered_gates") or {}
    pl, h1 = g.get("placebo", {}), g.get("h1", {})
    if r["overall"]["framework_sound"]:
        return []
    L = ["> **THE REGISTERED GATES DO NOT PASS. Read this before any number below.**", ">"]
    if pl.get("null_holds") is False:
        L += [f"> - **The registered placebo fails.** `{pl['source']}` → `null_holds` is **false** "
              f"(skill {pl.get('skill')}, CI {pl.get('ci95')}, DM p {pl.get('dm_p')}; run "
              f"`{pl.get('run_id')}`), registered at {pl.get('registration')}. §1 below shuffles H1's "
              f"state labels and spans zero; that is a **different, unregistered check** and it gates "
              f"nothing.", ">"]
    elif pl.get("null_holds") is None:
        L += [f"> - **The registered placebo could not be read** ({pl.get('unavailable')}). Absence is "
              f"reported as absence, never as a pass.", ">"]
    if h1.get("validated") is False:
        L += [f"> - **H1 is not validated — it is {h1.get('retier')}.** `{h1['source']}` → legs "
              f"{h1.get('legs')} under {h1.get('registration')}. Any H1 figure below (§2 surface "
              f"consistency, §6 hold-out) is a **diagnostic on a downgraded hypothesis**, not a result, "
              f"and none of them re-validates it.", ">"]
    elif h1.get("validated") is None:
        L += [f"> - **The evidentiary bar could not be read** ({h1.get('unavailable')}).", ">"]
    L += ["> For current status read `README.md`, `docs/PAPER_DRAFT.md` and `OPEN_ITEMS.md`.",
          ">",
          "> The frozen record is never edited; this banner is regenerated from the registered files "
          "every time the module runs, so it cannot go stale while the gates stay red. It replaces a "
          "hand-added banner of 2026-09-03, which said the same thing and which the next regeneration "
          "would have erased.", ""]
    return L


def _write_md(r):
    L = ["# EVALUATION — is the engine sound?", ""]
    L += _status_banner(r)
    L += ["*Generated by `src/evaluate.py` over the committed artifacts. Reruns each pipeline pass.*",
          "*Verdict from the registered gates only (protocol §6 placebo; the red_team_1 R7 bar); this "
          "module's own placebo and hold-out are diagnostics and gate nothing.*", "",
          f"**Overall:** {r['overall']['headline']}.", ""]
    L += _bar_section()
    pl = r["placebo"]
    reg = (r.get("registered_gates") or {}).get("placebo", {})
    L += ["## 1. Negative control on H1's state labels — DIAGNOSTIC, NOT THE REGISTERED PLACEBO",
          f"Shuffling H1's state labels collapses the amplification from **{pl.get('real_amp')}** to a "
          f"placebo mean **{pl.get('placebo_mean')}**, CI {pl.get('placebo_ci95')} — "
          f"{'spans zero' if pl.get('null_as_expected') else 'does NOT span zero'}.",
          "",
          f"**This is not the placebo the project gates on.** The registered one is "
          f"{reg.get('registration', 'WALK_FORWARD_PROTOCOL.md §6')} at `{reg.get('source', 'summary.json#/placebo')}`, "
          f"and its `null_holds` is **{reg.get('null_holds')}**"
          + (f" (skill {reg.get('skill')}, CI {reg.get('ci95')})." if reg.get('skill') is not None else ".")
          + " The two ask different questions of different objects; this one passing is not evidence "
            "that the registered one does, and here it does not.", ""]
    sc = r["surface_consistency"]
    L += ["## 2. Surface consistency",
          f"{sc['quantity']} across surfaces: {sc['values']} — "
          f"{'all agree ✓' if sc['all_consistent'] else 'MISMATCH (!!)'}.", ""]
    cal = r["calibration"]
    if cal.get("ran"):
        d = cal["decomposition"]
        L += ["## 3. Calibration (resolved gap ledger)",
              "*Honest and near-baseline: the engine has **no demonstrated forecast edge** — "
              "measuring and grounding, not predicting, is its job (see §0).*",
              f"n={cal['n_scored']}, Brier **{cal['brier']}** vs base {cal['base_rate_brier']} "
              f"(skill {cal['skill_vs_base']} — indistinguishable from zero). Murphy decomposition — "
              f"reliability {d['reliability']}, resolution {d['resolution']}, uncertainty {d['uncertainty']}.",
              "", "| forecast p | n | observed | 95% CI |", "|---|---|---|---|"]
        for b in cal["reliability_bins"]:
            L.append(f"| {b['forecast_p']} | {b['n']} | {b['observed']} | {b['observed_ci95']} |")
        L.append("")
    L += ["## 4. Power / robustness — RAW |CAR| leave-one-out (secondary diagnostic)",
          "*Superseded for tiering by §0. This is the raw-metric jackknife only; under the SAR bar (§0) "
          "these claims are SUGGESTIVE, not validated.*", "",
          "| claim | n | robust (leave-one-out) | jackknife amp range |", "|---|---|---|---|"]
    for c in r["power"]["claims"]:
        L.append(f"| {c['claim']} | {c.get('n')} | {c.get('robust_leave_one_out')} | {c.get('jackknife_amp_range')} |")
    L += ["", "## 5. Miss-audit (worst-scored resolved gaps)", "", "| gap | call | outcome | Brier | root cause |", "|---|---|---|---|---|"]
    for m in r["miss_audit"]:
        L.append(f"| {m['subject']} | {m['engine_call']} | {m['outcome']} | {m['brier']} | {m['root_cause']} |")
    ho, qc = r.get("temporal_holdout") or {}, r.get("quarterly_calibration") or {}
    if ho:
        h1 = (r.get("registered_gates") or {}).get("h1", {})
        L += ["", "## 6. Temporal hold-out (V-Q4) on H1 — DIAGNOSTIC ON A DOWNGRADED HYPOTHESIS",
              f"In-sample (pre-2019) **{ho.get('in_sample_pre2019_amp_pp')}pp** vs out-of-sample (2019+) "
              f"**{ho.get('oos_2019plus_amp_pp')}pp** using the FROZEN pre-2019 VIX threshold.",
              "",
              f"**This does not say H1 holds.** Under the single evidentiary bar "
              f"({h1.get('registration', 'red_team_1 R7')}) H1 is **{h1.get('retier', 'not validated')}** — "
              f"legs {h1.get('legs')} at `{h1.get('source', 'data/evidentiary_bar.json')}`. A split holding "
              f"across one date cut is not the bar, and the bar is what decides. The figures are kept "
              f"because a retracted result's diagnostics are part of the record, not because they revive it."]
    if qc:
        L += ["", "## 7. Quarterly calibration (V-Q4) — the forecast log as a standing OOS test",
              f"Overall n={qc.get('n')} ({qc.get('span')}), Brier **{qc.get('brier')}**, skill vs base "
              f"**{qc.get('skill_vs_base')}** across {qc.get('n_quarters')} quarters. "
              f"Full breakdown in data/calibration_report.txt."]
    L.append("")
    MD.write_text("\n".join(L))


def main():
    r = run()
    print("=" * 78)
    print("EVALUATION — soundness checks")
    print("=" * 78)
    print(f"  REGISTERED gates: {r['overall']['headline']}")
    print(f"  framework_sound (registered only): {r['overall']['framework_sound']}")
    print(f"  [diagnostic] own placebo CI {r['placebo'].get('placebo_ci95')} spans_zero={r['placebo'].get('null_as_expected')} (gates nothing)")
    print(f"  surface consistency: {r['surface_consistency']['all_consistent']}  {r['surface_consistency']['values']}")
    c = r["calibration"]
    if c.get("ran"):
        print(f"  calibration: Brier {c['brier']} vs base {c['base_rate_brier']} (skill {c['skill_vs_base']})")
    print(f"  power: {[(c['claim'], c.get('n'), c.get('robust_leave_one_out')) for c in r['power']['claims']]}")
    print(f"  framework_sound: {r['overall']['framework_sound']}")
    print(f"  wrote {OUT} + {MD.name}")


if __name__ == "__main__":
    main()
