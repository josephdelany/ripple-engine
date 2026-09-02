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


def episodes_for(s, kind, tier="daily"):
    """Detect episodes per BIG_MOVES_REGISTRATION.md (Amendment 2 daily / Amendment 3 monthly). Pure; unit-tested."""
    T = TIERS[tier]
    WINDOWS_, CLUSTER, MERGE = T["windows"], T["cluster_days"], T["merge_days"]
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
        eps = attribute(episodes_for(s, kind, tier), ev, tier)
        res = dict(asset=asset, label=label, series=sid, kind=kind, tier=tier, unit=TIERS[tier]["unit"],
                   first=str(s.index[0].date()), last=str(s.index[-1].date()),
                   registration="BIG_MOVES_REGISTRATION.md (Amendment 2)" if tier == "daily" else "BIG_MOVES_REGISTRATION.md (Amendment 3, monthly resolution)",
                   **rates(eps, ev, s, tier), episodes=eps)
        json.dump(res, open(OUT / f"{asset}.json", "w"), indent=1)
        summary[asset] = {k: v for k, v in res.items() if k != "episodes"}
        print(f"{label}: {res['n_episodes']} episodes, {res['no_identified_event']} with no identified event, "
              f"everyday base {res['everyday_base_rate_pct']}%")
    json.dump(summary, open(OUT / "summary.json", "w"), indent=1)
    conn.close()
    return summary


if __name__ == "__main__":
    run()
