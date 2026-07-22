"""
harvest_gdelt.py -- propose event CANDIDATES from GDELT (never auto-ingest).

WHAT THIS DOES:
Scans GDELT's global event files for military clashes / attacks / sanctions that
involve a major oil producer, aggregates the coverage, and writes the biggest
ones as CANDIDATES into data/candidate_events.csv for Joe to review. It NEVER
writes to the events table -- that only happens when Joe approves a candidate
(review_candidates.py -> events.csv -> load_events.py). Automated ingestion of
unverified events is exactly the failure mode this project is built against.

HONEST SCOPE (read this):
  * GDELT's per-event source URL (which every candidate needs, per the codebook)
    only exists in the daily export files from APRIL 2013 onward. So GDELT
    harvesting here covers 2013-present; the 1987-2012 decades are served by the
    manually-seeded, hand-sourced candidates instead. We say this rather than
    inventing URLs for older events.
  * The full daily archive is thousands of ~13 MB files -- too heavy to pull in
    one go on a laptop. So we SAMPLE dates (default: semi-annual) and say so in
    the output. GDELT re-reports a major event for weeks, so a sampled day still
    catches big events whose event-date (SQLDATE) is discussed that day. Run with
    a denser cadence (quarterly/monthly) for fuller coverage.

Filter (per TASK_BRIEF_03): CAMEO root codes 18/19/20 (assault / fight / mass
violence) or code 163 (embargo/sanctions), where either actor's country is a
major producer (Iraq, Iran, Saudi, Russia, Libya, Venezuela, Kuwait, UAE) or the
actor is OPEC.

Run:  python3 src/harvest_gdelt.py [semiannual|quarterly|monthly]
"""

import csv
import io
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "candidate_events.csv"
EVENTS = ROOT / "data" / "events.csv"

GDELT_BASE = "http://data.gdeltproject.org/events/"
UA = {"User-Agent": "Mozilla/5.0 (ripple-engine research harvester)"}

# GDELT 1.0 daily export files (tab-delimited, 58 columns) begin 2013-04-01.
FIRST_YEAR = 2013

# Column indices in the GDELT 1.0 export schema (verified against a live file).
I_SQLDATE, I_A1CC, I_A2CC = 1, 7, 17
I_A1NAME, I_A2NAME = 6, 16
I_EVENTCODE, I_ROOTCODE, I_NUMMENTIONS = 26, 28, 31
I_SOURCEURL = 57

# Major producers, as GDELT/CAMEO 3-letter country codes.
PRODUCERS = {
    "IRQ": "iraq", "IRN": "iran", "SAU": "saudi_arabia", "RUS": "russia",
    "LBY": "libya", "VEN": "venezuela", "KWT": "kuwait", "ARE": "uae",
}
ATTACK_ROOTS = {"18", "19", "20"}   # assault / fight / mass violence
SANCTION_CODE = "163"               # embargo, boycott, sanction

# Keep an aggregated event only if its peak single-day coverage clears this, and
# cap the number of candidates so the output is reviewable (hundreds, not floods).
PEAK_MENTIONS_MIN = 25
MAX_CANDIDATES = 300
DEDUPE_DAYS = 3                     # +/- window for "same event already known"

SAMPLE_DAYS = {
    "semiannual": [(1, 15), (7, 15)],
    "quarterly":  [(1, 15), (4, 15), (7, 15), (10, 15)],
    "monthly":    [(m, 15) for m in range(1, 13)],
}


def sample_dates(cadence):
    """Build the list of YYYYMMDD file dates to fetch, given a sampling cadence."""
    today = datetime.now(timezone.utc).date()
    out = []
    for year in range(FIRST_YEAR, today.year + 1):
        for month, day in SAMPLE_DAYS[cadence]:
            # daily files start 2013-04-01; nothing exists after today
            if year == FIRST_YEAR and month < 4:
                continue
            if datetime(year, month, day).date() > today:
                continue
            out.append(f"{year}{month:02d}{day:02d}")
    return out


