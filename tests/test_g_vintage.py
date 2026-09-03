"""Tests for src/g_vintage.py -- the STRUCTURAL vintage stamp (G-7 §§2-3).

The point of this module is that a value cannot be read without its publication date. These tests
are the enforcement; without them it is a convention an author in a hurry can drop.
"""
import ast
import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import g_vintage as V  # noqa: E402

S = dict(unit="million b/d", published="2011-03-02", reference_period="2009",
         source_id="EIA TIE #330", source_url="http://eia.gov/x", retrieved_at="2026-09-03",
         quote="15.5 million barrels per day (bbl/d)")


def mk(value=15.5, **kw):
    d = dict(S); d.update(kw)
    return V.stamp(value, **d)


# ------------------------------------------------------------------ §2 the schema is the guarantee

def test_G7_2_no_public_function_returns_a_value_without_a_required_date_argument():
    """§2, the whole point: 'if a capacity or flow value can be read without its publication date,
    the schema is wrong'. Any future convenience accessor fails here."""
    tree = ast.parse((ROOT / "src" / "g_vintage.py").read_text())
    VALUE_RETURNING = {"value_at", "latest_value"}
    seen = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in VALUE_RETURNING:
            seen.add(node.name)
            args = [a.arg for a in node.args.args]
            assert "t" in args, f"{node.name} does not take a date"
            # the date must be REQUIRED: no default may cover it
            n_defaults = len(node.args.defaults)
            required = args[:len(args) - n_defaults] if n_defaults else args
            assert "t" in required, f"{node.name}'s date argument has a default"
    assert seen == VALUE_RETURNING, f"a value-returning function was renamed or removed: {seen}"


def test_G7_2_there_is_no_bare_accessor_on_the_module():
    """No `.value` helper, no float() coercion, no default-t alias may be added."""
    src = (ROOT / "src" / "g_vintage.py").read_text()
    for bad in ("def value(", "def get_value(", "def __float__", "def unstamped", "t=None", "t=today"):
        assert bad not in src, f"g_vintage.py exposes {bad!r}, which would let a value be read undated"


def test_G7_2_a_register_entry_needs_its_verbatim_quote():
    with pytest.raises(ValueError):
        V.stamp(1.0, "mbd", "2011-03-02", "2009", "s", "u", "r", "")


def test_G7_2_published_is_validated_at_build_time_not_at_read_time():
    with pytest.raises(ValueError):
        V.stamp(1.0, "mbd", "not-a-date", "2009", "s", "u", "r", "q")


# ------------------------------------------------------------------ §2 reading

def test_G7_2_value_at_refuses_a_date_before_publication():
    s = mk()
    assert V.value_at(s, "2011-03-02") == 15.5          # the publication day itself is knowable
    assert V.value_at(s, "2020-01-01") == 15.5
    with pytest.raises(V.VintageError):
        V.value_at(s, "2011-03-01")


def test_G7_2_value_at_rejects_anything_that_is_not_a_stamped_entry():
    for bad in (15.5, None, {"value": 15.5}, "15.5"):
        with pytest.raises(TypeError):
            V.value_at(bad, "2020-01-01")


def test_G7_2_latest_takes_the_newest_entry_ON_OR_BEFORE_t_never_the_newest():
    reg = {"hormuz": [mk(15.5, published="2011-03-02"), mk(17.0, published="2014-12-01"),
                      mk(20.0, published="2025-06-16")]}
    assert V.latest(reg, "hormuz", "2013-01-01")["value"] == 15.5
    assert V.latest(reg, "hormuz", "2015-01-01")["value"] == 17.0
    assert V.latest(reg, "hormuz", "2030-01-01")["value"] == 20.0
    assert V.latest(reg, "hormuz", "2010-01-01") is None
    assert V.latest(reg, "absent", "2030-01-01") is None


def test_G7_4_a_registered_gap_is_never_a_zero():
    """§4: Cape of Good Hope is quantified by no release. None, not 0.0."""
    reg = {"cape": [mk(None, quote="the article does not provide a figure")]}
    s, v = V.latest_value(reg, "cape", "2020-01-01")
    assert s is not None and v is None
    assert v is not 0 and v != 0.0


def test_G7_2_register_summary_returns_provenance_and_deliberately_no_values():
    reg = {"hormuz": [mk(15.5)]}
    out = V.register_summary(reg)
    flat = str(out)
    assert "15.5" not in flat, "register_summary leaks a value, which would dodge the date requirement"
    assert out["hormuz"][0]["has_value"] is True and out["hormuz"][0]["published"] == "2011-03-02"


# ------------------------------------------------------------------ §3 the audit, F.1 standing

def _row(pub="2011-03-02", when="2012-01-01", value=15.5):
    return {"event_id": "e", "event_date": when, "chokepoint": "hormuz",
            "terms": {"flow": mk(value, published=pub)}, "zeroed_nulls": False}


def test_G7_3_audit_passes_a_clean_set():
    a = V.filtration_audit([_row(), _row(when="2015-01-01")])
    assert a["asserted"] is True and a["voided"] is False and a["violations"] == 0
    assert a["terms_checked"] == 2


def test_G7_3_a_single_post_dated_term_voids_the_study():
    """Amendment F.1's standing, and the proof the enforcement can fail: one injected violation."""
    rows = [_row(), _row(pub="2020-01-01", when="2012-01-01")]      # published 8 years after the event
    a = V.filtration_audit(rows)
    assert a["asserted"] is False and a["voided"] is True
    assert a["violations"] == 1
    assert "after the row's date" in a["first_violation"]["reason"]


def test_G7_3_audit_catches_an_unstamped_term():
    rows = [{"event_id": "e", "event_date": "2012-01-01", "terms": {"flow": 15.5}}]
    a = V.filtration_audit(rows)
    assert a["asserted"] is False and "not a stamped" in a["first_violation"]["reason"]


def test_G7_3_audit_catches_a_row_with_no_parseable_date():
    a = V.filtration_audit([{"event_id": "e", "event_date": "never", "terms": {}}])
    assert a["asserted"] is False and "no parseable date" in a["first_violation"]["reason"]


def test_G7_3_audit_catches_a_null_term_treated_as_zero():
    rows = [{"event_id": "e", "event_date": "2012-01-01",
             "terms": {"flow": mk(None, quote="gap")}, "zeroed_nulls": True}]
    a = V.filtration_audit(rows)
    assert a["asserted"] is False and "treated as zero" in a["first_violation"]["reason"]


def test_G7_3_the_audit_reads_raw_dates_and_not_the_functions_it_audits():
    """F.1's requirement: an independent code path. The audit must not call value_at/latest."""
    src = inspect.getsource(V.filtration_audit)
    for f in ("value_at(", "latest(", "latest_value("):
        assert f not in src, f"filtration_audit calls {f} -- it must audit by raw dates"
