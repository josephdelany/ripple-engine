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

ROOT = Path(__file__).resolve().parent.parent
TERMINAL_HTML = ROOT / "src" / "terminal.html"

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
