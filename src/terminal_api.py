"""
terminal_api.py -- the Oil & Petro Products TERMINAL (served at /terminal).

A fully interactive time-series terminal for tracking real oil & petro-products over time.
It READS ONLY real observations already in data/oil.db (the same series the engine fetches);
it never fabricates a point. Registered onto the existing FastAPI app with one line in
backend.py, so it cannot touch or break any existing endpoint.

Endpoints added:
  GET /terminal              -> the self-contained terminal page (src/terminal.html)
  GET /term_catalog          -> the tracked-product catalog, grouped, with latest value +
                                changes (1-period / 5-period / ~1y) + coverage + stale flag
  GET /term_series?id=&frm=&to=  -> the real observation points for one series (for charting)

Honesty: every point is a stored observation with its as_of; long daily series are evenly
DOWNSAMPLED for rendering (flagged), never smoothed or interpolated; a value we don't have
is absent, not guessed.
"""
from __future__ import annotations

import datetime as _dt
import math

from fastapi.responses import HTMLResponse, JSONResponse

from _db import connect
from pathlib import Path

import json

import shock_tracer
import escalation
import propagate

ROOT = Path(__file__).resolve().parent.parent
TERMINAL_HTML = ROOT / "src" / "terminal.html"
TRACE_HTML = ROOT / "src" / "trace.html"
BACKTEST_HTML = ROOT / "src" / "backtest.html"
QUESTION_HTML = ROOT / "src" / "question.html"
SITUATION_HTML = ROOT / "src" / "situation.html"

# Curated catalog: series_id -> (group, display label). Only those actually present in
# oil.db (with observations) are shown; anything missing is silently skipped (no fake rows).
CATALOG = [
    ("Crude", [
        ("fred.DCOILBRENTEU", "Brent Crude (spot)"),
        ("fred.DCOILWTICO", "WTI Crude (spot)"),
        ("derived.brent_wti_spread", "Brent–WTI spread"),
    ]),
    ("Refined products", [
        ("fred.DGASUSGULF", "Gulf Coast gasoline"),
        ("fred.DHOILNYH", "Heating oil / diesel (NYH)"),
        ("fred.GASREGW", "US retail gasoline"),
    ]),
    ("Refining margins (cracks)", [
        ("derived.gasoline_crack", "Gasoline crack"),
        ("derived.diesel_crack", "Diesel/heating-oil crack"),
    ]),
    ("Natural gas & LNG", [
        ("fred.DHHNGSP", "Henry Hub gas (US)"),
        ("yf.ttf", "TTF gas (Europe)"),
        ("yf.jkm", "JKM LNG (Asia)"),
    ]),
    ("NGLs", [
        ("fred.DPROPANEMBTX", "Propane (Mont Belvieu)"),
    ]),
    ("Volatility & positioning", [
        ("fred.OVXCLS", "OVX (oil implied vol)"),
        ("derived.brent_vol20", "Brent realised vol (20d)"),
        ("cftc.mm_net_wti", "WTI managed-money net"),
    ]),
    ("Inventories (US)", [
        ("eia.crude_stocks_xspr", "Crude stocks (ex-SPR)"),
        ("eia.cushing_stocks", "Cushing stocks"),
        ("eia.spr_stocks", "SPR stocks"),
    ]),
    ("Petrochemical / fertilizer", [
        ("fred.PCU325311325311", "Nitrogen fertilizer PPI"),
    ]),
    ("Credit context", [
        ("fred.BAMLH0A0HYM2", "US high-yield spread"),
    ]),
    ("Chokepoint flows (AIS transits)", [
        ("portwatch.hormuz.n_tanker", "Hormuz tanker transits"),
        ("portwatch.bab_el_mandeb.n_tanker", "Bab-el-Mandeb transits"),
        ("portwatch.suez.n_tanker", "Suez transits"),
        ("portwatch.cape_of_good_hope.n_tanker", "Cape of Good Hope transits"),
    ]),
    ("Cross-asset context", [
        ("yf.sp500", "S&P 500"), ("yf.gold", "Gold"), ("yf.copper", "Copper"),
        ("yf.silver", "Silver"), ("yf.palladium", "Palladium"),
        ("yf.platinum", "Platinum"), ("yf.wheat", "Wheat"),
        ("fred.DGS5", "5Y Treasury yield"), ("fred.DGS10", "10Y Treasury yield"),
    ]),
    ("Regime & stress signals", [
        ("derived.conflict_intensity_pct", "Conflict intensity %ile"),
        ("derived.curve_2s10s", "2s10s curve"),
        ("derived.credit_stress", "Credit stress"),
        ("derived.usd_z", "USD (z-score)"),
        ("derived.brent_wti_spread_z", "Brent–WTI spread (z)"),
    ]),
]

