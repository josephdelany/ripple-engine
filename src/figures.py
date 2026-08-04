"""
figures.py -- the figures pack. Papers need pictures; this makes them.

Six publication figures into data/figures/ (PNG, 150 dpi, one consistent style,
every axis labelled with its unit, and n printed on every panel so no picture ever
overstates its evidence). It generates NO new analysis -- it draws the numbers the
engine already computes, reusing event_study / robustness / inference / cross_asset
by import only.

  f1  mean CAR path per event type (clustered), the t-5..t+20 window
  f2  conflict-escalation CAR+20 per event, sorted (the dispersion picture)
  f3  H1 (VIX) conditioning: high vs low |CAR+20|, raw / clustered / standardized
  f4  cross-asset propagation heatmap (event type x asset, CAR+20, units annotated)
  f5  quiet set vs corpus |CAR+20| (box + strip)
  f6  policy_response vs conflict_escalation mean CAR paths, overlaid

Run:  python3 src/figures.py
"""

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from event_study import car_for_event, PRE, POST
from robustness import assign_clusters
from cross_asset import asset_returns, ASSETS, build_table, propagation_summary
from inference import build_frame, samples, split_amp, CAR20_LEN

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FIGDIR = ROOT / "data" / "figures"
BRENT = "fred.DCOILBRENTEU"

# Consistent style + a fixed per-type palette so a type is the same colour everywhere.
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150, "font.size": 10,
                     "axes.titlesize": 12, "axes.grid": True, "grid.alpha": 0.25,
                     "axes.axisbelow": True, "figure.facecolor": "white"})
TYPE_COLOR = {
    "conflict_escalation": "#c0392b", "opec_decision": "#2c7fb8",
    "sanctions": "#7b3294", "infrastructure_attack": "#e08214",
    "chokepoint_disruption": "#1a9850", "demand_shock": "#636363",
    "policy_response": "#00838f",
}


def _event_frame(conn):
    """One row per event with its full CAR path + type, clustered (first kept)."""
    ret = asset_returns(conn, BRENT, "price")
    events = pd.read_sql("SELECT event_id, event_date AS date, type FROM events "
                         "ORDER BY event_date", conn)
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["date"])
        if car is None:
            continue
        rows.append({"event_id": ev["event_id"], "date": ev["date"],
                     "type": ev["type"], "path": car, "car20": car[PRE + 20] * 100})
    return assign_clusters(pd.DataFrame(rows))


