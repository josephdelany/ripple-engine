"""
mcp_server.py -- the Engine MCP: let Claude query the engine directly.

This exposes the ripple engine to Claude (Desktop / Cowork) as a Model Context
Protocol server over stdio, so an analysis conversation can ask the data
questions -- no screenshots, no copy-paste. It is launched by the Claude app; it
binds no network port.

IT IS READ-ONLY, BY CONSTRUCTION. Every tool reads; none writes, approves,
promotes, logs a forecast, or changes anything. The database is opened in SQLite
read-only mode and there is no raw-SQL passthrough -- only parameterized queries.
The human gate (candidate_review -> apply_review -> load_events) is untouched and
stays a gate.

Each tool's docstring carries the engine's standing caveats so Claude repeats them
in conversation: n is small, some hypotheses are exploratory or failed
pre-registration, and -- always -- the engine measures the market CONSEQUENCES of
events, it never forecasts whether an event will occur.

Run (normally the Claude app does this):  python3 src/mcp_server.py
"""

import csv
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from mcp.server.fastmcp import FastMCP

# Import-only reuse of the analysis machinery (never modified).
from event_study import car_for_event, PRE, HORIZONS
from cross_asset import asset_returns
from derive_signals import load_wide, build_signals
from robustness import REGISTERED
import scenario
import situation

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
DATA = ROOT / "data"
BRENT = "fred.DCOILBRENTEU"

# One-line caveat appended (in spirit) to every quantitative answer.
CAVEATS = ("n is small (dozens of clustered events); read as indicative, not "
           "conclusive. H3 (positioning) FAILED pre-registration; H5 (GPR) is "
           "exploratory and two-sided. The engine measures market CONSEQUENCES of "
           "events and NEVER forecasts whether an event will occur.")

# get_results is whitelisted -- no arbitrary file reads.
RESULTS_WHITELIST = {
    "registered_run_results": "registered_run_results.txt",
    "expanded_run_results": "expanded_run_results.txt",
    "inference_results": "inference_results.txt",
    "h5_results": "h5_results.txt",
    "quiet_comparison": "quiet_comparison.txt",
    "cross_asset_results": "cross_asset_results.txt",
    "me_report": "me_report.txt",
    "gpr_validation": "gpr_validation.txt",
}

mcp = FastMCP("ripple-engine")


def _ro_conn():
    """A READ-ONLY connection -- SQLite refuses writes on this handle."""
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)


def _json_load(name):
    p = DATA / name
    if not p.exists():
        return {"error": f"{name} not generated yet -- run the pipeline (refresh.py)."}
    try:
        return json.loads(p.read_text())
    except (ValueError, OSError) as e:
        return {"error": f"could not read {name}: {e}"}


@mcp.tool()
def get_daily_read() -> dict:
    """Today's 'engine read': the one-sentence market-state read, the amplifier
    status for H1 (VIX) and H2 (inventories), the GPR percentile as descriptive
    context, and clustered base-rate CARs by event type. Point-in-time from the
    latest committed data. CAVEATS: H3 is FAILED and never an amplifier; H5/GPR is
    descriptive only; this is a conditional read of history, not a forecast."""
    return _json_load("engine_read.json")


@mcp.tool()
def get_health() -> dict:
    """Data-freshness summary from the heartbeat: overall status, each series'
    OK/STALE/DEAD, events loaded, forecasts pending, and whether the last refresh
    failed. STALE/DEAD usually just means normal publication lag, not corruption."""
    h = _json_load("health_status.json")
    if "error" in h:
        return h
    return {"overall": h.get("overall"), "generated_at": h.get("generated_at"),
            "events_count": h.get("events_count"),
            "forecasts_pending": h.get("forecasts_pending"),
            "last_refresh": h.get("last_refresh"),
            "series": [{"series_id": s["series_id"], "last_obs": s["last_obs"],
                        "status": s["status"]} for s in h.get("series", [])]}


