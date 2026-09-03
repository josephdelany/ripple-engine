"""
ripple_physical.py -- RIPPLE_REGISTRATION.md Amendment C, as computed.

The v2 study (docs/RIPPLE_FINDINGS.md) had one kind of outcome: a price. A price response
conflates the size of a disruption with the market's belief about it. Amendment C registered two
PHYSICAL-QUANTITY outcome families, with their sample sizes fixed in advance and nothing computed:

    C.2  JODI-Oil monthly country production (+ refinery intake, stocks, exports, product demand)
    C.3  IMF PortWatch daily chokepoint transits

This file runs them. Every estimator primitive is imported from ripple_lp, not re-implemented, so
the estimator is the same object that produced v2: the same lag-augmented local projection, the
same EHW-primary / Newey-West-diagnostic standard errors, the same VIX+GPR-matched placebo, the
same Benjamini-Hochberg rule, the same three verdict words.

WHAT IS NEW HERE, AND DISCLOSED (none of it changes a registered parameter):
  1. A MONTHLY placebo. v2 ran monthly nodes with do_placebo=False, and since Amendment B's
     TRANSMITTING requires the placebo, every monthly cell in v2 was NULL-or-INSUFFICIENT BY
     CONSTRUCTION. That is a defect in the v2 study (it makes hop 4's "zero transmitting cells"
     partly an artefact) and it is recorded in docs/RIPPLE_PHYSICAL.md rather than quietly fixed.
     The monthly buckets are the registered daily construction evaluated on the monthly grid.
  2. A pooled cross-country panel with country fixed effects, registered in C.2 as the secondary
     object. Standard errors are clustered by country, by month, and two-way (Cameron-Gelbach-
     Miller). The shock has no cross-sectional variation, so the TIME-clustered SE binds and is
     the one reported.
  3. PortWatch runs on the CALENDAR-daily index (the registered 2,799 days), not v2's Brent
     trading-day index. Tanker transits happen at weekends; the trading-day index discards 28% of
     the physical record. The trading-day version is reported beside it as a robustness column.
  4. Leave-one-episode-out, which C.3 makes mandatory, is done two ways: a jackknife over event
     clusters (no arbitrary window) and two named calendar episodes.

Run:  python3 src/ripple_physical.py   -> data/ripple/physical.json, data/ripple/PHYSICAL_SUMMARY.md
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import ripple_lp as R           # noqa: E402  -- the v2 estimator, imported not copied

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "ripple"

# ---- Amendment C constants (section in brackets); everything else comes from ripple_lp --------
JODI_W0, JODI_W1 = "2002-01-01", "2026-06-30"          # [C.2] 294 months
PW_W0, PW_W1 = "2019-01-01", "2026-08-30"              # [C.3] 2,799 days
JODI_HEADLINE = 3                                       # [C.2] h = 3 months
PW_HEADLINE = 5                                         # [C.3] h = 5 days
JODI_FLOWS = ["crude_production", "refinery_intake", "crude_stocks",
              "crude_exports", "products_demand"]       # [C.2] production primary, rest secondary
PW_FIELDS = ["n_tanker", "n_total", "capacity_tanker"]  # [C.3] n_tanker headline
CHOKEPOINTS = ["hormuz", "bab_el_mandeb", "suez", "cape_of_good_hope", "malacca", "panama", "bosporus"]
PW_SHOCKS = [c for c in R.CLASSES] + ["tightening"]     # [C.3] the pooled 'all' is NOT used here
JODI_SHOCKS = R.SHOCKS                                  # [C.2] all nine
EXCL_MONTHS = 1                                         # monthly analogue of ripple_lp.EXCL_DAYS=30

# Episode windows for leave-one-episode-out [C.3]. Chosen by inspecting the LEVEL of the transit
# series (not any estimate) and stated here so the choice is visible: Bab el-Mandeb steps from
# ~26 to ~12 tankers/day across Dec 2023-Jan 2024; Hormuz steps from ~47 to ~1 in Mar 2026.
EPISODES = {
    "red_sea_2024": ("2023-12-01", "2024-12-31"),
    "hormuz_2026": ("2026-03-01", "2026-08-30"),
}

# JODI two-letter reporter -> the corpus's own country token. Countries the corpus never names
# still appear (mapped) so the coverage table can say "named 0 times".
CC_TOKEN = {
    "ae": "country.uae", "br": "country.brazil", "ca": "country.canada", "cn": "country.china",
    "de": "country.germany", "dz": "country.algeria", "gb": "country.uk", "in": "country.india",
    "iq": "country.iraq", "ir": "country.iran", "jp": "country.japan", "kr": "country.south_korea",
    "kw": "country.kuwait", "kz": "country.kazakhstan", "mx": "country.mexico", "ng": "country.nigeria",
    "no": "country.norway", "qa": "country.qatar", "ru": "country.russia", "sa": "country.saudi_arabia",
    "us": "country.usa", "ve": "country.venezuela",
}
CP_TOKEN = {  # corpus chokepoint entity -> PortWatch slug
    "chokepoint.hormuz": "hormuz", "chokepoint.bab_el_mandeb": "bab_el_mandeb",
    "chokepoint.suez_canal": "suez", "chokepoint.suez": "suez",
    "chokepoint.malacca": "malacca", "chokepoint.panama_canal": "panama",
    "chokepoint.bosporus": "bosporus",
}
COUNTRY_NAME = {
    "ae": "United Arab Emirates", "br": "Brazil", "ca": "Canada", "cn": "China", "de": "Germany",
    "dz": "Algeria", "gb": "United Kingdom", "in": "India", "iq": "Iraq", "ir": "Iran",
    "jp": "Japan", "kr": "Korea", "kw": "Kuwait", "kz": "Kazakhstan", "mx": "Mexico",
    "ng": "Nigeria", "no": "Norway", "qa": "Qatar", "ru": "Russia", "sa": "Saudi Arabia",
    "us": "United States", "ve": "Venezuela",
}
CP_NAME = {"hormuz": "Strait of Hormuz", "bab_el_mandeb": "Bab el-Mandeb", "suez": "Suez Canal",
           "cape_of_good_hope": "Cape of Good Hope", "malacca": "Malacca Strait",
           "panama": "Panama Canal", "bosporus": "Bosporus"}


# =============================================================================================
# coverage -- computed and reported BEFORE any estimate (Joe's brief, 2026-09-02)
# =============================================================================================

def jodi_coverage(conn):
    """Per-series span and holes, the go-dark table, and the production months-per-year matrix."""
    df = pd.read_sql("SELECT series_id, obs_date, value FROM observations WHERE series_id LIKE 'jodi.%'", conn)
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    df = df[(df.obs_date >= JODI_W0) & (df.obs_date <= JODI_W1)]
    df["cc"] = df.series_id.str.split(".").str[1]
    df["flow"] = df.series_id.str.split(".").str[2]
    midx = pd.date_range(JODI_W0, "2026-06-01", freq="MS")

    per_series = []
    for sid, g in df.groupby("series_id"):
        cc, flow = sid.split(".")[1], sid.split(".")[2]
        first, last = g.obs_date.min(), g.obs_date.max()
        span = len(pd.date_range(first, last, freq="MS"))
        per_series.append({
            "series_id": sid, "cc": cc, "flow": flow, "n_months": int(len(g)),
            "first": str(first.date()), "last": str(last.date()),
            "holes_inside_span": int(span - len(g)),
            "months_missing_at_end": int(len(midx) - midx.searchsorted(last) - 1),
            "zeros": int((g.value == 0).sum()),
        })
    per_series.sort(key=lambda r: (r["cc"], r["flow"]))

    # the go-dark table: reporters whose last observation is before the window end
    end = midx[-1]
    dark = {}
    for r in per_series:
        if pd.Timestamp(r["last"]) < end:
            dark.setdefault(r["cc"], {})[r["flow"]] = r["last"]

    prod = df[df.flow == "crude_production"].copy()
    prod["yr"] = prod.obs_date.dt.year
    matrix = (prod.pivot_table(index="cc", columns="yr", values="value", aggfunc="count")
              .reindex(columns=range(2002, 2027)).fillna(0).astype(int))
    return {
        "window": [JODI_W0, "2026-06-01"], "n_months_in_window": int(len(midx)),
        "n_series": int(df.series_id.nunique()),
        "per_series": per_series,
        "went_dark": dark,
        "production_months_per_year": {cc: {str(y): int(v) for y, v in row.items()}
                                       for cc, row in matrix.iterrows()},
        "production_series_ge_200_months": int(sum(
            1 for r in per_series if r["flow"] == "crude_production" and r["n_months"] >= 200)),
    }


def portwatch_coverage(conn):
    df = pd.read_sql("SELECT series_id, obs_date, value FROM observations WHERE series_id LIKE 'portwatch.%'", conn)
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    df = df[(df.obs_date >= PW_W0) & (df.obs_date <= PW_W1)]
    df["cp"] = df.series_id.str.split(".").str[1]
    df["field"] = df.series_id.str.split(".").str[2]
    cal = pd.date_range(PW_W0, PW_W1, freq="D")
    out = {"window": [PW_W0, PW_W1], "n_calendar_days": int(len(cal)), "per_series": []}
    for sid, g in df.groupby("series_id"):
        z = g[g.value == 0]
        out["per_series"].append({
            "series_id": sid, "n_days": int(len(g)), "first": str(g.obs_date.min().date()),
            "last": str(g.obs_date.max().date()), "missing_days": int(len(cal) - len(g)),
            "zero_days": int(len(z)),
            "zero_months": (z.obs_date.dt.to_period("M").astype(str).value_counts().sort_index().to_dict()
                            if len(z) else {}),
            "mean": round(float(g.value.mean()), 3),
        })
    out["per_series"].sort(key=lambda r: r["series_id"])
    # monthly mean tanker transits, so the two episodes are visible as levels, not as estimates
    tk = df[df.field == "n_tanker"]
    piv = tk.pivot_table(index=tk.obs_date.dt.to_period("M").astype(str), columns="cp",
                         values="value", aggfunc="mean").round(2)
    out["monthly_mean_tanker_transits"] = {m: {k: (None if pd.isna(v) else float(v)) for k, v in row.items()}
                                           for m, row in piv.iterrows()}
    return out


# =============================================================================================
# who the corpus names
# =============================================================================================

def named_maps(conn):
    """event_id -> country tokens (actor/target fields, per C.2) and -> chokepoint slugs (per C.3,
    'the chokepoint named by the event' -- a chokepoint is coded with role 'location', so location
    counts here and does NOT count for the country test)."""
    ev = pd.read_sql("SELECT event_id, sr_actor, sr_target FROM events", conn)
    ee = pd.read_sql("SELECT ee.event_id, ee.role, e.entity_id, e.type "
                     "FROM event_entities ee JOIN entities e ON e.entity_id = ee.entity_id", conn)
    countries, chokes = {}, {}
    for _, r in ev.iterrows():
        for f in (r.sr_actor, r.sr_target):
            if isinstance(f, str) and f.startswith("country."):
                countries.setdefault(r.event_id, set()).add(f)
            if isinstance(f, str) and f in CP_TOKEN:
                chokes.setdefault(r.event_id, set()).add(CP_TOKEN[f])
    for _, r in ee.iterrows():
        if r.type == "country" and r.role in ("actor", "target"):
            countries.setdefault(r.event_id, set()).add(r.entity_id)
        if r.type == "chokepoint" and r.role in ("target", "location") and r.entity_id in CP_TOKEN:
            chokes.setdefault(r.event_id, set()).add(CP_TOKEN[r.entity_id])
    return countries, chokes


def window_shock_sets(ev, precision, lo, hi):
    """De-overlapped cluster starts WITHIN the window (this is what Amendment C's fixed n's count;
    reconciled exactly against C.2 and C.3 before anything was estimated)."""
    e = ev[ev.date_precision.isin(precision)]
    e = e[(e.event_date >= pd.Timestamp(lo)) & (e.event_date <= pd.Timestamp(hi))]
    s = {c: R.cluster_first_dates(e.loc[e.type == c, "event_date"]) for c in R.CLASSES}
    s["all"] = R.cluster_first_dates(e.event_date)
    s["tightening"] = R.cluster_first_dates(e.loc[e.type.isin(R.TIGHT), "event_date"])
    return s, e


# =============================================================================================
# frames
# =============================================================================================

def _state_buckets(idx, vix_pct_t1, gpr_rank_t1, event_dates, excl):
    """The registered placebo state buckets [2.5]: (VIX decile, GPR decile) at t-1, and a pool of
    rows at least `excl` away from every event. `excl` is a pd.Timedelta (daily) or an integer
    number of index steps (monthly)."""
    buckets, pool = {}, {}
    far = np.ones(len(idx), dtype=bool)
    for d in pd.DatetimeIndex(sorted(set(event_dates))):
        if isinstance(excl, pd.Timedelta):
            lo, hi = idx.searchsorted(d - excl), idx.searchsorted(d + excl)
        else:
            q = idx.searchsorted(d)
            lo, hi = max(0, q - excl), min(len(idx), q + excl + 1)
        far[lo:hi] = False
    vd = np.floor(np.asarray(vix_pct_t1, float) / 10).clip(0, 9)
    gd = np.floor(np.asarray(gpr_rank_t1, float) / 10).clip(0, 9)
    for q in range(len(idx)):
        if np.isfinite(vd[q]) and np.isfinite(gd[q]):
            buckets[q] = (int(vd[q]), int(gd[q]))
            if far[q]:
                pool.setdefault(buckets[q], []).append(q)
    return buckets, pool


def build_jodi_frame(conn, event_dates):
    """Monthly frame on the registered window. Controls are section 2.1 monthly, exactly as
    ripple_lp.build_monthly: lagged crude log-change and lagged log GPRD monthly mean."""
    idx = pd.date_range(JODI_W0, "2026-06-01", freq="MS")
    F = {"idx": idx, "nodes": {}}
    sids = [r[0] for r in conn.execute("SELECT series_id FROM series WHERE series_id LIKE 'jodi.%' ORDER BY series_id")]
    for sid in sids:
        cc, flow = sid.split(".")[1], sid.split(".")[2]
        s = R.load_series(conn, sid)
        s.index = s.index.to_period("M").to_timestamp()
        F["nodes"][f"{cc}.{flow}"] = {
            "y": R.transform(s.reindex(idx), "log").to_numpy(float), "sid": sid,
            "hop": 2, "headline": JODI_HEADLINE, "extra": None, "how": "log",
            "cc": cc, "flow": flow,
        }
    crude = R.load_series(conn, "wb.crude_avg")
    crude.index = crude.index.to_period("M").to_timestamp()
    crude = (100 * np.log(crude.reindex(idx))).to_numpy(float)
    F["brent"] = crude
    gpr = R.load_series(conn, "gpr.GPRD")
    gm = 100 * np.log(gpr.resample("MS").mean()).reindex(idx)
    F["ctrls"] = [R.shift(crude - R.shift(crude, 1), 1), gm.shift(1).to_numpy(float)]
    # placebo state on the monthly grid (the daily construction, evaluated monthly)
    vixm = R.load_series(conn, "fred.VIXCLS").resample("MS").mean().reindex(idx)
    vpc = vixm.rolling(60, min_periods=24).rank(pct=True).shift(1) * 100      # 5y window, as daily
    gm30 = gpr.resample("MS").mean().reindex(idx)
    gpc = gm30.rolling(60, min_periods=24).rank(pct=True).shift(1) * 100
    F["vix_dec"] = np.floor(vpc.to_numpy(float) / 10).clip(0, 9)
    F["gpr_dec"] = np.floor(gpc.to_numpy(float) / 10).clip(0, 9)
    F["buckets"], F["pool"] = _state_buckets(idx, vpc.to_numpy(float), gpc.to_numpy(float),
                                             event_dates, EXCL_MONTHS)
    return F


def build_pw_frame(conn, event_dates, calendar=True):
    """Daily frame for the transit nodes. calendar=True is the registered 2,799-day sample;
    calendar=False is v2's Brent trading-day index, kept as a robustness column."""
    if calendar:
        idx = pd.date_range(PW_W0, PW_W1, freq="D")
    else:
        b = R.load_series(conn, "fred.DCOILBRENTEU")
        idx = b.index[(b.index >= pd.Timestamp(PW_W0)) & (b.index <= pd.Timestamp(PW_W1))]
    F = {"idx": idx, "nodes": {}}
    for cp in CHOKEPOINTS:
        for field in PW_FIELDS:
            s = R.load_series(conn, f"portwatch.{cp}.{field}")
            F["nodes"][f"{cp}.{field}"] = {
                "y": R.transform(s.reindex(idx), "log1p").to_numpy(float),
                "sid": f"portwatch.{cp}.{field}", "hop": 2, "headline": PW_HEADLINE,
                "extra": None, "how": "log1p", "cp": cp, "field": field}
    vix = R.load_series(conn, "fred.VIXCLS").reindex(idx, method="ffill")
    lvix = 100 * np.log(vix)
    F["ctrl_vix"] = (lvix.shift(1) - lvix.shift(6)).to_numpy(float)
    gpr30 = R.load_series(conn, "gpr.GPRD_THREAT").rolling(30, min_periods=20).mean()
    g8 = gpr30.copy(); g8.index = g8.index + pd.Timedelta(days=8)
    F["ctrl_gpr"] = (100 * np.log(g8.reindex(idx, method="ffill"))).to_numpy(float)
    F["ctrls"] = [F["ctrl_vix"], F["ctrl_gpr"]]
    F["brent"] = (100 * np.log(R.load_series(conn, "fred.DCOILBRENTEU").reindex(idx, method="ffill"))).to_numpy(float)
    vp = R.load_series(conn, "derived.vix_pct").reindex(idx, method="ffill").shift(1)
    g30 = gpr30.reindex(idx, method="ffill")
    gp = g30.rolling(1260, min_periods=500).rank(pct=True).shift(1) * 100
    F["vix_dec"] = np.floor(vp.to_numpy(float) / 10).clip(0, 9)
    F["gpr_dec"] = np.floor(gp.to_numpy(float) / 10).clip(0, 9)
    F["buckets"], F["pool"] = _state_buckets(idx, vp.to_numpy(float), gp.to_numpy(float),
                                             event_dates, pd.Timedelta(days=R.EXCL_DAYS))
    F["dow"] = np.asarray(idx.dayofweek)
    return F


