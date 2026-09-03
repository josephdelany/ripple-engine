"""big_moves.py -- market-defined significance (NORTH_STAR §1c, spec §4.0, A11).

Reads the record the other way round: find every time an asset actually changed
(top 5% of trailing 20- and 60-day moves, per asset, over its own history), then
list what was knowable while it moved. Definition and both dated amendments are
in BIG_MOVES_REGISTRATION.md; this module implements Amendment 2 exactly.

Outputs data/big_moves/<asset>.json and data/big_moves/summary.json. Nothing here
asserts causation: "attributed" means knowable inside the move window.

Run:  python3 src/big_moves.py
"""
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "big_moves"

# asset key, series, kind (price -> log returns; spread -> level change), label, tier
ASSETS = [
    ("brent", "fred.DCOILBRENTEU", "price", "Brent", "daily"),
    ("wti", "fred.DCOILWTICO", "price", "WTI", "daily"),
    ("diesel_crack", "derived.diesel_crack", "spread", "Diesel crack", "daily"),
    ("wti_monthly", "fred.WTISPLC", "price", "WTI monthly (1946–)", "monthly"),   # Amendment 3
]
# Tier parameters (BIG_MOVES_REGISTRATION.md: Amendment 2 for daily, Amendment 3 for monthly).
TIERS = {
    "daily":   dict(windows=(20, 60), cluster_days=90, merge_days=60, attr_before_days=7, anticipated_lag=20,
                    unit="trading days"),
    "monthly": dict(windows=(3, 12), cluster_days=365, merge_days=180, attr_before_days=31, anticipated_lag=60,
                    unit="months"),
}
WINDOWS = TIERS["daily"]["windows"]          # kept for callers/tests that use the daily defaults
TOP_Q = 0.95                # |move| at or above this quantile of the asset's own history
CLUSTER_DAYS = 90
MERGE_DAYS = 60
ATTR_BEFORE_DAYS = 7
ANTICIPATED_LAG = 20


def series(conn, sid):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                     "ORDER BY obs_date, as_of", conn, params=(sid,))
    df = df.drop_duplicates("obs_date", keep="last")
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    return df.set_index("obs_date")["value"].astype(float)


def _trading_gap(index_pos, d1, d2):
    """Trading days between two dates, counted as positions in the asset's own observation index.
    §3 says 'within 60 trading days'; the as-computed code compared calendar days."""
    return index_pos[d2] - index_pos[d1]


def _episodes_registered(s, kind, tier):
    """BIG_MOVES_REGISTRATION.md §3 as written, with Amendment 1's onset/end and Amendment 4's
    reading of how the two windows combine (pooled, clustered once, no merge)."""
    T = TIERS[tier]
    lp = np.log(s[s > 0]) if kind == "price" else s
    index_pos = {d: i for i, d in enumerate(s.index)}
    CLUSTER_TD = 60 if tier == "daily" else T["cluster_days"]      # §3: 60 trading days (daily)

    # pool the qualifying dates of every window into ONE ordered set, each tagged with its window
    pooled = []
    thresholds = {}
    for W in T["windows"]:
        r = (lp - lp.shift(W)).dropna()
        if r.empty:
            continue
        thr = float(r.abs().quantile(TOP_Q))
        thresholds[W] = thr
        for d, v in r[r.abs() >= thr].items():
            pooled.append((d, W, float(v)))
    pooled.sort(key=lambda x: (x[0], x[1]))
    if not pooled:
        return []

    eps, i = [], 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and _trading_gap(index_pos, pooled[i][0], pooled[j + 1][0]) <= CLUSTER_TD:
            j += 1
        clus = pooled[i:j + 1]
        end, W, _ = max(clus, key=lambda x: abs(x[2]))              # Amendment 1: max |trailing return|
        up = max(clus, key=lambda x: abs(x[2]))[2] > 0
        win = s.loc[:end].iloc[-(W + 1):]
        onset = win.idxmin() if up else win.idxmax()                # Amendment 1: the price extreme
        chg = (s.loc[end] / s.loc[onset] - 1) * 100 if kind == "price" else s.loc[end] - s.loc[onset]
        eps.append(dict(window=W, windows=sorted({w for _, w, _ in clus}), onset=str(onset.date()),
                        end=str(end.date()), change=round(float(chg), 1), sign="+" if up else "-",
                        from_=round(float(s.loc[onset]), 2), to=round(float(s.loc[end]), 2),
                        threshold=round(thresholds[W], 3),
                        days=int((pd.Timestamp(end) - pd.Timestamp(onset)).days),
                        n_qualifying_dates=len({d for d, _, _ in clus})))
        i = j + 1
    return eps


