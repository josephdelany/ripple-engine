"""WALK_FORWARD_PROTOCOL.md Amendment I (Brief 2, B-9): every seed registered; two consecutive runs on the same inputs
produce identical content hashes and the same content digest (the seal hash itself differs by run id and clock)."""
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import walk as W
from test_read import _synthetic
from test_walk import MENU, FAST

M13 = {"id": "M13_recalibrated", "kind": "recalibrated"}
MENU13 = {"items": MENU["items"] + [M13]}


def test_amendment_i_two_runs_same_inputs_same_content(tmp_path):
    w1 = W.Walk(_synthetic(n=60, seed=3), MENU13, out_dir=tmp_path / "a", params=FAST, quiet=True).run_reads()
    w2 = W.Walk(_synthetic(n=60, seed=3), MENU13, out_dir=tmp_path / "b", params=FAST, quiet=True).run_reads()
    assert [r["content_hash"] for r in w1.reads] == [r["content_hash"] for r in w2.reads]
    assert W.content_digest(w1.reads) == W.content_digest(w2.reads)
    assert w1.run_id != w2.run_id and all(a["hash"] != b["hash"] for a, b in zip(w1.reads, w2.reads))     # the seal carries clock + run id
    for r in w1.reads:
        assert W.content_hash(r) == r["content_hash"]                                                    # recomputable from the sealed record
        assert W.verify_seal(r)
    assert "seeds" in W.REGISTERED and set(W.REGISTERED["seeds"]) >= {"bootstrap_and_spa", "permutation", "placebo", "reliability_bands", "power", "random_analogs"}
    # the digest read back from the file equals the in-memory one
    rows = [json.loads(l) for l in (tmp_path / "a" / "reads.jsonl").read_text().splitlines() if l.strip()]
    assert W.content_digest(rows) == W.content_digest(w1.reads)


def test_amendment_i_a_changed_input_changes_the_digest(tmp_path):
    w1 = W.Walk(_synthetic(n=60, seed=3), MENU13, out_dir=tmp_path / "a", params=FAST, quiet=True).run_reads()
    w3 = W.Walk(_synthetic(n=60, seed=4), MENU13, out_dir=tmp_path / "c", params=FAST, quiet=True).run_reads()
    assert W.content_digest(w1.reads) != W.content_digest(w3.reads)
