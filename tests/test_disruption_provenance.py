"""Provenance for the v3 inputs and detector outputs.

v2 could not commit its inputs, so it could only ever claim auditability by receipt
(`docs/audit/PROVENANCE_BOUNDARY.md`). The IMF licence lets v3 commit its input, so v3 can claim
something stronger — but only if the committed slice, the detector and the frozen output are
actually pinned to each other. That is what these tests check.
"""
import csv
import datetime as dt
import json
from pathlib import Path

import pytest

import disruption_episodes as D

ROOT = Path(__file__).resolve().parent.parent
V3 = ROOT / "data" / "v3"
SLICE = V3 / "portwatch_daily.csv"
SLICE_MANIFEST = V3 / "portwatch_manifest.json"
EPISODES = V3 / "episodes_n_tanker.csv"
EPISODE_MANIFEST = V3 / "episodes_n_tanker_manifest.json"


@pytest.fixture(scope="module")
def slice_manifest():
    if not SLICE_MANIFEST.exists():
        pytest.skip("PortWatch slice not present in this checkout")
    return json.loads(SLICE_MANIFEST.read_text(encoding="utf-8"))


def test_committed_slice_matches_its_manifest(slice_manifest):
    """The input is the frozen one. If this fails, every episode below it is unverifiable."""
    recorded = slice_manifest["files"]["portwatch_daily.csv"]
    assert D.file_sha256(SLICE) == recorded["sha256"]
    with SLICE.open(encoding="utf-8") as f:
        assert sum(1 for _ in f) - 1 == recorded["rows"]


def test_slice_carries_its_licence_and_attribution(slice_manifest):
    """Redistribution is permitted only with attribution, so it ships with the data."""
    assert "IMF PortWatch" in slice_manifest["attribution"]
    assert "UN Global Platform" in slice_manifest["attribution"]
    assert "imf.org/external/terms.htm" in slice_manifest["licence"]
    assert slice_manifest["source_url"] == "https://portwatch.imf.org/"


def test_slice_covers_every_route_and_measure_the_registration_names(slice_manifest):
    for route in D.IMPAIRMENT_ROUTES + D.DIAGNOSTIC_ROUTES:
        for measure in (D.PRIMARY_MEASURE, D.SECONDARY_MEASURE):
            assert f"portwatch.{route}.{measure}" in slice_manifest["series"]
    assert slice_manifest["series"][f"portwatch.hormuz.{D.PRIMARY_MEASURE}"] == "tankers/day"
    assert slice_manifest["series"][f"portwatch.hormuz.{D.SECONDARY_MEASURE}"] == "metric tons/day"


def test_slice_is_contiguous_daily_with_no_nulls():
    """Asserted on the committed file, independently of the database it came from."""
    if not SLICE.exists():
        pytest.skip("PortWatch slice not present in this checkout")
    per = {}
    with SLICE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            per.setdefault(row["series_id"], []).append(dt.date.fromisoformat(row["obs_date"]))
    assert len(per) == 21
    for sid, dates in per.items():
        assert len(dates) == len(set(dates)), f"{sid}: duplicate dates"
        assert dates == sorted(dates), f"{sid}: out of order"
        assert {(dates[i] - dates[i - 1]).days for i in range(1, len(dates))} == {1}, \
            f"{sid}: not contiguous daily"


@pytest.fixture(scope="module")
def episode_manifest():
    if not EPISODE_MANIFEST.exists():
        pytest.skip("frozen episode output not present in this checkout")
    return json.loads(EPISODE_MANIFEST.read_text(encoding="utf-8"))


def test_frozen_episodes_pin_input_detector_and_registration(episode_manifest):
    """Every artifact the result depends on is hashed, so silent drift in any of them is caught."""
    m = episode_manifest
    assert m["input"]["data/v3/portwatch_daily.csv"] == D.file_sha256(SLICE)
    assert m["detector_sha256"] == D.file_sha256(Path(D.__file__)), \
        "the detector changed after its output was frozen; re-run and re-freeze"
    assert m["registration_sha256"] == D.file_sha256(
        ROOT / "registrations" / "DISRUPTION_REALIZATION.md"), \
        "the registration changed after the run it governs; amend and re-freeze"
    assert m["outputs"]["episodes_n_tanker.csv"] == D.file_sha256(EPISODES)


def test_frozen_parameters_are_the_registered_ones(episode_manifest):
    p = episode_manifest["parameters"]
    assert p["threshold"] == D.THRESHOLD == 0.70
    assert p["min_impaired_days"] == D.MIN_IMPAIRED_DAYS == 5
    assert p["baseline_window"] == 365 and p["baseline_gap"] == 30
    assert p["max_gap"] == 2
    assert p["impairment_routes"] == list(D.IMPAIRMENT_ROUTES)
    assert p["diagnostic_routes_excluded"] == list(D.DIAGNOSTIC_ROUTES)


def test_rerunning_the_detector_reproduces_the_frozen_output(tmp_path, episode_manifest):
    """The whole claim of v3: the episode table rebuilds byte-for-byte from a committed input."""
    rows, manifest = D.run(SLICE, tmp_path, D.PRIMARY_MEASURE)
    rebuilt = tmp_path / "episodes_n_tanker.csv"
    assert D.file_sha256(rebuilt) == episode_manifest["outputs"]["episodes_n_tanker.csv"], \
        "episode detection is not reproducible from the committed slice"
    assert manifest["n_episodes"] == episode_manifest["n_episodes"]


def test_no_episode_is_reported_for_a_diagnostic_route(episode_manifest):
    if not EPISODES.exists():
        pytest.skip("frozen episode output not present")
    with EPISODES.open(newline="", encoding="utf-8") as f:
        routes = {row["route"] for row in csv.DictReader(f)}
    assert routes.isdisjoint(D.DIAGNOSTIC_ROUTES)
    assert routes <= set(D.IMPAIRMENT_ROUTES)
