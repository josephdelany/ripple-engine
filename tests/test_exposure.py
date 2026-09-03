"""PHYSICAL_EXPOSURE_REGISTRATION §2/§3 as tests: the three tiers, the vintage rule, and above all
the rule that a missing term is NULL and never zero.

The registers this study needs are two other sessions' and are not in the tree yet, so the T1 and
T2 paths cannot be exercised against real data today. They are exercised against fixtures instead —
hand-built CSV rows in a tmp_path, never a real table (CLAUDE.md <no_fabrication>: these are
pure-function inputs, not rows, and nothing here writes to the corpus). Otherwise the null discipline
would go untested until the day it matters, which is the day it fails.

Every test names the clause it covers.
"""
import csv
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import exposure as X  # noqa: E402

T = "2024-06-01"


def _cap(tmp_path, rows):
    p = tmp_path / "capacity.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["country", "measure", "value_kbd", "reference_year", "published_at", "source_url"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return X.read_capacity_register(p)


def _ck(tmp_path, rows):
    p = tmp_path / "chokepoints.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["chokepoint", "flow_mbd", "world_seaborne_mbd", "published_at", "source_url"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return X.read_chokepoint_register(p)


def _row(c, v, pub, measure="crude_production_capacity", year="2023"):
    return {"country": c, "measure": measure, "value_kbd": v, "reference_year": year,
            "published_at": pub, "source_url": "https://example.invalid/register"}


# ------------------------------------------------------------------ the invariant the module exists for

def test_S2_a_Val_is_either_a_number_or_a_reason_never_both_and_never_neither():
    with pytest.raises(AssertionError):
        X.Val(value=1.0, reason="both")
    with pytest.raises(AssertionError):
        X.Val()
    assert X.Val(value=0.0).ok is True          # a real measured ZERO is legal and is not a null
    assert X.Val(reason="r").ok is False


def test_S2_sum_is_null_when_any_part_is_null_never_the_sum_of_the_known_parts():
    """The failure this module exists to prevent: 3 known countries and 1 unknown must not add up
    to the total of the 3. That is `max(default=0)` wearing a different hat."""
    parts = [X.Val(value=1000.0), X.Val(value=500.0), X.Val(reason="no register")]
    total, missing = X._sum(parts)
    assert total is None and len(missing) == 1
    assert X._sum([X.Val(value=1000.0), X.Val(value=500.0)])[0] == 1500.0


def test_S2_x1_is_null_when_ANY_coded_country_lacks_a_register(tmp_path):
    cap = _cap(tmp_path, [_row("country.iraq", 4000, "2024-01-01")])
    x1, partial, missing = X.x1_country_capacity({"country.iraq", "country.iran"}, T, cap)
    assert x1.value is None, "X1 must not be 4000 with Iran silently worth zero"
    assert x1.reason == X.NullReason.COUNTRY_NOT_IN_REGISTER
    assert "country.iran" in x1.detail and missing == ["country.iran"]
    assert partial == 4000.0, "the partial sum is kept as a diagnostic"


def test_S2_the_partial_sum_is_never_returned_as_X1(tmp_path):
    """It is published beside X1 under a different name, like `level_location`, so the information
    survives without ever being mistaken for the value."""
    cap = _cap(tmp_path, [_row("country.iraq", 4000, "2024-01-01")])
    x1, partial, _ = X.x1_country_capacity({"country.iraq", "country.iran"}, T, cap)
    assert partial is not None and x1.value is None and partial != x1.value
    src = (ROOT / "src" / "exposure.py").read_text()
    assert '"x1_partial_kbd"' in src and "never enters a regression" in src


def test_S2_x1_sums_when_every_country_is_covered(tmp_path):
    cap = _cap(tmp_path, [_row("country.iraq", 4000, "2024-01-01"), _row("country.iran", 3000, "2024-01-01")])
    x1, partial, missing = X.x1_country_capacity({"country.iraq", "country.iran"}, T, cap)
    assert x1.value == 7000.0 and not missing and x1.published_at == "2024-01-01"


def test_S2_no_country_coded_is_its_own_reason_not_a_zero():
    x1, partial, _ = X.x1_country_capacity(set(), T, {"country.iraq": []})
    assert x1.value is None and x1.reason == X.NullReason.NO_COUNTRY_CODING and partial is None


