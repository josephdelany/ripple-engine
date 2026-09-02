"""
evidence.py -- claim-addressable receipts (every number one hop from its rows + CI + sources + commit).

The "an Ergo quant can inspect it" substrate: for every validated claim the engine surfaces, emit a
pack at data/evidence/<claim_id>.json carrying the EXACT underlying episodes (re-derived by the same
functions that made the claim -- no drift), the statistics (CI + p + FDR + robustness), the source
artifact, and TWO commit hashes (the artifact + oil.db) so the number is reproducible. EVIDENCE.md
indexes them; the MCP get_evidence_pack tool serves them read-only.

Claims covered: the registered H1 edge, the cross-asset ripple nodes, and the battery's conditioned
edges (copper_growth, hy_credit_stress, ...). Post red-team-1 (R7) each of these is re-tiered
SUGGESTIVE by the integrity guard in build_all (the validated set is empty under the one bar,
EVALUATION.md §0); packs are retained to publish the downgrade with receipts. Nulls are reported
elsewhere, not here.

Run:  python3 src/evidence.py
"""

import json
import subprocess
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

import research
import validate
import tiers
from robustness import assign_clusters

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
EVID = DATA / "evidence"
INDEX = ROOT / "EVIDENCE.md"


def git_hash(path):
    try:
        out = subprocess.check_output(["git", "-C", str(ROOT), "log", "-1", "--format=%h", "--", str(path)],
                                      stderr=subprocess.DEVNULL).decode().strip()
        return out or "uncommitted"
    except Exception:
        return "uncommitted"


def _rj(name):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else {}


def _episodes(conn, state_sid, asset_series, horizon=20):
    """The EXACT clustered episodes behind an amplification claim, with sources -- reusing the same
    research functions the claim was built from (so the rows can't drift from the number)."""
    events = research._events(conn)
    url = {r["event_id"]: r["source_url"] for _, r in events.iterrows()}
    asset = research._asset(asset_series)
    state = research._state_series(conn, state_sid)
    mags = research._car_mags(conn, asset, events, horizon)
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] not in mags:
            continue
        v = state.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))
        if pd.notna(v):
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                         "mag": mags[ev["event_id"]], "state": float(v),
                         "title": ev["title"], "source_url": url.get(ev["event_id"], "")})
    if len(rows) < 12:
        return []
    df = assign_clusters(pd.DataFrame(rows))
    return df.groupby("cluster").first().reset_index().to_dict("records")


def _pack(claim_id, tier, statement, quantity, stats, source_artifact, episodes, mechanism=""):
    return {"claim_id": claim_id, "tier": tier, "statement": statement, "quantity": quantity,
            "mechanism": mechanism,
            "method": "conditioned constant-mean event study; clustered median split; cluster-bootstrap "
                      "95% CI; 10k-permutation p; family-wise FDR+Bonferroni where applicable; "
                      "leave-one-cluster-out robustness. Point-in-time (state read at t-1).",
            "statistics": stats,
            "underlying_episodes": [{"event_id": e["event_id"], "date": e["date"],
                                     "car20_or_state": {"|CAR|": round(float(e["mag"]), 3),
                                                        "state_t_minus_1": round(float(e["state"]), 3)},
                                     "title": e.get("title", ""), "source_url": e.get("source_url", "")}
                                    for e in episodes],
            "n_episodes": len(episodes),
            "source_artifact": source_artifact,
            "source_commit": git_hash(DATA / source_artifact),
            "db_commit": git_hash(DB) if git_hash(DB) != "uncommitted" else "uncommitted (oil.db is gitignored; rebuild via repro.sh)",
            "repro_command": f"./repro.sh && python3 src/edge_battery.py   # then read data/{source_artifact}"}


