"""exposure.py -- PHYSICAL_EXPOSURE_REGISTRATION.md §2: the three-tier physical exposure builder.

For each corpus event at date t, a physically-denominated exposure read from registers published
strictly before t. Nothing is coded per event by a human, so the severity-ordinal failure cannot
recur through this variable (§2).

  T1  X1 = sum over the event's coded countries of CAP(c, vintage(t))          kb/d, and share of world
  T2  X2 = FLOW(k, vintage(t)) / WORLD_SEABORNE(vintage(t))                    dimensionless
  T3  X3 = X1 / SPARE(t)                                                       dimensionless -- THE PRIMARY REGRESSOR

THE ONE RULE THIS MODULE EXISTS TO ENFORCE: **a missing term is null, never zero.**

    This project has already been bitten once by the other choice. `ies90.score_event` used
    `max(..., default=0)`, so an event whose sources recorded something they could not date inside
    the window fell through to "level 0 -- none", and 18 events -- including the Abqaiq attack and
    the Soleimani strike -- were published as "no escalation" when the truth was "no answer".
    OUTCOME_MAPPING Amendment 4 fixed it by making the two states distinct.

    Every arithmetic path here is built so that failure cannot happen:
      * `_sum` returns null if ANY part is null. It never sums the parts it has and calls that a total.
      * there is no `or 0`, no `default=0`, no `sum()` over a possibly-empty set anywhere in this file;
        `tests/test_exposure.py` greps for them and fails.
      * every null carries a REASON from `NullReason` and lands in the exclusion table with a count.
      * `Val.value is None` if and only if `Val.reason is not None`, asserted on construction.
    A partial sum is still computed where some countries are known -- as `x1_partial_kbd`, a named
    diagnostic that is never X1 and never enters a regression. Same device as `level_location`.

VINTAGE (§3). A register's knowable_at is its PUBLICATION date, not its reference year. Every value
carries the publication date it came from, and `test_exposure.py` asserts no value derives from a
register published on or after its event date.

REGISTERS. Two are other sessions' and are not in the tree yet; this module reads them if present and
returns counted nulls if not, so the builder runs today and starts producing the moment they land:
  * `data/registers/capacity.csv`     -- session C. Proposed columns:
        country,measure,value_kbd,reference_year,published_at,source_url
        measure in {crude_production_capacity, refining_capacity}; country = a `country.*` entity id.
  * `data/registers/chokepoints.csv`  -- session G. Proposed columns:
        chokepoint,flow_mbd,world_seaborne_mbd,published_at,source_url
        chokepoint = a `chokepoint.*` entity id.
The schemas are proposals, not registrations: PHYSICAL_EXPOSURE_REGISTRATION §2 fixes the QUANTITIES,
not the file layout. If C or G publish a different shape, change the two readers here and nothing else.

SPARE. `spare_capacity_opec` (state_panel, entity `opec`, EIA STEO Table 3d), last value whose
`vintage` (knowable date) is <= t.

Run:  python3 src/exposure.py            build + write data/exposure/exposure.json and EXPOSURE.md
      python3 src/exposure.py --table    print the exclusion table only
"""
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "state"))
import ies90 as I  # noqa: E402  -- for LITTORAL and location_set, so L is defined once

REGISTRATION = "PHYSICAL_EXPOSURE_REGISTRATION.md (2026-09-03, commit 66b1c30)"
DB = ROOT / "data" / "oil.db"
OUT_DIR = ROOT / "data" / "exposure"
OUT_JSON = OUT_DIR / "exposure.json"
OUT_MD = ROOT / "EXPOSURE.md"
CAP_REGISTER = ROOT / "data" / "registers" / "capacity.csv"        # session C -- absent today
CHOKE_REGISTER = ROOT / "data" / "registers" / "chokepoints.csv"   # session G -- absent today
SPARE_FIELD, SPARE_ENTITY = "spare_capacity_opec", "opec"


