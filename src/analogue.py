"""
analogue.py -- the ANALOGUE PROBABILITY FUNCTION (Stage 1: activate the predictive engine).

This is the jump from "here's what's live" to "here's what usually happens next." Given a
shock's SIGNATURE (event type, archetype, surprise, ...), it finds the nearest historical
analogues in a 511-event seed library and returns the DISTRIBUTION of how markets resolved
in those analogues -- never a naked number, always its basis and a confidence that reflects
how much support there is.

    "In the 54 most-similar historical geopolitical shocks, WTI most often OVERSHOT
     (40%, 8/20), then mean-reverted; equities cleanly absorbed (55%); gold rallied.
     Confidence: moderate (N=54, agreement 0.40). Nearest analogue: <event> (score 70)."

This is k-nearest-neighbour / case-based analogue forecasting -- a legitimate, citable
method (see ENGINE_SPEC Type-B / probability function). The seed library
(data/seed_library/observations.jsonl) is migrated from the newquant research corpus:
511 historical shocks, each with the pattern every asset showed (clean_absorption,
overshoot, slow_absorption, directional_error, confounded_signal, bifurcated).

Scoring is the deterministic feature-overlap model from the research (re-implemented, not
imported -- legacy is read-only). "No good analogue / new regime" is a VALID output when
support is thin -- we do not manufacture confidence.

Deterministic Python only. No LLM. Run:  python3 src/analogue.py
"""

import collections
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "data" / "seed_library" / "observations.jsonl"
SITUATIONS = ROOT / "data" / "situations.yaml"
OUT = ROOT / "data" / "analogue.json"

MIN_ANALOGUES = 5          # below this, "no good analogue / thin" -- an honest output
TOP = 60                   # analogues to pool for the distribution

# The assets a conflict-oil analyst reads first; the forecast highlights these when present.
KEY_ASSETS = ["wti", "brent", "sp500", "gold", "vix", "10y_treasury", "xle", "dxy"]

# Map a ripple-engine situation kind -> a seed-library query. Exact event_type match scores
# 40, same archetype 15 (see score()). Kept explicit and small.
KIND_TO_QUERY = {
    "conflict_escalation":    {"event_type": "geo", "archetype": "geopolitical_shock"},
    "chokepoint_disruption":  {"event_type": "commodity_supply", "archetype": "commodity_supply_shock"},
    "infrastructure_attack":  {"event_type": "commodity_supply", "archetype": "commodity_supply_shock"},
    "sanctions":              {"event_type": "geo", "archetype": "geopolitical_shock"},
    "opec_decision":          {"event_type": "opec", "archetype": "commodity_decision"},
}


def load_library(path=LIBRARY):
    if not Path(path).exists():
        return []
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def era_of(date_str):
    if not date_str:
        return "unknown"
    if date_str < "1995-01-01":
        return "pre-1995"
    if date_str < "2008-01-01":
        return "1995-2007"
    if date_str < "2016-01-01":
        return "2008-2015"
    return "2016-present"


def score(query, obs):
    """Feature-overlap similarity (0-100). Exact event_type=40, archetype=15, surprise=15,
    rate_direction=10, era=10, and proximity on disagreement/importance up to 5 each."""
    total, b = 0, {}
    if query.get("event_type") and query["event_type"] == obs.get("event_type"):
        b["event_type"] = 40; total += 40
    if query.get("archetype") and query["archetype"] == obs.get("archetype"):
        b["archetype"] = 15; total += 15
    if query.get("surprise") and query["surprise"] == obs.get("surprise"):
        b["surprise"] = 15; total += 15
    if query.get("rate_direction") and query["rate_direction"] == obs.get("rate_direction"):
        b["rate_direction"] = 10; total += 10
    q_era = query.get("era") or (era_of(query["event_date"]) if query.get("event_date") else None)
    if q_era and q_era == era_of(obs.get("event_date")):
        b["era"] = 10; total += 10
    for k in ("disagreement_score", "importance_score"):
        if query.get(k) is not None and obs.get(k) is not None:
            pts = max(0, 5 - abs(query[k] - obs[k]))
            if pts:
                b[k] = pts; total += pts
    return total, b


def search(query, library, top=TOP):
    """Rank the library by similarity to ONE query; drop zero-score records."""
    scored = [(s, obs) for obs in library for s, _ in [score(query, obs)] if s > 0]
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def search_multi(queries, library, top=TOP):
    """Pool analogues across SEVERAL query signatures (a situation's mix of dominant kinds),
    keeping each event once at its best score. Lets a chokepoint+sanctions situation draw a
    different analogue set than a pure-escalation one."""
    best = {}
    for q in queries:
        for s, obs in search(q, library, top):
            eid = obs.get("event_id")
            if eid not in best or s > best[eid][0]:
                best[eid] = (s, obs)
    pooled = sorted(best.values(), key=lambda x: -x[0])
    return pooled[:top]


