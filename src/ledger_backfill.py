"""ledger_backfill.py -- session H: make the claim loop actually fire (CLAIM_LEDGER_REGISTRATION.md Amendment 7).

The Ledger's core mechanic is §4: a claim is logged at its knowable date and, at its horizon, resolves
ITSELF FROM DATA. It had never fired. Every one of the 14 claims in the ledger carried
knowable = 2026-09-02, so no horizon had passed and resolutions.jsonl was empty (0 bytes).

This module reads real historical stories whose horizons closed years ago, logs their claims at the
stories' TRUE publication dates, and lets ledger.resolve() settle them from the Brent series. Nothing
is backdated by fiat: a story with no extractable publication date is dropped, not stamped.

Everything here is fixed in Amendment 7 BEFORE it was run:
  * selection is mechanical -- every corpus event 2019-01-01..2020-12-31 in the four geopolitical
    classes carrying an http(s) source_url (n = 19). Stories are not picked one by one.
  * the page is fetched once, archived under data/ledger/backfill_pages/, and parsed by reader's own
    deterministic parsers. A fetch failure drops the story and is reported in the denominator.
  * the knowable date is EXTRACTED from the page (five methods, in order); no date -> dropped.
  * the reader gets NO class hint -- a live URL read has no corpus id and must classify for itself.
  * verdicts are point-in-time: verdict_for(..., as_of=knowable), so the reference class holds only
    events dated strictly before the story was published.
  * resolution is ledger.resolve() as written. Nothing hand-resolved, no row edited.

Run:  python3 src/ledger_backfill.py            # fetch (cached), read, log, resolve, print the board
      python3 src/ledger_backfill.py --dry-run  # everything except log_claims/resolve
      python3 src/ledger_backfill.py --refetch  # re-fetch the pages instead of using the archive
"""
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
LEDGER_DIR = DATA / "ledger"
PAGES = LEDGER_DIR / "backfill_pages"
MANIFEST = LEDGER_DIR / "backfill_manifest.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger as L                                  # noqa: E402
import reader as R                                  # noqa: E402
import story_read as SR                             # noqa: E402  read-only: branches() is session A's, reused not copied

REGISTRATION = "CLAIM_LEDGER_REGISTRATION.md Amendment 7"
BRENT = "fred.DCOILBRENTEU"
# Amendment 7 rule 1 -- the selection rule, not a list of stories.
WINDOW = ("2019-01-01", "2020-12-31")
CLASSES = ("infrastructure_attack", "chokepoint_disruption", "opec_decision", "conflict_escalation")
SELECT_SQL = (f"SELECT event_id, event_date, type, title, source_url FROM events "
              f"WHERE event_date BETWEEN ? AND ? AND type IN ({','.join('?' * len(CLASSES))}) "
              f"AND source_url LIKE 'http%' ORDER BY event_date")

# Amendment 7 rule 3 -- the knowable date is extracted, in this order, or the story is dropped.
_META = [r'property=["\']article:published_time["\'][^>]*content=["\']([^"\']+)',
         r'content=["\']([^"\']+)["\'][^>]*property=["\']article:published_time["\']',
         r'name=["\']datePublished["\'][^>]*content=["\']([^"\']+)',
         r'"datePublished"\s*:\s*"([^"]+)"']
_TIME_EL = r'<time[^>]*datetime=["\']((?:19|20)\d{2}-\d{2}-\d{2})'
_DATELINE = r'class=["\'](?:date|published|pubdate)["\'][^>]*>\s*([A-Z][a-z]+\s+\d{1,2},\s+(?:19|20)\d{2})'
_BODY_PUB = r'Published On\s+(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+((?:19|20)\d{2})'
_URL_PATH = r'/((?:19|20)\d{2})/(\d{1,2})/(\d{1,2})/'
_ISO = re.compile(r'^((?:19|20)\d{2})-(\d{2})-(\d{2})')
_MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def knowable_from(raw, url, body):
    """(iso date, basis) or (None, None). Pure: the page's own stated publication date, never today,
    never the corpus event_date. Unit-tested (REQ-H1-DATE)."""
    for pat in _META:
        m = re.search(pat, raw or "", re.I)
        if m:
            iso = _ISO.match(m.group(1).strip())
            if iso:
                return f"{iso.group(1)}-{iso.group(2)}-{iso.group(3)}", "meta"
    m = re.search(_TIME_EL, raw or "", re.I)
    if m:
        return m.group(1), "time_element"
    m = re.search(_DATELINE, raw or "", re.I)
    if m:
        try:
            return datetime.strptime(m.group(1).strip(), "%B %d, %Y").strftime("%Y-%m-%d"), "dateline"
        except ValueError:
            pass
    m = re.search(_URL_PATH, url or "")
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", "url_path"
    m = re.search(_BODY_PUB, body or "", re.I)
    if m and m.group(2).lower() in _MONTHS:
        return f"{int(m.group(3)):04d}-{_MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}", "body"
    return None, None


