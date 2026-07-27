"""
situation.py -- the Situation Memory assembler (DETERMINISTIC; NO LLM).

The "middle clock": between the engine's deep history (coded events + base rates)
and the live tape (the watcher), this maintains a persistent per-conflict TIMELINE
so "where do we stand right now" is remembered state, not re-derived every session.

WHAT THIS FILE DOES (all deterministic Python -- no judgement, no math the engine
doesn't already compute):
  Slice 1 (attach): read the human-owned situations.yaml + the watcher's
    alert_queue.csv, and file each alert that touches a situation's member entities
    into situation_log as a sourced, tagged atom (status='observed').
  Slice 2 (render): read engine_read.json base rates + Brent and write a dossier
    markdown per situation (timeline + priced-state), with the "where we stand"
    synthesis left for the scoped agent (a later slice).

WHAT IT NEVER DOES: type/interpret the alerts (kind stays 'unmapped' until the
agent), compute a new metric, or touch the human gate. Attaching an alert here is
context/memory; it is orthogonal to promoting it into a coded event (that stays the
untouched watcher -> candidate_review -> apply_review -> load_events flow).

Run:  python3 src/situation.py
"""

import csv
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# import-only reuse of the watcher's canonical GDELT country-code map (never
# modified). GDELT alerts carry country CODES (IRN, SAU); RSS alerts carry
# entity_ids (country.iran). We match against both, so we need this map.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from watcher import COUNTRY_CC  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SIT_CONFIG = ROOT / "data" / "situations.yaml"
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
ENGINE_READ = ROOT / "data" / "engine_read.json"
DOSSIER_DIR = ROOT / "data" / "situations"
BRENT = "fred.DCOILBRENTEU"
TIMELINE_CAP = 60          # newest-N atoms shown in the dossier (says so if more)

# Alerts Joe has explicitly marked noise are not woven into the memory.
SKIP_ALERT_STATUS = {"dismissed"}

# Copied from the engine's standing discipline: the dossier is a conditional read
# of history, not a forecast; small n; the engine never forecasts occurrence.
CAVEAT = ("History conditioned on today, NOT a forecast. Base rates are clustered "
          "CARs on small n; GPR is descriptive only (never an amplifier); H3 "
          "positioning FAILED pre-registration. The engine measures market "
          "CONSEQUENCES of events, never whether an event will occur.")


def load_situations(path=SIT_CONFIG):
    """The human-owned situation definitions. [] if the file is missing."""
    if not Path(path).exists():
        return []
    cfg = yaml.safe_load(Path(path).read_text()) or {}
    return cfg.get("situations", [])


def read_alerts(path=ALERT_QUEUE):
    """The watcher's alert queue as a list of dicts. [] if not generated yet."""
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def match_set(member_entities):
    """The set an alert's tokens must intersect to belong to this situation:
    the member entity_ids PLUS the GDELT country code of each country member
    (so both alert formats attach)."""
    s = set(member_entities)
    for eid in member_entities:
        if eid.startswith("country."):
            code = COUNTRY_CC.get(eid.split(".", 1)[1])
            if code:
                s.add(code)
    return s


def alert_tokens(alert):
    """The entity tokens on an alert row (entity_ids and/or country codes)."""
    return {t for t in (alert.get("matched_entities") or "").split(";") if t}


def attach(conn, situations, alerts, now):
    """File every situation-touching alert into situation_log as a sourced,
    tagged 'observed' atom. Idempotent: UNIQUE(situation_id, source_url) + INSERT
    OR IGNORE means re-running adds 0 rows. Returns rows actually inserted."""
    before = conn.total_changes
    cur = conn.cursor()
    for sit in situations:
        if sit.get("status") == "closed":
            continue
        sid = sit["situation_id"]
        want = match_set(sit.get("member_entities", []))
        for a in alerts:
            if a.get("status") in SKIP_ALERT_STATUS:
                continue
            url = (a.get("url") or "").strip()
            if not url or not (alert_tokens(a) & want):
                continue
            # Provenance is COPIED, never generated. kind stays 'unmapped' (the
            # agent types it later); status is 'observed' (a real sourced
            # headline); confidence 'low' (unvetted), mirroring promote_alert.
            cur.execute(
                "INSERT OR IGNORE INTO situation_log "
                "(situation_id, ts, kind, actor_entity, headline, detail, "
                " source_url, retrieved_at, status, confidence, alert_url, "
                " promoted_event_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (sid, a.get("timestamp_utc") or now, "unmapped", None,
                 a.get("headline") or "(no headline)", None, url, now,
                 "observed", "low", url, None))
    return conn.total_changes - before


# ---------------------------------------------------------------- Slice 2: render
# Everything below only FORMATS numbers the engine already computed. It performs
# no new analysis (a bespoke priced-vs-realized metric would be a derive_signals
# change with a declared mechanism -- out of scope). No LLM: the "where we stand"
# synthesis is left blank for the scoped agent, because prose is where fabrication
# lives and the engine never invents it.

def load_engine_read(path=ENGINE_READ):
    """engine_read.json as a dict, or {} if the pipeline hasn't produced it."""
    if not Path(path).exists():
        return {}
    try:
        return __import__("json").loads(Path(path).read_text())
    except (ValueError, OSError):
        return {}


def latest_brent(conn):
    """The two most recent distinct-date Brent closes as [(date, value), ...].
    Read-only display; no arithmetic beyond picking the latest as_of per date."""
    seen, out = set(), []
    for dt, val, _asof in conn.execute(
            "SELECT obs_date, value, as_of FROM observations WHERE series_id=? "
            "ORDER BY obs_date DESC, as_of DESC", (BRENT,)):
        if dt in seen:
            continue
        seen.add(dt)
        out.append((dt, val))
        if len(out) >= 2:
            break
    return out