def test_S2_an_absent_register_is_a_counted_null_not_a_zero():
    x1, _, _ = X.x1_country_capacity({"country.iraq"}, T, None)
    assert x1.value is None and x1.reason == X.NullReason.NO_CAP_REGISTER
    x2 = X.x2_chokepoint_share({"chokepoint.hormuz"}, T, None)
    assert x2.value is None and x2.reason == X.NullReason.NO_CHOKE_REGISTER


# ------------------------------------------------------------------ §3 the vintage rule

def test_S3_a_register_published_on_or_after_t_is_not_used(tmp_path):
    """"A register's knowable_at is its publication date, not its reference year." The 2023 figure
    published the day after the event may not inform it."""
    cap = _cap(tmp_path, [_row("country.iraq", 4000, "2024-06-01"),      # == t: not strictly before
                          _row("country.iraq", 9999, "2024-06-02")])     # after t
    x1, _, _ = X.x1_country_capacity({"country.iraq"}, T, cap)
    assert x1.value is None, "a register published on the event date is not knowable at it"
    cap2 = _cap(tmp_path, [_row("country.iraq", 4000, "2024-05-31"), _row("country.iraq", 9999, "2024-06-02")])
    x1b, _, _ = X.x1_country_capacity({"country.iraq"}, T, cap2)
    assert x1b.value == 4000.0 and x1b.published_at == "2024-05-31"


def test_S3_the_latest_publication_before_t_wins_not_the_latest_reference_year(tmp_path):
    cap = _cap(tmp_path, [_row("country.iraq", 4000, "2023-01-01", year="2025"),
                          _row("country.iraq", 4200, "2024-01-01", year="2019")])
    x1, _, _ = X.x1_country_capacity({"country.iraq"}, T, cap)
    assert x1.value == 4200.0, "publication date orders the register, not the reference year"


def test_S3_every_value_in_a_real_build_predates_its_event(monkeypatch, tmp_path):
    """The filtration test §3 demands, run over the whole corpus with a fixture register."""
    cap = _cap(tmp_path, [_row(c, 1000, "1970-01-01") for c in ("country.iran", "country.iraq",
                                                                "country.saudi_arabia", "country.usa")])
    conn = sqlite3.connect(f"file:{ROOT/'data'/'oil.db'}?mode=ro", uri=True)
    rows = X.build(conn, cap=cap, ck={})
    conn.close()
    for r in rows:
        for k in ("X1_kbd", "X2_share", "X3_buffer_share", "SPARE_kbd"):
            pub = r[k].get("published_at")
            if pub is not None:
                assert pub < r["date"], f"{r['event_id']}: {k} used a register published {pub} >= {r['date']}"


# ------------------------------------------------------------------ §2 T2 and T3

def test_S2_x2_is_a_share_of_world_seaborne_and_nulls_without_the_denominator(tmp_path):
    ck = _ck(tmp_path, [{"chokepoint": "chokepoint.hormuz", "flow_mbd": 21.0,
                         "world_seaborne_mbd": 60.0, "published_at": "2024-01-01", "source_url": "u"}])
    x2 = X.x2_chokepoint_share({"chokepoint.hormuz"}, T, ck)
    assert abs(x2.value - 21.0 / 60.0) < 1e-12
    ck2 = _ck(tmp_path, [{"chokepoint": "chokepoint.hormuz", "flow_mbd": 21.0,
                          "world_seaborne_mbd": "", "published_at": "2024-01-01", "source_url": "u"}])
    assert X.x2_chokepoint_share({"chokepoint.hormuz"}, T, ck2).reason == X.NullReason.NO_WORLD_SEABORNE


def test_S2_x3_is_null_when_either_side_is_and_keeps_BOTH_reasons():
    """"we do not know the capacity" and "we do not know the buffer" are different holes."""
    assert X.x3_buffer_share(X.Val(reason="no cap"), X.Val(value=2000.0)).reason == X.NullReason.X1_NULL
    assert X.x3_buffer_share(X.Val(value=5000.0), X.Val(reason="no spare")).reason == X.NullReason.SPARE_NOT_PUBLISHED
    got = X.x3_buffer_share(X.Val(value=5000.0), X.Val(value=2000.0))
    assert got.value == 2.5, "5000 kb/d against a 2000 kb/d buffer consumes 2.5x the world's spare"