def scan_file(yyyymmdd, agg):
    """Download one daily file, keep qualifying rows, fold them into `agg`.

    agg key = (event_date, a1cc, a2cc); value = dict(mentions_total, peak,
    source_url [from the peak row], code, name1, name2). Returns rows scanned,
    or None if the file couldn't be fetched.
    """
    url = f"{GDELT_BASE}{yyyymmdd}.export.CSV.zip"
    try:
        r = requests.get(url, headers=UA, timeout=90)
        r.raise_for_status()
    except requests.RequestException:
        return None
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
    except zipfile.BadZipFile:
        return None

    scanned = 0
    for name in z.namelist():
        for line in io.TextIOWrapper(z.open(name), encoding="utf-8", errors="replace"):
            scanned += 1
            c = line.rstrip("\n").split("\t")
            if len(c) <= I_SOURCEURL:
                continue
            a1cc, a2cc = c[I_A1CC], c[I_A2CC]
            n1, n2 = c[I_A1NAME].upper(), c[I_A2NAME].upper()
            # Must involve a producer country or OPEC...
            producer_hit = a1cc in PRODUCERS or a2cc in PRODUCERS \
                or "OPEC" in n1 or "OPEC" in n2
            if not producer_hit:
                continue
            # ...and be an attack/clash or a sanctions action.
            root, code = c[I_ROOTCODE], c[I_EVENTCODE]
            is_attack = root in ATTACK_ROOTS
            is_sanction = code == SANCTION_CODE
            if not (is_attack or is_sanction):
                continue
            try:
                mentions = int(c[I_NUMMENTIONS])
            except ValueError:
                continue

            key = (c[I_SQLDATE], a1cc, a2cc)
            rec = agg.get(key)
            if rec is None:
                rec = {"mentions_total": 0, "peak": -1, "source_url": "",
                       "kind": "sanctions" if is_sanction else "attack",
                       "name1": c[I_A1NAME], "name2": c[I_A2NAME]}
                agg[key] = rec
            rec["mentions_total"] += mentions
            if mentions > rec["peak"]:            # keep the most-mentioned article
                rec["peak"] = mentions
                rec["source_url"] = c[I_SOURCEURL]
    return scanned


# ---- Dedupe against events we already know (existing events + prior candidates) ----

def _read_csv(path):
    if not path.exists():
        return []
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def known_event_keys():
    """(date, producer_code) pairs already covered by events.csv or candidates.

    We map each existing row's entities/actors to producer codes so a GDELT hit on
    the same producer within +/- DEDUPE_DAYS is treated as already-known.
    """
    name_to_code = {v: k for k, v in PRODUCERS.items()}
    keys = []
    for path in (EVENTS, CANDIDATES):
        for row in _read_csv(path):
            d = row.get("event_date", "")
            try:
                dt = datetime.strptime(d, "%Y-%m-%d").date()
            except ValueError:
                continue
            ents = (row.get("entities", "") or "").lower()
            for cc, nm in PRODUCERS.items():
                if f"country.{nm}" in ents:
                    keys.append((dt, cc))
    return keys


def is_duplicate(event_date, codes, known):
    """True if this (date, producer) is within +/- DEDUPE_DAYS of a known event."""
    try:
        dt = datetime.strptime(event_date, "%Y%m%d").date()
    except ValueError:
        return True  # unparseable date -> don't emit
    for kd, kc in known:
        if kc in codes and abs((dt - kd).days) <= DEDUPE_DAYS:
            return True
    return False


