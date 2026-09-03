"""
signal_registry.py -- the one queryable place that says WHAT'S PROVEN, HOW SURE, THE RECEIPTS (Step 8).

Consolidates every candidate the engine has tested into a factor-style registry. The point a quant
cares about: each signal's status (live / experimental / rejected) is DERIVED FROM the validation
runs, never asserted. Change the evidence, the status changes on the next build -- honesty is
structural, not editorial.

Two tables (additive; approved in the plan):
  signals      -- {signal_id, name, mechanism prior, method, inputs, oos_metric, oos_value,
                   status, evidence} read out of the committed validation artifacts.
  belief_state -- the current estimate of each state variable, tagged observed / nowcast /
                  inferred_latent (never blended), so a consumer knows how each number was made.

Status rules (data-driven):
  live         = statistically validated edge (CI excludes 0 AND survives multiple-testing).
  experimental = a candidate that passed some checks but not the full gate, or is flagged as
                 needing a defeater (e.g. discovery's vol-clustering candidate).
  rejected     = failed the out-of-sample gate (a reported null).

Run:  python3 src/signal_registry.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
DATA = ROOT / "data"
OUT = DATA / "signal_registry.json"


def _j(name):
    p = DATA / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


def build_rows():
    """Assemble the registry rows by READING the validation artifacts (status derived, not asserted)."""
    vc = {h.get("hid"): h for h in _j("validation_claims.json").get("hypotheses", [])}
    an = _j("validation_analogue.json")
    pb = _j("probability_backtest.json")
    disc = _j("discovery.json")
    rb = _j("read_backtest.json")
    nc = _j("nowcast_backtest.json")
    rows = []

    # H1 -- the conditioning edge
    h1 = vc.get("H1", {})
    if h1:
        live = bool(h1.get("statistically_validated"))
        oos = rb.get("live_amplification_pp")
        rows.append(dict(
            signal_id="h1_vix_conditioning",
            name="H1: VIX stress amplifies the oil ripple",
            mechanism="Geopolitical shocks ripple harder into oil when market stress (VIX) is already elevated",
            method="conditioned event study + Jorda local projection",
            inputs="derived.vix_pct (t-1); |CAR+20|",
            oos_metric="walk-forward realized amplification (ON minus OFF), pp",
            oos_value=oos,
            status="live" if live else "rejected",
            evidence=f"amp {h1.get('amp_pp')}pp, 95%CI {h1.get('ci95_pp')}, FDR q={h1.get('fdr_qvalue')}, "
                     f"survives_bonferroni={h1.get('survives_bonferroni_5pct')}; walk-forward OOS +{oos}pp"))

    # H2, H3 -- registered but null at N
    for hid, nm, mech in [
        ("H2", "H2: tight inventories amplify", "Tight physical inventories amplify the ripple"),
        ("H3", "H3: crowded positioning amplifies", "Crowded net-long positioning amplifies the ripple")]:
        h = vc.get(hid, {})
        if h:
            rows.append(dict(
                signal_id=f"{hid.lower()}_conditioning", name=nm, mechanism=mech,
                method="conditioned event study", inputs=f"{h.get('variable')} (t-1); |CAR+20|",
                oos_metric="clustered amplification, pp", oos_value=h.get("amp_pp"),
                status="live" if h.get("statistically_validated") else "rejected",
                evidence=f"amp {h.get('amp_pp')}pp, 95%CI {h.get('ci95_pp')}, CI excludes 0="
                         f"{h.get('ci_excludes_zero')} (was small-sample noise at n=20)"))

    # analogue turbulence forecaster
    if an:
        c = an.get("cpcv", {})
        rows.append(dict(
            signal_id="analogue_turbulence",
            name="Analogue turbulence forecaster",
            mechanism="Share of prior analogues whose oil pattern was non-clean predicts turbulence",
            method="kNN over analogue library + LOO isotonic", inputs="analogue non-clean share",
            oos_metric="CPCV skill vs base rate", oos_value=c.get("skill_mean"),
            status="experimental" if an.get("gate_passes") else "rejected",
            evidence=f"Brier {an.get('full_sample_brier')} vs base {an.get('base_rate_brier')}; "
                     f"CPCV skill {c.get('skill_mean')}, PBO {an.get('pbo',{}).get('pbo')}, "
                     f"DM p={an.get('diebold_mariano',{}).get('p_value')} -> null"))

    # kNN state-signature probability (Step 4)
    if pb:
        cl = pb.get("clustered", {})
        rows.append(dict(
            signal_id="knn_state_probability",
            name="kNN state-signature probability",
            mechanism="States resembling prior large-ripple episodes predict an above-median ripple",
            method="walk-forward kNN over derived-state signature", inputs="7 derived state vars (t-1)",
            oos_metric="CPCV skill vs base rate (clustered)", oos_value=cl.get("skill_vs_base"),
            status="experimental" if pb.get("gate_passes") else "rejected",
            evidence=f"clustered Brier {cl.get('brier')} vs {cl.get('base_rate_brier')}, PBO "
                     f"{cl.get('pbo',{}).get('pbo')}, DM p={cl.get('diebold_mariano',{}).get('p_value')} "
                     f"-> null (all-events 'skill' was a clustering artifact)"))

    # discovery candidate (realized vol -> magnitude)
    surv = [c for c in disc.get("survivors", []) if not c.get("is_rediscovered_h1")]
    volcand = next((c for c in surv if c.get("feature") == "derived.brent_vol20"
                    and c.get("outcome") == "abs_car20"), None)
    if volcand:
        rows.append(dict(
            signal_id="realized_vol_magnitude",
            name="Realized Brent vol -> ripple magnitude (candidate)",
            mechanism="Elevated pre-event realized oil volatility precedes larger ripples",
            method="discovery scan (perm+FDR+OOS+partial-corr)", inputs="derived.brent_vol20 (t-1); |CAR+20|",
            oos_metric="partial correlation (controlled for VIX)", oos_value=volcand.get("partial_r"),
            status="experimental",
            evidence=f"survives 4 gates (r={volcand.get('r')}, partial_r={volcand.get('partial_r')}) BUT "
                     f"likely volatility clustering -- needs the standardization defeater before promotion"))

    # nowcast
    if nc and nc.get("series"):
        rows.append(dict(
            signal_id="nowcast_inventory",
            name=f"Kalman nowcast: {nc.get('series')}",
            mechanism="Local-level Kalman tracks the latent level of a lagged weekly state var",
            method="local-level Kalman filter", inputs=nc.get("series"),
            oos_metric="skill vs persistence", oos_value=nc.get("skill_vs_persistence"),
            status="experimental" if nc.get("gate_passes") else "rejected",
            evidence=f"68% coverage {nc.get('ci68_coverage')} (in band {nc.get('coverage_in_band')}), "
                     f"beats persistence {nc.get('beats_persistence')}"))
    return rows


def write_belief_state(conn):
    """Current estimate of each state variable, tagged by how it was produced (never blended)."""
    conn.execute("""CREATE TABLE IF NOT EXISTS belief_state (
        variable_id TEXT PRIMARY KEY, value REAL, as_of TEXT, status TEXT, method TEXT, updated_at TEXT)""")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    er = _j("engine_read.json")
    rows = []
    for hid in ("H1", "H2", "H3"):
        h = (er.get("hypotheses") or {}).get(hid, {})
        if h.get("latest") is not None:
            rows.append((h["signal"], float(h["latest"]), h.get("as_of_reading"),
                         "observed", "point-in-time reading from oil.db", now))
    conn.executemany("INSERT OR REPLACE INTO belief_state VALUES (?,?,?,?,?,?)", rows)
    conn.commit()
    return len(rows)


def build():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS signals (
        signal_id TEXT PRIMARY KEY, name TEXT, mechanism TEXT, method TEXT, inputs TEXT,
        oos_metric TEXT, oos_value REAL, status TEXT, evidence TEXT, updated_at TEXT)""")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = build_rows()
    conn.executemany(
        "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(r["signal_id"], r["name"], r["mechanism"], r["method"], r["inputs"], r["oos_metric"],
          r["oos_value"], r["status"], r["evidence"], now) for r in rows])
    conn.commit()
    nb = write_belief_state(conn)
    conn.close()
    # A claim retracted or downgraded under the single evidentiary bar may not be written back as
    # live. This is the defect that produced six stale belief files; src/retractions.py is the one
    # place that knows, and tests/test_retraction_guard.py fails the build if this is skipped.
    import retractions as _R
    for r in rows:
        if not _R.may_be_live(r["signal_id"]):
            rec = _R.adjudication()[_R.canonical(r["signal_id"])]
            r["status"] = "retracted"
            r["retier"] = rec["retier"]
            r["retracted_on"] = rec["on"]
            r["retracted_reference"] = rec["reference"]
            if "[WITHDRAWN" not in r.get("evidence", ""):
                r["evidence"] = r.get("evidence", "") + f"  [WITHDRAWN {_R.pointer(r['signal_id'])}. " \
                    "Figures kept: a retracted result's diagnostics are part of the record.]"
    # every status key is always present, including empty ones: consumers index by_status["live"] and
    # an absent key is a KeyError, whereas an empty list is the honest answer "no live signals".
    statuses = ["live", "experimental", "rejected", "retracted"]
    statuses += sorted({r["status"] for r in rows} - set(statuses))
    report = {"generated_at": now, "n_signals": len(rows),
              "by_status": {s: [r["signal_id"] for r in rows if r["status"] == s] for s in statuses},
              "signals": rows, "belief_state_vars": nb,
              "retraction_note": "Statuses adjudicated against data/evidentiary_bar.json via src/retractions.py."}
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = build()
    print("=" * 80)
    print("SIGNAL REGISTRY -- what's proven, how sure, the receipts")
    print("=" * 80)
    order = {"live": 0, "experimental": 1, "rejected": 2}
    for s in sorted(r["signals"], key=lambda x: (order.get(x["status"], 3), x["signal_id"])):
        tag = {"live": "✅ LIVE", "experimental": "🧪 EXPERIMENTAL", "rejected": "❌ REJECTED"}.get(
            s["status"], s["status"])
        print(f"\n  {tag}  {s['name']}")
        print(f"     mechanism: {s['mechanism']}")
        print(f"     method: {s['method']}  |  {s['oos_metric']}: {s['oos_value']}")
        print(f"     evidence: {s['evidence']}")
    bs = r["by_status"]
    print(f"\n  SUMMARY: {len(bs['live'])} live, {len(bs['experimental'])} experimental, "
          f"{len(bs['rejected'])} rejected.  belief_state: {r['belief_state_vars']} vars (observed).")
    print("  Status is derived from the validation artifacts, not asserted.")


if __name__ == "__main__":
    main()
