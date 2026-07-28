"""
propagation.py -- the oil/energy PROPAGATION GRAPH engine ("everything oil touches").

Turns data/propagation.yaml (directional transmission chains: trigger geography -> choke
-> downstream market) into the engine's answer to one question:

    Given the conflicts that are ACTIVE right now, which transmission paths are LIVE --
    and what downstream markets are they reaching?

This is the capability Joe described: a shock in the Gulf doesn't just move the oil price;
it ripples down sourced chains (gas -> ammonia -> fertilizer -> food; Russia -> palladium ->
autocatalysts; China -> heavy rare earths -> missiles). Where criticality.py answers "who is
exposed," propagation.py answers "which way does the shock travel, and how far."

It is DISPLAY/context: it surfaces which chains are live and their sourced mechanism/lag.
Transmission MAGNITUDE is a later, calibrated step -- not claimed here. Every field traces
to propagation.yaml's cited sources. Deterministic Python only (no LLM in the math).

Mirrors the criticality.py / situations.yaml pattern (see [[foundation-first]] discipline).

Run:  python3 src/propagation.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "data" / "propagation.yaml"
SITUATIONS = ROOT / "data" / "situations.yaml"
OUT = ROOT / "data" / "propagation.json"


def load_chains(path=MAP):
    """The chains dict from propagation.yaml, or {} if absent."""
    if not Path(path).exists():
        return {}
    return (yaml.safe_load(Path(path).read_text()) or {}).get("chains", {})


def active_situation_countries(path=SITUATIONS):
    """Country slugs in any ACTIVE (not closed) situation -- the current stress set.
    Identical rule to criticality.active_situation_countries so the two arms agree."""
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


def live_chains(chains, active_countries):
    """The transmission paths that are LIVE: a chain fires when one of its `countries`
    (the situation-slugs that would trigger it) is in an active situation. Returns each
    live chain with the specific triggering countries surfaced, sorted chokepoint-first
    (the sharp, hard-to-substitute paths) then by name for stability."""
    live = []
    for name, c in chains.items():
        triggers = [x for x in (c.get("countries") or []) if x in active_countries]
        if triggers:
            live.append({
                "chain": name,
                "geometry": c.get("geometry", ""),
                "triggered_by": sorted(triggers),
                "choke": c.get("choke", ""),
                "downstream": c.get("downstream", ""),
                "lag": c.get("lag", ""),
                "observe": c.get("observe", ""),
                "episode": c.get("episode", ""),
                "source": c.get("source", "")})
    # chokepoint chains first (0 sorts before 1), then alphabetical by chain name.
    live.sort(key=lambda d: (d["geometry"] != "chokepoint", d["chain"]))
    return live


def downstream_markets(live):
    """Flatten the live chains to the distinct downstream markets under stress -- the
    'so what' list an analyst reads first."""
    return sorted({d["downstream"] for d in live if d.get("downstream")})


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    chains = load_chains()
    active = active_situation_countries()
    live = live_chains(chains, active)
    n_choke = sum(1 for d in live if d["geometry"] == "chokepoint")
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now,
         "note": "Oil/energy propagation graph (sourced in propagation.yaml). live_chains = "
                 "a transmission path whose trigger geography is in an ACTIVE situation. "
                 "DISPLAY/context; transmission magnitude is a later calibrated step.",
         "active_situation_countries": sorted(active),
         "n_chains_total": len(chains), "n_live": len(live), "n_live_chokepoint": n_choke,
         "live_chains": live,
         "downstream_markets_at_risk": downstream_markets(live)}, indent=2))
    print(f"propagation -- {len(chains)} chains mapped; {len(live)} LIVE "
          f"({n_choke} chokepoint) given active situations {sorted(active)}.")
    for d in live[:10]:
        tag = "CHOKE" if d["geometry"] == "chokepoint" else "bulk "
        print(f"  {tag} {d['chain']:<26} <- {','.join(d['triggered_by']):<18} -> {d['downstream'][:52]}")


if __name__ == "__main__":
    main()