_STALE_DAYS = {"daily": 8, "weekly": 16, "monthly": 45}


def _meta(cur, sid):
    row = cur.execute("SELECT name, unit, frequency, source, source_url FROM series WHERE series_id=?",
                      (sid,)).fetchone()
    return row


def _one(cur, sid, order="DESC", offset=0):
    r = cur.execute(f"SELECT obs_date, value, as_of FROM observations WHERE series_id=? "
                    f"ORDER BY obs_date {order} LIMIT 1 OFFSET ?", (sid, offset)).fetchone()
    return r


def _asof_1y(cur, sid, end_date):
    try:
        cutoff = (_dt.date.fromisoformat(end_date) - _dt.timedelta(days=365)).isoformat()
    except Exception:
        return None
    return cur.execute("SELECT value FROM observations WHERE series_id=? AND obs_date<=? "
                       "ORDER BY obs_date DESC LIMIT 1", (sid, cutoff)).fetchone()


def _pct(latest, ref):
    if ref in (None, 0) or latest is None:
        return None
    return round((latest / ref - 1.0) * 100.0, 2)


def catalog():
    conn = connect(read_only=True)
    cur = conn.cursor()
    today = _dt.date.today()
    groups = []
    for gname, items in CATALOG:
        rows = []
        for sid, label in items:
            meta = _meta(cur, sid)
            if not meta:
                continue
            agg = cur.execute("SELECT COUNT(*), MIN(obs_date), MAX(obs_date) FROM observations "
                              "WHERE series_id=?", (sid,)).fetchone()
            n = agg[0] or 0
            if n < 5:
                continue
            last = _one(cur, sid, "DESC", 0)
            prev = _one(cur, sid, "DESC", 1)
            five = _one(cur, sid, "DESC", 5)
            yr = _asof_1y(cur, sid, agg[2])
            latest_v = last[1] if last else None
            freq = (meta[2] or "daily").lower()
            stale = False
            try:
                age = (today - _dt.date.fromisoformat(agg[2])).days
                stale = age > _STALE_DAYS.get(freq, 8)
            except Exception:
                age = None
            rows.append({
                "id": sid, "name": label, "engine_name": meta[0], "unit": meta[1],
                "frequency": freq, "source": meta[3], "n": n, "start": agg[1], "end": agg[2],
                "as_of": last[2] if last else None, "latest": latest_v,
                "chg1": _pct(latest_v, prev[1] if prev else None),
                "chg5": _pct(latest_v, five[1] if five else None),
                "chg1y": _pct(latest_v, yr[0] if yr else None),
                "age_days": age, "stale": stale,
            })
        if rows:
            groups.append({"group": gname, "items": rows})
    conn.close()
    return {"as_of": today.isoformat(), "groups": groups}


def series(sid, frm=None, to=None, max_points=1600):
    conn = connect(read_only=True)
    cur = conn.cursor()
    meta = _meta(cur, sid)
    if not meta:
        conn.close()
        return JSONResponse({"error": f"unknown series {sid}"}, status_code=404)
    q = "SELECT obs_date, value FROM observations WHERE series_id=?"
    args = [sid]
    if frm:
        q += " AND obs_date>=?"; args.append(frm)
    if to:
        q += " AND obs_date<=?"; args.append(to)
    q += " ORDER BY obs_date ASC"
    pts = cur.execute(q, args).fetchall()
    last = _one(cur, sid, "DESC", 0)
    conn.close()
    n_full = len(pts)
    downsampled = False
    if n_full > max_points:
        step = math.ceil(n_full / max_points)
        pts = pts[::step] + ([pts[-1]] if (n_full - 1) % step else [])
        downsampled = True
    return {"id": sid, "name": meta[0], "unit": meta[1], "frequency": meta[2],
            "source": meta[3], "source_url": meta[4], "as_of": last[2] if last else None,
            "n_full": n_full, "downsampled": downsampled,
            "points": [[r[0], r[1]] for r in pts]}


