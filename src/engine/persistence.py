"""
persistence.py -- WALK_FORWARD_PROTOCOL.md Amendment B (2026-09-02): G-persistence, the fourth G baseline.

For a read at as_of = t, the persistence forecast is a point mass on the IES level the event's primary
dyad had reached over the 90 days ending the day before t, W- = [t-90, t-1], computed by the SAME rules
and sources as the label (OUTCOME_MAPPING.md Amendments 1, 1.1, 2 -- session A's src/state/ies90.py,
called, never copied): ies90.score_event(t - 91 days, A, P, L, sources), since that function's window is
(d, d+90]. Only records dated <= t-1 enter. Smoothing: 0.9 on the level, 0.1 spread equally over its
adjacent levels (a boundary level has one neighbour). No covering source -> no level -> the walk falls
back to climatology for that read and counts it (n_persistence_fallback).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

LEVELS = ("0", "1", "2", "3")
PRE_DAYS = 90
STATE_DIR = Path(__file__).resolve().parents[1] / "state"


def _state_modules():
    """Session A's modules (read-only use). Imported lazily so synthetic tests never need them."""
    if str(STATE_DIR) not in sys.path:
        sys.path.insert(0, str(STATE_DIR))
    import ies90 as I          # noqa: E402
    import outcomes as O       # noqa: E402
    return I, O


def smooth(level: str) -> dict:
    """B.2: 0.9 on the level, 0.1 shared equally by its adjacent levels (one neighbour at 0 or 3)."""
    i = int(level)
    p = {l: 0.0 for l in LEVELS}
    p[level] = 0.9
    nb = [j for j in (i - 1, i + 1) if 0 <= j <= 3]
    for j in nb:
        p[str(j)] += 0.1 / len(nb)
    return p


def pre_window_level(as_of, A, pairs, L, src, score_event=None):
    """The IES level over W- = [as_of-90, as_of-1] (B.1). Returns level_pre as a string or None when no
    source covers W-, with the covering sources and the records that set the level."""
    if score_event is None:
        score_event = _state_modules()[0].score_event
    d = pd.Timestamp(as_of) - pd.Timedelta(days=PRE_DAYS + 1)          # score_event's window is (d, d+90] = [t-90, t-1]
    res = score_event(d, A, pairs, L, src)
    lv = res.get("level")
    return {"level_pre": (str(int(lv)) if lv is not None else None), "covering_pre": list(res.get("covering") or []),
            "basis_pre": res.get("basis"), "window_pre": [str((d + pd.Timedelta(days=1)).date()), str((d + pd.Timedelta(days=PRE_DAYS)).date())],
            "records_pre": [f"{x['source']}: {x['record']} {x['dates']} -> {x['level']}" for x in res.get("recs", []) if x.get("level") is not None]}


def precompute(conn, geo_types):
    """Per geopolitical corpus event: the persistence level at the event's own date (the walk reads at
    t = event_date). Actors, pairs and location set derived exactly as ies90.run does (A, P, L + littoral)."""
    I, O = _state_modules()
    src = I.load_sources()
    ev, ents, roles = O._corpus(conn)
    ents_all = defaultdict(set)
    for eid, en in conn.execute("SELECT event_id, entity_id FROM event_entities"):
        ents_all[eid].add(en)
    out = {}
    for r in ev.itertuples(index=False):
        if r.type not in geo_types:
            continue
        A, pairs = O._actors_and_pairs(r, ents, roles)
        rr = roles.get(r.event_id, {})
        L = (set(rr.get("location", set())) | set(rr.get("target", set()))) or set(A)
        for e in ents_all.get(r.event_id, set()):
            if e in I.LITTORAL:
                L |= set(I.LITTORAL[e])
        out[r.event_id] = pre_window_level(r.event_date, A, pairs, L, src, I.score_event)
    return out
