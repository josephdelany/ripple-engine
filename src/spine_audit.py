#!/usr/bin/env python3
"""
spine_audit.py -- the honest baseline for the event spine (Session E, step E-1).

WHAT THIS IS
The corpus (the `events` table) is the spine of the whole engine: every analog, every
label, every Big Moves attribution hangs off it. The paper (docs/PAPER_DRAFT.md Sec 3)
already calls this layer "the study's principal weakness". This script measures that
weakness precisely, per event, so the repair can be scored against a number instead of
an impression.

It is READ-ONLY. It opens data/oil.db with the sqlite read-only URI, writes nothing to
any table, and produces two files under data/spine/:
    AUDIT.md    -- the published, human-readable baseline
    audit.json  -- the same numbers, for later runs to diff against

WHAT IT MEASURES, per event (E-1)
  n_source_domains   distinct registrable domains across source_url and every URL that
                     appears in sr_json.sources. This is the two-source rule's own
                     yardstick: one domain means one source, whatever the field count.
  desc_len           description length in characters. A case narrative is ~120-250
                     words (roughly 700-1600 chars); a sentence is ~150.
  sr_* provenance    of the field-source slots in sr_json.sources, the share that are
                     external URLs, corpus-derived ("corpus:..."), or null.
  placeholder        whether the description still carries drafting scaffolding
                     ("deep-history tier", "DRAFT coding", "placeholder", "TODO").
  n_entities         rows in event_entities for the event.
  ies90              whether an independent IES-90 level exists (event_outcomes,
                     source='ies90', field='level'), or the event is flagged
                     no_independent_outcome, or neither (uncovered).

Aggregates are reported per decade and per class (`events.type`), because the two tell
different stories: the historical tail is thin by decade, and the coding scaffolding is
concentrated in particular classes.

USAGE
    python3 src/spine_audit.py            # writes data/spine/AUDIT.md + audit.json
    python3 src/spine_audit.py --print    # also prints the summary tables to stdout

Nothing here decides anything. It is a measurement, published as computed.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "oil.db"
OUT_DIR = ROOT / "data" / "spine"

# Text below this line in AUDIT.md is hand-written and preserved when the file is
# regenerated. Everything above it is computed.
APPEND_SENTINEL = "<!-- APPENDED BELOW: hand-written, preserved across regeneration -->"

# Text that marks a record as still carrying drafting scaffolding rather than a finished
# narrative. Matched case-insensitively against the description.
PLACEHOLDER_MARKERS = ("deep-history tier", "draft coding", "placeholder", "todo")

# A source_url that names only a site root, not a document. These pass "every event MUST
# be sourced" while citing nothing a reader can check, so they are counted separately.
GENERIC_URL_SUFFIXES = ("eia.gov", "www.eia.gov", "opec.org", "www.opec.org")

# Encyclopaedia domains. The codebook requires "a primary or major-wire source"; an
# encyclopaedia is a tertiary summary of sources it does not itself constitute, so it is
# counted separately rather than as a source. SPINE_REGISTRATION Sec 1a: it may orient a
# search and is never cited.
TERTIARY_DOMAINS = ("wikipedia.org", "wikiwand.com", "britannica.com")


def domain_of(url: str | None) -> str | None:
    """Registrable-ish domain of a URL, or None if this is not a URL.

    We strip a leading 'www.' so that eia.gov and www.eia.gov count as ONE source, which
    is the conservative reading of the two-source rule.
    """
    if not url or not isinstance(url, str):
        return None
    u = url.strip()
    if not u.lower().startswith(("http://", "https://")):
        return None
    host = (urlparse(u).netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host or None


def is_generic_root(url: str | None) -> bool:
    """True when the URL points at a site root rather than a specific document."""
    if not url:
        return False
    p = urlparse(url.strip())
    path = (p.path or "").strip("/")
    return bool(p.netloc) and path == ""


def classify_source_slot(value) -> str:
    """One sr_json.sources slot -> 'external' | 'corpus' | 'null'.

    'corpus:...' values (corpus:density, corpus:observed, corpus:dyad) are derived from
    our own corpus, so they are self-referential: they cannot corroborate the corpus.
    """
    if value is None:
        return "null"
    if not isinstance(value, str):
        return "null"
    v = value.strip()
    if v == "" or v.lower() in ("null", "none", "unknown"):
        return "null"
    if v.lower().startswith("corpus:"):
        return "corpus"
    if v.lower().startswith(("http://", "https://")):
        return "external"
    # Anything else is a free-text note: not a checkable source, so not external.
    return "null"


def load_events(conn: sqlite3.Connection) -> list[dict]:
    """Every event with the columns the audit needs, plus its joins."""
    rows = [dict(r) for r in conn.execute(
        "SELECT event_id, event_date, date_precision, type, title, description, "
        "       severity, confidence, source_url, sr_json "
        "FROM events ORDER BY event_date, event_id"
    )]

    ent = defaultdict(int)
    for eid, n in conn.execute(
        "SELECT event_id, COUNT(*) FROM event_entities GROUP BY event_id"
    ):
        ent[eid] = n

    # IES-90: an independent level, or an explicit 'no independent outcome' flag.
    ies_level = {r[0] for r in conn.execute(
        "SELECT DISTINCT event_id FROM event_outcomes "
        "WHERE source='ies90' AND field='level'"
    )}
    ies_none = {r[0] for r in conn.execute(
        "SELECT DISTINCT event_id FROM event_outcomes "
        "WHERE source='ies90' AND field='no_independent_outcome'"
    )}

    for r in rows:
        r["decade"] = r["event_date"][:3] + "0s"
        desc = r["description"] or ""
        r["desc_len"] = len(desc)
        low = desc.lower()
        r["placeholder"] = any(m in low for m in PLACEHOLDER_MARKERS)
        r["placeholder_marker"] = next(
            (m for m in PLACEHOLDER_MARKERS if m in low), None)
        r["n_entities"] = ent.get(r["event_id"], 0)
        r["ies90"] = ("level" if r["event_id"] in ies_level
                      else "no_independent_outcome" if r["event_id"] in ies_none
                      else "uncovered")

        # --- sources ---------------------------------------------------------------
        domains: set[str] = set()
        d0 = domain_of(r["source_url"])
        if d0:
            domains.add(d0)
        r["source_url_generic_root"] = is_generic_root(r["source_url"])
        r["source_url_tertiary"] = bool(d0 and any(t in d0 for t in TERTIARY_DOMAINS))

        slots = Counter()
        try:
            sr = json.loads(r["sr_json"]) if r["sr_json"] else {}
        except (TypeError, ValueError):
            sr = {}
        sources = sr.get("sources") if isinstance(sr, dict) else None
        if isinstance(sources, dict):
            for v in sources.values():
                kind = classify_source_slot(v)
                slots[kind] += 1
                if kind == "external":
                    d = domain_of(v)
                    if d:
                        domains.add(d)
        r["sr_slots_total"] = sum(slots.values())
        r["sr_slots_external"] = slots["external"]
        r["sr_slots_corpus"] = slots["corpus"]
        r["sr_slots_null"] = slots["null"]
        r["domains"] = sorted(domains)
        r["n_source_domains"] = len(domains)
        r["n_tertiary_domains"] = sum(
            1 for dd in domains if any(t in dd for t in TERTIARY_DOMAINS))
        # domains that actually count as sources under the codebook
        r["n_citable_domains"] = r["n_source_domains"] - r["n_tertiary_domains"]
    return rows


def pct(num: int, den: int) -> float:
    return round(100.0 * num / den, 1) if den else 0.0


def group_stats(rows: list[dict]) -> dict:
    """The per-group block used for both the decade and the class tables."""
    n = len(rows)
    slots_tot = sum(r["sr_slots_total"] for r in rows)
    return {
        "n": n,
        "placeholder": sum(r["placeholder"] for r in rows),
        "placeholder_pct": pct(sum(r["placeholder"] for r in rows), n),
        "two_or_more_domains": sum(r["n_source_domains"] >= 2 for r in rows),
        "two_or_more_domains_pct": pct(sum(r["n_source_domains"] >= 2 for r in rows), n),
        "one_domain": sum(r["n_source_domains"] == 1 for r in rows),
        "zero_domains": sum(r["n_source_domains"] == 0 for r in rows),
        "generic_root_url": sum(r["source_url_generic_root"] for r in rows),
        "tertiary_source_url": sum(r["source_url_tertiary"] for r in rows),
        "any_tertiary_domain": sum(r["n_tertiary_domains"] > 0 for r in rows),
        "zero_citable_domains": sum(r["n_citable_domains"] == 0 for r in rows),
        "desc_len_median": int(statistics.median([r["desc_len"] for r in rows])) if n else 0,
        "desc_len_min": min([r["desc_len"] for r in rows]) if n else 0,
        "desc_len_max": max([r["desc_len"] for r in rows]) if n else 0,
        "desc_ge_700": sum(r["desc_len"] >= 700 for r in rows),
        "entities_median": int(statistics.median([r["n_entities"] for r in rows])) if n else 0,
        "entities_zero": sum(r["n_entities"] == 0 for r in rows),
        "sr_slots_total": slots_tot,
        "sr_external_pct": pct(sum(r["sr_slots_external"] for r in rows), slots_tot),
        "sr_corpus_pct": pct(sum(r["sr_slots_corpus"] for r in rows), slots_tot),
        "sr_null_pct": pct(sum(r["sr_slots_null"] for r in rows), slots_tot),
        "sr_majority_null": sum(
            r["sr_slots_total"] > 0 and r["sr_slots_null"] * 2 > r["sr_slots_total"]
            for r in rows),
        "ies90_level": sum(r["ies90"] == "level" for r in rows),
        "ies90_none": sum(r["ies90"] == "no_independent_outcome" for r in rows),
        "ies90_uncovered": sum(r["ies90"] == "uncovered" for r in rows),
        "severity_null": sum(r["severity"] is None for r in rows),
    }


def md_table(headers: list[str], lines: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for row in lines:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def build_report(rows: list[dict]) -> tuple[str, dict]:
    n = len(rows)
    overall = group_stats(rows)

    by_decade = {}
    for dec in sorted({r["decade"] for r in rows}):
        by_decade[dec] = group_stats([r for r in rows if r["decade"] == dec])
    by_class = {}
    for cls in sorted({r["type"] for r in rows}):
        by_class[cls] = group_stats([r for r in rows if r["type"] == cls])

    dom_counter = Counter()
    for r in rows:
        for d in r["domains"]:
            dom_counter[d] += 1

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "generated_at": generated,
        "db": str(DB.relative_to(ROOT)),
        "n_events": n,
        "overall": overall,
        "by_decade": by_decade,
        "by_class": by_class,
        "domains": dom_counter.most_common(),
        "events": [
            {k: r[k] for k in (
                "event_id", "event_date", "decade", "type", "desc_len", "placeholder",
                "placeholder_marker", "n_source_domains", "source_url_generic_root",
                "sr_slots_total", "sr_slots_external", "sr_slots_corpus", "sr_slots_null",
                "n_entities", "ies90", "source_url_tertiary", "n_citable_domains")}
            for r in rows
        ],
    }

    dec_head = ["decade", "n", "placeholder", "≥2 domains", "encyclopaedia url", "generic-root url",
                "desc median", "desc ≥700", "sr ext %", "sr corpus %", "sr null %",
                "entities median", "IES-90 level", "uncovered"]
    dec_rows = [[d, s["n"], f'{s["placeholder"]} ({s["placeholder_pct"]}%)',
                 f'{s["two_or_more_domains"]} ({s["two_or_more_domains_pct"]}%)',
                 s["tertiary_source_url"], s["generic_root_url"], s["desc_len_median"], s["desc_ge_700"],
                 s["sr_external_pct"], s["sr_corpus_pct"], s["sr_null_pct"],
                 s["entities_median"], s["ies90_level"], s["ies90_uncovered"]]
                for d, s in by_decade.items()]

    cls_head = ["class", "n", "placeholder", "≥2 domains", "desc median",
                "sr ext %", "sr corpus %", "sr null %", "sr majority-null",
                "IES-90 level", "uncovered"]
    cls_rows = [[c, s["n"], f'{s["placeholder"]} ({s["placeholder_pct"]}%)',
                 f'{s["two_or_more_domains"]} ({s["two_or_more_domains_pct"]}%)',
                 s["desc_len_median"], s["sr_external_pct"], s["sr_corpus_pct"],
                 s["sr_null_pct"], s["sr_majority_null"], s["ies90_level"],
                 s["ies90_uncovered"]]
                for c, s in by_class.items()]

    ph = [r for r in rows if r["placeholder"]]
    ph_head = ["event_id", "date", "class", "marker", "desc len", "domains", "entities", "IES-90"]
    ph_rows = [[r["event_id"], r["event_date"], r["type"], r["placeholder_marker"],
                r["desc_len"], r["n_source_domains"], r["n_entities"], r["ies90"]]
               for r in ph]

    dom_rows = [[d, c] for d, c in dom_counter.most_common(20)]

    md = f"""# Spine audit — the honest baseline

