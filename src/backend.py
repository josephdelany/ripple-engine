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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from derive_signals import load_wide, build_signals, MECHANISMS
from event_study import load_returns, car_for_event, PRE

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
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
}


@app.get("/")
def root():
    return {"status": "ok", "engine": "ripple-engine"}


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


if __name__ == "__main__":
    print(f"Ripple Engine backend -> http://127.0.0.1:{PORT}")
    print("In OpenBB Workspace: Apps -> Connect backend -> "
          f"URL http://127.0.0.1:{PORT}")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
