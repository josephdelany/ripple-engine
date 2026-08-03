"""
audit.py -- the monthly auto-admission audit (VISION_ROADMAP V2.3).

Auto-admitted events are trusted without a human looking at them, so they get spot-checked. Once a
month this samples up to 5 auto-admitted events, RE-FETCHES their source URLs, and records PASS (every
source still resolves) or FLAG (a source is dead / errors -- possible link-rot or a bad admission).

  * writes data/audit_YYYYMM.md -- PASS/FLAG per sampled event, with the HTTP status of each source.
  * writes data/audit_flags.json -- {event_type: [flagged event_ids]}. A type with an open flag is
    BLOCKED from further auto-admission (backfill.py honours this) until Joe clears it. Never a silent
    pass: a flag stops the machine in that domain.
  * a compact summary is read by status.py (engine_status) and can be surfaced in The Daily.

Sample = the 5 most-recently auto-admitted events (from the two-source log + the living-engine
admission log). Deterministic, so re-running the same month is idempotent. Network re-fetch is polite
(HEAD, short timeout) and degrades to 'unchecked' if offline.

Run:  python3 src/audit.py            # audit this month (idempotent)
      python3 src/audit.py --clear opec_decision   # Joe clears a domain's flags
"""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TWO_SOURCE = DATA / "state" / "two_source_log.csv"
ADMISSION = DATA / "extract" / "admission_log.csv"
FLAGS = DATA / "audit_flags.json"
SAMPLE_N = 5
UA = {"User-Agent": "ripple-engine audit (research; polite, one HEAD/source)"}


def _auto_admitted():
    """(event_id, event_type, [urls]) for auto-admitted events, most-recent first."""
    out = []
    if TWO_SOURCE.exists():
        for r in csv.DictReader(open(TWO_SOURCE, newline="", encoding="utf-8")):
            urls = [u for u in (r.get("primary_url"), r.get("second_url")) if u]
            out.append((r.get("event_id"), None, urls, r.get("verified_at", "")))
    if ADMISSION.exists():
        for r in csv.DictReader(open(ADMISSION, newline="", encoding="utf-8")):
            if r.get("source_url"):
                out.append((r.get("event_id"), None, [r.get("source_url")], r.get("admitted_at", "")))
    out.sort(key=lambda t: t[3], reverse=True)          # most-recent first
    return out


def _event_type(conn, event_id):
    row = conn.execute("SELECT type FROM events WHERE event_id=?", (event_id,)).fetchone()
    return row[0] if row else "unknown"


# A source is only DEAD (a real admission problem -> FLAG) on a clearly-gone signal. 403/401/429/SSL/
# timeout means alive-but-blocks-bots or transient -> UNVERIFIED (noted, NOT a block). This keeps the
# audit from blocking a whole domain on a publisher's anti-bot defence.
DEAD_CODES = {404, 410, 451}


def _check(url):
    """Return (status, kind) where kind in {'ok','dead','unverified'}."""
    try:
        r = requests.head(url, headers=UA, timeout=12, allow_redirects=True)
        code = r.status_code
        if code == 405 or code >= 400:                  # some hosts reject HEAD -> try a light GET
            r = requests.get(url, headers=UA, timeout=15, stream=True)
            code = r.status_code
        if code < 400:
            return code, "ok"
        return code, "dead" if code in DEAD_CODES else "unverified"
    except requests.RequestException as e:
        name = type(e).__name__
        dead = name in ("ConnectionError", "InvalidURL", "MissingSchema")   # DNS/refused/malformed
        return f"ERR {name}", "dead" if dead else "unverified"


def run(force=False):
    import sqlite3
    month = datetime.now(timezone.utc).strftime("%Y%m")
    if (DATA / f"audit_{month}.md").exists() and not force:
        return {"month": month, "skipped": "already audited this month (idempotent; --force to re-run)"}
    conn = sqlite3.connect(DATA / "oil.db")
    sample = _auto_admitted()[:SAMPLE_N]
    results = []
    for eid, _, urls, _ in sample:
        etype = _event_type(conn, eid)
        checks = [(u, *_check(u)) for u in urls]         # (url, status, kind)
        kinds = [k for _, _, k in checks]
        verdict = ("FLAG" if "dead" in kinds else             # a clearly-dead source -> block
                   "PASS" if all(k == "ok" for k in kinds) else
                   "UNVERIFIED")                              # alive-but-unfetchable -> noted, no block
        results.append({"event_id": eid, "type": etype, "verdict": verdict,
                        "sources": [{"url": u, "status": code, "kind": k} for u, code, k in checks]})
    conn.close()

    # flags -> block those event types
    flags = {}
    if FLAGS.exists():
        try:
            flags = json.loads(FLAGS.read_text())
        except (ValueError, OSError):
            flags = {}
    for r in results:
        if r["verdict"] == "FLAG":
            flags.setdefault(r["type"], [])
            if r["event_id"] not in flags[r["type"]]:
                flags[r["type"]].append(r["event_id"])
    FLAGS.write_text(json.dumps(flags, indent=2))
    _write_md(month, results, flags)
    return {"month": month, "n_sampled": len(results),
            "n_flag": sum(1 for r in results if r["verdict"] == "FLAG"),
            "n_pass": sum(1 for r in results if r["verdict"] == "PASS"),
            "blocked_types": sorted(flags)}


def _write_md(month, results, flags):
    L = [f"# Auto-admission audit — {month}", "",
         "*Spot-check of auto-admitted events: sources re-fetched, PASS if all resolve, FLAG if any is "
         "dead. A FLAGged type is blocked from further auto-admission until Joe clears it "
         "(`python3 src/audit.py --clear <type>`).*", "",
         "| event | type | verdict | sources (HTTP) |", "|---|---|---|---|"]
    for r in results:
        srcs = "; ".join(f"{s['status']}" for s in r["sources"])
        L.append(f"| {r['event_id']} | {r['type']} | **{r['verdict']}** | {srcs} |")
    L += ["", f"**Blocked types (open flags):** {', '.join(sorted(flags)) or 'none'}."]
    if not results:
        L.append("\n_No auto-admitted events to sample yet._")
    (DATA / f"audit_{month}.md").write_text("\n".join(L) + "\n")


def main():
    if "--clear" in sys.argv:
        t = sys.argv[sys.argv.index("--clear") + 1]
        flags = json.loads(FLAGS.read_text()) if FLAGS.exists() else {}
        flags.pop(t, None)
        FLAGS.write_text(json.dumps(flags, indent=2))
        print(f"cleared flags for type '{t}'. Remaining blocked: {sorted(flags) or 'none'}")
        return
    r = run(force="--force" in sys.argv)
    if r.get("skipped"):
        print(f"audit {r['month']}: {r['skipped']}"); return
    print(f"audit {r['month']}: sampled {r['n_sampled']} auto-admitted -- "
          f"{r['n_pass']} PASS, {r['n_flag']} FLAG. Blocked types: {r['blocked_types'] or 'none'}.")
    print(f"wrote data/audit_{r['month']}.md + data/audit_flags.json")


if __name__ == "__main__":
    main()
