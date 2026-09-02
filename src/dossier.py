"""dossier.py -- pre-1987 admission dossiers (Brief A-6; rule: data/candidates/DOSSIER_RULE.md, registered first).

One markdown dossier per candidate under data/candidates/dossiers/<id>.md: dates from the primary dataset record,
actors, proposed class / entities under the codebook and entity register, and the two-source rule satisfied from
VERIFIED sources only -- the primary record plus one FRUS document (history.state.gov) whose page date lies inside the
crisis window; every citation is opened by this code and its URL + page date recorded. When no second source is found
the dossier says so and is not admissible. Nothing enters `events` here (that is src/admit.py, with Joe's flag).

Run:  python3 src/dossier.py                # every ICB crisis 1946-1986 with a registered-state actor
      python3 src/dossier.py --limit 5      # first five (smoke)
      python3 src/dossier.py --csv data/candidates/pre1987_candidates.csv   # session B's sheet when it lands (ICB rows)
"""
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "state"))
import countries as C  # noqa: E402
import outcomes as O  # noqa: E402
import panel as P  # noqa: E402

OUT = ROOT / "data" / "candidates" / "dossiers"
CACHE = OUT / "_cache"
INDEX = ROOT / "data" / "candidates" / "dossiers_index.json"
RULE = "data/candidates/DOSSIER_RULE.md (2026-09-02)"
UA = {"User-Agent": "ripple-engine/1.0 (research; pre-1987 dossiers, data/candidates/DOSSIER_RULE.md)"}
FRUS = "https://history.state.gov"
STATE_SET = {2, 20, 70, 100, 101, 130, 140, 160, 52, 200, 385, 365, 360, 615, 620, 475, 481, 540, 651, 630, 645, 670, 690, 692, 694,
             696, 698, 710, 850, 820, 835, 652, 660, 663, 666, 640, 678, 680, 679, 522, 520, 530, 531, 95, 830, 390, 740, 260, 255,
             220, 325, 750, 732}                                  # data/candidates/REGISTRATION.md (session B)
SEV = {1: 2, 2: 3, 3: 4, 4: 5}
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_RE = re.compile(rf"({MONTHS})\s+(\d{{1,2}}),\s+(\d{{4}})")
WINDOW_DAYS = 30
SLEEP = 0.4


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")[:40]


def proposed_class(name):
    n = name.lower()
    if re.search(r"canal|strait|blockade|tanker|shipping", n):
        return "chokepoint_disruption"
    if re.search(r"embargo|sanction|boycott", n):
        return "sanctions"
    return "conflict_escalation"


# ----------------------------------------------------------------------------- the network, cached and recorded

def _get(url, params=None):
    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "_", (url + json.dumps(params or {}, sort_keys=True)).lower())[:150]
    cp = CACHE / f"{key}.json"
    if cp.exists():
        return json.loads(cp.read_text())
    try:
        r = requests.get(url, params=params, headers=UA, timeout=30)
        rec = {"url": r.url, "status": r.status_code, "text": r.text if r.ok else "", "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    except requests.RequestException as e:
        rec = {"url": url, "status": None, "text": "", "error": type(e).__name__, "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    cp.write_text(json.dumps(rec))
    time.sleep(SLEEP)
    return rec


def frus_candidates(query):
    """Document links + titles from the FRUS full-text search (HTML; there is no JSON API -- verified 2026-09-02)."""
    rec = _get(f"{FRUS}/search", {"q": query, "within": "documents"})
    if not rec["text"]:
        return [], rec
    links = re.findall(r'<a[^>]+href="(/historicaldocuments/frus[^"]+/d\d+)"[^>]*>(.*?)</a>', rec["text"], re.S)
    seen, out = set(), []
    for href, title in links:
        if href in seen:
            continue
        seen.add(href)
        out.append({"url": FRUS + href, "title": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title)).strip()[:200]})
    return out, rec


