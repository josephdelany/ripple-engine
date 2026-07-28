"""
gpr_signal.py -- the RISK-vs-PRICED divergence read (built on the GPR index).

The GPR index (Caldara-Iacoviello, the Fed's benchmark) measures how much geopolitical
risk is "in the air" from the news. On its own that's just a number. The INSIGHT an
analyst reads is the DIVERGENCE:

    Geopolitical risk is at the Nth percentile of its whole history ... but is the oil
    market actually PRICING that risk, or is it complacent?

We answer it deterministically by ranking two things against their own histories:
  - GPR (the risk in the air)                     -> gpr.GPRD
  - Brent 20-day realised volatility (what the    -> derived.brent_vol20
    oil market is actually pricing as risk)
A wide gap -- risk hot, vol calm -- is the classic "market hasn't caught up yet" setup,
exactly the ahead-of-consensus pattern this engine exists to surface. We also split GPR
into THREATS vs ACTS (is risk anticipatory or already realised?) and tie in how many
chokepoint transmission chains are live (from propagation.json).

DISPLAY/context, honestly tagged: this is a descriptive divergence over full history, not
a calibrated trade signal and NOT part of the pre-registered H1-H3 study. Typed percentile
BANDS, not invented decimals. Deterministic Python only -- no LLM in the math.

Run:  python3 src/gpr_signal.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
PROP = ROOT / "data" / "propagation.json"
SITUATIONS = ROOT / "data" / "situations.yaml"
MARKET = ROOT / "data" / "market_live.json"
OUT = ROOT / "data" / "gpr_signal.json"

# Oil-producer / chokepoint-controlling countries. A shock concentrated HERE is a
# SUPPLY-fear shock (country-specific -> oil UP). A diffuse/global risk is a DEMAND-fear
# shock (-> oil DOWN). Grounded in ECB/AER-2022: global GPR pushes Brent ~-1.2%, country-
# specific (Iran/Russia/producers) pushes it +0.8-1.5%. This is the source-aware fix.
OIL_STATES = {"iran", "russia", "saudi_arabia", "uae", "iraq", "kuwait", "qatar",
              "venezuela", "libya", "nigeria", "algeria"}

# The priced-risk proxy: 20-day realised Brent vol (what the oil market prices as risk).
PRICED_SERIES = "derived.brent_vol20"


def series_values(conn, series_id):
    """(date, value) rows for a series, oldest-first, nulls dropped."""
    rows = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY obs_date", (series_id,)).fetchall()
    return [(d, float(v)) for d, v in rows]


def pct_rank(values, latest):
    """Percentile (0-100) of `latest` within `values`: the share of history at-or-below it.
    100 = highest ever seen, 50 = median."""
    if not values:
        return None
    n_le = sum(1 for v in values if v <= latest)
    return round(100.0 * n_le / len(values), 1)


def band(pct):
    """Typed percentile bucket -- no naked decimals at the surface."""
    if pct is None:
        return "n/a"
    if pct < 20:
        return "calm"
    if pct < 50:
        return "normal"
    if pct < 80:
        return "elevated"
    if pct < 95:
        return "high"
    return "extreme"


def divergence(gpr_pct, priced_pct):
    """The read: how far is risk-in-the-air running ahead of (or behind) what the market
    is pricing? Returns (gap, band, direction)."""
    if gpr_pct is None or priced_pct is None:
        return None, "n/a", "n/a"
    gap = round(gpr_pct - priced_pct, 1)
    mag = abs(gap)
    gband = "aligned" if mag < 15 else ("mild gap" if mag < 35 else "wide gap")
    if mag < 15:
        direction = "market in line with risk"
    elif gap > 0:
        direction = "risk HOTTER than the market is pricing"      # the classic setup
    else:
        direction = "market more nervous than the risk warrants"
    return gap, gband, direction


def n_live_chokepoint():
    """How many chokepoint transmission chains are live right now (from propagation.json),
    so the read ties risk to concrete downstream exposure. 0 if not yet generated."""
    if not PROP.exists():
        return None
    return json.loads(PROP.read_text()).get("n_live_chokepoint")


def active_supply_countries():
    """Oil-producer/chokepoint countries in any ACTIVE situation -- the SUPPLY-channel set."""
    if not SITUATIONS.exists():
        return []
    import yaml
    cfg = yaml.safe_load(SITUATIONS.read_text()) or {}
    out = set()
    for s in cfg.get("situations", []):
        if s.get("status") == "closed":
            continue
        for eid in s.get("member_entities", []):
            if eid.startswith("country.") and eid.split(".", 1)[1] in OIL_STATES:
                out.add(eid.split(".", 1)[1])
    return sorted(out)


def channel_of(supply_countries):
    """Which transmission channel dominates: SUPPLY (country-specific -> oil up) or DEMAND
    (diffuse/global -> oil down). Pure -- unit-tested."""
    return "supply" if supply_countries else "demand"


def fresh_oil_move():
    """(chg1d, chg5d, as_of) for Brent from the live feed, or (None, None, None)."""
    if not MARKET.exists():
        return None, None, None
    a = (json.loads(MARKET.read_text()).get("assets") or {}).get("live.brent") or {}
    return a.get("chg1d"), a.get("chg5d"), a.get("as_of")


def source_aware_verdict(channel, oil_5d, supply_countries):
    """Compare the EXPECTED oil direction (from the shock's source) to the REAL move. This is
    the fix for the engine's old 'aligned while oil craters' lie. Pure -- unit-tested."""
    expected = "up" if channel == "supply" else "down"
    if oil_5d is None:
        return {"expected": expected, "actual": "n/a", "verdict": "no live oil price",
                "flag": "unknown"}
    actual = "up" if oil_5d > 1 else "down" if oil_5d < -1 else "flat"
    who = ", ".join(supply_countries) if supply_countries else "no oil-producer theatre"
    if channel == "supply" and actual == "down":
        v, flag = (f"DIVERGENCE — supply-fear theatre active ({who}) yet Brent is FALLING "
                   f"({oil_5d}% 5d): the market is discounting the supply premium (de-escalation "
                   f"or demand fear). The oil-price signal contradicts the risk level.", "divergence")
    elif channel == "supply" and actual == "up":
        v, flag = (f"CONFIRMED — supply premium pricing in: Brent UP ({oil_5d}% 5d) with a "
                   f"country-specific shock ({who}).", "confirmed")
    elif channel == "demand" and actual == "down":
        v, flag = (f"CONSISTENT — diffuse/global risk with Brent falling ({oil_5d}% 5d): the "
                   f"demand-fear channel, as expected.", "consistent")
    elif channel == "demand" and actual == "up":
        v, flag = (f"WATCH — diffuse risk but Brent RISING ({oil_5d}% 5d): a supply factor may "
                   f"be emerging that the broad read misses.", "watch")
    else:
        v, flag = (f"NEUTRAL — Brent roughly flat ({oil_5d}% 5d); no clear directional signal.",
                   "flat")
    return {"channel": channel, "expected": expected, "actual": actual,
            "oil_5d": oil_5d, "supply_countries": supply_countries, "verdict": v, "flag": flag}


def build():
    conn = sqlite3.connect(DB)
    gpr = series_values(conn, "gpr.GPRD")
    threat = series_values(conn, "gpr.GPRD_THREAT")
    act = series_values(conn, "gpr.GPRD_ACT")
    priced = series_values(conn, PRICED_SERIES)
    conn.close()

    if not gpr or not priced:
        return {"error": "missing gpr.GPRD or derived.brent_vol20 -- run fetch_gpr.py "
                         "and derive_signals.py first."}

    g_date, g_val = gpr[-1]
    g_pct = pct_rank([v for _, v in gpr], g_val)
    p_date, p_val = priced[-1]
    p_pct = pct_rank([v for _, v in priced], p_val)
    gap, gband, direction = divergence(g_pct, p_pct)

    # Threats vs acts: is the risk anticipatory (threats leading) or already realised?
    t_val = threat[-1][1] if threat else None
    a_val = act[-1][1] if act else None
    posture = "n/a"
    if t_val is not None and a_val is not None:
        posture = "anticipatory (threats > acts)" if t_val > a_val else "realised (acts >= threats)"

    n_choke = n_live_chokepoint()

    # SOURCE-AWARE transmission: is the risk supply-channel (country-specific -> oil up) or
    # demand-channel (diffuse -> oil down), and does the REAL oil move confirm or contradict it?
    supply = active_supply_countries()
    channel = channel_of(supply)
    oil_1d, oil_5d, oil_date = fresh_oil_move()
    transmission = source_aware_verdict(channel, oil_5d, supply)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    # The headline now LEADS with the directional, source-aware read (the fix), not vol-only.
    headline = (f"Geopolitical risk {band(g_pct)} ({g_pct}th pct). {transmission['verdict']}")
    if n_choke:
        headline += f" ({n_choke} chokepoint chains live.)"

    return {
        "as_of": oil_date or g_date, "generated_at": now,
        "note": "Source-aware transmission read. Channel (supply vs demand) is inferred from "
                "which theatres are active; the REAL Brent move (live feed) confirms or "
                "contradicts the expected direction. Descriptive; not the pre-registered study.",
        "gpr": {"value": round(g_val, 1), "date": g_date, "percentile": g_pct,
                "band": band(g_pct), "posture": posture},
        "transmission": transmission,
        "oil_live": {"chg1d": oil_1d, "chg5d": oil_5d, "as_of": oil_date},
        "priced_vol": {"series": PRICED_SERIES, "value": round(p_val, 2), "date": p_date,
                       "percentile": p_pct, "band": band(p_pct)},
        "vol_divergence": {"gap_pctpts": gap, "band": gband, "direction": direction},
        "live_chokepoint_chains": n_choke,
        "headline": headline}


def main():
    rep = build()
    OUT.write_text(json.dumps(rep, indent=2))
    if "error" in rep:
        print(f"gpr_signal -- STOP: {rep['error']}")
        return
    print(f"gpr_signal -- {rep['headline']}")
    print(f"  GPR posture: {rep['gpr']['posture']}")


if __name__ == "__main__":
    main()