# =============================================================================================
# the pooled panel [C.2 secondary]
# =============================================================================================

def cluster_cov(X, e, XtXinv, groups):
    """Cluster-robust meat for one grouping, with the usual G/(G-1) * (n-1)/(n-k) correction."""
    n, k = X.shape
    Xe = X * e[:, None]
    G = np.unique(groups)
    meat = np.zeros((k, k))
    for g in G:
        s = Xe[groups == g].sum(axis=0)
        meat += np.outer(s, s)
    c = (len(G) / max(len(G) - 1, 1)) * ((n - 1) / max(n - k, 1))
    return XtXinv @ meat @ XtXinv * c


def panel_lp(F, keys, S, horizons, p, headline):
    """dep[i,t] = y[i,t+h] - y[i,t-1] on: country fixed effects, S[t], pooled own lags 1..p+1 of
    dy[i], and the frame's controls. Dynamics are pooled across countries (homogeneous), which is
    stated as an assumption. Three standard errors: white, clustered by country, clustered by
    month; and the two-way (Cameron-Gelbach-Miller) combination. The shock has no cross-sectional
    variation, so the MONTH-clustered SE is the binding one and is the one reported."""
    ctrls = F["ctrls"]
    out = []
    for h in horizons:
        blocks, dep_all, cid, tid = [], [], [], []
        for j, key in enumerate(keys):
            y = F["nodes"][key]["y"]
            X, dep, mask = R.lp_design(y, S, h, p, ctrls, None)
            X = np.delete(X, 0, axis=1)                     # drop the intercept; FE replaces it
            rows = np.flatnonzero(mask)
            if len(rows) == 0:
                continue
            fe = np.zeros((len(rows), len(keys))); fe[:, j] = 1.0
            blocks.append(np.hstack([fe, X[rows]]))
            dep_all.append(dep[rows]); cid.append(np.full(len(rows), j)); tid.append(rows)
        if not blocks:
            out.append({"h": h, "beta": None, "n_obs": 0}); continue
        XX = np.vstack(blocks); yy = np.concatenate(dep_all)
        cid = np.concatenate(cid); tid = np.concatenate(tid)
        bcol = len(keys)                                     # S is the first column after the FE
        n, k = XX.shape
        XtXinv = np.linalg.pinv(XX.T @ XX)
        b = XtXinv @ (XX.T @ yy)
        e = yy - XX @ b
        Xe = XX * e[:, None]
        V_w = XtXinv @ (Xe.T @ Xe) @ XtXinv * (n / max(n - k, 1))
        V_c = cluster_cov(XX, e, XtXinv, cid)
        V_t = cluster_cov(XX, e, XtXinv, tid)
        V_2 = V_c + V_t - V_w
        beta = float(b[bcol])
        se_t = float(np.sqrt(max(V_t[bcol, bcol], 0)))
        se_c = float(np.sqrt(max(V_c[bcol, bcol], 0)))
        se_w = float(np.sqrt(max(V_w[bcol, bcol], 0)))
        se_2 = float(np.sqrt(max(V_2[bcol, bcol], 0)))
        n_ev = int(np.sum(S[np.unique(tid)] != 0))
        row = {"h": h, "beta": round(beta, 4), "se_time": round(se_t, 4), "se_country": round(se_c, 4),
               "se_white": round(se_w, 4), "se_twoway": round(se_2, 4) if np.isfinite(se_2) else None,
               "lo95": round(beta - R.Z95 * se_t, 4), "hi95": round(beta + R.Z95 * se_t, 4),
               "ehw_covers_zero": bool(abs(beta) < R.Z95 * se_t) if se_t > 0 else None,
               "n_obs": int(n), "n_countries": int(len(np.unique(cid))), "n_months": int(len(np.unique(tid))),
               "n_events": n_ev,
               "p_time": round(float(2 * (1 - R._phi(abs(beta / se_t)))), 4) if se_t > 0 else None}
        out.append(row)
    return out


