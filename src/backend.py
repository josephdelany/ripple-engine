"""
backend.py -- serves YOUR engine into OpenBB Workspace as custom widgets.

HOW THIS WORKS (the client-server model, in plain English):
OpenBB Workspace (the UI in your browser) is a shell. It asks a "backend" two
questions: (1) "what widgets do you have?" (GET /widgets.json) and (2) "give me
the data for widget X" (GET /<endpoint>). This file is a small FastAPI server
that answers both -- from YOUR SQLite database. ~150 lines and your research
appears in a professional terminal.

Widgets served:
  1. state_of_system    - the live modulator panel (your derived signals, latest)
  2. ripple_by_type     - mean CAR by event type at 4 horizons (the ripple)
  3. event_detail       - every event, its ripple, and the state it landed in
  4. event_database     - the sourced event list (your codebook in action)

Run it:            python3 src/backend.py
Then in Workspace: Apps -> Connect backend -> Name: Ripple Engine
                   URL:  http://127.0.0.1:5050
Leave this running in its own Terminal window (Ctrl+C stops it).
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from derive_signals import load_wide, build_signals, MECHANISMS
from event_study import load_returns, car_for_event, PRE

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
DATA = ROOT / "data"


def _read_json(name, default=None):
    """Read a pipeline artifact (corroboration.json, predmkt.json, ...). Safe."""
    p = DATA / name
    if not p.exists():
        return default if default is not None else {}
    try:
        return json.loads(p.read_text())
    except (ValueError, OSError):
        return default if default is not None else {}


def _series(conn, series_id, days=140):
    """(dates, values) for one series, newest-`days`, de-duped by date. For charts."""
    seen, out = set(), []
    for d, v in conn.execute(
            "SELECT obs_date, value FROM observations WHERE series_id=? "
            "ORDER BY obs_date DESC, as_of DESC", (series_id,)):
        if d in seen or v is None:
            continue
        seen.add(d)
        out.append((d, v))
        if len(out) >= days:
            break
    out.reverse()
    return [d for d, _ in out], [v for _, v in out]


def _situation_options():
    """Dropdown options for the Situation selector, from the human-owned config.
    Computed at startup (restart the backend to pick up new situations)."""
    p = DATA / "situations.yaml"
    if not p.exists():
        return [{"label": "Israel-Iran War", "value": "situation.israel_iran_war_2025"}]
    try:
        cfg = yaml.safe_load(p.read_text()) or {}
    except (OSError, yaml.YAMLError):
        return []
    return [{"label": s.get("title", s["situation_id"]), "value": s["situation_id"]}
            for s in cfg.get("situations", []) if s.get("status") != "closed"]


_SIT_OPTIONS = _situation_options()
_SIT_DEFAULT = _SIT_OPTIONS[0]["value"] if _SIT_OPTIONS else ""


def _line_fig(title, traces, ytitle=""):
    """A dark-mode-friendly Plotly line figure as a plain dict (no plotly dep).
    traces = [(name, dates, values), ...]."""
    return {
        "data": [{"x": x, "y": y, "type": "scatter", "mode": "lines", "name": n}
                 for n, x, y in traces if x],
        "layout": {"title": {"text": title}, "margin": {"t": 40, "r": 15, "b": 35, "l": 45},
                   "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)",
                   "font": {"color": "#c7ccd6"}, "yaxis": {"title": ytitle},
                   "legend": {"orientation": "h"}, "template": "plotly_dark"},
    }
PORT = 5050

app = FastAPI(title="Ripple Engine backend")

# CORS: the browser (pro.openbb.co) must be allowed to call your local server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pro.openbb.co", "http://localhost:1420"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WIDGETS = {
    "state_of_system": {
        "name": "State of the System",
        "description": "Latest derived signals -- the modulators a shock would land into",
        "endpoint": "state_of_system",
        "gridData": {"w": 20, "h": 9},
        "type": "table",
    },
    "ripple_by_type": {
        "name": "The Ripple (CAR by event type)",
        "description": "Mean cumulative abnormal return in Brent around geopolitical shocks",
        "endpoint": "ripple_by_type",
        "gridData": {"w": 20, "h": 9},
        "type": "table",
    },
    "event_detail": {
        "name": "Conditioned Events",
        "description": "Each event's ripple and the market state the day before it hit",
        "endpoint": "event_detail",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "event_database": {
        "name": "Event Database",
        "description": "The curated, coded shock list (see EVENTS_CODEBOOK.md)",
        "endpoint": "event_database",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "forecast_log": {
        "name": "Forecast Log",
        "description": "Joe's logged forecasts vs Kalshi, Brier-scored once resolved",
        "endpoint": "forecast_log",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "system_health": {
        "name": "System Health",
        "description": "Data freshness per series (OK/STALE/DEAD) from heartbeat.py",
        "endpoint": "system_health",
        "gridData": {"w": 30, "h": 12},
        "type": "table",
    },
    "engine_read": {
        "name": "Engine Read",
        "description": "If a shock landed today: amplifier status + historical base rates",
        "endpoint": "engine_read",
        "gridData": {"w": 30, "h": 10},
        "type": "table",
    },
    "sowhat": {
        "name": "The So-What Wire — event → consequence → decision",
        "description": "Closes the warning-response gap: today's regime, the VALIDATED propagation "
                       "(the only claims), the market-priced gap, and the live situations ranked by "
                       "multi-modal corroboration — with receipts. Decision-relevant, not 'an alert.'",
        "endpoint": "sowhat",
        "gridData": {"w": 40, "h": 11},
        "type": "markdown",
    },
    "domain_conditioning": {
        "name": "Apt Conditioning — each commodity vs its natural driver",
        "description": "Pre-declared, FDR-corrected: does each commodity ripple harder under its "
                       "ECONOMIC driver (not generic stress)? Copper validates under a growth-regime "
                       "(steep-curve) conditioner it was null under stress. Honest — nulls shown.",
        "endpoint": "domain_conditioning",
        "gridData": {"w": 40, "h": 8},
        "type": "table",
    },
    "edge_portfolio": {
        "name": "Edge Portfolio — the pre-registered battery",
        "description": "A pre-registered family of economically-distinct conditioned hypotheses, "
                       "family-wise corrected (BH-FDR + Bonferroni across prior + new), EVERY verdict "
                       "shown. Only survivors are claims; the nulls are the credibility. Frozen "
                       "registration: PRE_REGISTRATION.md.",
        "endpoint": "edge_portfolio",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "domain_lens": {
        "name": "Domain Lens — your analyst view",
        "description": "The one validated engine, filtered to your domain: ME-risk / commodities / "
                       "macro / conflict / geopolitics / supply-chain. Shows that domain's validated "
                       "nodes, supply-chain edges, event coverage, and live situations — nulls shown.",
        "endpoint": "domain_lens",
        "gridData": {"w": 40, "h": 11},
        "type": "table",
        "params": [{"paramName": "domain", "label": "Domain", "description": "Which analyst lens",
                    "value": "me-risk", "type": "text",
                    "options": [{"label": d, "value": d} for d in
                                ["me-risk", "commodities", "macro", "conflict", "geopolitics",
                                 "energy", "supply-chain"]]}],
    },
    "supply_chain": {
        "name": "Supply-Chain Transmission — producer-conflict → commodity",
        "description": "Closes the criticality-exposure gap with validated transmission: when a "
                       "commodity's critical producer is in conflict, what has the commodity actually "
                       "done? validated / null / insufficient — refuses to assert what the data can't.",
        "endpoint": "supply_chain",
        "gridData": {"w": 40, "h": 10},
        "type": "table",
    },
    "propagation_graph": {
        "name": "Propagation Graph — validated edges + traps",
        "description": "The consequence network: a validated backbone (shocks ripple into these nodes, "
                       "FDR-corrected), an honest null layer, and TRAP flags where nodes co-move but "
                       "neither leads. Draws only what survives, and flags what doesn't.",
        "endpoint": "propagation_graph",
        "gridData": {"w": 40, "h": 11},
        "type": "table",
    },
    "ripple_map": {
        "name": "Conditioned Ripple Map — does the edge generalize?",
        "description": "Does H1 (VIX stress amplifies the geopolitical ripple) hold across oil, gas, "
                       "the dollar and rates? Each asset validated through the SAME gate (bootstrap CI "
                       "+ permutation + FDR). Honest null cells where it doesn't generalize.",
        "endpoint": "ripple_map",
        "gridData": {"w": 40, "h": 9},
        "type": "table",
    },
    "corroboration_convergence": {
        "name": "Corroboration — confirmation, not headlines",
        "description": "Cross-modal convergence per situation: how many independent evidence TYPES "
                       "(news / physical ship-transits / thermal fires / repricing markets) confirm "
                       "each event. Multi-modal = confirmed beyond attention. The anti-noise layer.",
        "endpoint": "corroboration_convergence",
        "gridData": {"w": 40, "h": 10},
        "type": "table",
    },
    "gap_board": {
        "name": "The Gap Board — where the engine disagrees with the market",
        "description": "Market-as-null: the engine's H1-conditioned view vs the market's implied "
                       "oil vol (OVX), tiered under-priced-risk / over-priced-fear / aligned, with "
                       "the resolving Brier scorecard. The value is in the disagreement, honestly scored.",
        "endpoint": "gap_board",
        "gridData": {"w": 40, "h": 11},
        "type": "table",
    },
    "track_record": {
        "name": "Track Record — how sure, and scored",
        "description": "The calibration/accountability view: H1's walk-forward out-of-sample skill, "
                       "the gap ledger's Brier by regime, and the signal registry's live/rejected "
                       "tally. Every claim resolves and is scored.",
        "endpoint": "track_record",
        "gridData": {"w": 40, "h": 10},
        "type": "markdown",
    },
    "signal_registry": {
        "name": "Signal Registry — what's proven",
        "description": "Every signal the engine has tested, tiered live / experimental / rejected "
                       "by its validation evidence (status derived, not asserted). The factor-style "
                       "'what's proven, how sure, the receipts' view.",
        "endpoint": "signal_registry",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "h1_live_edge": {
        "name": "H1 — The Validated Edge",
        "description": "The one signal that passed the full validation gate: geopolitical "
                       "shocks ripple harder into oil when VIX stress is elevated. Live "
                       "amplifier state + the receipts (CI, FDR/Bonferroni, N).",
        "endpoint": "h1_live_edge",
        "gridData": {"w": 40, "h": 11},
        "type": "markdown",
    },
    "scenario_playbook": {
        "name": "Scenario Playbook",
        "description": "Per event type: clustered base-rate ripple + today's conditioning",
        "endpoint": "scenario_playbook",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "propagation_map": {
        "name": "Propagation Map (cross-asset)",
        "description": "Clustered mean CAR+20 by event type x asset (% for prices, bps for yields)",
        "endpoint": "propagation_map",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "alert_queue": {
        "name": "Watcher Alert Queue",
        "description": "Live news alerts (curated attention, never conclusions) -- newest first",
        "endpoint": "alert_queue",
        "gridData": {"w": 40, "h": 14},
        "type": "table",
    },
    # --- Phase 2 cockpit: the headline read ---
    "risk_gauge": {
        "name": "Gulf Risk Gauge",
        "description": "At-a-glance KPIs: escalation, amplifiers, chokepoint status, "
                       "top corroboration, and what's priced.",
        "endpoint": "risk_gauge",
        "gridData": {"w": 40, "h": 5},
        "type": "metric",
    },
    "story_opec": {
        "name": "Story: OPEC Fiscal Stress",
        "description": "A tracked story: who can afford this oil price (IMF breakeven vs live "
                       "Brent), what changed since last run, and the next catalyst. The first "
                       "story built to the new architecture.",
        "endpoint": "story_opec",
        "gridData": {"w": 40, "h": 9},
        "type": "markdown",
    },
    "risk_vs_priced": {
        "name": "Risk vs Priced (source-aware)",
        "description": "Is the risk supply-channel (country-specific -> oil up) or demand "
                       "(diffuse -> oil down), and does the REAL Brent move confirm or "
                       "contradict it? Replaces the old vol-only read that lied.",
        "endpoint": "risk_vs_priced",
        "gridData": {"w": 40, "h": 7},
        "type": "markdown",
    },
    "where_we_stand": {
        "name": "Where We Stand",
        "description": "The situation dossier as prose -- history + state + what's priced. "
                       "Pick a situation.",
        "endpoint": "where_we_stand",
        "gridData": {"w": 40, "h": 11},
        "type": "markdown",
        "params": [{
            "paramName": "situation",
            "label": "Situation",
            "description": "Which Gulf situation to read",
            "value": _SIT_DEFAULT,
            "type": "text",
            "options": _SIT_OPTIONS,
        }],
    },
    # --- Enrichment layer: the multi-modal signals + the corroboration brain ---
    "corroborated_events": {
        "name": "Corroborated Events",
        "description": "The timeline collapsed into events, scored by independent-source "
                       "convergence (news + physical + thermal). Confidence, not fact.",
        "endpoint": "corroborated_events",
        "gridData": {"w": 40, "h": 13},
        "type": "table",
    },
    "prediction_markets": {
        "name": "Market-Implied Odds",
        "description": "Polymarket probabilities for oil/geopolitics events -- what's "
                       "priced. Context only, never a statistic.",
        "endpoint": "prediction_markets",
        "gridData": {"w": 40, "h": 13},
        "type": "table",
    },
    "chokepoint_transits": {
        "name": "Chokepoint Transits (physical flow)",
        "description": "IMF PortWatch daily tanker transits through Hormuz / Bab el-Mandeb "
                       "/ Suez; 'reduced' = physical disruption.",
        "endpoint": "chokepoint_transits",
        "gridData": {"w": 30, "h": 10},
        "type": "table",
    },
    "attention": {
        "name": "Attention (Wikipedia)",
        "description": "Pageview spikes on the situation's pages -- surge of global "
                       "attention. Context signal.",
        "endpoint": "attention",
        "gridData": {"w": 30, "h": 10},
        "type": "table",
    },
    "supply_fundamentals": {
        "name": "Supply Fundamentals (EIA)",
        "description": "Physical oil material: Cushing storage, refinery utilization, SPR "
                       "-- stats-safe, weekly.",
        "endpoint": "supply_fundamentals",
        "gridData": {"w": 30, "h": 10},
        "type": "table",
    },
    "opec_stress": {
        "name": "OPEC Fiscal Stress (breakeven vs oil)",
        "description": "Each producer's IMF fiscal breakeven oil price vs live Brent. Negative "
                       "gap = running the budget underwater. The fault line behind OPEC+ "
                       "cohesion (UAE/Qatar comfortable; Iran/Algeria/Saudi stressed).",
        "endpoint": "opec_stress",
        "gridData": {"w": 20, "h": 11},
        "type": "table",
    },
    "chart_oil_map": {
        "name": "Oil Transit Map",
        "description": "The physical map: oil chokepoints sized by throughput (Mb/d, EIA), "
                       "coloured by live status -- red disrupted (PortWatch flow), amber "
                       "watch (active-situation theatre), blue normal. Key oil ports shown.",
        "endpoint": "chart_oil_map",
        "gridData": {"w": 40, "h": 13},
        "type": "chart",
    },
    "commodity_exposure": {
        "name": "Strategic Commodity Exposure",
        "description": "Critical commodities under geopolitical stress -- a key producer "
                       "is in an active situation. Sourced (USGS/WNA/EI/USDA/IEA).",
        "endpoint": "commodity_exposure",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "conflict_intensity": {
        "name": "Conflict Media Intensity (GDELT)",
        "description": "Per active theatre: news coverage VOLUME vs its 7-day baseline "
                       "(surge/elevated/normal/quiet) and TONE. Media claims -- attention & "
                       "sentiment, not verified facts. Free, no token.",
        "endpoint": "conflict_intensity",
        "gridData": {"w": 20, "h": 9},
        "type": "table",
    },
    "analogue_backtest": {
        "name": "Analogue Backtest (does the oil-turbulence forecast work?)",
        "description": "Point-in-time walk-forward: the analogue engine's P(realised oil vol "
                       "rises in 20td) vs what oil actually did, across 52 historical events. "
                       "Brier, skill vs base rate, reliability curve. Honest -- nulls shown.",
        "endpoint": "analogue_backtest",
        "gridData": {"w": 40, "h": 9},
        "type": "markdown",
    },
    "analogue_forecast": {
        "name": "Analogue Forecast (what usually happens next)",
        "description": "kNN over a 511-event seed library: for each active situation, the "
                       "nearest historical analogues by signature and the pattern markets "
                       "showed (oil/equities/gold/VIX). Basis shown; 'thin' = no good analogue.",
        "endpoint": "analogue_forecast",
        "gridData": {"w": 40, "h": 12},
        "type": "table",
    },
    "transmission_chains": {
        "name": "Oil Ripple: Live Transmission Chains",
        "description": "'Everything oil touches' -- transmission paths (trigger -> choke -> "
                       "downstream market) that are LIVE given active situations. Sourced "
                       "mechanism + lag; chokepoint chains first. Context, not magnitude.",
        "endpoint": "transmission_chains",
        "gridData": {"w": 40, "h": 13},
        "type": "table",
    },
    # --- Charts (Plotly) -- the visual layer, not just tables ---
    "chart_brent": {
        "name": "Brent Crude ($/bbl)",
        "description": "Brent spot price (FRED). The market's headline number over time.",
        "endpoint": "chart_brent",
        "gridData": {"w": 20, "h": 9},
        "type": "chart",
    },
    "chart_chokepoints": {
        "name": "Chokepoint Tanker Flow",
        "description": "Daily tanker transits through Hormuz / Bab el-Mandeb / Suez "
                       "(IMF PortWatch) -- the physical-flow trend.",
        "endpoint": "chart_chokepoints",
        "gridData": {"w": 20, "h": 9},
        "type": "chart",
    },
    "chart_attention": {
        "name": "Attention Over Time",
        "description": "Wikipedia pageviews for the situation's pages -- attention spikes.",
        "endpoint": "chart_attention",
        "gridData": {"w": 20, "h": 9},
        "type": "chart",
    },
}


def _lw(i, x, y, w, h):
    """One layout entry (widget id + grid position) for an apps.json tab."""
    return {"i": i, "x": x, "y": y, "w": w, "h": h, "groups": []}


# A ready-made, arranged dashboard (served at /apps.json). 40-column grid.
# Three tabs: the live read, the physical picture, and the historical study.
APPS = [{
    "name": "Ripple Engine",
    "description": "Multi-modal geopolitical-oil intelligence: live read, physical "
                   "supply, and the historical event study.",
    "allowCustomization": True,
    "tabs": {
        "situation": {
            "id": "situation", "name": "Where We Stand",
            "layout": [
                _lw("risk_gauge", 0, 0, 40, 5),
                _lw("risk_vs_priced", 0, 5, 40, 6),
                _lw("where_we_stand", 0, 11, 40, 11),
                _lw("corroborated_events", 0, 22, 20, 9),
                _lw("prediction_markets", 20, 22, 20, 9),
                _lw("chart_chokepoints", 0, 31, 20, 9),
                _lw("chart_attention", 20, 31, 20, 9),
                _lw("engine_read", 0, 40, 20, 9),
                _lw("alert_queue", 20, 40, 20, 9),
                _lw("story_opec", 0, 49, 40, 9),
                _lw("transmission_chains", 0, 58, 40, 13),
                _lw("conflict_intensity", 0, 71, 40, 9),
            ],
        },
        "physical": {
            "id": "physical", "name": "Physical & Market",
            "layout": [
                _lw("chart_oil_map", 0, 0, 40, 13),
                _lw("chart_brent", 0, 13, 40, 9),
                _lw("supply_fundamentals", 0, 22, 20, 9),
                _lw("chokepoint_transits", 20, 22, 20, 9),
                _lw("state_of_system", 0, 31, 20, 9),
                _lw("attention", 20, 31, 20, 9),
                _lw("opec_stress", 0, 40, 20, 11),
                _lw("commodity_exposure", 20, 40, 20, 12),
            ],
        },
        "history": {
            "id": "history", "name": "The Study",
            "layout": [
                _lw("analogue_forecast", 0, 0, 40, 12),
                _lw("analogue_backtest", 0, 12, 40, 9),
                _lw("ripple_by_type", 0, 21, 20, 9),
                _lw("scenario_playbook", 20, 21, 20, 9),
                _lw("event_detail", 0, 30, 40, 11),
                _lw("event_database", 0, 41, 20, 11),
                _lw("propagation_map", 20, 41, 20, 11),
            ],
        },
    },
}]


@app.get("/")
def root():
    return {"status": "ok", "engine": "ripple-engine"}


@app.get("/agents.json")
def agents():
    """OpenBB probes this for a custom AI copilot (a paid feature we don't use). Return an
    empty list so the Workspace stops 404-ing -- no copilot, by design."""
    return []


@app.get("/apps.json")
def apps():
    """A pre-built, arranged dashboard so OpenBB shows a ready-made 'Ripple Engine'
    app (3 tabs) instead of loose widgets to drag around."""
    return APPS


@app.get("/digest", response_class=HTMLResponse)
def digest_page():
    """The Daily -- a calm front page. Re-rendered from committed artifacts on each
    request (cheap). Open http://127.0.0.1:5050/digest in a browser."""
    import digest
    return digest.render()


@app.get("/widgets.json")
def widgets():
    return WIDGETS


@app.get("/state_of_system")
def state_of_system():
    conn = sqlite3.connect(DB)
    signals = build_signals(load_wide(conn))
    conn.close()
    rows = []
    for sid, (name, unit, mech) in MECHANISMS.items():
        if sid not in signals:
            continue
        col = signals[sid].dropna()
        if col.empty:
            continue
        rows.append({
            "signal": name,
            "latest": round(float(col.iloc[-1]), 2),
            "unit": unit,
            "as_of": str(col.index[-1].date()),
            "mechanism": mech,
        })
    return rows


@app.get("/ripple_by_type")
def ripple_by_type():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    events = pd.read_sql("SELECT event_id, event_date, type FROM events", conn)
    conn.close()
    buckets = {}
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is not None:
            buckets.setdefault(ev["type"], []).append(car)
    rows = []
    for etype, cars in sorted(buckets.items()):
        paths = np.vstack(cars)
        mean = paths.mean(axis=0)
        rows.append({
            "event_type": etype,
            "n": len(cars),
            "CAR+1 (%)": round(float(mean[PRE + 1]) * 100, 1),
            "CAR+5 (%)": round(float(mean[PRE + 5]) * 100, 1),
            "CAR+10 (%)": round(float(mean[PRE + 10]) * 100, 1),
            "CAR+20 (%)": round(float(mean[PRE + 20]) * 100, 1),
        })
    return rows


@app.get("/event_detail")
def event_detail():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql(
        "SELECT event_id, event_date, type, severity, surprise FROM events "
        "ORDER BY event_date", conn)
    conn.close()
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)
        def at(sid):
            if sid in signals:
                s = signals[sid].dropna()
                v = s.asof(cutoff) if len(s) else np.nan
                return None if pd.isna(v) else round(float(v), 2)
            return None
        rows.append({
            "event": ev["event_id"],
            "date": ev["event_date"],
            "type": ev["type"],
            "CAR+5 (%)": round(float(car[PRE + 5]) * 100, 1),
            "CAR+20 (%)": round(float(car[PRE + 20]) * 100, 1),
            "VIX %ile (t-1)": at("derived.vix_pct"),
            "Brent vol (t-1)": at("derived.brent_vol20"),
            "USD z (t-1)": at("derived.usd_z"),
            "severity": ev["severity"],
            "surprise": ev["surprise"],
        })
    return rows


