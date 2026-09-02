"""
pre1987_candidates.py -- Brief B-3 (2026-09-02): Joe's admission sheet for the monthly tier, per
data/candidates/REGISTRATION.md (registered before this code). Every ICB crisis, COW war and Dyadic MID with
hihost >= 4 dated 1946-01 .. 1986-12 with at least one actor in the registered producer / transit / consumer state
set, joined to the monthly WTI Big Moves episodes and to the +3 m WTI change. READS session A's raw files and
loaders (src/state/icb.py, outcomes.py); WRITES data/candidates/pre1987_candidates.csv and
pre1987_candidates_summary.json. NOTHING enters the events table. suggested_title is blank by design.

Run:  python3 src/engine/pre1987_candidates.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "src" / "state"))
OUT = ROOT / "data" / "candidates"
START, END = pd.Timestamp("1946-01-01"), pd.Timestamp("1986-12-31")
BEFORE_DAYS = 31                      # read.TIERS["monthly"]["before_days"]: the walk's materiality window
HORIZON_M = 3                         # the monthly tier's registered P horizon

# data/candidates/REGISTRATION.md: COW ccode -> (name, roles)
STATES = {
    2: ("United States", "producer,consumer"), 20: ("Canada", "producer"), 70: ("Mexico", "producer"), 100: ("Colombia", "producer"),
    101: ("Venezuela", "producer"), 130: ("Ecuador", "producer"), 140: ("Brazil", "producer"), 160: ("Argentina", "producer"),
    52: ("Trinidad and Tobago", "producer"), 200: ("United Kingdom", "producer,consumer"), 385: ("Norway", "producer"),
    365: ("USSR/Russia", "producer,consumer"), 360: ("Romania", "producer"), 615: ("Algeria", "producer"), 620: ("Libya", "producer"),
    475: ("Nigeria", "producer"), 481: ("Gabon", "producer"), 540: ("Angola", "producer"), 651: ("Egypt", "producer,transit"),
    630: ("Iran", "producer,transit"), 645: ("Iraq", "producer"), 670: ("Saudi Arabia", "producer"), 690: ("Kuwait", "producer"),
    692: ("Bahrain", "producer,transit"), 694: ("Qatar", "producer"), 696: ("UAE", "producer,transit"), 698: ("Oman", "producer,transit"),
    710: ("China", "producer,consumer"), 850: ("Indonesia", "producer,transit"), 820: ("Malaysia", "producer,transit"), 835: ("Brunei", "producer"),
    652: ("Syria", "transit"), 660: ("Lebanon", "transit"), 663: ("Jordan", "transit"), 666: ("Israel", "transit"), 640: ("Turkey", "transit"),
    678: ("Yemen Arab Republic", "transit"), 680: ("Yemen People's Republic", "transit"), 679: ("Yemen", "transit"),
    522: ("Djibouti", "transit"), 520: ("Somalia", "transit"), 530: ("Ethiopia", "transit"), 531: ("Eritrea", "transit"),
    95: ("Panama", "transit"), 830: ("Singapore", "transit"), 390: ("Denmark", "transit"),
    740: ("Japan", "consumer"), 260: ("West Germany", "consumer"), 255: ("Germany", "consumer"), 220: ("France", "consumer"),
    325: ("Italy", "consumer"), 750: ("India", "consumer"), 732: ("South Korea", "consumer"),
}


def _name(cc):
    try:
        cc = int(cc)
    except (TypeError, ValueError):
        return str(cc)
    return STATES[cc][0] if cc in STATES else f"ccode {cc}"


def _date(y, m, d):
    """COW dates: unknown (-9) month/day -> 1; day clamped to 28 (as session A's ies90._mid_date does)."""
    y, m, d = int(y), int(m), int(d)
    if y <= 0:
        return pd.NaT
    return pd.Timestamp(year=y, month=min(max(m, 1), 12), day=min(max(d, 1), 28))


def _in_range(d):
    return pd.notna(d) and START <= d <= END


def icb_rows():
    import icb as ICB
    import panel as P
    sysd = ICB.crises()
    act = pd.read_csv(P.raw_path("icb", "icb2v16.csv"), encoding="latin-1")
    act.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in act.columns]
    actors = defaultdict(list)
    for r in act.itertuples(index=False):
        actors[int(r.crisno)].append(int(r.cracid))
    rows = []
    for c in sysd.itertuples(index=False):
        if not _in_range(c.trigdate):
            continue
        cc = actors.get(int(c.crisno), [])
        if not any(x in STATES for x in cc):
            continue
        rows.append({"event_date": str(c.trigdate.date()), "actors": "; ".join(_name(x) for x in sorted(set(cc))), "source": "ICB v16",
                     "source_id": f"crisno {int(c.crisno)}",
                     "source_detail": f"{c.crisname}; {c.trigdate.date()}..{c.termdate.date() if pd.notna(c.termdate) else '?'}; viol {int(c.viol) if pd.notna(c.viol) else '?'}; forout {int(c.forout) if pd.notna(c.forout) else '?'}"})
    return rows


