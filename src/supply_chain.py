"""
supply_chain.py -- close criticality's transmission-magnitude gap (Step 2), validated.

criticality.py maps WHO controls each strategic commodity and flags exposure ("a critical producer
is in an active conflict"), but explicitly leaves the TRANSMISSION MAGNITUDE "a later, calibrated
step." This is that step, gated: for each strategic commodity that has a priced node, and each of its
top producers that appears enough in the event corpus, measure the commodity's signed CAR+20 around
shocks involving that producer, with a bootstrap CI + permutation p. The edge is:

    producer-conflict  →  commodity   {validated | null | insufficient}

validated = the CI excludes zero (a real directional ripple); insufficient = too few producer events
to test (reported, not hidden). This turns the supply-chain map from "exposure" into calibrated
"this is what a Russia shock has historically done to palladium/wheat," with receipts. Edges land in
the propagation_edges table (kind='supplychain'). Reuses criticality + cross_asset + event study +
robustness clustering + validate. numpy-only; point-in-time.

Run:  python3 src/supply_chain.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

import criticality
from cross_asset import asset_returns, ASSETS
from event_study import car_for_event, PRE
from robustness import assign_clusters
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "supply_chain.json"

# strategic commodity (criticality.yaml key) -> priced node series in the engine
COMMODITY_NODE = {
    "palladium": "yf.palladium", "wheat": "yf.wheat", "copper": "yf.copper",
    "crude_oil": "fred.DCOILBRENTEU", "natural_gas": "fred.DHHNGSP",
}
MIN_PRODUCER_EVENTS = 6         # below this, we say "insufficient", never guess
ASSET_BY_SERIES = {a["series"]: a for a in ASSETS}


def _producer_events(conn, producer):
    rows = conn.execute(
        "SELECT DISTINCT e.event_id, e.event_date FROM events e "
        "JOIN event_entities ee ON ee.event_id=e.event_id WHERE ee.entity_id=? "
        "ORDER BY e.event_date", (f"country.{producer}",)).fetchall()
    return rows


def _edge(conn, node_series, events):
    """Clustered signed CAR+20 of the commodity node around a producer's events -> CI + perm."""
    a = ASSET_BY_SERIES.get(node_series, {"kind": "price"})
    ret = asset_returns(conn, node_series, a.get("kind", "price"))
    if ret is None:
        return None
    rows = []
    for eid, d in events:
        car = car_for_event(ret, d)
        if car is None or PRE + 20 >= len(car):
            continue
        c = float(car[PRE + 20]) * (100 if a.get("kind") in ("price", "weekly") else 1)
        rows.append({"event_id": eid, "date": d, "car": c})
    if len(rows) < MIN_PRODUCER_EVENTS:
        return {"n": len(rows), "status": "insufficient"}
    df = assign_clusters(pd.DataFrame(rows))
    cars = df.groupby("cluster").first()["car"].tolist()
    if len(cars) < 4:
        return {"n": len(cars), "status": "insufficient"}
    ci = validate.bootstrap_ci(cars, stat="mean")
    excl0 = ci["lo"] is not None and (ci["lo"] > 0 or ci["hi"] < 0)
    return {"n": ci["n"], "car": ci["stat"], "ci": [ci["lo"], ci["hi"]],
            "status": "validated" if excl0 else "null",
            "polarity": "+" if (ci["stat"] or 0) >= 0 else "-", "unit": a.get("unit", "%")}


def build(conn):
    commodities = criticality.load_map()
    edges = []
    for commodity, node in COMMODITY_NODE.items():
        c = commodities.get(commodity, {})
        producers = list((c.get("top") or {}).items())
        for producer, share in producers:
            evs = _producer_events(conn, producer)
            r = _edge(conn, node, evs)
            if r is None:
                continue
            edges.append({"kind": "supplychain", "producer": producer, "producer_share": share,
                          "commodity": commodity, "node": node, "n": r["n"],
                          "car": r.get("car"), "ci": r.get("ci"), "unit": r.get("unit", "%"),
                          "status": r["status"],
                          "mechanism": f"{producer} ({share}% of {commodity}) conflict -> {commodity} "
                                       f"CAR+20"})
    # persist validated/null edges into the propagation graph's edge table
    conn.execute("""CREATE TABLE IF NOT EXISTS propagation_edges (
        edge_id TEXT PRIMARY KEY, kind TEXT, from_node TEXT, to_node TEXT, lag TEXT,
        strength REAL, ci_lo REAL, ci_hi REAL, perm_p REAL, status TEXT, mechanism TEXT)""")
    rows = [(f"sc.{e['producer']}.{e['commodity']}", "supplychain",
             f"conflict.{e['producer']}", e["commodity"], "20d", e.get("car"),
             (e.get("ci") or [None, None])[0], (e.get("ci") or [None, None])[1],
             None, e["status"], e["mechanism"]) for e in edges if e["status"] != "insufficient"]
    conn.executemany("INSERT OR REPLACE INTO propagation_edges VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()

    validated = [e for e in edges if e["status"] == "validated"]
    report = {
        "what": "Validated supply-chain transmission: producer-conflict -> strategic-commodity ripple, "
                "gated (signed CAR+20 + bootstrap CI). Closes criticality's 'transmission magnitude' gap.",
        "min_producer_events": MIN_PRODUCER_EVENTS, "n_edges_tested": len(edges),
        "validated": validated, "all_edges": edges,
    }
    OUT.write_text(json.dumps(report, indent=2, default=str))
    return report


def main():
    conn = sqlite3.connect(DB)
    r = build(conn)
    conn.close()
    print("=" * 82)
    print("SUPPLY-CHAIN TRANSMISSION -- producer-conflict -> strategic-commodity (validated)")
    print("=" * 82)
    print(f"  {len(r['validated'])} VALIDATED of {r['n_edges_tested']} tested "
          f"(>= {r['min_producer_events']} producer events required):")
    for e in sorted(r["all_edges"], key=lambda e: (e["status"] != "validated", -(abs(e.get("car") or 0)))):
        if e["status"] == "insufficient":
            tag = f"insufficient (n={e['n']})"
            print(f"    {e['producer']:<14} -> {e['commodity']:<12} [{tag}]")
        else:
            ci = e["ci"]
            print(f"    {e['producer']:<14} -> {e['commodity']:<12} {e['car']:+6.1f}{e['unit']:<3} "
                  f"CI[{ci[0]:+.1f},{ci[1]:+.1f}]  [{e['status'].upper()}]  ({e['producer_share']}% producer)")
    print("\n  Validated = CI excludes zero (a real directional ripple); null = spans zero; insufficient")
    print("  = too few producer events to test (reported, not guessed). Receipts in data/supply_chain.json.")


if __name__ == "__main__":
    main()
