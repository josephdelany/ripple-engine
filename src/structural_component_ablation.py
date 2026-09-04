"""Registered component/concentration ablation for the frozen analogy experiment.

This program consumes only the two frozen ledgers named in the registration and writes only to
``data/structural_surface/ablation``.  It deliberately does not run on import.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np

from structural_surface_experiment import ROOT, SEED, paired_block, weighted_crps

READS = ROOT / "data" / "structural_surface" / "reads.jsonl"
SCORES = ROOT / "data" / "structural_surface" / "scores.jsonl"
OUT = ROOT / "data" / "structural_surface" / "ablation"
REGISTRATION = ROOT / "registrations" / "STRUCTURAL_COMPONENT_ABLATION.md"
FROZEN_RELEASE_COMMIT = "1705713b801d7ffc48d7cc39adb5a802b613157c"
REGISTRATION_COMMIT = "75a280fb01452811ccc33c4a33f68967919fc149"
IMPLEMENTATION_COMMIT = None  # Filled after the implementation commit and before publication run.
TOL = 1e-8


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def effective_n(weights):
    w = np.asarray(weights, dtype=float)
    return float(1.0 / np.sum(np.square(w / w.sum())))


def minimum_attainable_ess(distances, atol=1e-14):
    """Limit of effective N as temperature tends to zero, including tied minima."""
    d = np.asarray(distances, dtype=float)
    if not len(d) or not np.isfinite(d).all():
        raise ValueError("distances must be a non-empty finite vector")
    return float(np.sum(np.isclose(d, d.min(), rtol=0.0, atol=atol)))


def weights_at_temperature(distances, temperature):
    d = np.asarray(distances, dtype=float)
    if not len(d) or not np.isfinite(d).all():
        raise ValueError("distances must be a non-empty finite vector")
    if np.isinf(temperature):
        return np.ones(len(d), dtype=float) / len(d)
    if temperature == 0:
        selected = np.isclose(d, d.min(), rtol=0.0, atol=1e-14).astype(float)
        return selected / selected.sum()
    if temperature < 0 or not np.isfinite(temperature):
        raise ValueError("temperature must be nonnegative or positive infinity")
    z = np.exp(-(d - d.min()) / temperature)
    return z / z.sum()


def calibrate_ess(distances, target, tol=TOL):
    """Choose weights by deterministic bisection; this function cannot receive outcomes."""
    d = np.asarray(distances, dtype=float)
    n = len(d)
    lower = minimum_attainable_ess(d)
    if target < lower - tol or target > n + tol:
        raise ValueError(f"target ESS {target} is outside attainable [{lower}, {n}]")
    if np.ptp(d) <= 1e-14 or target >= n - tol:
        w = np.ones(n) / n
        return w, float("inf"), effective_n(w), "uniform_boundary"
    if target <= lower + tol:
        w = weights_at_temperature(d, 0.0)
        return w, 0.0, effective_n(w), "minimum_boundary"
    lo, hi = 0.0, 1.0
    while effective_n(weights_at_temperature(d, hi)) < target:
        hi *= 2.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if effective_n(weights_at_temperature(d, mid)) < target:
            lo = mid
        else:
            hi = mid
    temperature = (lo + hi) / 2.0
    w = weights_at_temperature(d, temperature)
    achieved = effective_n(w)
    if abs(achieved - target) > tol:
        raise ArithmeticError(f"ESS calibration missed target: {achieved} versus {target}")
    return w, float(temperature), achieved, "interior"


def holm_adjust(p_values):
    """Holm step-down adjusted p-values in the original order."""
    p = np.asarray(p_values, dtype=float)
    if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("p-values must be finite and in [0, 1]")
    order = np.argsort(p, kind="stable")
    adjusted = np.empty(len(p), dtype=float)
    running = 0.0
    m = len(p)
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adjusted[idx] = min(running, 1.0)
    return adjusted.tolist()


def _field_audit(reads):
    fields, combinations = Counter(), Counter()
    total = market_only = actors = other = 0
    all_market_dates = 0
    for read in reads:
        read_all_market = True
        for detail in read["structural"]["detail"]:
            blocks = tuple(sorted(detail["blocks"]))
            combinations["|".join(blocks)] += 1
            fields.update(detail["fields"])
            total += 1
            is_market = blocks == ("market",)
            market_only += int(is_market)
            actors += int("actors" in blocks)
            other += int(any(block not in {"market", "actors"} for block in blocks))
            read_all_market &= is_market
        all_market_dates += int(read_all_market)
    return {
        "n_comparisons": total,
        "field_counts": dict(sorted(fields.items())),
        "block_combination_counts": dict(sorted(combinations.items())),
        "market_only": market_only,
        "market_only_fraction": market_only / total,
        "containing_actors": actors,
        "containing_actors_fraction": actors / total,
        "containing_dyads_or_other": other,
        "containing_dyads_or_other_fraction": other / total,
        "dates_all_comparisons_market_only": all_market_dates,
    }


def _contrast(losses, arm_a, arm_b, dates, n_boot):
    result = paired_block(losses[arm_a], losses[arm_b], dates, n_boot)
    result["arm_a"] = arm_a
    result["arm_b"] = arm_b
    return result


def run(reads_path=READS, scores_path=SCORES, out_dir=OUT, n_boot=2000):
    reads, frozen_scores = load_jsonl(reads_path), load_jsonl(scores_path)
    score_by_key = {(x["event_id"], x["date"]): x for x in frozen_scores}
    if len(score_by_key) != len(frozen_scores):
        raise ValueError("frozen scores do not have unique event/date keys")
    if len(reads) != len(frozen_scores):
        raise ValueError("frozen read and score counts differ")

    rows = []
    for read in reads:
        key = (read["event_id"], read["date"])
        if key not in score_by_key:
            raise ValueError(f"read has no frozen score: {key}")
        score = score_by_key[key]
        atoms = np.asarray(read["forecasts"]["20"]["abnormal_atoms"], dtype=float)
        ids = read["candidate_ids"]
        details = read["structural"]["detail"]
        if not (len(ids) == len(atoms) == len(details) == len(read["surface"]["distances"])):
            raise ValueError(f"support mismatch in {key}")
        if score["read_hash"] != read["hash"]:
            raise ValueError(f"read hash mismatch in {key}")
        market = np.asarray([d["blocks"]["market"] for d in details], dtype=float)
        combined = np.asarray(read["structural"]["distances"], dtype=float)
        surface = np.asarray(read["surface"]["distances"], dtype=float)
        vectors = {"market_matched": market, "combined_matched": combined, "surface_matched": surface}
        natural_structural_ess = effective_n(read["structural"]["weights"])
        minima = {name: minimum_attainable_ess(d) for name, d in vectors.items()}
        common_target = min(float(len(ids)), max(natural_structural_ess, *minima.values()))
        matched, calibration = {}, {}
        for name, distances in vectors.items():
            w, temperature, achieved, boundary = calibrate_ess(distances, common_target)
            matched[name] = w
            calibration[name] = {"temperature": temperature, "effective_n": achieved,
                                 "minimum_attainable_n": minima[name], "boundary": boundary}
        fixed = {
            "uniform": np.ones(len(ids)) / len(ids),
            "registered_structural": np.asarray(read["structural"]["weights"], dtype=float),
            "market_tau_0_25": weights_at_temperature(market, 0.25),
            "market_plus_actors_tau_0_25": weights_at_temperature(
                [np.mean([v for b, v in d["blocks"].items() if b in {"market", "actors"}]) for d in details], 0.25),
            "registered_surface": np.asarray(read["surface"]["weights"], dtype=float),
        }
        all_weights = {**fixed, **matched}
        outcome = float(score["outcome"])
        losses = {name: weighted_crps(atoms, w, outcome) for name, w in all_weights.items()}
        rows.append({
            "event_id": read["event_id"], "date": read["date"], "read_hash": read["hash"],
            "candidate_ids": ids, "atoms_sha256": hashlib.sha256(canonical(atoms.tolist()).encode()).hexdigest(),
            "outcome": outcome, "common_target_effective_n": common_target,
            "constant_surface": bool(np.ptp(surface) <= 1e-14), "calibration": calibration,
            "weights": {name: w.tolist() for name, w in all_weights.items()}, "losses": losses,
        })

    dates = [x["date"] for x in rows]
    if len(set(dates)) != len(dates):
        raise ValueError("ablation expects the frozen one-read-per-date sample")
    arm_names = list(rows[0]["losses"])
    losses = {name: np.asarray([row["losses"][name] for row in rows]) for name in arm_names}
    primary = {
        "market_minus_surface_matched": _contrast(losses, "market_matched", "surface_matched", dates, n_boot),
        "combined_minus_market_matched": _contrast(losses, "combined_matched", "market_matched", dates, n_boot),
    }
    raw_p = [primary[name]["dm"].get("p_value") for name in primary]
    adjusted = holm_adjust(raw_p)
    for (name, result), p_adj in zip(primary.items(), adjusted):
        result["dm_p_holm"] = p_adj
        result["holm_reject_0_05"] = bool(p_adj < 0.05)
    secondary_pairs = [
        ("registered_structural", "market_tau_0_25"),
        ("market_plus_actors_tau_0_25", "market_tau_0_25"),
        ("registered_structural", "surface_matched"),
        ("registered_surface", "surface_matched"),
        ("surface_matched", "uniform"),
    ]
    summary = {
        "registration": str(REGISTRATION.relative_to(ROOT)), "frozen_release_commit": FROZEN_RELEASE_COMMIT,
        "n_dates": len(rows), "n_boot": n_boot, "seed": SEED,
        "mean_loss": {name: float(np.mean(values)) for name, values in losses.items()},
        "median_effective_n": {name: float(np.median([effective_n(row["weights"][name]) for row in rows]))
                               for name in arm_names},
        "primary_explanatory": primary,
        "secondary": {f"{a}_minus_{b}": _contrast(losses, a, b, dates, n_boot) for a, b in secondary_pairs},
        "calibration": {"tolerance": TOL, "constant_surface_dates": sum(r["constant_surface"] for r in rows),
                        "boundary_counts": dict(sorted(Counter(
                            c["boundary"] for row in rows for c in row["calibration"].values()).items()))},
        "field_use_audit": _field_audit(reads),
    }
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    scores_out, summary_out = out_dir / "scores.jsonl", out_dir / "summary.json"
    scores_out.write_text("".join(canonical(row) + "\n" for row in rows), encoding="utf-8")
    summary_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    execution_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    manifest = {
        "frozen_release_commit": FROZEN_RELEASE_COMMIT,
        "registration_commit": REGISTRATION_COMMIT,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "execution_commit": execution_commit,
        "inputs": {str(Path(p).relative_to(ROOT)): file_hash(p) for p in (reads_path, scores_path)},
        "registration": {"path": str(REGISTRATION.relative_to(ROOT)), "sha256": file_hash(REGISTRATION)},
        "outputs": {p.name: file_hash(p) for p in (scores_out, summary_out)},
        "note": "manifest.json cannot contain its own hash",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reads", type=Path, default=READS)
    parser.add_argument("--scores", type=Path, default=SCORES)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--fast", action="store_true", help="200 bootstrap draws; not publication output")
    args = parser.parse_args()
    print(json.dumps(run(args.reads, args.scores, args.out, 200 if args.fast else 2000), indent=2))


if __name__ == "__main__":
    main()
