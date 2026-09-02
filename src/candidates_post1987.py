"""candidates_post1987.py -- Brief A-12: the post-1987 candidate sheet (data/candidates/DOSSIER_RULE.md §5).

Every ICB crisis, Dyadic MID with hihost >= 4, UCDP dyad onset and GPR daily spike (> p99 of 1987+) in 1987-2026 with a
registered-state party, that is not within 3 days of a corpus event -> data/candidates/post1987_candidates.csv.
Read-only on every source; nothing enters events.

Run:  python3 src/candidates_post1987.py
"""
import csv
import json
import sqlite3
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "state"))
import countries as C  # noqa: E402
import outcomes as O  # noqa: E402
import panel as P  # noqa: E402
from dossier import STATE_SET, slug  # noqa: E402

OUT = ROOT / "data" / "candidates" / "post1987_candidates.csv"
SUMMARY = ROOT / "data" / "candidates" / "post1987_candidates_summary.json"
LO, HI = "1987-01-01", "2026-12-31"
NEAR_DAYS = 3
COLS = ["event_date", "source", "source_id", "source_detail", "actors", "nearest_corpus_event", "days_to_corpus"]


def corpus_dates(conn):
    return sorted((pd.Timestamp(d), e) for e, d in conn.execute("SELECT event_id, event_date FROM events"))


def nearest(cd, d):
    best = None
    for t, e in cd:
        gap = abs((t - d).days)
        if best is None or gap < best[1]:
            best = (e, gap)
    return best or ("", None)


def icb_rows():
    sysd, _ = O.load_icb()
    act = pd.read_csv(P.raw_path("icb", "icb2v16.csv"), encoding="latin-1"); act.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in act.columns]
    codes = act.groupby("crisno")["cracid"].apply(lambda s: sorted(set(int(x) for x in s))).to_dict()
    for c in sysd[(sysd.trigdate >= LO) & (sysd.trigdate <= HI)].itertuples(index=False):
        cc = codes.get(int(c.crisno), [])
        if set(cc) & STATE_SET:
            yield {"event_date": c.trigdate, "source": "icb", "source_id": str(int(c.crisno)), "source_detail": f"{c.crisname} {c.trigdate.date()}..{c.termdate.date() if pd.notna(c.termdate) else '?'} viol {c.viol}",
                   "actors": ";".join(str(x) for x in cc), "name": c.crisname, "termdate": c.termdate, "viol": c.viol, "forout": c.forout, "ccodes": cc}


def mid_rows():
    m = O.load_mid()
    m = m[(m.hihost >= 4) & (m.start >= LO) & (m.start <= HI)]
    raw = pd.read_csv(P.raw_path("cow_mid", "dyadic_mid_4.03.csv"))
    for disno, g in m.groupby("disno"):
        rr = raw[raw.disno == disno]
        cc = sorted(set(int(x) for x in pd.concat([rr.statea, rr.stateb])))
        if not (set(cc) & STATE_SET):
            continue
        start = g.start.min(); end = g.end.max()
        names = sorted(set(g.namea) | set(g.nameb))
        yield {"event_date": start, "source": "mid", "source_id": str(int(disno)), "source_detail": f"dispute {int(disno)} {'-'.join(names)} {start.date()}..{end.date() if pd.notna(end) else '?'} hihost {int(g.hihost.max())}",
               "actors": ";".join(str(x) for x in cc), "name": " ".join(names) + " dispute", "termdate": end, "hihost": int(g.hihost.max()), "ccodes": cc}


def ucdp_rows():
    z = zipfile.ZipFile(P.raw_path("ucdp", "ucdp-dyadic-261-csv.zip"))
    d = pd.read_csv(z.open([x for x in z.namelist() if x.endswith(".csv")][0]))
    d = d.sort_values(["dyad_id", "year"]).drop_duplicates("dyad_id")
    for r in d.itertuples(index=False):
        sd = str(r.start_date2)[:10]
        if not (LO <= sd <= HI):
            continue
        cc = []
        for col in ("gwno_a", "gwno_b"):
            for tok in str(getattr(r, col)).replace(";", ",").split(","):
                tok = tok.strip()
                if tok.isdigit():
                    cc.append(int(tok))
        cc = sorted(set(cc))
        if not (set(cc) & STATE_SET):
            continue
        yield {"event_date": pd.Timestamp(sd), "source": "ucdp", "source_id": str(int(r.dyad_id)), "source_detail": f"dyad {int(r.dyad_id)} {r.side_a} vs {r.side_b} ({r.location}) onset {sd} intensity {r.intensity_level}",
               "actors": ";".join(str(x) for x in cc), "name": f"{r.side_a} {r.side_b} {r.location}", "termdate": pd.NaT, "ccodes": cc}


def gpr_rows(conn):
    g = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id='gpr.GPRD' AND obs_date>=? ORDER BY obs_date", conn, params=(LO,))
    p99 = float(g.value.quantile(0.99))
    hi = g[g.value > p99].copy()
    hi["obs_date"] = pd.to_datetime(hi.obs_date)
    last = None
    for r in hi.itertuples(index=False):
        if last is not None and (r.obs_date - last).days <= 1:
            last = r.obs_date; continue
        last = r.obs_date
        yield {"event_date": r.obs_date, "source": "gpr", "source_id": r.obs_date.strftime("%Y%m%d"), "source_detail": f"GPRD {r.value:.1f} > p99 {p99:.2f} (1987+, n {len(g)})",
               "actors": "", "name": f"GPR spike {r.obs_date.date()}", "termdate": pd.NaT, "ccodes": []}


def build(conn=None):
    conn = conn or sqlite3.connect(P.DB)
    cd = corpus_dates(conn)
    rows = []
    for gen in (icb_rows(), mid_rows(), ucdp_rows(), gpr_rows(conn)):
        for r in gen:
            e, gap = nearest(cd, r["event_date"])
            if gap is not None and gap <= NEAR_DAYS:
                continue
            r["nearest_corpus_event"], r["days_to_corpus"] = e, gap
            rows.append(r)
    rows.sort(key=lambda r: (r["event_date"], r["source"]))
    return rows


def main():
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "event_date": r["event_date"].date().isoformat()})
    dec = Counter((r["event_date"].year // 10 * 10, r["source"]) for r in rows)
    summary = {"rule": "data/candidates/DOSSIER_RULE.md §5", "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "n": len(rows),
               "by_source": dict(Counter(r["source"] for r in rows)),
               "by_decade": {f"{d}s": {s: n for (dd, s), n in dec.items() if dd == d} for d in sorted({d for d, _ in dec})},
               "excluded_within_3_days_of_corpus": "not counted here; see build()", "output": str(OUT.relative_to(ROOT))}
    SUMMARY.write_text(json.dumps(summary, indent=1))
    print(f"post-1987 candidates: {len(rows)} {summary['by_source']} -> {OUT.relative_to(ROOT)}")
    for d, v in summary["by_decade"].items():
        print(f"  {d}: {v}")


if __name__ == "__main__":
    main()