@app.get("/event_database")
def event_database():
    conn = sqlite3.connect(DB)
    df = pd.read_sql(
        "SELECT event_id, event_date, type, title, severity, surprise, "
        "confidence, source_url FROM events ORDER BY event_date DESC", conn)
    conn.close()
    return json.loads(df.to_json(orient="records"))


@app.get("/forecast_log")
def forecast_log():
    """The forecast track record. Brier is filled only for resolved forecasts."""
    conn = sqlite3.connect(DB)
    df = pd.read_sql(
        "SELECT forecast_id, question, made_at, my_prob, market_prob, "
        "outcome FROM forecasts ORDER BY forecast_id DESC", conn)
    conn.close()
    rows = []
    for _, r in df.iterrows():
        outcome = None if pd.isna(r["outcome"]) else int(r["outcome"])
        # Brier = (forecast - outcome)^2; only defined once the outcome is known.
        brier = None if outcome is None else round((r["my_prob"] - outcome) ** 2, 3)
        rows.append({
            "id": int(r["forecast_id"]),
            "question": r["question"],
            "made_at": (r["made_at"] or "")[:10],
            "my_prob": round(float(r["my_prob"]), 2) if pd.notna(r["my_prob"]) else None,
            "market_prob": round(float(r["market_prob"]), 2) if pd.notna(r["market_prob"]) else None,
            "outcome": outcome,
            "brier": brier,
        })
    return rows