@mcp.tool()
def list_events(type: str = "", entity: str = "", since: str = "") -> list:
    """List curated events (each hand-coded and sourced). Optional filters: `type`
    (e.g. conflict_escalation, sanctions, policy_response), `entity` (e.g.
    country.iran, chokepoint.hormuz), `since` (YYYY-MM-DD). Returns event_id, date,
    type, title, severity, surprise, confidence, source_url. CAVEAT: severity is
    expected supply-disruption (not the price reaction); every event is sourced."""
    q = ("SELECT DISTINCT e.event_id, e.event_date, e.type, e.title, e.severity, "
         "e.surprise, e.confidence, e.source_url FROM events e")
    params, where = [], []
    if entity:
        q += " JOIN event_entities ee ON ee.event_id = e.event_id"
        where.append("ee.entity_id = ?"); params.append(entity)
    if type:
        where.append("e.type = ?"); params.append(type)
    if since:
        where.append("e.event_date >= ?"); params.append(since)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY e.event_date"
    conn = _ro_conn()
    cols = ["event_id", "event_date", "type", "title", "severity", "surprise",
            "confidence", "source_url"]
    rows = [dict(zip(cols, r)) for r in conn.execute(q, params)]
    conn.close()
    return rows


@mcp.tool()
def get_event(event_id: str) -> dict:
    """Everything the engine knows about one event: its coded row + source, its
    Brent CAR at +1/+5/+10/+20 days (%), the market state at t-1 (VIX %ile, inv
    sigma, COT %ile -- point-in-time, no lookahead), and its cross-asset reactions
    from the edges table. CAVEAT: a single event is an anecdote; CARs are abnormal
    returns vs a constant-mean baseline, not forecasts."""
    conn = _ro_conn()
    cols = ["event_id", "event_date", "date_precision", "type", "title",
            "description", "severity", "surprise", "confidence", "source_url"]
    row = conn.execute(f"SELECT {','.join(cols)} FROM events WHERE event_id=?",
                       (event_id,)).fetchone()
    if not row:
        conn.close()
        return {"error": f"no event '{event_id}'"}
    ev = dict(zip(cols, row))
    ret = asset_returns(conn, BRENT, "price")
    car = car_for_event(ret, ev["event_date"])
    ev["brent_car_pct"] = ({f"CAR+{h}": round(float(car[PRE + h]) * 100, 1)
                            for h in HORIZONS} if car is not None
                           else "outside price history")
    signals = build_signals(load_wide(conn))
    cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)
    state = {}
    for _hid, sid, key, _sign, _desc in REGISTERED:
        s = signals[sid].dropna() if sid in signals else pd.Series(dtype=float)
        v = s.asof(cutoff) if len(s) else np.nan
        state[key] = None if pd.isna(v) else round(float(v), 2)
    ev["state_at_t_minus_1"] = state
    ev["cross_asset_edges"] = [
        {"asset": ts, "car5": c5, "car20": c20, "units": u}
        for ts, c5, c20, u in conn.execute(
            "SELECT target_series, car5, car20, units FROM edges WHERE event_id=? "
            "ORDER BY target_series", (event_id,))]
    conn.close()
    return ev


@mcp.tool()
def scenario_card(event_type: str) -> dict:
    """The 'if an event of this type happened today' scenario card: clustered
    historical analogs, base-rate CARs, today's amplifier conditioning, and the
    fixed caveat. CAVEAT (always on the card): the card is CONDITIONAL on such an
    event occurring; the engine does not forecast whether it will, or when."""
    pb = scenario.build_playbook()
    card = next((c for c in pb["cards"] if c["type"] == event_type), None)
    if card is None:
        return {"error": f"unknown event_type '{event_type}'",
                "known_types": [c["type"] for c in pb["cards"]]}
    return {"as_of": pb["as_of"], "card": card,
            "todays_conditioning": pb["conditioning"],
            "gpr_context": pb.get("gpr_context"),
            "caveat": scenario.CAVEAT}