class NullReason:
    """Why a tier is null. Every one lands in the exclusion table with a count, so 'missing' is
    always a stated quantity and never an absence a reader has to notice."""
    NO_COUNTRY_CODING = "no country coded on the event"
    NO_CAP_REGISTER = "capacity register not published yet (session C)"
    COUNTRY_NOT_IN_REGISTER = "a coded country has no capacity register published before t"
    NO_CHOKEPOINT_CODING = "no chokepoint coded on the event"
    NO_CHOKE_REGISTER = "chokepoint register not published yet (session G)"
    CHOKEPOINT_NOT_IN_REGISTER = "a coded chokepoint has no register published before t"
    NO_WORLD_SEABORNE = "no world seaborne total published before t"
    SPARE_NOT_PUBLISHED = "no spare_capacity_opec value knowable at t"
    X1_NULL = "X1 is null, so X1/SPARE is undefined"


class Val:
    """A value that knows why it is missing. value is None IF AND ONLY IF reason is not None --
    asserted here, so no path can produce a silent zero or a reasonless null."""

    __slots__ = ("value", "reason", "detail", "published_at")

    def __init__(self, value=None, reason=None, detail=None, published_at=None):
        assert (value is None) != (reason is None), \
            f"a Val must be either a number with no reason or None with a reason (got {value!r}, {reason!r})"
        self.value, self.reason, self.detail, self.published_at = value, reason, detail, published_at

    @property
    def ok(self):
        return self.value is not None

    def as_dict(self):
        return {"value": self.value, "reason": self.reason, "detail": self.detail,
                "published_at": self.published_at}

    def __repr__(self):
        return f"Val({self.value!r}, {self.reason!r})"


def _sum(parts):
    """Sum of Vals, null if ANY part is null. This is the whole point of the module: a total over a
    set with an unknown member is unknown, not the total of the members that happen to be known."""
    missing = [p for p in parts if not p.ok]
    if missing:
        return None, missing
    return sum(p.value for p in parts), []


# ------------------------------------------------------------------ registers

def read_capacity_register(path=CAP_REGISTER):
    """{country: [rows sorted by published_at]}. Absent file -> {} (and every X1 is a counted null)."""
    import csv
    if not Path(path).exists():
        return None
    out = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["country"]].append({"measure": r.get("measure") or "crude_production_capacity",
                                      "value_kbd": float(r["value_kbd"]),
                                      "reference_year": r.get("reference_year"),
                                      "published_at": r["published_at"][:10],
                                      "source_url": r.get("source_url")})
    for c in out:
        out[c].sort(key=lambda x: x["published_at"])
    return dict(out)


def read_chokepoint_register(path=CHOKE_REGISTER):
    import csv
    if not Path(path).exists():
        return None
    out = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["chokepoint"]].append({"flow_mbd": float(r["flow_mbd"]),
                                         "world_seaborne_mbd": (float(r["world_seaborne_mbd"])
                                                                if r.get("world_seaborne_mbd") else None),
                                         "published_at": r["published_at"][:10],
                                         "source_url": r.get("source_url")})
    for k in out:
        out[k].sort(key=lambda x: x["published_at"])
    return dict(out)


def latest_before(rows, t, measure=None):
    """§3: the most recent register row PUBLISHED STRICTLY BEFORE t. Not the most recent reference
    year -- the 2019 review published mid-2020 may not inform a 2019 forecast."""
    cand = [r for r in (rows or [])
            if r["published_at"] < t and (measure is None or r.get("measure") == measure)]
    return cand[-1] if cand else None


def load_spare(conn):
    """[(vintage, obs_date, value_mbd)] sorted by vintage -- the knowable date, not the reference month."""
    return conn.execute(
        "SELECT vintage, obs_date, value FROM state_panel WHERE field=? AND entity_id=? "
        "AND value IS NOT NULL ORDER BY vintage", (SPARE_FIELD, SPARE_ENTITY)).fetchall()


def spare_at(spare_rows, t):
    """SPARE(t) in kb/d, from the last STEO value knowable at t. Null (never 0, never the earliest
    value) when nothing is knowable yet -- which is every event before 2022-03 in this tree, because
    the STEO archive refuses scripted access and the loader only has the current workbook."""
    cand = [r for r in spare_rows if r[0][:10] < t]
    if not cand:
        return Val(reason=NullReason.SPARE_NOT_PUBLISHED,
                   detail=(f"earliest knowable spare_capacity_opec is {spare_rows[0][0][:10]}"
                           if spare_rows else "no spare_capacity_opec rows at all"))
    vintage, obs_date, mbd = cand[-1]
    return Val(value=float(mbd) * 1000.0, detail=f"STEO month {obs_date[:10]}, {mbd} mb/d",
               published_at=vintage[:10])