@app.get("/system_health")
def system_health():
    """Data-freshness panel, read from the JSON heartbeat.py writes."""
    health_path = ROOT / "data" / "health_status.json"
    if not health_path.exists():
        # The file is a runtime artifact -- if heartbeat hasn't run, say so plainly.
        return [{"series": "(no health report yet)",
                 "last_update": "-", "cadence": "-",
                 "status": "run: python3 src/heartbeat.py"}]
    health = json.loads(health_path.read_text())
    rows = [{
        "series": s["series_id"],
        "last_update": s["last_obs"] or "never",
        "cadence": s["frequency"],
        "status": s["status"],
    } for s in health.get("series", [])]
    # Sort worst-first so trouble is at the top of the widget.
    order = {"DEAD": 0, "STALE": 1, "OK": 2}
    rows.sort(key=lambda r: order.get(r["status"], 3))
    # A summary row so the overall state is visible at a glance.
    rows.insert(0, {
        "series": f"== OVERALL: {health.get('overall', '?')} ==",
        "last_update": health.get("generated_at", "")[:16],
        "cadence": f"events={health.get('events_count', '?')}",
        "status": health.get("last_refresh", {}).get("state", "?"),
    })
    return rows


@app.get("/engine_read")
def engine_read():
    """Today's conditional read, from the JSON engine_read.py writes."""
    path = ROOT / "data" / "engine_read.json"
    if not path.exists():
        return [{"item": "(no engine read yet)",
                 "detail": "run: python3 src/engine_read.py",
                 "verdict": "", "amplifier": ""}]
    r = json.loads(path.read_text())
    rows = [{"item": f"READ ({r.get('as_of', '')})", "detail": r.get("read", ""),
             "verdict": "", "amplifier": ""}]
    for hid in ("H1", "H2", "H3"):
        h = r.get("hypotheses", {}).get(hid)
        if not h:
            continue
        rows.append({
            "item": f"{hid} {h['label']}",
            "detail": f"latest {h['latest']} vs event-median {h['event_median']} ({h['unit']})",
            "verdict": h["verdict"],
            "amplifier": h["amplifier"],
        })
    gc = r.get("gpr_context") or {}
    if gc.get("gpr_pct") is not None:
        rows.append({
            "item": "H5 GPR (descriptive)",
            "detail": f"GPR percentile today {gc['gpr_pct']} (index {gc['gpr_value']}, "
                      f"as of {gc['as_of']})",
            "verdict": "exploratory",
            "amplifier": "n/a (no registered direction)",
        })
    return rows


