"""
watcher.py -- THE WATCHER. A live-news attention layer for the engine.

THE ONE RULE (non-negotiable): THE WATCHER CURATES ATTENTION, IT NEVER CONCLUDES.
It reads free news streams, keeps only the items that hit Joe's net (the keyword
file + the entity table), and writes them as ALERT CARDS for Joe to look at. It
codes nothing, scores nothing, decides nothing. Only Joe turns an alert into a
candidate event (promote_alert.py), and only Joe turns a candidate into an event.
The gate stays a gate, forever.

ONE CYCLE PER RUN. No daemon, no cron, no scheduler here -- you run it, it does a
single polite pass and exits:
  1. GDELT 2.0 live -- the single latest 15-minute event export. Parsed with
     harvest_gdelt.py's own column map (imported, not forked); GDELT 2.0's
     SOURCEURL is the last column.
  2. RSS -- one pass over the feeds in data/watch_feeds.txt.
  3. Dedup against everything seen before (data/watch_seen.db, a tiny separate
     SQLite so the canonical oil.db stays clean).
Anything unreachable is printed plainly and skipped -- a partial cycle is fine;
silence is not.

Every net hit becomes one row in data/alert_queue.csv (append-only; the watcher
never edits an existing row -- Joe owns the status column). Each card carries:
timestamp, source, headline, url, matched entities, matched keywords, a HEURISTIC
closest-event-type guess (labelled as such), and today's read line copied verbatim
from engine_read.json. No other generated text.

Run:  python3 src/watcher.py             # one cycle, verbose
      python3 src/watcher.py --summary   # one cycle, one-screen digest of new alerts
"""

import argparse
import csv
import hashlib
import io
import json
import re
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

# Reuse harvest_gdelt's parsing -- import, do not fork.
from harvest_gdelt import (PRODUCERS, ATTACK_ROOTS, SANCTION_CODE, I_SQLDATE,
                           I_A1CC, I_A2CC, I_A1NAME, I_A2NAME, I_EVENTCODE,
                           I_ROOTCODE, I_NUMMENTIONS)

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
KEYWORDS_FILE = ROOT / "data" / "watch_keywords.txt"
FEEDS_FILE = ROOT / "data" / "watch_feeds.txt"
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
SEEN_DB = ROOT / "data" / "watch_seen.db"          # tiny, separate; keeps oil.db clean
ENGINE_READ = ROOT / "data" / "engine_read.json"

GDELT_LASTUPDATE = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
UA = {"User-Agent": "ripple-engine watcher (research; polite, one pull/cycle)"}
GDELT_MIN_MENTIONS = 3        # ignore near-zero-coverage GDELT rows (noise floor)

ALERT_FIELDS = ["timestamp_utc", "source", "headline", "url", "matched_entities",
                "matched_keywords", "heuristic_type", "amp_context", "status"]

# CAMEO country codes for the entity-table countries (extends harvest_gdelt's
# producer set to the whole entity net). Anything not here is simply not matched.
# USA is deliberately OMITTED from the GDELT actor net: as a lone actor it floods
# the stream with domestic-politics noise. US oil relevance still surfaces via the
# OTHER actor (e.g. "USA sanctions IRAN" matches on IRN) and via RSS keywords.
COUNTRY_CC = {
    "iran": "IRN", "iraq": "IRQ", "saudi_arabia": "SAU", "russia": "RUS",
    "libya": "LBY", "venezuela": "VEN", "kuwait": "KWT", "uae": "ARE",
    "ukraine": "UKR", "georgia": "GEO", "israel": "ISR", "lebanon": "LBN",
    "yemen": "YEM", "thailand": "THA",
}

# Heuristic keyword -> closest playbook event type. LABELLED heuristic; it is a
# hint for Joe's eye, never a coding.
TYPE_MAP = [
    (("opec", "spare capacity"), "opec_decision"),
    (("spr", "strategic reserve", "iea"), "policy_response"),
    (("sanctions", "embargo", "price cap"), "sanctions"),
    (("refinery", "pipeline", "tanker", "oil field", "crude"), "infrastructure_attack"),
    (("strait", "hormuz", "suez", "bab el-mandeb", "chokepoint", "blockade",
      "red sea", "houthi"), "chokepoint_disruption"),
    (("missile", "drone strike", "airstrike", "escalation", "mobilization",
      "ceasefire", "nuclear", "enrichment"), "conflict_escalation"),
]


# --------------------------------------------------------------- the net (inputs)

def load_keywords():
    """Joe's keyword net -- reloaded every cycle so his edits take effect at once."""
    if not KEYWORDS_FILE.exists():
        return []
    out = []
    for line in KEYWORDS_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line.lower())
    return out