def ripples(series_id):
    """The RIPPLE LENS: end the terminal's isolation. For one product, return (a) the
    MEASURED historic reaction to each event type (from edges×events — history ripple-aligned
    to this product), and (b) the LIVE situations now (situation_log), each linked to what
    that shock-type has historically done to THIS product. Real data only; the gap between a
    near-zero mean and a wide range is the 'priced risk, not realized disruption' takeaway."""
    conn = connect(read_only=True)
    cur = conn.cursor()
    meta = _meta(cur, series_id)
    if not meta:
        conn.close()
        return JSONResponse({"error": f"unknown series {series_id}"}, status_code=404)
    # (a) measured reaction by event type
    q = """SELECT ev.type, COUNT(*) n, ROUND(AVG(e.car20),2) avg20, ROUND(AVG(e.car5),2) avg5,
                  ROUND(MIN(e.car20),1) lo, ROUND(MAX(e.car20),1) hi
           FROM edges e JOIN events ev ON ev.event_id=e.event_id
           WHERE e.target_series=? AND e.units='%'
           GROUP BY ev.type ORDER BY ABS(AVG(e.car20)) DESC"""
    by_type = []
    for r in cur.execute(q, (series_id,)):
        # dispersion vs mean -> honest label
        spread = (r[5] - r[4]) if (r[5] is not None and r[4] is not None) else 0
        noisy = abs(r[2] or 0) * 4 < (spread or 0)   # mean small vs range => risk-priced, not directional
        by_type.append({"type": r[0], "n": r[1], "avg20": r[2], "avg5": r[3],
                        "lo": r[4], "hi": r[5],
                        "read": "priced as risk, not realized disruption" if noisy
                                else ("directional" )})
    tmap = {b["type"]: b for b in by_type}
    # (b) live situations (recent, grouped), linked to this product's historic reaction
    live = []
    try:
        rows = cur.execute(
            """SELECT situation_id, MAX(ts) ts, COUNT(*) signals,
                      (SELECT kind FROM situation_log s2 WHERE s2.situation_id=s1.situation_id
                       ORDER BY ts DESC LIMIT 1) kind,
                      (SELECT headline FROM situation_log s3 WHERE s3.situation_id=s1.situation_id
                       ORDER BY ts DESC LIMIT 1) headline,
                      (SELECT source_url FROM situation_log s4 WHERE s4.situation_id=s1.situation_id
                       ORDER BY ts DESC LIMIT 1) src
               FROM situation_log s1 GROUP BY situation_id ORDER BY ts DESC LIMIT 8""").fetchall()
        for r in rows:
            react = tmap.get(r[3])
            live.append({"situation_id": r[0], "last_ts": r[1], "signals": r[2],
                        "kind": r[3], "headline": r[4], "source_url": r[5],
                        "historic_reaction": ({"avg20": react["avg20"], "n": react["n"],
                                               "range": [react["lo"], react["hi"]],
                                               "read": react["read"]} if react else None)})
    except Exception:
        pass
    conn.close()
    return {"id": series_id, "name": meta[0], "unit": meta[1],
            "reactions_by_type": by_type, "live_situations": live,
            "note": "Measured 20-day cumulative reaction of this product to each event class "
                    "across the 296-event corpus. A small mean with a wide range means the "
                    "market priced risk, not a realized supply loss — the flow usually did not stop."}


