"""materiality.py -- the gate in front of the Feed (NORTH_STAR §1b/§1c, A10).

Significance is defined by the market, not by us: a story's event class is
MATERIAL when that class sits inside big moves (data/big_moves) more often than
any random day does. Rules are registered in CLAIM_LEDGER_REGISTRATION.md §1;
this module implements them and nothing else. Attention flags are context.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SUMMARY = DATA / "big_moves" / "summary.json"

MATERIAL_RATIO = 1.2
INLINE_RATIO = 0.8
MIN_N = 8
ENDOGENOUS = {"policy_response"}
ASSETS = ("brent", "diesel_crack")          # crude side + product side
LOUD_PCT = 80
QUIET_PCT = 40

_cache = {"mtime": None, "data": None}


def load_summary(path=SUMMARY):
    if not path.exists():
        return {}
    m = path.stat().st_mtime
    if _cache["mtime"] != m:
        _cache.update(mtime=m, data=json.load(open(path)))
    return _cache["data"]


def class_rates(etype, summary=None):
    """Per-asset [k, n, rate%, base%, ratio] for an event class. Pure."""
    summary = summary if summary is not None else load_summary()
    out = {}
    for a in ASSETS:
        s = summary.get(a) or {}
        kn = (s.get("p_big_given_class") or {}).get(etype)
        base = s.get("everyday_base_rate_pct")
        if not kn or not base:
            continue
        k, n = kn
        rate = 100.0 * k / n if n else 0.0
        out[a] = {"k": k, "n": n, "rate_pct": round(rate, 1), "base_pct": base,
                  "ratio": round(rate / base, 2) if base else None, "label": s.get("label", a)}
    return out


def gate(etype, summary=None):
    """MATERIAL / IN_LINE / NOISE for an event class, with the numbers that decided it.
    Pure given `summary`; unit-tested."""
    if not etype:
        return {"significance": "NOISE", "why": "maps to no event class the record measures",
                "rates": {}, "flags": []}
    rates = class_rates(etype, summary)
    if not rates:
        return {"significance": "NOISE", "why": f"'{etype}' has no big-move record", "rates": {}, "flags": ["no_record"]}
    best_asset, best = max(rates.items(), key=lambda kv: kv[1]["ratio"] or 0)
    n = min(r["n"] for r in rates.values())
    ratio = best["ratio"] or 0
    flags = []
    if etype in ENDOGENOUS:
        sig = "IN_LINE" if ratio >= INLINE_RATIO else "NOISE"
        flags.append("endogenous")
        why = (f"{etype} is a reaction to moves, not a driver (endogenous by construction); capped at IN LINE. "
               f"Inside a big move {best['rate_pct']}% of the time on {best['label']} vs everyday {best['base_pct']}%.")
    elif n < MIN_N:
        sig = "IN_LINE" if ratio >= INLINE_RATIO else "NOISE"
        flags.append("thin")
        why = f"only {n} events of this class in the record — too thin to call material."
    elif ratio >= MATERIAL_RATIO:
        sig = "MATERIAL"
        why = (f"{etype.replace('_', ' ')} sits inside a big {best['label']} move {best['rate_pct']}% of the time "
               f"({best['k']} of {best['n']}) vs {best['base_pct']}% for any random day — {ratio:.1f}× the everyday rate.")
    elif ratio >= INLINE_RATIO:
        sig = "IN_LINE"
        why = (f"{etype.replace('_', ' ')} is inside a big move {best['rate_pct']}% of the time on {best['label']} — "
               f"about the everyday rate ({best['base_pct']}%).")
    else:
        sig = "NOISE"
        why = (f"{etype.replace('_', ' ')} is inside a big move only {best['rate_pct']}% of the time on {best['label']} "
               f"— below the everyday {best['base_pct']}%. The record says this class rarely changes the market.")
    if "brent" in rates and "diesel_crack" in rates and (rates["diesel_crack"]["ratio"] or 0) > (rates["brent"]["ratio"] or 0) + 0.3:
        flags.append("product_side")
    return {"significance": sig, "why": why, "rates": rates, "decisive_asset": best_asset, "ratio": ratio,
            "n": n, "flags": flags, "registration": "CLAIM_LEDGER_REGISTRATION.md §1"}


def attention(entities=None):
    """Attention context from files the daily loop already writes: GPR percentile (global) and
    Wikipedia pageview spikes on matched pages. Returns percentile-like score 0-100 + evidence."""
    ents = set(entities or [])
    gpr = _load(DATA / "gpr_signal.json").get("gpr") or {}
    wiki = _load(DATA / "wiki_attention.json").get("pages") or []
    pct = gpr.get("percentile")
    spikes = [p for p in wiki if p.get("flag") == "spike" and _matches(p, ents)]
    score = None
    if pct is not None:
        score = float(pct)
    if spikes:
        score = max(score or 0, 90.0)
    ev = {"gpr_percentile": pct, "gpr_as_of": gpr.get("date"), "wiki_spikes": [p.get("page") for p in spikes]}
    return {"score": score, "evidence": ev}


def flags_for(significance, att_score):
    if att_score is None:
        return []
    if significance != "MATERIAL" and att_score >= LOUD_PCT:
        return ["LOUD_QUIET"]
    if significance == "MATERIAL" and att_score <= QUIET_PCT:
        return ["QUIET_LOUD"]
    return []


def _matches(page, ents):
    slug = (page.get("slug") or "").lower()
    return any(slug and slug in e.lower() for e in ents) if ents else False


def _load(p):
    try:
        return json.load(open(p))
    except Exception:
        return {}


if __name__ == "__main__":
    for t in ("infrastructure_attack", "chokepoint_disruption", "opec_decision", "demand_shock",
              "conflict_escalation", "sanctions", "policy_response", None):
        g = gate(t)
        print(f"{str(t):24s} {g['significance']:9s} {g.get('why', '')}")
    print(attention(["country.iran", "chokepoint.hormuz"]))
