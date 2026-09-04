"""Event-blind detection of chokepoint transit impairment episodes.

Implements `registrations/DISRUPTION_REALIZATION.md`. This module is deliberately isolated:

* it reads **only** an explicitly supplied PortWatch CSV (`data/v3/portwatch_daily.csv`);
* it never imports, opens, or references the event catalogue, any price series, or `data/oil.db`;
* every baseline uses strictly prior observations;
* output is deterministic and written only beneath `data/v3/`.

The isolation is the point. If detection could see the events it is later compared against, the
comparison would be worthless, so `tests/test_disruption_blinding.py` enforces it mechanically
rather than trusting this docstring.

Sources: UN Global Platform; IMF PortWatch.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "v3" / "portwatch_daily.csv"
OUT = ROOT / "data" / "v3"
REGISTRATION = ROOT / "registrations" / "DISRUPTION_REALIZATION.md"

DETECTOR_VERSION = "1.0.0"

# Registered parameters (DISRUPTION_REALIZATION.md §6-§11). Changing any of these is an amendment,
# not a code change.
BASELINE_WINDOW = 365     # §6  days in the trailing median window
BASELINE_GAP = 30         # §7  days excluded immediately before t, so an onset cannot mask itself
BASELINE_MIN_OBS = 300    # §5  minimum observations required inside the window
THRESHOLD = 0.70          # §8  impaired when observed / baseline < THRESHOLD
MIN_IMPAIRED_DAYS = 5     # §9  minimum impaired days for an episode to qualify
MAX_GAP = 2               # §10 non-impaired days tolerated inside an episode
# §11 the recovery rule is MAX_GAP + 1: more than MAX_GAP consecutive clean days ends the episode.
# This is the module's only look-ahead, it is bounded at 3 days, and it can only move an end
# boundary -- it can never create or delete an episode's start.

IMPAIRMENT_ROUTES = ("hormuz", "suez", "bab_el_mandeb", "bosporus", "malacca", "panama")
DIAGNOSTIC_ROUTES = ("cape_of_good_hope",)   # §3 diversion destination; never an impairment episode
PRIMARY_MEASURE = "n_tanker"
SECONDARY_MEASURE = "capacity_tanker"


class InputError(Exception):
    """Raised loudly on malformed input. Never swallowed, never worked around."""


def load_panel(path=INPUT):
    """Read the committed slice and validate it hard before any arithmetic happens."""
    path = Path(path)
    if not path.exists():
        raise InputError(f"PortWatch input not found: {path}. Run src/export_portwatch_slice.py.")
    panel = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["series_id", "obs_date", "value"]:
            raise InputError(f"unexpected columns: {reader.fieldnames}")
        for row in reader:
            try:
                d = dt.date.fromisoformat(row["obs_date"])
                v = float(row["value"])
            except (ValueError, TypeError) as exc:
                raise InputError(f"unparseable row {row}: {exc}") from exc
            if not np.isfinite(v):
                raise InputError(f"non-finite value in {row}")
            panel.setdefault(row["series_id"], []).append((d, v))
    if not panel:
        raise InputError("input contained no rows")

    for sid, obs in panel.items():
        dates = [d for d, _ in obs]
        if len(set(dates)) != len(dates):
            raise InputError(f"{sid}: duplicate observation dates")
        if dates != sorted(dates):
            raise InputError(f"{sid}: observations are not in date order")
        gaps = {(dates[i] - dates[i - 1]).days for i in range(1, len(dates))}
        if gaps - {1}:
            raise InputError(f"{sid}: non-daily spacing, gaps of {sorted(gaps - {1})} days")
    return panel


def baselines(values, window=BASELINE_WINDOW, gap=BASELINE_GAP, min_obs=BASELINE_MIN_OBS):
    """Trailing median over [t-window-gap, t-gap-1]. Uses only observations strictly before t.

    Returns NaN where the window holds fewer than `min_obs` observations, which marks the date
    ineligible rather than imputing a baseline for it.
    """
    v = np.asarray(values, float)
    out = np.full(len(v), np.nan)
    span = window + gap
    for i in range(len(v)):
        lo, hi = i - span, i - gap
        if lo < 0 or hi <= lo:
            continue
        w = v[lo:hi]
        if len(w) < min_obs:
            continue
        out[i] = float(np.median(w))
    return out


def episodes_from_flags(dates, ratio, impaired, min_impaired=MIN_IMPAIRED_DAYS, max_gap=MAX_GAP):
    """Group impaired days into episodes under the registered gap and recovery rules (§9-§11)."""
    runs, current, clean = [], [], 0
    for i, flag in enumerate(impaired):
        if flag:
            if current and clean:
                current.extend(range(current[-1] + 1, i))   # absorb the tolerated clean days
            current.append(i)
            clean = 0
        elif current:
            clean += 1
            if clean > max_gap:                              # §11 recovery: episode is closed
                runs.append(current)
                current, clean = [], 0
    if current:
        runs.append(current)

    out = []
    for run in runs:
        idx = [i for i in run if impaired[i]]
        if len(idx) < min_impaired:
            continue
        start, end = idx[0], idx[-1]
        trough = min(idx, key=lambda i: (ratio[i], i))       # earliest index wins a tie
        out.append({"start": start, "end": end, "trough": trough, "impaired_idx": idx})
    return out


def detect_route(dates, values, route, measure, threshold=THRESHOLD,
                 min_impaired=MIN_IMPAIRED_DAYS, max_gap=MAX_GAP, **kw):
    """Detect episodes for one (route, measure). Knows nothing about events or prices."""
    base = baselines(values, **kw)
    v = np.asarray(values, float)
    with np.errstate(invalid="ignore", divide="ignore"):
        ratio = np.where((base > 0) & np.isfinite(base), v / base, np.nan)
    eligible = np.isfinite(ratio)
    impaired = eligible & (ratio < threshold)

    rows = []
    for n, ep in enumerate(episodes_from_flags(dates, ratio, impaired,
                                               min_impaired, max_gap), start=1):
        s, e, tr = ep["start"], ep["end"], ep["trough"]
        lost = float(sum(max(0.0, base[i] - v[i]) for i in ep["impaired_idx"]))
        rows.append({
            "episode_id": f"{route}.{measure}.{dates[s].isoformat()}",
            "route": route,
            "series": f"portwatch.{route}.{measure}",
            "start_date": dates[s].isoformat(),
            "end_date": dates[e].isoformat(),
            "trough_date": dates[tr].isoformat(),
            "duration_days": (dates[e] - dates[s]).days + 1,
            "n_impaired_days": len(ep["impaired_idx"]),
            "baseline_at_trough": round(float(base[tr]), 4),
            "observed_at_trough": round(float(v[tr]), 4),
            "fractional_impairment": round(float(1.0 - ratio[tr]), 6),
            "mean_fractional_impairment": round(
                float(np.mean([1.0 - ratio[i] for i in ep["impaired_idx"]])), 6),
            "tanker_days_lost": round(lost, 4),
            "n_ineligible_days_in_span": int(np.sum(~eligible[s:e + 1])),
            "detector_version": DETECTOR_VERSION,
        })
    return rows, {"n_days": len(dates), "n_eligible": int(eligible.sum()),
                  "n_impaired": int(impaired.sum()),
                  "first_eligible": next((dates[i].isoformat() for i in range(len(dates))
                                          if eligible[i]), None)}


FIELDS = ("episode_id", "route", "series", "start_date", "end_date", "trough_date",
          "duration_days", "n_impaired_days", "baseline_at_trough", "observed_at_trough",
          "fractional_impairment", "mean_fractional_impairment", "tanker_days_lost",
          "n_ineligible_days_in_span", "detector_version")


def detect_all(panel, measure=PRIMARY_MEASURE, routes=IMPAIRMENT_ROUTES, **kw):
    rows, coverage = [], {}
    for route in routes:
        sid = f"portwatch.{route}.{measure}"
        if sid not in panel:
            raise InputError(f"required series missing from input: {sid}")
        obs = panel[sid]
        r, cov = detect_route([d for d, _ in obs], [v for _, v in obs], route, measure, **kw)
        rows.extend(r)
        coverage[route] = cov
    rows.sort(key=lambda r: (r["route"], r["start_date"]))
    return rows, coverage


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(input_path=INPUT, out_dir=OUT, measure=PRIMARY_MEASURE):
    panel = load_panel(input_path)
    rows, coverage = detect_all(panel, measure=measure)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    episodes = out_dir / f"episodes_{measure}.csv"
    with episodes.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    manifest = {
        "attribution": "Sources: UN Global Platform; IMF PortWatch.",
        "detector_version": DETECTOR_VERSION,
        "registration": str(REGISTRATION.relative_to(ROOT)),
        "registration_sha256": file_sha256(REGISTRATION),
        "detector_sha256": file_sha256(Path(__file__)),
        "input": {str(Path(input_path).relative_to(ROOT)): file_sha256(input_path)},
        "parameters": {"measure": measure, "baseline_window": BASELINE_WINDOW,
                       "baseline_gap": BASELINE_GAP, "baseline_min_obs": BASELINE_MIN_OBS,
                       "threshold": THRESHOLD, "min_impaired_days": MIN_IMPAIRED_DAYS,
                       "max_gap": MAX_GAP,
                       "impairment_routes": list(IMPAIRMENT_ROUTES),
                       "diagnostic_routes_excluded": list(DIAGNOSTIC_ROUTES)},
        "coverage": coverage,
        "n_episodes": len(rows),
        "outputs": {episodes.name: file_sha256(episodes)},
    }
    (out_dir / f"episodes_{measure}_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return rows, manifest


def report(rows, coverage):
    import collections
    lines = [f"detector {DETECTOR_VERSION} | threshold {THRESHOLD} | min impaired days "
             f"{MIN_IMPAIRED_DAYS} | baseline {BASELINE_WINDOW}/{BASELINE_GAP}", ""]
    lines.append(f"{'route':20s} {'days':>6s} {'eligible':>9s} {'impaired':>9s} {'episodes':>9s}"
                 f"  first eligible")
    per = collections.Counter(r["route"] for r in rows)
    for route, cov in coverage.items():
        lines.append(f"{route:20s} {cov['n_days']:6d} {cov['n_eligible']:9d} "
                     f"{cov['n_impaired']:9d} {per[route]:9d}  {cov['first_eligible']}")
    lines += ["", f"{'route':20s} {'year':>6s} {'episodes':>9s}"]
    by = collections.Counter((r["route"], r["start_date"][:4]) for r in rows)
    for (route, year), n in sorted(by.items()):
        lines.append(f"{route:20s} {year:>6s} {n:9d}")
    lines += ["", f"total episodes: {len(rows)}"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Event-blind chokepoint impairment detector.")
    ap.add_argument("--input", type=Path, default=INPUT, help="PortWatch daily CSV")
    ap.add_argument("--out", type=Path, default=OUT, help="output directory (under data/v3)")
    ap.add_argument("--measure", default=PRIMARY_MEASURE,
                    choices=[PRIMARY_MEASURE, SECONDARY_MEASURE])
    ap.add_argument("--report", action="store_true", help="print coverage and episode counts")
    args = ap.parse_args()
    rows, manifest = run(args.input, args.out, args.measure)
    if args.report:
        print(report(rows, manifest["coverage"]))
    else:
        print(json.dumps({k: manifest[k] for k in
                          ("detector_version", "n_episodes", "outputs")}, indent=2))
    print("Sources: UN Global Platform; IMF PortWatch.")


if __name__ == "__main__":
    main()