def _priced_state_md(conn, sit, er):
    """The priced-state block: Brent + amplifiers + the situation's channel base
    rates, all pulled verbatim from engine_read.json / observations."""
    lines = ["## Priced-state — what history says, conditioned on today", ""]

    brent = latest_brent(conn)
    if brent:
        head = f"**Brent** ${brent[0][1]:.2f} ({brent[0][0]})"
        if len(brent) > 1:
            head += f"  ·  prior ${brent[1][1]:.2f} ({brent[1][0]})"
        lines += [head + "  _(observations; the engine's last committed close — "
                  "the live tape may sit above this)_", ""]
    else:
        lines += ["**Brent** — no observations found.", ""]

    if not er:
        lines += ["_engine_read.json not generated yet — run refresh.py for "
                  "amplifier status and base rates._", ""]
        return "\n".join(lines)

    lines += [f"_Engine read as of {er.get('as_of', '?')}:_ "
              + (er.get("read", "").strip() or "(no read line)"), ""]
    lines += ["**Amplifiers** (magnitude, not direction):", ""]
    for hid in ("H1", "H2", "H3"):
        h = er.get("hypotheses", {}).get(hid)
        if not h:
            continue
        lines.append(
            f"- **{hid} {h.get('label', '')}** — {h.get('amplifier', '?')} "
            f"(latest {h.get('latest', '?')} vs event median "
            f"{h.get('event_median', '?')})")
    gpr = er.get("gpr_context") or {}
    if gpr:
        lines += ["", f"GPR context: {gpr.get('gpr_pct', '?')}th percentile "
                  f"({gpr.get('gpr_value', '?')}) — descriptive only.", ""]

    # This situation's channels -> their clustered base rates (verbatim).
    by_type = {b["type"]: b for b in er.get("base_rates", [])}
    kinds = sit.get("dominant_kinds", [])
    lines += ["**Base rates for this situation's channels** (clustered abnormal "
              "return vs baseline, %):", "",
              "| channel | n | CAR+1 | CAR+5 | CAR+10 | CAR+20 |",
              "|---|---|---|---|---|---|"]
    for k in kinds:
        b = by_type.get(k)
        if b:
            lines.append(f"| {k} | {b['n']} | {b['car1']} | {b['car5']} | "
                         f"{b['car10']} | {b['car20']} |")
        else:
            lines.append(f"| {k} | — | (not in engine_read base rates) | | | |")
    lines.append("")
    return "\n".join(lines)


def _timeline_md(conn, sid):
    """The observed, sourced timeline (newest first), capped for readability."""
    total = conn.execute("SELECT COUNT(*) FROM situation_log WHERE situation_id=?",
                         (sid,)).fetchone()[0]
    rows = conn.execute(
        "SELECT ts, status, kind, headline, source_url FROM situation_log "
        "WHERE situation_id=? ORDER BY ts DESC, log_id DESC LIMIT ?",
        (sid, TIMELINE_CAP)).fetchall()
    out = [f"## Timeline — observed & sourced ({total} atoms"
           + (f", newest {TIMELINE_CAP} shown" if total > TIMELINE_CAP else "")
           + ")", ""]
    if not rows:
        out += ["_No atoms attached yet — run the attach step against the "
                "watcher's alert queue._", ""]
        return "\n".join(out)
    out += ["| date | status | kind | headline | source |",
            "|---|---|---|---|---|"]
    for ts, status, kind, headline, url in rows:
        safe = (headline or "").replace("|", "\\|")
        out.append(f"| {(ts or '')[:10]} | {status} | {kind} | {safe} | "
                   f"[link]({url}) |")
    out.append("")
    return "\n".join(out)


def render_dossier(conn, sit, er, now):
    """Assemble the full dossier markdown for one situation. Pure formatter."""
    sid = sit["situation_id"]
    md = [f"# Situation dossier — {sit.get('title', sid)}", "",
          f"_situation_id: `{sid}` · status: **{sit.get('status', '?')}** · "
          f"started {sit.get('started_at', '?')} · generated {now}_", "",
          "_Deterministic assembly (attach + priced-state). The synthesis section "
          "is agent-authored and currently pending._", "",
          "## Where we stand — synthesis (pending)", "",
          "> The narrative read (\"where we stand\": actor postures, which channels "
          "have fired, the plain-English situation) is written by the scoped "
          "research agent in a later slice. It is intentionally blank now — the "
          "engine never fabricates prose. The facts below are deterministic and "
          "sourced.", "",
          _priced_state_md(conn, sit, er), "",
          _timeline_md(conn, sid), "",
          "---", f"_{CAVEAT}_", ""]
    return "\n".join(md)


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    situations = load_situations()
    alerts = read_alerts()
    if not situations:
        print("No situations defined in data/situations.yaml -- nothing to do.")
        return
    conn = sqlite3.connect(DB)
    inserted = attach(conn, situations, alerts, now)
    conn.commit()

    DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
    er = load_engine_read()
    print(f"Situation Memory -- {now}")
    print(f"  situations: {len(situations)}   alerts scanned: {len(alerts)}   "
          f"new atoms: {inserted}")
    for sit in situations:
        sid = sit["situation_id"]
        n = conn.execute("SELECT COUNT(*) FROM situation_log WHERE situation_id=?",
                         (sid,)).fetchone()[0]
        out = DOSSIER_DIR / f"{sid}.md"
        out.write_text(render_dossier(conn, sit, er, now))
        print(f"    {sid:<34} {n:>4} atoms  ->  {out.relative_to(ROOT)}")
    conn.close()


if __name__ == "__main__":
    main()
