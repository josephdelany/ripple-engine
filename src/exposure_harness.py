"""
exposure_harness.py -- PHYSICAL_EXPOSURE_REGISTRATION.md §4: the estimation harness for the four
registered comparisons, on the whole petroleum complex rather than crude alone.

Written before K's exposure file exists, against the schema declared in SCHEMA below. When
`data/exposure.{json,csv}` lands it runs; until then it prints the schema it expects and exits clean.
**This module constructs no exposure value.** K owns the exposure; B owns the estimation.

  A  class dummy (status quo)          C  both together      -- does the dummy survive magnitude?
  B  exposure X3 (share of buffer)     D  exposure X1 alone  -- is the NORMALISATION doing the work?

THE UNIT OF DEPENDENCE IS THE SOURCE EVENT, NOT THE CELL. Estimation uses every event; inference
resamples the registered 35-day source-event clusters. `n_events` and `n_clusters` are both published and
only `n_clusters` is inferential. This is the finding of `docs/INTERVAL_AUDIT_2026-09-03.md`, and a local
projection stacking eight horizons across eight targets is the single easiest place in this project to
repeat the defect it found: a flat vector of 512 (target, horizon) cells resampled with an event-level block
would report ~500 quasi-independent observations where there are ~120 clusters.

FOUR READINGS OF THE REGISTRATION THAT B HAD TO FIX TO WRITE CODE AT ALL. Flagged here, before any number,
so Cowork can correct them while correction is still free:
  R1. §4's "class dummy" on an event-date-only sample has no variance if it means "an event occurred", so
      it is read as the CLASS indicator set (7 corpus types, drop-first). That is the only reading on which
      spec A is estimable at all, and it is the status quo design: the class is what the engine conditions on.
  R2. "B beats A" (§5) is read as BOTH of: X3's coefficient band excludes zero, AND the band on the
      R-squared difference (B - A) excludes zero. A coefficient alone does not establish that a regressor
      beats a rival specification.
  R3. §6's "PortWatch reroute distance" is not a series in the tree. It is constructed here, declared, as
      log(Cape of Good Hope tanker capacity) - log(Bab el-Mandeb tanker capacity): the substitution between
      the long route and the short one. PortWatch begins 2019-01-01, so this target exists for post-2019
      events only and its n is reported separately, never pooled into a complex-wide claim.
  R4. Fertilizer has no free global price series here; `yf.eq_mos` (Mosaic) is the registered EQUITY PROXY
      already in the tree, with `yf.eq_cf` (CF Industries, 2005->) beside it. An equity proxy is not a
      fertilizer price and the output labels it `proxy: equity`.

Run:  python3 src/exposure_harness.py [--fast]
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from engine import inference as INF      # noqa: E402
from robustness import assign_clusters, CLUSTER_DAYS    # noqa: E402

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "exposure_estimates.json"

# ------------------------------------------------------------------ registered constants
HORIZONS = (0, 1, 2, 5, 10, 20, 40, 60)     # §1
HEADLINE_H = 20                              # §1
N_BOOT = 2000
SEED = 19900802
PLACEBO_EXCL_DAYS = 30                       # the registered placebo rule
FDR_Q = 0.05
SPECS = ("A_dummy", "B_X3", "C_both", "D_X1")

TARGETS = {                                  # §1, in the order they are scored
    "brent":          {"kind": "price", "series": "fred.DCOILBRENTEU"},
    "wti":            {"kind": "price", "series": "fred.DCOILWTICO"},
    "diesel_crack":   {"kind": "crack", "series": "derived.diesel_crack"},
    "gasoline_crack": {"kind": "crack", "series": "derived.gasoline_crack"},
    "henry_hub":      {"kind": "gas",   "series": "fred.DHHNGSP"},
    "propane":        {"kind": "gas",   "series": "fred.DPROPANEMBTX"},
    "fertilizer":     {"kind": "fertilizer", "series": "yf.eq_mos", "proxy": "equity",
                       "secondary": "yf.eq_cf"},
    "reroute":        {"kind": "freight", "proxy": "portwatch_reroute",
                       "construction": "log(portwatch.cape_of_good_hope.capacity_tanker) - "
                                       "log(portwatch.bab_el_mandeb.capacity_tanker)",
                       "available_from": "2019-01-01"},
}
CRACK_TARGETS = tuple(k for k, v in TARGETS.items() if v["kind"] == "crack")
CRUDE_TARGETS = tuple(k for k, v in TARGETS.items() if v["kind"] == "price")

# ------------------------------------------------------------------ §2 the declared input schema
SCHEMA = {
    "event_id":     {"names": ("event_id", "id"), "required": True,
                     "what": "corpus event id; must join to events.event_id"},
    "X1_kbd":       {"names": ("X1_kbd", "X1", "X1_prod_kbd", "x1_capacity_kbd"), "required": True,
                     "what": "T1 country capacity exposure, kb/d. NULL where no register precedes t "
                             "(§2: null, not zero)"},
    "X3_share":     {"names": ("X3_share", "X3", "X3_share_of_spare", "x3"), "required": True,
                     "what": "T3 = X1 / SPARE(t), dimensionless. NULL before 2003 (§2 fallback)"},
    "register_pub": {"names": ("register_pub", "X1_register_pub", "register_pub_date", "knowable_at"),
                     "required": True,
                     "what": "publication date of the capacity register the value came from. §3's "
                             "filtration test asserts this is STRICTLY BEFORE the event date"},
    "X2_share":     {"names": ("X2_share", "X2", "X2_chokepoint_share"), "required": False,
                     "what": "T2 chokepoint flow share. Optional: not one of §4's four comparisons"},
    "spare_kbd":    {"names": ("spare_kbd", "spare", "spare_capacity_kbd"), "required": False,
                     "what": "SPARE(t) in kb/d, for the exclusion table"},
}


def schema_doc():
    return {k: {"accepted_columns": list(v["names"]), "required": v["required"], "meaning": v["what"]}
            for k, v in SCHEMA.items()}


def exposure_path():
    for n in ("exposure.json", "exposure.csv", "exposure.csv.gz"):
        p = ROOT / "data" / n
        if p.exists():
            return p
    return None


def load_exposure(path=None):
    """Read K's file through §2's declared schema and fail LOUDLY, naming exactly what is missing."""
    path = path or exposure_path()
    if path is None:
        raise FileNotFoundError(
            "K's exposure file is not in the tree. This harness constructs no exposure value (§2 is K's). "
            f"Expected data/exposure.json or data/exposure.csv under {ROOT/'data'}.")
    if path.suffix == ".json":
        raw = json.loads(path.read_text())
        df = pd.DataFrame(raw["events"] if isinstance(raw, dict) and "events" in raw else raw)
    else:
        df = pd.read_csv(path, low_memory=False)
    ren, missing = {}, []
    for concept, spec in SCHEMA.items():
        hit = next((n for n in spec["names"] if n in df.columns), None)
        if hit:
            ren[hit] = concept
        elif spec["required"]:
            missing.append(f"{concept} (tried {', '.join(spec['names'])})")
    if missing:
        raise KeyError("K's exposure file does not carry: " + "; ".join(missing) +
                       f". Columns present: {sorted(df.columns)}. Fix SCHEMA here or send a handoff to K "
                       "-- do not rename K's file.")
    df = df.rename(columns=ren)
    df["register_pub"] = pd.to_datetime(df["register_pub"], errors="coerce")
    for c in ("X1_kbd", "X3_share", "X2_share", "spare_kbd"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df, path


# ------------------------------------------------------------------ the panel

def load_series(conn, ids):
    q = ("select series_id, obs_date, value from observations where series_id in (%s) and value is not null"
         % ",".join("?" * len(ids)))
    d = pd.read_sql(q, conn, params=list(ids))
    d["obs_date"] = pd.to_datetime(d["obs_date"])
    return {k: g.set_index("obs_date")["value"].sort_index() for k, g in d.groupby("series_id")}


def target_series(series):
    """One level series per target, including R3's declared reroute construction."""
    out = {}
    for name, spec in TARGETS.items():
        if name == "reroute":
            cape = series.get("portwatch.cape_of_good_hope.capacity_tanker")
            bab = series.get("portwatch.bab_el_mandeb.capacity_tanker")
            if cape is None or bab is None:
                continue
            idx = cape.index.intersection(bab.index)
            with np.errstate(divide="ignore", invalid="ignore"):
                v = np.log(cape.reindex(idx).to_numpy()) - np.log(bab.reindex(idx).to_numpy())
            s = pd.Series(v, index=idx).replace([np.inf, -np.inf], np.nan).dropna()
            out[name] = ("level_log_ratio", s)      # already in log points; do NOT log again
        else:
            s = series.get(spec["series"])
            if s is not None:
                out[name] = ("price", s.dropna())
    return out