def frus_doc_date(url):
    """The first date printed on a FRUS document page (the document's own dateline), as ISO; None if none."""
    rec = _get(url)
    if not rec["text"]:
        return None, rec
    body = rec["text"]
    m = re.search(r'<div[^>]+class="[^"]*tei-div[^"]*"', body)
    seg = body[m.start():] if m else body
    for mm in DATE_RE.finditer(seg):
        try:
            return datetime.strptime(f"{mm.group(1)} {mm.group(2)} {mm.group(3)}", "%B %d %Y").date().isoformat(), rec
        except ValueError:
            continue
    return None, rec


def second_source(name, trig, term, max_docs=6):
    """A FRUS document dated inside [trig-30d, term+30d], or the record of what was searched and found nothing."""
    lo, hi = (trig - pd.Timedelta(days=WINDOW_DAYS)).date().isoformat(), (term + pd.Timedelta(days=WINDOW_DAYS)).date().isoformat()
    query = f"{re.sub(r'[^A-Za-z ]+', ' ', name).title().strip()} {trig.year}"
    cands, srec = frus_candidates(query)
    opened = []
    for c in cands[:max_docs]:
        d, drec = frus_doc_date(c["url"])
        opened.append({"url": c["url"], "title": c["title"], "page_date": d, "retrieved_at": drec.get("retrieved_at")})
        if d and lo <= d <= hi:
            return {"found": True, "route": "FRUS", "url": c["url"], "title": c["title"], "date": d, "window": [lo, hi],
                    "query": query, "search_url": srec.get("url"), "retrieved_at": drec.get("retrieved_at"), "opened": opened}
    return {"found": False, "route": "FRUS", "query": query, "search_url": srec.get("url"), "search_status": srec.get("status"),
            "window": [lo, hi], "opened": opened, "retrieved_at": srec.get("retrieved_at")}


# ----------------------------------------------------------------------------- candidates and dossiers

def icb_candidates(limit=None):
    sysd, members = O.load_icb()
    act = pd.read_csv(P.raw_path("icb", "icb2v16.csv"), encoding="latin-1")
    act.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in act.columns]
    codes = act.groupby("crisno")["cracid"].apply(lambda s: sorted(set(int(x) for x in s))).to_dict()
    sel = sysd[(sysd.trigdate >= "1946-01-01") & (sysd.trigdate <= "1986-12-31")].sort_values("trigdate")
    out = []
    for c in sel.itertuples(index=False):
        cc = codes.get(int(c.crisno), [])
        if not (set(cc) & STATE_SET):
            continue
        out.append({"crisno": int(c.crisno), "name": c.crisname, "trigdate": c.trigdate, "termdate": c.termdate, "trigent": getattr(c, "trigent", None),
                    "viol": int(c.viol) if pd.notna(c.viol) else None, "forout": int(c.forout) if pd.notna(c.forout) else None,
                    "datrig_missing": bool(pd.isna(getattr(c, "datrig", None))), "ccodes": cc})
    return out[:limit] if limit else out