*Generated {generated} by `src/spine_audit.py` from `data/oil.db` (read-only).
Session E, step E-1: published before any record is rewritten, so the repair can be
scored against a number rather than an impression. Every figure below is computed;
none is asserted. Re-run the script to regenerate this file.*

## What is measured

Per event: the number of distinct source domains (across `source_url` and every URL in
`sr_json.sources`), the description length, the provenance mix of the `sr_json` field
sources (external URL / corpus-derived / null), whether the description still carries
drafting scaffolding, the entity count, and whether an independent IES-90 level exists.
A "domain" strips a leading `www.`, so `eia.gov` and `www.eia.gov` are one source — the
conservative reading of the two-source rule. A `corpus:` source is self-referential: it
is derived from this corpus and so cannot corroborate it. An **encyclopaedia** domain
(wikipedia and similar) is counted separately and excluded from "citable domains": the
codebook requires "a primary or major-wire source", and an encyclopaedia is a tertiary
summary of sources it does not itself constitute.

## Overall ({n} events)

| measure | value |
|---|---|
| events | {n} |
| carrying drafting scaffolding | {overall['placeholder']} ({overall['placeholder_pct']}%) |
| with ≥ 2 distinct source domains | {overall['two_or_more_domains']} ({overall['two_or_more_domains_pct']}%) |
| with exactly 1 source domain | {overall['one_domain']} |
| with 0 source domains | {overall['zero_domains']} |
| whose `source_url` is a bare site root, not a document | {overall['generic_root_url']} |
| whose `source_url` is an encyclopaedia (wikipedia and similar) | {overall['tertiary_source_url']} |
| citing an encyclopaedia anywhere (incl. `sr_json`) | {overall['any_tertiary_domain']} |
| with **no citable domain at all** once encyclopaedias are set aside | {overall['zero_citable_domains']} |
| description length, median / min / max (chars) | {overall['desc_len_median']} / {overall['desc_len_min']} / {overall['desc_len_max']} |
| descriptions ≥ 700 chars (roughly a 120-word narrative) | {overall['desc_ge_700']} |
| `sr_json` field-source slots | {overall['sr_slots_total']} |
| — external URL | {overall['sr_external_pct']}% |
| — corpus-derived | {overall['sr_corpus_pct']}% |
| — null | {overall['sr_null_pct']}% |
| events whose field sources are majority null | {overall['sr_majority_null']} |
| entities per event, median | {overall['entities_median']} |
| events with 0 entities | {overall['entities_zero']} |
| IES-90 level present | {overall['ies90_level']} |
| flagged `no_independent_outcome` | {overall['ies90_none']} |
| neither (uncovered) | {overall['ies90_uncovered']} |
| `severity` null | {overall['severity_null']} |

