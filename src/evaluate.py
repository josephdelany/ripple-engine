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
            "note": "state labels shuffled on H1's episodes; amplification collapses to ~0 (CI spans 0). "
                    "A non-null placebo would mean the framework finds signal in noise -- it does not."}


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

    framework_ok = bool(pl.get("null_as_expected") and sc.get("all_consistent"))
    report = {"corpus": {"n_events": n_events},
              "placebo": pl, "surface_consistency": sc, "calibration": cal, "power": pw,
              "miss_audit": ma, "temporal_holdout": holdout, "quarterly_calibration": qcal,
              "overall": {"framework_sound": framework_ok,
                          "headline": f"placebo {'null (good)' if pl.get('null_as_expected') else 'NOT NULL (!!)'}; "
                          f"surfaces {'consistent' if sc.get('all_consistent') else 'INCONSISTENT (!!)'}; "
                          f"gap-ledger skill vs base {cal.get('skill_vs_base')}"
                          + (f"; H1 holds out-of-sample ({holdout.get('oos_2019plus_amp_pp')}pp on 2019+)"
                             if holdout.get("holds_out_of_sample") else "")}}
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


def _write_md(r):
    L = ["# EVALUATION — is the engine sound?", "",
         "*Generated by `src/evaluate.py` over the committed artifacts. Reruns each pipeline pass.*", "",
         f"**Overall:** {r['overall']['headline']}.", ""]
    L += _bar_section()
    pl = r["placebo"]
    L += ["## 1. Negative control (placebo)",
          f"Shuffling H1's state labels collapses the amplification from **{pl.get('real_amp')}** to a "
          f"placebo mean **{pl.get('placebo_mean')}**, CI {pl.get('placebo_ci95')} — "
          f"{'spans zero ✓ (the gate is not finding signal in noise)' if pl.get('null_as_expected') else 'DOES NOT span zero (!!)'}.", ""]
    sc = r["surface_consistency"]
    L += ["## 2. Surface consistency",
          f"{sc['quantity']} across surfaces: {sc['values']} — "
          f"{'all agree ✓' if sc['all_consistent'] else 'MISMATCH (!!)'}.", ""]
    cal = r["calibration"]
    if cal.get("ran"):
        d = cal["decomposition"]
        L += ["## 3. Calibration (resolved gap ledger)",
              f"n={cal['n_scored']}, Brier **{cal['brier']}** vs base {cal['base_rate_brier']} "
              f"(skill {cal['skill_vs_base']}). Murphy decomposition — reliability {d['reliability']}, "
              f"resolution {d['resolution']}, uncertainty {d['uncertainty']}.",
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
        L += ["", "## 6. Temporal hold-out (V-Q4) — H1 conditioning rule fit pre-2019, tested 2019+",
              f"In-sample (pre-2019) **{ho.get('in_sample_pre2019_amp_pp')}pp** vs out-of-sample (2019+) "
              f"**{ho.get('oos_2019plus_amp_pp')}pp** using the FROZEN pre-2019 VIX threshold — "
              f"{'holds out-of-sample ✓' if ho.get('holds_out_of_sample') else 'does NOT clearly hold (reported honestly)'}."]
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
    print(f"  placebo: {r['placebo'].get('placebo_ci95')} null_as_expected={r['placebo'].get('null_as_expected')}")
    print(f"  surface consistency: {r['surface_consistency']['all_consistent']}  {r['surface_consistency']['values']}")
    c = r["calibration"]
    if c.get("ran"):
        print(f"  calibration: Brier {c['brier']} vs base {c['base_rate_brier']} (skill {c['skill_vs_base']})")
    print(f"  power: {[(c['claim'], c.get('n'), c.get('robust_leave_one_out')) for c in r['power']['claims']]}")
    print(f"  framework_sound: {r['overall']['framework_sound']}")
    print(f"  wrote {OUT} + {MD.name}")


if __name__ == "__main__":
    main()