def f1_mean_paths(clustered):
    rel = np.arange(-PRE, POST + 1)
    fig, ax = plt.subplots(figsize=(8, 5))
    for etype, grp in clustered.groupby("type"):
        paths = np.vstack(grp["path"].to_list()) * 100
        ax.plot(rel, paths.mean(axis=0), lw=2, color=TYPE_COLOR.get(etype, "#333"),
                label=f"{etype} (n={len(grp)})")
    ax.axvline(0, color="k", lw=0.8, ls="--", alpha=0.6)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xlabel("trading days relative to event (0 = event)")
    ax.set_ylabel("mean cumulative abnormal return, Brent (%)")
    ax.set_title("F1 — Mean ripple by event type (clustered)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIGDIR / "f1_mean_car_paths.png"); plt.close(fig)


def f2_conflict_dispersion(clustered):
    conf = clustered[clustered["type"] == "conflict_escalation"].sort_values("car20")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    colors = ["#c0392b" if v >= 0 else "#2c7fb8" for v in conf["car20"]]
    ax.barh(range(len(conf)), conf["car20"], color=colors)
    ax.set_yticks(range(len(conf)))
    ax.set_yticklabels([e[:26] for e in conf["event_id"]], fontsize=7)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("CAR+20, Brent (%)")
    ax.set_title(f"F2 — Conflict escalation: CAR+20 per event (n={len(conf)})\n"
                 f"mean {conf['car20'].mean():+.1f}%, "
                 f"range [{conf['car20'].min():+.1f}%, {conf['car20'].max():+.1f}%]")
    fig.tight_layout(); fig.savefig(FIGDIR / "f2_conflict_dispersion.png"); plt.close(fig)


def f3_h1_conditioning(conn):
    df, _ = build_frame(conn)
    baseline, clustered, _ = [s[1] for s in samples(df)]
    panels = [("raw (baseline)", baseline, "abs_car_raw", "|CAR+20| (%)", 1.0),
              ("raw (clustered)", clustered, "abs_car_raw", "|CAR+20| (%)", 1.0),
              ("standardized (clustered)", clustered, "abs_car_std",
               "|CAR+20| (sigma)", 100.0)]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2))
    for ax, (title, samp, mag, ylab, scale) in zip(axes, panels):
        r = split_amp(samp, "vix", mag)
        if r is None:
            ax.set_title(title + "\n(too few)"); continue
        hi, lo = r["hi_mean"] / scale, r["lo_mean"] / scale
        ax.bar(["high VIX", "low VIX"], [hi, lo],
               color=["#c0392b", "#2c7fb8"])
        ax.set_title(f"{title}\nn={r['n']} (hi {r['n_hi']} / lo {r['n_lo']})")
        ax.set_ylabel(ylab)
        for i, v in enumerate([hi, lo]):
            ax.text(i, v, f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    fig.suptitle("F3 — H1 (VIX) conditioning: |CAR+20| high vs low VIX", y=1.02)
    fig.tight_layout(); fig.savefig(FIGDIR / "f3_h1_conditioning.png",
                                    bbox_inches="tight"); plt.close(fig)


def f4_propagation_heatmap(conn):
    summary = propagation_summary(build_table(conn))
    types = list(summary.keys())
    assets = [a["label"] for a in ASSETS]
    grid = np.array([[summary[t]["cells"][a["series"]]["car20"] or np.nan
                      for a in ASSETS] for t in types])
    # Colour each column on its own scale (units differ: % vs bps); annotate raw.
    norm = np.zeros_like(grid)
    for j in range(grid.shape[1]):
        col = grid[:, j]
        m = np.nanmax(np.abs(col)) or 1
        norm[:, j] = col / m
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.imshow(norm, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(assets)))
    ax.set_xticklabels([f"{a['label']}\n({a['unit']})" for a in ASSETS], fontsize=8)
    ax.set_yticks(range(len(types)))
    ax.set_yticklabels([f"{t} (n={summary[t]['n_type']})" for t in types], fontsize=8)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            v = grid[i, j]
            ax.text(j, i, "n/a" if np.isnan(v) else f"{v:+.1f}", ha="center",
                    va="center", fontsize=7,
                    color="black" if abs(norm[i, j]) < 0.6 else "white")
    ax.set_title("F4 — Cross-asset propagation: clustered mean CAR+20\n"
                 "(colour normalised per column; units differ — see cells)")
    fig.tight_layout(); fig.savefig(FIGDIR / "f4_propagation_heatmap.png"); plt.close(fig)


def f5_quiet_vs_corpus(conn, clustered):
    from quiet_compare import FUJAIRAH_ID
    main_abs = clustered["car20"].abs().to_numpy()
    ret = asset_returns(conn, BRENT, "price")
    quiet = pd.read_sql("SELECT event_id, event_date FROM quiet_events", conn)
    q = []
    for _, ev in quiet.iterrows():
        if ev["event_id"] == FUJAIRAH_ID:
            continue
        car = car_for_event(ret, ev["event_date"])
        if car is not None:
            q.append(abs(car[PRE + 20]) * 100)
    q = np.array(q)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.boxplot([q, main_abs], tick_labels=[f"quiet set\n(n={len(q)})",
               f"main corpus\n(n={len(main_abs)})"], widths=0.5,
               showfliers=False)
    for i, data in enumerate([q, main_abs], 1):
        ax.scatter(np.random.default_rng(1).normal(i, 0.05, len(data)), data,
                   alpha=0.6, s=22, color="#c0392b" if i == 1 else "#2c7fb8", zorder=3)
    ax.set_ylabel("|CAR+20|, Brent (%)")
    ax.set_title("F5 — Quiet set vs main corpus |CAR+20|\n(Fujairah excluded; "
                 "descriptive, small n)")
    fig.tight_layout(); fig.savefig(FIGDIR / "f5_quiet_vs_corpus.png"); plt.close(fig)


def f6_policy_vs_conflict(clustered):
    rel = np.arange(-PRE, POST + 1)
    fig, ax = plt.subplots(figsize=(8, 5))
    for etype in ("policy_response", "conflict_escalation"):
        grp = clustered[clustered["type"] == etype]
        if grp.empty:
            continue
        paths = np.vstack(grp["path"].to_list()) * 100
        ax.plot(rel, paths.mean(axis=0), lw=2.2, color=TYPE_COLOR[etype],
                label=f"{etype} (n={len(grp)})")
    ax.axvline(0, color="k", lw=0.8, ls="--", alpha=0.6)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xlabel("trading days relative to event")
    ax.set_ylabel("mean CAR, Brent (%)")
    ax.set_title("F6 — Policy response vs conflict escalation (mean paths, clustered)")
    ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(FIGDIR / "f6_policy_vs_conflict.png"); plt.close(fig)