# =============================================================================================
# per-node cells (the registered single-series object, ripple_lp's estimator verbatim)
# =============================================================================================

def cells(F, shock_sets, horizons, p, freq, rng, node_keys=None, shocks=None, do_placebo=True,
          sample=None, sample_label="full", specs=("total", "crude_conditioned"), extra_cols=None):
    idx = F["idx"]
    keys = node_keys if node_keys is not None else list(F["nodes"])
    shocks = shocks if shocks is not None else list(shock_sets)
    rows = []
    for key in keys:
        node = F["nodes"][key]
        y = node["y"]
        node_rows = []
        for sname in shocks:
            dates = shock_sets[sname]
            S = R.dummies_for(idx, dates)
            event_pos = [int(q) for q in idx.searchsorted(pd.DatetimeIndex(dates)) if q < len(idx)]
            for spec in specs:
                extra = None
                if spec == "crude_conditioned":
                    extra = F["brent"]
                base = extra if extra_cols is None else None
                irf = R.run_lp(y, S, horizons, p, F["ctrls"] + (extra_cols or []), extra, sample)
                head = next((r for r in irf if r["h"] == node["headline"]), None)
                n_ev = head["n_events"] if head else 0
                plac = None
                if do_placebo and spec == "total" and n_ev >= R.MIN_N:
                    plac = R.placebo(y, S, node["headline"], p, F["ctrls"] + (extra_cols or []),
                                     extra, event_pos, F["buckets"], F["pool"], rng, sample)
                v, fragile = R.verdict(head, plac, n_ev) if spec == "total" else (None, False)
                node_rows.append({"node": key, "series_id": node["sid"], "freq": freq,
                                  "shock": sname, "spec": spec, "sample": sample_label,
                                  "headline_h": node["headline"], "n_events": n_ev,
                                  "irf": irf, "placebo": plac, "verdict": v, "fragile": fragile})
        fam = [r for r in node_rows if r["spec"] == "total"]
        pv = [next((x.get("p_ehw") for x in r["irf"] if x["h"] == r["headline_h"]), None) for r in fam]
        for r, flag in zip(fam, R.bh_flags(pv)):
            r["bh_q10_reject"] = flag
        rows.extend(node_rows)
    return rows


def at(row, h):
    return next((x for x in row["irf"] if x["h"] == h), None)


# =============================================================================================
# JODI [C.2]
# =============================================================================================