def page(event_id, url, refetch=False):
    """(raw html, error). Fetched once and archived, so a read can be audited against the exact bytes."""
    PAGES.mkdir(parents=True, exist_ok=True)
    p = PAGES / f"{event_id}.html"
    if p.exists() and not refetch:
        return p.read_text(encoding="utf-8", errors="replace"), None
    try:
        raw = R.fetch(url, timeout=25)
    except Exception as e:                                    # noqa: BLE001 -- the failure is reported, not hidden
        return None, f"fetch failed: {e}"
    p.write_text(raw, encoding="utf-8", errors="replace")
    return raw, None


def price_at(conn, knowable):
    """Brent at the first trading day on/after the knowable date -- the same index rule ledger.resolve
    uses, so the logged price and the resolved path start on the same bar (Amendment 7 rule 5)."""
    s = L._price(conn, BRENT)
    pos = s.index.searchsorted(pd.Timestamp(knowable))
    if pos >= len(s):
        return None, None
    return round(float(s.iloc[pos]), 2), str(s.index[pos].date())


def read_one(conn, ev, refetch=False):
    """One story, end to end up to (not including) the ledger write. Returns the manifest row."""
    eid, edate, etype, title, url = ev
    row = {"event_id": eid, "corpus_event_date": edate, "corpus_class": etype, "corpus_title": title, "url": url}
    raw, err = page(eid, url, refetch)
    if err:
        return {**row, "status": "DROPPED", "drop_reason": err}
    body = R.body_from_html(raw)
    if len(body) < 120:
        return {**row, "status": "DROPPED", "drop_reason": f"parsed body is {len(body)} chars (<120): not an article"}
    knowable, basis = knowable_from(raw, url, body)
    if not knowable:
        return {**row, "status": "DROPPED", "drop_reason": "no extractable publication date (Amendment 7 rule 3); never backdated"}
    p0, p0_date = price_at(conn, knowable)
    if p0 is None:
        return {**row, "status": "DROPPED", "drop_reason": f"no Brent print on/after {knowable}"}

    # Amendment 7 rule 4: no class hint. The reader classifies as it would on a live URL read.
    rr = R.read_story(body, conn=conn)
    etype_read = rr["event_class"]
    ents = [e["id"] for e in rr["entities"]]
    br = SR.branches(conn, etype_read, entities=ents, as_of=knowable) if etype_read else {"applicable": False}

    claims = []
    for t in rr["claims"]:
        t["event_class"] = t.get("event_class") or etype_read
        # Amendment 7 rule 6: point-in-time. The live Story page passes as_of=None on a URL read (defect S-1).
        t["verdict"] = L.verdict_for(conn, t, price_at_knowable=p0, as_of=knowable,
                                     escalation_read=br if br.get("applicable") else None)
        claims.append(t)
    return {**row, "status": "READ", "knowable": knowable, "knowable_basis": basis,
            "days_after_event": (pd.Timestamp(knowable) - pd.Timestamp(edate)).days,
            "page_title": R.title_from_html(raw, url, body), "body_chars": len(body),
            "archive": str((PAGES / f"{eid}.html").relative_to(ROOT)),
            "price_at_knowable": p0, "price_bar": p0_date,
            "reader": rr["reader"], "reader_class": etype_read, "class_agrees_with_corpus": etype_read == etype,
            "entities": ents, "n_claims": len(claims), "n_checkable": sum(1 for c in claims if c.get("checkable")),
            "n_rejected": len(rr["rejected"]), "rejected": rr["rejected"], "claims": claims}