# ------------------------------------------------------------------ the three tiers

def x1_country_capacity(countries, t, cap, measure="crude_production_capacity"):
    """T1. Null if the event codes no country, if C's register is absent, or if ANY coded country
    lacks a register published before t. The partial sum over the countries that DO have one is
    returned beside it as a diagnostic and is never X1."""
    if not countries:
        return Val(reason=NullReason.NO_COUNTRY_CODING), None, []
    if cap is None:
        return Val(reason=NullReason.NO_CAP_REGISTER,
                   detail=f"expected at {CAP_REGISTER.relative_to(ROOT)}"), None, sorted(countries)
    parts, missing, pubs = [], [], []
    for c in sorted(countries):
        row = latest_before(cap.get(c), t, measure)
        if row is None:
            missing.append(c)
            parts.append(Val(reason=NullReason.COUNTRY_NOT_IN_REGISTER, detail=c))
        else:
            parts.append(Val(value=row["value_kbd"], detail=c, published_at=row["published_at"]))
            pubs.append(row["published_at"])
    total, miss = _sum(parts)
    partial = sum(p.value for p in parts if p.ok) if any(p.ok for p in parts) else None
    if total is None:
        return (Val(reason=NullReason.COUNTRY_NOT_IN_REGISTER,
                    detail=f"no register before {t} for: {', '.join(missing)}"), partial, missing)
    return Val(value=total, detail=f"{len(parts)} countries", published_at=max(pubs)), partial, []


def x2_chokepoint_share(chokepoints, t, ck):
    """T2. FLOW(k)/WORLD_SEABORNE, max over the event's chokepoints (a share, so not additive)."""
    if not chokepoints:
        return Val(reason=NullReason.NO_CHOKEPOINT_CODING)
    if ck is None:
        return Val(reason=NullReason.NO_CHOKE_REGISTER,
                   detail=f"expected at {CHOKE_REGISTER.relative_to(ROOT)}")
    best, missing = None, []
    for k in sorted(chokepoints):
        row = latest_before(ck.get(k), t)
        if row is None:
            missing.append(k)
            continue
        if row["world_seaborne_mbd"] in (None, 0):
            return Val(reason=NullReason.NO_WORLD_SEABORNE, detail=f"{k} @ {row['published_at']}")
        share = row["flow_mbd"] / row["world_seaborne_mbd"]
        if best is None or share > best[0]:
            best = (share, k, row["published_at"])
    if best is None:
        return Val(reason=NullReason.CHOKEPOINT_NOT_IN_REGISTER,
                   detail=f"no register before {t} for: {', '.join(missing)}")
    return Val(value=best[0], detail=f"max over {len(chokepoints)} chokepoint(s): {best[1]}",
               published_at=best[2])


def x3_buffer_share(x1, spare):
    """T3, the primary regressor: the share of the world's spare capacity this disruption would
    consume. Null if either side is null -- and BOTH reasons are kept, because 'we do not know the
    capacity' and 'we do not know the buffer' are different holes in the study."""
    if not x1.ok:
        return Val(reason=NullReason.X1_NULL, detail=x1.reason)
    if not spare.ok:
        return Val(reason=NullReason.SPARE_NOT_PUBLISHED, detail=spare.detail)
    if spare.value == 0:
        return Val(reason=NullReason.SPARE_NOT_PUBLISHED, detail="spare capacity is zero; X1/0 undefined")
    # the later of the two publication dates is when X3 became knowable; `max` over a possibly-empty
    # iterable is exactly the family of bug this module guards against, so the empty case is explicit
    pubs = [d for d in (x1.published_at, spare.published_at) if d]
    return Val(value=x1.value / spare.value,
               detail=f"X1 {x1.value:.0f} kb/d / SPARE {spare.value:.0f} kb/d",
               published_at=max(pubs) if pubs else None)


# ------------------------------------------------------------------ the build

