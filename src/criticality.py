"""
criticality.py -- the strategic-commodity criticality engine.

Turns data/criticality.yaml (WHO controls the world's critical inputs) into three
things the engine needs:
  1. a WATCH-LIST -- the supply-critical countries to keep eyes on and WHY (Kazakhstan
     because uranium, DRC because cobalt, Netherlands because EUV lithography, ...).
  2. per-country EXPOSURE -- what a given country is critical for.
  3. COMMODITIES AT RISK -- cross-referenced with the ACTIVE situations: which strategic
     commodities are under geopolitical stress right now because a critical producer is
     in an active conflict (Russia-Ukraine -> palladium, wheat, potash, gas at risk).

That third output is the payoff: it extends the engine's "shock -> ripple" thesis from
oil to the whole commodity complex, grounded in real, sourced concentration data. It is
DISPLAY/context (surfaces exposure; the transmission magnitude is a later, calibrated
step). All figures trace to criticality.yaml's cited sources.

Run:  python3 src/criticality.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "data" / "criticality.yaml"
SITUATIONS = ROOT / "data" / "situations.yaml"
OUT = ROOT / "data" / "criticality.json"


def load_map(path=MAP):
    """The commodities dict from criticality.yaml, or {} if absent."""
    if not Path(path).exists():
        return {}
    return (yaml.safe_load(Path(path).read_text()) or {}).get("commodities", {})


def watch_list(commodities):
    """country slug -> [(commodity, share, stage)], sorted by share. The supply-critical
    countries to watch, and what each is critical for."""
    out = {}
    for name, c in commodities.items():
        for country, share in (c.get("top") or {}).items():
            out.setdefault(country, []).append((name, share, c.get("stage", "")))
    for country in out:
        out[country].sort(key=lambda t: t[1], reverse=True)
    return out


def exposure(commodities, country):
    """What one country is strategically critical for."""
    return watch_list(commodities).get(country, [])


def at_risk(commodities, active_countries):
    """Given the countries in ACTIVE situations, which strategic commodities are under
    stress -- and by how much of global supply. The transmission-exposure signal."""
    risks = []
    for name, c in commodities.items():
        top = c.get("top") or {}
        hit = [(k, v) for k, v in top.items() if k in active_countries]
        if hit:
            risks.append({
                "commodity": name, "stage": c.get("stage", ""),
                "at_risk_countries": [{"country": k, "share": v} for k, v in
                                      sorted(hit, key=lambda t: t[1], reverse=True)],
                "at_risk_share": sum(v for _, v in hit), "source": c.get("source", "")})
    return sorted(risks, key=lambda r: r["at_risk_share"], reverse=True)


def active_situation_countries(path=SITUATIONS):
    """Country slugs that appear in any ACTIVE situation (the current stress set)."""
    if not Path(path).exists():
        return set()
    cfg = yaml.safe_load(Path(path).read_text()) or {}
    out = set()
    for s in cfg.get("situations", []):
        if s.get("status") == "closed":
            continue
        for eid in s.get("member_entities", []):
            if eid.startswith("country."):
                out.add(eid.split(".", 1)[1])
    return out


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    commodities = load_map()
    wl = watch_list(commodities)
    active = active_situation_countries()
    risks = at_risk(commodities, active)
    # rank the watch-list countries by how systemically critical they are.
    ranked = sorted(({"country": k, "n_commodities": len(v),
                      "top_share": v[0][1] if v else 0,
                      "critical_for": [x[0] for x in v]} for k, v in wl.items()),
                    key=lambda d: (d["top_share"], d["n_commodities"]), reverse=True)
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now,
         "note": "Strategic-commodity criticality (sourced in criticality.yaml). "
                 "commodities_at_risk = a critical producer is in an ACTIVE situation. "
                 "DISPLAY/context; transmission magnitude is a later calibrated step.",
         "critical_countries": ranked,
         "active_situation_countries": sorted(active),
         "commodities_at_risk": risks}, indent=2))
    print(f"criticality -- {len(wl)} supply-critical countries mapped; "
          f"{len(risks)} strategic commodities under stress (active situations).")
    for r in risks[:8]:
        who = ", ".join(f"{c['country']} {c['share']}%" for c in r["at_risk_countries"])
        print(f"  AT RISK  {r['commodity']:<22} {r['stage']:<12} {who}")


if __name__ == "__main__":
    main()