def outcome_distribution(matches):
    """For each asset seen across the matched analogues, the pattern distribution and the
    dominant pattern + its share. This is the 'what usually happens' payload."""
    by_asset = collections.defaultdict(collections.Counter)
    overall = collections.Counter()
    for _, obs in matches:
        for gp in obs.get("gap_patterns", []):
            tok = gp.get("asset_token") or gp.get("asset_class")
            pat = gp.get("pattern")
            if tok and pat:
                by_asset[tok][pat] += 1
                overall[pat] += 1
    out = {}
    for tok, ctr in by_asset.items():
        n = sum(ctr.values())
        dom, dom_n = ctr.most_common(1)[0]
        out[tok] = {"n": n, "dominant": dom, "share": round(dom_n / n, 2),
                    "patterns": dict(ctr)}
    return out, overall


def confidence(matches, overall):
    """Typed confidence band from f(N, similarity, agreement) -- never a naked number.
    Thin support returns the honest 'no good analogue' bucket."""
    n = len(matches)
    if n < MIN_ANALOGUES:
        return {"band": "thin — no good analogue", "n": n, "mean_similarity": None,
                "agreement": None}
    mean_sim = round(sum(s for s, _ in matches) / n, 1)
    total = sum(overall.values())
    agreement = round(overall.most_common(1)[0][1] / total, 2) if total else 0.0
    if n >= 25 and mean_sim >= 45 and agreement >= 0.35:
        band = "well-supported"
    elif n >= 12 and agreement >= 0.30:
        band = "moderate"
    else:
        band = "indicative"
    return {"band": band, "n": n, "mean_similarity": mean_sim, "agreement": agreement}


def forecast(queries, library, top=TOP, key_assets=KEY_ASSETS):
    """The full analogue forecast for one or more query signatures (a situation's kind mix).
    Accepts a single query dict or a list of them."""
    if isinstance(queries, dict):
        queries = [queries]
    matches = search_multi(queries, library, top)
    dist, overall = outcome_distribution(matches)
    conf = confidence(matches, overall)
    key = {a: dist[a] for a in key_assets if a in dist}          # highlight oil-analyst assets
    nearest = [{"event_id": o.get("event_id"), "date": o.get("event_date"),
                "type": o.get("event_type"), "score": s} for s, o in matches[:5]]
    return {"queries": queries, "n_analogues": len(matches), "confidence": conf,
            "overall_pattern": dict(overall.most_common()),
            "key_assets": key, "all_assets": dist, "nearest": nearest}


def active_situations(path=SITUATIONS):
    """(label, [kinds]) for each active (non-closed) situation."""
    if not Path(path).exists():
        return []
    cfg = yaml.safe_load(Path(path).read_text()) or {}
    out = []
    for s in cfg.get("situations", []):
        if s.get("status") == "closed":
            continue
        label = s.get("title") or s.get("situation_id") or "situation"
        out.append((label, s.get("dominant_kinds") or []))
    return out


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    library = load_library()
    if not library:
        OUT.write_text(json.dumps({"error": "seed library missing"}, indent=2))
        print("analogue -- STOP: data/seed_library/observations.jsonl not found.")
        return

    default_q = {"event_type": "geo", "archetype": "geopolitical_shock"}
    forecasts = []
    for label, kinds in active_situations():
        kinds = kinds or ["conflict_escalation"]
        queries = [KIND_TO_QUERY.get(k, default_q) for k in kinds]
        fc = forecast(queries, library)
        fc["situation"] = label
        fc["kinds"] = kinds
        forecasts.append(fc)

    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now, "library_n": len(library),
         "note": "Analogue probability function (kNN over 511-event seed library). For each "
                 "active situation: nearest historical analogues by signature + the pattern "
                 "distribution markets showed. Basis shown; 'thin' = no good analogue. "
                 "DISPLAY/context; not a calibrated trade signal.",
         "forecasts": forecasts}, indent=2))
    print(f"analogue -- {len(library)} library events; {len(forecasts)} situation forecasts:")
    for fc in forecasts:
        c = fc["confidence"]
        wti = fc["key_assets"].get("wti") or fc["key_assets"].get("brent")
        oil = f"oil={wti['dominant']} {int(wti['share']*100)}%" if wti else "oil=n/a"
        print(f"  {fc['situation'][:34]:<34} N={c['n']:<3} {c['band']:<20} {oil}")


if __name__ == "__main__":
    main()