def build(conn, cap=None, ck=None):
    """One row per corpus event. Reads; writes nothing to any table."""
    cap = read_capacity_register() if cap is None else cap
    ck = read_chokepoint_register() if ck is None else ck
    spare_rows = load_spare(conn)

    roles, ents_all = defaultdict(lambda: defaultdict(set)), defaultdict(set)
    for eid, ent, role in conn.execute("SELECT event_id, entity_id, role FROM event_entities"):
        ents_all[eid].add(ent)
        if ent.startswith("country."):
            roles[eid][role or "actor"].add(ent)

    rows = []
    for eid, date, typ in conn.execute("SELECT event_id, event_date, type FROM events ORDER BY event_date"):
        t = str(date)[:10]
        A = {e for e in ents_all[eid] if e.startswith("country.")}
        L, lit = I.location_set(A, roles[eid], ents_all[eid])
        chokes = {e for e in ents_all[eid] if e.startswith("chokepoint.")}
        x1, partial, missing = x1_country_capacity(L, t, cap)
        x2 = x2_chokepoint_share(chokes, t, ck)
        sp = spare_at(spare_rows, t)
        x3 = x3_buffer_share(x1, sp)
        rows.append({"event_id": eid, "date": t, "class": typ,
                     "countries_L": sorted(L), "chokepoints": sorted(chokes),
                     "littoral_from": sorted(lit),
                     "X1_kbd": x1.as_dict(), "X2_share": x2.as_dict(),
                     "X3_buffer_share": x3.as_dict(), "SPARE_kbd": sp.as_dict(),
                     "x1_partial_kbd": partial,
                     "x1_partial_note": ("DIAGNOSTIC ONLY -- the sum over the countries that DO have a "
                                         "register. It is NOT X1 and never enters a regression."),
                     "x1_missing_countries": missing})
    return rows


def exclusion_table(rows):
    """§2's registered fallbacks, as counts. How many events get each tier, and why the rest do not."""
    def tier(key):
        got = [r for r in rows if r[key]["value"] is not None]
        why = Counter(r[key]["reason"] for r in rows if r[key]["value"] is None)
        return {"n_with_value": len(got), "n_null": len(rows) - len(got),
                "null_reasons": dict(sorted(why.items(), key=lambda kv: -kv[1]))}
    out = {"registration": REGISTRATION, "n_events": len(rows),
           "T1_country_capacity_kbd": tier("X1_kbd"),
           "T2_chokepoint_share": tier("X2_share"),
           "T3_buffer_share": tier("X3_buffer_share"),
           "SPARE_knowable": tier("SPARE_kbd")}
    # The ceiling: what T3 could reach once session C's register lands, assuming it covers every
    # coded country. Stated because "T3 = 0 today" invites the reading that it will be ~313 later.
    ceil = [r for r in rows if r["countries_L"] and r["SPARE_kbd"]["value"] is not None]
    out["T3_ceiling_if_capacity_register_covers_every_coded_country"] = {
        "n": len(ceil),
        "of": len(rows),
        "blocked_by_no_country_coding": sum(1 for r in rows if not r["countries_L"]
                                            and r["SPARE_kbd"]["value"] is not None),
        "blocked_by_spare": sum(1 for r in rows if r["SPARE_kbd"]["value"] is None),
        "distinct_countries_the_register_must_cover": len({c for r in ceil for c in r["countries_L"]}),
        "note": ("an upper bound, not a forecast: X1 is null unless EVERY coded country on the event "
                 "has a register published before t, so the realised n is this or lower")}
    out["by_class"] = {c: {"n": sum(1 for r in rows if r["class"] == c),
                           "T3": sum(1 for r in rows if r["class"] == c and r["X3_buffer_share"]["value"] is not None)}
                       for c in sorted({r["class"] for r in rows})}
    out["by_decade"] = {d: {"n": sum(1 for r in rows if r["date"][:3] + "0s" == d),
                            "SPARE_knowable": sum(1 for r in rows if r["date"][:3] + "0s" == d
                                                  and r["SPARE_kbd"]["value"] is not None)}
                        for d in sorted({r["date"][:3] + "0s" for r in rows})}
    return out


