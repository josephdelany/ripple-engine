"""The reproducibility boundary must be checked, not asserted in prose.

These tests fix two things the project got wrong elsewhere and must not get wrong here: a
committed input that drifts after freezing, and a limitation that is true when written and
silently false later.
"""
import json
import shutil

import pytest

import bundle_provenance as P


def test_committed_bundle_matches_its_frozen_manifest():
    """The experiment's ground truth. If this fails, every frozen number is unverifiable."""
    files = P.bundle_files()
    assert set(files) == {"events.csv", "market_observations.csv", "situation_state.csv"}
    for name, got in files.items():
        assert got["present"], f"{name} missing from the committed bundle"
        assert got["actual_sha256"] == got["expected_sha256"], f"{name} hash drifted after freezing"
        assert got["actual_rows"] == got["expected_rows"], f"{name} row count drifted after freezing"
    assert P.report()["bundle_intact"] is True


def test_absent_upstream_is_reported_not_ignored(tmp_path, monkeypatch):
    """The state of every clean clone: gitignored database, so the chain cannot be re-derived."""
    monkeypatch.setattr(P, "SOURCE_DB", tmp_path / "does_not_exist.db")
    up = P.upstream()
    assert up["status"] == P.ABSENT
    assert up["local_sha256"] is None
    assert up["recorded_sha256"]


def test_diverged_upstream_is_reported_not_ignored(tmp_path, monkeypatch):
    """The state of this working tree: a database is present but is not the exporting one."""
    other = tmp_path / "oil.db"
    other.write_bytes(b"not the database the bundle came from")
    monkeypatch.setattr(P, "SOURCE_DB", other)
    up = P.upstream()
    assert up["status"] == P.DIVERGED
    assert up["local_sha256"] != up["recorded_sha256"]


def test_matching_upstream_would_be_reported_as_reproduced(tmp_path, monkeypatch):
    """The status is a real three-way check, not a constant that always says 'diverged'."""
    db = tmp_path / "oil.db"
    db.write_bytes(b"stand-in for the exporting database")
    manifest = tmp_path / "bundle_manifest.json"
    manifest.write_text(json.dumps({"source_database_sha256": P.file_hash(db), "files": {}}))
    monkeypatch.setattr(P, "SOURCE_DB", db)
    monkeypatch.setattr(P, "MANIFEST", manifest)
    assert P.upstream()["status"] == P.REPRODUCED


def test_tampered_bundle_file_fails_the_check(tmp_path, monkeypatch):
    """A committed input edited after freezing must be caught, not absorbed."""
    bundle = tmp_path / "input"
    shutil.copytree(P.BUNDLE, bundle)
    (bundle / "events.csv").open("a", encoding="utf-8").write("tampered\n")
    monkeypatch.setattr(P, "BUNDLE", bundle)
    monkeypatch.setattr(P, "MANIFEST", bundle / "bundle_manifest.json")
    assert P.bundle_files()["events.csv"]["ok"] is False
    with pytest.raises(SystemExit):
        P.main()
