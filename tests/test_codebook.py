"""PATH Step 1: WORLD_STATE_CODEBOOK.md parses; every field has all 8 columns; no source URL outside
the register (WORLD_STATE_SOURCES.md / WORLD_STATE_FRAMEWORK.md). DB-free."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = {"PHYSICAL", "MARKET", "ACTORS", "DYADS", "SYSTEM", "NARRATIVE"}
COLS = ["block", "field", "unit", "resolution", "source", "coverage", "licence", "rule_id"]
URL = re.compile(r"https?://[^\s|)]+")


def rows():
    out = []
    for line in (ROOT / "docs" / "reference" / "WORLD_STATE_CODEBOOK.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| block") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        out.append(dict(zip(COLS, cells)) | {"_n": len(cells)})
    return out


def test_cb1_every_field_has_all_eight_columns():
    rs = rows()
    assert len(rs) >= 40
    for r in rs:
        assert r["_n"] == 8, r
        assert all(r[c] for c in COLS), r
        assert r["block"] in BLOCKS, r["block"]
        assert re.fullmatch(r"WS-[PMADSN]\d{2}", r["rule_id"]), r["rule_id"]
        assert r["resolution"].split("/")[0].split("→")[0].strip() in {"d", "w", "m", "q", "a", "e"}, r["resolution"]


def test_cb2_rule_ids_and_field_ids_are_unique():
    rs = rows()
    assert len({r["rule_id"] for r in rs}) == len(rs)
    assert len({r["field"] for r in rs}) == len(rs)


def test_cb3_no_source_url_outside_the_register():
    register = (ROOT / "docs" / "reference" / "WORLD_STATE_SOURCES.md").read_text(encoding="utf-8") + (ROOT / "docs" / "reference" / "WORLD_STATE_FRAMEWORK.md").read_text(encoding="utf-8")
    text = (ROOT / "docs" / "reference" / "WORLD_STATE_CODEBOOK.md").read_text(encoding="utf-8")
    urls = {u.rstrip(".,") for u in URL.findall(text)}
    assert urls, "the codebook must cite its sources"
    missing = sorted(u for u in urls if u not in register)
    assert not missing, f"URLs not in the register: {missing}"


def test_cb4_licence_codes_are_the_registered_set():
    for r in rows():
        assert r["licence"] in {"PD", "CC-BY", "CC-BY-SA", "cite", "local", "gap"}, r