def responses(tsr, dates):
    """y_{i,h} = 100 * (log P_{t+h} - log P_{t-1}) for a price target; the same difference in log points
    for the already-logged reroute ratio. t-1 is the last observation strictly before the event date, which
    is the registered form in src/ripple_lp.py [2.1]."""
    kind, s = tsr
    idx = s.index.to_numpy()
    vals = s.to_numpy(float)
    out = {}
    pos_pre = np.searchsorted(idx, np.array(dates, dtype="datetime64[ns]"), side="left") - 1
    pos_0 = np.searchsorted(idx, np.array(dates, dtype="datetime64[ns]"), side="left")
    for h in HORIZONS:
        y = np.full(len(dates), np.nan)
        tgt = pos_0 + h
        ok = (pos_pre >= 0) & (tgt < len(vals))
        base = np.where(ok, vals[np.clip(pos_pre, 0, len(vals) - 1)], np.nan)
        end = np.where(ok, vals[np.clip(tgt, 0, len(vals) - 1)], np.nan)
        with np.errstate(divide="ignore", invalid="ignore"):
            y = (end - base) if kind == "level_log_ratio" else 100.0 * (np.log(end) - np.log(base))
        out[h] = np.where(np.isfinite(y), y, np.nan)
    return out


def build_panel(exposure):
    conn = sqlite3.connect(DB)
    ev = pd.read_sql("select event_id, event_date as date, type from events order by event_date", conn)
    ev["date"] = pd.to_datetime(ev["date"])
    df = ev.merge(exposure, on="event_id", how="inner")
    df = assign_clusters(df)                       # the registered 35-day source-event cluster
    need = [v["series"] for v in TARGETS.values() if "series" in v]
    need += ["portwatch.cape_of_good_hope.capacity_tanker", "portwatch.bab_el_mandeb.capacity_tanker",
             "yf.eq_cf", "derived.vix_pct"]
    series = load_series(conn, sorted(set(need)))
    tsr = target_series(series)
    Y = {name: responses(t, df["date"].to_numpy()) for name, t in tsr.items()}
    return df, Y, series, conn