@app.get("/sowhat")
def sowhat():
    """The live so-what read (markdown). Reads data/sowhat.json (src/sowhat.py)."""
    r = _read_json("sowhat.json")
    if not r.get("so_what"):
        return "### The So-What Wire\n\n_run: `python3 src/sowhat.py`_"
    lines = [f"## The So-What Wire — regime: **{r.get('regime','?')}**", "",
             r["so_what"], "", "### Validated propagation (the only claims)"]
    for b in r.get("validated_propagation", []):
        ci = b.get("ci") or [None, None]
        cis = f" · CI [{ci[0]:+.1f}, {ci[1]:+.1f}]" if ci[0] is not None else ""
        lines.append(f"- shock → **{b['to']}** {b['strength']:+.1f}{b['unit']}{cis}")
    lines += ["", "### Active situations (by multi-modal corroboration)"]
    for s in r.get("active_situations", [])[:5]:
        cb = ", ".join(s.get("confirmed_by", [])) or "news only"
        lines.append(f"- **{s['situation']}** — {s['events']} events, {s['multi_modal']} multi-modal "
                     f"[{cb}]; top: {s.get('top_event','')[:60]}")
    lines += ["", f"*{r.get('discipline','')}*"]
    return "\n".join(lines)


@app.get("/domain_conditioning")
def domain_conditioning():
    """Pre-declared apt-conditioning tests. Reads data/domain_conditioning.json."""
    r = _read_json("domain_conditioning.json")
    res = r.get("results")
    if not res:
        return [{"hypothesis": "(none)", "detail": "run: python3 src/domain_conditioning.py"}]
    rows = []
    for x in res:
        if "amp" not in x:
            continue
        ci = x.get("ci") or [None, None]
        rows.append({"hypothesis": x["hypothesis"], "commodity": x["asset"],
                     "conditioner": x["state"].split(".")[-1],
                     "amp": f"{x['amp']:+.1f}%",
                     "ci95": f"[{ci[0]:+.1f},{ci[1]:+.1f}]" if ci[0] is not None else "n/a",
                     "verdict": "VALIDATED" if x.get("validated") else "null"})
    return rows


@app.get("/edge_portfolio")
def edge_portfolio():
    """The pre-registered edge battery, family-wise corrected. Reads data/edge_battery.json.
    Every hypothesis carries a verdict; only 'validated' rows are claims. Nulls shown, not hidden."""
    r = _read_json("edge_battery.json")
    amp = r.get("amplification")
    if not amp:
        return [{"hypothesis": "(none)", "detail": "run: python3 src/edge_battery.py"}]
    rows = []
    for x in sorted(amp, key=lambda z: (not z.get("validated"), z.get("fdr_q") or 1.0)):
        if not x.get("testable"):
            rows.append({"hypothesis": x["hypothesis"], "amp": "n/a", "ci95": "",
                         "perm_p": "", "fdr_q": "", "verdict": "not testable"})
            continue
        ci = x.get("ci") or [None, None]
        unit = x.get("unit", "")
        v = "VALIDATED" if x.get("validated") else ("prior" if x.get("prior") else "null")
        rows.append({"hypothesis": x["hypothesis"], "amp": f"{x['amp']:+.2f}{unit}",
                     "ci95": f"[{ci[0]:+.2f},{ci[1]:+.2f}]" if ci[0] is not None else "n/a",
                     "perm_p": x.get("perm_p"), "fdr_q": x.get("fdr_q"), "verdict": v})
    m = r.get("mispricing") or {}
    if m.get("testable"):
        ci = m.get("wilson_ci") or [None, None]
        rows.append({"hypothesis": "under_priced_risk_oos", "amp": f"{m['turbulence_rate']} turb",
                     "ci95": f"Wilson[{ci[0]},{ci[1]}]", "perm_p": f"base {m['base_rate']}",
                     "fdr_q": "", "verdict": "SUGGESTIVE (small-N)"})
    return rows


@app.get("/engine_status")
def engine_status():
    """One-glance GREEN/AMBER/RED verdict (freshness + coverage + last run + review queue + backups +
    framework soundness). Reads data/engine_status.json."""
    s = _read_json("engine_status.json")
    if not s:
        return [{"row": "(no status yet)", "detail": "run: python3 src/status.py"}]
    rows = [{"row": "VERDICT", "item": s.get("verdict"), "detail": "; ".join(s.get("reasons", []))}]
    fr = s.get("freshness", {}); rows.append({"row": "freshness", "item": fr.get("overall"),
        "detail": f"{fr.get('n_dead')} dead / {fr.get('n_stale')} stale series"})
    cv = s.get("coverage", {}); rows.append({"row": "coverage", "item":
        f"{len(cv.get('undercovered_domains', []))} undercovered", "detail":
        f"{cv.get('n_dead_feeds')} dead feeds"})
    rows.append({"row": "review queue", "item": s.get("review_queue", {}).get("n_pending"),
                 "detail": "LLM-extracted events awaiting your coding"})
    bk = s.get("backups", {}); rows.append({"row": "backups", "item": bk.get("count"),
        "detail": f"restore_tested={bk.get('restore_tested')}"})
    rows.append({"row": "framework", "item": s.get("evaluation", {}).get("framework_sound"),
                 "detail": "placebo null + surfaces consistent"})
    return rows


@app.get("/domain_lens")
def domain_lens(domain: str = "me-risk"):
    """The one validated engine filtered to an analyst domain. Reuses research.lens_data."""
    import research
    r = research.lens_data(domain)
    if not r.get("ok"):
        return [{"row": "(pick a domain)", "detail": ", ".join(r.get("domains", []))}]
    rows = []
    for n in r["validated_nodes"]:
        ci = n["ci"]
        rows.append({"row": "VALIDATED node", "item": n["node"],
                     "value": f"{n['amp']:+.1f}{n['unit']}",
                     "detail": f"CI[{ci[0]:+.1f},{ci[1]:+.1f}] — stress amplifies the ripple here"})
    if r["null_nodes"]:
        rows.append({"row": "null nodes", "item": ", ".join(n["node"] for n in r["null_nodes"]),
                     "value": "", "detail": "no validated amplification (honest)"})
    if r["supply_chain"]:
        val = sum(1 for e in r["supply_chain"] if e["status"] == "validated")
        rows.append({"row": "supply-chain", "item": f"{val}/{len(r['supply_chain'])} validated",
                     "value": "", "detail": "producer→commodity edges (rest null/insufficient)"})
    if r["event_coverage"]:
        rows.append({"row": "event coverage", "item": "", "value": "",
                     "detail": ", ".join(f"{t}={n}" for t, n in r["event_coverage"].items())})
    for s in r["situations"]:
        rows.append({"row": "live situation", "item": s["situation"], "value": f"{s['multi_modal']} multi-modal",
                     "detail": f"{s['events']} corroborated events"})
    return rows


@app.get("/supply_chain")
def supply_chain():
    """Validated supply-chain transmission. Reads data/supply_chain.json (src/supply_chain.py)."""
    r = _read_json("supply_chain.json")
    edges = r.get("all_edges")
    if not edges:
        return [{"edge": "(none)", "detail": "run: python3 src/supply_chain.py"}]
    order = {"validated": 0, "null": 1, "insufficient": 2}
    rows = []
    for e in sorted(edges, key=lambda e: (order.get(e["status"], 3), -(abs(e.get("car") or 0)))):
        ci = e.get("ci") or [None, None]
        rows.append({
            "edge": f"{e['producer']} conflict → {e['commodity']}",
            "producer_share": f"{e.get('producer_share','?')}%",
            "ripple": (f"{e['car']:+.1f}{e['unit']}" if e.get("car") is not None else "—"),
            "ci95": (f"[{ci[0]:+.1f}, {ci[1]:+.1f}]" if ci[0] is not None else f"n={e['n']}"),
            "status": e["status"].upper()})
    return rows