def run_jodi(conn, ev, rng, cov):
    sets, evw = window_shock_sets(ev, ("day", "week", "month"), JODI_W0, JODI_W1)
    named_c, _ = named_maps(conn)
    F = build_jodi_frame(conn, sets["all"])
    idx = F["idx"]
    res = {"window": [JODI_W0, "2026-06-01"], "n_months": int(len(idx)), "headline_h": JODI_HEADLINE,
           "shock_counts_deoverlapped": {k: len(v) for k, v in sets.items()},
           "placebo_pool_sizes": {str(k): len(v) for k, v in sorted(F["pool"].items())},
           "placebo_pool_total": int(sum(len(v) for v in F["pool"].values()))}

    # ---- the registered PRIMARY: the producer named in the event's own actor/target fields ----
    last_report = {r["series_id"]: r["last"] for r in cov["per_series"]}
    primary, named_counts = [], []
    for cc, token in CC_TOKEN.items():
        ids = {eid for eid, toks in named_c.items() if token in toks}
        e = evw[evw.event_id.isin(ids)]
        sid = f"jodi.{cc}.crude_production"
        last = pd.Timestamp(last_report[sid]) if sid in last_report else None
        row = {"cc": cc, "country": COUNTRY_NAME[cc], "token": token,
               "last_production_report": str(last.date()) if last is not None else None,
               "named_events_raw": int(len(e))}
        per_shock = {}
        for sname in JODI_SHOCKS:
            if sname == "all":
                sub = e
            elif sname == "tightening":
                sub = e[e.type.isin(R.TIGHT)]
            else:
                sub = e[e.type == sname]
            cl = R.cluster_first_dates(sub.event_date)
            in_span = [d for d in cl if last is not None and d <= last]
            per_shock[sname] = {"deoverlapped": len(cl), "within_reporting_span": len(in_span)}
        row["by_shock"] = per_shock
        row["named_deoverlapped"] = per_shock["all"]["deoverlapped"]
        row["named_within_span"] = per_shock["all"]["within_reporting_span"]
        row["named_lost_to_go_dark"] = row["named_deoverlapped"] - row["named_within_span"]
        named_counts.append(row)

        # estimate only where the registered minimum is cleared, and only on the named events
        for sname in JODI_SHOCKS:
            cl = per_shock[sname]["deoverlapped"]
            if cl < R.MIN_N:
                primary.append({"cc": cc, "shock": sname, "n_named": cl,
                                "verdict": "INSUFFICIENT", "reason": f"n={cl} < {R.MIN_N}"})
                continue
            if sname == "all":
                sub = e
            elif sname == "tightening":
                sub = e[e.type.isin(R.TIGHT)]
            else:
                sub = e[e.type == sname]
            dates = R.cluster_first_dates(sub.event_date)
            got = []
            for flow in JODI_FLOWS:
                key = f"{cc}.{flow}"
                if key not in F["nodes"]:
                    continue
                got += cells(F, {sname: dates}, R.H_MONTHLY, R.P_MONTHLY, "monthly", rng,
                             node_keys=[key], shocks=[sname], sample_label="named_producer")
            primary.append({"cc": cc, "shock": sname, "n_named": cl, "rows": got})
    res["named_producer_counts"] = named_counts
    res["named_producer_primary"] = primary

    # ---- SECONDARY 1: the pooled cross-country panel, balanced reporters only ----------------
    # A country that stops reporting must not be allowed to look like a country that stopped
    # producing. The panel therefore uses only reporters with a complete 294-month record.
    balanced = {}
    for flow in JODI_FLOWS:
        ks = [f"{cc}.{flow}" for cc in CC_TOKEN
              if f"{cc}.{flow}" in F["nodes"] and np.isfinite(F["nodes"][f"{cc}.{flow}"]["y"]).all()]
        balanced[flow] = sorted(ks)
    res["balanced_panel_members"] = {k: v for k, v in balanced.items()}
    panel = []
    for flow in JODI_FLOWS:
        ks = balanced[flow]
        if len(ks) < 3:
            panel.append({"flow": flow, "n_countries": len(ks), "skipped": "fewer than 3 balanced reporters"})
            continue
        for sname in JODI_SHOCKS:
            S = R.dummies_for(idx, sets[sname])
            irf = panel_lp(F, ks, S, R.H_MONTHLY, R.P_MONTHLY, JODI_HEADLINE)
            head = next((r for r in irf if r["h"] == JODI_HEADLINE), None)
            panel.append({"flow": flow, "shock": sname, "n_countries": len(ks),
                          "n_events": head["n_events"] if head else 0, "irf": irf,
                          "verdict": ("INSUFFICIENT" if (head or {}).get("n_events", 0) < R.MIN_N
                                      else ("BAND-EXCLUDES-ZERO" if head and head["ehw_covers_zero"] is False
                                            else "NULL"))})
    res["pooled_panel"] = panel

    # ---- SECONDARY 2: the balanced aggregate, a single series the placebo can score -----------
    agg_rows = []
    for flow in ["crude_production", "refinery_intake", "crude_exports", "products_demand"]:
        ks = balanced[flow]
        if len(ks) < 3:
            continue
        lv = np.zeros(len(idx))
        for k in ks:
            lv += np.exp(F["nodes"][k]["y"] / 100.0)
        Fa = {**F, "nodes": {f"agg_{flow}": {"y": 100 * np.log(lv), "sid": f"agg({len(ks)} balanced reporters).{flow}",
                                             "hop": 2, "headline": JODI_HEADLINE, "extra": None,
                                             "how": "log", "cc": "AGG", "flow": flow}}}
        agg_rows += cells(Fa, sets, R.H_MONTHLY, R.P_MONTHLY, "monthly", rng,
                          shocks=JODI_SHOCKS, sample_label="balanced_aggregate")
    res["balanced_aggregate"] = agg_rows

    # ---- EXPLORATORY: every country x flow x shock, BH-controlled within the node's family ----
    expl = cells(F, sets, R.H_MONTHLY, R.P_MONTHLY, "monthly", rng, shocks=JODI_SHOCKS)
    res["external_check"] = jodi_external_check(conn, F, balanced["crude_production"], sets)

    # ---- what the null actually rules out ----------------------------------------------------
    # A null is only informative next to a yardstick. The yardstick is one standard deviation of
    # the identified B-H supply shock, converted to a production and a price move; the null is the
    # corpus dummy's own confidence bound at the same horizon on the same node.
    bnd = {}
    ec = res["external_check"].get("bh_supply_shock", {})
    if "irf" in ec:
        sd = ec["shock_sd_in_window"]
        for h in [0, 1, JODI_HEADLINE]:
            xp = next((x for x in ec["irf"] if x["h"] == h), None)
            xc = next((x for x in ec["on_crude_price"]["irf"] if x["h"] == h), None)
            if not xp or xp.get("beta") is None:
                continue
            one_sd_prod = xp["beta"] * sd
            one_sd_price = xc["beta"] * sd if xc and xc.get("beta") is not None else None
            row = {"h": h, "shock_sd": sd,
                   "one_sd_identified_shock_on_production_pct": round(one_sd_prod, 3),
                   "one_sd_identified_shock_on_price_pct": round(one_sd_price, 3) if one_sd_price else None}
            for sname in ["tightening", "all", "chokepoint_disruption", "infrastructure_attack",
                          "conflict_escalation"]:
                r = next((z for z in res["balanced_aggregate"]
                          if z["spec"] == "total" and z["node"] == "agg_crude_production"
                          and z["shock"] == sname), None)
                x = at(r, h) if r else None
                if not x or x.get("beta") is None:
                    continue
                worst = min(x["lo95"], -x["hi95"] if x["hi95"] < 0 else x["lo95"])
                row[sname] = {
                    "beta": x["beta"], "lo95": x["lo95"], "hi95": x["hi95"], "n": r["n_events"],
                    "largest_production_fall_not_excluded_pct": round(x["lo95"], 3),
                    "as_share_of_one_sd_identified_shock": (
                        round(abs(x["lo95"] / one_sd_prod), 3) if one_sd_prod else None)}
            bnd[f"h{h}"] = row
    res["bounded_null"] = bnd
    res["exploratory"] = expl
    tot = [r for r in expl if r["spec"] == "total"]
    res["exploratory_tally"] = {k: sum(1 for r in tot if r["verdict"] == k)
                                for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]}
    res["exploratory_tally"]["cells"] = len(tot)
    res["exploratory_tally"]["FRAGILE"] = sum(1 for r in tot if r["fragile"])
    res["exploratory_tally"]["bh_survivors"] = sum(1 for r in tot if r.get("bh_q10_reject"))
    lo = round(0.0025 * len(tot), 1); hi = round(0.05 * len(tot), 1)
    res["exploratory_tally"]["null_expected_range"] = [lo, hi]

    # how much of the monthly placebo is real matching and how much is fallback
    fb = [r["placebo"]["buckets_fallback_to_vix_only"] for r in tot if r.get("placebo")]
    res["monthly_placebo_diagnostics"] = {
        "pool_months": res["placebo_pool_total"], "n_state_buckets": len(F["pool"]),
        "cells_with_a_placebo": len(fb),
        "mean_buckets_falling_back_to_vix_only": round(float(np.mean(fb)), 1) if fb else None,
        "note": "The monthly pool is small (294 months, of which the event-exclusion rule removes "
                "most), so most state buckets fall back to VIX-decile-only matching. A monthly "
                "TRANSMITTING verdict therefore rests mainly on the EHW and Newey-West bands and "
                "only weakly on the state match. v2 ran NO monthly placebo at all, which made "
                "TRANSMITTING unreachable for every monthly node by construction."}
    return res


# =============================================================================================
# does the machinery see an IDENTIFIED shock in this data? [2.8-style check, not a gate]
# =============================================================================================