def load_feeds():
    """Return [(name, url)] from watch_feeds.txt."""
    if not FEEDS_FILE.exists():
        return []
    feeds = []
    for line in FEEDS_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            feeds.append((parts[0], parts[1]))
    return feeds


def load_entity_net(conn):
    """Entity match terms (for RSS text) and country codes (for GDELT actors).
    Skips tiny/ambiguous names (usa/eu/who) that would false-match everything."""
    rows = conn.execute("SELECT entity_id, type, name FROM entities").fetchall()
    terms, codes = {}, set()
    stop = {"usa", "eu", "who"}
    for eid, etype, name in rows:
        if etype in ("country", "chokepoint", "commodity", "institution"):
            nm = (name or "").lower()
            if len(nm) >= 3 and nm not in stop:
                terms[nm] = eid                      # matchable name -> entity id
        if etype == "country":
            key = eid.split(".", 1)[1]               # 'country.iran' -> 'iran'
            if key in COUNTRY_CC:
                codes.add(COUNTRY_CC[key])
    return terms, codes


def net_match_text(text, keywords, entity_terms):
    """Return (matched_keywords, matched_entities) for a piece of headline text."""
    low = text.lower()
    kw = [k for k in keywords if k in low]
    ents = [entity_terms[t] for t in entity_terms
            if re.search(rf"\b{re.escape(t)}\b", low)]
    return kw, sorted(set(ents))


def heuristic_type(matched_keywords, matched_entities):
    """Closest playbook type from the keyword map (a hint, not a coding)."""
    for terms, etype in TYPE_MAP:
        if any(k in terms for k in matched_keywords):
            return etype
    if any("chokepoint." in e for e in matched_entities):
        return "chokepoint_disruption"
    return "unmapped"


def amp_context():
    """Today's read line, copied verbatim from engine_read.json (no generation)."""
    if ENGINE_READ.exists():
        try:
            return json.loads(ENGINE_READ.read_text()).get("read", "").strip()
        except (ValueError, OSError):
            pass
    return "n/a (run engine_read.py)"


# --------------------------------------------------------------- dedup (seen db)

def open_seen():
    conn = sqlite3.connect(SEEN_DB)
    conn.execute("CREATE TABLE IF NOT EXISTS seen "
                 "(story_hash TEXT PRIMARY KEY, first_seen TEXT)")
    return conn


def is_new(seen, url):
    """True and marks it if this url hasn't been seen before."""
    h = hashlib.sha1(url.encode("utf-8", "replace")).hexdigest()
    if seen.execute("SELECT 1 FROM seen WHERE story_hash=?", (h,)).fetchone():
        return False
    seen.execute("INSERT INTO seen VALUES (?,?)",
                 (h, datetime.now(timezone.utc).isoformat(timespec="seconds")))
    return True


# --------------------------------------------------------------- GDELT live

def gdelt_category(root, code):
    if code == SANCTION_CODE:
        return "sanctions/embargo signal"
    return {"20": "mass-violence signal", "19": "fight/clash signal",
            "18": "assault signal"}.get(root, "event signal")


def run_gdelt(seen, keywords, net_codes, now):
    """Pull the single latest 15-min export and return net-matching alert dicts."""
    try:
        last = requests.get(GDELT_LASTUPDATE, headers=UA, timeout=30).text
        export_url = next(l.split()[-1] for l in last.splitlines() if "export" in l)
        content = requests.get(export_url, headers=UA, timeout=60).content
        zf = zipfile.ZipFile(io.BytesIO(content))
        rows = zf.read(zf.namelist()[0]).decode("utf-8", "replace").splitlines()
    except (requests.RequestException, StopIteration, zipfile.BadZipFile) as e:
        print(f"  GDELT unreachable this cycle ({type(e).__name__}) -- skipped.")
        return []

    alerts = []
    for line in rows:
        c = line.split("\t")
        if len(c) < 61:                              # GDELT 2.0 export has 61 cols
            continue
        a1cc, a2cc = c[I_A1CC], c[I_A2CC]
        n1, n2 = c[I_A1NAME].upper(), c[I_A2NAME].upper()
        entity_hit = (a1cc in net_codes or a2cc in net_codes
                      or "OPEC" in n1 or "OPEC" in n2)
        root, code = c[I_ROOTCODE], c[I_EVENTCODE]
        if not entity_hit or not (root in ATTACK_ROOTS or code == SANCTION_CODE):
            continue
        try:
            if int(c[I_NUMMENTIONS]) < GDELT_MIN_MENTIONS:
                continue
        except ValueError:
            continue
        url = c[-1].strip()                          # SOURCEURL = last column in 2.0
        if not url.startswith("http") or not is_new(seen, url):
            continue
        matched_kw = [k for k in keywords if k in url.lower()]
        ents = sorted({e for e in net_codes if e in (a1cc, a2cc)})
        if "OPEC" in n1 or "OPEC" in n2:
            ents.append("institution.opec")
        headline = (f"[GDELT] {c[I_A1NAME] or a1cc or '?'} / "
                    f"{c[I_A2NAME] or a2cc or '?'}: {gdelt_category(root, code)}")
        alerts.append({
            "timestamp_utc": now, "source": "gdelt", "headline": headline,
            "url": url, "matched_entities": ";".join(ents),
            "matched_keywords": ";".join(matched_kw),
            "heuristic_type": heuristic_type(matched_kw, ents),
            "amp_context": "", "status": "new"})
    return alerts


