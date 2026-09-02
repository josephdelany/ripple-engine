"""bridge.py -- Brief A-7: the registered fields whose data the engine already holds, stamped into state_panel.

Three kinds of rows, every one with a vintage (WS-R1):
1. SERIES BRIDGE -- market / physical fields whose codebook line says "(loaded: <series>)": the observation is copied
   from `observations` with vintage = obs_date + the series' registered publish lag (data/series_cadence_overrides.json,
   the same table heartbeat.py uses); monthly WTI: knowable the following month + lag. release = the pull date
   (retrieved_at). retrospective = 0 (contemporaneous records).
2. DERIVED -- opec_decision_dated from the corpus's own opec_decision events (dated announcements, sourced).
   leader_change_last_365d is computed at read time by situation_state (Archigos tenure), never stored.
3. COW Diplomatic Exchange v2006.1 (keyless CSV, 1817-2005) -> diplomatic_representation per dyad-year.
Everything else registered but not loadable here is written as an explicit gap line with its reason
(data/state/GAPS.md), alongside the block x decade coverage table. Nothing is guessed.

Run:  python3 src/state/bridge.py
"""
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import panel as P  # noqa: E402
import countries as C  # noqa: E402
import heartbeat as H  # noqa: E402

GAPS_OUT = P.DATA / "state" / "GAPS.md"
DIPEX_URL = "https://correlatesofwar.org/wp-content/uploads/Diplomatic_Exchange_2006v1.csv"

# field -> (series, entity, note)   [the codebook's "(loaded: ...)" lines]
SERIES = {
    "wti_monthly": ("fred.WTISPLC", "world", "monthly: knowable the following month + 20 d"),
    "brent_daily": ("fred.DCOILBRENTEU", "world", "EIA spot via FRED, weekly re-publication (7 d lag)"),
    "wti_daily": ("fred.DCOILWTICO", "world", "EIA spot via FRED (7 d lag)"),
    "diesel_crack": ("derived.diesel_crack", "world", "derived from EIA/FRED series (derived.* 4 d lag)"),
    "vix": ("fred.VIXCLS", "world", "CBOE via FRED (3 d lag)"),
    "ovx": ("fred.OVXCLS", "world", "CBOE via FRED (3 d lag)"),
    "cot_managed_money_net": ("cftc.mm_net_wti", "world", "CFTC weekly, Friday release for Tuesday positions (3 d lag)"),
    "us_crude_stocks_xspr": ("eia.crude_stocks_xspr", "country.usa", "EIA weekly, Wednesday release for the prior Friday (5 d lag)"),
    "us_spr_stock": ("eia.spr_stocks", "country.usa", "EIA weekly (5 d lag)"),
    "us_refinery_utilization": ("eia.refinery_util", "country.usa", "EIA weekly (5 d lag)"),
}
CHOKEPOINTS = {"portwatch.hormuz.n_tanker": "chokepoint.hormuz", "portwatch.suez.n_tanker": "chokepoint.suez",
               "portwatch.bab_el_mandeb.n_tanker": "chokepoint.bab_el_mandeb"}
GDELT = {"gdelt.tone.hormuz": "chokepoint.hormuz", "gdelt.tone.opec": "opec"}
BREAKEVEN_PREFIX = "imf.breakeven."
DEFAULT_LAG = {"cftc": 3, "eia": 5, "portwatch": 5, "gdelt": 1}

# registered fields computed at read time by situation_state.state_at (never stored in the panel)
READ_TIME = {"leader_change_last_365d": "computed at read time from Archigos tenure (archigos.tenure_at); a stored change-date row would carry forward as 1"}
GAPS = {
    "arms_imports_tiv": "SIPRI Arms Transfers TIV tables are generated per query on sipri.org (no bulk keyless file); a local export under data/state/local/sipri/ would load -- none present",
    "consumption_annual": "EI Statistical Review xlsx (local, licence: cite) absent from data/state/local/ei/ (HTTP 403 to scripts; download by hand)",
    "crude_production_annual": "EI Statistical Review xlsx absent (as above)",
    "proven_reserves": "EI Statistical Review xlsx absent (as above)",
    "refinery_capacity_annual": "EI Statistical Review xlsx absent (as above)",
    "net_import_dependence": "derived from EI consumption - production; EI xlsx absent",
    "crude_production": "EIA International Energy Statistics API v2 needs EIA_API_KEY (free registration); not set in this environment",
    "vdem_polyarchy": "V-Dem v16 Country-Year Core csv absent from data/state/local/vdem/ (served through a form)",
    "sanctions_in_force": "GSDB R5 dyadic csv absent (by request; Joe)",
    "trade_share_bilateral": "IMF DOTS: DataMapper / SDMX endpoints refuse scripted access (verified); local dots_exports.csv absent",
    "tanker_freight": "Baltic Dirty/Clean Tanker Index is licensed; no free source (register §5) -- a stated gap, not a missing download",
    "curve_m1_m4_spread_cme": "delayed continuous CL contracts beyond the front month are not fetched (yfinance CL=F is front only); the EIA NYMEX curve field curve_m1_m4_spread is loaded instead",
    "macro_vintages": "ALFRED vintages (alfred.*) are not in observations; fetch_fred_alfred.py has not been run into the panel -- next loader",
    "vxo": "fred.VXOCLS is not in observations (VIXCLS is); add to fetch_series to load",
    "gpr_vintage_monthly": "the GPR monthly vintage archive file names (data_gpr_export_YYYYMM.xls) are not verified on matteoiacoviello.com; the current export is loaded as gpr_monthly",
    "opec_supply_shock_kilian": "Kilian OPEC supply-shock series (1971-2004) stubbed with instructions in src/state/kilian.py (WS-M13)",
    "nyt_article_count": "NYT Article Search API needs NYT_API_KEY (free); not set; never committed",
    "gp_posture_gulf": "dossier field (sourced statements): coded per event by hand, none coded yet",
    "unsc_action": "dossier field (UN records): un.org resolution pages return 403 to scripts and the UN Digital Library serves a JS challenge; coded by hand, none yet",
    "contemporaneous_claims": "per-event claim extraction (reader.py + ledger) is not a panel field; lives in data/ledger/",
}