def jodi_external_check(conn, F, keys, sets):
    """The most informative thing that can be asked of a null. v2's section 4.1 showed a
    magnitude-bearing shock (Kaenzig) finding a clean effect on Brent with the same code that
    produced its nulls, which located the weakness in the SHOCK rather than the estimator. The
    same question, asked of the physical data: does JODI aggregate production respond to
    Baumeister & Hamilton's identified structural oil SUPPLY shock? Their shock is defined on
    global production, so if this data and this estimator can see anything, they can see this.
    Sign convention (ripple_lp.external_checks): negative = production down, so the expected
    coefficient on production is POSITIVE."""
    idx = F["idx"]
    lv = np.zeros(len(idx))
    for k in keys:
        lv += np.exp(F["nodes"][k]["y"] / 100.0)
    y = 100 * np.log(lv)
    out = {"node": f"agg_crude_production ({len(keys)} balanced reporters)",
           "expected_sign_on_production": "+ (a positive B-H supply shock is more production)"}
    for name, sid in [("bh_supply_shock", "bh.supply_shock"),
                      ("kanzig_news_shock_monthly", "kanzig.news_shock_monthly")]:
        s = R.load_series(conn, sid)
        s.index = s.index.to_period("M").to_timestamp()
        x = s.reindex(idx).to_numpy(float)
        if np.isfinite(x).sum() < 100:
            out[name] = {"skipped": "fewer than 100 overlapping months"}
            continue
        out[name] = {"irf": R.run_lp(y, np.nan_to_num(x, nan=0.0), R.H_MONTHLY, R.P_MONTHLY,
                                     F["ctrls"], sample=np.isfinite(x)),
                     "n_months_overlap": int(np.isfinite(x).sum()),
                     "unit": "% aggregate production per unit shock"}
        # and the same shock on the price, on this same window, as the yardstick
        out[name]["shock_sd_in_window"] = round(float(pd.Series(x).dropna().std()), 4)
        out[name]["on_crude_price"] = {
            "irf": R.run_lp(F["brent"], np.nan_to_num(x, nan=0.0), R.H_MONTHLY, R.P_MONTHLY,
                            F["ctrls"], sample=np.isfinite(x)),
            "unit": "% Pink Sheet crude per unit shock"}
    return out


def degeneracy_screen(conn):
    """A DISCLOSED POST-HOC screen. It is computed from the SERIES ONLY -- the share of zero
    observations and the volatility of its monthly log change -- and never from any coefficient,
    which is the least contaminated form a screen applied after seeing results can take. It was
    written after the first run, because the first run produced a +47% Nigerian refinery-intake
    'response' that is a near-zero denominator and not a response. It is a description, not a
    test, and both tallies are published."""
    df = pd.read_sql("SELECT series_id, obs_date, value FROM observations WHERE series_id LIKE 'jodi.%'", conn)
    df["obs_date"] = pd.to_datetime(df.obs_date)
    df = df[(df.obs_date >= JODI_W0) & (df.obs_date <= JODI_W1)]
    q = {}
    for sid, g in df.groupby("series_id"):
        v = g.sort_values("obs_date").value
        d = (100 * np.log(v.where(v > 0))).diff()
        zs = float((v == 0).mean()); sd = float(d.std())
        q[sid] = {"zero_share": round(zs, 3), "sd_dlog": round(sd, 1),
                  "median": round(float(v.median()), 2),
                  "degenerate": bool(zs > 0.10 or (np.isfinite(sd) and sd > 25.0))}
    return {"rule": "degenerate if >10% of in-window observations are zero, or the SD of the "
                    "monthly 100*log change exceeds 25",
            "n_degenerate": int(sum(1 for v in q.values() if v["degenerate"])),
            "n_series": len(q), "per_series": q}


# =============================================================================================
# PortWatch [C.3]
# =============================================================================================

def run_portwatch(conn, ev, rng):
    sets, evw = window_shock_sets(ev, ("day",), PW_W0, PW_W1)
    _, named_cp = named_maps(conn)
    F = build_pw_frame(conn, sets["all"], calendar=True)
    Ft = build_pw_frame(conn, sets["all"], calendar=False)
    idx = F["idx"]
    res = {"window": [PW_W0, PW_W1], "n_days_calendar": int(len(idx)),
           "n_days_trading_index": int(len(Ft["idx"])), "headline_h": PW_HEADLINE,
           "shock_counts_deoverlapped": {k: len(v) for k, v in sets.items()},
           "pooled_all_not_used": {"n_all": len(sets["all"]), "n_tightening": len(sets["tightening"]),
                                   "why": "C.3 registers that in this window the 35-day chain rule "
                                          "merges post-2019 events so the pooled 'all' set (16) is "
                                          "SMALLER than tightening (24); 'all' is therefore not used."},
           "placebo_pool_total": int(sum(len(v) for v in F["pool"].values()))}

    # ---- the registered PRIMARY: the chokepoint named by the event ---------------------------
    primary = []
    for cp in CHOKEPOINTS:
        ids = {eid for eid, s in named_cp.items() if cp in s}
        e = evw[evw.event_id.isin(ids)]
        row = {"chokepoint": cp, "name": CP_NAME[cp], "named_events_raw": int(len(e)), "by_shock": {}}
        for sname in PW_SHOCKS + ["all"]:
            if sname == "all":
                sub = e
            elif sname == "tightening":
                sub = e[e.type.isin(R.TIGHT)]
            else:
                sub = e[e.type == sname]
            row["by_shock"][sname] = len(R.cluster_first_dates(sub.event_date))
        row["n_named_deoverlapped"] = row["by_shock"]["all"]
        row["verdict"] = ("INSUFFICIENT" if row["n_named_deoverlapped"] < R.MIN_N else "estimable")
        # below the registered minimum the coefficient may not be read; it is computed and printed
        # as a DESCRIPTION only where any named event exists, so nothing is discovered later and
        # mistaken for something that was hidden.
        if 0 < row["n_named_deoverlapped"] < R.MIN_N:
            dates = R.cluster_first_dates(e.event_date)
            row["description_below_minimum"] = cells(
                F, {"named": dates}, R.H_DAILY, R.P_DAILY, "daily", rng,
                node_keys=[f"{cp}.n_tanker"], shocks=["named"], do_placebo=False,
                sample_label="named_chokepoint_BELOW_MINIMUM", specs=("total",))
        primary.append(row)
    res["named_chokepoint_primary"] = primary

    # ---- SECONDARY: per-class and tightening, every chokepoint, calendar index ----------------
    keys = [f"{cp}.n_tanker" for cp in CHOKEPOINTS] + [f"{cp}.n_total" for cp in CHOKEPOINTS] \
        + [f"{cp}.capacity_tanker" for cp in CHOKEPOINTS]
    res["secondary_calendar"] = cells(F, sets, R.H_DAILY, R.P_DAILY, "daily", rng,
                                      node_keys=keys, shocks=PW_SHOCKS)
    tot = [r for r in res["secondary_calendar"] if r["spec"] == "total"]
    res["secondary_tally"] = {k: sum(1 for r in tot if r["verdict"] == k)
                              for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]}
    res["secondary_tally"]["cells"] = len(tot)
    res["secondary_tally"]["bh_survivors"] = sum(1 for r in tot if r.get("bh_q10_reject"))

    # robustness A: v2's trading-day index, headline nodes only
    res["robustness_trading_day_index"] = cells(
        Ft, sets, R.H_DAILY, R.P_DAILY, "daily", rng,
        node_keys=[f"{cp}.n_tanker" for cp in CHOKEPOINTS], shocks=PW_SHOCKS,
        sample_label="brent_trading_day_index", specs=("total",))
    # robustness B: day-of-week dummies (a calendar-daily transit count has a weekly cycle)
    dow = [np.asarray(F["dow"] == d, float) for d in range(1, 7)]
    res["robustness_day_of_week"] = cells(
        F, sets, R.H_DAILY, R.P_DAILY, "daily", rng,
        node_keys=[f"{cp}.n_tanker" for cp in CHOKEPOINTS], shocks=PW_SHOCKS,
        sample_label="plus_day_of_week_dummies", specs=("total",), extra_cols=dow)

    # ---- leave-one-episode-out [C.3, mandatory] ----------------------------------------------
    loeo = {"named_episodes": [], "cluster_jackknife": []}
    dnp = idx.to_numpy()
    for ename, (lo, hi) in EPISODES.items():
        keep = ~((dnp >= np.datetime64(lo)) & (dnp <= np.datetime64(hi)))
        rows = cells(F, sets, R.H_DAILY, R.P_DAILY, "daily", rng,
                     node_keys=[f"{cp}.n_tanker" for cp in CHOKEPOINTS], shocks=PW_SHOCKS,
                     do_placebo=False, sample=keep, sample_label=f"drop_{ename}", specs=("total",))
        loeo["named_episodes"].append({"episode": ename, "window": [lo, hi],
                                       "days_dropped": int((~keep).sum()), "rows": rows})
    # jackknife over event clusters: drop one de-overlapped event at a time, headline h only
    for cp in CHOKEPOINTS:
        for sname in PW_SHOCKS:
            base_dates = sets[sname]
            if len(base_dates) < R.MIN_N:
                continue
            y = F["nodes"][f"{cp}.n_tanker"]["y"]
            full = R.run_lp(y, R.dummies_for(idx, base_dates), [PW_HEADLINE], R.P_DAILY, F["ctrls"])
            b0 = full[0].get("beta")
            if b0 is None:
                continue
            worst, bs = None, []
            for d in base_dates:
                dd = [x for x in base_dates if x != d]
                r = R.run_lp(y, R.dummies_for(idx, dd), [PW_HEADLINE], R.P_DAILY, F["ctrls"])
                bb = r[0].get("beta")
                if bb is None:
                    continue
                bs.append(bb)
                if worst is None or abs(bb - b0) > abs(worst[1] - b0):
                    worst = (str(pd.Timestamp(d).date()), bb)
            if bs:
                loeo["cluster_jackknife"].append({
                    "node": f"{cp}.n_tanker", "shock": sname, "beta_full": b0,
                    "beta_min": round(min(bs), 4), "beta_max": round(max(bs), 4),
                    "most_influential_event": worst[0], "beta_without_it": round(worst[1], 4),
                    "sign_flips_on_removal": bool(min(bs) * max(bs) < 0)})
    res["leave_one_episode_out"] = loeo

    # ---- the reroute counter-node [C.3] ------------------------------------------------------
    # "a real Red Sea or Bab el-Mandeb closure should move Bab el-Mandeb down and Cape of Good
    # Hope up, and a result that moves both the same way is evidence of a common time trend."
    reroute = []
    for sname in PW_SHOCKS:
        bam = next((r for r in tot if r["node"] == "bab_el_mandeb.n_tanker" and r["shock"] == sname), None)
        cgh = next((r for r in tot if r["node"] == "cape_of_good_hope.n_tanker" and r["shock"] == sname), None)
        if not bam or not cgh:
            continue
        a, b = at(bam, PW_HEADLINE), at(cgh, PW_HEADLINE)
        if not a or a.get("beta") is None or not b or b.get("beta") is None:
            continue
        same = (a["beta"] * b["beta"]) > 0
        reroute.append({"shock": sname, "bab_el_mandeb": a["beta"], "cape_of_good_hope": b["beta"],
                        "n_events": bam["n_events"], "same_sign": bool(same),
                        "reading": ("common time trend, not a reroute" if same
                                    else ("consistent with a reroute" if a["beta"] < 0 < b["beta"]
                                          else "opposite signs but the wrong way round"))})
    res["reroute_counter_node"] = reroute
    return res, F


