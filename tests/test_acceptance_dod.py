"""Two defects found in src/acceptance_v2.py --dod on 2026-09-02, each pinned here:
1. D7 read "paper drafted=False" while docs/PAPER_DRAFT.md existed -- a fixed filename list, not a missing paper.
2. D4 reported an older walk run than the summary.json in the tree: the --dod ran 29 s before session B finished
   writing the file. Not a cache; the acceptance now stamps the file it read and says so if it changed mid-run."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import acceptance_v2 as A     # noqa: E402


def test_dod_d7_finds_the_paper_by_glob_not_a_fixed_name(tmp_path, monkeypatch):
    status, evidence, note = A._d7()
    real = sorted(str(p.relative_to(ROOT)) for pat in ("PAPER*.md", "docs/PAPER*.md", "docs/paper*.md", "paper/*.md") for p in ROOT.glob(pat))
    assert ("paper drafted=True" in note) == bool(real)
    for p in real:
        assert p in note                      # the note names the file it found, so a wrong path is visible
    assert real, "no PAPER*.md in the tree: this test would not be pinning anything"
    # a tree with no paper reads False, and the old fixed names are not what decides it
    monkeypatch.setattr(A, "ROOT", tmp_path)
    (tmp_path / "PAPER.md").write_text("x")
    assert "paper drafted=True" in A._d7()[2]


def test_dod_d4_stamps_the_walk_file_it_read_and_flags_a_mid_run_rewrite():
    rid, written = A._walk_stamp()
    live = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    assert rid == live["run_id"] and written                       # the stamp is the file on disk now, never a cached value
    status, evidence, note = A._d4()
    assert live["run_id"] in note and "written" in note            # D4 names the run AND when that file was written
    assert evidence == "data/walk_forward/summary.json"
    rec = json.loads((ROOT / "data" / "acceptance_dod.json").read_text())
    for k in ("walk_summary_at_start", "walk_summary_at_end", "walk_summary_changed_during_run"):
        assert k in rec                                            # a --dod that straddles a walk records both stamps


def test_dod_d4_passes_only_with_the_four_registered_baselines():
    live = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    g = list((live["tiers"]["daily"]["G"]["engine_vs"]).keys())
    status, _, note = A._d4()
    present, missing = note.split("missing:")[0], note.split("missing:")[1]
    if len(g) >= 4:
        assert status == "PASS" and "persistence" in g             # G-persistence (protocol Amendment B) landed
        assert "four baselines" in present and "four baselines" not in missing and missing.strip() == "[]"
    else:
        assert "four baselines" in missing and status != "PASS"