def test_S2_spare_before_the_first_published_vintage_is_null_not_zero_and_not_the_earliest_value():
    rows = [("2022-03-01", "2022-01-01", 2.31), ("2022-04-01", "2022-02-01", 1.88)]
    assert X.spare_at(rows, "1990-01-01").value is None
    assert X.spare_at(rows, "1990-01-01").reason == X.NullReason.SPARE_NOT_PUBLISHED
    assert X.spare_at(rows, "2022-05-01").value == 1880.0          # mb/d -> kb/d, last knowable
    assert X.spare_at([], "2024-01-01").value is None


# ------------------------------------------------------------------ no silent zeros anywhere in the file

def test_the_source_contains_no_silent_zero_idiom():
    """Checked on the PARSED CODE, not on the text. The defect this module guards against is one
    line long, easy to reintroduce, and invisible in output until it has already published a wrong
    number — but the module's own prose has to be free to name the idioms it forbids, and a text
    grep that reads its own warning can never pass. So this walks the AST instead: prose cannot
    trip it, and no amount of rewording can hide a real one."""
    import ast
    tree = ast.parse((ROOT / "src" / "exposure.py").read_text())
    bad = []
    for n in ast.walk(tree):
        # `f(..., default=0)` -- the max()/min() fallback that started all this
        if isinstance(n, ast.Call):
            for kw in n.keywords:
                if kw.arg == "default" and isinstance(kw.value, ast.Constant) and kw.value.value in (0, 0.0):
                    bad.append(f"line {n.lineno}: default=0 fallback")
        # `x or 0` -- a null quietly becoming a number
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
            for v in n.values[1:]:
                if isinstance(v, ast.Constant) and v.value in (0, 0.0):
                    bad.append(f"line {n.lineno}: `or 0` fallback")
    assert not bad, "silent-zero idiom in exposure.py: " + "; ".join(bad)


def test_the_ast_check_would_actually_catch_one():
    """A guard nobody has seen fail is a guard nobody knows works."""
    import ast
    for snippet, why in [("m = max(xs, default=0)", "default=0"), ("v = spare or 0", "or 0")]:
        tree = ast.parse(snippet)
        hits = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                hits += [1 for kw in n.keywords
                         if kw.arg == "default" and isinstance(kw.value, ast.Constant) and kw.value.value in (0, 0.0)]
            if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
                hits += [1 for v in n.values[1:] if isinstance(v, ast.Constant) and v.value in (0, 0.0)]
        assert hits, f"the check misses {why}"


# ------------------------------------------------------------------ the exclusion table is published

def test_S2_the_exclusion_table_counts_every_event_exactly_once():
    p = ROOT / "data" / "exposure" / "exposure.json"
    if not p.exists():
        pytest.skip("run python3 src/exposure.py first")
    d = json.loads(p.read_text())
    tab, rows = d["exclusion_table"], d["rows"]
    assert tab["n_events"] == len(rows)
    for k in ("T1_country_capacity_kbd", "T2_chokepoint_share", "T3_buffer_share", "SPARE_knowable"):
        t = tab[k]
        assert t["n_with_value"] + t["n_null"] == tab["n_events"], k
        assert sum(t["null_reasons"].values()) == t["n_null"], f"{k}: a null with no reason"


def test_S2_the_published_table_states_the_spare_gap_rather_than_the_registered_one():
    """§2 excludes events whose SPARE "predates 2003". The loader only has 2022-> because the STEO
    archive 403s. The document must report the hole that exists, not the one that was registered."""
    p = ROOT / "EXPOSURE.md"
    if not p.exists():
        pytest.skip("run python3 src/exposure.py first")
    md = p.read_text()
    assert "2022-01" in md and "2003" in md
    assert "403" in md or "refuses scripted access" in md


def test_the_location_set_is_ies90s_own_function_not_a_second_copy():
    """Two implementations of one definition is how a corpus ends up with two answers."""
    src = (ROOT / "src" / "exposure.py").read_text()
    assert "I.location_set(" in src
    sys.path.insert(0, str(ROOT / "src" / "state"))
    import ies90
    assert callable(ies90.location_set)
    L, lit = ies90.location_set({"country.iran"}, {"location": {"country.iraq"}}, {"chokepoint.hormuz"})
    assert "country.iraq" in L and "country.iran" in L and "country.uae" in L and lit
