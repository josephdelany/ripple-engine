"""Render one small, inspectable instrument demonstration from a frozen sealed read."""
import csv
import json
from pathlib import Path

import numpy as np

import structural_surface_experiment as E

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "structural_surface"
DEFAULT_EVENT = "hormuz_closure_2026"


def weighted_quantile(values, weights, q):
    x, w = np.asarray(values, float), np.asarray(weights, float)
    order = np.argsort(x); x, w = x[order], w[order]
    return float(x[np.searchsorted(np.cumsum(w) / w.sum(), q, side="left")])


def load(event_id=DEFAULT_EVENT):
    reads = {r["event_id"]: r for r in map(json.loads, (DATA / "reads.jsonl").open())}
    scores = {r["event_id"]: r for r in map(json.loads, (DATA / "scores.jsonl").open())}
    with (DATA / "input" / "events.csv").open(newline="", encoding="utf-8") as f:
        events = {r["event_id"]: r for r in csv.DictReader(f)}
    r, s = reads[event_id], scores[event_id]
    if not E.verify_seal(r) or s["read_hash"] != r["hash"]:
        raise ValueError("the demonstration read does not verify against its seal and score")
    atoms = np.asarray(r["forecasts"]["20"]["abnormal_atoms"], float)
    out = {"event": events[event_id], "read": r, "score": s, "arms": {}}
    for arm in ("structural", "surface"):
        w = np.asarray(r[arm]["weights"], float)
        order = np.argsort(-w)[:5]
        out["arms"][arm] = {
            "mean": float(np.sum(w * atoms)), "p25": weighted_quantile(atoms, w, .25),
            "median": weighted_quantile(atoms, w, .5), "p75": weighted_quantile(atoms, w, .75),
            "top": [{"event": events[eid], "weight": float(w[i]), "atom": float(atoms[i])}
                    for i, eid in ((int(i), r["candidate_ids"][int(i)]) for i in order)]}
    return out


def render(event_id=DEFAULT_EVENT):
    d = load(event_id); e, r, s = d["event"], d["read"], d["score"]
    lines = ["# Instrument demonstration — 2026 Hormuz closure", "",
             "> A single frozen historical read, shown to explain the instrument—not selected as proof of average performance.", "",
             f"**Target:** {e['event_date']} · `{e['type']}` · {e['title']}", "",
             f"**Seal:** `{r['hash']}` (verified before the outcome is attached)", "",
             f"The read compares the same {r['n_pool']} closed prior events. Structural weighting uses "
             f"strictly available market/state fields (effective weight n {r['structural_n_eff']:.1f}); surface "
             f"weighting uses event class only (effective weight n {r['surface_n_eff']:.1f}).", ""]
    for arm, title in (("structural", "Structural state"), ("surface", "Surface class")):
        a = d["arms"][arm]
        lines += [f"## {title}", "",
                  f"Forecast abnormal-return distribution: p25 {a['p25']:+.2f}%, median {a['median']:+.2f}%, "
                  f"p75 {a['p75']:+.2f}% (weighted mean {a['mean']:+.2f}%).", "",
                  "| weight | date | class | historical case | +20d abnormal return |", "|---:|---|---|---|---:|"]
        for x in a["top"]:
            z = x["event"]
            lines.append(f"| {x['weight']:.3f} | {z['event_date']} | `{z['type']}` | {z['title']} | {x['atom']:+.2f}% |")
        lines.append("")
    winner = "structural" if s["structural_crps"] < s["surface_crps"] else "surface"
    lines += ["## Resolution", "", f"Realized +20-day abnormal Brent return: **{s['outcome']:+.2f}%**.", "",
              f"CRPS: structural **{s['structural_crps']:.3f}**, surface **{s['surface_crps']:.3f}**, "
              f"uniform pooling **{s['uniform_crps']:.3f}** (lower is better). The **{winner}** arm scored better on this case.", "",
              "This one read demonstrates mechanics and auditability. The project-level conclusion comes from all 264 "
              "inferential dates in `data/structural_surface/summary.json`, not from this example.", ""]
    return "\n".join(lines)


def main():
    out = ROOT / "docs" / "DEMO.md"
    out.write_text(render() + "\n")
    print(out)


if __name__ == "__main__":
    main()
