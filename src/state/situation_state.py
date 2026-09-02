"""situation_state.py -- PATH Step 3: the state-at-event join and the stand-anywhere call.

    situation_state(event_id, entity_id, field, obs_date, value, value_text, vintage, release, retrospective, source)

For every corpus event: every panel field, for the entities the event names (world, opec, each coded
country entity, the actor/target dyad), as of `event_date` with vintage <= event_date -- read through
panel.value_at, so the vintage rule is the same code path everywhere (framework §4.3; tested in
tests/state/test_vintage_rule.py). Missing = no row; the coverage report counts it as unknown (WS-R3).
Datasets that list only positives get an explicit 0 inside their own coverage window (ZERO_IF_ABSENT:
ATOP lists only allied dyad-years, MID only dispute-years, ICB only crisis dyads) -- a documented rule,
not an imputation. Archigos spells are turned into tenure/change at t here.

`state_at(date, entities)` returns the same object for ANY date (the "stand anywhere" call).
Reads events / event_entities only; never writes to them.

Run:  python3 src/state/situation_state.py            join every corpus event, write coverage JSON
      python3 src/state/situation_state.py 2001-09-11 country.usa country.saudi_arabia   stand at a date
"""
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402
import archigos as AR  # noqa: E402

SCHEMA = """
CREATE TABLE IF NOT EXISTS situation_state (
    event_id      TEXT NOT NULL,
    entity_id     TEXT NOT NULL,
    field         TEXT NOT NULL,
    obs_date      TEXT,
    value         REAL,
    value_text    TEXT,
    vintage       TEXT NOT NULL,
    release       TEXT NOT NULL,
    retrospective INTEGER NOT NULL DEFAULT 0,
    source        TEXT NOT NULL,
    joined_at     TEXT NOT NULL,
    PRIMARY KEY (event_id, entity_id, field)
);
CREATE INDEX IF NOT EXISTS idx_situation_state_event ON situation_state(event_id);
"""
COVERAGE_OUT = P.DATA / "state" / "join_coverage.json"
# datasets that enumerate only positives: absent inside the window means 0, stated as such (source tag)
ZERO_IF_ABSENT = {
    "atop_defense_pact": ("dyad", "1815-01-01", "2018-12-31", "ATOP 5.1: no obligation listed (absent = none)"),
    "atop_any_obligation": ("dyad", "1815-01-01", "2018-12-31", "ATOP 5.1: no obligation listed (absent = none)"),
    "mid_count_10y": ("dyad", "1816-01-01", "2015-12-31", "COW dyadic MID 4.03: no dispute listed (absent = none)"),
    "icb_crisis_count": ("dyad", "1918-01-01", "2021-12-31", "ICB v16: no crisis listed for the dyad (absent = none)"),
}
ENTITY_FIELDS = {"world": None, "opec": None}      # filled from the panel: which fields exist per entity kind


def ensure_schema(conn):
    conn.executescript(SCHEMA)
    conn.commit()


# ----------------------------------------------------------------------------- entities per event

def event_entities(conn, event_id):
    """world, opec, every coded country entity of the event (any role), and the actor-target dyad when both are countries."""
    ents = {"world", "opec"}
    roles = defaultdict(set)
    for eid, role in conn.execute("SELECT entity_id, role FROM event_entities WHERE event_id=?", (event_id,)):
        if eid.startswith("country."):
            ents.add(eid); roles[role or "mention"].add(eid)
    row = conn.execute("SELECT sr_actor, sr_target FROM events WHERE event_id=?", (event_id,)).fetchone()
    actor, target = (row or (None, None))
    for e in (actor, target):
        if e and e.startswith("country.") and e != "unknown":
            ents.add(e)
    pairs = set()
    if actor and target and actor.startswith("country.") and target.startswith("country.") and actor != target:
        pairs.add(C.dyad_id(actor, target))
    for a in roles.get("actor", set()):
        for t in roles.get("target", set()) | roles.get("location", set()):
            if a != t:
                pairs.add(C.dyad_id(a, t))
    return sorted(ents), sorted(pairs)


def fields_by_kind(conn):
    """Which panel fields exist for which entity kind (world / opec / region / country / dyad)."""
    out = defaultdict(set)
    for ent, field in conn.execute("SELECT DISTINCT entity_id, field FROM state_panel"):
        kind = ent.split(".", 1)[0] if "." in ent else ent
        out[kind].add(field)
    return out


# ----------------------------------------------------------------------------- the state at a date

def state_at(conn, t, entities=(), dyads=()):
    """{entity: {field: value_at(...)}} for world, opec, the given countries and dyads, at date t."""
    fbk = fields_by_kind(conn)
    out = {}
    targets = [("world", "world"), ("opec", "opec")] + [(e, "country") for e in entities] + [(d, "dyad") for d in dyads]
    for ent, kind in targets:
        got = {}
        for field in sorted(fbk.get(kind, ())):
            if field == "leader_tenure_days":
                ten = AR.tenure_at(conn, ent, t)
                if ten:
                    got["leader_tenure_days"] = {"obs_date": ten["since"], "value": float(ten["tenure_days"]), "value_text": ten["leader"],
                                                 "vintage": ten["since"], "release": None, "retrospective": False, "source": ten["source"], "unit": "days"}
                    got["leader_change_last_365d"] = {"obs_date": ten["since"], "value": float(ten["change_last_365d"]), "value_text": None,
                                                      "vintage": ten["since"], "release": None, "retrospective": False, "source": ten["source"], "unit": "0/1"}
                continue
            v = P.value_at(conn, ent, field, t)
            if v is not None:
                got[field] = v
        for field, (k, lo, hi, tag) in ZERO_IF_ABSENT.items():
            if kind == k and field not in got and lo <= str(t)[:10] <= hi and field in fbk.get(kind, ()):
                got[field] = {"obs_date": str(t)[:10], "value": 0.0, "value_text": None, "vintage": str(t)[:10], "release": None,
                              "retrospective": False, "source": tag, "unit": None}
        if got:
            out[ent] = got
    return out