@mcp.tool()
def query_series(series_id: str, start: str = "", end: str = "") -> dict:
    """Observations for one series (e.g. fred.DCOILBRENTEU, derived.vix_pct,
    gpr.GPRD, eia.crude_stocks_xspr). Optional start/end (YYYY-MM-DD). Capped at
    2,000 rows per call (says so if truncated). Read-only, parameterized."""
    q = "SELECT obs_date, value FROM observations WHERE series_id=?"
    params = [series_id]
    if start:
        q += " AND obs_date >= ?"; params.append(start)
    if end:
        q += " AND obs_date <= ?"; params.append(end)
    q += " ORDER BY obs_date LIMIT 2001"
    conn = _ro_conn()
    rows = conn.execute(q, params).fetchall()
    conn.close()
    truncated = len(rows) > 2000
    return {"series_id": series_id, "n_returned": min(len(rows), 2000),
            "truncated_at_2000": truncated,
            "observations": [{"date": d, "value": v} for d, v in rows[:2000]]}


@mcp.tool()
def get_alerts(status: str = "", limit: int = 25) -> list:
    """Watcher alert cards (curated attention, NEVER conclusions). Optional
    `status` (new|seen|promoted|dismissed) and `limit` (default 25), newest first.
    heuristic_type is a labelled guess, not a coding; amp_context is copied from
    the engine read. Promotion into a candidate is a human step, never automatic."""
    p = DATA / "alert_queue.csv"
    if not p.exists():
        return [{"note": "no alerts yet -- run watcher.py"}]
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    if status:
        rows = [r for r in rows if r.get("status") == status]
    return list(reversed(rows))[:max(1, min(limit, 200))]


@mcp.tool()
def list_situations() -> list:
    """The tracked situations (the running memory / 'middle clock'): for each, its
    id, title, status, when it started, and how many sourced timeline atoms it
    holds. Situations are human-defined in data/situations.yaml -- never invented
    by the engine. CAVEAT: atoms are curated ATTENTION (sourced headlines), not
    coded events; typing is a heuristic hint until the agent refines it."""
    conn = _ro_conn()
    out = []
    for sit in situation.load_situations():
        sid = sit["situation_id"]
        try:
            n = conn.execute("SELECT COUNT(*) FROM situation_log WHERE "
                             "situation_id=?", (sid,)).fetchone()[0]
        except sqlite3.Error:
            n = 0
        out.append({"situation_id": sid, "title": sit.get("title"),
                    "status": sit.get("status"), "started_at": sit.get("started_at"),
                    "n_atoms": n})
    conn.close()
    return out


@mcp.tool()
def get_situation(situation_id: str) -> dict:
    """One situation's full dossier: its config, atom count, most-recent sourced
    timeline atoms, and the rendered 'where we stand' markdown (timeline +
    priced-state). This joins the engine's history, today's state, and the live
    memory on one read. CAVEAT: the synthesis prose (if present) is agent-authored
    and tagged; the priced-state numbers are the engine's, the atoms are sourced
    attention, and NONE of it forecasts whether an event will occur."""
    sit = next((s for s in situation.load_situations()
                if s["situation_id"] == situation_id), None)
    if sit is None:
        return {"error": f"no situation '{situation_id}'",
                "known": [s["situation_id"] for s in situation.load_situations()]}
    conn = _ro_conn()
    n = conn.execute("SELECT COUNT(*) FROM situation_log WHERE situation_id=?",
                     (situation_id,)).fetchone()[0]
    recent = [{"ts": ts, "kind": k, "status": st, "headline": h, "source_url": u}
              for ts, k, st, h, u in conn.execute(
                  "SELECT ts, kind, status, headline, source_url FROM situation_log "
                  "WHERE situation_id=? ORDER BY ts DESC, log_id DESC LIMIT 15",
                  (situation_id,))]
    now = pd.Timestamp.utcnow().isoformat(timespec="seconds")
    dossier_md = situation.render_dossier(conn, sit, situation.load_engine_read(), now)
    conn.close()
    return {"situation_id": situation_id, "title": sit.get("title"),
            "status": sit.get("status"), "member_entities": sit.get("member_entities"),
            "dominant_kinds": sit.get("dominant_kinds"), "n_atoms": n,
            "recent_atoms": recent, "dossier_md": dossier_md, "caveat": CAVEATS}