def war_rows():
    import panel as P
    rows = []
    inter = pd.read_csv(P.raw_path("cow_war", "Inter-StateWarData_v4.0.csv"), encoding="latin-1")
    by = defaultdict(list)
    for r in inter.itertuples(index=False):
        by[int(r.WarNum)].append(r)
    for wn, ps in by.items():
        starts = [x for x in (_date(p.StartYear1, p.StartMonth1, p.StartDay1) for p in ps) if pd.notna(x)]
        d = min(starts) if starts else pd.NaT
        if not _in_range(d):
            continue
        ccs = [int(p.ccode) for p in ps]
        if not any(x in STATES for x in ccs):
            continue
        rows.append({"event_date": str(d.date()), "actors": "; ".join(f"{_name(p.ccode)} (side {int(p.Side)})" for p in ps), "source": "COW War v4.0 inter-state",
                     "source_id": f"WarNum {wn}", "source_detail": f"{ps[0].WarName}; {len(ps)} participants; battle deaths {sum(int(p.BatDeath) for p in ps if int(p.BatDeath) > 0)}"})
    intra = pd.read_csv(P.raw_path("cow_war", "Intra-StateWarData_v4.1.csv"), encoding="latin-1")
    byi = defaultdict(list)
    for r in intra.itertuples(index=False):
        byi[int(r.WarNum)].append(r)
    for wn, ps in byi.items():                       # one row per war: the file carries one row per war-side / spell
        starts = [x for x in (_date(p.StartYear1, p.StartMonth1, p.StartDay1) for p in ps) if pd.notna(x)]
        d = min(starts) if starts else pd.NaT
        if not _in_range(d):
            continue
        ccs = sorted({int(x) for p in ps for x in (p.CcodeA, p.CcodeB) if pd.notna(x) and int(x) > 0})
        if not any(x in STATES for x in ccs):
            continue
        sides = sorted({f"{p.SideA} vs {p.SideB}" for p in ps})
        ends = [x for x in (_date(p.EndYear1, p.EndMonth1, p.EndDay1) for p in ps) if pd.notna(x)]
        rows.append({"event_date": str(d.date()), "actors": "; ".join(_name(x) for x in ccs) + "; " + " | ".join(sides), "source": "COW War v4.1 intra-state",
                     "source_id": f"WarNum {wn}", "source_detail": f"{ps[0].WarName}; {d.date()}..{max(ends).date() if ends else 'ongoing/unknown'}"})
    return rows


def mid_rows():
    import outcomes as O
    mid = O.load_mid()
    rows = []
    for disno, g in mid.groupby("disno"):
        d = g["start"].min()
        if not _in_range(d):
            continue
        hi = int(g["hihost"].max())
        if hi < 4:
            continue
        ccs = set(int(x) for x in g["statea"]) | set(int(x) for x in g["stateb"])
        if not any(x in STATES for x in ccs):
            continue
        pairs = sorted({f"{a}-{b}" for a, b in zip(g["namea"], g["nameb"])})
        rows.append({"event_date": str(d.date()), "actors": "; ".join(_name(x) for x in sorted(ccs)), "source": "Dyadic MID 4.03",
                     "source_id": f"disno {int(disno)}",
                     "source_detail": f"hihost {hi} ({'war' if hi == 5 else 'use of force'}); dyads {', '.join(pairs)}; {d.date()}..{g['end'].max().date() if pd.notna(g['end'].max()) else '?'}"})
    return rows


def main():
    from _db import connect
    import engine.similarity as S
    rows = icb_rows() + war_rows() + mid_rows()
    eps = json.load(open(ROOT / "data" / "big_moves" / "wti_monthly.json"))["episodes"]
    win = [(f"wti_{e['onset']}", pd.Timestamp(e["onset"]) - pd.Timedelta(days=BEFORE_DAYS), pd.Timestamp(e["end"]), e["change"]) for e in eps]
    wti = S._series(connect(read_only=True), "fred.WTISPLC")
    for r in rows:
        d = pd.Timestamp(r["event_date"])
        hit = next(((eid, chg) for eid, a, b, chg in win if a <= d <= b), None)
        r["inside_big_move"] = bool(hit)
        r["episode_id"] = hit[0] if hit else ""
        r["monthly_move_pct"] = hit[1] if hit else ""
        pos = int(wti.index.searchsorted(d.replace(day=1)))
        r["wti_chg_3m_pct"] = round(float((wti.iloc[pos + HORIZON_M] / wti.iloc[pos] - 1) * 100), 2) if pos + HORIZON_M < len(wti) else ""
        r["suggested_title"] = ""
    rows.sort(key=lambda r: (r["event_date"], r["source"], r["source_id"]))
    cols = ["event_date", "actors", "source", "source_id", "source_detail", "inside_big_move", "episode_id", "monthly_move_pct", "wti_chg_3m_pct", "suggested_title"]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pre1987_candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    dec = Counter(r["event_date"][:3] + "0s" for r in rows)
    summary = {"registration": "data/candidates/REGISTRATION.md (2026-09-02)", "generated_at": pd.Timestamp.utcnow().isoformat(),
               "n_rows": len(rows), "by_decade": dict(sorted(dec.items())), "by_source": dict(Counter(r["source"] for r in rows)),
               "by_decade_and_source": {k: dict(Counter(r["source"] for r in rows if r["event_date"][:3] + "0s" == k)) for k in sorted(dec)},
               "inside_big_move": sum(1 for r in rows if r["inside_big_move"]), "episodes_1946_1986": sum(1 for e in eps if e["onset"] <= "1986-12-31"),
               "episodes_with_a_candidate": len({r["episode_id"] for r in rows if r["episode_id"]}),
               "note": "Joe's admission sheet (PATH Step 5). Nothing here enters events. Each source's own record; duplicates across sources by design."}
    json.dump(summary, open(OUT / "pre1987_candidates_summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