# ------------------------------------------------------------------ §3 the filtration test

def filtration_test(df):
    """§3: a register's knowable_at is its PUBLICATION date. No exposure value may derive from a register
    published on or after its event date. One violation voids the run."""
    pub, d = df["register_pub"], df["date"]
    bad = pub.isna() | (pub >= d)
    first = None
    if bad.any():
        r = df.loc[bad].iloc[0]
        first = {"event_id": r["event_id"], "event_date": str(r["date"].date()),
                 "register_pub": (None if pd.isna(r["register_pub"]) else str(r["register_pub"].date()))}
    return {"n_events": int(len(df)), "n_violations": int(bad.sum()), "asserted": bool(not bad.any()),
            "first_violation": first,
            "rule": "§3: register publication date STRICTLY before the event date. A missing publication "
                    "date is a violation, not a pass -- sourced-or-unknown."}


# ------------------------------------------------------------------ estimation

def design(df, spec, mask):
    """The four registered specifications. R1: the 'class dummy' is the class indicator set, drop-first."""
    sub = df.loc[mask]
    cols, names = [np.ones(len(sub))], ["const"]
    if spec in ("A_dummy", "C_both"):
        types = sorted(df["type"].dropna().unique())[1:]       # drop-first
        for t in types:
            cols.append((sub["type"] == t).to_numpy(float)); names.append(f"class[{t}]")
    if spec in ("B_X3", "C_both"):
        cols.append(sub["X3_share"].to_numpy(float)); names.append("X3")
    if spec == "D_X1":
        cols.append(sub["X1_kbd"].to_numpy(float)); names.append("X1")
    return np.column_stack(cols), names


def _ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / sst if sst > 0 else np.nan
    return beta, r2


def spec_mask(df, spec, yv):
    m = np.isfinite(yv)
    if spec in ("B_X3", "C_both"):
        m &= np.isfinite(df["X3_share"].to_numpy(float))
    if spec == "D_X1":
        m &= np.isfinite(df["X1_kbd"].to_numpy(float))
    if spec in ("A_dummy", "C_both"):
        m &= df["type"].notna().to_numpy()
    return m


def cluster_boot_idx(clusters, rng, n_draw=None):
    """Resample SOURCE-EVENT CLUSTERS with replacement; every event of a drawn cluster travels with it."""
    uniq = np.unique(clusters)
    take = rng.choice(uniq, size=n_draw or len(uniq), replace=True)
    return np.concatenate([np.flatnonzero(clusters == c) for c in take])