def f7_chain_heatmap():
    """V5.2 -- value-chain hop-by-hop correlation heatmap (upstream x downstream), from chain_view.json."""
    import json
    hops = json.loads((ROOT / "data" / "chain_view.json").read_text()).get("hops", [])
    hops = [h for h in hops if h.get("result")]
    if not hops:
        return
    ups = list(dict.fromkeys(h["up_label"] for h in hops))
    downs = list(dict.fromkeys(h["down_label"] for h in hops))
    grid = np.full((len(downs), len(ups)), np.nan)
    for h in hops:
        grid[downs.index(h["down_label"]), ups.index(h["up_label"])] = h["result"]["corr"]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.imshow(grid, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(ups))); ax.set_xticklabels(ups, fontsize=8, rotation=30, ha="right")
    ax.set_yticks(range(len(downs))); ax.set_yticklabels(downs, fontsize=8)
    for h in hops:
        i, j = downs.index(h["down_label"]), ups.index(h["up_label"])
        ax.text(j, i, f"{h['result']['corr']:+.2f}\n{h['result']['strength'][:4]}", ha="center",
                va="center", fontsize=7, color="black" if abs(grid[i, j]) < 0.6 else "white")
    ax.set_title("F7 — Value chain: hop-by-hop return correlation\n"
                 "(upstream → downstream; cadence per hop in chain_report.txt)")
    fig.tight_layout(); fig.savefig(FIGDIR / "f7_chain_heatmap.png"); plt.close(fig)


def f8_corpus_growth(conn):
    """V5.2 -- cumulative verified events over time (the corpus accreting)."""
    dates = [d for (d,) in conn.execute(
        "SELECT event_date FROM events WHERE event_date IS NOT NULL ORDER BY event_date")]
    x = [pd.Timestamp(d) for d in dates]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.step(x, range(1, len(x) + 1), where="post", color="#2c7fb8", lw=2)
    ax.set_ylabel("cumulative verified events"); ax.set_xlabel("event date")
    ax.set_title(f"F8 — Corpus growth ({len(x)} verified events)")
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGDIR / "f8_corpus_growth.png"); plt.close(fig)


def f9_calibration():
    """V5.2 -- reliability plot from the forecast log (observed vs forecast, vs the perfect diagonal)."""
    import json
    p = ROOT / "data" / "calibration_report.json"
    rep = json.loads(p.read_text()) if p.exists() else {}
    bins = (rep.get("overall") or {}).get("reliability", []) if rep.get("ran") else []
    if not bins:
        return
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.plot([0, 1], [0, 1], ls="--", color="grey", lw=1, label="perfect calibration")
    ax.plot([b["mean_forecast"] for b in bins], [b["observed"] for b in bins], "-o",
            color="#2c7fb8", label="engine")
    for b in bins:
        ax.annotate(f"n={b['n']}", (b["mean_forecast"], b["observed"]), fontsize=7,
                    textcoords="offset points", xytext=(5, -8))
    o = rep.get("overall", {})
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("forecast probability"); ax.set_ylabel("observed frequency")
    ax.set_title(f"F9 — Calibration (n={o.get('n')}, Brier {o.get('brier')}, "
                 f"skill {o.get('skill_vs_base')})")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGDIR / "f9_calibration.png"); plt.close(fig)


def main():
    FIGDIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    clustered = _event_frame(conn)
    f1_mean_paths(clustered)
    f2_conflict_dispersion(clustered)
    f3_h1_conditioning(conn)
    f4_propagation_heatmap(conn)
    f5_quiet_vs_corpus(conn, clustered)
    f6_policy_vs_conflict(clustered)
    f7_chain_heatmap()            # V5.2
    f8_corpus_growth(conn)        # V5.2
    f9_calibration()              # V5.2
    conn.close()
    pngs = sorted(p.name for p in FIGDIR.glob("*.png"))
    print(f"Wrote {len(pngs)} figures to {FIGDIR}:")
    for p in pngs:
        print(f"  {p}")


if __name__ == "__main__":
    main()