def build_all():
    conn = sqlite3.connect(DB)
    EVID.mkdir(parents=True, exist_ok=True)
    packs = []

    # H1 (registered)
    vc = _rj("validation_claims.json")
    h1 = next((h for h in vc.get("hypotheses", []) if h.get("hid") == "H1"), None)
    if h1:
        eps = _episodes(conn, "derived.vix_pct", "fred.DCOILBRENTEU", 20)
        packs.append(_pack("hyp.H1", "validated",
                           "Geopolitical shocks ripple harder into Brent oil when VIX stress is elevated.",
                           {"value": h1.get("amp_pp"), "unit": "pp", "metric": "|CAR+20| high-minus-low amplification"},
                           {"n_episodes": len(eps), "ci95": h1.get("ci95_pp"),
                            "survives_fdr": h1.get("survives_fdr_10pct"),
                            "survives_bonferroni": h1.get("survives_bonferroni_5pct")},
                           "validation_claims.json", eps, "stress transmits shocks harder"))

    retracted_packs = RETRACTED_RECORD                     # Joe's Ruling 1: claims not emitted, recorded instead
    retracted_packs.clear()
    # validated cross-asset ripple nodes (map cells key by label -> resolve to series via ASSETS)
    from cross_asset import ASSETS
    label2series = {a["label"]: a["series"] for a in ASSETS}
    from propagation_graph import RETRACTED_EDGE_IDS, RETRACTED_POINTER      # Joe's Ruling 1, 2026-09-02
    retracted_labels = {e.split(".", 1)[1] for e in RETRACTED_EDGE_IDS}
    for c in _rj("cross_asset_conditioned.json").get("map", []):
        if c["label"] == "Palladium":
            # Joe's Ruling 1: palladium does NOT generalize here (CI covers zero) and so emits no claim, but
            # session C's re-test retained it. Record that as computed, with the reasons it is not a finding, so
            # the stale card on disk cannot keep asserting a claim.
            (EVID / "node.palladium.json").write_text(json.dumps({
                "claim_id": "node.palladium", "tier": "NOT_A_FINDING",
                "statement": "Palladium's re-test result, recorded as computed. This is NOT a finding and is not "
                             "to be surfaced on any page, in any export, or in the paper.",
                "quantity": {"value": c.get("amp"), "unit": c.get("unit", ""), "metric": "|CAR+20| amplification (this sample)"},
                "statistics": {"n_episodes": c.get("n_episodes"), "ci95": c.get("ci95"), "generalizes": False,
                               "re_test": "-5.807% [-10.663, -0.951] n=22, placebo pct 0.0, verdict TRANSMITTING "
                                          "(data/ripple/retraction_six.json, RIPPLE_REGISTRATION.md Amendment B)"},
                "not_a_finding": {"ruling": "data/gates/ripple_2026-09-02.md Ruling 1 (Joe, 2026-09-02)",
                                  "reasons": ["its propagation_edges row was already null and does not gain status here",
                                              "palladium is not on the oil chain",
                                              "one survivor of six at this base rate is what noise looks like (~26% chance of >=1 at a 5% threshold under a complete null)",
                                              "the re-test's sign (-5.81%) is opposite to this sample's (+5.14%)"]},
                "n_episodes": c.get("n_episodes")}, indent=2, default=str))
            continue
        if not c.get("generalizes"):
            continue
        if c["label"] in retracted_labels:
            # EDGE_PORTFOLIO.md amendment 2026-09-02: this node's amplification edge was retracted. No CLAIM card
            # is emitted; a RETRACTION card is written to the same path so no stale claim can be served by
            # get_pack()/the MCP tool. The computed numbers stay here and on the propagation_edges row.
            cid = f"node.{c['label'].lower().replace(' ', '_')}"
            retracted_packs.append({"claim_id": cid, "label": c["label"], "amp": c.get("amp"),
                                    "ci95": c.get("ci95"), "note": RETRACTED_POINTER})
            (EVID / f"{cid}.json").write_text(json.dumps({
                "claim_id": cid, "tier": "RETRACTED", "statement":
                    f"RETRACTED 2026-09-02 (Joe's Ruling 1). This card previously claimed that a shock ripples "
                    f"harder into {c['label']} when VIX stress is elevated. Session C's registered re-test "
                    f"(all-event shock on VIX >= median days, h=20, vs the VIX-and-GPR-matched placebo) returns "
                    f"NULL: the band covers zero. The claim is withdrawn; the numbers below are kept as computed.",
                "quantity": {"value": c.get("amp"), "unit": c.get("unit", ""), "metric": "|CAR+20| amplification (as computed, superseded)"},
                "statistics": {"n_episodes": c.get("n_episodes"), "ci95": c.get("ci95"), "perm_p": c.get("perm_p")},
                "retraction": {"ruling": "data/gates/ripple_2026-09-02.md Ruling 1 (Joe, 2026-09-02)",
                               "amendment": "EDGE_PORTFOLIO.md amendment 2026-09-02",
                               "re_test": "data/ripple/retraction_six.json", "red_team": "docs/red_team_1.md",
                               "edge_status": "retracted_h1_retest"},
                "n_episodes": c.get("n_episodes")}, indent=2, default=str))
            continue
        eps = _episodes(conn, "derived.vix_pct", label2series.get(c["label"], ""), 20)
        packs.append(_pack(f"node.{c['label'].lower().replace(' ', '_')}", "validated",
                           f"A shock ripples harder into {c['label']} when VIX stress is elevated.",
                           {"value": c["amp"], "unit": c.get("unit", ""), "metric": "|CAR+20| amplification"},
                           {"n_episodes": c.get("n_episodes"), "ci95": c.get("ci95"),
                            "perm_p": c.get("perm_p"), "survives_fdr": c.get("survives_fdr")},
                           "cross_asset_conditioned.json", eps, "H1 generalization"))

    # battery validated conditioned edges
    for x in _rj("edge_battery.json").get("amplification", []):
        if not x.get("validated") or not x.get("state"):
            continue
        eps = _episodes(conn, x["state"], x["asset"], 20)
        packs.append(_pack(f"edge.{x['hypothesis']}", "validated",
                           f"{x['hypothesis']}: {x.get('mechanism', '')}",
                           {"value": x["amp"], "unit": x.get("unit", ""), "metric": "|CAR+20| amplification"},
                           {"n_episodes": x.get("n"), "ci95": x.get("ci"), "perm_p": x.get("perm_p"),
                            "fdr_q": x.get("fdr_q"), "survives_fdr": x.get("survives_fdr"),
                            "robustness": x.get("robustness")},
                           "edge_battery.json", eps, x.get("mechanism", "")))

    # V3 cross-chain validated edges (a SEPARATE pre-registered family; its own test + method).
    _CC_META = {
        "CC2_supply_gasoline_crack": ("Physical supply-shock events widen the gasoline crack over +10 "
                                      "trading days.", "refined product tightens faster than crude",
                                      "signed CAR+10 (crack change, $/bbl)"),
        "CC5_fertilizer_corn": ("Fertilizer prices transmit to corn prices (monthly pass-through).",
                                "fertilizer cost lifts crop prices", "monthly pass-through beta"),
    }
    for r in _rj("cross_chain.json").get("results", []):
        if not r.get("validated"):
            continue
        stmt, mech, metric = _CC_META.get(r["id"], (r["id"], "", "cross-chain effect"))
        packs.append({
            "claim_id": f"edge.{r['id']}", "tier": "validated", "statement": stmt, "mechanism": mech,
            "quantity": {"value": r["signed_amp"], "unit": r.get("unit", ""), "metric": metric},
            "method": "pre-registered cross-chain test (PRE_REGISTRATION.md amendment 2026-08-03): signed "
                      "constant-mean event study (crack) or monthly pass-through regression (food); 95% "
                      "bootstrap CI; sign-flip/permutation p; family-wise BH-FDR q=0.10 + Bonferroni; "
                      "placebo-controlled (shuffled dates -> null). Directions fixed BEFORE results.",
            "statistics": {"n": r["n"], "ci95": r["ci"], "perm_p_raw": r["perm_p"],
                           "survives_fdr": r.get("survives_fdr"),
                           "survives_bonferroni": r.get("survives_bonferroni"),
                           "predicted_direction": r.get("predicted_sign")},
            # event-based edges (cracks) carry their clustered event episodes (event_id + source);
            # node-to-node passthrough edges (food) have no discrete events -> 0 episodes, n is in stats.
            "underlying_episodes": [{"event_id": e["event_id"], "date": e["date"],
                                     "source_url": e["source_url"], "car": e["car"]}
                                    for e in r.get("episodes", [])],
            "n_episodes": len(r.get("episodes", [])), "source_artifact": "cross_chain.json",
            "source_commit": git_hash(DATA / "cross_chain.json"),
            "db_commit": git_hash(DB) if git_hash(DB) != "uncommitted" else "uncommitted (rebuild via repro.sh)",
            "repro_command": "./repro.sh && python3 src/cross_chain.py   # then read data/cross_chain.json"})
    corpus_n = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    conn.close()

    # RED-TEAM-1 (R7) INTEGRITY GUARD. Under the single evidentiary bar (EVALUATION.md §0:
    # SAR-standardized + regime-block-robust CI excluding zero + permutation-FDR) NO amplification
    # claim is certified `validated` -- the validated set is empty. So no regenerated pack may be
    # emitted as `validated`; every claim pack floors at SUGGESTIVE until it is SAR-certified.
    # (The hand-curated packs already carry the per-claim SAR numbers + tier_status; this guard is
    # the durable floor so a plain regen can never silently re-validate a downgraded claim.)
    RETIER_STATUS = ("Re-tiered SUGGESTIVE under the red-team-1 evidentiary bar (EVALUATION.md §0). "
                     "Not certified `validated`: requires a SAR-standardized, regime-block-robust "
                     "(drop 2008/2020/2026/all) bootstrap CI excluding zero + permutation-FDR. "
                     "Receipts: docs/red_team_1.md, data/evidentiary_bar.json, data/NUMBERS.md.")
    for p in packs:
        if p.get("tier") == "validated":
            p["tier"] = "SUGGESTIVE"
            p.setdefault("tier_status", RETIER_STATUS)

    # F1: mark every pack with the CURRENT-SAMPLE corpus version. The registered study is FROZEN at
    # its own N (see PRE_REGISTRATION.md / EDGE_PORTFOLIO.md); these packs are the live post-sweep read.
    corpus_marker = {"n_events": corpus_n,
                     "note": "CURRENT post-sweep sample. The REGISTERED study is frozen separately "
                             "(PRE_REGISTRATION.md, n=20 / N=289) and is never recomputed; these packs "
                             "track the growing corpus, versioned by n_events."}
    for p in packs:
        p["corpus"] = corpus_marker
        (EVID / f"{p['claim_id']}.json").write_text(json.dumps(p, indent=2, default=str))
    _write_index(packs, RETRACTED_RECORD)
    return packs