# ----------------------------------------------------------------------------- the join

def join(conn, event_ids=None, replace=True):
    ensure_schema(conn)
    q = "SELECT event_id, event_date FROM events"
    events = conn.execute(q).fetchall() if not event_ids else [r for r in conn.execute(q).fetchall() if r[0] in set(event_ids)]
    ts = P.now()
    rows = []
    for eid, edate in events:
        ents, dyads = event_entities(conn, eid)
        st = state_at(conn, edate, [e for e in ents if e.startswith("country.")], dyads)
        for ent, fields in st.items():
            for f, v in fields.items():
                rows.append((eid, ent, f, v.get("obs_date"), v.get("value"), v.get("value_text"), v["vintage"],
                             v.get("release") or v["vintage"], 1 if v.get("retrospective") else 0, v["source"], ts))
    if replace:
        conn.execute("DELETE FROM situation_state" + ("" if not event_ids else f" WHERE event_id IN ({','.join('?' * len(event_ids))})"),
                     () if not event_ids else tuple(event_ids))
    conn.executemany("INSERT OR REPLACE INTO situation_state VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    return len(events), len(rows)


# ----------------------------------------------------------------------------- coverage (published as computed)

def coverage(conn):
    cb = P.codebook()
    ev = pd.read_sql("SELECT event_id, event_date, type FROM events", conn)
    ss = pd.read_sql("SELECT event_id, entity_id, field, retrospective FROM situation_state", conn)
    ev["era"] = ev["event_date"].map(lambda d: "1946-86" if d < "1987-01-01" else "1987->")
    ss["block"] = ss["field"].map(lambda f: cb.get(f, {}).get("block", "?"))
    per_event = ss.groupby("event_id").agg(n_fields=("field", "size"), n_distinct=("field", "nunique"),
                                           n_nonretro=("retrospective", lambda s: int((s == 0).sum()))).reindex(ev["event_id"]).fillna(0)
    ev = ev.join(per_event, on="event_id")
    out = {"generated_at": P.now(), "n_events": int(len(ev)), "events_with_a_row": int((ev["n_fields"] > 0).sum()),
           "fields_registered": len(cb), "eras": {}}
    for era, g in ev.groupby("era"):
        blocks = {}
        sub = ss[ss["event_id"].isin(g["event_id"])]
        for b in ("PHYSICAL", "MARKET", "ACTORS", "DYADS", "SYSTEM", "NARRATIVE"):
            bb = sub[sub["block"] == b]
            blocks[b] = {"events_with_field": int(bb["event_id"].nunique()), "share_of_events": round(bb["event_id"].nunique() / max(len(g), 1), 3),
                         "fields_seen": sorted(bb["field"].unique().tolist()), "rows": int(len(bb))}
        out["eras"][era] = {"n_events": int(len(g)), "median_fields_per_event": float(g["n_fields"].median()),
                            "median_distinct_fields": float(g["n_distinct"].median()), "min_fields": int(g["n_fields"].min()),
                            "events_ge_25_fields": int((g["n_distinct"] >= 25).sum()), "events_ge_12_fields": int((g["n_distinct"] >= 12).sum()),
                            "blocks": blocks}
    out["acceptance_S2"] = {"rule": "every event >= 25 non-unknown fields for 1987+ and >= 12 for 1946-86 (framework §7)",
                            "1987->": f"{out['eras'].get('1987->', {}).get('events_ge_25_fields', 0)} of {out['eras'].get('1987->', {}).get('n_events', 0)}",
                            "1946-86": f"{out['eras'].get('1946-86', {}).get('events_ge_12_fields', 0)} of {out['eras'].get('1946-86', {}).get('n_events', 0)}"}
    return out


def main():
    conn = sqlite3.connect(P.DB)
    try:
        P.ensure_schema(conn); ensure_schema(conn)
        if len(sys.argv) > 1 and sys.argv[1][:4].isdigit():
            t = sys.argv[1]; ents = [a for a in sys.argv[2:] if a.startswith("country.")]
            dy = [C.dyad_id(a, b) for i, a in enumerate(ents) for b in ents[i + 1:]]
            print(json.dumps(state_at(conn, t, ents, dy), indent=1, default=str)[:6000]); return
        n_ev, n_rows = join(conn)
        cov = coverage(conn)
    finally:
        conn.close()
    COVERAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    COVERAGE_OUT.write_text(json.dumps(cov, indent=1, default=str))
    print(f"situation_state: {n_ev} events joined, {n_rows} rows; events with a row {cov['events_with_a_row']} of {cov['n_events']}")
    for era, e in cov["eras"].items():
        print(f"  {era}: n={e['n_events']} median fields/event {e['median_fields_per_event']} (distinct {e['median_distinct_fields']}), min {e['min_fields']}, "
              f">=25: {e['events_ge_25_fields']}, >=12: {e['events_ge_12_fields']}")
        for b, v in e["blocks"].items():
            print(f"     {b:10s} events with a field {v['events_with_field']:>4d} ({v['share_of_events']:.0%})  rows {v['rows']:>6d}  fields {len(v['fields_seen'])}")
    print("  acceptance S2:", cov["acceptance_S2"])


if __name__ == "__main__":
    main()