def build_candidate_row(key, rec):
    """Turn one aggregated GDELT event into a candidate_events.csv row (dict)."""
    sqldate, a1cc, a2cc = key
    dt = datetime.strptime(sqldate, "%Y%m%d").date()
    producers = [PRODUCERS[c] for c in (a1cc, a2cc) if c in PRODUCERS]
    label = " / ".join(p.replace("_", " ").title() for p in producers) or "producer"
    etype = "sanctions" if rec["kind"] == "sanctions" else "conflict_escalation"
    verb = "sanctions action" if rec["kind"] == "sanctions" else "military clash / attack"
    who = " and ".join(filter(None, [rec["name1"].title(), rec["name2"].title()]))
    eid = f"gdelt_{a1cc.lower() or 'x'}_{a2cc.lower() or 'x'}_{sqldate}"
    # entities: attach producers + the oil markets. Actor/target is ambiguous from
    # GDELT alone, so both go in as 'location' for Joe to refine on review.
    ent = ";".join([f"country.{PRODUCERS[c]}:location" for c in (a1cc, a2cc)
                    if c in PRODUCERS] + ["commodity.brent:affected_market"])
    return {
        "event_id": eid,
        "event_date": dt.isoformat(),
        "date_precision": "day",
        "type": etype,
        "title": f"GDELT candidate: {verb} involving {label} ({dt.isoformat()})",
        "description": (f"AUTO-HARVESTED, UNVERIFIED. GDELT recorded a {verb} "
                        f"(actors: {who or 'n/a'}), peak {rec['peak']} mentions, "
                        f"{rec['mentions_total']} total across sampled files. Joe "
                        f"must verify the source and code severity/surprise before "
                        f"approval."),
        "severity": 3,   # neutral placeholder; real coding is Joe's on review
        "surprise": 3,
        "confidence": "low",
        "source_url": rec["source_url"],
        "entities": ent,
        "status": "candidate",
        "candidate_source": "gdelt",
    }


FIELDNAMES = ["event_id", "event_date", "date_precision", "type", "title",
              "description", "severity", "surprise", "confidence", "source_url",
              "entities", "status", "candidate_source"]


def main():
    cadence = sys.argv[1] if len(sys.argv) > 1 else "semiannual"
    if cadence not in SAMPLE_DAYS:
        print(f"Unknown cadence '{cadence}'. Choose: {', '.join(SAMPLE_DAYS)}")
        return

    dates = sample_dates(cadence)
    print(f"GDELT harvest ({cadence} sample): {len(dates)} daily files, "
          f"{dates[0]}..{dates[-1]}")
    print("NOTE: this is a SAMPLE of GDELT, not a full scan -- see the file header "
          "for why.\n")

    agg, fetched, scanned_total = {}, 0, 0
    for i, d in enumerate(dates, 1):
        scanned = scan_file(d, agg)
        if scanned is None:
            print(f"  [{i:>3}/{len(dates)}] {d}  skipped (unreachable)")
            continue
        fetched += 1
        scanned_total += scanned
        print(f"  [{i:>3}/{len(dates)}] {d}  {scanned:>7,} rows, "
              f"{len(agg):>5} distinct producer-events so far")

    if not agg:
        print("\nNo qualifying events found in the sample. Try a denser cadence.")
        return

    # Keep the well-covered events, dedupe against what we already know, cap.
    known = known_event_keys()
    kept = []
    for key, rec in agg.items():
        if rec["peak"] < PEAK_MENTIONS_MIN or not rec["source_url"]:
            continue
        codes = {c for c in (key[1], key[2]) if c in PRODUCERS}
        if is_duplicate(key[0], codes, known):
            continue
        kept.append((key, rec))
    kept.sort(key=lambda kr: kr[1]["mentions_total"], reverse=True)
    kept = kept[:MAX_CANDIDATES]

    # Append to the candidate file (create with header if it somehow doesn't exist).
    write_header = not CANDIDATES.exists()
    with open(CANDIDATES, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            w.writeheader()
        for key, rec in kept:
            w.writerow(build_candidate_row(key, rec))

    print(f"\nScanned {scanned_total:,} GDELT rows across {fetched} files.")
    print(f"Aggregated {len(agg):,} producer-events; after the "
          f"{PEAK_MENTIONS_MIN}-mention floor + dedupe, appended "
          f"{len(kept)} GDELT candidates to {CANDIDATES.name}.")
    print("These are UNVERIFIED. Review them with: python3 src/review_candidates.py")


if __name__ == "__main__":
    main()