## By decade

{md_table(dec_head, dec_rows)}

## By class

{md_table(cls_head, cls_rows)}

## Every event still carrying drafting scaffolding ({len(ph)})

{md_table(ph_head, ph_rows)}

## Source domains, most common first (top 20)

{md_table(["domain", "events citing it"], dom_rows)}

## How to read this

The two-source admission rule in the codebook is a standard for future admissions, not a
property of the present corpus: the `≥2 domains` column is the measurement of that gap.
A bare site root (`https://www.eia.gov`) satisfies "every event MUST be sourced" while
citing nothing a reader can check, so it is counted separately rather than treated as a
source. The `sr corpus %` column matters for the same reason a self-citation does: those
field values were derived from this corpus, so they cannot be evidence about it.

`data/spine/audit.json` carries the same numbers per event for later runs to diff.
"""
    return md, payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--print", dest="do_print", action="store_true",
                    help="also print the summary to stdout")
    args = ap.parse_args()

    if not DB.exists():
        raise SystemExit(f"database not found: {DB}")

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = load_events(conn)
    finally:
        conn.close()

    md, payload = build_report(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Anything below the sentinel is hand-written and survives regeneration. The
    # generated tables above it are always rebuilt from the database, so a dated record
    # of a repair can live in the same file as the live numbers without either one
    # silently overwriting the other.
    out = OUT_DIR / "AUDIT.md"
    appended = ""
    if out.exists():
        prev = out.read_text(encoding="utf-8")
        if APPEND_SENTINEL in prev:
            appended = "\n" + APPEND_SENTINEL + prev.split(APPEND_SENTINEL, 1)[1]
    out.write_text(md + appended, encoding="utf-8")
    (OUT_DIR / "audit.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")

    o = payload["overall"]
    print(f"spine audit: {payload['n_events']} events")
    print(f"  drafting scaffolding : {o['placeholder']} ({o['placeholder_pct']}%)")
    print(f"  >=2 source domains   : {o['two_or_more_domains']} ({o['two_or_more_domains_pct']}%)")
    print(f"  bare site-root urls  : {o['generic_root_url']}")
    print(f"  encyclopaedia urls   : {o['tertiary_source_url']} "
          f"(any encyclopaedia citation: {o['any_tertiary_domain']}; "
          f"no citable domain at all: {o['zero_citable_domains']})")
    print(f"  description median   : {o['desc_len_median']} chars")
    print(f"  sr sources ext/corp/null: {o['sr_external_pct']}% / {o['sr_corpus_pct']}% / {o['sr_null_pct']}%")
    print(f"  IES-90 level/none/uncovered: {o['ies90_level']} / {o['ies90_none']} / {o['ies90_uncovered']}")
    print(f"  wrote {OUT_DIR/'AUDIT.md'} and {OUT_DIR/'audit.json'}")
    if args.do_print:
        print()
        print(md)


if __name__ == "__main__":
    main()