RETRACTED_RECORD = []                                      # filled by build_all: nodes whose claim card is withheld


def _write_index(packs, retracted=()):
    L = ["# EVIDENCE — every claim, one hop from its receipt", "",
         "Each validated claim below has a machine pack at `data/evidence/<claim_id>.json` with its exact "
         "underlying episodes (event ids + dates + source URLs), CI, method, and commit hashes. "
         "Regenerated by `src/evidence.py`. Post red-team-1 these claims are **SUGGESTIVE** (the "
         "validated set is empty under the one bar, `EVALUATION.md` §0); packs are kept to publish the "
         "downgrade with receipts. Nulls are reported in `EDGE_PORTFOLIO.md` / `evaluation.json`.", "",
         "| claim_id | tier | quantity | n | receipt |", "|---|---|---|---|---|"]
    for p in sorted(packs, key=lambda z: z["claim_id"]):
        q = p["quantity"]
        L.append(f"| `{p['claim_id']}` | {tiers.BADGE.get(p['tier'], p['tier'])} | "
                 f"{q.get('value')}{q.get('unit', '')} | {p['n_episodes']} | "
                 f"`data/evidence/{p['claim_id']}.json` |")
    if retracted:
        L += ["", "## Retracted 2026-09-02 (Joe's Ruling 1) — no claim card is emitted for these",
              "", "| node | amplification as computed | 95% CI | status |", "|---|---|---|---|"]
        for r in sorted(retracted, key=lambda z: z["label"]):
            ci = r.get("ci95") or [None, None]
            L.append(f"| {r['label']} | {r.get('amp')} | "
                     f"{('[%s, %s]' % (ci[0], ci[1])) if ci and ci[0] is not None else 'n/a'} | "
                     f"`retracted_h1_retest` — {r['note']} |")
        L += ["", "The numbers stay in `data/cross_asset_conditioned.json` and on the `propagation_edges` row; "
              "what is withdrawn is the claim, per `EDGE_PORTFOLIO.md` (amendment 2026-09-02)."]
    L += ["", f"*{len(packs)} claims. Every number is reproducible: `./repro.sh` rebuilds `oil.db` from "
          "zero, then the producer script regenerates the artifact.*"]
    INDEX.write_text("\n".join(L))


def get_pack(claim_id):
    """Read one committed pack (for the MCP tool). Whitelisted by existence; no arbitrary reads."""
    p = EVID / f"{claim_id}.json"
    return json.loads(p.read_text()) if p.exists() else {"error": f"no evidence pack '{claim_id}'"}


def list_claims():
    return sorted(p.stem for p in EVID.glob("*.json"))


def main():
    packs = build_all()
    print(f"evidence: wrote {len(packs)} claim packs to data/evidence/ + EVIDENCE.md")
    for p in packs:
        print(f"  {p['claim_id']:<28} {p['quantity'].get('value')}{p['quantity'].get('unit','')}"
              f"  n={p['n_episodes']}  artifact@{p['source_commit']}")


if __name__ == "__main__":
    main()