@app.get("/propagation_graph")
def propagation_graph():
    """The validated propagation network. Reads data/propagation_graph.json (src/propagation_graph.py).
    Backbone (validated) + honest null layer + trap flags -- the consequence map with confidence."""
    r = _read_json("propagation_graph.json")
    if not r.get("n_edges"):
        return [{"layer": "(none)", "detail": "run: python3 src/propagation_graph.py"}]
    rows = []
    for e in sorted(r.get("backbone_validated", []), key=lambda e: -abs(e.get("strength") or 0)):
        ci = e.get("ci") or [None, None]
        rows.append({"layer": "BACKBONE (validated)", "edge": f"shock → {e['to']}",
                     "strength": f"{e['strength']:+.1f} {e['unit']}",
                     "ci95": f"[{ci[0]:+.1f}, {ci[1]:+.1f}]" if ci[0] is not None else "n/a",
                     "note": "ripples harder under stress (FDR-corrected)"})
    for e in r.get("node_to_node", []):
        if e.get("status_pre_fdr") == "trap":
            rows.append({"layer": "TRAP (co-move, no lead)", "edge": f"{e['from']} → {e['to']}",
                         "strength": f"contemp {e['contemp_corr']:+.2f}",
                         "ci95": f"lead {e['lead_corr']:+.2f}@{e['lag_days']}d",
                         "note": "co-moves same-day; does NOT reliably lead — don't trade the lead"})
    rows.append({"layer": "— honest —", "edge": "event-type → node (directional)", "strength": "",
                 "ci95": "", "note": "null layer at this N: signed effects mixed/weak, none survive FDR"})
    return rows


@app.get("/ripple_map")
def ripple_map():
    """The conditioned ripple map: does H1 generalize across assets? Reads
    data/cross_asset_conditioned.json (src/cross_asset_conditioned.py). Honest null cells shown."""
    r = _read_json("cross_asset_conditioned.json")
    cells = r.get("map") or []
    if not cells:
        return [{"asset": "(none)", "detail": "run: python3 src/cross_asset_conditioned.py"}]
    rows = []
    for c in cells:
        ci = c.get("ci95") or [None, None]
        cis = f"[{ci[0]:+.1f}, {ci[1]:+.1f}]" if ci[0] is not None else "n/a"
        rows.append({
            "asset": c["label"], "n": c["n_episodes"],
            "amplification": f"{c['amp']:+.1f} {c['unit']}",
            "ci95": cis, "perm_p": c.get("perm_p"),
            "verdict": "GENERALIZES" if c.get("generalizes") else "null (honest)",
        })
    return rows


@app.get("/corroboration_convergence")
def corroboration_convergence():
    """Cross-modal convergence per situation (news/physical/thermal/priced). Reads
    data/corroboration.json (src/corroborate.py). The 'confirmation not headlines' layer."""
    c = _read_json("corroboration.json")
    conv = c.get("convergence") or {}
    sits = c.get("situations") or {}
    if not conv:
        return [{"situation": "(none)", "detail": "run: python3 src/corroborate.py"}]
    rows = []
    for sid, s in conv.items():
        top = s.get("top") or {}
        rows.append({
            "situation": sid.replace("situation.", ""),
            "events": s.get("n_events", 0),
            "multi_modal": f"{s.get('n_multi_modal', 0)} (max {s.get('max_modality_classes', 0)} types)",
            "top_event": (top.get("headline") or "")[:60],
            "confirmed_by": ", ".join(top.get("modality_classes", [])) or "news only",
        })
    rows.sort(key=lambda r: r["events"], reverse=True)
    return rows


@app.get("/gap_board")
def gap_board():
    """The gap board: the live gap + the resolving scorecard, tiered by where the engine disagrees
    with the market's priced vol. Reads data/gaps.json (src/gaps.py). Market-as-null, honestly scored."""
    g = _read_json("gaps.json")
    led = g.get("ledger", {})
    if not led.get("n_scored"):
        return [{"tier": "(none)", "detail": "run: python3 src/gaps.py"}]
    rows = []
    live = g.get("live_gap")
    if live:
        rows.append({"tier": "LIVE", "engine_call": live["engine_call"],
                     "market": f"OVX {live['priced_ovx']} (p{live['priced_ovx_pct']})",
                     "gap": live["gap_direction"], "detail": live["notes"]})
    labels = {"under_priced_risk": "UNDER-PRICED RISK", "over_priced_fear": "OVER-PRICED FEAR",
              "aligned": "aligned (no disagreement)"}
    for d, lbl in labels.items():
        grp = (led.get("by_gap_direction") or {}).get(d)
        if grp:
            ci = grp["turbulence_rate_ci95"]
            rows.append({"tier": lbl, "engine_call": "", "market": f"n={grp['n']}",
                         "gap": f"turb rate {grp['turbulence_rate']}",
                         "detail": f"95% CI [{ci[0]}, {ci[1]}]  ·  Brier {grp['brier']}  "
                                   f"(base rate {led['turbulence_base_rate']})"})
    rows.append({"tier": "— honest —", "engine_call": "", "market": "",
                 "gap": f"overall skill {led['skill_vs_base']:+}",
                 "detail": "SUGGESTIVE, small-N: value is in the DISAGREEMENT, not the average. "
                           "Not yet a validated edge; the ledger tests it as N grows."})
    return rows


@app.get("/track_record")
def track_record():
    """How sure, and scored: H1 walk-forward OOS + the gap ledger Brier + the registry tally.
    The anti-black-box accountability view -- every claim resolves and is scored. Markdown."""
    rb = _read_json("read_backtest.json")
    g = _read_json("gaps.json").get("ledger", {})
    reg = _read_json("signal_registry.json").get("by_status", {})
    lines = ["## Track record — how sure, and scored", "",
             "Everything here resolves and is Brier-scored. Nothing is asserted.", ""]
    if rb.get("n_scored"):
        lines += ["**H1 (the validated edge), walk-forward out-of-sample:**",
                  f"- Conditioning the ripple read on H1 cut error {rb.get('mae_uncond_pp')}pp → "
                  f"{rb.get('mae_cond_pp')}pp (N={rb.get('n_scored')}).",
                  f"- Realized amplification ON vs OFF: **{rb.get('live_amplification_pp'):+.1f}pp** "
                  f"out-of-sample.", ""]
    if g.get("n_scored"):
        lines += ["**The gap ledger (engine view vs market-implied vol), resolved:**",
                  f"- {g['n_scored']} gaps scored; overall skill vs base {g['skill_vs_base']:+} "
                  f"(turbulence base rate {g['turbulence_base_rate']}).",
                  f"- Where the engine *disagrees* with the market it leans right — but the CIs are "
                  f"wide (small-N); suggestive, not yet validated.", ""]
    pg = _read_json("propagation_graph.json")
    bb = pg.get("backbone_validated") or []
    if bb:
        lines += ["**Validated propagation backbone (edges that survived the gate):**",
                  f"- {len(bb)} validated edges: " + ", ".join(f"{e['to']} {e['strength']:+.1f}{e['unit']}"
                                                               for e in bb) + ".", ""]
    if reg:
        lines += ["**Signal registry (status derived from the evidence, not asserted):**",
                  f"- {len(reg.get('live', []))} live · {len(reg.get('experimental', []))} experimental · "
                  f"{len(reg.get('rejected', []))} rejected.", ""]
    lines.append("*This is the glass-box the black boxes can't be: what's proven, how sure, and the "
                 "receipts — including what we rejected.*")
    return "\n".join(lines)


@app.get("/signal_registry")
def signal_registry():
    """The factor-style registry: every tested signal, tiered by its validation evidence.
    Status is derived from the committed artifacts (see src/signal_registry.py), not asserted."""
    reg = _read_json("signal_registry.json")
    sigs = reg.get("signals", [])
    if not sigs:
        return [{"status": "(none)", "name": "run: python3 src/signal_registry.py"}]
    tag = {"live": "LIVE", "experimental": "EXPERIMENTAL", "rejected": "REJECTED"}
    order = {"live": 0, "experimental": 1, "rejected": 2}
    rows = []
    for s in sorted(sigs, key=lambda x: (order.get(x["status"], 3), x["signal_id"])):
        rows.append({
            "tier": tag.get(s["status"], s["status"]),
            "signal": s["name"],
            "mechanism": s["mechanism"],
            "OOS": f"{s['oos_metric']}: {s['oos_value']}",
            "evidence": s["evidence"],
        })
    return rows


