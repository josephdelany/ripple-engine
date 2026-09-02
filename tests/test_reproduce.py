"""
test_reproduce.py -- D-6 replication check.

Compares a reproduced walk (built by `make reproduce`, in a clean clone -- never in this tree)
against the COMMITTED run walk_20260902T182828Z (data/walk_forward/summary.json, reads.jsonl).

Point this at a reproduction's outputs with two env vars:
    REPRO_SUMMARY=/path/to/clone/data/walk_forward/summary.json
    REPRO_READS=/path/to/clone/data/walk_forward/reads.jsonl
Absent either one, every test in this file SKIPS (never fails) with a message naming
`make reproduce`.

Never writes under data/: everything here is read-only, against paths named by env vars or the
committed files in this checkout.

Seal hashes across two runs, precisely (walk.py's own `seal`/`_canon`): the sealed `hash` field is
a SHA-256 over the WHOLE record except "hash" itself -- which includes `run_id` and `sealed_at`
(wall-clock). So two separate runs of the identical inputs can never produce an identical `hash`
for "the same" read; that is by construction, not nondeterminism. What two runs SHOULD reproduce,
if the read content itself is deterministic, is everything else in the record -- so this file
recomputes a content hash (the same `_canon`/sha256 walk.py uses, over the record with `hash`,
`sealed_at` and `run_id` stripped) and compares THAT, read by read, matched by (tier, event_id).
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import walk as W  # noqa: E402 -- for _canon(), the exact canonicalization the committed seal used

COMMITTED_SUMMARY = ROOT / "data" / "walk_forward" / "summary.json"
COMMITTED_READS = ROOT / "data" / "walk_forward" / "reads.jsonl"
COMMITTED_RUN_ID = "walk_20260902T182828Z"

REPRO_SUMMARY = os.environ.get("REPRO_SUMMARY")
REPRO_READS = os.environ.get("REPRO_READS")

pytestmark = pytest.mark.skipif(
    not (REPRO_SUMMARY and REPRO_READS),
    reason="REPRO_SUMMARY / REPRO_READS not set -- run `make reproduce` in a clean clone "
           "(REPRO_DB=/path/to/oil.db REPRO_FORCE=1), then re-run this test with "
           "REPRO_SUMMARY=<clone>/data/walk_forward/summary.json "
           "REPRO_READS=<clone>/data/walk_forward/reads.jsonl",
)


def _load_json(path):
    return json.loads(Path(path).read_text())


def _load_jsonl(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _content_hash(record):
    """Same canonicalization walk.py's seal() used, minus the fields that are run-identity, not
    read content: hash (the field itself), sealed_at (wall clock) and run_id (this run's name)."""
    body = {k: v for k, v in record.items() if k not in ("hash", "sealed_at", "run_id")}
    return hashlib.sha256(W._canon(body).encode()).hexdigest()


def _by_tier_event(records, run_id=None):
    out = {}
    for r in records:
        if run_id is not None and r.get("run_id") != run_id:
            continue
        out[(r["tier"], r["event_id"])] = r
    return out


def _deep_diff(a, b, path="", tol=0.0, out=None, max_diffs=200):
    """Recursively diff two JSON-like values. Numbers compared with tolerance `tol`; everything
    else (str/bool/None/list length/dict keys) compared exactly. Returns a list of
    (path, value_in_a, value_in_b) for every leaf that differs, capped at max_diffs entries."""
    if out is None:
        out = []
    if len(out) >= max_diffs:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        keys = sorted(set(a) | set(b))
        for k in keys:
            if k not in a:
                out.append((f"{path}.{k}", "<MISSING>", b[k]))
            elif k not in b:
                out.append((f"{path}.{k}", a[k], "<MISSING>"))
            else:
                _deep_diff(a[k], b[k], f"{path}.{k}", tol, out, max_diffs)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((f"{path}.<len>", len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            _deep_diff(x, y, f"{path}[{i}]", tol, out, max_diffs)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        if abs(a - b) > tol:
            out.append((path, a, b))
    else:
        if a != b:
            out.append((path, a, b))
    return out


def _format_diffs(diffs, limit=40):
    lines = [f"  {p}: committed={a!r} reproduced={b!r}" for p, a, b in diffs[:limit]]
    if len(diffs) > limit:
        lines.append(f"  ... and {len(diffs) - limit} more")
    return "\n".join(lines)


@pytest.fixture(scope="module")
def committed_summary():
    return _load_json(COMMITTED_SUMMARY)


@pytest.fixture(scope="module")
def reproduced_summary():
    return _load_json(REPRO_SUMMARY)


@pytest.fixture(scope="module")
def committed_reads():
    return _by_tier_event(_load_jsonl(COMMITTED_READS), run_id=COMMITTED_RUN_ID)


@pytest.fixture(scope="module")
def reproduced_reads(reproduced_summary):
    """reads.jsonl is append-only (docstring at the top of src/walk.py): a reproduction run in a
    clean CLONE still carries the committed history's prior sealed runs beside the new one (the
    clone's reads.jsonl is a tracked file `make reproduce` appends to, never replaces). So the
    reproduction's own run is picked out by run_id, taken from its own summary.json -- not assumed
    to be the only run in the file."""
    all_reads = _load_jsonl(REPRO_READS)
    run_id = reproduced_summary["run_id"]
    reads = _by_tier_event(all_reads, run_id=run_id)
    assert reads, f"no reads with run_id={run_id!r} found in {REPRO_READS}"
    return reads


def test_reproduce_run_id_present(reproduced_summary):
    """Sanity: the reproduction actually ran (has its own, necessarily different, run_id)."""
    assert reproduced_summary["run_id"] != COMMITTED_RUN_ID
    assert reproduced_summary["run_id"].startswith("walk_")


def test_reproduce_same_reads_covered(committed_reads, reproduced_reads):
    """The reproduction sealed a read for every (tier, event_id) the committed run 182828Z did,
    and nothing extra -- same corpus, same menu, same tier assignment."""
    missing = set(committed_reads) - set(reproduced_reads)
    extra = set(reproduced_reads) - set(committed_reads)
    assert not missing, f"reproduced run is missing reads for: {sorted(missing)[:20]}"
    assert not extra, f"reproduced run has extra reads not in committed run: {sorted(extra)[:20]}"


def test_reproduce_seal_hash_embeds_run_identity(committed_reads, reproduced_reads):
    """Documents, by execution, why raw `hash` values can never match across two runs: seal()
    hashes the record INCLUDING run_id and sealed_at. If this ever starts failing (i.e. hashes
    now match raw), walk.py's seal() changed to exclude run identity -- note it, don't silence
    this test."""
    key = next(iter(set(committed_reads) & set(reproduced_reads)))
    c, r = committed_reads[key], reproduced_reads[key]
    assert c["run_id"] != r["run_id"]
    assert c["sealed_at"] != r["sealed_at"]
    assert c["hash"] != r["hash"], (
        "raw sealed hashes matched across two different runs -- seal() no longer embeds "
        "run_id/sealed_at; re-read walk.py's seal()/verify_seal() before trusting this"
    )


def test_reproduce_content_hash_matches_read_by_read(committed_reads, reproduced_reads):
    """The actual reproducibility claim: strip run_id/sealed_at/hash and re-hash. If the read
    CONTENT is deterministic from the same DB + code + seeds, this content hash matches for every
    (tier, event_id) common to both runs. Every mismatch is reported by key, not just counted."""
    common = sorted(set(committed_reads) & set(reproduced_reads))
    assert common, "no (tier, event_id) reads in common between committed and reproduced runs"
    mismatches = []
    for key in common:
        ch = _content_hash(committed_reads[key])
        rh = _content_hash(reproduced_reads[key])
        if ch != rh:
            mismatches.append(key)
    assert not mismatches, (
        f"{len(mismatches)} / {len(common)} reads have a different content hash "
        f"(run_id/sealed_at/hash excluded) between committed run {COMMITTED_RUN_ID} and the "
        f"reproduction; first 20: {mismatches[:20]}"
    )


def test_reproduce_registered_block_matches(committed_summary, reproduced_summary):
    """registered (the hyperparameters src/walk.py ran with) must match exactly. A mismatch here
    most often means the committed src/walk.py at HEAD is not byte-for-byte the version that
    produced the committed summary.json -- check `git log --format='%h %ci' -- src/walk.py` vs
    `-- data/walk_forward/summary.json` before assuming nondeterminism."""
    diffs = _deep_diff(committed_summary["registered"], reproduced_summary["registered"], "registered")
    assert not diffs, f"registered block differs:\n{_format_diffs(diffs)}"


def test_reproduce_verdict_block_matches(committed_summary, reproduced_summary):
    diffs = _deep_diff(committed_summary["verdict"], reproduced_summary["verdict"], "verdict")
    assert not diffs, f"verdict block differs:\n{_format_diffs(diffs)}"


def test_reproduce_scored_numbers_match_to_1e9(committed_summary, reproduced_summary):
    """tiers, fdr, permutation, placebo and spec_curve's numeric leaves, tolerance 1e-9. Reported
    as one collected diff (path, committed value, reproduced value), not a wall of asserts."""
    diffs = []
    for block in ("tiers", "fdr", "permutation", "placebo", "spec_curve"):
        diffs += _deep_diff(committed_summary.get(block), reproduced_summary.get(block), block, tol=1e-9, max_diffs=200)
    assert not diffs, f"{len(diffs)} numeric/structural diffs (tol 1e-9) in tiers/fdr/permutation/placebo/spec_curve:\n{_format_diffs(diffs)}"
