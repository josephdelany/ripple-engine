"""
me_subset.py -- the Middle East subset, prepped for the 'ME conflict & the global
                economy' paper. DESCRIPTIVE ONLY.

It slices the corpus to events touching a Middle-East entity (the ME producers,
Israel/Lebanon, and the Hormuz/Bab-el-Mandeb/Suez chokepoints), then lays the
numbers out three ways for a writing session:
  1. a per-decade table of clustered CAR+20 for ME conflict + infrastructure
     shocks (1990s -> 2020s);
  2. a per-event appendix (every ME event, its type and Brent CAR+20);
  3. cross-asset reaction lines (read from the committed edges table) for the five
     biggest ME ripples.

There is NO trend test and NO verdict here -- decade means at this sample size are
anecdote, and the report says so loudly. Reuses event_study/robustness by import.

Run:  python3 src/me_subset.py
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from event_study import car_for_event, PRE
from robustness import assign_clusters
from cross_asset import asset_returns

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "me_report.txt"
BRENT = "fred.DCOILBRENTEU"

# The Middle-East entity net for this slice.
ME_ENTITIES = {
    "country.iraq", "country.iran", "country.israel", "country.saudi_arabia",
    "country.kuwait", "country.yemen", "country.lebanon",
    "chokepoint.hormuz", "chokepoint.bab_el_mandeb", "chokepoint.suez",
}
DECADE_LABEL = {1990: "1990s", 2000: "2000s", 2010: "2010s", 2020: "2020s"}
SMALL_N = 3


def me_events(conn):
    """Events touching a Middle-East entity, with their Brent CAR+20 (%)."""
    me_ids = {r[0] for r in conn.execute(
        "SELECT DISTINCT event_id FROM event_entities WHERE entity_id IN "
        f"({','.join('?' * len(ME_ENTITIES))})", tuple(ME_ENTITIES))}
    ev = pd.read_sql("SELECT event_id, event_date AS date, type FROM events "
                     "ORDER BY event_date", conn)
    ev = ev[ev["event_id"].isin(me_ids)].copy()
    ret = asset_returns(conn, BRENT, "price")
    rows = []
    for _, e in ev.iterrows():
        car = car_for_event(ret, e["date"])
        if car is None:
            continue
        rows.append({"event_id": e["event_id"], "date": e["date"], "type": e["type"],
                     "car20": car[PRE + 20] * 100,
                     "decade": (int(e["date"][:4]) // 10) * 10})
    return pd.DataFrame(rows)


def main():
    conn = sqlite3.connect(DB)
    me = me_events(conn)
    if me.empty:
        print("No Middle-East events found."); conn.close(); return

    lines = []
    w = lines.append
    w("=" * 88)
    w("MIDDLE EAST SUBSET -- data prep for the 'ME conflict & the global economy' paper")
    w("DESCRIPTIVE ONLY. No trend test, no verdict. Decade means at this n are "
      "anecdote, not statistics.")
    w("=" * 88)
    w(f"ME entities: {', '.join(sorted(e.split('.')[-1] for e in ME_ENTITIES))}")
    w(f"ME events in corpus: {len(me)}  "
      f"(types: {', '.join(f'{t}={n}' for t, n in me['type'].value_counts().items())})")
    w("")

    # 1. Per-decade clustered CAR+20 for ME conflict + infrastructure shocks
    ci = me[me["type"].isin(["conflict_escalation", "infrastructure_attack"])].copy()
    clustered = assign_clusters(ci).groupby("cluster").first().reset_index()
    w("1. PER-DECADE CAR+20 -- ME conflict + infrastructure shocks (clustered, Brent)")
    w(f"   {'decade':<10}{'n':>4}{'mean CAR+20':>14}{'range':>22}")
    w("   " + "-" * 50)
    for dec in sorted(DECADE_LABEL):
        grp = clustered[clustered["decade"] == dec]
        if grp.empty:
            w(f"   {DECADE_LABEL[dec]:<10}{0:>4}{'  -- no events --':>36}")
            continue
        v = grp["car20"]
        flag = "  << n<=%d, ANECDOTE" % SMALL_N if len(grp) <= SMALL_N else ""
        w(f"   {DECADE_LABEL[dec]:<10}{len(grp):>4}{v.mean():>+13.1f}%"
          f"{f'[{v.min():+.1f}%, {v.max():+.1f}%]':>22}{flag}")
    w("   >>> Every cell above is a small-sample mean. Read as illustration, not trend. <<<")
    w("")

    # 2. Per-event appendix
    w("2. PER-EVENT APPENDIX -- all ME events (Brent CAR+20)")
    w(f"   {'date':<12}{'type':<24}{'CAR+20':>9}  event_id")
    w("   " + "-" * 74)
    for _, r in me.sort_values("date").iterrows():
        w(f"   {r['date']:<12}{r['type']:<24}{r['car20']:>+8.1f}%  {r['event_id']}")
    w("")

    # 3. Cross-asset lines for the five biggest ME ripples (from the edges table)
    w("3. CROSS-ASSET REACTION -- the 5 biggest ME ripples (|CAR+20|), from edges table")
    top5 = me.reindex(me["car20"].abs().sort_values(ascending=False).index).head(5)
    for _, r in top5.iterrows():
        w(f"   {r['event_id']} ({r['date']}, Brent CAR+20 {r['car20']:+.1f}%):")
        edges = conn.execute(
            "SELECT target_series, car20, units FROM edges WHERE event_id=? "
            "ORDER BY target_series", (r["event_id"],)).fetchall()
        if not edges:
            w("       (no cross-asset edges -- run cross_asset.py)")
        else:
            w("       " + "   ".join(f"{ts.split('.')[-1]}={c20:+.1f}{u.split(' ')[0]}"
                                     for ts, c20, u in edges))
    w("")
    w("DESCRIPTIVE MEASUREMENT ONLY. Conditioning or trend claims require a future "
      "registered hypothesis (Joe's gate).")
    conn.close()

    text = "\n".join(lines)
    OUT.write_text(text + "\n")
    print(text)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
