"""
ripple_big_move_order.py -- C-6: who moved first inside each registered Big Move episode.

DESCRIPTIVE ONLY. No test, no p-value, no verdict. For every Big Moves episode
(data/big_moves/{brent,wti,diesel_crack}.json, BIG_MOVES_REGISTRATION.md Amendments 1-3) and
every daily chain node, the first trading day on which the node's cumulative move since the
close before onset exceeds its own trailing-60-day 2-sigma band:

    sigma   = standard deviation of the node's daily change over the 60 trading days ending the
              day before onset (its own quiet-time scale)
    cum[t]  = y[t] - y[onset-1]                    (100*log for prices; level for cracks/pp)
    first   = min t in [onset, end] with |cum[t]| > 2*sigma        (else "none within episode")

The rule is the brief's rule, applied literally: the band is 2 sigma of a ONE-day change, not
scaled by sqrt(days), so it is a low bar at long horizons -- read the ordering, not the fact
of crossing. n is stated everywhere: episodes with fewer than 3 nodes available are listed but
not aggregated.

Run:  python3 src/ripple_big_move_order.py   -> data/ripple/big_move_order.json (+ a markdown block)
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ripple_lp as RL

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "ripple" / "big_move_order.json"
TRAIL, K_SIGMA = 60, 2.0
ASSETS = ["brent", "wti", "diesel_crack"]           # daily tiers; wti_monthly is a monthly tier (not daily nodes)

# the chain nodes shown, in hop order (equity proxies included, labelled)
NODES = [n for n in RL.NODES_DAILY if not n[0].startswith("transit_")] + \
        [n for n in RL.NODES_DAILY if n[0].startswith("transit_")]
HOP_LABEL = {0: "crude", 1: "products/cracks", 2: "transits", 3: "gas", "x": "macro", "e": "equity proxy"}


def first_crossing(y, idx, onset, end):
    o = idx.searchsorted(pd.Timestamp(onset))
    e = idx.searchsorted(pd.Timestamp(end), side="right") - 1
    if o < TRAIL + 1 or o >= len(idx) or e < o:
        return None
    base = y[o - 1]
    if not np.isfinite(base):
        return None
    d = np.diff(y[o - TRAIL - 1:o])
    d = d[np.isfinite(d)]
    if len(d) < 40:
        return None
    sigma = float(np.std(d, ddof=1))
    if not sigma > 0:
        return None
    cum = y[o:e + 1] - base
    for k, c in enumerate(cum):
        if np.isfinite(c) and abs(c) > K_SIGMA * sigma:
            return {"day": k, "date": idx[o + k].strftime("%Y-%m-%d"), "cum": round(float(c), 3),
                    "sigma_1d": round(sigma, 3), "sign": "+" if c > 0 else "-"}
    return {"day": None, "note": "none within episode", "sigma_1d": round(sigma, 3),
            "max_abs_cum": round(float(np.nanmax(np.abs(cum))) if np.isfinite(cum).any() else float("nan"), 3)}


def main():
    conn = sqlite3.connect(RL.DB)
    Fd = RL.build_daily(conn)
    idx = Fd["idx"]
    episodes_out, per_node_ranks = [], {}
    for asset in ASSETS:
        path = ROOT / "data" / "big_moves" / f"{asset}.json"
        if not path.exists():
            continue
        book = json.loads(path.read_text())
        for ep in book.get("episodes", []):
            rows = []
            for key, sid, how, hop, hh, extra in NODES:
                r = first_crossing(Fd["nodes"][key]["y"], idx, ep["onset"], ep["end"])
                if r is None:
                    continue
                rows.append({"node": key, "hop": HOP_LABEL.get(hop, str(hop)), **r})
            crossed = sorted([r for r in rows if r.get("day") is not None], key=lambda r: (r["day"], r["node"]))
            never = [r["node"] for r in rows if r.get("day") is None]
            for rank, r in enumerate(crossed, 1):
                per_node_ranks.setdefault(r["node"], []).append((rank, r["day"]))
            episodes_out.append({"asset": asset, "onset": ep["onset"], "end": ep["end"], "change_pct": ep.get("change"),
                                 "sign": ep.get("sign"), "attributed_events": [e.get("event_id") or e.get("title") for e in ep.get("events", [])],
                                 "n_nodes_available": len(rows), "order": crossed, "never_crossed": never})
    # cross-episode description (counts only)
    summary = {}
    for node, lst in per_node_ranks.items():
        ranks = [a for a, _ in lst]; days = [b for _, b in lst]
        summary[node] = {"n_episodes_crossed": len(lst), "median_rank": float(np.median(ranks)),
                         "median_day": float(np.median(days)), "first_mover_count": int(sum(1 for a in ranks if a == 1))}
    # crude-before-products count: episodes where brent's day < min(product days)
    prod = ["heating_oil_nyh", "gasoline_gulf", "gasoline_nyh", "jet_gulf", "propane"]
    cbp = {"crude_first": 0, "product_first": 0, "tie": 0, "n": 0}
    for ep in episodes_out:
        days = {r["node"]: r["day"] for r in ep["order"]}
        if "brent" in days and any(p in days for p in prod):
            pm = min(days[p] for p in prod if p in days)
            cbp["n"] += 1
            cbp["crude_first" if days["brent"] < pm else ("tie" if days["brent"] == pm else "product_first")] += 1
    out = {"meta": {"when": datetime.now(timezone.utc).isoformat(timespec="seconds"), "rule": __doc__.split("\n\n")[1],
                    "trailing_days": TRAIL, "k_sigma": K_SIGMA, "assets": ASSETS, "n_episodes": len(episodes_out),
                    "descriptive_only": True},
           "episodes": episodes_out, "per_node": dict(sorted(summary.items(), key=lambda kv: kv[1]["median_rank"])),
           "crude_vs_products": cbp}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print(markdown(out))
    conn.close()
    return out


def markdown(out):
    L = ["## Who moved first (C-6, descriptive, no test)", ""]
    m = out["meta"]
    L.append(f"*{m['n_episodes']} Big Move episodes ({', '.join(m['assets'])} daily tiers). Rule: first day the node's "
             f"cumulative move since the close before onset exceeds {m['k_sigma']}× its own trailing-{m['trailing_days']}-day "
             f"one-day sigma. A low bar at long horizons by construction; the ORDER is the information, not the crossing.*")
    L.append("")
    c = out["crude_vs_products"]
    L.append(f"Brent vs the first product to cross: crude first in {c['crude_first']}, product first in {c['product_first']}, "
             f"same day in {c['tie']}, of n={c['n']} episodes where both crossed.")
    L.append("")
    L.append("| node | hop | episodes crossed | median rank | median day | first-mover count |")
    L.append("|---|---|---|---|---|---|")
    hop_of = {n[0]: HOP_LABEL.get(n[3], str(n[3])) for n in NODES}
    for node, s in out["per_node"].items():
        L.append(f"| {node} | {hop_of.get(node, '')} | {s['n_episodes_crossed']} | {s['median_rank']:.1f} | {s['median_day']:.0f} | {s['first_mover_count']} |")
    L.append("")
    L.append("Per-episode order tables: data/ripple/big_move_order.json (one row per node with day, cumulative move, sigma).")
    L.append("Nodes that never crossed inside an episode are listed there under never_crossed; equity proxies are labelled.")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
