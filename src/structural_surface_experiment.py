"""Frozen central experiment: structural versus surface historical analogy.

This module implements registrations/STRUCTURAL_SURFACE_EXPERIMENT.md.  It writes only beneath
data/structural_surface and never changes the existing walk or grid ledgers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from engine import inference as INF

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "structural_surface"
BUNDLE = OUT / "input"
REGISTRATION = ROOT / "registrations" / "STRUCTURAL_SURFACE_EXPERIMENT.md"
CODEBOOK = ROOT / "docs" / "reference" / "WORLD_STATE_CODEBOOK.md"
BRENT = "fred.DCOILBRENTEU"
MARKET_SERIES = {"brent": BRENT, "wti": "fred.DCOILWTICO", "vix": "fred.VIXCLS"}
HORIZON = 20
EST_WINDOW = 250
EST_GAP = 21
EST_MIN = 100
MIN_POOL = 8
MIN_FIELDS = 3
MIN_SCALE_N = 30
TAU = 0.25
SEED = 19900802


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def seal(record):
    """Hash the forecast before an outcome is attached."""
    out = dict(record)
    out["hash"] = hashlib.sha256(canonical(record).encode()).hexdigest()
    return out


def verify_seal(record):
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(canonical(body).encode()).hexdigest() == record.get("hash")


def weighted_crps(atoms, weights, y):
    """CRPS for a weighted empirical distribution, including unequal weights."""
    x = np.asarray(atoms, float); w = np.asarray(weights, float)
    if len(x) == 0 or len(x) != len(w) or not np.isfinite(y):
        return np.nan
    good = np.isfinite(x) & np.isfinite(w) & (w >= 0)
    x, w = x[good], w[good]
    if not len(x) or w.sum() <= 0:
        return np.nan
    w = w / w.sum()
    return float(np.sum(w * np.abs(x - y)) - 0.5 * np.sum((w[:, None] * w[None, :]) * np.abs(x[:, None] - x[None, :])))


def kernel_weights(distances, tau=TAU):
    d = np.asarray(distances, float)
    w = np.exp(-d / tau)
    return w / w.sum()


def surface_distances(target_type, candidate_types):
    return np.asarray([0.0 if x == target_type else 1.0 for x in candidate_types], float)


def codebook_blocks():
    """Field -> block. The codebook is metadata; values still come only from the database."""
    out = {}
    for line in CODEBOOK.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| block") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8:
            out[cells[1]] = cells[0].lower()
    return out


def strict_panel_rows(conn):
    """Rows whose own stored receipts establish availability by their event date."""
    q = """
      SELECT s.event_id,s.field,s.value,s.value_text,s.entity_id
      FROM situation_state s JOIN events e ON e.event_id=s.event_id
      WHERE s.entity_id!='situation' AND s.obs_date<=e.event_date
        AND s.vintage<=e.event_date AND s.release<=e.event_date AND s.retrospective=0
      ORDER BY s.event_id,s.field,s.entity_id
    """
    return conn.execute(q).fetchall()


def connect_bundle(bundle):
    """Reconstruct only the three read-only tables used by the experiment from committed CSVs."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
      CREATE TABLE events(event_id TEXT,event_date TEXT,type TEXT,title TEXT,date_precision TEXT);
      CREATE TABLE observations(series_id TEXT,obs_date TEXT,value REAL,as_of TEXT);
      CREATE TABLE situation_state(event_id TEXT,entity_id TEXT,field TEXT,obs_date TEXT,value REAL,
        value_text TEXT,vintage TEXT,release TEXT,retrospective INTEGER,source TEXT,joined_at TEXT);
    """)
    specs = {
        "events.csv": ("events", ("event_id", "event_date", "type", "title", "date_precision")),
        "market_observations.csv": ("observations", ("series_id", "obs_date", "value", "as_of")),
        "situation_state.csv": ("situation_state", ("event_id", "entity_id", "field", "obs_date", "value",
                                                       "value_text", "vintage", "release", "retrospective", "source", "joined_at")),
    }
    for name, (table, cols) in specs.items():
        with (bundle / name).open(newline="", encoding="utf-8") as f:
            rows = []
            for r in csv.DictReader(f):
                rows.append(tuple(None if r[c] == "" else r[c] for c in cols))
        conn.executemany(f"INSERT INTO {table} VALUES ({','.join('?' for _ in cols)})", rows)
    conn.executescript("""
      CREATE INDEX idx_bundle_events ON events(event_date,event_id);
      CREATE INDEX idx_bundle_obs ON observations(series_id,obs_date,as_of);
      CREATE INDEX idx_bundle_state ON situation_state(event_id,field,entity_id);
    """)
    return conn


def reduce_panel(rows, blocks=None):
    """Apply registered Amendment 1 to event/entity rows."""
    blocks = blocks or {}
    grouped = defaultdict(list)
    for eid, field, value, value_text, entity in rows:
        grouped[(eid, field)].append((value, value_text, entity))
    vecs, meta = defaultdict(dict), defaultdict(dict)
    for (eid, field), vals in grouped.items():
        nums = [float(v) for v, _, _ in vals if v is not None and np.isfinite(float(v))]
        texts = sorted({str(vt) for _, vt, _ in vals if vt not in (None, "", "unknown")})
        if nums:
            value, kind = float(np.mean(nums)), "num"
        elif texts:
            value, kind = "|".join(texts), "cat"
        else:
            continue
        key = f"panel:{field}"
        vecs[eid][key] = value
        meta[eid][key] = {"block": blocks.get(field, "panel"), "kind": kind,
                          "n_entities": len({e for _, _, e in vals})}
    return vecs, meta


def latest_available_series(conn, sid, as_of):
    """Latest vintage per observation date, constrained by stored as_of."""
    df = pd.read_sql_query(
        "SELECT obs_date,value,as_of FROM observations WHERE series_id=? AND value IS NOT NULL "
        "AND obs_date<? AND as_of IS NOT NULL AND as_of<=? ORDER BY obs_date,as_of",
        conn, params=(sid, as_of, as_of))
    if df.empty:
        return pd.Series(dtype=float)
    df = df.drop_duplicates("obs_date", keep="last")
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    return df.set_index("obs_date")["value"].astype(float)


def market_vector(conn, event_date):
    held = {name: latest_available_series(conn, sid, event_date) for name, sid in MARKET_SERIES.items()}
    out, meta = {}, {}
    for name in ("brent", "wti"):
        s = held[name]
        if len(s) >= 21 and s.iloc[-21] > 0 and s.iloc[-1] > 0:
            key = f"market:{name}_chg20"
            out[key] = float(100 * np.log(s.iloc[-1] / s.iloc[-21]))
            meta[key] = {"block": "market", "kind": "num", "n_entities": 1}
    b = held["brent"]
    if len(b) >= 21:
        ret = np.diff(np.log(b.iloc[-21:].to_numpy(float)))
        if np.isfinite(ret).all():
            out["market:brent_vol20"] = float(np.std(ret, ddof=1) * np.sqrt(252) * 100)
            meta["market:brent_vol20"] = {"block": "market", "kind": "num", "n_entities": 1}
    v = held["vix"]
    if len(v):
        out["market:vix_close"] = float(v.iloc[-1])
        meta["market:vix_close"] = {"block": "market", "kind": "num", "n_entities": 1}
    return out, meta


def latest_full_series(conn, sid):
    df = pd.read_sql_query("SELECT obs_date,value,as_of FROM observations WHERE series_id=? AND value IS NOT NULL ORDER BY obs_date,as_of", conn, params=(sid,))
    if df.empty:
        return pd.Series(dtype=float)
    df = df.drop_duplicates("obs_date", keep="last")
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    return df.set_index("obs_date")["value"].astype(float).sort_index()


def abnormal_outcome(series, event_date, horizon=HORIZON):
    """Registered constant-mean abnormal return and its closing date."""
    t = pd.Timestamp(event_date)
    pos = int(series.index.searchsorted(t))
    anchor = pos - 1
    end = pos + horizon
    est_end = pos - EST_GAP + 1
    est_start = est_end - EST_WINDOW
    if anchor < 0 or end >= len(series) or est_start < 1:
        return None
    levels = series.to_numpy(float)
    rets = np.diff(np.log(levels), prepend=np.nan)
    est = rets[est_start:est_end]
    est = est[np.isfinite(est)]
    if len(est) < EST_MIN or levels[anchor] <= 0 or levels[end] <= 0:
        return None
    raw = float(100 * np.log(levels[end] / levels[anchor]))
    return {"value": raw - float(100 * horizon * est.mean()), "raw": raw,
            "closed_on": str(series.index[end].date()), "n_est": int(len(est))}


def outcome_design(series, event_date, horizon=HORIZON):
    """Check target availability without reading the post-event value or computing the outcome."""
    pos = int(series.index.searchsorted(pd.Timestamp(event_date)))
    anchor, end = pos - 1, pos + horizon
    est_end, est_start = pos - EST_GAP + 1, pos - EST_GAP + 1 - EST_WINDOW
    if anchor < 0 or end >= len(series) or est_start < 1:
        return None
    rets = np.diff(np.log(series.iloc[:anchor + 1].to_numpy(float)), prepend=np.nan)
    n_est = int(np.isfinite(rets[est_start:est_end]).sum())
    if n_est < EST_MIN:
        return None
    return {"closed_on": str(series.index[end].date()), "n_est": n_est}


def structural_distance(target, candidate, history, target_date, target_meta, candidate_meta):
    """Existing block-wise distance, with scaling learned only from earlier event states."""
    common = sorted(set(target) & set(candidate))
    per_block = defaultdict(list)
    fields = []
    for field in common:
        kind = target_meta.get(field, {}).get("kind") or candidate_meta.get(field, {}).get("kind")
        block = target_meta.get(field, {}).get("block") or candidate_meta.get(field, {}).get("block") or "panel"
        a, b = target[field], candidate[field]
        if kind == "cat":
            d = 0.0 if str(a) == str(b) else 1.0
        else:
            prior = [float(v[field]) for date, v in history if date < target_date and field in v and isinstance(v[field], (int, float, np.number))]
            if len(prior) < MIN_SCALE_N:
                continue
            sd = float(np.std(prior, ddof=0))
            if not np.isfinite(sd) or sd <= 0:
                continue
            d = min(abs(float(a) - float(b)) / sd / 3.0, 1.0)
        per_block[block].append(float(d)); fields.append(field)
    if len(fields) < MIN_FIELDS:
        return None
    bd = {b: float(np.mean(x)) for b, x in per_block.items()}
    return {"distance": float(np.mean(list(bd.values()))), "n_fields": len(fields),
            "fields": fields, "blocks": bd}


def cluster_mean_block(dates, days=35):
    if not dates:
        return 1.0
    sizes, n = [], 1
    for a, b in zip(dates, dates[1:]):
        if (b - a).days <= days:
            n += 1
        else:
            sizes.append(n); n = 1
    sizes.append(n)
    return float(np.mean(sizes))


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def paired_block(a, b, dates, n_boot):
    """Registered date-level paired inference, reused by primary and diagnostics."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    mean_block = cluster_mean_block([pd.Timestamp(x) for x in dates])
    lag = max(int(np.ceil(mean_block)) - 1, 0)
    dm = INF.dm_test(a, b, h=1, lag=lag) if len(a) else {"ok": False, "n": 0}
    ci = INF.bootstrap_ci(lambda ix: float(np.mean((a - b)[ix])), len(a), n_boot=n_boot,
                          mean_block=mean_block, seed=SEED) if len(a) else {
                              "estimate": None, "lo": None, "hi": None, "n_boot": 0}
    return {"n": len(a), "mean_a": float(np.mean(a)) if len(a) else None,
            "mean_b": float(np.mean(b)) if len(b) else None,
            "mean_diff": ci.get("estimate"), "ci95": [ci.get("lo"), ci.get("hi")],
            "dm": dm, "mean_block": mean_block, "n_boot": n_boot}


