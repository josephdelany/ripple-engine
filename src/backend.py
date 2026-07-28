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
    "commodity_exposure": {
        "name": "Strategic Commodity Exposure",
        "description": "Critical commodities under geopolitical stress -- a key producer "
                       "is in an active situation. Sourced (USGS/WNA/EI/USDA/IEA).",
        "endpoint": "commodity_exposure",
        "gridData": {"w": 40, "h": 12},
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
                _lw("where_we_stand", 0, 5, 40, 11),
                _lw("corroborated_events", 0, 16, 20, 9),
                _lw("prediction_markets", 20, 16, 20, 9),
                _lw("chart_chokepoints", 0, 25, 20, 9),
                _lw("chart_attention", 20, 25, 20, 9),
                _lw("engine_read", 0, 34, 20, 9),
                _lw("alert_queue", 20, 34, 20, 9),
            ],
        },
        "physical": {
            "id": "physical", "name": "Physical & Market",
            "layout": [
                _lw("chart_brent", 0, 0, 40, 9),
                _lw("supply_fundamentals", 0, 9, 20, 9),
                _lw("chokepoint_transits", 20, 9, 20, 9),
                _lw("state_of_system", 0, 18, 20, 9),
                _lw("attention", 20, 18, 20, 9),
                _lw("commodity_exposure", 0, 27, 40, 12),
            ],
        },
        "history": {
            "id": "history", "name": "The Study",
            "layout": [
                _lw("ripple_by_type", 0, 0, 20, 9),
                _lw("scenario_playbook", 20, 0, 20, 9),
                _lw("event_detail", 0, 9, 40, 11),
                _lw("event_database", 0, 20, 20, 11),
                _lw("propagation_map", 20, 20, 20, 11),
            ],
        },
    },
}]


@app.get("/")
def root():
    return {"status": "ok", "engine": "ripple-engine"}


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
