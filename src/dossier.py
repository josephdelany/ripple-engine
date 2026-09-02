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
STOPWORDS = {"spike", "government", "vs", "dispute", "crisis", "war", "conflict"}     # §5.2: generic words name nobody
SLEEP = 0.4
# Per-host minimum spacing between live requests. GDELT DOC 2.0 states its own limit ("Please limit requests to one
# every 5 seconds", HTTP 429) and DOSSIER_RULE.md §5(b) registers it; a shorter gap gets the request refused or timed
# out, which would read as "no second source" when the truth is "we asked too fast". (2026-09-02)
HOST_SPACING_S = {"api.gdeltproject.org": 10.0}     # §5.1(3): 5 s was still refused in practice on 2026-09-02
RETRY_AFTER_429_S = 60.0
_LAST_CALL = {}


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

def _get(url, params=None, _retry=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "_", (url + json.dumps(params or {}, sort_keys=True)).lower())[:150]
    cp = CACHE / f"{key}.json"
    if cp.exists():
        return json.loads(cp.read_text())
    host = url.split("/")[2]
    gap = HOST_SPACING_S.get(host)
    if gap:
        wait = gap - (time.monotonic() - _LAST_CALL.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
    try:
        r = requests.get(url, params=params, headers=UA, timeout=60)
        rec = {"url": r.url, "status": r.status_code, "text": r.text if r.ok else "", "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    except requests.RequestException as e:
        rec = {"url": url, "status": None, "text": "", "error": type(e).__name__, "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    _LAST_CALL[host] = time.monotonic()
    if rec["status"] == 429 and not _retry:           # §5.1(3): one retry after a minute, then give up and say UNDETERMINED
        time.sleep(RETRY_AFTER_429_S)
        return _get(url, params, _retry=True)
    if rec["status"] is None or rec["status"] >= 400:
        return rec                                    # a refused/failed request is NOT cached: "we asked too fast" must never read as "no source"
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


GDELT_DOC = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_FROM = "2017-01-01"


def gdelt_second_source(name, parties, d):
    """DOSSIER_RULE §5(b): a GDELT DOC 2.0 article whose seendate lies in [d-3d, d+30d] and whose title names the crisis or
    a party. One request (the caller spaces requests 5 s apart via _get's sleep). Coverage begins 2017-01-01."""
    lo, hi = (d - pd.Timedelta(days=3)), (d + pd.Timedelta(days=30))
    terms = query_terms(name, parties)
    query = " ".join(dict.fromkeys(terms)) or name
    params = {"query": query, "mode": "artlist", "format": "json", "maxrecords": 25,
              "startdatetime": lo.strftime("%Y%m%d000000"), "enddatetime": hi.strftime("%Y%m%d235959")}
    rec = _get(GDELT_DOC, params)
    opened = []
    try:
        arts = json.loads(rec["text"]).get("articles", []) if rec["text"].strip().startswith("{") else []
    except ValueError:
        arts = []
    keys = [t.lower() for t in terms]
    for a in arts:
        title, url, seen = (a.get("title") or ""), (a.get("url") or ""), (a.get("seendate") or "")
        sd = f"{seen[:4]}-{seen[4:6]}-{seen[6:8]}" if len(seen) >= 8 else None
        opened.append({"url": url, "title": title[:160], "page_date": sd, "domain": a.get("domain")})
        if sd and lo.date().isoformat() <= sd <= hi.date().isoformat() and any(k in title.lower() for k in keys):
            return {"found": True, "status": "found", "route": "GDELT DOC 2.0", "url": url, "title": title[:200], "date": sd, "domain": a.get("domain"),
                    "window": [lo.date().isoformat(), hi.date().isoformat()], "query": query, "search_url": rec.get("url"),
                    "retrieved_at": rec.get("retrieved_at"), "opened": opened}
    st = rec.get("status")
    status = "none_found" if st == 200 else "undetermined"
    return {"found": False, "status": status, "route": "GDELT DOC 2.0", "query": query, "search_url": rec.get("url"), "search_status": st,
            "window": [lo.date().isoformat(), hi.date().isoformat()], "opened": opened, "retrieved_at": rec.get("retrieved_at"),
            "note": rec.get("error") or (rec["text"][:120] if rec["text"] and not rec["text"].strip().startswith("{") else "")}


def query_terms(name, parties):
    """§5.2: the terms a search may use -- the record's own content words plus any named registered state."""
    return [t for t in re.split(r"[^A-Za-z]+", name) if len(t) >= 4 and t.lower() not in STOPWORDS][:3] + [p for p in parties if p][:2]


def searchable(name, parties):
    """§5.2: a search runs only if the query can name a registered state, or carries >= 2 content terms of the record."""
    if parties:
        return True
    return len(query_terms(name, [])) >= 2


def route_second_source(name, parties, trig, term):
    """§3 for the FRUS era, §5(b) GDELT DOC from 2017; both tried where both could answer; the record says which."""
    if not searchable(name, parties):
        return {"found": False, "status": "none_found", "route": "none", "opened": [], "window": None,
                "note": ("a GPR spike names no party; no query can name a state, so no second source can be sought (§5.2)"
                         if name.lower().startswith("gpr") else
                         f"no query can be formed from '{name}' that names a registered state or carries two content terms (§5.2)")}
    tried = []
    if trig.year <= 2000:
        ss = second_source(name, trig, term if pd.notna(term) else trig)
        if ss["found"]:
            return ss
        tried.append(ss)
    if trig.date().isoformat() >= GDELT_FROM:
        ss = gdelt_second_source(name, parties, trig)
        if ss["found"]:
            return ss
        tried.append(ss)
    if not tried:
        return {"found": False, "status": "none_found", "route": "none", "note": f"no verified route for {trig.year}: FRUS volumes end in the early 1990s, GDELT DOC begins {GDELT_FROM} (DOSSIER_RULE.md §5)", "opened": [], "window": None}
    out = dict(tried[-1]); out["also_tried"] = [t["route"] for t in tried[:-1]]
    return out


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
            return {"found": True, "status": "found", "route": "FRUS", "url": c["url"], "title": c["title"], "date": d, "window": [lo, hi],
                    "query": query, "search_url": srec.get("url"), "retrieved_at": drec.get("retrieved_at"), "opened": opened}
    return {"found": False, "status": ("none_found" if srec.get("status") == 200 else "undetermined"), "route": "FRUS", "query": query,
            "search_url": srec.get("url"), "search_status": srec.get("status"), "window": [lo, hi], "opened": opened, "retrieved_at": srec.get("retrieved_at")}


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
    """A dossier from a candidate dict. ICB candidates carry crisno/viol/forout; post-1987 rows (§5) carry source/source_id."""
    src = cand.get("source", "icb")
    if src == "icb":
        cand.setdefault("crisno", int(cand.get("source_id")))
        did = f"icb_{cand['crisno']}_{slug(cand['name'])}"
    else:
        did = f"{src}_{cand['source_id']}_{slug(cand['name'])}" if src != "gpr" else f"gpr_{cand['source_id']}"
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
    parties = [C.ALL[a["entity"]][3].split(" (")[0] for a in actors if a["entity"] and a["entity"] in C.ALL][:2]
    ss = route_second_source(cand["name"], parties, cand["trigdate"], cand.get("termdate", pd.NaT)) if src != "icb" or cand["trigdate"].year >= 1987 \
        else second_source(cand["name"], cand["trigdate"], cand["termdate"])
    cls = proposed_class(cand["name"])
    admissible = bool(ss["found"])
    prim_url = {"icb": f"https://www.icb.umd.edu/dataviewer/?crisno={cand.get('crisno', cand.get('source_id'))}",
                "mid": "https://correlatesofwar.org/data-sets/mids/", "ucdp": "https://ucdp.uu.se/downloads/",
                "gpr": "https://www.matteoiacoviello.com/gpr.htm"}[src]
    prim_ds = {"icb": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)", "mid": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
               "ucdp": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)", "gpr": "Caldara-Iacoviello GPR daily (gpr.GPRD in observations)"}[src]
    term = cand.get("termdate")
    front = {"id": did, "built_by": "session A", "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "rule": RULE,
             "primary": {"dataset": prim_ds, "crisno": cand.get("crisno"), "source": src, "source_id": str(cand.get("source_id", cand.get("crisno"))),
                         "detail": cand.get("source_detail"), "url": prim_url, "trigdate": cand["trigdate"].date().isoformat(),
                         "termdate": term.date().isoformat() if term is not None and pd.notna(term) else None, "viol": cand.get("viol"), "forout": cand.get("forout")},
             "event_date": cand["trigdate"].date().isoformat(), "date_precision": "month" if cand["datrig_missing"] else "day",
             "proposed_class": cls, "proposed_severity": SEV.get(cand["viol"] or 0, 2), "proposed_surprise": 3, "proposed_confidence": "medium",
             "entities": [{"entity": e, "role": r} for e, r in roles],
             "unmapped_ccodes": [a["ccode"] for a in actors if not a["entity"]],
             "second_source": ss, "admissible": admissible, "approved_by": None, "approved_at": None}
    L = [f"# Dossier {did} — {cand['name']}", "", "```json", json.dumps(front, indent=1, default=str), "```", "",
         "## Primary record (source 1)",
         f"{prim_ds} record {front['primary']['source_id']} **{cand['name']}**: {cand.get('source_detail') or ''} trigdate {front['primary']['trigdate']}, termdate {front['primary']['termdate']}, "
         f"viol {cand.get('viol')}, forout {cand.get('forout')}. Page: {front['primary']['url']}", "",
         "## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)",
         *[f"- {a['ccode']}: {a['entity'] or 'UNMAPPED'}{' (registered state set)' if a['registered'] else ''}" for a in actors], "",
         "## Proposed coding (provisional, rule §2 — Joe decides)",
         f"- class: `{cls}`; severity {front['proposed_severity']} (from viol {cand['viol']}); surprise 3 (provisional); confidence medium",
         f"- entities: " + (", ".join(f"{e}:{r}" for e, r in roles) or "none mapped"), "",
         "## Second source (rule §3)"]
    if ss["found"]:
        L += [f"- {ss['route']} document opened {ss['retrieved_at']}: **{ss['title']}** — page date {ss['date']} (window {ss['window'][0]}..{ss['window'][1]})",
              f"  {ss['url']}", f"- search: {ss['search_url']}"]
    elif ss.get("status") == "undetermined":
        L += [f"- **second source: UNDETERMINED — the source refused or failed, not an absence.** {ss.get('route')} returned HTTP {ss.get('search_status')} "
              f"for `{ss.get('query', '')}` ({ss.get('search_url')}). This dossier is NOT admissible and is NOT evidence that no second source exists; "
              f"re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). {ss.get('note') or ''}",]
    else:
        L += [f"- **second source: none found — not admissible.** {ss.get('route')} search `{ss.get('query', '')}` ({ss.get('search_url')}, HTTP {ss.get('search_status')}) "
              f"returned {len(ss.get('opened') or [])} document(s) opened, none dated inside {ss['window'][0] if ss.get('window') else '?'}..{ss['window'][1] if ss.get('window') else '?'}. {ss.get('note') or ''}",
              "- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3)."]
        if ss["opened"]:
            L += ["- opened: " + "; ".join(f"{o['title'][:60]} ({o['page_date'] or 'no date'})" for o in ss["opened"][:6])]
    L += ["", f"## Admissible: **{'yes' if admissible else 'no'}**", "", "Joe: to admit, write the approval line and run",
          f"`python3 src/admit.py --dossier {did} --approved-by joe`. The code never runs it."]
    (OUT / f"{did}.md").write_text("\n".join(L) + "\n")
    return front


def csv_candidates(path, limit=None):
    """Session B's / A-12's candidate sheet -> candidate dicts (DOSSIER_RULE §5 columns)."""
    import csv as _csv
    rows = list(_csv.DictReader(open(path, encoding="utf-8")))
    out = []
    for r in rows:
        cc = [int(x) for x in (r.get("actors") or "").split(";") if x.strip().isdigit()]
        det = r.get("source_detail", "")
        if r["source"] == "icb":
            name = re.split(r"\s+\d{4}-\d{2}-\d{2}", det)[0].strip()                       # "NAME 1987-01-05..": the crisis name
        elif r["source"] == "mid":
            m = re.search(r"dispute \d+ (\S+)", det); name = (m.group(1).replace("-", " ") + " dispute") if m else det[:40]
        elif r["source"] == "ucdp":
            m = re.search(r"dyad \d+ (.+?) \(", det); name = m.group(1) if m else det[:40]
        else:
            name = f"GPR spike {r['event_date']}"
        name = (r.get("suggested_title") or "").strip() or name
        out.append({"source": r["source"], "source_id": r["source_id"], "source_detail": r.get("source_detail", ""), "name": name or f"{r['source']} {r['source_id']}",
                    "trigdate": pd.Timestamp(r["event_date"]), "termdate": pd.NaT, "trigent": None, "viol": None, "forout": None, "datrig_missing": False, "ccodes": cc})
    return out[:limit] if limit else out


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    OUT.mkdir(parents=True, exist_ok=True)
    global INDEX
    if "--csv" in sys.argv:
        cands = csv_candidates(sys.argv[sys.argv.index("--csv") + 1], limit)
        INDEX = ROOT / "data" / "candidates" / "dossiers_index_post1987.json"
    else:
        cands = icb_candidates(limit)
    fronts = []
    for i, c in enumerate(cands, 1):
        f = build_one(c)
        fronts.append(f)
        ss = f["second_source"]
        print(f"  [{i}/{len(cands)}] {f['id']:<45} {f['event_date']} {f['proposed_class']:<22} second source: "
              f"{ss['route'] + ' ' + str(ss.get('date')) if f['admissible'] else (ss.get('status') or 'none_found')}", flush=True)
    dec = {}
    for f in fronts:
        d = f["event_date"][:3] + "0s"
        dec.setdefault(d, {"dossiers": 0, "admissible": 0})
        dec[d]["dossiers"] += 1; dec[d]["admissible"] += int(f["admissible"])
    from collections import Counter as _C
    states = _C((f["second_source"].get("status") or ("found" if f["admissible"] else "none_found")) for f in fronts)
    idx = {"rule": RULE, "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "n": len(fronts),
           "admissible": sum(f["admissible"] for f in fronts), "second_source_states": dict(states),
           "by_decade": dict(sorted(dec.items())),
           "dossiers": [{k: f[k] for k in ("id", "event_date", "proposed_class", "admissible")} |
                        {"second_source_date": f["second_source"].get("date"), "second_source_status": f["second_source"].get("status")} for f in fronts]}
    INDEX.write_text(json.dumps(idx, indent=1))
    print(f"{len(fronts)} dossiers, {idx['admissible']} admissible; second source {dict(states)}; by decade {idx['by_decade']} -> {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
