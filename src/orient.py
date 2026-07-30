"""
orient.py -- "what should I pay attention to about <topic> right now?" (read-support, never the read).

Given a topic (or a keyword like "iran"), assemble the engine's relevant RAW MATERIAL in one pull:
the regime, the VALIDATED edges + nulls for that domain, base rates by the domain's event types, the
live market gap, the corroborated live situations with receipts, the coverage gaps (where the engine is
SILENT so you don't over-claim), and a receipts index (every claim -> its evidence pack). Deterministic
assembly of committed artifacts -- no new numbers, NO prose, NO opinion. Joe writes the read from this.

Reuses research.lens_data + sowhat.json + engine_read.json + gaps.json + evidence packs.

Run:  python3 src/orient.py --topic me-risk
"""

import argparse
import json
from pathlib import Path

import research
import tiers

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# fuzzy topic -> domain key (research.DOMAINS). A bare keyword falls back to me-risk/conflict.
ALIASES = {
    "middle east": "me-risk", "mideast": "me-risk", "me": "me-risk", "iran": "me-risk",
    "israel": "me-risk", "hormuz": "me-risk", "gulf": "me-risk", "yemen": "me-risk",
    "oil": "energy", "gas": "energy", "opec": "energy",
    "commodity": "commodities", "metals": "commodities", "copper": "commodities",
    "macro": "macro", "rates": "macro", "fed": "macro", "inflation": "macro",
    "war": "conflict", "ukraine": "conflict", "russia": "conflict",
    "sanction": "geopolitics", "tariff": "geopolitics", "china": "geopolitics",
    "shipping": "supply-chain", "freight": "supply-chain", "port": "supply-chain", "chokepoint": "supply-chain",
}


def _rj(name):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else {}


def _resolve(topic):
    t = (topic or "").strip().lower()
    if t in research.DOMAINS:
        return t
    for k, dom in ALIASES.items():
        if k in t:
            return dom
    return "me-risk"


def orient(topic):
    domain = _resolve(topic)
    lens = research.lens_data(domain)
    if not lens.get("ok"):
        return {"ok": False, "topic": topic, "domains": sorted(research.DOMAINS)}

    er = _rj("engine_read.json")
    regime = (er.get("hypotheses", {}).get("H1", {}) or {}).get("amplifier", "?")
    base_rates = [b for b in er.get("base_rates", [])
                  if b.get("type") in set(research.DOMAINS[domain].get("event_types", []))]
    gaps = _rj("gaps.json")
    live_gap = gaps.get("live_gap")

    # coverage gaps: event types too thin to test, and domain labels with no validated node
    thin = [b["type"] for b in base_rates if (b.get("n") or 0) < tiers.MIN_N]
    validated_labels = {n["node"] for n in lens.get("validated_nodes", [])}
    domain_labels = set(research.DOMAINS[domain].get("labels", []))
    silent_nodes = sorted(domain_labels - validated_labels) if domain_labels else []

    # receipts index: each validated node -> its evidence claim id
    receipts = {n["node"]: f"node.{n['node'].lower().replace(' ', '_')}"
                for n in lens.get("validated_nodes", [])}

    return {"ok": True, "topic": topic, "domain": domain,
            "regime": {"H1_amplifier": regime,
                       "reading": "shocks transmit harder right now" if regime == "ON"
                       else "normal transmission" if regime == "OFF" else "n/a"},
            "validated_edges": [{**n, "tier": "validated"} for n in lens.get("validated_nodes", [])],
            "null_edges": lens.get("null_nodes", []),
            "supply_chain": lens.get("supply_chain", []),
            "base_rates": base_rates,
            "live_gap": live_gap,
            "situations": lens.get("situations", []),
            "gaps_in_coverage": {"underpowered_event_types": thin,
                                 "domain_nodes_without_a_validated_edge": silent_nodes},
            "receipts_index": receipts,
            "tiering_legend": tiers.TIERS,
            "discipline": "RAW MATERIAL for YOUR read. Only 'validated' items are claims; nulls and "
                          "coverage gaps are shown so you don't over-claim. The engine measures "
                          "consequence, never whether an event will happen. You write the read."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default="me-risk")
    a = ap.parse_args()
    r = orient(a.topic)
    if not r.get("ok"):
        print("  pick a topic/domain:", ", ".join(r["domains"])); return
    print("=" * 78)
    print(f"ORIENT -- {a.topic}  (domain: {r['domain']})   [raw material; you write the read]")
    print("=" * 78)
    print(f"  regime: H1 amplifier {r['regime']['H1_amplifier']} -- {r['regime']['reading']}")
    print("  VALIDATED edges here:")
    for n in r["validated_edges"]:
        ci = n.get("ci", [None, None])
        print(f"    {n['node']:<16} {n['amp']:+.1f}{n.get('unit','')}  CI{ci}  ({r['receipts_index'].get(n['node'])})")
    if r["null_edges"]:
        print("  null: " + ", ".join(n["node"] for n in r["null_edges"]))
    if r["live_gap"]:
        g = r["live_gap"]
        print(f"  live gap: engine {g.get('engine_call')} vs market OVX {g.get('priced_ovx')} -> {g.get('gap_direction')}")
    if r["situations"]:
        print("  live situations: " + ", ".join(f"{s['situation']}({s['multi_modal']}mm)" for s in r["situations"]))
    cg = r["gaps_in_coverage"]
    print(f"  coverage gaps: thin types={cg['underpowered_event_types'] or 'none'}; "
          f"silent nodes={cg['domain_nodes_without_a_validated_edge'] or 'none'}")


if __name__ == "__main__":
    main()