def run(dry_run=False, refetch=False, echo=print):
    conn = sqlite3.connect(DB)
    try:
        evs = list(conn.execute(SELECT_SQL, [WINDOW[0], WINDOW[1], *CLASSES]))
        echo(f"Amendment 7 selection: {len(evs)} corpus events {WINDOW[0]}..{WINDOW[1]} in {CLASSES}")
        rows = []
        for i, ev in enumerate(evs, 1):
            r = read_one(conn, ev, refetch)
            rows.append(r)
            if r["status"] == "DROPPED":
                echo(f"  [{i:2d}/{len(evs)}] DROP {r['event_id']:34s} {r['drop_reason'][:80]}")
            else:
                echo(f"  [{i:2d}/{len(evs)}] READ {r['event_id']:34s} knowable={r['knowable']} ({r['knowable_basis']}, "
                     f"+{r['days_after_event']}d) class={r['reader_class']} claims={r['n_claims']} "
                     f"checkable={r['n_checkable']} mode={r['reader'].get('mode')}")
        read = [r for r in rows if r["status"] == "READ"]
        ids = []
        if not dry_run:
            for r in read:
                r["ledger_ids"] = L.log_claims(f"hist:{r['event_id']}", _domain(r["url"]), r["knowable"],
                                               r["claims"], price_at_knowable=r["price_at_knowable"], url=r["url"])
                ids += r["ledger_ids"]
            n_new = L.resolve(conn)
            echo(f"\nledger.resolve(): {n_new} newly resolved")
        man = {"registration": REGISTRATION, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "window": WINDOW, "classes": list(CLASSES), "selected": len(evs),
               "read": len(read), "dropped": len(rows) - len(read),
               "drops": [{k: r[k] for k in ("event_id", "url", "drop_reason")} for r in rows if r["status"] == "DROPPED"],
               "claims_logged": len(ids), "dry_run": dry_run,
               "class_agreement": {"n": len(read), "agree": sum(1 for r in read if r["class_agrees_with_corpus"]),
                                   "note": "reader vs corpus class; a DIAGNOSTIC, gates nothing (Amendment 7 rule 4)"},
               "stories": [{k: v for k, v in r.items() if k != "claims"} for r in rows],
               "claims": [{"event_id": r["event_id"], "knowable": r["knowable"], **c} for r in read for c in r["claims"]]}
        MANIFEST.write_text(json.dumps(man, indent=1, default=str))
        echo(f"manifest -> {MANIFEST.relative_to(ROOT)}")
        return man
    finally:
        conn.close()


# ----------------------------------------------------------------------------- the first real scoreboard

