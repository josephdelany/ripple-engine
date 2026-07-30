"""
sowhat.py -- the live "so-what" wire (Step 3): close the warning-response gap.

Conflict early-warning's documented failure is "warning without response" -- a feed tells you
something happened, not what it MEANS or how sure. This wire answers the analyst's actual question:
given today's regime, if a shock lands (or just did), here is the CONSEQUENCE (propagated through the
VALIDATED graph only), what the market has already PRICED (the gap), how CORROBORATED the live
situations are (multi-modal, not headlines), and the RECEIPTS. Decision-relevant, not "an alert."

Deterministic assembly of committed artifacts (no LLM, no new numbers):
  regime        <- engine_read.json (H1 amplifier ON/OFF)
  propagation   <- propagation_graph.json (validated backbone edges only)
  base rates    <- engine_read.json (clustered CAR by event type)
  priced gap    <- gaps.json (live gap)
  corroboration <- corroboration.json (multi-modal convergence per active situation)

Run:  python3 src/sowhat.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "sowhat.json"


def _j(name):
    p = DATA / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


def build():
    er = _j("engine_read.json")
    pg = _j("propagation_graph.json")
    gp = _j("gaps.json")
    corr = _j("corroboration.json")

    h1 = (er.get("hypotheses") or {}).get("H1", {})
    regime = h1.get("amplifier", "?")          # ON = stressed, OFF = calm
    backbone = [{"to": e["to"], "strength": e["strength"], "unit": e["unit"], "ci": e.get("ci")}
                for e in pg.get("backbone_validated", [])]
    base_rates = er.get("base_rates", [])
    live_gap = gp.get("live_gap")

    # per active situation: the multi-modal corroboration read + receipts
    situations = []
    conv = corr.get("convergence") or {}
    sits = corr.get("situations") or {}
    for sid, c in conv.items():
        top = c.get("top") or {}
        # a couple of sourced receipts from the top events
        evs = sits.get(sid, [])
        receipts = []
        for e in evs[:3]:
            receipts += (e.get("source_urls") or [])[:2]
        situations.append({
            "situation": sid.replace("situation.", ""),
            "events": c.get("n_events", 0), "multi_modal": c.get("n_multi_modal", 0),
            "max_modality_classes": c.get("max_modality_classes", 0),
            "top_event": top.get("headline", ""), "top_tag": top.get("tag", ""),
            "confirmed_by": top.get("modality_classes", []),
            "receipts": sorted(set(receipts))[:4]})
    situations.sort(key=lambda s: (s["max_modality_classes"], s["events"]), reverse=True)

    read = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "regime": regime,
        "so_what": (
            f"Regime is {regime} (VIX-stress {'elevated' if regime == 'ON' else 'calm'}). "
            f"If a shock lands, the VALIDATED propagation is into "
            + (", ".join(f"{b['to']} {b['strength']:+.1f}{b['unit']}" for b in backbone) or "nothing validated")
            + f". Market-priced gap: {live_gap['gap_direction'] if live_gap else 'n/a'}. "
            "Everything else (direction by event type, cross-node leads) is a null/trap -- not a claim."),
        "validated_propagation": backbone,
        "base_rate_ripple_by_type": base_rates,
        "priced_gap": live_gap,
        "active_situations": situations,
        "discipline": "Only validated-backbone edges are claims; base rates carry their n; the gap is "
                      "market-as-null; situations are ranked by multi-modal corroboration, with receipts.",
    }
    OUT.write_text(json.dumps(read, indent=2, default=str))
    return read


def main():
    r = build()
    print("=" * 82)
    print(f"THE SO-WHAT WIRE  --  regime: {r['regime']}   ({r['generated_at'][:16]})")
    print("=" * 82)
    print(f"  {r['so_what']}")
    print("\n  VALIDATED propagation (the only claims):")
    for b in r["validated_propagation"]:
        ci = b.get("ci") or [None, None]
        cis = f"CI[{ci[0]:+.1f},{ci[1]:+.1f}]" if ci[0] is not None else ""
        print(f"    shock =(stress)=> {b['to']:<14} {b['strength']:+.1f}{b['unit']:<3} {cis}")
    if r["priced_gap"]:
        print(f"\n  priced gap: {r['priced_gap']['notes']}")
    print("\n  active situations (ranked by multi-modal corroboration):")
    for s in r["active_situations"][:5]:
        cb = ", ".join(s["confirmed_by"]) or "news only"
        print(f"    {s['situation']:<24} events={s['events']:<3} multi-modal={s['multi_modal']} "
              f"[{cb}]  top: {s['top_event'][:40]}")
    print("\n  " + r["discipline"])


if __name__ == "__main__":
    main()