def estimate(df, Y, target, h, n_boot=N_BOOT, seed=SEED):
    """All four specs at one (target, horizon), with cluster-bootstrap bands and the B-vs-A R2 difference."""
    yv = Y[target][h]
    out = {"target": target, "horizon": h, "specs": {}}
    fits = {}
    for spec in SPECS:
        m = spec_mask(df, spec, yv)
        if m.sum() < 12:
            out["specs"][spec] = {"note": f"only {int(m.sum())} usable events"}
            continue
        X, names = design(df, spec, m)
        y = yv[m]
        beta, r2 = _ols(X, y)
        cl = df.loc[m, "cluster"].to_numpy()
        rng = np.random.default_rng(seed + h)
        bb, br = [], []
        for _ in range(n_boot):
            ix = cluster_boot_idx(cl, rng)
            if len(ix) < X.shape[1] + 2:
                continue
            try:
                b_, r_ = _ols(X[ix], y[ix])
            except np.linalg.LinAlgError:
                continue
            bb.append(b_); br.append(r_)
        bb = np.array(bb)
        key = "X3" if spec in ("B_X3", "C_both") else ("X1" if spec == "D_X1" else None)
        blk = {"n_events": int(m.sum()), "n_clusters": int(len(np.unique(cl))),
               "unit_of_dependence": "source event (35-day cluster); n_clusters is the inferential n, "
                                     "n_events is not",
               "r2": round(float(r2), 5), "coefficients": {}}
        for j, nm in enumerate(names):
            lo, hi = (np.percentile(bb[:, j], [2.5, 97.5]) if len(bb) >= 50 else (np.nan, np.nan))
            blk["coefficients"][nm] = {"beta": round(float(beta[j]), 5),
                                       "ci95": [round(float(lo), 5), round(float(hi), 5)],
                                       "excludes_zero": bool(np.isfinite(lo) and (lo > 0 or hi < 0))}
        if key:
            blk["key_regressor"] = key
        out["specs"][spec] = blk
        fits[spec] = (X, y, cl, names, r2, m)

    # R2: "B beats A" needs the R-squared difference too, on the events where BOTH are estimable
    if "A_dummy" in fits and "B_X3" in fits:
        mA, mB = fits["A_dummy"][5], fits["B_X3"][5]
        m = mA & mB
        if m.sum() >= 12:
            XA, _ = design(df, "A_dummy", m); XB, _ = design(df, "B_X3", m)
            y = yv[m]; cl = df.loc[m, "cluster"].to_numpy()
            d0 = _ols(XB, y)[1] - _ols(XA, y)[1]
            rng = np.random.default_rng(seed + 991 + h)
            dd = []
            for _ in range(n_boot):
                ix = cluster_boot_idx(cl, rng)
                if len(ix) < max(XA.shape[1], XB.shape[1]) + 2:
                    continue
                try:
                    dd.append(_ols(XB[ix], y[ix])[1] - _ols(XA[ix], y[ix])[1])
                except np.linalg.LinAlgError:
                    continue
            lo, hi = (np.percentile(dd, [2.5, 97.5]) if len(dd) >= 50 else (np.nan, np.nan))
            out["r2_diff_B_minus_A"] = {"delta_r2": round(float(d0), 5),
                                        "ci95": [round(float(lo), 5), round(float(hi), 5)],
                                        "excludes_zero": bool(np.isfinite(lo) and (lo > 0 or hi < 0)),
                                        "n_events": int(m.sum()),
                                        "n_clusters": int(len(np.unique(cl)))}
    return out


# ------------------------------------------------------------------ the state-matched placebo (§5)