@mcp.tool()
def get_sowhat() -> dict:
    """The live 'so-what' read: today's regime, the VALIDATED propagation (the only claims), the
    market-priced gap, and the active situations ranked by multi-modal corroboration, with receipts.
    CAVEAT: only validated-backbone edges are claims; directional/lead links are null/trap; the engine
    measures consequences, never whether an event will occur."""
    return _json_load("sowhat.json")


@mcp.tool()
def get_propagation_graph() -> dict:
    """The validated propagation network: the VALIDATED backbone (shock -> node ripples that survived
    the gate, FDR-corrected), the honest null layer (directional event->node, mostly weak at this N),
    and the TRAP edges (nodes that co-move but where neither reliably leads). CAVEAT: only 'validated'
    edges are claims; 'trap' means do-not-trade-the-lead; small-N."""
    r = _json_load("propagation_graph.json")
    if "error" in r:
        return r
    return {"backbone_validated": r.get("backbone_validated", []),
            "node_to_node": r.get("node_to_node", []),
            "event_to_node_note": "directional event->node is a null layer at this N (see file)",
            "caveat": CAVEATS}


@mcp.tool()
def get_gaps() -> dict:
    """The gap ledger (market-as-null): the live gap (engine view vs the market's implied oil vol,
    OVX) and the resolving, Brier-scored scorecard by gap direction. CAVEAT: the disagreement finding
    is small-N and SUGGESTIVE, not a validated edge; the scorecard is published either way."""
    g = _json_load("gaps.json")
    if "error" in g:
        return g
    return {"live_gap": g.get("live_gap"), "ledger": g.get("ledger"), "caveat": CAVEATS}


@mcp.tool()
def test_hypothesis(state: str, asset: str = "fred.DCOILBRENTEU",
                    sign: str = "high", horizon: int = 20) -> dict:
    """Run a hypothesis through the full validation gate, read-only: does `state` (a derived.* signal,
    e.g. derived.vix_pct), on its `sign` side (high|low), amplify the |CAR+horizon| ripple in `asset`
    (a fred.* series)? Returns amplification + cluster-bootstrap 95% CI + permutation p + a HOLDS/
    no-effect verdict. This is the research bench, callable in conversation. CAVEAT: a single test is
    one hypothesis -- correct for multiple testing if you scan many; small-N; believe the wide CIs."""
    import research
    conn = _ro_conn()
    r = research.run_test(conn, state, asset, sign, horizon)
    conn.close()
    if r.get("ok"):
        r["caveat"] = CAVEATS
    return r


@mcp.tool()
def get_results(name: str) -> str:
    """Verbatim contents of a committed results file (WHITELISTED only): one of
    registered_run_results, expanded_run_results, inference_results, h5_results,
    quiet_comparison, cross_asset_results, me_report, gpr_validation. These files
    carry their own caveats and small-n warnings inline -- read them. No arbitrary
    file reads are possible."""
    fname = RESULTS_WHITELIST.get(name)
    if not fname:
        return (f"'{name}' is not whitelisted. Choose one of: "
                f"{', '.join(sorted(RESULTS_WHITELIST))}.")
    p = DATA / fname
    return p.read_text() if p.exists() else f"{fname} not generated yet."


if __name__ == "__main__":
    mcp.run()          # stdio transport; launched by the Claude app
