"""Link catalogue events to frozen impairment episodes (DISRUPTION_REALIZATION.md §15-§17).

This module runs **after** `src/disruption_episodes.py` has frozen its output. It reads that frozen
table and the event catalogue; it never re-detects and never alters an episode.

Two quantities only, and the wording of the second matters:

* **A** — of *eligible* catalogue events, the proportion linked to a detected episode.
* **B** — of detected episodes, the proportion linked to an eligible catalogue event.

An episode with no linked event is **"not matched to the current event catalogue"**. It is not
"silent", "undeclared", "unexpected" or "ignored": the 313-event catalogue is curated and is not a
census of declarations (`docs/audit/V3_DATA_AUDIT.md` §10), so the bottom row of a 2×2 is not
identifiable from this data and no 2×2 is produced.

Sources: UN Global Platform; IMF PortWatch.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V3 = ROOT / "data" / "v3"
EPISODES = V3 / "episodes_n_tanker.csv"
EVENT_ROUTES = V3 / "event_routes.csv"

# §15, fixed before linkage ran. Built by earlier sessions for other purposes, so exogenous here.
ENTITY_TO_ROUTE = {
    "chokepoint.hormuz": "hormuz",
    "chokepoint.bab_el_mandeb": "bab_el_mandeb",
    "chokepoint.suez": "suez",
    "chokepoint.suez_canal": "suez",
    "chokepoint.bosporus": "bosporus",
    "chokepoint.malacca": "malacca",
    "chokepoint.panama": "panama",
}
# §16 primary window, plus the strict variant reported alongside so the lead is visible.
WINDOW_PRIMARY = (-2, 14)
WINDOW_STRICT = (0, 14)
DETECTION_START = dt.date(2020, 1, 31)   # §4


def export_event_routes(db, out_path=EVENT_ROUTES):
    """One-time export of the exogenous event→route mapping, so linkage is reproducible offline."""
    import sqlite3
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rows = conn.execute("""
            SELECT v.event_id, v.event_date, v.type, v.title, e.entity_id
            FROM events v JOIN event_entities e ON e.event_id = v.event_id
            WHERE e.role = 'location' ORDER BY v.event_date, v.event_id
        """).fetchall()
    finally:
        conn.close()
    mapped = [(eid, d, t, title, ENTITY_TO_ROUTE[ent])
              for eid, d, t, title, ent in rows if ent in ENTITY_TO_ROUTE]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("event_id", "event_date", "type", "title", "route"))
        w.writerows(mapped)
    return mapped


def wilson(k, n, z=1.96):
    """Wilson score interval. Honest at small n, which is the whole situation here."""
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def load_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def link(episodes_path=EPISODES, events_path=EVENT_ROUTES, window=WINDOW_PRIMARY):
    episodes = load_rows(episodes_path)
    events = load_rows(events_path)
    lo, hi = window

    eligible, excluded = [], []
    for e in events:
        d = dt.date.fromisoformat(e["event_date"])
        if d < DETECTION_START:
            excluded.append({**e, "reason": "before detection window"})
        else:
            eligible.append({**e, "_date": d})

    links = []
    for ev in eligible:
        for ep in episodes:
            if ep["route"] != ev["route"]:
                continue
            start = dt.date.fromisoformat(ep["start_date"])
            if ev["_date"] + dt.timedelta(days=lo) <= start <= ev["_date"] + dt.timedelta(days=hi):
                links.append((ev["event_id"], ep["episode_id"]))

    linked_events = {a for a, _ in links}
    linked_eps = {b for _, b in links}
    n_ev, n_ep = len(eligible), len(episodes)
    return {
        "window": list(window),
        "n_catalogue_total": 313,
        "n_route_mapped": len(events),
        "n_excluded_before_detection": len(excluded),
        "n_eligible_events": n_ev,
        "n_eligible_events_linked": len(linked_events),
        "proportion_A_events_linked": round(len(linked_events) / n_ev, 4) if n_ev else None,
        "proportion_A_wilson95": wilson(len(linked_events), n_ev),
        "n_episodes": n_ep,
        "n_episodes_linked": len(linked_eps),
        "proportion_B_episodes_linked": round(len(linked_eps) / n_ep, 4) if n_ep else None,
        "proportion_B_wilson95": wilson(len(linked_eps), n_ep),
        "links": sorted(links),
        "eligible_events_not_linked": sorted(
            (e["event_id"], e["event_date"], e["route"], e["title"])
            for e in eligible if e["event_id"] not in linked_events),
        "episodes_not_matched_to_catalogue": sorted(
            (ep["episode_id"], ep["route"], ep["start_date"], ep["end_date"],
             ep["fractional_impairment"])
            for ep in episodes if ep["episode_id"] not in linked_eps),
        "excluded_events": sorted((e["event_id"], e["event_date"], e["reason"]) for e in excluded),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--episodes", type=Path, default=EPISODES)
    ap.add_argument("--events", type=Path, default=EVENT_ROUTES)
    ap.add_argument("--export-from-db", type=Path, default=None,
                    help="one-time export of the event→route mapping from data/oil.db")
    ap.add_argument("--out", type=Path, default=V3)
    args = ap.parse_args()

    if args.export_from_db:
        rows = export_event_routes(args.export_from_db, args.events)
        print(f"exported {len(rows)} route-mapped events -> {args.events}")

    primary = link(args.episodes, args.events, WINDOW_PRIMARY)
    strict = link(args.episodes, args.events, WINDOW_STRICT)
    result = {"primary": primary, "strict_window_sensitivity": {
        k: strict[k] for k in ("window", "n_eligible_events_linked", "proportion_A_events_linked",
                               "n_episodes_linked", "proportion_B_episodes_linked")}}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "linkage.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    p = primary
    print(f"\nELIGIBILITY: 313 catalogue -> {p['n_route_mapped']} route-mapped -> "
          f"{p['n_eligible_events']} inside detection window "
          f"({p['n_excluded_before_detection']} excluded as pre-2020-01-31)")
    print(f"\nA  eligible events linked to an episode: {p['n_eligible_events_linked']}"
          f"/{p['n_eligible_events']} = {p['proportion_A_events_linked']}  "
          f"95% Wilson {p['proportion_A_wilson95']}")
    print(f"B  episodes linked to an eligible event:  {p['n_episodes_linked']}"
          f"/{p['n_episodes']} = {p['proportion_B_episodes_linked']}  "
          f"95% Wilson {p['proportion_B_wilson95']}")
    print(f"\nstrict window {WINDOW_STRICT}: A = {strict['proportion_A_events_linked']}, "
          f"B = {strict['proportion_B_episodes_linked']}")
    print("\nEpisodes not matched to the current event catalogue "
          "(NOT 'undeclared' -- the catalogue is not a census):")
    for eid, route, s, e, frac in p["episodes_not_matched_to_catalogue"]:
        print(f"   {route:14s} {s} .. {e}  impairment {frac}")
    print("\nEligible events not linked to any episode:")
    for eid, d, route, title in p["eligible_events_not_linked"]:
        print(f"   {d}  {route:14s} {title[:60]}")
    print("\nSources: UN Global Platform; IMF PortWatch.")


if __name__ == "__main__":
    main()
