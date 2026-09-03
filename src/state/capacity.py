"""
capacity.py -- T1 of PHYSICAL_EXPOSURE_REGISTRATION.md: the country capacity register.

T1 needs, per country, CRUDE PRODUCTION CAPACITY and REFINING CAPACITY, each row carrying the
PUBLICATION DATE of the register it came from -- not its reference year (section 3: the 2019 EI
Review published mid-2020 may not inform a 2019 forecast, and a filtration test asserts it).

THIS MODULE CURRENTLY RUNS ONLY ITS FEASIBILITY PROBE, because the probe's answer is that the
register cannot be built to specification from anything reachable in this environment. Joe's brief
asked for that answer inside an hour rather than a day, so it is reported before the build:

    crude production capacity, by country ....  0 of 187 geopolitical events coverable
    refining capacity, by country ...........  15 of 187 (the United States alone)

The wall is the SOURCE, not the corpus: 160 of the 187 events carry a coded country, they name only
28 distinct countries, and 145 of them are dated 2010 or later. There is nothing wrong with the
events. There is no reachable register.

WHAT WAS PROBED, and what each source turned out to be:

  EI Statistical Review xlsx  -- Joe's first preference and the one src/state/bridge.py:60 has been
                                 waiting for (`refinery_capacity_annual`). ABSENT: data/state/local/ei/
                                 does not exist, and energyinst.org returns 403 to scripts, exactly as
                                 that GAPS entry already recorded. Note also that the EI Review carries
                                 refinery capacity but NOT crude production capacity -- consistent with
                                 bridge.py listing a refinery_capacity_annual stub and no crude-capacity
                                 stub. Even delivered, it solves one half of T1.
  OPEC Annual Statistical Bulletin -- 403 to scripts.
  EIA International Energy Statistics API -- 403 without EIA_API_KEY (unset; bridge.py records it).
  EIA bulk INTL.zip           -- REACHABLE (24 MB, no key). Contains no petroleum capacity series:
                                 the 13 records whose name is "Capacity" are empty navigation nodes
                                 with no units, no geography and no data points.
  EIA STEO + monthly archives -- REACHABLE and genuinely VINTAGED (each archived release has a known
                                 publication month, which is exactly what section 3 requires). But its
                                 capacity lines are aggregates, not countries: table 3d carries "Crude
                                 oil production capacity" only as OPEC total / Middle East / Other,
                                 and table 4b's "Refinery operable distillation capacity" is the
                                 United States alone. Archives resolve back to January 2015
                                 (jan14 and earlier 404).

So the only country-resolved, vintage-dated capacity figure obtainable today is US refining capacity
from STEO 4b, back to the January 2015 archive.

Run:  python3 src/state/capacity.py       -> data/state/capacity_feasibility.json
"""

import json
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "state"
UA = {"User-Agent": "Mozilla/5.0 (compatible; ripple-engine research loader)"}

GEO_CLASSES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
STEO_ARCHIVE = "https://www.eia.gov/outlooks/steo/archives/{mon}{yy:02d}_base.xlsx"

SOURCES = [
    {"key": "ei_statistical_review", "preference": 1,
     "what": "crude production capacity? NO. refining capacity by country? YES (annual)",
     "local_path": "data/state/local/ei/", "url": "https://www.energyinst.org/statistical-review",
     "status": None, "note": "bridge.py GAPS refinery_capacity_annual has been waiting for this file"},
    {"key": "opec_asb", "preference": 2,
     "what": "crude production capacity (OPEC members) + refining capacity",
     "local_path": None, "url": "https://www.opec.org/opec_web/en/publications/202.htm",
     "status": None, "note": ""},
    {"key": "eia_ies_api", "preference": 3,
     "what": "country capacity via API", "local_path": None,
     "url": "https://api.eia.gov/v2/international/data/?frequency=annual&data[0]=value",
     "status": None, "note": "needs EIA_API_KEY; bridge.py records it as unset"},
    {"key": "eia_bulk_intl", "preference": 3,
     "what": "no petroleum capacity series (the 13 'Capacity' records are empty nodes)",
     "local_path": "data/state/raw/eia_intl/INTL.zip",
     "url": "https://www.eia.gov/opendata/bulk/INTL.zip", "status": None, "note": ""},
    {"key": "eia_steo_archives", "preference": 3,
     "what": "VINTAGED. crude capacity = OPEC/Middle East/Other aggregates only; "
             "refining capacity = United States only",
     "local_path": "data/state/raw/eia_steo/STEO_m.xlsx",
     "url": STEO_ARCHIVE.format(mon="jan", yy=15), "status": None, "note": ""},
]


def head_ok(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"reachable": r.status == 200, "http": r.status,
                    "bytes": r.headers.get("Content-Length")}
    except Exception as e:
        return {"reachable": False, "http": getattr(e, "code", type(e).__name__), "bytes": None}


def steo_archive_depth(probe_years=range(5, 27)):
    """The earliest January STEO archive that resolves -- the floor on any vintaged STEO figure."""
    earliest, checked = None, {}
    for yy in probe_years:
        u = STEO_ARCHIVE.format(mon="jan", yy=yy)
        ok = head_ok(u)["reachable"]
        checked[f"jan{yy:02d}"] = ok
        if ok:
            earliest = 2000 + yy
            break
    return earliest, checked