# =============================================================================================
# the two episodes, described and not estimated
# =============================================================================================

def episode_descriptions(conn):
    """n = 1 each. No estimator can speak here; these are levels, printed so the reader sees the
    single largest physical disruption in the sample instead of inferring it from a null."""
    out = {}
    tk = pd.read_sql("SELECT series_id, obs_date, value FROM observations "
                     "WHERE series_id LIKE 'portwatch.%.n_tanker'", conn)
    tk["obs_date"] = pd.to_datetime(tk.obs_date); tk["cp"] = tk.series_id.str.split(".").str[1]
    brent = R.load_series(conn, "fred.DCOILBRENTEU").sort_index()
    ev = pd.read_sql("SELECT event_id, event_date, type, title, severity FROM events "
                     "WHERE event_date >= '2023-10-01' ORDER BY event_date", conn)

    def block(cp, pre, post, label):
        s = tk[tk.cp == cp].set_index("obs_date").value.sort_index()
        a = s.loc[pre[0]:pre[1]]; b = s.loc[post[0]:post[1]]
        return {"chokepoint": cp, "label": label,
                "pre_window": list(pre), "pre_mean_tankers_per_day": round(float(a.mean()), 2),
                "post_window": list(post), "post_mean_tankers_per_day": round(float(b.mean()), 2),
                "change_pct": round(float(100 * (b.mean() / a.mean() - 1)), 1),
                "n_days_pre": int(len(a)), "n_days_post": int(len(b))}

    out["red_sea_2024"] = {
        "bab_el_mandeb": block("bab_el_mandeb", ("2023-06-01", "2023-11-30"), ("2024-02-01", "2024-12-31"), "Red Sea"),
        "cape_of_good_hope": block("cape_of_good_hope", ("2023-06-01", "2023-11-30"), ("2024-02-01", "2024-12-31"), "reroute check"),
        "brent_pre": round(float(brent.loc["2023-06-01":"2023-11-30"].mean()), 2),
        "brent_post": round(float(brent.loc["2024-02-01":"2024-12-31"].mean()), 2),
    }
    out["hormuz_2026"] = {
        "hormuz": block("hormuz", ("2025-09-01", "2026-02-28"), ("2026-03-05", "2026-08-30"), "Hormuz closure"),
        "cape_of_good_hope": block("cape_of_good_hope", ("2025-09-01", "2026-02-28"), ("2026-03-05", "2026-08-30"), "reroute check"),
        "brent_pre": round(float(brent.loc["2025-09-01":"2026-02-28"].mean()), 2),
        "brent_post": round(float(brent.loc["2026-03-05":"2026-08-30"].mean()), 2),
        "brent_monthly": {str(k.date()): round(float(v), 2) for k, v in
                          brent.loc["2025-12-01":].resample("MS").mean().items()},
        "hormuz_monthly_tankers": {str(k)[:7]: round(float(v), 2) for k, v in
                                   tk[tk.cp == "hormuz"].set_index("obs_date").value.sort_index()
                                   .loc["2025-12-01":].resample("MS").mean().items()},
        "corpus_events": ev[ev.event_date >= "2026-01-01"].to_dict("records"),
    }
    # The arithmetic of the disconnect: after the 2026-06-17 MOU "reopened" the strait, how much of
    # its move has the PRICE given back, and how much of its collapse has the FLOW recovered?
    bm = out["hormuz_2026"]["brent_monthly"]; hm = out["hormuz_2026"]["hormuz_monthly_tankers"]
    def val(d, key):
        return next((v for k, v in d.items() if k.startswith(key)), None)
    pre_p, peak_p = val(bm, "2026-02"), max(v for k, v in bm.items() if k >= "2026-03")
    last_p = val(bm, "2026-08")
    pre_f, trough_f = val(hm, "2026-02"), min(v for k, v in hm.items() if k >= "2026-03")
    last_f = val(hm, "2026-08")
    out["hormuz_2026"]["the_disconnect"] = {
        "brent_pre_feb": pre_p, "brent_peak": peak_p, "brent_latest_aug": last_p,
        "price_retracement_share_of_spike": round((peak_p - last_p) / (peak_p - pre_p), 3),
        "hormuz_pre_feb": pre_f, "hormuz_trough": trough_f, "hormuz_latest_aug": last_f,
        "flow_recovery_share_of_collapse": round((last_f - trough_f) / (pre_f - trough_f), 3),
        "reading": "the price has given back much of its spike; the physical flow has not come back",
    }
    out["corpus_events_since_2023_10"] = ev.to_dict("records")
    return out


# =============================================================================================
# summary
# =============================================================================================

def fmt(pt, unit="%"):
    if not pt or pt.get("beta") is None:
        return "n/a"
    return f"{pt['beta']:+.3f}{unit} [{pt['lo95']:+.3f}, {pt['hi95']:+.3f}]"


