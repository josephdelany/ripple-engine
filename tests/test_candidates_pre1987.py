"""Brief B-3: the pre-1987 candidate sheet (data/candidates/pre1987_candidates.csv) obeys its registration
(data/candidates/REGISTRATION.md): dates 1946-01..1986-12, one of the three sources, an actor from the registered
set, the Big Moves join consistent, suggested_title blank, and the summary's counts equal the sheet's. DB-free:
reads the committed CSV / JSON only. The generator writes nothing to any table (asserted on its source text)."""
import csv
import json
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
CSV = os.path.join(ROOT, "data", "candidates", "pre1987_candidates.csv")
SUMMARY = os.path.join(ROOT, "data", "candidates", "pre1987_candidates_summary.json")
SRC = os.path.join(ROOT, "src", "engine", "pre1987_candidates.py")


def test_b3_candidate_sheet_obeys_its_registration():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    assert rows and list(rows[0]) == ["event_date", "actors", "source", "source_id", "source_detail", "inside_big_move", "episode_id",
                                       "monthly_move_pct", "wti_chg_3m_pct", "suggested_title"]
    for r in rows:
        assert "1946-01-01" <= r["event_date"] <= "1986-12-31"
        assert r["source"] in ("ICB v16", "COW War v4.0 inter-state", "COW War v4.1 intra-state", "Dyadic MID 4.03")
        assert r["actors"] and r["source_id"] and r["suggested_title"] == ""
        assert r["inside_big_move"] in ("True", "False")
        assert (r["episode_id"] != "") == (r["inside_big_move"] == "True") == (r["monthly_move_pct"] != "")
        if r["source"] == "Dyadic MID 4.03":
            assert "hihost 4" in r["source_detail"] or "hihost 5" in r["source_detail"]
    assert rows == sorted(rows, key=lambda r: (r["event_date"], r["source"], r["source_id"]))
    assert len({(r["source"], r["source_id"]) for r in rows}) == len(rows)                 # one row per source record
    s = json.load(open(SUMMARY))
    assert s["n_rows"] == len(rows) and sum(s["by_decade"].values()) == len(rows) and sum(s["by_source"].values()) == len(rows)
    assert s["inside_big_move"] == sum(1 for r in rows if r["inside_big_move"] == "True")
    src = open(SRC, encoding="utf-8").read()
    import re
    assert not re.search(r"INSERT INTO|UPDATE \w+ SET|DELETE FROM|executemany|\.commit\(", src)      # the generator writes no table
