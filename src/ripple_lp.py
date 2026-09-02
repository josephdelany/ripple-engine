"""
ripple_lp.py -- the registered ripple study: lag-augmented local projections of every chain
node on the corpus shocks (RIPPLE_REGISTRATION.md, sealed at cbf4fdc + Amendments A, B).

WHAT IT DOES (plain language)
-----------------------------
For each node (crude, products, cracks, physical, gas, fertilizer, macro, equity proxies) and
each shock (the seven event classes; the pooled 'all' and 'tightening' sets; Big Moves onsets
as a market-defined comparison), one regression per horizon h:

    y[t+h] - y[t-1]  =  a_h + beta_h * S[t] + own lags (p+1, the lag augmentation) + controls[t-1] + u

beta_h is the ripple at h. Standard errors: Eicker-Huber-White HC1 (primary, per Montiel Olea &
Plagborg-Moller 2021) and Newey-West with bandwidth h (diagnostic, per Jorda 2005). Every
headline coefficient is compared with 500 pseudo-event draws matched on the VIX and GPR state
(Caldara-Iacoviello), so "turbulent times" cannot masquerade as transmission. Verdicts use the
registered words only: TRANSMITTING / NULL / INSUFFICIENT (Amendment B) for node x shock, and
CONSISTENT / INCONSISTENT / INDETERMINATE for the nine pre-stated expectations (section 6).

Nothing here changes a registered parameter; the constants below are copied from the
registration and the file says so next to each. Deterministic (seed 19900802).

Run:  python3 src/ripple_lp.py            -> data/ripple/*.json, data/ripple/SUMMARY.md
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "ripple"
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ---- registered constants (RIPPLE_REGISTRATION.md section, in brackets) --------------------
H_DAILY = [0, 1, 2, 5, 10, 20, 40, 60]        # [2.2]
H_WEEKLY = [0, 1, 2, 4, 8, 13, 26]            # [2.2]
H_MONTHLY = [0, 1, 2, 3, 6, 9, 12]            # [2.2]
P_DAILY, P_WEEKLY, P_MONTHLY = 5, 4, 6        # [2.3]  (+1 lag = augmentation)
MIN_N = 15                                    # [2.5]
CLUSTER_DAYS = 35                             # [Amendment A] = robustness.CLUSTER_DAYS
N_PLACEBO, EXCL_DAYS = 500, 30                # [2.5]
BH_Q = 0.10                                   # [2.9]
GAS_BREAK_PRE, GAS_BREAK_POST = "2009-02-06", "2009-02-13"   # [2.7] Ramberg & Parsons
SEED = 19900802
Z95, Z90 = 1.959964, 1.644854

CLASSES = ["chokepoint_disruption", "infrastructure_attack", "conflict_escalation",
           "opec_decision", "sanctions", "demand_shock", "policy_response"]
TIGHT = ["chokepoint_disruption", "infrastructure_attack", "conflict_escalation"]   # [Amendment A]
SHOCKS = CLASSES + ["all", "tightening"]                     # verdict-bearing shock sets
BM_SHOCKS = ["bigmove_up", "bigmove_down"]                    # descriptive only [2.5]

# node key, series_id, transform, hop, headline h, extra regressor (None | 'sp500')   [Table N + Amendment B]
NODES_DAILY = [
    ("brent", "fred.DCOILBRENTEU", "log", 0, 5, None),
    ("wti", "fred.DCOILWTICO", "log", 0, 5, None),
    ("brent_wti_spread", "derived.brent_wti_spread", "lvl", 0, 5, None),
    ("heating_oil_nyh", "fred.DHOILNYH", "log", 1, 20, None),
    ("gasoline_gulf", "fred.DGASUSGULF", "log", 1, 20, None),
    ("gasoline_nyh", "fred.DGASNYH", "log", 1, 20, None),
    ("jet_gulf", "fred.DJFUELUSGULF", "log", 1, 20, None),
    ("propane", "fred.DPROPANEMBTX", "log", 1, 20, None),
    ("diesel_crack", "derived.diesel_crack", "lvl", 1, 20, None),
    ("gasoline_crack", "derived.gasoline_crack", "lvl", 1, 20, None),
    ("henry_hub", "fred.DHHNGSP", "log", 3, 20, None),
    ("ttf", "yf.ttf", "log", 3, 20, None),
    ("t5yie", "fred.T5YIE", "pp", "x", 20, None),
    ("usd_broad", "fred.DTWEXBGS", "log", "x", 20, None),
    ("vix", "fred.VIXCLS", "log", "x", 20, None),
    ("hyg_proxy", "yf.hyg", "log", "x", 20, None),
    ("palladium", "yf.palladium", "log", "x", 20, None),       # Amendment B (retraction check)
    ("platinum", "yf.platinum", "log", "x", 20, None),
    ("sp500", "yf.sp500", "log", "x", 20, None),
    ("eq_fro", "yf.eq_fro", "log", "e", 5, "sp500"), ("eq_dht", "yf.eq_dht", "log", "e", 5, "sp500"),
    ("eq_tnk", "yf.eq_tnk", "log", "e", 5, "sp500"), ("eq_insw", "yf.eq_insw", "log", "e", 5, "sp500"),
    ("eq_stng", "yf.tankers", "log", "e", 5, "sp500"),
    ("eq_vlo", "yf.eq_vlo", "log", "e", 5, "sp500"), ("eq_mpc", "yf.eq_mpc", "log", "e", 5, "sp500"),
    ("eq_psx", "yf.eq_psx", "log", "e", 5, "sp500"),
    ("eq_cf", "yf.eq_cf", "log", "e", 5, "sp500"), ("eq_ntr", "yf.eq_ntr", "log", "e", 5, "sp500"),
    ("eq_mos", "yf.eq_mos", "log", "e", 5, "sp500"), ("eq_lng", "yf.eq_lng", "log", "e", 5, "sp500"),
] + [(f"transit_{s}", f"portwatch.{s}.n_tanker", "log1p", 2, 5, None)
     for s in ["hormuz", "bab_el_mandeb", "suez", "cape_of_good_hope", "malacca", "panama", "bosporus"]]

NODES_WEEKLY = [
    ("refinery_util", "eia.refinery_util", "pp", 2, 4, None),
    ("crude_stocks_xspr", "eia.crude_stocks_xspr", "log", 2, 4, None),
    ("distillate_stocks", "eia.distillate_stocks", "log", 2, 4, None),
    ("gasoline_stocks", "eia.gasoline_stocks", "log", 2, 4, None),
    ("crude_imports", "eia.crude_imports", "log", 2, 4, None),
]
NODES_MONTHLY = [
    ("m_crude_avg", "wb.crude_avg", "log", 0, 3, None),
    ("m_ngas_us", "wb.ngas_us", "log", 3, 3, None),
    ("m_ngas_eu", "wb.ngas_eu", "log", 3, 3, None),
    ("m_lng_japan", "wb.lng_japan", "log", 3, 3, None),
    ("m_ppi_nfert", "fred.PCU325311325311", "log", 4, 3, None),
    ("m_urea", "wb.urea", "log", 4, 3, None),
    ("m_dap", "wb.dap", "log", 4, 3, None),
    ("m_tsp", "wb.tsp", "log", 4, 3, None),
    ("m_potash", "wb.potash", "log", 4, 3, None),
    ("m_coal_aus", "wb.coal_aus", "log", 4, 3, None),
]
SIX = {  # propagation_edges 'validated' rows -> node key   [Amendment B]
    "Brent oil": "brent", "Heating oil": "heating_oil_nyh", "5Y breakeven": "t5yie",
    "Palladium": "palladium", "S&P 500": "sp500", "Platinum": "platinum",
}


# =============================================================================================
# data
# =============================================================================================

def load_series(conn, sid):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? ORDER BY obs_date",
                     conn, params=(sid,))
    s = pd.Series(df["value"].to_numpy(float), index=pd.to_datetime(df["obs_date"]))
    return s[~s.index.duplicated(keep="last")]


def transform(s, how):
    if how == "log":
        return 100.0 * np.log(s.where(s > 0))
    if how == "log1p":
        return 100.0 * np.log1p(s.where(s >= 0))
    return s.astype(float)


def shift(a, k):
    """Positional shift with NaN fill: shift(a,1)[t] = a[t-1]; shift(a,-h)[t] = a[t+h]."""
    out = np.full_like(a, np.nan, dtype=float)
    if k > 0:
        out[k:] = a[:-k]
    elif k < 0:
        out[:k] = a[-k:]
    else:
        out[:] = a
    return out


def cluster_first_dates(dates, window_days=CLUSTER_DAYS):
    """Chain rule as robustness.assign_clusters: consecutive dates within `window_days` of the
    previous one belong to the same cluster; return the first date of each cluster."""
    dates = sorted(set(pd.to_datetime(dates)))
    keep, last = [], None
    for d in dates:
        if last is None or (d - last).days > window_days:
            keep.append(d)
        last = d
    return keep


def dummies_for(index, dates):
    """0/1 array on `index` with 1 at the first index date >= each event date."""
    S = np.zeros(len(index))
    pos = index.searchsorted(pd.DatetimeIndex(dates))
    pos = pos[pos < len(index)]
    S[pos] = 1.0
    return S


# =============================================================================================
# estimator
# =============================================================================================

def ols(X, y, L):
    """OLS with HC1 (primary) and Newey-West(L) (diagnostic) covariances. Returns dict."""
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    e = y - X @ b
    Xe = X * e[:, None]
    meat = Xe.T @ Xe
    V_hc = XtX_inv @ meat @ XtX_inv * (n / max(n - k, 1))
    S = meat.copy()
    for l in range(1, min(L, n - 1) + 1):
        w = 1.0 - l / (L + 1.0)
        G = Xe[l:].T @ Xe[:-l]
        S += w * (G + G.T)
    V_nw = XtX_inv @ S @ XtX_inv
    return {"b": b, "se_hc": np.sqrt(np.maximum(np.diag(V_hc), 0)),
            "se_nw": np.sqrt(np.maximum(np.diag(V_nw), 0)), "V_hc": V_hc, "n": n, "e": e}


def lp_design(y, S, h, p, ctrls, extra=None):
    """Registered regression [2.1]: dep = y[t+h]-y[t-1]; regressors 1, S[t], own lags 1..p+1 of
    dy, controls (already lagged to t-1), optional extra (long change of a control series)."""
    dep = shift(y, -h) - shift(y, 1)
    dy = y - shift(y, 1)
    cols = [np.ones(len(y)), S] + [shift(dy, l) for l in range(1, p + 2)] + list(ctrls)
    if extra is not None:
        cols.append(shift(extra, -h) - shift(extra, 1))
    X = np.column_stack(cols)
    mask = np.isfinite(dep) & np.all(np.isfinite(X), axis=1)
    return X, dep, mask


def run_lp(y, S, horizons, p, ctrls, extra=None, sample=None):
    """IRF over horizons. `sample` = boolean array restricting rows (regimes). Returns list of
    per-h dicts and the number of events in the estimation sample at h=headline."""
    out = []
    for h in horizons:
        X, dep, mask = lp_design(y, S, h, p, ctrls, extra)
        if sample is not None:
            mask &= sample
        n_ev = int(np.nansum(S[mask])) if set(np.unique(S[mask])) <= {0.0, 1.0} else int(np.sum(S[mask] != 0))
        if mask.sum() < 50 or n_ev == 0:
            out.append({"h": h, "beta": None, "n_events": n_ev, "T": int(mask.sum())})
            continue
        r = ols(X[mask], dep[mask], L=h)
        b, se, senw = float(r["b"][1]), float(r["se_hc"][1]), float(r["se_nw"][1])
        out.append({"h": h, "beta": round(b, 4), "se_ehw": round(se, 4), "se_nw": round(senw, 4),
                    "lo95": round(b - Z95 * se, 4), "hi95": round(b + Z95 * se, 4),
                    "lo90": round(b - Z90 * se, 4), "hi90": round(b + Z90 * se, 4),
                    "z_ehw": round(b / se, 3) if se > 0 else None,
                    "p_ehw": round(float(2 * (1 - _phi(abs(b / se)))), 4) if se > 0 else None,
                    "nw_covers_zero": bool(abs(b) < Z95 * senw) if senw > 0 else None,
                    "ehw_covers_zero": bool(abs(b) < Z95 * se) if se > 0 else None,
                    "n_events": n_ev, "T": int(mask.sum())})
    return out


def _phi(z):
    from math import erf, sqrt
    return 0.5 * (1 + erf(z / sqrt(2)))


def fwl_beta(Z_masked, ZtZinv, ytil, rows_idx):
    """beta on a 0/1 dummy at masked rows `rows_idx`, partialling out Z (Frisch-Waugh-Lovell).
    S'ytil = sum ytil[rows]; S'S - (Z'S)' ZtZinv (Z'S)."""
    zs = Z_masked[rows_idx].sum(axis=0)
    denom = len(rows_idx) - zs @ ZtZinv @ zs
    if denom <= 1e-9:
        return np.nan
    return float(ytil[rows_idx].sum() / denom)


def placebo(y, S, h, p, ctrls, extra, event_pos, buckets, pool_by_bucket, rng, sample=None):
    """Percentile of the real beta_h in N_PLACEBO pseudo draws matched on (VIX decile, GPR decile)
    at t-1 [2.5]. Returns dict or None if fewer than MIN_N events."""
    X, dep, mask = lp_design(y, S, h, p, ctrls, extra)
    if sample is not None:
        mask &= sample
    rows = np.flatnonzero(mask)
    row_of = {r: i for i, r in enumerate(rows)}
    # an event enters the placebo only if it is in the estimation sample AND has a state bucket
    # (derived.vix_pct starts 1990-12; the GPR 5y rank needs 500 days): unbucketed events are counted
    ev_in = [q for q in event_pos if q in row_of]
    ev_keep = [q for q in ev_in if q in buckets]
    n_unbucketed = len(ev_in) - len(ev_keep)
    ev_rows = [row_of[q] for q in ev_keep]
    if len(ev_rows) < MIN_N:
        return None
    Z = np.delete(X[mask], 1, axis=1)
    ZtZinv = np.linalg.pinv(Z.T @ Z)
    yy = dep[mask]
    ytil = yy - Z @ (ZtZinv @ (Z.T @ yy))
    real = fwl_beta(Z, ZtZinv, ytil, np.array(ev_rows))
    ev_b = [buckets[q] for q in ev_keep]
    pseudo, fallback = [], 0
    pools = {}
    for bkt in set(ev_b):
        cand = [row_of[q] for q in pool_by_bucket.get(bkt, []) if q in row_of]
        if len(cand) < 5:                                   # fall back to the VIX decile only
            fallback += 1
            cand = [row_of[q] for k, qs in pool_by_bucket.items() if k[0] == bkt[0] for q in qs if q in row_of]
        pools[bkt] = np.array(cand) if cand else np.array([], dtype=int)
    for _ in range(N_PLACEBO):
        draw = []
        for bkt in ev_b:
            pool = pools[bkt]
            if len(pool) == 0:
                continue
            draw.append(int(pool[rng.integers(0, len(pool))]))
        if len(draw) < MIN_N:
            continue
        pseudo.append(fwl_beta(Z, ZtZinv, ytil, np.array(draw)))
    pseudo = np.array([v for v in pseudo if np.isfinite(v)])
    if len(pseudo) < 100:
        return None
    pct = float(np.mean(pseudo < real) * 100)
    return {"beta_real": round(real, 4), "pseudo_p2_5": round(float(np.percentile(pseudo, 2.5)), 4),
            "pseudo_p97_5": round(float(np.percentile(pseudo, 97.5)), 4),
            "percentile": round(pct, 1), "beyond_state": bool(pct < 2.5 or pct > 97.5),
            "n_pseudo": int(len(pseudo)), "buckets_fallback_to_vix_only": fallback,
            "n_events_matched": len(ev_rows), "n_events_unbucketed": n_unbucketed}


def bh_flags(pvals, q=BH_Q):
    """Benjamini-Hochberg at q within one family; returns list of bools (rejected)."""
    idx = [i for i, p in enumerate(pvals) if p is not None]
    m = len(idx)
    if m == 0:
        return [False] * len(pvals)
    order = sorted(idx, key=lambda i: pvals[i])
    thresh, kmax = [(pvals[i], (r + 1) / m * q) for r, i in enumerate(order)], -1
    for r, (p, t) in enumerate(thresh):
        if p <= t:
            kmax = r
    rejected = set(order[: kmax + 1]) if kmax >= 0 else set()
    return [i in rejected for i in range(len(pvals))]


def verdict(head, plac, n_events):
    """Amendment B: TRANSMITTING / NULL / INSUFFICIENT (+ FRAGILE flag counted as null)."""
    if n_events < MIN_N or head is None or head.get("beta") is None:
        return "INSUFFICIENT", False
    ehw_excl = head["ehw_covers_zero"] is False
    nw_agrees = head["nw_covers_zero"] is False
    beyond = bool(plac and plac["beyond_state"])
    fragile = ehw_excl and not nw_agrees
    if ehw_excl and nw_agrees and beyond:
        return "TRANSMITTING", False
    return "NULL", fragile


# =============================================================================================
# frames
# =============================================================================================

def build_daily(conn):
    brent = load_series(conn, "fred.DCOILBRENTEU")
    idx = brent.index
    F = {"idx": idx, "nodes": {}}
    for key, sid, how, hop, hh, extra in NODES_DAILY:
        s = load_series(conn, sid)
        F["nodes"][key] = {"y": transform(s.reindex(idx), how).to_numpy(float), "sid": sid, "hop": hop,
                           "headline": hh, "extra": extra, "how": how}
    vix = load_series(conn, "fred.VIXCLS").reindex(idx)
    lvix = 100 * np.log(vix)
    F["ctrl_vix"] = (lvix.shift(1) - lvix.shift(6)).to_numpy(float)          # [2.1] change over t-6..t-1
    gpr = load_series(conn, "gpr.GPRD_THREAT")
    gpr30 = gpr.rolling(30, min_periods=20).mean()
    g8 = gpr30.copy(); g8.index = g8.index + pd.Timedelta(days=8)             # knowable at t-8 [1.8]
    F["ctrl_gpr"] = (100 * np.log(g8.reindex(idx))).to_numpy(float)
    F["ctrls"] = [F["ctrl_vix"], F["ctrl_gpr"]]
    F["sp500"] = F["nodes"]["sp500"]["y"]
    F["brent"] = F["nodes"]["brent"]["y"]
    # placebo state buckets at t-1: VIX 5y percentile decile (derived.vix_pct) and GPR30 5y-rank decile
    vp = load_series(conn, "derived.vix_pct").reindex(idx).shift(1)
    g30 = gpr30.reindex(idx)
    gp = g30.rolling(1260, min_periods=500).rank(pct=True).shift(1) * 100
    F["vix_dec"] = np.floor(vp.to_numpy(float) / 10).clip(0, 9)
    F["gpr_dec"] = np.floor(gp.to_numpy(float) / 10).clip(0, 9)
    F["vix_pct_t1"] = vp.to_numpy(float)
    return F


def build_weekly(conn):
    base = load_series(conn, "eia.crude_stocks_xspr")
    idx = base.index
    F = {"idx": idx, "nodes": {}}
    for key, sid, how, hop, hh, extra in NODES_WEEKLY:
        s = load_series(conn, sid)
        F["nodes"][key] = {"y": transform(s.reindex(idx), how).to_numpy(float), "sid": sid, "hop": hop,
                           "headline": hh, "extra": extra, "how": how}
    lvix = 100 * np.log(load_series(conn, "fred.VIXCLS")).reindex(idx, method="ffill")
    F["ctrl_vix"] = (lvix.shift(1) - lvix.shift(2)).to_numpy(float)
    gpr30 = load_series(conn, "gpr.GPRD_THREAT").rolling(30, min_periods=20).mean()
    g8 = gpr30.copy(); g8.index = g8.index + pd.Timedelta(days=8)
    F["ctrl_gpr"] = (100 * np.log(g8.reindex(idx, method="ffill"))).shift(1).to_numpy(float)
    F["ctrls"] = [F["ctrl_vix"], F["ctrl_gpr"]]
    brent = 100 * np.log(load_series(conn, "fred.DCOILBRENTEU")).reindex(idx, method="ffill")
    F["brent"] = brent.to_numpy(float)
    return F


def build_monthly(conn):
    base = load_series(conn, "wb.crude_avg")
    idx = base.index
    F = {"idx": idx, "nodes": {}}
    for key, sid, how, hop, hh, extra in NODES_MONTHLY:
        s = load_series(conn, sid)
        s.index = s.index.to_period("M").to_timestamp()
        F["nodes"][key] = {"y": transform(s.reindex(idx), how).to_numpy(float), "sid": sid, "hop": hop,
                           "headline": hh, "extra": extra, "how": how}
    crude = F["nodes"]["m_crude_avg"]["y"]
    F["brent"] = crude
    gpr = load_series(conn, "gpr.GPRD")
    gm = 100 * np.log(gpr.resample("MS").mean()).reindex(idx)
    F["ctrls"] = [shift(crude - shift(crude, 1), 1), gm.shift(1).to_numpy(float)]   # [2.1] monthly controls
    return F


# =============================================================================================
# shocks
# =============================================================================================

def load_events(conn):
    ev = pd.read_sql("SELECT event_id, event_date, type, date_precision, surprise FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])
    return ev


def shock_dates(ev, precision=("day",)):
    e = ev[ev["date_precision"].isin(precision)]
    sets = {c: cluster_first_dates(e.loc[e["type"] == c, "event_date"]) for c in CLASSES}
    sets["all"] = cluster_first_dates(e["event_date"])
    sets["tightening"] = cluster_first_dates(e.loc[e["type"].isin(TIGHT), "event_date"])
    return sets


def bigmove_dates():
    path = ROOT / "data" / "big_moves" / "brent.json"
    if not path.exists():
        return {}
    eps = json.loads(path.read_text()).get("episodes", [])
    return {"bigmove_up": [pd.Timestamp(e["onset"]) for e in eps if e.get("sign") == "+"],
            "bigmove_down": [pd.Timestamp(e["onset"]) for e in eps if e.get("sign") == "-"]}


# =============================================================================================
# the study
# =============================================================================================

def study_frame(F, shock_sets, horizons, p, all_event_dates, rng, freq_name, specs=("total", "crude_conditioned"),
                do_placebo=True, sample=None, sample_label=None):
    idx = F["idx"]
    results = []
    # placebo pools: non-event rows (>= EXCL_DAYS from any event) by (vix_dec, gpr_dec)
    pool_by_bucket, buckets = {}, {}
    if do_placebo and "vix_dec" in F:
        ev_idx = pd.DatetimeIndex(sorted(set(all_event_dates)))
        far = np.ones(len(idx), dtype=bool)
        for d in ev_idx:
            lo, hi = idx.searchsorted(d - pd.Timedelta(days=EXCL_DAYS)), idx.searchsorted(d + pd.Timedelta(days=EXCL_DAYS))
            far[lo:hi] = False
        for q in range(len(idx)):
            v, g = F["vix_dec"][q], F["gpr_dec"][q]
            if np.isfinite(v) and np.isfinite(g):
                buckets[q] = (int(v), int(g))
                if far[q]:
                    pool_by_bucket.setdefault((int(v), int(g)), []).append(q)
    for key, node in F["nodes"].items():
        y = node["y"]
        extra_series = F["sp500"] if node["extra"] == "sp500" else None
        node_rows = []
        for sname, dates in shock_sets.items():
            S = dummies_for(idx, dates) if not isinstance(dates, np.ndarray) else dates
            event_pos = [int(q) for q in idx.searchsorted(pd.DatetimeIndex(dates)) if q < len(idx)] \
                if not isinstance(dates, np.ndarray) else list(np.flatnonzero(dates != 0))
            for spec in specs:
                if spec == "crude_conditioned" and (node["hop"] == 0 or key.startswith("m_crude")):
                    continue
                extra = extra_series
                if spec == "crude_conditioned":
                    extra = F["brent"] if extra is None else None   # equities: S&P control only
                    if extra is None:
                        continue
                irf = run_lp(y, S, horizons, p, F["ctrls"], extra, sample)
                head = next((r for r in irf if r["h"] == node["headline"]), None)
                n_ev = head["n_events"] if head else 0
                plac = None
                if do_placebo and spec == "total" and sname in SHOCKS and n_ev >= MIN_N and "vix_dec" in F:
                    plac = placebo(y, S, node["headline"], p, F["ctrls"], extra, event_pos, buckets,
                                   pool_by_bucket, rng, sample)
                v, fragile = verdict(head, plac, n_ev) if (spec == "total" and sname in SHOCKS) else (None, False)
                node_rows.append({"node": key, "series_id": node["sid"], "hop": node["hop"], "freq": freq_name,
                                  "transform": node["how"], "shock": sname, "spec": spec,
                                  "sample": sample_label or "full", "headline_h": node["headline"],
                                  "n_events": n_ev, "irf": irf, "placebo": plac,
                                  "verdict": v, "fragile": fragile})
        # BH within the node's family: verdict-bearing shocks, total spec, headline h   [2.9]
        fam = [r for r in node_rows if r["spec"] == "total" and r["shock"] in SHOCKS]
        pv = [next((x.get("p_ehw") for x in r["irf"] if x["h"] == r["headline_h"]), None) for r in fam]
        for r, flag in zip(fam, bh_flags(pv)):
            r["bh_q10_reject"] = flag
        results.extend(node_rows)
    return results


def passthrough(Fd, Fw, conn):
    """[2.6] uncensored sign split at the crude->product hop. Daily spot leg h=5,10,20; weekly
    retail leg (GASREGW) h=4,8. W = beta_plus - beta_minus with HC1 Wald."""
    out = {"note": "slope-based symmetry test (Kilian & Vigfusson 2011 caveat: informative about slopes, "
                   "not the shape of the nonlinear response); never censored: both signs enter together",
           "daily_spot": [], "weekly_retail": []}
    idx = Fd["idx"]
    dB = Fd["brent"] - shift(Fd["brent"], 1)
    dpos, dneg = np.where(dB > 0, dB, 0.0), np.where(dB < 0, dB, 0.0)
    dpos[~np.isfinite(dB)] = np.nan; dneg[~np.isfinite(dB)] = np.nan
    for key in ["heating_oil_nyh", "gasoline_gulf", "gasoline_nyh", "jet_gulf", "propane"]:
        y = Fd["nodes"][key]["y"]
        for h in [5, 10, 20]:
            dep = shift(y, -h) - shift(y, 1)
            dy = y - shift(y, 1)
            cols = [np.ones(len(y)), dpos, dneg] + [shift(dy, l) for l in range(1, P_DAILY + 2)] + Fd["ctrls"]
            X = np.column_stack(cols)
            m = np.isfinite(dep) & np.all(np.isfinite(X), axis=1)
            r = ols(X[m], dep[m], L=h)
            bp, bn = r["b"][1], r["b"][2]
            V = r["V_hc"]
            var_w = V[1, 1] + V[2, 2] - 2 * V[1, 2]
            W = bp - bn
            z = W / np.sqrt(var_w) if var_w > 0 else np.nan
            out["daily_spot"].append({"node": key, "h": h, "beta_plus": round(float(bp), 4),
                                      "beta_minus": round(float(bn), 4), "se_plus": round(float(r["se_hc"][1]), 4),
                                      "se_minus": round(float(r["se_hc"][2]), 4), "W": round(float(W), 4),
                                      "z_W": round(float(z), 3), "p_W": round(float(2 * (1 - _phi(abs(z)))), 4),
                                      "asymmetric_at_5pct": bool(abs(z) > Z95), "T": int(m.sum())})
    # weekly retail leg
    gas = load_series(conn, "fred.GASREGW")
    widx = gas.index
    yg = (100 * np.log(gas)).to_numpy(float)
    brent_w = (100 * np.log(load_series(conn, "fred.DCOILBRENTEU"))).reindex(widx, method="ffill").to_numpy(float)
    dBw = brent_w - shift(brent_w, 1)
    wpos, wneg = np.where(dBw > 0, dBw, 0.0), np.where(dBw < 0, dBw, 0.0)
    wpos[~np.isfinite(dBw)] = np.nan; wneg[~np.isfinite(dBw)] = np.nan
    lvix = (100 * np.log(load_series(conn, "fred.VIXCLS"))).reindex(widx, method="ffill")
    cv = (lvix.shift(1) - lvix.shift(2)).to_numpy(float)
    for h in [4, 8]:
        dep = shift(yg, -h) - shift(yg, 1)
        dy = yg - shift(yg, 1)
        cols = [np.ones(len(yg)), wpos, wneg] + [shift(dy, l) for l in range(1, P_WEEKLY + 2)] + [cv]
        X = np.column_stack(cols)
        m = np.isfinite(dep) & np.all(np.isfinite(X), axis=1)
        r = ols(X[m], dep[m], L=h)
        bp, bn = r["b"][1], r["b"][2]; V = r["V_hc"]
        var_w = V[1, 1] + V[2, 2] - 2 * V[1, 2]; W = bp - bn
        z = W / np.sqrt(var_w) if var_w > 0 else np.nan
        out["weekly_retail"].append({"node": "retail_gasoline_GASREGW", "h_weeks": h,
                                     "beta_plus": round(float(bp), 4), "beta_minus": round(float(bn), 4),
                                     "W": round(float(W), 4), "z_W": round(float(z), 3),
                                     "p_W": round(float(2 * (1 - _phi(abs(z)))), 4),
                                     "increases_pass_faster": bool(W > 0 and abs(z) > Z95),
                                     "asymmetric_at_5pct": bool(abs(z) > Z95), "T": int(m.sum())})
    return out


def external_checks(Fd, Fm, conn, shock_sets_daily, shock_sets_monthly):
    """[2.8] Kaenzig daily PC on Brent; B-H monthly shocks on Pink Sheet crude; correlations."""
    out = {"note": "documented sanity checks, not gates [2.8]"}
    idx = Fd["idx"]
    k = load_series(conn, "kanzig.surprise_daily_pc").reindex(idx).fillna(0.0).to_numpy(float)
    irf = run_lp(Fd["brent"], k, H_DAILY, P_DAILY, Fd["ctrls"])
    out["kanzig_daily_pc_on_brent"] = {"irf": irf, "n_announcement_days": int(np.sum(k != 0)),
                                       "unit": "% Brent per unit of the futures-surprise PC"}
    opec = next(r for r in irf if r["h"] == 5)
    out["kanzig_h5"] = opec
    # monthly correlation: our opec_decision count vs |monthly surprise|
    midx = Fm["idx"]
    ks = load_series(conn, "kanzig.surprise_monthly"); ks.index = ks.index.to_period("M").to_timestamp()
    ks = ks.reindex(midx)
    cnt = pd.Series(shock_sets_monthly["opec_decision"], index=midx)
    m = ks.notna() & (ks.index >= "1983-04-01")
    out["corr_opec_count_vs_abs_kanzig_monthly"] = {"r": round(float(np.corrcoef(cnt[m], ks[m].abs())[0, 1]), 3),
                                                    "n_months": int(m.sum())}
    bh_s = load_series(conn, "bh.supply_shock"); bh_s.index = bh_s.index.to_period("M").to_timestamp()
    bh_i = load_series(conn, "bh.inventory_demand_shock"); bh_i.index = bh_i.index.to_period("M").to_timestamp()
    crude = Fm["nodes"]["m_crude_avg"]["y"]
    for name, s in [("bh_supply_shock", bh_s), ("bh_inventory_demand_shock", bh_i)]:
        x = s.reindex(midx).to_numpy(float)
        if np.isfinite(x).sum() > 100:
            out[f"{name}_on_pinksheet_crude"] = {"irf": run_lp(crude, np.nan_to_num(x, nan=0.0), H_MONTHLY, P_MONTHLY, Fm["ctrls"],
                                                               sample=np.isfinite(x)),
                                                 "unit": "% crude per unit shock (posterior median)"}
    tight = pd.Series(shock_sets_monthly["tightening"], index=midx)
    xs = bh_s.reindex(midx)
    m = xs.notna()
    out["corr_tightening_count_vs_bh_supply_shock"] = {"r": round(float(np.corrcoef(tight[m], xs[m])[0, 1]), 3),
                                                       "n_months": int(m.sum()),
                                                       "sign_note": "B-H supply shock: negative = production down"}
    return out


def exogeneity(Fd, shock_sets):
    """[2.5] pre-window y[t-1]-y[t-6] of Brent by shock set, HC1 band (difference-in-means)."""
    out = {}
    y = Fd["brent"]; idx = Fd["idx"]
    pre = shift(y, 1) - shift(y, 6)
    for sname, dates in shock_sets.items():
        S = dummies_for(idx, dates)
        m = np.isfinite(pre)
        X = np.column_stack([np.ones(m.sum()), S[m]])
        r = ols(X, pre[m], L=0)
        b, se = float(r["b"][1]), float(r["se_hc"][1])
        out[sname] = {"pre_window_mean_pct": round(b, 3), "se": round(se, 3), "n_events": int(S[m].sum()),
                      "flat": bool(abs(b) < Z95 * se), "label": "" if abs(b) < Z95 * se else "ANTICIPATED-IN-PRICE"}
    return out


# =============================================================================================
# summary (the nine expectations + tallies + retraction of the six)
# =============================================================================================

def _find(rows, node, shock, spec="total", sample="full"):
    return next((r for r in rows if r["node"] == node and r["shock"] == shock and r["spec"] == spec
                 and r["sample"] == sample), None)


def _at(row, h):
    if not row:
        return None
    return next((x for x in row["irf"] if x["h"] == h and x.get("beta") is not None), None)


def _sign_verdict(pt, expected_sign):
    """CONSISTENT if 95% band excludes zero on the expected side; INCONSISTENT if excludes zero on the
    other side; INDETERMINATE if the band covers zero."""
    if pt is None:
        return "INDETERMINATE (no estimate)"
    if pt["ehw_covers_zero"]:
        return "INDETERMINATE"
    return "CONSISTENT" if np.sign(pt["beta"]) == expected_sign else "INCONSISTENT"


def _fmt(pt, unit="%"):
    if pt is None:
        return "no estimate"
    return f"{pt['beta']:+.3f}{unit} [95% {pt['lo95']:+.3f}, {pt['hi95']:+.3f}] n={pt['n_events']}"


def summarize(rows, rows_gas, rows_gas_m, pt, ext, exo, retraction, tallies, meta):
    L = ["# RIPPLE SUMMARY — computed once, as registered", ""]
    L.append(f"*{meta['when']}. Registration RIPPLE_REGISTRATION.md (sealed cbf4fdc; Amendments A, B). "
             f"Numbers below are read from data/ripple/*.json written by src/ripple_lp.py in this run. "
             f"Vocabulary: node×shock verdicts are TRANSMITTING / NULL / INSUFFICIENT; the nine expectations are "
             f"CONSISTENT / INCONSISTENT / INDETERMINATE. Nothing was re-run or re-labelled after reading.*")
    L.append("")
    L.append("## Tally (primary spec, headline horizon, verdict-bearing shocks)")
    L.append("| verdict | count |")
    L.append("|---|---|")
    for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]:
        L.append(f"| {k} | {tallies[k]} |")
    L.append(f"| of the NULL, FRAGILE (EHW and Newey–West disagree) | {tallies['FRAGILE']} |")
    L.append(f"| node×shock cells | {tallies['cells']} |")
    L.append("")
    L.append(f"Base rate: {tallies['TRANSMITTING']}/{tallies['cells']} = "
             f"{100*tallies['TRANSMITTING']/max(tallies['cells'],1):.1f}% of cells transmit. Under the null every cell "
             f"has a 5% chance of an EHW band excluding zero, a further 5% chance of a placebo percentile outside the "
             f"central 95%, and the two are not independent (both are driven by the same β); the expected count under "
             f"no transmission anywhere is therefore between {0.0025*tallies['cells']:.0f} and {0.05*tallies['cells']:.0f} cells. "
             f"Read the tally against that range, not against zero.")
    L.append("")
    L.append("### Transmitting cells")
    tr = [r for r in rows if r.get("verdict") == "TRANSMITTING"]
    if not tr:
        L.append("None.")
    for r in sorted(tr, key=lambda r: (str(r["hop"]), r["node"])):
        h = _at(r, r["headline_h"])
        L.append(f"- hop {r['hop']} **{r['node']}** ← {r['shock']} at h={r['headline_h']}: {_fmt(h, '' if r['transform'] in ('pp','lvl') else '%')}; "
                 f"placebo percentile {r['placebo']['percentile']} (pseudo 95% band [{r['placebo']['pseudo_p2_5']}, {r['placebo']['pseudo_p97_5']}])"
                 + ("; BH q=.10 reject" if r.get("bh_q10_reject") else "; BH q=.10 not rejected"))
    L.append("")
    L.append("## Retraction check of the six `validated` propagation edges (Amendment B)")
    L.append("| edge (node) | β at h=20, all-shock, VIX≥median | n | placebo pct | verdict | status |")
    L.append("|---|---|---|---|---|---|")
    for name, rr in retraction.items():
        L.append(f"| {name} ({rr['node']}) | {rr['beta']} | {rr['n_events']} | {rr['placebo_pct']} | {rr['verdict']} | **{rr['status']}** |")
    pal = retraction.get("Palladium", {})
    L.append("")
    L.append("**Palladium, stated as Joe's Ruling 1 requires.** The re-test result is published above "
             f"as computed: {pal.get('beta', 'n/a')}, placebo percentile {pal.get('placebo_pct')}, "
             f"verdict {pal.get('verdict')}. In the same breath: palladium is **not on the oil chain** — "
             "it is a macro cross-check node, and no mechanism in this study predicts a crude shock "
             "reaching it. And one survivor out of six re-tested edges is exactly what this base rate "
             "produces by chance: at a 5% band and a 5% placebo tail, one hit in six is consistent with "
             "noise. **This is not a finding and must not be surfaced as one.** It is published because "
             "the re-test was registered before it ran and every result of a registered test is "
             "published, including the awkward one.")
    L.append("")
    L.append("## The nine expectations (§6)")
    # E-1
    L.append("**E-1 (crude, h=5).**")
    for c, sgn in [("chokepoint_disruption", 1), ("infrastructure_attack", 1), ("conflict_escalation", 1), ("demand_shock", -1)]:
        p = _at(_find(rows, "brent", c), 5)
        L.append(f"- Brent ← {c}: {_fmt(p)} → {_sign_verdict(p, sgn)}")
    # E-2
    L.append("**E-2 (pass-through completeness, h=20, shock = all).**")
    pc = _at(_find(rows, "brent", "all"), 20)
    for prod in ["heating_oil_nyh", "gasoline_gulf"]:
        pp = _at(_find(rows, prod, "all"), 20)
        if pc and pp and pc["beta"] and not pc["ehw_covers_zero"]:
            ratio = pp["beta"] / pc["beta"]
            v = "CONSISTENT" if (0.5 <= ratio <= 1.5 and np.sign(pp["beta"]) == np.sign(pc["beta"])) else "INCONSISTENT"
            L.append(f"- {prod}: {_fmt(pp)} vs Brent {_fmt(pc)}; ratio {ratio:.2f} → {v}")
        else:
            L.append(f"- {prod}: {_fmt(pp)} vs Brent {_fmt(pc)} → INDETERMINATE (crude band covers zero)")
    for crk in ["diesel_crack", "gasoline_crack"]:
        pk = _at(_find(rows, crk, "all"), 20)
        L.append(f"- {crk} (USD/bbl): {_fmt(pk, '')} → {'CONSISTENT (transitory: band covers zero)' if pk and pk['ehw_covers_zero'] else ('INCONSISTENT' if pk else 'INDETERMINATE')}")
    # E-3
    L.append("**E-3 (asymmetry at the crude→product hop, §2.6).**")
    ds = pt["daily_spot"]
    asym = [d for d in ds if d["asymmetric_at_5pct"]]
    L.append(f"- daily spot legs: {len(asym)} of {len(ds)} (node, h) tests reject symmetry at 5% → "
             f"{'CONSISTENT (no asymmetry at the spot hop)' if len(asym) == 0 else ('INCONSISTENT' if len(asym) > len(ds)/2 else 'INDETERMINATE (some rejections)')}")
    for d in ds:
        L.append(f"  - {d['node']} h={d['h']}: β⁺ {d['beta_plus']:+.3f} β⁻ {d['beta_minus']:+.3f} W {d['W']:+.3f} (p={d['p_W']})")
    for w in pt["weekly_retail"]:
        L.append(f"- retail weekly h={w['h_weeks']}w: β⁺ {w['beta_plus']:+.3f} β⁻ {w['beta_minus']:+.3f} W {w['W']:+.3f} (p={w['p_W']}) → "
                 f"{'CONSISTENT (increases pass faster)' if w['increases_pass_faster'] else ('INCONSISTENT (decreases pass faster)' if w['asymmetric_at_5pct'] else 'INDETERMINATE')}")
    # E-4
    L.append("**E-4 (gas regime, Henry Hub ← tightening/all, h=20; pre ≤ 2009-02-06 vs post ≥ 2009-02-13).**")
    for sh in ["tightening", "all"]:
        pre = _at(_find(rows_gas, "henry_hub", sh, sample="pre_2009-02-06"), 20)
        post = _at(_find(rows_gas, "henry_hub", sh, sample="post_2009-02-13"), 20)
        if pre and post and pre["n_events"] >= MIN_N and post["n_events"] >= MIN_N:
            v = ("CONSISTENT" if (pre["beta"] > post["beta"] and not pre["ehw_covers_zero"] and pre["beta"] > 0 and post["ehw_covers_zero"])
                 else ("INCONSISTENT" if (post["beta"] > pre["beta"] and not post["ehw_covers_zero"]) else "INDETERMINATE"))
        elif pre and post:
            v = f"INSUFFICIENT (a regime has n<{MIN_N}; registered 2.7 minimum)"
        else:
            v = "INDETERMINATE (a regime lacks an estimate)"
        L.append(f"- {sh}: pre {_fmt(pre)} | post {_fmt(post)} → {v}")
    # E-5
    L.append("**E-5 (fertilizer lag, monthly ← tightening count).**")
    for nd in ["m_urea", "m_dap"]:
        r = _find(rows, nd, "tightening")
        if r:
            pts = [x for x in r["irf"] if x.get("beta") is not None]
            peak = max(pts, key=lambda x: abs(x["beta"])) if pts else None
            p0 = _at(r, 0)
            v = ("CONSISTENT" if (peak and peak["h"] in (3, 6) and p0 and p0["ehw_covers_zero"])
                 else ("INDETERMINATE" if (peak is None or all(x["ehw_covers_zero"] for x in pts)) else "INCONSISTENT"))
            L.append(f"- {nd}: peak |β| at h={peak['h'] if peak else '?'} ({_fmt(peak)}); h=0 {_fmt(p0)} → {v}")
    # E-6
    L.append("**E-6 (physical, weekly h=4 ← tightening).**")
    cs = _at(_find(rows, "crude_stocks_xspr", "tightening"), 4)
    L.append(f"- crude stocks ex-SPR: {_fmt(cs)} → {'CONSISTENT (no significant fall)' if cs and not (cs['beta'] < 0 and not cs['ehw_covers_zero']) else ('INCONSISTENT' if cs else 'INDETERMINATE')}")
    ru = _at(_find(rows, "refinery_util", "tightening"), 4)
    L.append(f"- refinery utilization (pp): {_fmt(ru, 'pp')} → {'CONSISTENT (band covers zero)' if ru and ru['ehw_covers_zero'] else ('INCONSISTENT' if ru else 'INDETERMINATE')}")
    # E-7
    L.append("**E-7 (OPEC, external).**")
    k5 = ext["kanzig_h5"]
    L.append(f"- Brent ← Känzig daily PC, h=5: {_fmt(k5)} → {_sign_verdict(k5, 1)}")
    op = _at(_find(rows, "brent", "opec_decision"), 5)
    L.append(f"- Brent ← opec_decision dummy, h=5: {_fmt(op)} → {'CONSISTENT (indeterminate as expected)' if op and op['ehw_covers_zero'] else ('INCONSISTENT (a pooled sign emerged)' if op else 'INDETERMINATE')}")
    # E-8
    L.append("**E-8 (placebo).**")
    beyond = [c for c in TIGHT if (_find(rows, "brent", c) or {}).get("placebo") and _find(rows, "brent", c)["placebo"]["beyond_state"]]
    L.append(f"- Brent h=5 classes beyond the VIX+GPR state: {beyond or 'none'} → {'CONSISTENT' if beyond else 'INCONSISTENT'}")
    # E-9
    L.append("**E-9 (equity proxies, h=5, S&P-controlled).**")
    for nd in ["eq_fro", "eq_dht", "eq_tnk", "eq_insw", "eq_stng"]:
        p = _at(_find(rows, nd, "chokepoint_disruption"), 5)
        L.append(f"- {nd} ← chokepoint_disruption: {_fmt(p)} → {_sign_verdict(p, 1)}")
    L.append("")
    L.append("## Exogeneity diagnostic (Brent pre-window t−6…t−1, by shock set)")
    for s, e in exo.items():
        L.append(f"- {s}: {e['pre_window_mean_pct']:+.3f}% (se {e['se']}) n={e['n_events']} {e['label']}")
    L.append("")
    L.append("## External checks (§2.8)")
    L.append(f"- corr(opec_decision monthly count, |Känzig monthly surprise|) = {ext['corr_opec_count_vs_abs_kanzig_monthly']['r']} over {ext['corr_opec_count_vs_abs_kanzig_monthly']['n_months']} months")
    L.append(f"- corr(tightening monthly count, B-H supply shock) = {ext['corr_tightening_count_vs_bh_supply_shock']['r']} over {ext['corr_tightening_count_vs_bh_supply_shock']['n_months']} months ({ext['corr_tightening_count_vs_bh_supply_shock']['sign_note']})")
    for k in ["bh_supply_shock_on_pinksheet_crude", "bh_inventory_demand_shock_on_pinksheet_crude"]:
        if k in ext:
            h3 = next((x for x in ext[k]["irf"] if x["h"] == 3), None)
            L.append(f"- Pink Sheet crude ← {k.split('_on_')[0]}, h=3 months: {_fmt(h3)}")
    L.append("")
    L.append("## Limits that apply to every number above")
    L.append("Dummies carry no magnitude; the daily sample starts 1990-01-09 (VIX control); PortWatch nodes are 2019→ "
             "and INSUFFICIENT by construction; equity proxies are S&P-controlled but otherwise confounded; monthly "
             "nodes see counts per month. See RIPPLE_REGISTRATION.md §7.")
    return "\n".join(L) + "\n"


# =============================================================================================
# main
# =============================================================================================

def main():
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    conn = sqlite3.connect(DB)
    ev = load_events(conn)
    Fd, Fw, Fm = build_daily(conn), build_weekly(conn), build_monthly(conn)

    sets_d = shock_dates(ev, ("day",))
    all_dates_d = list(ev.loc[ev["date_precision"] == "day", "event_date"])
    bm = bigmove_dates()
    sets_daily = dict(sets_d); sets_daily.update(bm)

    print("daily frame:", len(Fd["idx"]), "trading days;", {k: len(v) for k, v in sets_daily.items()})
    rows = study_frame(Fd, sets_daily, H_DAILY, P_DAILY, all_dates_d, rng, "daily")
    print("  daily rows:", len(rows))

    rows_w = study_frame(Fw, sets_d, H_WEEKLY, P_WEEKLY, all_dates_d, rng, "weekly", do_placebo=False)
    print("  weekly rows:", len(rows_w))

    # monthly: counts per month of de-overlapped cluster starts (week/month precision events included)
    sets_m_dates = shock_dates(ev, ("day", "week", "month"))
    midx = Fm["idx"]
    sets_m = {}
    for sname, dates in sets_m_dates.items():
        cnt = np.zeros(len(midx))
        for d in dates:
            q = midx.searchsorted(pd.Timestamp(d).to_period("M").to_timestamp())
            if q < len(midx) and midx[q] == pd.Timestamp(d).to_period("M").to_timestamp():
                cnt[q] += 1
        sets_m[sname] = cnt
    rows_m = study_frame(Fm, sets_m, H_MONTHLY, P_MONTHLY, [], rng, "monthly", do_placebo=False)
    print("  monthly rows:", len(rows_m))

    # regimes [2.7]
    dates_np = Fd["idx"].to_numpy()
    pre = dates_np <= np.datetime64(GAS_BREAK_PRE); post = dates_np >= np.datetime64(GAS_BREAK_POST)
    Fhh = {**Fd, "nodes": {"henry_hub": Fd["nodes"]["henry_hub"]}}
    rows_gas = (study_frame(Fhh, sets_d, H_DAILY, P_DAILY, all_dates_d, rng, "daily", do_placebo=False, sample=pre, sample_label=f"pre_{GAS_BREAK_PRE}")
                + study_frame(Fhh, sets_d, H_DAILY, P_DAILY, all_dates_d, rng, "daily", do_placebo=False, sample=post, sample_label=f"post_{GAS_BREAK_POST}"))
    mdates = midx.to_numpy()
    mpre = mdates <= np.datetime64(GAS_BREAK_PRE); mpost = mdates >= np.datetime64(GAS_BREAK_POST)
    Fgm = {**Fm, "nodes": {k: Fm["nodes"][k] for k in ["m_ngas_us", "m_ngas_eu", "m_lng_japan"]}}
    rows_gas_m = (study_frame(Fgm, sets_m, H_MONTHLY, P_MONTHLY, [], rng, "monthly", do_placebo=False, sample=mpre, sample_label=f"pre_{GAS_BREAK_PRE}")
                  + study_frame(Fgm, sets_m, H_MONTHLY, P_MONTHLY, [], rng, "monthly", do_placebo=False, sample=mpost, sample_label=f"post_{GAS_BREAK_POST}"))

    # retraction check [Amendment B]: all-shock restricted to VIX>=median at t-1, six nodes, h=20
    all_pos = [int(q) for q in Fd["idx"].searchsorted(pd.DatetimeIndex(sets_d["all"])) if q < len(Fd["idx"])]
    vp = Fd["vix_pct_t1"]
    vals = np.array([vp[q] for q in all_pos]); med = float(np.nanmedian(vals))
    hi_pos = [q for q in all_pos if np.isfinite(vp[q]) and vp[q] >= med]
    S_hi = np.zeros(len(Fd["idx"])); S_hi[hi_pos] = 1.0
    Fsix = {**Fd, "nodes": {SIX[k]: Fd["nodes"][SIX[k]] for k in SIX}}
    for k in Fsix["nodes"]:
        Fsix["nodes"][k] = {**Fsix["nodes"][k], "headline": 20}
    rows_six = study_frame(Fsix, {"all": S_hi}, H_DAILY, P_DAILY, all_dates_d, rng, "daily", specs=("total",),
                           sample_label="vix_ge_median")
    retraction = {}
    for name, node in SIX.items():
        r = _find(rows_six, node, "all", sample="vix_ge_median")
        h20 = _at(r, 20)
        status = {"TRANSMITTING": "RETAINED", "NULL": "RETRACTED", "INSUFFICIENT": "INSUFFICIENT"}[r["verdict"]]
        retraction[name] = {"node": node, "beta": _fmt(h20, "" if node == "t5yie" else "%"), "n_events": r["n_events"],
                            "placebo_pct": r["placebo"]["percentile"] if r["placebo"] else None,
                            "verdict": r["verdict"] + (" (FRAGILE)" if r["fragile"] else ""), "status": status,
                            "vix_pct_median_used": round(med, 1)}

    pt = passthrough(Fd, Fw, conn)
    ext = external_checks(Fd, Fm, conn, sets_d, sets_m)
    exo = exogeneity(Fd, sets_d)

    all_rows = rows + rows_w + rows_m
    cells = [r for r in all_rows if r["spec"] == "total" and r["shock"] in SHOCKS and r["verdict"]]
    tallies = {k: sum(1 for r in cells if r["verdict"] == k) for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]}
    tallies["FRAGILE"] = sum(1 for r in cells if r["fragile"])
    tallies["cells"] = len(cells)

    meta = {"when": t0.isoformat(timespec="seconds"), "registration": "RIPPLE_REGISTRATION.md cbf4fdc + A, B",
            "seed": SEED, "n_placebo": N_PLACEBO, "daily_T": int(len(Fd["idx"])),
            "shock_counts_daily_deoverlapped": {k: int(len(v)) if not isinstance(v, np.ndarray) else int(v.sum()) for k, v in sets_daily.items()},
            "runtime_s": None}
    meta["runtime_s"] = round((datetime.now(timezone.utc) - t0).total_seconds(), 1)   # stamped BEFORE the writes
    (OUT / "irf.json").write_text(json.dumps({"meta": meta, "rows": all_rows}, indent=1))
    (OUT / "regimes.json").write_text(json.dumps({"meta": meta, "henry_hub_daily": rows_gas, "gas_monthly": rows_gas_m}, indent=1))
    (OUT / "retraction_six.json").write_text(json.dumps({"meta": meta, "rows": rows_six, "status": retraction}, indent=1))
    (OUT / "passthrough.json").write_text(json.dumps({"meta": meta, **pt}, indent=1))
    (OUT / "external_checks.json").write_text(json.dumps({"meta": meta, **ext}, indent=1))
    (OUT / "exogeneity.json").write_text(json.dumps({"meta": meta, **exo}, indent=1))
    summary = summarize(all_rows, rows_gas, rows_gas_m, pt, ext, exo, retraction, tallies, meta)
    (OUT / "SUMMARY.md").write_text(summary)
    print(summary)
    print("runtime", meta["runtime_s"], "s")
    conn.close()


if __name__ == "__main__":
    main()