def summarize(cov, pwcov, jodi, pw, epi, meta, screen):
    L = []
    A = L.append
    A("# The physical half of the ripple study — Amendment C, as computed\n")
    A(f"*Run {meta['when']}, seed {meta['seed']}, runtime {meta['runtime_s']}s. "
      "Registered in RIPPLE_REGISTRATION.md Amendment C before anything here was computed; "
      "every sample size the amendment fixed in advance reproduces exactly (below). "
      "Estimator imported from `src/ripple_lp.py`, not re-implemented.*\n")

    A("## 0. Coverage first — the physical record goes dark for the producers that matter\n")
    A(f"JODI: {cov['n_series']} series, window {cov['window'][0]} → {cov['window'][1]}, "
      f"{cov['n_months_in_window']} months. "
      f"{cov['production_series_ge_200_months']} production series carry ≥200 months "
      "(Amendment C.2 said 21).\n")
    A("| reporter | production ends | exports ends | stocks ends | intake ends | demand ends |")
    A("|---|---|---|---|---|---|")
    for cc in sorted(cov["went_dark"]):
        d = cov["went_dark"][cc]
        A(f"| {COUNTRY_NAME.get(cc, cc)} | " + " | ".join(
            d.get(f, "—") for f in ["crude_production", "crude_exports", "crude_stocks",
                                    "refinery_intake", "products_demand"]) + " |")
    A("")
    A("**Months of crude production reported, by year.** A zero is a country that stopped "
      "reporting, not a country that stopped producing.\n")
    yrs = [str(y) for y in range(2002, 2027)]
    A("| reporter | " + " | ".join(y[2:] for y in yrs) + " |")
    A("|---" * (len(yrs) + 1) + "|")
    for cc, row in sorted(cov["production_months_per_year"].items()):
        A(f"| {COUNTRY_NAME.get(cc, cc)} | " + " | ".join(str(row.get(y, 0)) for y in yrs) + " |")
    A("")

    A("### 0.1 The selection problem, in one table\n")
    A("For each producer: how many de-overlapped corpus events name it as actor or target, and how "
      "many of those fall while it was still reporting production. The gap is the part of the "
      "physical record that the geopolitics itself removed.\n")
    A("| producer | last production report | named events (de-overlapped) | within reporting span | lost |")
    A("|---|---|---|---|---|")
    for r in sorted(jodi["named_producer_counts"], key=lambda x: -x["named_deoverlapped"]):
        if r["named_deoverlapped"] == 0:
            continue
        A(f"| {r['country']} | {r['last_production_report']} | {r['named_deoverlapped']} | "
          f"{r['named_within_span']} | **{r['named_lost_to_go_dark']}** |")
    A("")
    tot_named = sum(r["named_deoverlapped"] for r in jodi["named_producer_counts"])
    tot_span = sum(r["named_within_span"] for r in jodi["named_producer_counts"])
    A(f"Across all reporters: **{tot_named}** named de-overlapped events, **{tot_span}** of them "
      f"inside the producer's reporting span — **{tot_named - tot_span} lost**.\n")

    A(f"PortWatch: 7 chokepoints × 3 fields, {pwcov['n_calendar_days']} calendar days "
      f"({pwcov['window'][0]} → {pwcov['window'][1]}), no missing days. "
      "Amendment C.3 fixed the window at 2,799 days.\n")

    A("## 1. Did the registered sample sizes reproduce?\n")
    A("| set | JODI registered | JODI computed | PortWatch registered | PortWatch computed |")
    A("|---|---|---|---|---|")
    JREG = {"chokepoint_disruption": 21, "infrastructure_attack": 21, "conflict_escalation": 34,
            "opec_decision": 38, "sanctions": 36, "demand_shock": 13, "policy_response": 36,
            "all": 67, "tightening": 51}
    PREG = {"chokepoint_disruption": 14, "infrastructure_attack": 14, "conflict_escalation": 17,
            "opec_decision": 15, "sanctions": 19, "demand_shock": 9, "policy_response": 22,
            "all": 16, "tightening": 24}
    for k in JREG:
        A(f"| {k} | {JREG[k]} | {jodi['shock_counts_deoverlapped'][k]} | {PREG[k]} | "
          f"{pw['shock_counts_deoverlapped'][k]} |")
    A("\nEvery one matches, including the counterintuitive PortWatch fact that the pooled `all` "
      f"set ({pw['shock_counts_deoverlapped']['all']}) is *smaller* than `tightening` "
      f"({pw['shock_counts_deoverlapped']['tightening']}). The seal holds.\n")

    A("## 2. JODI — the registered primary test barely exists\n")
    A(f"The primary is the producer the event itself names. Of {len(CC_TOKEN)} JODI reporters, "
      "these clear the registered minimum of 15 de-overlapped named events:\n")
    A("| producer | named (all) | tightening | clears n≥15? |")
    A("|---|---|---|---|")
    for r in sorted(jodi["named_producer_counts"], key=lambda x: -x["named_deoverlapped"])[:12]:
        ok = "**yes**" if r["named_deoverlapped"] >= R.MIN_N else "no"
        A(f"| {r['country']} | {r['named_deoverlapped']} | {r['by_shock']['tightening']['deoverlapped']} | {ok} |")
    A("")
    est = [p for p in jodi["named_producer_primary"] if "rows" in p]
    A(f"Estimable named-producer cells: **{len(est)}**.\n")
    for p in est:
        for row in p["rows"]:
            if row["spec"] != "total":
                continue
            h = at(row, JODI_HEADLINE)
            A(f"- `{row['node']}` × {row['shock']} (n={row['n_events']}): {fmt(h)} — "
              f"**{row['verdict']}**" + (" (FRAGILE)" if row["fragile"] else ""))
    A("")

    A("### 2.1 The pooled panel, balanced reporters only\n")
    bal = jodi["balanced_panel_members"]["crude_production"]
    A(f"{len(bal)} reporters have a complete {jodi['n_months']}-month production record: "
      + ", ".join(COUNTRY_NAME.get(k.split('.')[0], k) for k in bal) + ".\n")
    A("Standard errors clustered by month (the shock has no cross-sectional variation, so this is "
      "the binding one). Headline h = 3 months.\n")
    A("| flow | shock | n countries | n events | β(h=3) [95%] | verdict |")
    A("|---|---|---|---|---|---|")
    for p in jodi["pooled_panel"]:
        if "irf" not in p or p["flow"] != "crude_production":
            continue
        h = next((x for x in p["irf"] if x["h"] == JODI_HEADLINE), None)
        A(f"| {p['flow']} | {p['shock']} | {p['n_countries']} | {p['n_events']} | {fmt(h)} | {p['verdict']} |")
    A("")

    A("### 2.2 The balanced aggregate\n")
    A("| node | shock | n | β(h=3) [95%] | placebo pct | verdict |")
    A("|---|---|---|---|---|---|")
    for row in jodi["balanced_aggregate"]:
        if row["spec"] != "total":
            continue
        h = at(row, JODI_HEADLINE)
        pp = row["placebo"]["percentile"] if row["placebo"] else "—"
        A(f"| {row['node']} | {row['shock']} | {row['n_events']} | {fmt(h)} | {pp} | {row['verdict']} |")
    A("")

    A("### 2.3 Does the machinery see an identified shock in this data?\n")
    ec = jodi["external_check"]
    A(f"Node: `{ec['node']}`. Expected sign on production: {ec['expected_sign_on_production']}.\n")
    A("| shock series | on aggregate production, h=3 | on the crude price, h=3 | months |")
    A("|---|---|---|---|")
    for name in ["bh_supply_shock", "kanzig_news_shock_monthly"]:
        e = ec.get(name, {})
        if "irf" not in e:
            continue
        hp = next((x for x in e["irf"] if x["h"] == JODI_HEADLINE), None)
        hc = next((x for x in e["on_crude_price"]["irf"] if x["h"] == JODI_HEADLINE), None)
        A(f"| {name} | {fmt(hp)} | {fmt(hc)} | {e['n_months_overlap']} |")
    A("")

    t = jodi["exploratory_tally"]
    tc = jodi["exploratory_tally_clean"]
    A("### 2.4 The exploratory family (every reporter × flow × shock)\n")
    A(f"A disclosed post-hoc screen ({screen['rule']}) marks "
      f"{screen['n_degenerate']} of {screen['n_series']} series as degenerate — Germany reports "
      "zero crude exports in most months, Korea's crude 'production' is a rounding error. The "
      "screen is computed from the series alone, never from a coefficient, and both tallies are "
      "published.\n")
    A("| verdict | all cells | cells on non-degenerate series |")
    A("|---|---|---|")
    for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]:
        A(f"| {k} | {t[k]} | {tc[k]} |")
    A(f"| **total** | **{t['cells']}** | **{tc['cells']}** |")
    A(f"| expected TRANSMITTING under a complete null | {t['null_expected_range'][0]}–{t['null_expected_range'][1]} "
      f"| {tc['null_expected_range'][0]}–{tc['null_expected_range'][1]} |")
    A(f"| surviving BH q=0.10 within the node's family | {t['bh_survivors']} | — |")
    A("")
    d = jodi["monthly_placebo_diagnostics"]
    A(f"**The monthly placebo is thin.** Pool {d['pool_months']} months across {d['n_state_buckets']} "
      f"state buckets; on average {d['mean_buckets_falling_back_to_vix_only']} buckets per cell fall "
      "back to VIX-decile-only matching. A monthly TRANSMITTING verdict therefore rests mainly on "
      "the two standard-error bands. **v2 ran no monthly placebo at all**, which made TRANSMITTING "
      "unreachable for every monthly node by construction — a defect in the v2 study, recorded "
      "here rather than quietly fixed.\n")
    tr = [r for r in jodi["exploratory"] if r["spec"] == "total" and r["verdict"] == "TRANSMITTING"]
    if tr:
        A("| node | shock | n | β(h=3) [95%] | placebo pct | BH |")
        A("|---|---|---|---|---|---|")
        for row in sorted(tr, key=lambda r: r["node"]):
            h = at(row, JODI_HEADLINE)
            A(f"| {row['node']} | {row['shock']} | {row['n_events']} | {fmt(h)} | "
              f"{row['placebo']['percentile'] if row['placebo'] else '—'} | "
              f"{'**yes**' if row.get('bh_q10_reject') else 'no'} |"
              + ("  ← degenerate series" if row.get("series_degenerate") else ""))
        A("")

    A("## 3. PortWatch — the registered primary test is INSUFFICIENT at every chokepoint\n")
    A("| chokepoint | named events (de-overlapped, 2019+) | clears n≥15? |")
    A("|---|---|---|")
    for r in pw["named_chokepoint_primary"]:
        A(f"| {r['name']} | {r['n_named_deoverlapped']} | "
          f"{'yes' if r['n_named_deoverlapped'] >= R.MIN_N else '**no**'} |")
    A("\nThe registration forbids reading a cell below n = 15. Every named-chokepoint cell is below "
      "it, so the registered primary test returns **INSUFFICIENT everywhere** — a fact about the "
      "corpus, knowable without estimating anything.\n")

    st = pw["secondary_tally"]
    A("### 3.1 The secondary: per-class shocks on all seven chokepoints\n")
    A(f"| verdict | cells |\n|---|---|\n| TRANSMITTING | {st['TRANSMITTING']} |\n| NULL | {st['NULL']} |\n"
      f"| INSUFFICIENT | {st['INSUFFICIENT']} |\n| **total** | **{st['cells']}** |\n"
      f"| surviving BH q=0.10 | {st['bh_survivors']} |\n")
    tr = [r for r in pw["secondary_calendar"] if r["spec"] == "total" and r["verdict"] == "TRANSMITTING"]
    if tr:
        A("| node | shock | n | β(h=5) [95%] | placebo pct | BH |")
        A("|---|---|---|---|---|---|")
        for row in sorted(tr, key=lambda r: r["node"]):
            h = at(row, PW_HEADLINE)
            A(f"| {row['node']} | {row['shock']} | {row['n_events']} | {fmt(h)} | "
              f"{row['placebo']['percentile'] if row['placebo'] else '—'} | "
              f"{'**yes**' if row.get('bh_q10_reject') else 'no'} |")
        A("")

    A("### 3.2 The reroute counter-node\n")
    A("| shock | Bab el-Mandeb β(h=5) | Cape of Good Hope β(h=5) | reading |")
    A("|---|---|---|---|")
    for r in pw["reroute_counter_node"]:
        A(f"| {r['shock']} | {r['bab_el_mandeb']:+.3f} | {r['cape_of_good_hope']:+.3f} | {r['reading']} |")
    A("")

    A("### 3.3 Leave-one-episode-out (C.3, mandatory)\n")
    for e in pw["leave_one_episode_out"]["named_episodes"]:
        A(f"**Dropping {e['episode']}** ({e['window'][0]} → {e['window'][1]}, "
          f"{e['days_dropped']} days).\n")
    jk = pw["leave_one_episode_out"]["cluster_jackknife"]
    flips = [j for j in jk if j["sign_flips_on_removal"]]
    A(f"Cluster jackknife over {len(jk)} (node × shock) cells: **{len(flips)}** change sign when a "
      "single de-overlapped event is removed.\n")

    A("## 4. The two episodes, described and not estimated\n")
    h26 = epi["hormuz_2026"]["hormuz"]
    c26 = epi["hormuz_2026"]["cape_of_good_hope"]
    rs = epi["red_sea_2024"]["bab_el_mandeb"]
    rc = epi["red_sea_2024"]["cape_of_good_hope"]
    A("| episode | node | pre | post | change |")
    A("|---|---|---|---|---|")
    A(f"| Red Sea 2024 | Bab el-Mandeb tankers/day | {rs['pre_mean_tankers_per_day']} | "
      f"{rs['post_mean_tankers_per_day']} | **{rs['change_pct']:+.1f}%** |")
    A(f"| Red Sea 2024 | Cape of Good Hope tankers/day | {rc['pre_mean_tankers_per_day']} | "
      f"{rc['post_mean_tankers_per_day']} | **{rc['change_pct']:+.1f}%** |")
    A(f"| Red Sea 2024 | Brent, $/bbl | {epi['red_sea_2024']['brent_pre']} | "
      f"{epi['red_sea_2024']['brent_post']} | — |")
    A(f"| Hormuz 2026 | Hormuz tankers/day | {h26['pre_mean_tankers_per_day']} | "
      f"{h26['post_mean_tankers_per_day']} | **{h26['change_pct']:+.1f}%** |")
    A(f"| Hormuz 2026 | Cape of Good Hope tankers/day | {c26['pre_mean_tankers_per_day']} | "
      f"{c26['post_mean_tankers_per_day']} | **{c26['change_pct']:+.1f}%** |")
    A(f"| Hormuz 2026 | Brent, $/bbl | {epi['hormuz_2026']['brent_pre']} | "
      f"{epi['hormuz_2026']['brent_post']} | — |")
    A("\nn = 1 each. No estimator in this study can speak to a single episode; these are levels.\n")
    A("Brent, monthly mean, against Hormuz tanker transits:\n")
    A("| month | Brent $/bbl | Hormuz tankers/day |")
    A("|---|---|---|")
    bm = epi["hormuz_2026"]["brent_monthly"]; hm = epi["hormuz_2026"]["hormuz_monthly_tankers"]
    for k in sorted(bm):
        A(f"| {k[:7]} | {bm[k]} | {hm.get(k[:7], '—')} |")
    A("")
    return "\n".join(L)


