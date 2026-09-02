"""audit_ies90.py -- Joe's audit recorder for the IES-90 label audit (PATH Step 4 gate; Brief A-5).

Walks data/audits/ies90_audit_30.csv event by event in the terminal: the event, its dyad/location set, the engine's
level / basis / rule_fired, and every source record that produced the level with the URL of that record's page.
Asks Joe for HIS level (0/1/2/3), the DEAL flag, and a note; writes data/audits/outcome_audit.json after every
answer (resumable). The code never fills a row: a blank answer records nothing. kappa is Cohen's unweighted kappa
over the four levels between Joe and the engine on the answered rows (outcomes.cohen_kappa, the Step 4 code);
`passed` is true only when every row is answered and kappa >= 0.6 (WALK_FORWARD_PROTOCOL.md §1 / §7).

Run:  python3 src/audit_ies90.py            # resume where Joe left off
      python3 src/audit_ies90.py --status   # progress only, no questions
"""
import csv
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHEET = ROOT / "data" / "audits" / "ies90_audit_30.csv"
OUT = ROOT / "data" / "audits" / "outcome_audit.json"
THRESHOLD = 0.6
LEVELS = ("0", "1", "2", "3")
sys.path.insert(0, str(ROOT / "src" / "state"))


def record_url(src, record, locations=""):
    """The page of the exact source record, so Joe can open it. GED has no event id in the cache: the UCDP country page."""
    m = re.search(r"crisis (\d+)", record)
    if src == "icb" and m:
        return f"https://www.icb.umd.edu/dataviewer/?crisno={m.group(1)}"
    m = re.search(r"dispute (\d+)", record)
    if src in ("mid", "midi") and m:
        return f"https://correlatesofwar.org/data-sets/mids/  (MID 5 narratives PDFs in data/state/raw/cow_mid/MID-5-Data-and-Supporting-Materials.zip; dispute {m.group(1)})"
    m = re.search(r"war (\d+)", record)
    if src == "war" and m:
        return f"https://correlatesofwar.org/data-sets/cow-war/  (WarNum {m.group(1)})"
    if src == "ged":
        import countries as C
        urls = []
        for ent in (locations or "").split(","):
            ent = ent.strip()
            if ent in C.ALL:
                urls.append(f"https://ucdp.uu.se/country/{C.ALL[ent][0]}")
        return " ".join(urls) or "https://ucdp.uu.se/downloads/"
    return ""


def load_sheet(path=SHEET):
    """{event_id: {"event": row, "sources": [rows]}} in sheet order."""
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    ev = OrderedDict()
    for r in rows:
        if r["row_type"] == "event":
            ev[r["event_id"]] = {"event": r, "sources": []}
        else:
            ev[r["event_id"]]["sources"].append(r)
    return ev


def load_out(path=OUT):
    if Path(path).exists():
        return json.loads(Path(path).read_text())
    return {"auditor": "joe", "protocol": "WALK_FORWARD_PROTOCOL.md §1 (kappa >= 0.6 against sources) / §7", "threshold": THRESHOLD,
            "sheet": str(SHEET.relative_to(ROOT)), "started_at": None, "dated": None, "rows": [], "n_rows": None, "n_done": 0,
            "kappa": None, "passed": False}


def kappa(rows):
    import outcomes as O
    a = [str(r["joe_level"]) for r in rows if str(r.get("joe_level")) in LEVELS]
    b = [str(r["engine_level"]) for r in rows if str(r.get("joe_level")) in LEVELS]
    k, n, conf = O.cohen_kappa(a, b, labels=LEVELS)
    return k, n, conf


