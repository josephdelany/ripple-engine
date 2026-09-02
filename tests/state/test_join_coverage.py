"""PATH Step 3 -- test_join_coverage.py: every corpus event has a situation_state row; coverage per block is
reported for 1946-86 and 1987-> (numbers PUBLISHED, not asserted). Runs against the real oil.db when the
join has been run (data/state/join_coverage.json present); otherwise skipped with the command to run."""
import json
import sqlite3
from pathlib import Path

import pytest

from _helpers import P
import situation_state as SS


def _ready():
    if not SS.COVERAGE_OUT.exists() or not P.DB.exists():
        pytest.skip("run `python3 src/state/situation_state.py` first (joins every corpus event, writes data/state/join_coverage.json)")
    conn = sqlite3.connect(f"file:{P.DB}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT name FROM sqlite_master WHERE name='situation_state'").fetchone():
            pytest.skip("situation_state table absent: run src/state/situation_state.py")
    finally:
        conn.close()


def test_jc1_every_corpus_event_has_a_row_and_nothing_postdates_its_event():
    _ready()
    conn = sqlite3.connect(f"file:{P.DB}?mode=ro", uri=True)
    try:
        n_events = conn.execute("SELECT count(*) FROM events").fetchone()[0]
        with_row = conn.execute("SELECT count(DISTINCT event_id) FROM situation_state").fetchone()[0]
        assert with_row == n_events, f"{n_events - with_row} events without a situation_state row"
        late = conn.execute("SELECT count(*) FROM situation_state s JOIN events e USING(event_id) WHERE s.vintage > e.event_date").fetchone()[0]
        assert late == 0
    finally:
        conn.close()


def test_jc2_coverage_per_block_per_era_is_published():
    _ready()
    cov = json.loads(SS.COVERAGE_OUT.read_text())
    assert set(cov["eras"]) <= {"1946-86", "1987->"} and cov["eras"]
    for era, e in cov["eras"].items():
        assert set(e["blocks"]) == {"PHYSICAL", "MARKET", "ACTORS", "DYADS", "SYSTEM", "NARRATIVE"}
        for b, v in e["blocks"].items():
            assert 0.0 <= v["share_of_events"] <= 1.0
    assert "acceptance_S2" in cov                     # the S2 threshold is reported, whatever it says
    print("coverage:", json.dumps(cov["acceptance_S2"]), {era: {b: v["share_of_events"] for b, v in e["blocks"].items()} for era, e in cov["eras"].items()})
