import inspect
import json
from pathlib import Path

import numpy as np
import pytest

import structural_component_ablation as A
from structural_surface_experiment import weighted_crps


def test_effective_n_and_weighted_crps_are_independently_reconstructed():
    atoms = np.array([-2.0, 1.0, 5.0])
    weights = np.array([0.2, 0.3, 0.5])
    outcome = 0.5
    manual_crps = sum(w * abs(x - outcome) for x, w in zip(atoms, weights))
    manual_crps -= 0.5 * sum(
        weights[i] * weights[j] * abs(atoms[i] - atoms[j])
        for i in range(3) for j in range(3)
    )
    assert weighted_crps(atoms, weights, outcome) == pytest.approx(manual_crps)
    assert A.effective_n(weights) == pytest.approx(1 / sum(x * x for x in weights))


@pytest.mark.parametrize("distances,target", [
    ([0.0, 0.5, 1.0, 1.5], 2.5),
    ([0.0, 0.0, 1.0, 1.0], 3.0),
    ([0.0, 1.0, 1.0, 1.0, 1.0], 4.25),
])
def test_calibration_attains_registered_effective_size(distances, target):
    weights, temperature, achieved, boundary = A.calibrate_ess(distances, target)
    assert temperature > 0
    assert boundary == "interior"
    assert weights.sum() == pytest.approx(1)
    assert achieved == pytest.approx(target, abs=A.TOL)
    assert A.effective_n(weights) == pytest.approx(target, abs=A.TOL)


def test_calibration_handles_ties_and_constant_distance_boundaries():
    assert A.minimum_attainable_ess([0, 0, 1, 2]) == 2
    weights, temperature, achieved, boundary = A.calibrate_ess([0, 0, 1, 2], 2)
    assert temperature == 0
    assert boundary == "minimum_boundary"
    assert weights.tolist() == [0.5, 0.5, 0.0, 0.0]
    weights, temperature, achieved, boundary = A.calibrate_ess([1, 1, 1], 3)
    assert np.isinf(temperature)
    assert boundary == "uniform_boundary"
    assert achieved == pytest.approx(3)
    with pytest.raises(ValueError):
        A.calibrate_ess([0, 0, 1], 1.5)


def test_calibration_is_order_invariant_and_has_no_outcome_parameter():
    assert list(inspect.signature(A.calibrate_ess).parameters) == ["distances", "target", "tol"]
    d = np.array([0.8, 0.1, 0.4, 0.2])
    permutation = np.array([2, 0, 3, 1])
    w, temperature, achieved, _ = A.calibrate_ess(d, 3.0)
    wp, temperature_p, achieved_p, _ = A.calibrate_ess(d[permutation], 3.0)
    restored = np.empty_like(wp)
    restored[permutation] = wp
    assert restored == pytest.approx(w)
    assert temperature_p == pytest.approx(temperature)
    assert achieved_p == pytest.approx(achieved)


def test_holm_step_down_is_monotone_in_rank_and_returns_original_order():
    # Sorted raw p: .01, .03; adjusted: .02, .03, returned in original order.
    assert A.holm_adjust([0.03, 0.01]) == pytest.approx([0.03, 0.02])


def test_frozen_field_audit_is_reproduced_directly_from_reads():
    reads = A.load_jsonl(A.READS)
    audit = A._field_audit(reads)
    assert audit["n_comparisons"] == 41_997
    assert audit["market_only"] == 20_915
    assert audit["containing_actors"] == 21_082
    assert audit["containing_dyads_or_other"] == 3
    assert audit["dates_all_comparisons_market_only"] == 73
    assert audit["block_combination_counts"] == {
        "actors|dyads|market": 3,
        "actors|market": 21_079,
        "market": 20_915,
    }
    assert audit["market_only_fraction"] == pytest.approx(20_915 / 41_997)


def test_run_preserves_frozen_support_atoms_and_is_byte_reproducible(tmp_path, monkeypatch):
    # Inference is independently tested elsewhere.  Replacing it here keeps this invariant test fast.
    def fake_paired(a, b, dates, n_boot):
        diff = np.asarray(a) - np.asarray(b)
        return {"n": len(diff), "mean_a": float(np.mean(a)), "mean_b": float(np.mean(b)),
                "mean_diff": float(np.mean(diff)), "ci95": [float(np.min(diff)), float(np.max(diff))],
                "dm": {"p_value": 0.5}, "mean_block": 1.0, "n_boot": n_boot}

    monkeypatch.setattr(A, "paired_block", fake_paired)
    monkeypatch.setattr(A.subprocess, "check_output", lambda *args, **kwargs: "f" * 40 + "\n")
    out_a, out_b = tmp_path / "a", tmp_path / "b"
    A.run(out_dir=out_a, n_boot=7)
    A.run(out_dir=out_b, n_boot=7)
    for name in ("scores.jsonl", "summary.json", "manifest.json"):
        assert (out_a / name).read_bytes() == (out_b / name).read_bytes()

    frozen_reads = A.load_jsonl(A.READS)
    produced = A.load_jsonl(out_a / "scores.jsonl")
    assert len(produced) == len(frozen_reads) == 264
    for source, row in zip(frozen_reads, produced):
        assert row["candidate_ids"] == source["candidate_ids"]
        atoms = source["forecasts"]["20"]["abnormal_atoms"]
        assert row["atoms_sha256"] == A.hashlib.sha256(A.canonical(atoms).encode()).hexdigest()
        for arm_weights in row["weights"].values():
            assert len(arm_weights) == len(source["candidate_ids"])

    manifest = json.loads((out_a / "manifest.json").read_text())
    assert manifest["registration_commit"] == A.REGISTRATION_COMMIT
    assert "implementation_commit" in manifest
    assert manifest["execution_commit"] == "f" * 40
    assert manifest["inputs"][str(A.READS.relative_to(A.ROOT))] == A.file_hash(A.READS)
    assert manifest["inputs"][str(A.SCORES.relative_to(A.ROOT))] == A.file_hash(A.SCORES)