def coded_country_sets(conn):
    """Section 2 T1: 'countries c in the event's coded location/actor set'."""
    ev = pd.read_sql("SELECT event_id, event_date, type, sr_actor, sr_target FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])
    geo = ev[ev["type"].isin(GEO_CLASSES)].copy()
    ee = pd.read_sql("SELECT ee.event_id, ee.role, e.entity_id, e.type "
                     "FROM event_entities ee JOIN entities e ON e.entity_id = ee.entity_id", conn)
    sets = {}
    for _, r in geo.iterrows():
        s = {f for f in (r.sr_actor, r.sr_target) if isinstance(f, str) and f.startswith("country.")}
        sets[r.event_id] = s
    for _, r in ee[(ee.type == "country") & (ee.role.isin(["actor", "target", "location"]))].iterrows():
        if r.event_id in sets:
            sets[r.event_id].add(r.entity_id)
    return geo, sets


def main():
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    geo, sets = coded_country_sets(conn)

    for s in SOURCES:
        if s["local_path"]:
            s["local_present"] = (ROOT / s["local_path"]).exists()
        s["probe"] = head_ok(s["url"])
    depth, checked = steo_archive_depth()

    named = {e: v for e, v in sets.items() if v}
    countries = sorted(set().union(*sets.values())) if sets else []
    usa = [e for e, v in sets.items() if "country.usa" in v]
    usa_after = [e for e in usa
                 if depth and geo.loc[geo.event_id == e, "event_date"].iloc[0] >= pd.Timestamp(f"{depth}-01-01")]

    by_decade = {}
    for a, b in [(1973, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2026)]:
        m = (geo.event_date.dt.year >= a) & (geo.event_date.dt.year <= b)
        by_decade[f"{a}-{b}"] = {"events": int(m.sum()),
                                 "with_coded_country": int(sum(1 for e in geo.loc[m, "event_id"] if sets[e]))}

    payload = {
        "meta": {"when": t0.isoformat(timespec="seconds"),
                 "registration": "PHYSICAL_EXPOSURE_REGISTRATION.md T1, committed 66b1c30",
                 "status": "FEASIBILITY PROBE ONLY -- the register was not built, see verdict"},
        "corpus_side": {
            "geopolitical_events": int(len(geo)),
            "classes": list(GEO_CLASSES),
            "with_at_least_one_coded_country": len(named),
            "without_any_coded_country": int(len(geo)) - len(named),
            "distinct_countries_named": len(countries),
            "countries": countries,
            "by_period": by_decade,
            "reads": "the corpus side is not the constraint",
        },
        "sources": SOURCES,
        "steo_archive_depth": {"earliest_resolving_january_archive": depth, "probed": checked},
        "coverage_answer": {
            "question": ("how many of the 187 geopolitical events have a coded country with a "
                         "capacity figure PUBLISHED BEFORE the event date"),
            "crude_production_capacity_by_country": {
                "events_coverable": 0, "of": int(len(geo)),
                "why": "no reachable source carries crude production capacity at country resolution; "
                       "STEO gives OPEC/Middle East/Other aggregates, EIA bulk carries none, "
                       "OPEC ASB and the EIA API are 403/keyed, and the EI Review does not carry it"},
            "refining_capacity_by_country": {
                "events_coverable": len(usa_after), "of": int(len(geo)),
                "countries_available": ["country.usa"],
                "vintage_floor": f"{depth}-01" if depth else None,
                "why": "STEO table 4b 'Refinery operable distillation capacity' is the United States "
                       "alone; STEO monthly archives supply a genuine publication date but resolve "
                       "only back to January 2015"},
        },
        "verdict": "BLOCKED ON SOURCE -- T1 cannot be built to section 3's specification today",
        "unblocks": [
            "data/state/local/ei/<EI Statistical Review xlsx> would supply REFINING capacity by "
            "country with per-edition publication dates, closing bridge.py's refinery_capacity_annual "
            "stub and about half of T1",
            "crude production capacity by country needs OPEC ASB (403), IEA OMR (licensed) or the "
            "EIA IES API (EIA_API_KEY unset) -- none reachable, and the EI Review does not carry it",
        ],
    }
    (OUT / "capacity_feasibility.json").write_text(json.dumps(payload, indent=1, default=str))

    c = payload["corpus_side"]
    print(f"corpus side: {c['geopolitical_events']} geopolitical events, "
          f"{c['with_at_least_one_coded_country']} with a coded country, "
          f"{c['distinct_countries_named']} distinct countries")
    for s in SOURCES:
        lp = s.get("local_present")
        print(f"  [{s['key']:22s}] pref {s['preference']}  http={str(s['probe']['http']):>6}  "
              f"local_present={lp}")
    print(f"  STEO archive floor: {depth}")
    a = payload["coverage_answer"]
    print(f"\nANSWER  crude production capacity by country: "
          f"{a['crude_production_capacity_by_country']['events_coverable']} of {len(geo)}")
    print(f"ANSWER  refining capacity by country:        "
          f"{a['refining_capacity_by_country']['events_coverable']} of {len(geo)} (USA only)")
    print(f"\n{payload['verdict']}")
    conn.close()


if __name__ == "__main__":
    main()
