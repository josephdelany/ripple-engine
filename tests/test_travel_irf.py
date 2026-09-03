"""Band 5, "where does it travel", after the rewire of 2026-09-03.

Two things are proved here, both of them Joe's acceptance criteria:

  1. NO MODULE CONDITIONS ON THE RETIRED LABEL. `sr_outcome_90` was retired at κ≈0 against
     ICB/MID/UCDP on 2026-09-02 (OUTCOME_MAPPING.md Amendment 1). It is corpus-derived, not an
     outcome. A retired label may still be STORED (it is a record of what the corpus said) and
     READ for the retirement audit that retired it -- but nothing may CONDITION on it: no WHERE,
     no filter, no branch. This test reads every SQL string in src/ and fails on any that does.

  2. THE BAND'S NUMBERS ALL TRACE TO data/ripple/irf.json. Every number the Story propagation
     block shows is checked back against the registered local projections, cell by cell, and the
     count is checked too -- because the finding here is an ABSENCE, and a band that quietly
     dropped its null rows would look like a pass (DESIGN.md Amendment 1 A1.1, A1.4).

Registrations under test: DESIGN.md Amendment 1 (A1.1 selection, A1.2 fields, A1.3 absence
language, A1.4 order + finding sentence, A1.5 provenance); OUTCOME_MAPPING.md Amendment 1.
"""
import ast
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import story_read as SR            # noqa: E402

IRF = ROOT / "data" / "ripple" / "irf.json"
DB = ROOT / "data" / "oil.db"


def _db_ready():
    if not DB.exists():
        return False
    try:
        return sqlite3.connect(DB).execute("SELECT COUNT(*) FROM events").fetchone()[0] > 0
    except sqlite3.Error:
        return False


needs_db = pytest.mark.skipif(not _db_ready(), reason="needs a built data/oil.db (gitignored)")


# =================================================================================================
# 1. nothing conditions on the retired label
# =================================================================================================

# The retirement audit is the work that PROVED the label worthless: it must read the column to
# cross-tabulate it against IES-90. Reading it there is the point; conditioning on it is not.
AUDIT_ALLOWED = {"src/state/outcomes.py", "src/state/ies90.py"}
LABEL = "sr_outcome_90"


# This repo builds SQL incrementally -- `q += " AND sr_outcome_90=?"` was exactly how the retired
# filter was written -- so a detector that only looks at whole statements, or only at literals
# containing SELECT/WHERE, sees nothing. We therefore look at EVERY string constant and ask one
# question: is the label used as a PREDICATE?
#
#   predicate  ->  preceded by a boolean connective (WHERE / AND / OR / ON / HAVING), or sitting
#                  after a WHERE inside the same literal, and compared with =, IS, IN, ...
#   NOT a predicate ->  named in a SELECT list ("SELECT ..., sr_outcome_90 FROM events") or
#                  assigned in an UPDATE ... SET list ("sr_outcome_30=?,sr_outcome_90=?"), which
#                  are a read and a write. Storing the corpus's own record is allowed; letting it
#                  decide which rows exist is not.
CONNECTIVE = re.compile(r"\b(where|and|or|on|having)\s+(not\s+)?\(*\s*" + LABEL, re.I)
COMPARED = re.compile(LABEL + r"\s*(=|!=|<>|>|<|\bis\b|\bin\b|\blike\b)", re.I)