def backtest():
    """The self-backtest console: how the engine scored against REALITY, out-of-sample.
    Reads the existing backtest artifacts (holdout / read_backtest / backtest_analogue /
    calibration) and the resolved gaps ledger. Reports the validated edges AND the honest
    nulls — the null IS the retrain signal (more corpus, not tuning). Nothing recomputed."""
    import json as _json
    import statistics as _st

    def rj(name):
        p = ROOT / "data" / name
        try:
            return _json.loads(p.read_text())
        except Exception:
            return {}

    hold = rj("holdout.json"); wf = rj("read_backtest.json")
    an = rj("backtest_analogue.json"); cal = rj("calibration.json")

    conn = connect(read_only=True); cur = conn.cursor()
    gaps = cur.execute("SELECT gap_direction, outcome, brier FROM gaps "
                       "WHERE resolved_at IS NOT NULL AND brier IS NOT NULL").fetchall()
    conn.close()
    briers = [g[2] for g in gaps]
    dir_counts = {}
    for g in gaps:
        dir_counts[g[0]] = dir_counts.get(g[0], 0) + 1
    gaps_summary = {
        "n_resolved": len(gaps),
        "mean_brier": round(_st.mean(briers), 3) if briers else None,
        "coin_brier": 0.25,
        "by_direction": dir_counts,
    }
    return {
        "as_of": an.get("as_of"),
        "walk_forward_v2": rj("walk_forward/summary.json"),
        "panels": [
            {"id": "holdout", "title": "Temporal hold-out — the validated edge (H1)",
             "verdict": "HOLDS" if hold.get("holds_out_of_sample") else "FAILS",
             "good": bool(hold.get("holds_out_of_sample")),
             "detail": hold.get("verdict"),
             "spec": hold.get("spec"), "split": hold.get("split_date")},
            {"id": "walkforward", "title": "Walk-forward accountability — does conditioning cut error?",
             "verdict": "HELPS" if wf.get("conditioning_helps") else "NO GAIN",
             "good": bool(wf.get("conditioning_helps")),
             "detail": f"MAE {wf.get('mae_uncond_pp')}pp → {wf.get('mae_cond_pp')}pp "
                       f"(improvement {wf.get('mae_improvement_pp')}pp) on n={wf.get('n_scored')} "
                       f"events, forecast from prior events only.",
             "spec": wf.get("note")},
            {"id": "analogue", "title": "Analogue forecaster — point-in-time Brier vs base rate",
             "verdict": "NULL — no edge at this N" if (an.get("skill_vs_base", 0) or 0) <= 0 else "EDGE",
             "good": (an.get("skill_vs_base", 0) or 0) > 0,
             "detail": f"Brier {an.get('brier')} vs base-rate {an.get('base_rate_brier')} "
                       f"(skill {an.get('skill_vs_base')}) on n={an.get('n_scored')}; "
                       f"LOO-calibrated skill {cal.get('calibrated_skill_loo')}. "
                       + (cal.get("verdict") or ""),
             "spec": an.get("note")},
            {"id": "gaps", "title": "Engine vs market, resolved against realized volatility",
             "verdict": (f"Brier {gaps_summary['mean_brier']} vs 0.25 coin"
                         if gaps_summary["mean_brier"] is not None else "—"),
             "good": (gaps_summary["mean_brier"] is not None
                      and gaps_summary["mean_brier"] < 0.25),
             "detail": f"{gaps_summary['n_resolved']} resolved calls; direction mix "
                       f"{gaps_summary['by_direction']}.",
             "spec": "Each call resolved at +20 trading days vs whether Brent vol actually rose."},
        ],
        "honest_note": "Validated edges and nulls are shown side by side. Where the engine does "
                       "NOT beat the base rate, that is reported as a null and the fix is more "
                       "corpus, never tuning a test to pass. This is the backtest-against-reality "
                       "spine: walk the modern-history corpus point-in-time, predict, score vs "
                       "what actually happened, keep only what survives out-of-sample.",
    }


def situation_read(event_id):
    """B4: compose the Read for one event — Layer G (escalation) + Layer P per branch
    (propagate) + the Situation Record + a live-market overlay + track-record placeholder
    (filled by B5). Pure composition of existing engines; recomputes nothing."""
    conn = connect(read_only=True)
    cur = conn.cursor()
    cols = [c[1] for c in cur.execute("PRAGMA table_info(events)")]
    row = cur.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
    if not row:
        conn.close()
        return JSONResponse({"error": f"unknown event {event_id}"}, status_code=404)
    e = dict(zip(cols, row))
    g = escalation.read_event(conn, event_id)
    layer_p = {}
    if not g.get("no_adequate_precedent"):
        for b, rate in (g.get("branch_rates", {}).get("rates") or {}).items():
            if rate:
                layer_p[b] = propagate.propagate(conn, branch=b)
    br = cur.execute("SELECT obs_date, value FROM observations WHERE series_id='fred.DCOILBRENTEU' "
                     "ORDER BY obs_date DESC LIMIT 6").fetchall()
    ovx = cur.execute("SELECT value FROM observations WHERE series_id='derived.ovx_pct' "
                      "ORDER BY obs_date DESC LIMIT 1").fetchone()
    conn.close()
    overlay = {"brent": br[0][1] if br else None, "as_of": br[0][0] if br else None,
               "brent_5d_pct": round((br[0][1] / br[5][1] - 1) * 100, 1) if len(br) >= 6 else None,
               "ovx_pct": round(ovx[0], 1) if ovx else None}
    return {
        "event": {"id": e["event_id"], "title": e.get("title"), "date": e["event_date"],
                  "type": e["type"], "actor": e.get("sr_actor"), "target": e.get("sr_target")},
        "record": json.loads(e["sr_json"]) if e.get("sr_json") else None,
        "layer_g": g, "layer_p": layer_p, "live_overlay": overlay,
        "track_record": _track_record(),
    }