def _lag(sid, overrides):
    cad, lag = H.override_for(sid, overrides)
    if lag:
        return int(lag)
    return DEFAULT_LAG.get(sid.split(".")[0], 0)


def bridge_rows(conn, overrides):
    rows, notes = [], {}
    obs = pd.read_sql("SELECT series_id, obs_date, value, retrieved_at FROM observations WHERE value IS NOT NULL", conn)
    obs["obs_date"] = obs["obs_date"].str[:10]
    obs["rel"] = obs["retrieved_at"].fillna("").str[:10]
    obs = obs.sort_values(["series_id", "obs_date", "retrieved_at"]).drop_duplicates(["series_id", "obs_date"], keep="last")
    by = {k: g for k, g in obs.groupby("series_id")}
    src = dict(conn.execute("SELECT series_id, source || ' ' || COALESCE(source_url, '') FROM series"))

    def emit(field, sid, entity, vint_fn, unit=None, note=""):
        g = by.get(sid)
        if g is None or g.empty:
            notes[field] = f"series {sid} absent from observations"
            return
        for r in g.itertuples(index=False):
            rel = r.rel or datetime.now(timezone.utc).date().isoformat()
            rows.append({"entity_id": entity, "field": field, "obs_date": r.obs_date, "value": float(r.value), "unit": unit,
                         "source": f"{src.get(sid, sid)} (series {sid}; bridge)", "vintage": vint_fn(r.obs_date), "release": rel, "retrospective": 0})
        notes[field] = f"{len(g)} rows from {sid}; {note}"

    for field, (sid, ent, note) in SERIES.items():
        lag = _lag(sid, overrides)
        if field == "wti_monthly":
            fn = lambda d, lag=lag: (pd.Timestamp(P.knowable_month(pd.Timestamp(d))) + pd.Timedelta(days=lag)).date().isoformat()
        else:
            fn = lambda d, lag=lag: (pd.Timestamp(d) + pd.Timedelta(days=lag)).date().isoformat()
        emit(field, sid, ent, fn, note=f"{note}; lag {lag} d")
    for sid, ent in CHOKEPOINTS.items():
        lag = _lag(sid, overrides)
        emit("chokepoint_transits", sid, ent, lambda d, lag=lag: (pd.Timestamp(d) + pd.Timedelta(days=lag)).date().isoformat(), note=f"IMF PortWatch tanker transits; lag {lag} d")
    for sid, ent in GDELT.items():
        emit("gdelt_volume_tone", sid, ent, lambda d: (pd.Timestamp(d) + pd.Timedelta(days=1)).date().isoformat(), note="GDELT DOC tone, next-day")
    for sid in [s for s in by if s.startswith(BREAKEVEN_PREFIX)]:
        ent = "country." + sid[len(BREAKEVEN_PREFIX):]
        if ent in C.ALL:
            emit("fiscal_breakeven", sid, ent, lambda d, g=by[sid]: g["rel"].max() or d, note="IMF REO breakeven via FRED; one vintage held (the pull date)")
    return rows, notes


def derived_rows(conn):
    rows, notes = [], {}
    # leader_change_last_365d is NOT stored: at a change date the tenure is 0, so a stored row would read 1 forever
    # under carry-forward. situation_state.state_at computes it at read time from Archigos tenure (archigos.tenure_at).
    conn.execute("DELETE FROM state_panel WHERE field='leader_change_last_365d'"); conn.commit()
    notes["leader_change_last_365d"] = "computed at read time by situation_state.state_at from Archigos tenure (not stored: a stored change-date row would carry forward as 1)"
    ev = pd.read_sql("SELECT event_id, event_date, title, source_url, added_at FROM events WHERE type='opec_decision'", conn)
    for r in ev.itertuples(index=False):
        rows.append({"entity_id": "opec", "field": "opec_decision_dated", "obs_date": r.event_date[:10], "value_text": r.title, "unit": "text",
                     "source": f"corpus opec_decision {r.event_id} ({r.source_url})", "vintage": r.event_date[:10],
                     "release": (r.added_at or r.event_date)[:10], "retrospective": 0})
    notes["opec_decision_dated"] = f"{len(ev)} dated OPEC decisions from the corpus (sourced events; Kaenzig announcement set not loaded)"
    return rows, notes