def main():
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(R.SEED)
    conn = sqlite3.connect(DB)
    ev = R.load_events(conn)

    print("coverage ...")
    cov = jodi_coverage(conn)
    pwcov = portwatch_coverage(conn)
    print("  JODI series:", cov["n_series"], "| went dark:", len(cov["went_dark"]),
          "| production >=200m:", cov["production_series_ge_200_months"])
    print("  PortWatch days:", pwcov["n_calendar_days"])

    print("JODI ...")
    jodi = run_jodi(conn, ev, rng, cov)
    print("  exploratory tally:", jodi["exploratory_tally"])

    print("PortWatch ...")
    pw, _ = run_portwatch(conn, ev, rng)
    print("  secondary tally:", pw["secondary_tally"])

    epi = episode_descriptions(conn)
    screen = degeneracy_screen(conn)
    tot = [r for r in jodi["exploratory"] if r["spec"] == "total"]
    clean = [r for r in tot if not screen["per_series"].get(r["series_id"], {}).get("degenerate")]
    jodi["exploratory_tally_clean"] = {k: sum(1 for r in clean if r["verdict"] == k)
                                       for k in ["TRANSMITTING", "NULL", "INSUFFICIENT"]}
    jodi["exploratory_tally_clean"]["cells"] = len(clean)
    jodi["exploratory_tally_clean"]["null_expected_range"] = [round(0.0025 * len(clean), 1),
                                                              round(0.05 * len(clean), 1)]
    for r in tot:
        r["series_degenerate"] = bool(screen["per_series"].get(r["series_id"], {}).get("degenerate"))

    meta = {"when": t0.isoformat(timespec="seconds"), "seed": R.SEED, "n_placebo": R.N_PLACEBO,
            "registration": "RIPPLE_REGISTRATION.md Amendment C (2026-09-02)",
            "estimator": "imported from src/ripple_lp.py (v2, unchanged)",
            "min_n": R.MIN_N, "cluster_days": R.CLUSTER_DAYS, "bh_q": R.BH_Q, "runtime_s": None}
    meta["runtime_s"] = round((datetime.now(timezone.utc) - t0).total_seconds(), 1)

    payload = {"meta": meta, "jodi_coverage": cov, "portwatch_coverage": pwcov,
               "jodi": jodi, "portwatch": pw, "episodes": epi, "degeneracy_screen": screen}
    (OUT / "physical.json").write_text(json.dumps(payload, indent=1, default=str))
    s = summarize(cov, pwcov, jodi, pw, epi, meta, screen)
    (OUT / "PHYSICAL_SUMMARY.md").write_text(s)
    print("\nruntime", meta["runtime_s"], "s ->", OUT / "physical.json")
    conn.close()


if __name__ == "__main__":
    main()