def write_md(rows, tab):
    """EXPOSURE.md -- the exclusion table, published as §2's registered fallbacks require."""
    L = ["# PHYSICAL EXPOSURE — the three tiers, and what is missing from each", "",
         f"*Generated by `src/exposure.py` under {REGISTRATION}. Reads the corpus and the registers; "
         f"writes no table. Every figure below is a count of events, not an estimate.*", "",
         "> **A missing term is null, never zero.** `X1` is null when any coded country has no capacity",
         "> register published before the event date — not the sum of the ones that do. `X3` is null",
         "> when either side is. Every null carries a reason and is counted here. This is the same rule",
         "> OUTCOME_MAPPING Amendment 4 had to impose on the escalation target after `max(default=0)`",
         "> published 18 events as \"no escalation\" when the truth was \"no answer\".", "",
         f"**Corpus: {tab['n_events']} events.**", "",
         "| tier | events with a value | null | why null |", "|---|---:|---:|---|"]
    for key, name in (("T1_country_capacity_kbd", "**T1** country capacity (kb/d)"),
                      ("T2_chokepoint_share", "**T2** chokepoint share"),
                      ("T3_buffer_share", "**T3** buffer share — *the primary regressor*"),
                      ("SPARE_knowable", "SPARE(t) alone (input to T3)")):
        d = tab[key]
        why = "; ".join(f"{r} × {n}" for r, n in d["null_reasons"].items()) or "—"
        L.append(f"| {name} | {d['n_with_value']} | {d['n_null']} | {why} |")
    L += ["", "## SPARE(t) — the binding constraint on T3 today", "",
          "`spare_capacity_opec` is registered in `WORLD_STATE_CODEBOOK.md` as *2003→*, and "
          "PHYSICAL_EXPOSURE §2 excludes only events whose `SPARE(t)` *\"predates 2003\"*. **In this "
          "tree it is loaded from 2022-01 only** — `src/state/eia_steo.py` says why in its own "
          "docstring: the STEO archive refuses scripted access (403), so coverage starts where the "
          "current workbook starts. The registered exclusion rule and the actual hole are therefore "
          "different sizes, and the table above reports the actual one.", "",
          "| decade | events | SPARE knowable at t |", "|---|---:|---:|"]
    for d, v in tab["by_decade"].items():
        L.append(f"| {d} | {v['n']} | {v['SPARE_knowable']} |")
    c3 = tab["T3_ceiling_if_capacity_register_covers_every_coded_country"]
    L += ["", "## The ceiling on T3", "",
          f"T3 is 0 today because session C's register is absent, not because the events are unusable. "
          f"**At most {c3['n']} of {c3['of']} events can ever carry T3** — those with at least one coded "
          f"country *and* a knowable SPARE(t). Of the rest, {c3['blocked_by_spare']} are blocked by SPARE "
          f"alone and {c3['blocked_by_no_country_coding']} code no country at all. The register would need "
          f"to cover **{c3['distinct_countries_the_register_must_cover']} distinct countries** to reach that "
          f"ceiling, and X1 is null unless *every* coded country on an event is covered — so the realised n "
          f"is this or lower, never higher.", ""]
    L += ["", "## T3 by class", "", "| class | events | T3 available |", "|---|---:|---:|"]
    for c, v in tab["by_class"].items():
        L.append(f"| `{c}` | {v['n']} | {v['T3']} |")
    L += ["", "## What is not built yet, and what it is waiting on", "",
          f"- **T1** needs session C's capacity register at `{CAP_REGISTER.relative_to(ROOT)}`. The reader, "
          "the vintage rule and the null semantics are built and tested against a fixture; the moment the "
          "file lands, T1 and T3 populate with no further change here.",
          f"- **T2** needs session G's chokepoint register at `{CHOKE_REGISTER.relative_to(ROOT)}`. Same.",
          "- The column schemas in `src/exposure.py`'s docstring are **proposals**: §2 registers the "
          "quantities, not the file layout. If C or G publish a different shape, only the two readers change.",
          ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        rows = build(conn)
    finally:
        conn.close()
    tab = exclusion_table(rows)
    if "--table" in sys.argv:
        print(json.dumps(tab, indent=1))
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"registration": REGISTRATION, "exclusion_table": tab, "rows": rows},
                                   indent=1), encoding="utf-8")
    write_md(rows, tab)
    print(f"exposure: {tab['n_events']} events")
    for k in ("T1_country_capacity_kbd", "T2_chokepoint_share", "T3_buffer_share", "SPARE_knowable"):
        d = tab[k]
        print(f"  {k:<28} value {d['n_with_value']:>4}   null {d['n_null']:>4}   {d['null_reasons']}")
    print(f"  -> {OUT_JSON.relative_to(ROOT)} + {OUT_MD.name}")


if __name__ == "__main__":
    main()
