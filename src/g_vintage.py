"""g_vintage.py -- the STRUCTURAL vintage stamp for PHYSICAL_EXPOSURE (§3), Session G.

Registered first, in docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md (2026-09-03) §§2-3.

THE POINT, and it is a schema decision rather than a convention:

    A register entry is an OBJECT, never a number, and the only way to obtain the number is a
    function that takes the date you are claiming to be at. There is no `.value` accessor, no
    `float(stamped)`, and no default `t` anywhere in this module. If a capacity or flow value can
    be read without its publication date, the schema is wrong -- Joe, 2026-09-03.

G-3 is why. A strict vintage rule emptied 726 of 786 situation values at t, and the reason nobody
noticed until it was measured is that the date was DOCUMENTARY -- carried beside the value, and
therefore droppable by anyone in a hurry. Here it is load-bearing: drop it and the code will not run.

`published` is the RELEASE'S PUBLICATION DATE, never its reference year. That is §3's trap: the 2019
EI Statistical Review, published mid-2020, may not inform a 2019 forecast. WORLD_STATE_CODEBOOK.md
Amendment 1 governs.

This module holds no data. It is imported by the register modules and by anything else in the study
that needs a point-in-time value.
"""
from __future__ import annotations

import datetime as dt
import json
from typing import Any

REQUIRED = ("value", "unit", "published", "reference_period", "source_id", "source_url",
            "retrieved_at", "quote")


class VintageError(ValueError):
    """Raised when a value is read at a date before the register that carries it was published."""


def _d(x) -> dt.date:
    if isinstance(x, dt.date):
        return x
    return dt.date.fromisoformat(str(x)[:10])


def stamp(value, unit, published, reference_period, source_id, source_url, retrieved_at, quote):
    """§2. Build a register entry. Every field is required; a value with no verbatim quote may not
    enter the register (§4). `value` may be None -- a gap is a measurement, never a zero."""
    if value is not None and not isinstance(value, (int, float)):
        raise TypeError("value must be a number or None (a gap), not %r" % type(value).__name__)
    if not quote or not str(quote).strip():
        raise ValueError("a register entry needs the verbatim quote its number was read from (§4)")
    _d(published)                                        # raises now rather than at read time
    return {"value": (None if value is None else float(value)), "unit": unit,
            "published": _d(published).isoformat(), "reference_period": str(reference_period),
            "source_id": str(source_id), "source_url": str(source_url),
            "retrieved_at": str(retrieved_at), "quote": str(quote)}


def is_stamped(obj: Any) -> bool:
    return isinstance(obj, dict) and all(k in obj for k in REQUIRED)


def value_at(stamped: dict, t):
    """§2. THE number -- and the only way to get it. Raises VintageError if the register that
    carries it was published after `t`. There is no version of this function without `t`."""
    if not is_stamped(stamped):
        raise TypeError("not a stamped register entry: %r" % (sorted(stamped) if isinstance(stamped, dict) else type(stamped),))
    if _d(stamped["published"]) > _d(t):
        raise VintageError(
            "%s was published %s, which is after %s -- it was not knowable at that date"
            % (stamped["source_id"], stamped["published"], _d(t).isoformat()))
    return stamped["value"]


def latest(register: dict, key: str, t):
    """§2. The stamped entry for `key` with the greatest `published <= t`, or None. NEVER the newest
    entry, and never one published after `t`. Entries whose value is None (a registered gap) are
    still candidates: a release that covered a chokepoint and gave no figure is information."""
    td = _d(t)
    cands = [e for e in register.get(key, ()) if _d(e["published"]) <= td]
    if not cands:
        return None
    return max(cands, key=lambda e: _d(e["published"]))


def latest_value(register: dict, key: str, t):
    """(stamped, value) for `key` at `t`, or (None, None). Still takes `t`; still cannot be called
    without one. Kept separate from `latest` so a caller that wants only provenance need not read
    the number at all."""
    s = latest(register, key, t)
    return (None, None) if s is None else (s, value_at(s, t))


# ----------------------------------------------------------------------------- §3 the audit

def filtration_audit(rows, date_key="event_date", terms_key="terms"):
    """§3, in WALK_FORWARD_PROTOCOL Amendment F.1's standing. Runs over EVERY emitted row on an
    independent path -- raw dates only, never the functions above -- and asserts:

      1. every stamped term the row rests on has published <= the row's date;
      2. no term has an absent or unparseable `published`;
      3. no term with value None was treated as 0.

    A SINGLE violation sets `asserted` false and voids the study. Counts and the first violation are
    published either way."""
    checked = viol = 0
    first = None
    reasons = {}
    for r in rows:
        try:
            when = _d(r[date_key])
        except (KeyError, ValueError, TypeError):
            viol += 1
            reasons["row has no parseable date"] = reasons.get("row has no parseable date", 0) + 1
            first = first or {"row": _brief(r), "reason": "row has no parseable date"}
            continue
        for name, term in (r.get(terms_key) or {}).items():
            if term is None:
                continue
            checked += 1
            why = None
            if not is_stamped(term):
                why = "term is not a stamped register entry"
            else:
                try:
                    p = _d(term["published"])
                except (ValueError, TypeError):
                    why = "term has an unparseable published date"
                else:
                    if p > when:
                        why = ("term published %s, after the row's date %s" % (p.isoformat(), when.isoformat()))
                    elif term["value"] is None and r.get("zeroed_nulls"):
                        why = "a null term was treated as zero"
            if why:
                viol += 1
                reasons[why.split(",")[0]] = reasons.get(why.split(",")[0], 0) + 1
                first = first or {"row": _brief(r), "term": name, "reason": why}
    return {"rule": ("G7 §3, in WALK_FORWARD_PROTOCOL Amendment F.1's standing: a single violation "
                     "voids the study."),
            "terms_checked": checked, "rows": len(rows), "violations": viol,
            "violation_reasons": reasons, "first_violation": first,
            "asserted": viol == 0,
            "voided": viol > 0}


def _brief(r):
    return {k: r.get(k) for k in ("event_id", "event_date", "chokepoint") if k in r}


def register_summary(register: dict):
    """Provenance only -- deliberately returns no values, so a caller cannot use it to dodge `t`."""
    out = {}
    for key, entries in sorted(register.items()):
        out[key] = [{"published": e["published"], "reference_period": e["reference_period"],
                     "source_id": e["source_id"], "has_value": e["value"] is not None}
                    for e in sorted(entries, key=lambda x: x["published"])]
    return out


def dumps(obj):
    return json.dumps(obj, indent=1, default=str)