def _literals(path):
    """Every string constant in a module (ast joins implicit concatenation for us)."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:                                   # not our problem here; other tests catch it
        return []
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _conditions_on(sql):
    """True if this fragment uses the retired label to decide which rows come back."""
    if LABEL not in sql or not COMPARED.search(sql):
        return False
    if CONNECTIVE.search(sql):
        return True
    # single-literal statement: the label sits in the predicate half
    low = sql.lower()
    w = low.find("where")
    return w != -1 and LABEL in sql[w:]


def test_amendment1_no_module_conditions_on_retired_sr_outcome_90():
    offenders = []
    for f in sorted((ROOT / "src").rglob("*.py")):
        rel = f.relative_to(ROOT).as_posix()
        if rel in AUDIT_ALLOWED:
            continue
        for sql in _literals(f):
            if _conditions_on(sql):
                offenders.append(f"{rel}: {' '.join(sql.split())[:160]}")
    assert not offenders, (
        "a retired label (sr_outcome_90, κ≈0, OUTCOME_MAPPING.md Amendment 1) is still deciding "
        "which rows exist:\n  " + "\n  ".join(offenders))


def test_amendment1_propagate_module_does_not_query_the_retired_label():
    """propagate.py fed the Story band and filtered on the label at line 45. The filter is gone and
    the `branch` parameter with it -- gone rather than defaulted, so a stale caller fails loudly."""
    src = (ROOT / "src" / "propagate.py").read_text(encoding="utf-8")
    assert not any(_conditions_on(s) for s in _literals(ROOT / "src" / "propagate.py")), \
        "propagate.py still conditions on the retired label"
    # the label survives in this module only as the docstring recording why the filter went
    assert LABEL not in re.sub(r'"""[\s\S]*?"""', "", src, count=1), \
        "propagate.py names the retired label outside its docstring"
    tree = ast.parse(src)
    fns = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for name in ("propagate", "_contributing"):
        args = [a.arg for a in fns[name].args.args] + [a.arg for a in fns[name].args.kwonlyargs]
        assert "branch" not in args, f"{name}() still takes a branch: the branch was the retired label"
    # and the module says why, so the next reader does not put it back
    assert "retired" in src.lower() and "OUTCOME_MAPPING" in src


# =================================================================================================
# 2. every number in the band traces to irf.json
# =================================================================================================

def _file_rows(shock):
    doc = json.loads(IRF.read_text())
    return [r for r in doc["rows"]
            if r["shock"] == shock and r["spec"] == "total" and r["sample"] == "full"], doc["meta"]


@pytest.mark.parametrize("shock", ["infrastructure_attack", "chokepoint_disruption",
                                   "conflict_escalation", "sanctions", "opec_decision",
                                   "demand_shock", "policy_response"])
def test_amendment1_a1_1_every_registered_cell_is_shown_for_every_class(shock):
    """A1.1: 53 cells per class, ALL of them, never filtered by verdict. A dropped null would be a
    silent lie about an absence, so the count is asserted, not just the contents."""
    rows, _ = _file_rows(shock)
    t = SR.travel(shock)
    cells = [c for h in t["hops"] for c in h["cells"]]
    assert t["available"] and t["shock"] == shock
    assert len(cells) == len(rows) == 53, f"{len(cells)} cells shown for {len(rows)} registered rows"
    assert {c["node"] for c in cells} == {r["node"] for r in rows}
    assert "note" not in t, t.get("note")            # nothing fell outside the registered hop ladder
    # the nulls are present and are the majority -- the finding is the absence
    assert sum(1 for c in cells if c["verdict"] == "NULL") > 0


@pytest.mark.parametrize("shock", ["infrastructure_attack", "chokepoint_disruption"])
def test_amendment1_a1_2_each_cell_traces_to_its_irf_json_row(shock):
    """A1.2: estimate, 95% band, n and verdict are the file's, at the row's OWN headline horizon."""
    rows, meta = _file_rows(shock)
    by_node = {r["node"]: r for r in rows}
    t = SR.travel(shock)
    for c in (c for h in t["hops"] for c in h["cells"]):
        r = by_node[c["node"]]
        h = next(x for x in r["irf"] if x["h"] == r["headline_h"])
        assert c["h"] == r["headline_h"], f"{c['node']}: horizon not the registered headline_h"
        assert c["estimate"] == h["beta"]
        assert (c["lo95"], c["hi95"]) == (h["lo95"], h["hi95"])     # EHW HC1, the registered primary
        assert c["n"] == r["n_events"]
        assert c["verdict"] == r["verdict"]                          # copied, never recomputed
        assert c["fragile"] == bool(r.get("fragile"))
        assert c["series_id"] == r["series_id"] and c["freq"] == r["freq"]
        assert c["unit"] == ("%" if r["transform"] in ("log", "log1p") else "index points")
    # A1.5 provenance travels with the band
    assert t["source"] == "data/ripple/irf.json" and t["spec"] == "total" and t["sample"] == "full"
    assert t["registration"] == meta["registration"] and t["run_when"] == meta["when"]
    assert t["seed"] == meta["seed"] and t["n_placebo"] == meta["n_placebo"]


def test_amendment1_a1_3_absence_language_is_the_registered_mapping():
    """A1.3: verdict -> state -> colour -> caption, exactly as registered. Amber is not used here."""
    seen = set()
    for shock in ("infrastructure_attack", "chokepoint_disruption", "conflict_escalation",
                  "sanctions", "opec_decision", "demand_shock", "policy_response"):
        for c in (c for h in SR.travel(shock)["hops"] for c in h["cells"]):
            seen.add(c["verdict"])
            assert c["zero_line"] is True                       # §2: the zero rule, on every cell
            if c["verdict"] == "TRANSMITTING":
                assert (c["state"], c["colour"]) == ("excludes_zero", "green")
                assert "excludes zero" in c["caption"] and "placebo" in c["caption"]
            elif c["verdict"] == "INSUFFICIENT":
                assert (c["state"], c["colour"]) == ("insufficient", "hatch")
                assert c["caption"].startswith(f"insufficient (n={c['n']})") and "minimum of 15" in c["caption"]
            else:
                assert c["verdict"] == "NULL"
                assert (c["state"], c["colour"]) == ("crosses_zero", "neutral")
                assert ("flagged fragile" in c["caption"]) if c["fragile"] else \
                       (c["caption"] == "The interval crosses zero: no effect distinguishable from "
                                        "none at this sample size.")
            assert c["colour"] != "amber", "§2 reserves amber for a baseline comparison this band has none of"
    assert seen == {"TRANSMITTING", "NULL", "INSUFFICIENT"}        # all three states really occur


def test_amendment1_a1_4_hop_order_and_finding_sentence_are_the_registered_ones():
    t = SR.travel("infrastructure_attack")
    assert [h["hop"] for h in t["hops"]] == ["0", "1", "2", "3", "4", "x", "e"]
    k, n = t["counts"]["TRANSMITTING"], t["counts"]["cells"]
    assert t["finding"] == (f"{k} of {n} registered cells transmit for this class." if k else
                            f"No cell transmits for this class: all {n} registered cells are null "
                            f"or insufficient.")
    assert str(k) in t["finding"] or k == 0            # a count, never an adjective
    # the counts add up: nothing is shown that is not counted, nothing counted that is not shown
    assert t["counts"]["TRANSMITTING"] + t["counts"]["NULL"] + t["counts"]["INSUFFICIENT"] == n


def test_amendment1_unknown_class_states_the_absence_rather_than_inventing_a_band():
    t = SR.travel("not_a_registered_shock")
    assert t["available"] is False and "not a registered shock set" in t["note"]
    assert "hops" not in t                             # no fabricated cells, ever
    assert SR.travel(None)["available"] is False


# =================================================================================================
# 3. the Story object itself
# =================================================================================================

@needs_db
def test_amendment1_story_propagation_block_is_the_irf_band_not_the_retired_one():
    s = SR.read(event_id="abqaiq_attack_2019", log=False)
    p = s["propagation"]
    assert p["available"] and p["source"] == "data/ripple/irf.json"
    assert p["shock"] == s["event_class"] == "infrastructure_attack"
    # the superseded propagate.py shape is gone from this block
    cells = [c for h in p["hops"] for c in h["cells"]]
    assert not any(k in p for k in ("signed_median_pct", "material_move_pct", "contributing_n"))
    assert not any(k in c for c in cells for k in ("signed_median_pct", "material_move_pct"))
    # and every number in it is in the file
    rows, _ = _file_rows("infrastructure_attack")
    by_node = {r["node"]: r for r in rows}
    assert len(cells) == len(rows)
    for c in cells:
        r = by_node[c["node"]]
        h = next(x for x in r["irf"] if x["h"] == r["headline_h"])
        assert (c["estimate"], c["lo95"], c["hi95"], c["n"], c["verdict"]) == \
               (h["beta"], h["lo95"], h["hi95"], r["n_events"], r["verdict"])


@needs_db
def test_amendment1_branch_rates_still_carry_the_retired_banner():
    """Joe's rule 3: a surface may still show the retired label's numbers, but only bannered."""
    s = SR.read(event_id="abqaiq_attack_2019", log=False)
    br = s["branches"]
    assert br["retired"] is True and "retired" in br["outcome_label"] and LABEL in br["outcome_label"]