def board(echo=print):
    """The scoreboard for the resolved claims, reported at BOTH levels (Amendment 7 rule 7).

    Claim level is what the ledger stores; STORY level is what is statistically honest. Every price
    claim inside one story resolves against the SAME realized Brent path, so 7 flow claims in the
    Druzhba story are seven copies of one observation, not seven tests. The claim-level n is
    reported because it is what §4 defines, and it is labelled non-independent wherever it appears.
    """
    import math
    from collections import defaultdict
    claims = {c["claim_id"]: c for c in L._rows(L.CLAIMS)}
    res = L._rows(L.RESOLUTIONS)
    hist = [c for c in claims.values() if c["story_id"].startswith("hist:")]
    done = {r["claim_id"] for r in res}
    called = [r for r in res if r.get("record_true") is not None]

    per_story = defaultdict(list)
    for r in called:
        per_story[claims[r["claim_id"]]["story_id"]].append(r)
    votes = {}
    for s, rs in per_story.items():
        rr = sum(1 for r in rs if r["record_true"])
        nn = sum(1 for r in rs if r["claim_true"])
        votes[s] = {"claims": len(rs), "record_right": rr, "narrative_right": nn,
                    "winner": "record" if rr > nn else ("narrative" if nn > rr else "tie")}
    rw = sum(1 for v in votes.values() if v["winner"] == "record")
    nw = sum(1 for v in votes.values() if v["winner"] == "narrative")
    n_dec = rw + nw
    p = None
    if n_dec:
        obs = math.comb(n_dec, rw)
        p = sum(math.comb(n_dec, i) for i in range(n_dec + 1) if math.comb(n_dec, i) <= obs) * 0.5 ** n_dec
    need = None
    for kk in range(n_dec, -1, -1):
        if 2 * sum(math.comb(n_dec, i) for i in range(kk, n_dec + 1)) * 0.5 ** n_dec > 0.05:
            need = kk + 1
            break

    # every price claim in a story shares one realized path -> distinct outcome cells, not claim count
    cells = len({(claims[r["claim_id"]]["story_id"], r["kind"], r["claim_true"]) for r in res})
    by_kind = {}
    for k in sorted({r["kind"] for r in res}):
        rs = [r for r in res if r["kind"] == k]
        by_kind[k] = {"n_claims": len(rs), "n_stories": len({claims[r["claim_id"]]["story_id"] for r in rs}),
                      "claim_true": sum(1 for r in rs if r["claim_true"]),
                      "true_rate": round(sum(1 for r in rs if r["claim_true"]) / len(rs), 3)}
    unresolved = [c for c in hist if c.get("checkable") and c["claim_id"] not in done]
    b = {
        "registration": REGISTRATION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "receipts": {"claims": "data/ledger/claims.jsonl", "resolutions": "data/ledger/resolutions.jsonl",
                     "manifest": "data/ledger/backfill_manifest.json", "pages": "data/ledger/backfill_pages/"},
        "counts": {"backfill_claims": len(hist), "checkable": sum(1 for c in hist if c.get("checkable")),
                   "resolved": len(res), "unresolved_checkable": len(unresolved),
                   "stories_read": len({c["story_id"] for c in hist}),
                   "stories_with_a_resolution": len({claims[r["claim_id"]]["story_id"] for r in res})},
        "unresolved_reason": {"all_hypothetical": all(c.get("modality") == "hypothetical" for c in unresolved),
                              "by_kind_modality": {f"{c['kind']}/{c['modality']}": 0 for c in unresolved},
                              "note": "ledger.resolve() skips modality=hypothetical outright; §2 says such a claim "
                                      "resolves if its antecedent enters the corpus, and no such mechanism exists "
                                      "(defect L-2)"},
        "claim_level": {"n": len(called), "record_right": sum(1 for r in called if r["record_true"]),
                        "narrative_right": sum(1 for r in called if r["claim_true"]),
                        "record_only_right": sum(1 for r in called if r["record_true"] and not r["claim_true"]),
                        "narrative_only_right": sum(1 for r in called if r["claim_true"] and not r["record_true"]),
                        "INDEPENDENCE": "NOT independent: every price claim in a story resolves against the same "
                                        "realized Brent path. Do not read this n as a sample size."},
        "story_level": {"stories_with_a_call": len(votes), "record_wins": rw, "narrative_wins": nw,
                        "decisive": n_dec, "binomial_p_two_sided": round(p, 3) if p is not None else None,
                        "needed_for_p_lt_0.05": need, "votes": votes,
                        "verdict": "NO CALL: the loop resolves, the board does not yet separate the record from the "
                                   "narrative at any conventional level."},
        "distinct_outcome_cells": cells,
        "by_kind": by_kind,
    }
    for c in unresolved:
        b["unresolved_reason"]["by_kind_modality"][f"{c['kind']}/{c['modality']}"] += 1
    (LEDGER_DIR / "scoreboard_h.json").write_text(json.dumps(b, indent=1))
    echo(f"resolved {b['counts']['resolved']} claims from {b['counts']['stories_with_a_resolution']} stories "
         f"({b['distinct_outcome_cells']} distinct outcome cells)")
    echo(f"  claim level : record {b['claim_level']['record_right']}/{b['claim_level']['n']} vs "
         f"narrative {b['claim_level']['narrative_right']}/{b['claim_level']['n']}  <- NOT independent")
    echo(f"  story level : record {rw} vs narrative {nw} of {n_dec} decisive, two-sided p={b['story_level']['binomial_p_two_sided']} "
         f"(need >={need} of {n_dec} for p<0.05)")
    echo(f"  -> {b['story_level']['verdict']}")
    return b


def _domain(url):
    from urllib.parse import urlparse
    return (urlparse(url or "").netloc or "").replace("www.", "") or "unknown"


if __name__ == "__main__":
    if "--board" in sys.argv:
        board()
    else:
        run(dry_run="--dry-run" in sys.argv, refetch="--refetch" in sys.argv)
        board()