# --------------------------------------------------------------- RSS

def run_rss(seen, keywords, entity_terms, now):
    """One pass over the feeds; net-matching entries become alerts."""
    alerts = []
    for name, url in load_feeds():
        try:
            resp = requests.get(url, headers=UA, timeout=25)
            feed = feedparser.parse(resp.content)
            if not feed.entries:
                print(f"  rss:{name} returned 0 entries -- skipped this cycle.")
                continue
        except requests.RequestException as e:
            print(f"  rss:{name} unreachable ({type(e).__name__}) -- skipped.")
            continue
        for entry in feed.entries:
            link = (entry.get("link") or "").strip()
            title = (entry.get("title") or "").strip()
            if not link or not title:
                continue
            text = title + " " + (entry.get("summary") or "")
            kw, ents = net_match_text(text, keywords, entity_terms)
            if not kw and not ents:
                continue
            if not is_new(seen, link):
                continue
            alerts.append({
                "timestamp_utc": now, "source": f"rss:{name}", "headline": title,
                "url": link, "matched_entities": ";".join(ents),
                "matched_keywords": ";".join(kw),
                "heuristic_type": heuristic_type(kw, ents),
                "amp_context": "", "status": "new"})
    return alerts


# --------------------------------------------------------------- output

def append_alerts(alerts):
    new_file = not ALERT_QUEUE.exists()
    with open(ALERT_QUEUE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ALERT_FIELDS)
        if new_file:
            w.writeheader()
        for a in alerts:
            w.writerow(a)


def print_verbose(alerts, ctx):
    by_src = {}
    for a in alerts:
        by_src[a["source"].split(":")[0]] = by_src.get(a["source"].split(":")[0], 0) + 1
    print(f"\nNew alerts this cycle: {len(alerts)}  "
          f"({', '.join(f'{k}={v}' for k, v in sorted(by_src.items())) or 'none'})")
    print(f"Today's read (context copied onto each card): {ctx or 'n/a'}\n")
    for a in alerts:
        print(f"  [{a['source']}] {a['heuristic_type']:<22} {a['headline'][:70]}")
        print(f"     ents: {a['matched_entities'] or '-'}  | kw: {a['matched_keywords'] or '-'}")
        print(f"     {a['url'][:90]}")


def print_summary(alerts, ctx):
    print(f"\n=== WATCHER DIGEST -- {len(alerts)} new alert(s) ===")
    print(f"read: {ctx or 'n/a'}")
    for a in alerts:
        print(f"  {a['source']:<14} {a['heuristic_type']:<22} {a['headline'][:60]}")
    if not alerts:
        print("  (nothing new hit the net this cycle)")


def main():
    ap = argparse.ArgumentParser(description="The Watcher -- one polling cycle.")
    ap.add_argument("--summary", action="store_true",
                    help="print a one-screen digest of new alerts instead of the full log")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ctx = amp_context()
    keywords = load_keywords()
    conn = sqlite3.connect(DB)
    entity_terms, net_codes = load_entity_net(conn)
    conn.close()
    seen = open_seen()

    if not args.summary:
        print(f"Watcher cycle {now}  |  {len(keywords)} keywords, "
              f"{len(entity_terms)} entity terms, {len(net_codes)} country codes")

    gdelt = run_gdelt(seen, keywords, net_codes, now)
    rss = run_rss(seen, keywords, entity_terms, now)
    seen.commit()
    seen.close()

    alerts = gdelt + rss
    for a in alerts:                                 # stamp the read line onto each card
        a["amp_context"] = ctx
    append_alerts(alerts)

    (print_summary if args.summary else print_verbose)(alerts, ctx)
    if not args.summary:
        print(f"\nAppended to {ALERT_QUEUE.name}. Joe reviews; promote with "
              f"promote_alert.py. Nothing here is an event.")


if __name__ == "__main__":
    main()