def episodes_for(s, kind, tier="daily", variant="as_computed"):
    """Detect episodes per BIG_MOVES_REGISTRATION.md.

    Two variants, both published (Amendment 4). Neither moves a threshold, an attribution window or
    the top-5% cut; they differ ONLY in how qualifying dates are grouped into episodes.

    "registered"   -- §3 as written: the qualifying dates of BOTH windows are pooled into one
                      ordered set and clustered once, within 60 TRADING days of the episode's start.
                      No merge step. This is the primary result.
    "as_computed"  -- what src/big_moves.py has always done: cluster each window separately within
                      90 CALENDAR days, then merge same-sign episodes whose onsets are within 60
                      calendar days. The merge is not in §3; it was the device that combined the two
                      windows. Kept, labelled, so the published history is not silently retracted.

    The DEFAULT stays "as_computed" on purpose: src/walk.py (session B) calls this and its numbers
    must not move without B choosing it. data/big_moves/*.json publishes both and leads with
    "registered".
    """
    if variant not in ("registered", "as_computed"):
        raise ValueError(f"unknown variant {variant!r}")
    T = TIERS[tier]
    WINDOWS_, CLUSTER, MERGE = T["windows"], T["cluster_days"], T["merge_days"]
    if variant == "registered" and tier == "daily":
        return _episodes_registered(s, kind, tier)
    # The MONTHLY tier is not in dispute: Amendment 3 registers cluster 365 days + same-sign merge
    # within 180, which is exactly what TIERS["monthly"] implements. Its registered rule IS the
    # as-computed one, so both variants return the same episodes and neither is relabelled.
    if kind == "price":
        s = s[s > 0]
        lp = np.log(s)
    else:
        lp = s
    eps = []
    for W in WINDOWS_:
        r = (lp - lp.shift(W)).dropna()
        if r.empty:
            continue
        thr = float(r.abs().quantile(TOP_Q))
        q = r[r.abs() >= thr]
        dates = list(q.index)
        i = 0
        while i < len(dates):
            j = i
            while j + 1 < len(dates) and (dates[j + 1] - dates[i]).days <= CLUSTER:
                j += 1
            clus = q.loc[dates[i]:dates[j]]
            end = clus.abs().idxmax()
            up = bool(clus.loc[end] > 0)
            win = s.loc[:end].iloc[-(W + 1):]
            onset = win.idxmin() if up else win.idxmax()
            chg = (s.loc[end] / s.loc[onset] - 1) * 100 if kind == "price" else s.loc[end] - s.loc[onset]
            eps.append(dict(window=W, onset=str(onset.date()), end=str(end.date()),
                            change=round(float(chg), 1), sign="+" if up else "-",
                            from_=round(float(s.loc[onset]), 2), to=round(float(s.loc[end]), 2),
                            threshold=round(thr, 3)))
            i = j + 1
    eps.sort(key=lambda e: e["onset"])
    merged = []
    for e in eps:
        if merged and (pd.Timestamp(e["onset"]) - pd.Timestamp(merged[-1]["onset"])).days <= MERGE \
                and e["sign"] == merged[-1]["sign"]:
            m = merged[-1]
            m["windows"] = sorted(set(m["windows"] + [e["window"]]))
            if abs(e["change"]) > abs(m["change"]):
                m.update({k: e[k] for k in ("change", "end", "window", "from_", "to")})
        else:
            e["windows"] = [e["window"]]
            merged.append(e)
    for m in merged:
        m["days"] = int((pd.Timestamp(m["end"]) - pd.Timestamp(m["onset"])).days)
    return merged


def attribute(eps, ev, tier="daily"):
    """Attach every corpus event knowable in [onset - before, end] with its lag from onset."""
    before, ant = TIERS[tier]["attr_before_days"], TIERS[tier]["anticipated_lag"]
    for m in eps:
        on = pd.Timestamp(m["onset"]); en = pd.Timestamp(m["end"])
        hits = ev[(ev.event_date >= on - pd.Timedelta(days=before)) & (ev.event_date <= en)]
        m["events"] = [dict(id=r.event_id, date=str(r.event_date.date()), type=r.type, title=r.title,
                            lag_days=int((r.event_date - on).days),
                            anticipated=bool((r.event_date - on).days > ant))
                       for r in hits.itertuples()]
    return eps