def _track_record():
    """The walk-forward stamp every card carries (spec §4.4)."""
    p = ROOT / "data" / "walk_forward" / "summary.json"
    try:
        wf = json.loads(p.read_text())
        w = wf["windows"]
        return {"status": wf["verdict"]["G_conditioning"],
                "G_skill": {k: w[k]["G_skill"] for k in w},
                "detail": "escalation-branch forecast, walk-forward vs base rate, two windows"}
    except Exception:
        return {"status": "walk-forward not yet run"}


def register_terminal(app):
    @app.get("/terminal", response_class=HTMLResponse)
    def _terminal_page():
        if not TERMINAL_HTML.exists():
            return HTMLResponse("<h1>terminal.html missing</h1>", status_code=500)
        return HTMLResponse(TERMINAL_HTML.read_text())

    @app.get("/term_catalog")
    def _term_catalog():
        return catalog()

    @app.get("/term_series")
    def _term_series(id: str, frm: str = None, to: str = None):
        return series(id, frm, to)

    @app.get("/term_ripples")
    def _term_ripples(id: str):
        return ripples(id)

    @app.get("/trace_view", response_class=HTMLResponse)
    def _trace_view():
        if not TRACE_HTML.exists():
            return HTMLResponse("<h1>trace.html missing</h1>", status_code=500)
        return HTMLResponse(TRACE_HTML.read_text())

    @app.get("/trace_entities")
    def _trace_entities():
        return shock_tracer.list_anchors()

    @app.get("/trace")
    def _trace(entity: str = None, series: str = None, situation: str = None):
        return shock_tracer.trace(entity=entity, series=series, situation=situation)

    @app.get("/backtest_view", response_class=HTMLResponse)
    def _backtest_view():
        if not BACKTEST_HTML.exists():
            return HTMLResponse("<h1>backtest.html missing</h1>", status_code=500)
        return HTMLResponse(BACKTEST_HTML.read_text())

    @app.get("/backtest")
    def _backtest():
        return backtest()

    @app.get("/question_view", response_class=HTMLResponse)
    def _question_view():
        if not QUESTION_HTML.exists():
            return HTMLResponse("<h1>question.html missing</h1>", status_code=500)
        return HTMLResponse(QUESTION_HTML.read_text())

    @app.get("/desk.css")
    def _desk_css():
        from fastapi.responses import Response
        css = ROOT / "src" / "desk.css"
        return Response(css.read_text() if css.exists() else "", media_type="text/css")

    @app.get("/situation_view", response_class=HTMLResponse)
    def _situation_view():
        if not SITUATION_HTML.exists():
            return HTMLResponse("<h1>situation.html missing</h1>", status_code=500)
        return HTMLResponse(SITUATION_HTML.read_text())

    @app.get("/situation")
    def _situation(event: str):
        return situation_read(event)

    @app.get("/situation_events")
    def _situation_events():
        conn = connect(read_only=True)
        rows = conn.execute(
            "SELECT event_id, event_date, type, title FROM events "
            "WHERE type IN ('conflict_escalation','infrastructure_attack','chokepoint_disruption','sanctions') "
            "AND sr_outcome_90 IS NOT NULL ORDER BY event_date DESC").fetchall()
        conn.close()
        return [{"event_id": r[0], "date": r[1], "type": r[2], "title": r[3]} for r in rows]