@app.get("/h1_live_edge")
def h1_live_edge():
    """THE READ for the one validated edge (H1). Markdown, assembled purely from committed
    artifacts -- validation_claims.json (the receipts) + engine_read.json (today's live
    amplifier state). No new analysis; honest tiering (H2/H3/analogue shown as the nulls
    they are). Never presented as a forecast of whether a shock occurs."""
    vc = _read_json("validation_claims.json")
    er = _read_json("engine_read.json")
    hyps = {h.get("hid"): h for h in vc.get("hypotheses", [])}
    h1 = hyps.get("H1", {})
    h2 = hyps.get("H2", {})
    if not h1:
        return "### H1 — The Validated Edge\n\n_Run `python3 src/validate.py claims` first._"

    n = vc.get("current_sample_events", "?")
    amp = h1.get("amp_pp")
    lo, hi = (h1.get("ci95_pp") or [None, None])[:2]
    doc = h1.get("documented_amp_pp")
    bonf = "survives Bonferroni" if h1.get("survives_bonferroni_5pct") else \
           ("survives FDR@10%" if h1.get("survives_fdr_10pct") else "does not survive correction")

    # today's live amplifier state, from the (frozen-verdict) engine read
    e1 = (er.get("hypotheses") or {}).get("H1", {})
    latest, median = e1.get("latest"), e1.get("event_median")
    ampstate, asof = e1.get("amplifier", "?"), e1.get("as_of_reading", "")

    def pp(x):
        return "n/a" if x is None else f"{x:+.1f}"

    lines = [
        "## H1 — the validated edge",
        "",
        "**Geopolitical shocks ripple harder into oil when market stress (VIX) is already "
        "elevated.** This is the one signal in the engine that has passed the full "
        "validation gate.",
        "",
        "| | |",
        "|---|---|",
        f"| Amplification | **{pp(amp)} pp** ( \\|CAR+20\\|, high-VIX minus low-VIX) |",
        f"| 95% CI | [{pp(lo)}, {pp(hi)}] pp — {'excludes zero' if (lo is not None and lo > 0) else 'spans zero'} |",
        f"| Significance | perm p={h1.get('perm_p_raw')}, FDR q={h1.get('fdr_qvalue')}, **{bonf}** |",
        f"| Sample | N={n} events (1987–2025); frozen pre-registered anchor n=20 |",
        f"| Trajectory | {pp(doc)}pp (n=20) → {pp(amp)}pp (n={n}) — *strengthened as N grew* |",
        "",
        "### Today",
    ]
    if latest is not None and median is not None:
        lines.append(f"VIX at **{latest} percentile** vs the event-sample median **{median}** "
                     f"→ **H1 amplifier {ampstate}** *(as of {asof})*.")
        # H1-ONLY read sentence -- deliberately NOT the engine_read.json line, which still
        # mentions H2 as an amplifier (it reads the frozen n=20 verdict where H2 held; H2 is
        # now a null at N=161). Keeping this H1-only avoids contradicting the honest tier below.
        mood = ("psychologically stressed — a shock today would ripple toward the WIDER end of "
                "its historical range" if ampstate == "ON" else
                "psychologically calm — a shock today would ripple toward the NARROWER end of "
                "its historical range")
        lines += ["", f"> A supply shock today would land on a market that is {mood}."]
    else:
        lines.append("_Live VIX reading unavailable — run `python3 src/engine_read.py`._")
    # walk-forward accountability -- does using H1 actually improve the read out-of-sample?
    rb = _read_json("read_backtest.json")
    if rb.get("n_scored"):
        reg = rb.get("by_regime", {})
        on = reg.get("ON", {}).get("mean_realized_pp")
        off = reg.get("OFF", {}).get("mean_realized_pp")
        lines += [
            "",
            "### Does it actually help? (walk-forward accountability)",
            f"Replaying every shock using only prior events, conditioning the expected ripple on "
            f"H1 cut the out-of-sample error from **{rb.get('mae_uncond_pp')}pp** to "
            f"**{rb.get('mae_cond_pp')}pp** (N={rb.get('n_scored')}).",
        ]
        if on is not None and off is not None:
            lines.append(f"Realized \\|CAR+20\\| ran **{on}pp** when H1 was ON vs **{off}pp** "
                         f"when OFF (**{rb.get('live_amplification_pp'):+.1f}pp**) — the edge "
                         f"holds *forward*, not just in-sample.")
    lines += [
        "",
        "### The honest tier (what is *not* an edge)",
        f"- **H2** (tight inventories): NULL at N={n} ({pp(h2.get('amp_pp'))}pp, CI includes 0) "
        "— the n=20 \"hold\" was small-sample noise.",
        "- **H3** (crowded positioning): rejected (wrong direction).",
        "- **Analogue turbulence forecaster**: no OOS edge (CPCV skill −0.14, PBO 0.0, "
        "Diebold-Mariano p=0.0002 — the base rate wins).",
        "- **kNN state-signature probability**: no validated edge on the de-overlapped sample "
        "(PBO 0.44, DM p=0.11) — the apparent all-events skill was a clustering artifact.",
        "",
        "*Receipts: `data/validation_claims.json`, `data/registered_sample_n20.csv` "
        "(`REGISTERED_SAMPLE.md`). A conditional read of history, not a forecast — the engine "
        "never predicts whether a shock occurs, only how oil has rippled when one did.*",
    ]
    return "\n".join(lines)


@app.get("/scenario_playbook")
def scenario_playbook():
    """One row per event type: clustered base-rate ripple + today's conditioning.
    Computed live (like the other analytic widgets); the amplifier context is the
    same current-state summary for every row."""
    try:
        import scenario
        pb = scenario.build_playbook()
    except Exception as e:                     # never 500 the dashboard
        return [{"event_type": "(error)", "n": "", "note": str(e)[:100]}]
    today = scenario.conditioning_summary(pb["conditioning"])
    gc = pb.get("gpr_context") or {}
    if gc.get("gpr_pct") is not None:      # descriptive only -- never an amplifier
        today += f" | GPR p{gc['gpr_pct']} (desc)"
    rows = []
    for c in pb["cards"]:
        b = c["base"]
        fmt = lambda k: f"{b[k]:+.1f}%" if k in b else "-"
        rng = (f"[{b['car20_min']:+.1f}%, {b['car20_max']:+.1f}%]"
               if "car20_min" in b else "-")
        rows.append({
            "event_type": c["type"],
            "n": c["n"],
            "CAR+1": fmt("car1"), "CAR+5": fmt("car5"),
            "CAR+10": fmt("car10"), "CAR+20": fmt("car20"),
            "range(CAR+20)": rng,
            "today": today,
        })
    return rows


@app.get("/propagation_map")
def propagation_map():
    """Cross-asset grid: clustered mean CAR+20 per event type x asset.
    Descriptive only -- units differ (% for prices, bps for yields)."""
    try:
        import cross_asset
        conn = sqlite3.connect(DB)
        summary = cross_asset.propagation_summary(cross_asset.build_table(conn))
        conn.close()
    except Exception as e:
        return [{"event_type": "(error)", "note": str(e)[:100]}]
    rows = []
    for etype, info in summary.items():
        row = {"event_type": etype, "n": info["n_type"]}
        for a in cross_asset.ASSETS:
            v = info["cells"][a["series"]]["car20"]
            row[a["label"]] = "n/a" if v is None else f"{v:+.1f}{a['unit']}"
        rows.append(row)
    return rows


@app.get("/alert_queue")
def alert_queue():
    """The watcher's alert cards, newest first. Read-only view; Joe edits status
    in the CSV. These are curated attention -- never conclusions."""
    path = ROOT / "data" / "alert_queue.csv"
    if not path.exists():
        return [{"timestamp_utc": "(no alerts yet)",
                 "headline": "run: python3 src/watcher.py", "source": "",
                 "heuristic_type": "", "status": ""}]
    df = pd.read_csv(path).fillna("")
    df = df.iloc[::-1]                                    # newest first
    rows = []
    for _, r in df.head(200).iterrows():
        rows.append({
            "timestamp_utc": str(r.get("timestamp_utc", ""))[:16],
            "source": r.get("source", ""),
            "heuristic_type": r.get("heuristic_type", ""),
            "headline": str(r.get("headline", ""))[:90],
            "matched": f"{r.get('matched_keywords', '')} / {r.get('matched_entities', '')}"[:40],
            "status": r.get("status", ""),
            "url": r.get("url", ""),
        })
    return rows


# ----------------------------------------------------------------------------
# Enrichment-layer widgets -- read the pipeline's JSON artifacts (generated by
# refresh.py). Each returns a list of row-dicts (OpenBB table format).
# ----------------------------------------------------------------------------

@app.get("/corroborated_events")
def corroborated_events():
    """The corroboration brain's output: events scored by independent-source
    convergence. Confidence, not fact."""
    data = _read_json("corroboration.json")
    rows = []
    for sid, evs in (data.get("situations") or {}).items():
        for e in evs:
            rows.append({
                "confidence": f"{e.get('confidence', 0) * 100:.0f}%",
                "tag": e.get("tag", ""),
                "sources": e.get("n_independent_sources", 0),
                "modalities": ", ".join(e.get("modalities", [])),
                "kind": e.get("kind", ""),
                "headline": (e.get("headline") or "")[:90],
                "as_of": e.get("latest_ts", ""),
            })
    rows.sort(key=lambda r: r["confidence"], reverse=True)
    return rows or [{"headline": "(run corroborate.py)", "tag": "", "confidence": ""}]


@app.get("/prediction_markets")
def prediction_markets():
    """Market-implied probabilities (Polymarket). Context only."""
    mk = _read_json("predmkt.json").get("markets", [])
    rows = [{"probability": f"{m.get('prob', 0) * 100:.0f}%",
             "outcome": m.get("outcome", ""),
             "question": (m.get("question") or "")[:90],
             "volume_usd": f"{m.get('volume', 0):,.0f}",
             "ends": m.get("end_date", "")} for m in mk[:60]]
    return rows or [{"question": "(run fetch_predmkt.py)", "probability": ""}]


@app.get("/chokepoint_transits")
def chokepoint_transits():
    """IMF PortWatch daily tanker transits + disruption flag."""
    cps = _read_json("portwatch.json").get("chokepoints", [])
    rows = [{"chokepoint": c.get("chokepoint", ""), "tankers": c.get("latest", ""),
             "vs_median": f"{c.get('pct_of_median', '')}x", "flag": c.get("flag", ""),
             "as_of": c.get("latest_date", "")} for c in cps]
    return rows or [{"chokepoint": "(run fetch_portwatch.py)", "flag": ""}]