def finalize(out, n_rows):
    k, n, conf = kappa(out["rows"])
    out["n_rows"] = n_rows
    out["n_done"] = n
    out["kappa"] = k
    out["confusion_joe_x_engine"] = conf
    out["passed"] = bool(n_rows and n == n_rows and k is not None and k >= THRESHOLD)
    out["dated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out["deal_agreement"] = None
    pairs = [(r["joe_deal"], r["engine_deal"]) for r in out["rows"] if r.get("joe_deal") in (0, 1) and r.get("engine_deal") in (0, 1)]
    if pairs:
        out["deal_agreement"] = {"n": len(pairs), "agree": sum(1 for a, b in pairs if a == b)}
    return out


def show(eid, item, i, n):
    e = item["event"]
    print("=" * 78)
    print(f"[{i}/{n}] {eid}   {e['event_date']} ({e['date_precision']})   class {e['class']}")
    print(f"  {e['title']}")
    print(f"  source: {e['source_url']}")
    print(f"  countries A: {e['countries_A'] or '-'}   location L: {e['location_L'] or '-'}" + (f"   (littoral: {e['littoral_from']})" if e.get("littoral_from") else ""))
    print(f"  ENGINE: level {e['ies90_level']} ({e['ies90_level_meaning']})   DEAL {e['ies90_deal'] or '-'}   basis {e['basis']}   rule {e['rule_fired']}")
    print("  source records:")
    for s in item["sources"]:
        print(f"    - [{s['src']}/{s['record_basis']}] {s['record']}  {s['record_dates']}  -> level {s['level_contributed'] or '-'}  rule {s['record_rule'] or '-'}")
        print(f"        {s['code_and_rule']}")
        u = record_url(s["src"], s["record"], e["location_L"])
        if u:
            print(f"        open: {u}")


def ask_row(ask):
    """Joe's answer for one row, or None (skip) / 'quit'. Blank level = nothing recorded."""
    while True:
        lv = ask("  YOUR level (0 none / 1 threat-display / 2 force / 3 war; s = skip, q = quit): ").strip().lower()
        if lv in ("q", "quit"):
            return "quit"
        if lv in ("s", "skip", ""):
            return None
        if lv in LEVELS:
            break
        print("  enter 0, 1, 2, 3, s or q")
    while True:
        d = ask("  DEAL in the 90 days? (y / n / blank = unknown): ").strip().lower()
        if d in ("", "y", "n", "yes", "no"):
            break
    note = ask("  note (source you checked, disagreement reason; blank ok): ").strip()
    return {"joe_level": int(lv), "joe_deal": (1 if d.startswith("y") else 0 if d.startswith("n") else None), "joe_note": note}


def run(sheet=SHEET, out_path=OUT, ask=input, echo=print):
    ev = load_sheet(sheet)
    out = load_out(out_path)
    out["started_at"] = out.get("started_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
    done = {r["event_id"] for r in out["rows"]}
    todo = [e for e in ev if e not in done]
    echo(f"IES-90 label audit -- {len(done)} of {len(ev)} rows answered; {len(todo)} to go. Auditor: joe. Ctrl-C or q to stop; answers are saved as you go.")
    n = len(ev)
    for i, eid in enumerate(list(ev), 1):
        if eid in done:
            continue
        show(eid, ev[eid], i, n)
        ans = ask_row(ask)
        if ans == "quit":
            break
        if ans is None:
            echo("  skipped (nothing recorded)")
            continue
        e = ev[eid]["event"]
        out["rows"].append({"event_id": eid, "event_date": e["event_date"], "engine_level": int(e["ies90_level"]),
                            "engine_deal": (int(float(e["ies90_deal"])) if e["ies90_deal"] not in ("", None) else None),
                            "engine_basis": e["basis"], "rule_fired": e["rule_fired"], **ans,
                            "answered_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        finalize(out, n)
        Path(out_path).write_text(json.dumps(out, indent=1))
    finalize(out, n)
    Path(out_path).write_text(json.dumps(out, indent=1))
    echo(f"saved {Path(out_path).name}: {out['n_done']}/{out['n_rows']} answered, kappa {out['kappa']}, passed {out['passed']} (threshold {THRESHOLD}, all rows required)")
    return out


def status(sheet=SHEET, out_path=OUT):
    n = len(load_sheet(sheet)) if Path(sheet).exists() else 0
    if not Path(out_path).exists():
        return {"status": "pending", "n_done": 0, "n_rows": n, "kappa": None, "passed": False, "auditor": None, "dated": None}
    o = json.loads(Path(out_path).read_text())
    st = "done" if o.get("n_done") == n and n else ("in progress" if o.get("n_done") else "pending")
    return {"status": st, "n_done": o.get("n_done", 0), "n_rows": n, "kappa": o.get("kappa"), "passed": bool(o.get("passed")),
            "auditor": o.get("auditor"), "dated": o.get("dated"), "threshold": o.get("threshold", THRESHOLD)}


if __name__ == "__main__":
    if "--status" in sys.argv:
        print(json.dumps(status(), indent=1))
    else:
        run()
