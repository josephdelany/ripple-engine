"""Preregistered sensitivity grid for the impairment detector (DISRUPTION_REALIZATION.md §8).

Nine cells: threshold {0.60, 0.70, 0.80} × minimum impaired days {3, 5, 7}, holding the baseline at
365/30. **Every cell is reported and none may be selected.** The primary specification is (0.70, 5)
and it stays primary whatever this grid shows.

Like the detector, this reads only the committed PortWatch slice. It sees no events and no prices.

Sources: UN Global Platform; IMF PortWatch.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import disruption_episodes as D

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "v3"

THRESHOLDS = (0.60, 0.70, 0.80)
MIN_DAYS = (3, 5, 7)
FIELDS = ("threshold", "min_impaired_days", "n_episodes", "median_duration_days",
          "median_fractional_impairment", "longest_episode_days", "is_primary",
          *(f"n_{r}" for r in D.IMPAIRMENT_ROUTES))


def _median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    mid = len(xs) // 2
    return xs[mid] if len(xs) % 2 else (xs[mid - 1] + xs[mid]) / 2


def grid(input_path=D.INPUT):
    panel = D.load_panel(input_path)
    rows = []
    for threshold in THRESHOLDS:
        for min_days in MIN_DAYS:
            eps, _ = D.detect_all(panel, threshold=threshold, min_impaired=min_days)
            durations = [e["duration_days"] for e in eps]
            per_route = {r: sum(1 for e in eps if e["route"] == r) for r in D.IMPAIRMENT_ROUTES}
            rows.append({
                "threshold": threshold,
                "min_impaired_days": min_days,
                "n_episodes": len(eps),
                "median_duration_days": _median(durations),
                "median_fractional_impairment": (
                    round(_median([e["fractional_impairment"] for e in eps]), 4) if eps else None),
                "longest_episode_days": max(durations) if durations else 0,
                "is_primary": (threshold == D.THRESHOLD and min_days == D.MIN_IMPAIRED_DAYS),
                **{f"n_{r}": per_route[r] for r in D.IMPAIRMENT_ROUTES},
            })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=D.INPUT)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    rows = grid(args.input)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "sensitivity_grid.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (args.out / "sensitivity_grid_manifest.json").write_text(json.dumps({
        "registration": "registrations/DISRUPTION_REALIZATION.md",
        "detector_version": D.DETECTOR_VERSION,
        "detector_sha256": D.file_sha256(Path(D.__file__)),
        "input": {"data/v3/portwatch_daily.csv": D.file_sha256(args.input)},
        "thresholds": list(THRESHOLDS), "min_impaired_days": list(MIN_DAYS),
        "primary": {"threshold": D.THRESHOLD, "min_impaired_days": D.MIN_IMPAIRED_DAYS},
        "outputs": {path.name: D.file_sha256(path)},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    hdr = f"{'thr':>5s} {'min':>4s} {'eps':>5s} {'med_dur':>8s} {'med_impair':>11s} {'longest':>8s}  primary"
    print(hdr); print("-" * len(hdr))
    for r in rows:
        print(f"{r['threshold']:5.2f} {r['min_impaired_days']:4d} {r['n_episodes']:5d} "
              f"{str(r['median_duration_days']):>8s} {str(r['median_fractional_impairment']):>11s} "
              f"{r['longest_episode_days']:8d}  {'<== PRIMARY' if r['is_primary'] else ''}")
    print("\nSources: UN Global Platform; IMF PortWatch.")


if __name__ == "__main__":
    main()