def placebo(df, series, tsr_all, target, h, n_boot=500, seed=SEED):
    """§5's state-matched placebo: each event's exposure is kept and re-dated to a non-event day in the
    SAME VIX-percentile decile, >= 30 days from any corpus event. X3's coefficient must cover zero."""
    vix = series.get("derived.vix_pct")
    if vix is None or target not in tsr_all:
        return {"note": "no VIX percentile series; placebo not run"}
    ev_dates = df["date"].to_numpy()
    vi, vv = vix.index.to_numpy(), vix.to_numpy(float)
    kind, s = tsr_all[target]
    cand = {}
    for d, v in zip(vi, vv):
        gap = np.min(np.abs((ev_dates - d).astype("timedelta64[D]").astype(int)))
        if gap < PLACEBO_EXCL_DAYS:
            continue
        cand.setdefault(int(min(9, max(0, v // 10))), []).append(d)
    rng = np.random.default_rng(seed)
    dec = []
    for d in ev_dates:
        j = np.searchsorted(vi, d) - 1
        dec.append(int(min(9, max(0, vv[j] // 10))) if j >= 0 else None)
    betas = []
    for _ in range(25):
        pseudo = []
        for k in dec:
            pool = cand.get(k) or []
            pseudo.append(pool[rng.integers(len(pool))] if len(pool) else np.datetime64("NaT"))
        yv = responses(tsr_all[target], np.array(pseudo))[h]
        m = np.isfinite(yv) & np.isfinite(df["X3_share"].to_numpy(float))
        if m.sum() < 12:
            continue
        X, names = design(df, "B_X3", m)
        b, _ = _ols(X, yv[m])
        betas.append(b[names.index("X3")])
    if len(betas) < 5:
        return {"note": f"only {len(betas)} placebo replicates"}
    lo, hi = np.percentile(betas, [2.5, 97.5])
    return {"reps": len(betas), "beta_mean": round(float(np.mean(betas)), 5),
            "ci95": [round(float(lo), 5), round(float(hi), 5)],
            "covers_zero": bool(lo <= 0 <= hi),
            "rule": "§5: X3's coefficient on state-matched pseudo-dates must be indistinguishable from "
                    "zero. A placebo that excludes zero voids the corresponding real estimate."}


# ------------------------------------------------------------------ §5 the verdict

def verdict(res):
    """§5's words, fixed before the numbers. NO ADDITION is a PERMITTED OUTCOME, not a failure."""
    head = {t: res["estimates"].get(f"{t}|h{HEADLINE_H}") for t in TARGETS}
    def ok(t, spec, key):
        b = ((head.get(t) or {}).get("specs") or {}).get(spec) or {}
        c = (b.get("coefficients") or {}).get(key) or {}
        return bool(c.get("excludes_zero")), c.get("beta")
    out = {"headline_horizon": HEADLINE_H, "per_target": {}, "rule": "PHYSICAL_EXPOSURE_REGISTRATION §5"}
    for t in TARGETS:
        h = head.get(t)
        if not h:
            out["per_target"][t] = "NOT ESTIMATED"; continue
        b_ex, b_beta = ok(t, "B_X3", "X3")
        r2 = (h.get("r2_diff_B_minus_A") or {})
        beats_A = bool(b_ex and r2.get("excludes_zero"))
        dummy_moves = None
        A = (h["specs"].get("A_dummy") or {}).get("coefficients") or {}
        C = (h["specs"].get("C_both") or {}).get("coefficients") or {}
        pairs = [(k, A[k]["beta"], C[k]["beta"]) for k in A if k.startswith("class[") and k in C]
        if pairs:
            dummy_moves = bool(np.mean([abs(c) for _, a, c in pairs]) < np.mean([abs(a) for _, a, c in pairs]))
        d_ex, d_beta = ok(t, "D_X1", "X1")
        label = ("MAGNITUDE CARRIES" if (beats_A and dummy_moves) else
                 "NO ADDITION" if not b_ex else "SUGGESTIVE -- B's band excludes zero but not the R2 gain")
        out["per_target"][t] = {
            "verdict": label,
            "B_X3_excludes_zero": b_ex, "B_X3_beta": b_beta,
            "r2_gain_excludes_zero": r2.get("excludes_zero"), "delta_r2": r2.get("delta_r2"),
            "dummy_moves_toward_zero_in_C": dummy_moves,
            "BUFFER_MATTERS": (None if (b_beta is None or d_beta is None) else
                               bool(b_ex and not d_ex)),
            "D_X1_excludes_zero": d_ex,
            "note": ("NO ADDITION is a registered permitted outcome (§5) and is not a failure of the study."
                     if label == "NO ADDITION" else None),
        }
    cracks = [out["per_target"][t] for t in CRACK_TARGETS if isinstance(out["per_target"].get(t), dict)]
    crude = [out["per_target"][t] for t in CRUDE_TARGETS if isinstance(out["per_target"].get(t), dict)]
    out["cowork_prediction_section_8"] = {
        "predicted": "T3 beats the dummy on the CRACK targets and not on crude flat price",
        "cracks_carry": bool(cracks) and all(c["verdict"] == "MAGNITUDE CARRIES" for c in cracks),
        "crude_carries": bool(crude) and any(c["verdict"] == "MAGNITUDE CARRIES" for c in crude),
        "registered_before_the_numbers": True,
    }
    p = out["cowork_prediction_section_8"]
    p["prediction_held"] = bool(p["cracks_carry"] and not p["crude_carries"])
    return out


# ------------------------------------------------------------------ run

def run(fast=False):
    exposure, path = load_exposure()
    df, Y, series, conn = build_panel(exposure)
    filt = filtration_test(df)
    n_boot = 200 if fast else N_BOOT
    res = {
        "study": "PHYSICAL_EXPOSURE_REGISTRATION.md §4 (2026-09-03)",
        "harness": "src/exposure_harness.py -- B owns estimation; K owns the exposure construction (§2)",
        "exposure_source": str(path.relative_to(ROOT)),
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registered": {"horizons": list(HORIZONS), "headline_h": HEADLINE_H, "specs": list(SPECS),
                       "targets": {k: {kk: vv for kk, vv in v.items()} for k, v in TARGETS.items()},
                       "cluster_days": CLUSTER_DAYS, "n_boot": n_boot, "seed": SEED, "fdr_q": FDR_Q},
        "readings_flagged_for_cowork": {
            "R1": "§4's 'class dummy' read as the 7-class indicator set, drop-first -- the only reading on "
                  "which spec A is estimable on an event-date sample",
            "R2": "'B beats A' read as X3's band excluding zero AND the band on R2(B) - R2(A) excluding zero",
            "R3": TARGETS["reroute"]["construction"] + " (PortWatch from 2019 only; never pooled)",
            "R4": "fertilizer is an EQUITY proxy (yf.eq_mos), not a fertilizer price",
        },
        "schema_expected": schema_doc(),
        "filtration_test": filt,
        "exclusions": {
            "n_events_joined": int(len(df)),
            "X1_null": int(df["X1_kbd"].isna().sum()),
            "X3_null_pre_2003_or_no_register": int(df["X3_share"].isna().sum()),
            "rule": "§2: a missing register gives NULL, never zero; the event is excluded and counted",
        },
        "estimates": {}, "placebo": {},
    }
    if not filt["asserted"]:
        res["status"] = "VOID -- the §3 filtration test failed; no estimate is computed"
        return res

    tsr_all = target_series(series)
    fdr_names, fdr_p = [], []
    for t in TARGETS:
        if t not in Y:
            res["estimates"][f"{t}|unavailable"] = {"note": "target series not in the tree"}
            continue
        for h in HORIZONS:
            e = estimate(df, Y, t, h, n_boot=n_boot)
            res["estimates"][f"{t}|h{h}"] = e
            b = (e["specs"].get("B_X3") or {}).get("coefficients", {}).get("X3")
            if b and np.isfinite(b["ci95"][0]):
                # a two-sided bootstrap p from the band's symmetric tail position
                lo, hi = b["ci95"]; beta = b["beta"]
                half = (hi - lo) / 2 or np.nan
                z = abs(beta) / (half / 1.96) if half and np.isfinite(half) else np.nan
                fdr_names.append(f"{t}|h{h}|B_X3"); fdr_p.append(float(2 * (1 - INF.norm_cdf(z))) if np.isfinite(z) else 1.0)
        res["placebo"][t] = placebo(df, series, tsr_all, t, HEADLINE_H, n_boot=n_boot)
    if fdr_p:
        res["fdr"] = {"names": fdr_names, "p": fdr_p, "bh": INF.bh_fdr(fdr_p, q=FDR_Q),
                      "note": "§5: BH-FDR across the family of B_X3 coefficients over all targets and "
                              "horizons. A comparison that does not survive is not a finding."}
    res["verdict"] = verdict(res)
    res["cannot"] = ("make anything VALIDATED -- §7's label audit is unpassed (registration §5)")
    return res


def main():
    if exposure_path() is None:
        print(json.dumps({
            "gated": True,
            "reason": "K's exposure file is not in the tree; this harness constructs no exposure value (§2)",
            "expected": ["data/exposure.json", "data/exposure.csv"],
            "schema_expected": schema_doc(),
            "readings_flagged_for_cowork": ["R1 class dummy = class indicator set", "R2 beats = coef AND R2 gain",
                                            "R3 reroute construction declared", "R4 fertilizer is an equity proxy"],
            "targets": list(TARGETS), "horizons": list(HORIZONS), "headline_h": HEADLINE_H,
        }, indent=1))
        return
    res = run(fast="--fast" in sys.argv)
    OUT.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({k: res[k] for k in ("filtration_test", "exclusions", "verdict") if k in res},
                     indent=1, default=str)[:4000])


if __name__ == "__main__":
    main()