def build_one(cand):
    did = f"icb_{cand['crisno']}_{slug(cand['name'])}"
    actors = []
    for cc in cand["ccodes"]:
        e = C.from_ccode(cc)
        actors.append({"ccode": cc, "entity": e, "registered": cc in STATE_SET})
    trig_e = C.from_ccode(cand["trigent"]) if cand.get("trigent") not in (None, "") and not pd.isna(cand.get("trigent")) else None
    roles = []
    for a in actors:
        if not a["entity"]:
            continue
        roles.append((a["entity"], "actor" if trig_e and a["entity"] == trig_e else ("target" if trig_e else "unknown")))
    ss = second_source(cand["name"], cand["trigdate"], cand["termdate"])
    cls = proposed_class(cand["name"])
    admissible = bool(ss["found"])
    front = {"id": did, "built_by": "session A", "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "rule": RULE,
             "primary": {"dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)", "crisno": cand["crisno"],
                         "url": f"https://www.icb.umd.edu/dataviewer/?crisno={cand['crisno']}", "trigdate": cand["trigdate"].date().isoformat(),
                         "termdate": cand["termdate"].date().isoformat(), "viol": cand["viol"], "forout": cand["forout"]},
             "event_date": cand["trigdate"].date().isoformat(), "date_precision": "month" if cand["datrig_missing"] else "day",
             "proposed_class": cls, "proposed_severity": SEV.get(cand["viol"] or 0, 2), "proposed_surprise": 3, "proposed_confidence": "medium",
             "entities": [{"entity": e, "role": r} for e, r in roles],
             "unmapped_ccodes": [a["ccode"] for a in actors if not a["entity"]],
             "second_source": ss, "admissible": admissible, "approved_by": None, "approved_at": None}
    L = [f"# Dossier {did} — {cand['name']}", "", "```json", json.dumps(front, indent=1, default=str), "```", "",
         "## Primary record (source 1)",
         f"ICB crisis {cand['crisno']} **{cand['name']}**: trigdate {front['primary']['trigdate']}, termdate {front['primary']['termdate']}, "
         f"viol {cand['viol']}, forout {cand['forout']}. Page: {front['primary']['url']}", "",
         "## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)",
         *[f"- {a['ccode']}: {a['entity'] or 'UNMAPPED'}{' (registered state set)' if a['registered'] else ''}" for a in actors], "",
         "## Proposed coding (provisional, rule §2 — Joe decides)",
         f"- class: `{cls}`; severity {front['proposed_severity']} (from viol {cand['viol']}); surprise 3 (provisional); confidence medium",
         f"- entities: " + (", ".join(f"{e}:{r}" for e, r in roles) or "none mapped"), "",
         "## Second source (rule §3)"]
    if ss["found"]:
        L += [f"- FRUS document opened {ss['retrieved_at']}: **{ss['title']}** — page date {ss['date']} (window {ss['window'][0]}..{ss['window'][1]})",
              f"  {ss['url']}", f"- search: {ss['search_url']}"]
    else:
        L += [f"- **second source: none found — not admissible.** FRUS search `{ss['query']}` ({ss['search_url']}, HTTP {ss['search_status']}) "
              f"returned {len(ss['opened'])} document(s) opened, none dated inside {ss['window'][0]}..{ss['window'][1]}.",
              "- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3)."]
        if ss["opened"]:
            L += ["- opened: " + "; ".join(f"{o['title'][:60]} ({o['page_date'] or 'no date'})" for o in ss["opened"][:6])]
    L += ["", f"## Admissible: **{'yes' if admissible else 'no'}**", "", "Joe: to admit, write the approval line and run",
          f"`python3 src/admit.py --dossier {did} --approved-by joe`. The code never runs it."]
    (OUT / f"{did}.md").write_text("\n".join(L) + "\n")
    return front


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    OUT.mkdir(parents=True, exist_ok=True)
    cands = icb_candidates(limit)
    fronts = []
    for i, c in enumerate(cands, 1):
        f = build_one(c)
        fronts.append(f)
        print(f"  [{i}/{len(cands)}] {f['id']:<45} {f['event_date']} {f['proposed_class']:<22} second source: {'FRUS ' + f['second_source']['date'] if f['admissible'] else 'none'}")
    dec = {}
    for f in fronts:
        d = f["event_date"][:3] + "0s"
        dec.setdefault(d, {"dossiers": 0, "admissible": 0})
        dec[d]["dossiers"] += 1; dec[d]["admissible"] += int(f["admissible"])
    idx = {"rule": RULE, "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "n": len(fronts),
           "admissible": sum(f["admissible"] for f in fronts), "by_decade": dict(sorted(dec.items())),
           "dossiers": [{k: f[k] for k in ("id", "event_date", "proposed_class", "admissible")} | {"second_source_date": f["second_source"].get("date")} for f in fronts]}
    INDEX.write_text(json.dumps(idx, indent=1))
    print(f"{len(fronts)} dossiers, {idx['admissible']} admissible; by decade {idx['by_decade']} -> {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