def dipex_rows():
    p, meta = P.fetch_file(DIPEX_URL, P.raw_path("cow_dipex", "Diplomatic_Exchange_2006v1.csv"))
    release = P.vintage_from(meta, "2022-07-11")
    df = pd.read_csv(p, encoding="latin-1")
    rows = []
    for r in df.itertuples(index=False):
        a, b = C.from_ccode(r.ccode1), C.from_ccode(r.ccode2)
        if not a or not b or a == b:
            continue
        lv = [int(x) for x in (r.DR_at_1, r.DR_at_2) if not pd.isna(x) and int(x) in (0, 1, 2, 3)]
        if not lv:
            continue
        rows.append({"entity_id": C.dyad_id(a, b), "field": "diplomatic_representation", "obs_date": f"{int(r.year)}-01-01", "value": float(max(lv)),
                     "unit": "level", "source": "COW Diplomatic Exchange v2006.1 (Diplomatic_Exchange_2006v1.csv)", "vintage": P.knowable_annual(int(r.year)),
                     "release": release, "retrospective": 1})
    # both directions of a pair land on the same undirected dyad id: keep the max per (dyad, year)
    best = {}
    for x in rows:
        k = (x["entity_id"], x["obs_date"])
        if k not in best or x["value"] > best[k]["value"]:
            best[k] = x
    return list(best.values()), f"{len(best)} dyad-years 1817-2005 (level = max of the two directions; 9 = missing dropped); release {release}"


def gaps_doc(notes, cov):
    cb = P.codebook()
    L = ["# World-state panel — loaded by the bridge, and the stated gaps (Brief A-7, generated by src/state/bridge.py)", "",
         f"_generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}; every line names the codebook source; nothing here is a value_", "",
         "## Loaded by this pass", "", "| field | block | rows / note |", "|---|---|---|"]
    for f, n in sorted(notes.items()):
        L.append(f"| `{f}` | {cb.get(f, {}).get('block', '?')} | {n} |")
    L += ["", "## Computed at read time (registered, never stored)", ""] + [f"- `{f}` — {why}" for f, why in READ_TIME.items()]
    L += ["", "## Registered, not loaded — the reason (each a gap, not a value)", "", "| field | block | codebook source | why not loaded |", "|---|---|---|---|"]
    for f, why in sorted(GAPS.items()):
        L.append(f"| `{f}` | {cb.get(f, {}).get('block', '?')} | {str(cb.get(f, {}).get('source', ''))[:120].replace('|', '/')} | {why} |")
    L += ["", "## Coverage: rows per block per decade, 1940s–2020s (`state_panel`)", ""]
    blocks = cov.get("blocks") or {}
    decades = [f"{d}s" for d in range(1940, 2030, 10)]
    L += ["| block | " + " | ".join(decades) + " |", "|---|" + "---|" * len(decades)]
    for b, dd in sorted(blocks.items()):
        L.append(f"| {b} | " + " | ".join(str(dd.get(d, 0)) if dd.get(d, 0) else "**gap**" for d in decades) + " |")
    L += ["", "A **gap** cell means no registered field of that block has a row dated in that decade; the reasons are the lines above "
          "(PHYSICAL before 1970: no keyless annual production/consumption series is held -- the EI review file is a local download).", ""]
    GAPS_OUT.write_text("\n".join(L))


def load(conn=None):
    conn = conn or P.connect()
    P.ensure_schema(conn)
    overrides = H.load_overrides()
    rows, notes = bridge_rows(conn, overrides)
    d_rows, d_notes = derived_rows(conn)
    notes.update(d_notes)
    try:
        x_rows, x_note = dipex_rows()
        notes["diplomatic_representation"] = x_note
    except Exception as e:
        x_rows = []
        GAPS["diplomatic_representation"] = f"COW Diplomatic Exchange fetch failed: {type(e).__name__}"
    n = P.write(conn, rows + d_rows + x_rows)
    cov = P.coverage(conn)
    gaps_doc(notes, cov)
    fields = sorted({r["field"] for r in rows + d_rows + x_rows})
    P.report("bridge", n, fields, f"{len(fields)} fields; gaps listed in {GAPS_OUT.relative_to(P.ROOT)}")
    return n, fields


if __name__ == "__main__":
    n, fields = load()
    print(f"bridge: {n} rows into state_panel for {len(fields)} fields: {fields}")