@app.get("/attention")
def attention():
    """Wikipedia pageview spikes -- the attention modality (context)."""
    pg = _read_json("wiki_attention.json").get("pages", [])
    rows = [{"page": p.get("page", ""), "views": f"{p.get('latest', 0):,}",
             "vs_median": f"{p.get('pct_of_median', '')}x", "flag": p.get("flag", "")}
            for p in pg]
    return rows or [{"page": "(run fetch_wiki_attention.py)", "flag": ""}]


@app.get("/supply_fundamentals")
def supply_fundamentals():
    """Physical oil material: Cushing storage, refinery utilization, SPR (EIA)."""
    conn = sqlite3.connect(DB)
    out = []
    for label, sid, unit in (("Cushing crude stocks", "eia.cushing_stocks", "kbbl"),
                             ("Refinery utilization", "eia.refinery_util", "%"),
                             ("SPR crude stocks", "eia.spr_stocks", "kbbl")):
        row = conn.execute("SELECT obs_date, value FROM observations WHERE "
                           "series_id=? ORDER BY obs_date DESC LIMIT 1", (sid,)).fetchone()
        if row:
            out.append({"series": label, "latest": round(row[1], 1),
                        "unit": unit, "as_of": row[0]})
    conn.close()
    return out or [{"series": "(run fetch_eia_fundamentals.py)", "latest": ""}]


@app.get("/story_opec")
def story_opec():
    """The OPEC Fiscal Stress story as a legible markdown card (src/story.py)."""
    s = _read_json("stories/opec_fiscal_stress.state.json", {})
    if not s or "read" not in s:
        return "_Run `python3 src/story.py` (after fetch_breakevens.py) to build the story._"
    top = s.get("board", [])[:5]
    rows = "".join(f"| {r['country']} | ${r['breakeven']} | {r['gap']:+.1f} | {r['band']} |\n"
                   for r in top)
    changes = s.get("changes") or []
    chg = ("\n".join(f"- ⚠️ {c}" for c in changes)) if changes else "_no material change since last run_"
    wn = s.get("whats_next") or {}
    return (
        f"### {s.get('title','')} &nbsp;·&nbsp; _{s.get('as_of','')}_\n\n"
        f"**{s.get('n_underwater')}/{len(s.get('board',[]))} producers underwater at Brent "
        f"${s.get('brent')}.**\n\n"
        f"| most stressed | breakeven | gap | band |\n|---|---|---|---|\n{rows}\n"
        f"**What changed:**\n{chg}\n\n"
        f"**Next catalyst:** {wn.get('event','—')}"
        + (f" — in {wn['days_away']}d ({wn['date']})" if wn else "") + "\n\n"
        f"**Watch:** {', '.join(s.get('watch_gauges', [])) or '—'}\n")


@app.get("/opec_stress")
def opec_stress():
    """OPEC producers ranked by fiscal stress: IMF breakeven vs live Brent (src/fetch_
    breakevens.py). Negative gap = the state is running its oil budget underwater."""
    d = _read_json("breakevens.json", {})
    rows = [{"country": r["country"], "breakeven": f"${r['breakeven']}",
             "brent": f"${r.get('brent','')}", "gap": f"{r['gap']:+.2f}" if r.get("gap") is not None else "-",
             "stress": r.get("band", "")} for r in d.get("producers", [])]
    return rows or [{"country": "(run src/fetch_breakevens.py)", "breakeven": ""}]


@app.get("/commodity_exposure")
def commodity_exposure():
    """Strategic commodities under geopolitical stress: a supply-critical producer is
    in an ACTIVE situation. Sourced concentration (criticality.yaml). DISPLAY/context."""
    risks = _read_json("criticality.json", {}).get("commodities_at_risk", [])
    rows = []
    for r in risks:
        who = ", ".join(f"{c['country']} {c['share']}%"
                        for c in r.get("at_risk_countries", []))
        rows.append({"commodity": r["commodity"], "stage": r.get("stage", ""),
                     "at_risk_share": f"{r.get('at_risk_share', 0)}%",
                     "producers_in_conflict": who, "source": r.get("source", "")})
    return rows or [{"commodity": "(run src/criticality.py)", "stage": ""}]


@app.get("/conflict_intensity")
def conflict_intensity():
    """Per-situation media coverage volume + tone (src/fetch_conflict_intensity.py)."""
    sits = _read_json("conflict_intensity.json", {}).get("situations", [])
    rows = [{"situation": s.get("situation", ""), "intensity": s.get("band", ""),
             "volume_vs_baseline": f"x{s.get('vol_ratio')}" if s.get("vol_ratio") else "-",
             "tone": s.get("tone"), "mood": s.get("mood", "")} for s in sits]
    return rows or [{"situation": "(run fetch_conflict_intensity.py)", "intensity": ""}]


@app.get("/analogue_backtest")
def analogue_backtest():
    """The honest calibration verdict on the analogue oil-spike forecast (src/backtest_
    analogue.py) -- rendered as markdown, nulls and negative skill shown, not hidden."""
    r = _read_json("backtest_analogue.json", {})
    if not r or not r.get("n_scored"):
        return "_Run `python3 src/backtest_analogue.py` to score the analogue forecast._"
    skill = r.get("skill_vs_base", 0)
    verdict = ("**carries information** (beats the base rate)" if skill > 0.01
               else "**no skill yet** — does not beat just predicting the base rate")
    rows = "".join(f"| {b['range']} | {b['n']} | {b['mean_pred']} | {b['mean_outcome']} |\n"
                   for b in r.get("reliability", []))
    return (
        f"### Analogue oil-spike forecast — calibration &nbsp;·&nbsp; _{r.get('as_of','')}_\n\n"
        f"Point-in-time walk-forward over **{r.get('n_scored')}/{r.get('n_events')}** events "
        f"(prior-only analogues). Target: {r.get('target','')}.\n\n"
        f"| metric | value |\n|---|---|\n"
        f"| Brier (engine) | **{r.get('brier')}** |\n"
        f"| Brier (base rate) | {r.get('base_rate_brier')} |\n"
        f"| skill vs base | **{skill:+}** |\n"
        f"| base rate of spikes | {r.get('base_rate')} |\n\n"
        f"**Verdict:** the analogue non-clean (turbulence) share {verdict}.\n\n"
        f"| pred range | n | mean pred | realised |\n|---|---|---|---|\n{rows}\n"
        f"_{r.get('note','')}_")


@app.get("/analogue_forecast")
def analogue_forecast():
    """The analogue probability function (src/analogue.py): for each active situation, the
    historical playbook -- what oil/equities/gold/VIX usually did in the nearest analogues,
    with confidence and the single closest historical match."""
    def _cell(ka, tok):
        v = ka.get(tok)
        return f"{v['dominant']} {int(v['share']*100)}%" if v else "-"
    rows = []
    for fc in _read_json("analogue.json", {}).get("forecasts", []):
        ka = fc.get("key_assets", {})
        c = fc.get("confidence", {})
        near = (fc.get("nearest") or [{}])[0]
        rows.append({
            "situation": fc.get("situation", ""),
            "confidence": f"{c.get('band','')} (N={c.get('n','')})",
            "oil": _cell(ka, "wti") if ka.get("wti") else _cell(ka, "brent"),
            "equities": _cell(ka, "sp500"), "gold": _cell(ka, "gold"),
            "vix": _cell(ka, "vix"), "10y": _cell(ka, "10y_treasury"),
            "nearest_analogue": f"{near.get('event_id','')} ({near.get('score','')})"})
    return rows or [{"situation": "(run src/analogue.py)", "confidence": ""}]


@app.get("/transmission_chains")
def transmission_chains():
    """'Everything oil touches': the transmission paths that are LIVE given the active
    situations -- trigger geography -> choke -> downstream market, with sourced mechanism
    and lag. Chokepoint chains first (the sharp, hard-to-substitute paths)."""
    live = _read_json("propagation.json", {}).get("live_chains", [])
    rows = []
    for d in live:
        kind = "CHOKEPOINT" if d.get("geometry") == "chokepoint" else "bulk"
        rows.append({"chain": d["chain"], "type": kind,
                     "triggered_by": ", ".join(d.get("triggered_by", [])),
                     "choke": d.get("choke", ""), "downstream": d.get("downstream", ""),
                     "lag": d.get("lag", ""), "source": d.get("source", "")})
    return rows or [{"chain": "(run src/propagation.py)", "type": ""}]


