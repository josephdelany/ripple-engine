"""WALK_FORWARD_PROTOCOL.md Amendment D (Brief B-4): after a run, every earlier run's rows are moved -- never edited,
never dropped -- to runs/<run_id>/*.jsonl.gz; the tree holds the current run only; both sides still verify."""
import gzip
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import walk as W
from test_read import _synthetic
from test_walk import MENU, FAST


def _rows(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def test_amendment_d_archive_moves_prior_runs_and_both_sides_verify(tmp_path):
    c = _synthetic(n=40, seed=3)
    w1 = W.Walk(c, MENU, out_dir=tmp_path, params=FAST, quiet=True, run_id="run_A").run_reads()
    w2 = W.Walk(c, MENU, out_dir=tmp_path, params=FAST, quiet=True, run_id="run_B").run_reads()
    n = len(w1.reads)
    assert len(_rows(tmp_path / "reads.jsonl")) == 2 * n                                 # append-only: both runs in the tree before archiving
    before = {r["hash"] for r in _rows(tmp_path / "reads.jsonl") if r["run_id"] == "run_A"}
    man = W.archive_prior_runs(tmp_path, "run_B")
    assert set(man) == {"run_A"} and man["run_A"]["reads.jsonl"] == n and man["run_A"]["scores.jsonl"] == n and man["run_A"]["weights.jsonl"] == n
    assert man["run_A"]["reads_seal_ok"] is True and man["run_A"]["reads_records_in_archive"] == n
    # the tree holds run_B only; the archive holds run_A whole, byte-identical seals
    for name in ("reads.jsonl", "scores.jsonl", "weights.jsonl"):
        assert {r["run_id"] for r in _rows(tmp_path / name)} == {"run_B"} and len(_rows(tmp_path / name)) == n
        assert {r["run_id"] for r in _rows(tmp_path / "runs" / "run_A" / (name + ".gz"))} == {"run_A"}
    assert {r["hash"] for r in _rows(tmp_path / "runs" / "run_A" / "reads.jsonl.gz")} == before
    assert W.verify_file(tmp_path / "reads.jsonl") == (True, n, None)
    assert W.verify_file(tmp_path / "runs" / "run_A" / "reads.jsonl.gz") == (True, n, None)
    # a third run archives run_B beside run_A; archiving again with nothing to move is a no-op
    W.Walk(c, MENU, out_dir=tmp_path, params=FAST, quiet=True, run_id="run_C").run_reads()
    man2 = W.archive_prior_runs(tmp_path, "run_C")
    assert set(man2) == {"run_B"} and W.archive_prior_runs(tmp_path, "run_C") == {}
    assert sorted(os.listdir(tmp_path / "runs")) == ["run_A", "run_B"]
    assert len(_rows(tmp_path / "runs" / "run_A" / "reads.jsonl.gz")) == n                  # untouched by later archiving
    # the leakage test and the seal check read the run in the tree
    w3 = W.Walk(c, MENU, out_dir=tmp_path / "x", params=FAST, quiet=True, break_filtration=True).run_reads()
    w_c = W.Walk(c, MENU, out_dir=tmp_path / "y", params=FAST, quiet=True).run_reads()
    assert W.leakage_test(w_c, w3)["asserted"]