def rates(eps, ev, s, tier="daily"):
    before = TIERS[tier]["attr_before_days"]
    n = len(eps)
    noev = sum(1 for m in eps if not m["events"])
    p_cls = {}
    for m in eps:
        for t in {e["type"] for e in m["events"]}:
            p_cls[t] = p_cls.get(t, 0) + 1
    p_big = {}
    for t, g in ev[ev.event_date >= s.index[0]].groupby("type"):
        k = sum(1 for d in g.event_date if any(
            pd.Timestamp(m["onset"]) - pd.Timedelta(days=before) <= d <= pd.Timestamp(m["end"]) for m in eps))
        p_big[t] = [int(k), int(len(g))]
    inwin = pd.Series(False, index=s.index)
    for m in eps:
        inwin.loc[pd.Timestamp(m["onset"]) - pd.Timedelta(days=before): m["end"]] = True
    base = round(float(inwin.mean() * 100), 1)
    return dict(n_episodes=n, no_identified_event=noev, everyday_base_rate_pct=base,
                p_class_given_big={t: [k, n] for t, k in p_cls.items()}, p_big_given_class=p_big)


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    ev = pd.read_sql("SELECT event_id, event_date, type, title FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])
    summary = {}
    for asset, sid, kind, label, tier in ASSETS:
        s = series(conn, sid)
        if s.empty:
            print(f"{label}: no data for {sid} (run src/fetch_wti_monthly.py)"); continue
        # Amendment 4: the REGISTERED rule is the primary result and sits at the top level; the
        # AS-COMPUTED rule is published beside it so the previous numbers are not silently retracted.
        eps = attribute(episodes_for(s, kind, tier, variant="registered"), ev, tier)
        alt = attribute(episodes_for(s, kind, tier, variant="as_computed"), ev, tier)
        alt_rates = rates(alt, ev, s, tier)
        res = dict(asset=asset, label=label, series=sid, kind=kind, tier=tier, unit=TIERS[tier]["unit"],
                   first=str(s.index[0].date()), last=str(s.index[-1].date()),
                   registration=("BIG_MOVES_REGISTRATION.md §3 as written (Amendments 1-2 for onset/end, "
                                 "Amendment 4 for the re-run): qualifying dates of both windows pooled and "
                                 "clustered once within 60 TRADING days, no merge step"
                                 if tier == "daily" else
                                 "BIG_MOVES_REGISTRATION.md (Amendment 3, monthly resolution)"),
                   variant="registered",
                   variant_note=("PRIMARY = the registered rule. `as_computed` below is what this file "
                                 "published before 2026-09-03: clustering at 90 CALENDAR days plus an "
                                 "unregistered same-sign merge within 60. Amendment 4 records why both "
                                 "are here." if tier == "daily" else
                                 "the monthly tier is not in dispute: Amendment 3 registers cluster 365 "
                                 "days + same-sign merge within 180, which is what the code does, so both "
                                 "variants are identical here"),
                   **rates(eps, ev, s, tier), episodes=eps,
                   as_computed=dict(variant="as_computed", **alt_rates, episodes=alt))
        json.dump(res, open(OUT / f"{asset}.json", "w"), indent=1)
        summary[asset] = {k: v for k, v in res.items()
                          if k not in ("episodes", "as_computed")}
        summary[asset]["as_computed"] = {k: v for k, v in alt_rates.items()}
        d = "" if tier != "daily" else (f"  (as-computed: {alt_rates['n_episodes']} episodes, "
                                        f"{alt_rates['no_identified_event']} with no identified event, "
                                        f"base {alt_rates['everyday_base_rate_pct']}%)")
        print(f"{label}: {res['n_episodes']} episodes, {res['no_identified_event']} with no identified event, "
              f"everyday base {res['everyday_base_rate_pct']}%{d}")
    json.dump(summary, open(OUT / "summary.json", "w"), indent=1)
    conn.close()
    return summary


if __name__ == "__main__":
    run()