@app.get("/risk_gauge")
def risk_gauge():
    """The headline KPI row (metric widget): escalation, amplifiers, chokepoint
    status, top corroboration, and what's priced -- all from committed artifacts."""
    er = _read_json("engine_read.json")
    cards = []

    # Brent + day change.
    conn = sqlite3.connect(DB)
    bx, by = _series(conn, "fred.DCOILBRENTEU", 5)
    conn.close()
    if by:
        delta = f"{by[-1] - by[-2]:+.2f}" if len(by) > 1 else "0"
        cards.append({"label": "Brent ($/bbl)", "value": f"{by[-1]:.2f}", "delta": delta})

    # Amplifiers (H1/H2 ON) + GPR percentile.
    hyp = er.get("hypotheses", {})
    on = [h for h in ("H1", "H2") if hyp.get(h, {}).get("amplifier") == "ON"]
    cards.append({"label": "Amplifiers ON", "value": f"{len(on)}/2 ({'+'.join(on) or 'none'})",
                  "delta": "0"})
    gpr = (er.get("gpr_context") or {}).get("gpr_pct")
    if gpr is not None:
        cards.append({"label": "Geopolitical risk %ile", "value": f"{gpr}", "delta": "0"})

    # Chokepoint status (worst-flagged) from PortWatch.
    cps = _read_json("portwatch.json").get("chokepoints", [])
    hot = [c for c in cps if c.get("flag") in ("reduced", "elevated")]
    pick = hot[0] if hot else (cps[0] if cps else None)
    if pick:
        cards.append({"label": f"{pick['chokepoint'][:16]} flow",
                      "value": f"{pick.get('latest','')} ({pick.get('flag','')})",
                      "delta": f"{(pick.get('pct_of_median') or 1) - 1:+.2f}"})

    # Top corroborated event confidence.
    cor = [e for evs in (_read_json("corroboration.json").get("situations") or {}).values()
           for e in evs]
    if cor:
        top = max(cor, key=lambda e: e.get("confidence", 0))
        cards.append({"label": "Top corroboration", "value": f"{top['confidence']*100:.0f}% "
                      f"({top['tag']})", "delta": "0"})

    # Attention: the top-spiking page.
    pages = [p for p in _read_json("wiki_attention.json").get("pages", [])
             if p.get("flag") in ("spike", "elevated")]
    if pages:
        top = max(pages, key=lambda p: p.get("pct_of_median", 0))
        cards.append({"label": "Attention spike", "value": f"{top['page'][:16]} "
                      f"{top['pct_of_median']}x", "delta": "0"})
    return cards or [{"label": "Engine", "value": "run refresh.py", "delta": "0"}]


@app.get("/risk_vs_priced")
def risk_vs_priced():
    """The SOURCE-AWARE transmission read (src/gpr_signal.py): is the risk supply- or demand-
    channel, and does the REAL oil move confirm or contradict it? Replaces the old vol-only
    'aligned' read that contradicted reality."""
    s = _read_json("gpr_signal.json", {})
    if not s or "error" in s or "transmission" not in s:
        return "_Run `python3 src/gpr_signal.py` (after fetch_market_live.py) for the read._"
    g, t, o = s["gpr"], s["transmission"], s.get("oil_live", {})
    return (
        f"### Risk vs Priced &nbsp;·&nbsp; source-aware &nbsp;·&nbsp; _{s.get('as_of','')}_\n\n"
        f"**{s.get('headline','')}**\n\n"
        f"| | |\n|---|---|\n"
        f"| Geopolitical risk (GPR) | {g['percentile']}th pct — **{g['band']}** |\n"
        f"| Transmission channel | **{t.get('channel','')}** (expected oil: {t.get('expected','')}) |\n"
        f"| Real Brent move | {o.get('chg1d')}% 1d, **{o.get('chg5d')}% 5d** |\n"
        f"| Verdict | **{t.get('flag','')}** |\n\n"
        f"- **Read:** {t.get('verdict','')}\n"
        f"- **GPR posture:** {g.get('posture','')}\n"
        f"- **Live chokepoint chains:** {s.get('live_chokepoint_chains','n/a')}\n\n"
        f"_{s.get('note','')}_")


@app.get("/where_we_stand")
def where_we_stand(situation: str = _SIT_DEFAULT):
    """The chosen situation's dossier as prose (markdown), trimmed to the read (the
    full timeline table lives in its own widget). Driven by the Situation dropdown."""
    md = DATA / "situations" / f"{situation}.md"
    if not md.exists():
        return f"_No dossier for **{situation}** yet — run `python3 src/situation.py`._"
    text = md.read_text()
    # Keep everything up to the raw timeline table (synthesis + priced-state + odds).
    cut = text.find("## Timeline")
    return text[:cut].strip() if cut > 0 else text


def oil_map_status(flag, adj_active):
    """Status bucket for a chokepoint: physical-flow anomaly (PortWatch) wins; else whether
    its theatre is in an active situation; else normal. Pure -- unit-tested."""
    if flag == "reduced":
        return "disrupted"
    if flag == "elevated":
        return "elevated"
    return "watch" if adj_active else "normal"


_STATUS_COLOR = {"disrupted": "#e8663a", "elevated": "#d9a441",
                 "watch": "#c9b23a", "normal": "#4a90d9"}


@app.get("/chart_oil_map")
def chart_oil_map():
    """The physical oil map (Plotly scattergeo, no map token): chokepoints sized by mb/d,
    coloured by live status (PortWatch flow anomaly + active-situation theatre), key oil
    ports as reference. The geography is sourced in data/oil_map.yaml (EIA)."""
    import yaml
    cfg = yaml.safe_load((DATA / "oil_map.yaml").read_text()) or {}
    pw = {c.get("chokepoint"): c.get("flag")
          for c in _read_json("portwatch.json", {}).get("chokepoints", [])}
    active = set(_read_json("propagation.json", {}).get("active_situation_countries", []))

    lat, lon, size, color, text = [], [], [], [], []
    for slug, c in (cfg.get("chokepoints") or {}).items():
        adj_active = any(a in active for a in c.get("adjacent", []))
        status = oil_map_status(pw.get(slug), adj_active)
        lat.append(c["lat"]); lon.append(c["lon"])
        size.append(9 + float(c.get("mbd", 3)))
        color.append(_STATUS_COLOR[status])
        text.append(f"{c['name']} — {c.get('mbd','?')} Mb/d — {status}")
    choke = {"type": "scattergeo", "lat": lat, "lon": lon, "text": text, "mode": "markers",
             "name": "chokepoints", "hoverinfo": "text",
             "marker": {"size": size, "color": color, "line": {"width": 0.5, "color": "#0b0d10"},
                        "opacity": 0.9}}

    plat, plon, ptext = [], [], []
    for slug, p in (cfg.get("ports") or {}).items():
        plat.append(p["lat"]); plon.append(p["lon"]); ptext.append(p["name"])
    ports = {"type": "scattergeo", "lat": plat, "lon": plon, "text": ptext, "mode": "markers",
             "name": "oil ports", "hoverinfo": "text",
             "marker": {"size": 6, "color": "#8a93a3", "symbol": "diamond"}}

    return {
        "data": [choke, ports],
        "layout": {"title": {"text": "Oil transit map — chokepoints by throughput & status"},
                   "margin": {"t": 40, "r": 0, "b": 0, "l": 0},
                   "paper_bgcolor": "rgba(0,0,0,0)", "font": {"color": "#c7ccd6"},
                   "legend": {"orientation": "h"}, "template": "plotly_dark",
                   "geo": {"projection": {"type": "natural earth"}, "bgcolor": "rgba(0,0,0,0)",
                           "showland": True, "landcolor": "#1a1d24", "showocean": True,
                           "oceancolor": "#0f1116", "showcountries": True,
                           "countrycolor": "#2a2e37", "coastlinecolor": "#2a2e37"}},
    }


@app.get("/chart_brent")
def chart_brent():
    """Brent spot price line chart (Plotly)."""
    conn = sqlite3.connect(DB)
    x, y = _series(conn, "fred.DCOILBRENTEU", 180)
    conn.close()
    return _line_fig("Brent crude spot ($/bbl)", [("Brent", x, y)], "$/bbl")


@app.get("/chart_chokepoints")
def chart_chokepoints():
    """Daily tanker transits through the key chokepoints (Plotly, multi-line)."""
    conn = sqlite3.connect(DB)
    traces = []
    for name, slug in (("Hormuz", "hormuz"), ("Bab el-Mandeb", "bab_el_mandeb"),
                       ("Suez", "suez")):
        x, y = _series(conn, f"portwatch.{slug}.n_tanker", 120)
        traces.append((name, x, y))
    conn.close()
    return _line_fig("Chokepoint tanker transits / day (IMF PortWatch)", traces,
                     "tankers/day")


@app.get("/chart_attention")
def chart_attention():
    """Wikipedia pageviews over time for the situation's pages (Plotly, multi-line)."""
    conn = sqlite3.connect(DB)
    traces = []
    for name, slug in (("Hormuz", "hormuz"), ("Bab el-Mandeb", "bab_el_mandeb"),
                       ("Iran war", "iran_war")):
        x, y = _series(conn, f"wiki.views.{slug}", 90)
        traces.append((name, x, y))
    conn.close()
    return _line_fig("Wikipedia pageviews (attention)", traces, "views/day")


if __name__ == "__main__":
    print(f"Ripple Engine backend -> http://127.0.0.1:{PORT}")
    print("In OpenBB Workspace: Apps -> Connect backend -> "
          f"URL http://127.0.0.1:{PORT}")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