def run(db=DB, bundle=None, out_dir=OUT, n_boot=2000):
    conn = connect_bundle(Path(bundle)) if bundle else sqlite3.connect(db)
    try:
        events = [dict(zip(("event_id", "event_date", "type", "title", "date_precision"), r)) for r in conn.execute(
            "SELECT event_id,event_date,type,title,date_precision FROM events ORDER BY event_date,event_id")]
        panel, panel_meta = reduce_panel(strict_panel_rows(conn), codebook_blocks())
        vectors, metadata = {}, {}
        for e in events:
            mv, mm = market_vector(conn, e["event_date"])
            vectors[e["event_id"]] = {**panel.get(e["event_id"], {}), **mv}
            metadata[e["event_id"]] = {**panel_meta.get(e["event_id"], {}), **mm}
        brent = latest_full_series(conn, BRENT)
    finally:
        conn.close()

    outcomes = {}
    history = [(e["event_date"], vectors[e["event_id"]]) for e in events]
    reads, scores, abstain = [], [], defaultdict(int)
    for e in events:
        target_design = outcome_design(brent, e["event_date"])
        if e["date_precision"] != "day" or target_design is None:
            abstain["target_unusable"] += 1; continue
        candidates, details = [], []
        for c in events:
            if c["event_date"] >= e["event_date"]:
                continue
            if c["event_id"] not in outcomes:
                outcomes[c["event_id"]] = {h: abnormal_outcome(brent, c["event_date"], h) for h in (5, 10, 20)}
            co = outcomes[c["event_id"]][20]
            if co is None or co["closed_on"] >= e["event_date"]:
                continue
            sd = structural_distance(vectors[e["event_id"]], vectors[c["event_id"]], history,
                                     e["event_date"], metadata[e["event_id"]], metadata[c["event_id"]])
            if sd is None:
                continue
            candidates.append(c); details.append(sd)
        if len(candidates) < MIN_POOL:
            abstain["pool_lt_8"] += 1; continue
        ds = np.asarray([x["distance"] for x in details])
        du = surface_distances(e["type"], [c["type"] for c in candidates])
        ws, wu = kernel_weights(ds), kernel_weights(du)
        forecasts = {}
        for h in (5, 10, 20):
            forecasts[str(h)] = {
                "abnormal_atoms": [outcomes[c["event_id"]][h]["value"] for c in candidates],
                "raw_atoms": [outcomes[c["event_id"]][h]["raw"] for c in candidates],
            }
        read = seal({"event_id": e["event_id"], "date": e["event_date"], "type": e["type"],
                     "candidate_ids": [c["event_id"] for c in candidates], "forecasts": forecasts,
                     "structural": {"distances": ds.tolist(), "weights": ws.tolist(), "detail": details},
                     "surface": {"distances": du.tolist(), "weights": wu.tolist()},
                     "n_pool": len(candidates), "target_n_fields": len(vectors[e["event_id"]]),
                     "structural_n_eff": float(1 / np.sum(ws * ws)),
                     "surface_n_eff": float(1 / np.sum(wu * wu))})
        assert verify_seal(read)
        # The target outcome is looked up only after the complete forecast object has been sealed.
        target_outcomes = {h: abnormal_outcome(brent, e["event_date"], h) for h in (5, 10, 20)}
        assert target_outcomes[20] is not None
        outcomes[e["event_id"]] = target_outcomes
        diag = {}
        for h in (5, 10, 20):
            ho, hf = target_outcomes[h], forecasts[str(h)]
            unif = np.ones(len(candidates)) / len(candidates)
            diag[str(h)] = {
                "outcome": ho["value"], "raw_outcome": ho["raw"],
                "abnormal": {"structural": weighted_crps(hf["abnormal_atoms"], ws, ho["value"]),
                             "surface": weighted_crps(hf["abnormal_atoms"], wu, ho["value"]),
                             "uniform": weighted_crps(hf["abnormal_atoms"], unif, ho["value"])},
                "raw": {"structural": weighted_crps(hf["raw_atoms"], ws, ho["raw"]),
                        "surface": weighted_crps(hf["raw_atoms"], wu, ho["raw"]),
                        "uniform": weighted_crps(hf["raw_atoms"], unif, ho["raw"])}}
        primary = diag["20"]["abnormal"]
        reads.append(read)
        scores.append({"event_id": e["event_id"], "date": e["event_date"], "read_hash": read["hash"],
                       "outcome": target_outcomes[20]["value"], "raw_return": target_outcomes[20]["raw"],
                       "structural_crps": primary["structural"], "surface_crps": primary["surface"],
                       "uniform_crps": primary["uniform"],
                       "loss_diff": primary["structural"] - primary["surface"], "diagnostics": diag})

    by_date = defaultdict(list)
    for s in scores:
        by_date[s["date"]].append(s)
    dates = sorted(by_date)
    a = np.asarray([np.mean([x["structural_crps"] for x in by_date[d]]) for d in dates])
    b = np.asarray([np.mean([x["surface_crps"] for x in by_date[d]]) for d in dates])
    primary_comparison = paired_block(a, b, dates, n_boot)
    est, (lo, hi), dm = primary_comparison["mean_diff"], primary_comparison["ci95"], primary_comparison["dm"]
    p = dm.get("p_value")
    if len(a) < 30:
        verdict = "INSUFFICIENT"
    elif est is not None and est < 0 and lo is not None and hi < 0 and p is not None and p < 0.05:
        verdict = "STRUCTURE ADDS INFORMATION"
    elif est is not None and est > 0 and lo is not None and lo > 0 and p is not None and p < 0.05:
        verdict = "SURFACE PERFORMS BETTER"
    else:
        verdict = "NOT DISTINGUISHABLE ON THIS RECORD"
    summary = {"registration": str(REGISTRATION.relative_to(ROOT)), "primary": "Brent abnormal return +20td",
               "n_event_reads": len(reads), "n_inferential_dates": len(dates), "abstentions": dict(abstain),
               "mean_loss": {"structural": float(np.mean(a)) if len(a) else None,
                             "surface": float(np.mean(b)) if len(b) else None},
               "mean_loss_diff_structural_minus_surface": est, "ci95": [lo, hi], "dm": dm,
               "mean_block": primary_comparison["mean_block"], "n_boot": n_boot, "verdict": verdict,
               "pool": {"min": min((r["n_pool"] for r in reads), default=None),
                        "median": float(np.median([r["n_pool"] for r in reads])) if reads else None,
                        "max": max((r["n_pool"] for r in reads), default=None)},
               "effective_weight_n_median": {
                   "structural": float(np.median([r["structural_n_eff"] for r in reads])) if reads else None,
                   "surface": float(np.median([r["surface_n_eff"] for r in reads])) if reads else None}}
    # Registered non-verdict pooling comparator and target/horizon diagnostics.
    diagnostics = {}
    for target_kind in ("abnormal", "raw"):
        diagnostics[target_kind] = {}
        for h in (5, 10, 20):
            aa = np.asarray([np.mean([x["diagnostics"][str(h)][target_kind]["structural"] for x in by_date[d]]) for d in dates])
            bb = np.asarray([np.mean([x["diagnostics"][str(h)][target_kind]["surface"] for x in by_date[d]]) for d in dates])
            uu = np.asarray([np.mean([x["diagnostics"][str(h)][target_kind]["uniform"] for x in by_date[d]]) for d in dates])
            diagnostics[target_kind][str(h)] = {
                "structural_vs_surface": paired_block(aa, bb, dates, n_boot),
                "structural_vs_uniform": paired_block(aa, uu, dates, n_boot),
                "surface_vs_uniform": paired_block(bb, uu, dates, n_boot)}
    summary["diagnostics_non_verdict"] = diagnostics

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "reads.jsonl").write_text("".join(canonical(x) + "\n" for x in reads))
    (out_dir / "scores.jsonl").write_text("".join(canonical(x) + "\n" for x in scores))
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        commit = None
    if bundle:
        bundle_path = Path(bundle).resolve()
        input_files = {p.name: file_hash(p) for p in sorted(bundle_path.glob("*.csv"))}
        source_input = {"bundle": {"path": str(bundle_path.relative_to(ROOT)), "files": input_files}}
    else:
        source_input = {"database": {"path": str(Path(db).relative_to(ROOT)) if Path(db).is_relative_to(ROOT) else str(db),
                                      "sha256": file_hash(db)}}
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(), "implementation_commit": commit,
                "inputs": {**source_input,
                           "registration": {"path": str(REGISTRATION.relative_to(ROOT)), "sha256": file_hash(REGISTRATION)}},
                "outputs": {name: file_hash(out_dir / name) for name in ("reads.jsonl", "scores.jsonl", "summary.json")}}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true", help="200 bootstrap draws; never publication output")
    ap.add_argument("--db", type=Path, default=DB)
    ap.add_argument("--bundle", type=Path)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    result = run(db=args.db, bundle=args.bundle, out_dir=args.out, n_boot=200 if args.fast else 2000)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
