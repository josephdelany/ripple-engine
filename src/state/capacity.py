"""
capacity.py -- T1 of PHYSICAL_EXPOSURE_REGISTRATION.md: the country capacity register.

T1 needs, per country, CRUDE PRODUCTION CAPACITY and REFINING CAPACITY, every row carrying the
PUBLICATION DATE of the register it came from -- not its reference year. Section 3 is the trap: the
2019 EI Review published mid-2020 may not inform a 2019 forecast, and `test_capacity_filtration`
asserts that no value is ever read before it was published.

WHAT THIS REGISTER ACTUALLY CONTAINS, stated before the code so nothing is oversold. The feasibility
probe (kept below as `probe_sources`, reported to Joe before the build) established that no reachable
source carries crude production capacity at COUNTRY resolution:

    EI Statistical Review xlsx  ABSENT -- data/state/local/ei/ does not exist and energyinst.org is
                                403 to scripts, exactly as src/state/bridge.py:60's
                                refinery_capacity_annual GAPS entry already recorded. It carries
                                refining capacity but not crude production capacity, so even
                                delivered it closes one half of T1.
    OPEC ASB                    403.  EIA IES API  403 (EIA_API_KEY unset).
    EIA bulk INTL.zip           reachable, but its 13 "Capacity" records are empty navigation nodes.
    EIA STEO + monthly archives reachable AND genuinely vintaged -- each release states its own
                                forecast month on the `Dates` sheet -- but its capacity lines are
                                regional aggregates, and its refining capacity is the US alone.

So the register is built from STEO archives and is honest about its shape:

    refining capacity     country  United States            -- a real country row, per vintage
    crude prod. capacity  AGGREGATE OPEC / Middle East / Other / Africa / South America
    surplus capacity      AGGREGATE OPEC and regions (this is section 2's SPARE(t), vintaged)

and every country the corpus names, for which no register exists, gets an explicit **null row with a
reason** rather than a zero or a silent absence. Section 2's registered fallback governs: "Where a
country has no capacity register before t, X1 is null, not zero."

`knowable_at` is the LAST DAY of the release month. STEO is published in the first half of its month,
so end-of-month is conservative: it can only delay knowability, never manufacture look-ahead.

Run:  python3 src/state/capacity.py             -> data/state/capacity_register.json
      python3 src/state/capacity.py --probe     -> data/state/capacity_feasibility.json
"""

import calendar
import json
import re
import sqlite3
import sys
import urllib.request
import warnings
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "state"
RAW = ROOT / "data" / "state" / "raw" / "steo_archives"          # gitignored
UA = {"User-Agent": "Mozilla/5.0 (compatible; ripple-engine research loader)"}

GEO_CLASSES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
ARCHIVE = "https://www.eia.gov/outlooks/steo/archives/{mon}{yy:02d}_base.xlsx"
CURRENT = ROOT / "data" / "state" / "raw" / "eia_steo" / "STEO_m.xlsx"
MONTHS = ["jan", "apr", "jul", "oct"]                             # quarterly vintage grid
YEARS = range(15, 27)
BLOCKS = {
    "crude_production_capacity": "crude oil production capacity",
    "surplus_crude_production_capacity": "surplus crude oil production capacity",
}
REFINING_LABEL = "refinery operable distillation capacity"
AGG_ENTITIES = {"africa": "region.africa", "south america": "region.south_america",
                "middle east": "region.middle_east", "other": "region.other",
                "opec total": "opec.total"}


# =============================================================================================
# source probe (reported to Joe before the register was built)
# =============================================================================================

def head_ok(url, timeout=12):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA, method="HEAD"),
                                    timeout=timeout) as r:
            return {"reachable": r.status == 200, "http": r.status,
                    "bytes": r.headers.get("Content-Length")}
    except Exception as e:
        return {"reachable": False, "http": getattr(e, "code", type(e).__name__), "bytes": None}


def probe_sources():
    srcs = [
        ("ei_statistical_review", 1, "https://www.energyinst.org/statistical-review",
         "data/state/local/ei/", "refining capacity by country; NOT crude production capacity"),
        ("opec_asb", 2, "https://www.opec.org/opec_web/en/publications/202.htm", None,
         "crude production capacity (OPEC members) + refining capacity"),
        ("eia_ies_api", 3, "https://api.eia.gov/v2/international/data/?frequency=annual&data[0]=value",
         None, "needs EIA_API_KEY; bridge.py records it unset"),
        ("eia_bulk_intl", 3, "https://www.eia.gov/opendata/bulk/INTL.zip",
         "data/state/raw/eia_intl/INTL.zip", "no petroleum capacity series (13 empty 'Capacity' nodes)"),
        ("eia_steo_archives", 3, ARCHIVE.format(mon="jan", yy=15),
         "data/state/raw/steo_archives/", "VINTAGED; aggregates for crude capacity, US-only refining"),
    ]
    out = []
    for key, pref, url, local, what in srcs:
        out.append({"key": key, "preference": pref, "url": url, "what": what,
                    "local_path": local,
                    "local_present": bool(local and (ROOT / local).exists()),
                    "probe": head_ok(url)})
    return out


# =============================================================================================
# STEO archive parsing
# =============================================================================================

def fetch_vintage(mon, yy):
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"{mon}{yy:02d}_base.xlsx"
    if p.exists():
        return p
    try:
        with urllib.request.urlopen(urllib.request.Request(ARCHIVE.format(mon=mon, yy=yy),
                                                           headers=UA), timeout=90) as r:
            p.write_bytes(r.read())
        return p
    except Exception:
        return None


def release_month(path):
    """The release's own statement of its forecast month, from the `Dates` sheet."""
    try:
        d = pd.read_excel(path, sheet_name="Dates", header=None)
    except Exception:
        return None
    for _, row in d.iterrows():
        cells = [str(v) for v in row.tolist() if isinstance(v, str)]
        if any("Forecast Month" in c for c in cells):
            for v in row.tolist():
                if isinstance(v, str) and re.match(r"^[A-Z][a-z]+ \d{4}$", v.strip()):
                    return pd.Timestamp(v.strip())
    return None


def period_columns(df):
    """column index -> Timestamp, from the sparse year row and the month row."""
    yr_row = mo_row = None
    for i in range(0, 8):
        vals = df.iloc[i].tolist()
        if mo_row is None and sum(1 for v in vals if isinstance(v, str) and v.strip()[:3] in
                                  ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                                   "Sep", "Oct", "Nov", "Dec")) >= 6:
            mo_row = i
        if yr_row is None and sum(1 for v in vals if isinstance(v, (int, float))
                                  and v == v and 1990 < float(v) < 2100) >= 1:
            yr_row = i
    if mo_row is None or yr_row is None:
        return {}
    cols, cur = {}, None
    for j in range(2, df.shape[1]):
        y = df.iloc[yr_row, j]
        if isinstance(y, (int, float)) and y == y and 1990 < float(y) < 2100:
            cur = int(y)
        m = df.iloc[mo_row, j]
        if cur and isinstance(m, str) and m.strip()[:3] in calendar.month_abbr[1:]:
            cols[j] = pd.Timestamp(year=cur, month=list(calendar.month_abbr).index(m.strip()[:3]), day=1)
    return cols


def find_block(df, label):
    for i in range(len(df)):
        v = df.iloc[i, 1]
        if isinstance(v, str) and label in v.strip().lower():
            return i
    return None


def read_vintage(path, pub):
    """Every capacity row this release states, at the last period on or before the release month."""
    rows = []
    knowable = pd.Timestamp(pub.year, pub.month, calendar.monthrange(pub.year, pub.month)[1])
    xl = pd.ExcelFile(path)

    def latest_col(cols):
        ok = [j for j, d in cols.items() if d <= pub]
        return max(ok, key=lambda j: cols[j]) if ok else None

    for sheet in xl.sheet_names:
        try:
            df = pd.read_excel(xl, sheet_name=sheet, header=None)
        except Exception:
            continue
        cols = period_columns(df)
        if not cols:
            continue
        j = latest_col(cols)
        if j is None:
            continue
        for measure, label in BLOCKS.items():
            st = find_block(df, label)
            if st is None:
                continue
            for i in range(st + 1, min(st + 9, len(df))):
                lab = df.iloc[i, 1]
                if not isinstance(lab, str) or not lab.strip():
                    break
                key = lab.strip().lower()
                if key not in AGG_ENTITIES:
                    continue
                val = df.iloc[i, j]
                if not isinstance(val, (int, float)) or val != val:
                    continue
                rows.append({"measure": measure, "scope": "aggregate",
                             "entity_id": AGG_ENTITIES[key], "entity_label": lab.strip(),
                             "value_kbd": round(float(val) * 1000, 3), "unit": "kb/d",
                             "reference_period": str(cols[j].date())[:7],
                             "publication_date": str(pub.date())[:7],
                             "knowable_at": str(knowable.date()),
                             "source": "EIA STEO", "vintage_file": path.name, "sheet": sheet})
        st = find_block(df, REFINING_LABEL)
        if st is not None:
            val = df.iloc[st, j]
            if isinstance(val, (int, float)) and val == val:
                rows.append({"measure": "refining_capacity", "scope": "country",
                             "entity_id": "country.usa", "entity_label": "United States",
                             "value_kbd": round(float(val) * 1000, 3), "unit": "kb/d",
                             "reference_period": str(cols[j].date())[:7],
                             "publication_date": str(pub.date())[:7],
                             "knowable_at": str(knowable.date()),
                             "source": "EIA STEO table 4b", "vintage_file": path.name, "sheet": sheet})
    # de-duplicate: the same measure/entity can appear on more than one sheet in a release
    seen, out = set(), []
    for r in rows:
        k = (r["measure"], r["entity_id"], r["publication_date"])
        if k in seen:
            continue
        seen.add(k); out.append(r)
    return out


# =============================================================================================
# the register
# =============================================================================================

def lookup(register, entity_id, measure, t):
    """Section 3, enforced here rather than trusted: the most recent row PUBLISHED strictly on or
    before t. Returns None where no register predates t -- null, not zero (section 2)."""
    t = pd.Timestamp(t)
    cand = [r for r in register
            if r["entity_id"] == entity_id and r["measure"] == measure
            and pd.Timestamp(r["knowable_at"]) <= t]
    return max(cand, key=lambda r: pd.Timestamp(r["knowable_at"])) if cand else None


def coded_country_sets(conn):
    ev = pd.read_sql("SELECT event_id, event_date, type, sr_actor, sr_target FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])
    geo = ev[ev["type"].isin(GEO_CLASSES)].copy()
    ee = pd.read_sql("SELECT ee.event_id, ee.role, e.entity_id, e.type "
                     "FROM event_entities ee JOIN entities e ON e.entity_id = ee.entity_id", conn)
    sets = {r.event_id: {f for f in (r.sr_actor, r.sr_target)
                         if isinstance(f, str) and f.startswith("country.")}
            for _, r in geo.iterrows()}
    for _, r in ee[(ee.type == "country") & (ee.role.isin(["actor", "target", "location"]))].iterrows():
        if r.event_id in sets:
            sets[r.event_id].add(r.entity_id)
    return geo, sets


def main(argv):
    t0 = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    sources = probe_sources()
    if "--probe" in argv:
        (OUT / "capacity_feasibility.json").write_text(json.dumps(
            {"when": t0.isoformat(timespec="seconds"), "sources": sources}, indent=1, default=str))
        for s in sources:
            print(f"  [{s['key']:22s}] http={str(s['probe']['http']):>6} local={s['local_present']}")
        return

    vintages, register = [], []
    todo = [(m, y) for y in YEARS for m in MONTHS]
    for mon, yy in todo:
        p = fetch_vintage(mon, yy)
        if not p:
            continue
        pub = release_month(p)
        if pub is None:
            continue
        rows = read_vintage(p, pub)
        if rows:
            register.extend(rows)
            vintages.append({"file": p.name, "publication_month": str(pub.date())[:7],
                             "knowable_at": rows[0]["knowable_at"], "rows": len(rows)})
    if CURRENT.exists():
        pub = release_month(CURRENT)
        if pub is not None:
            rows = read_vintage(CURRENT, pub)
            if rows:
                register.extend(rows)
                vintages.append({"file": CURRENT.name, "publication_month": str(pub.date())[:7],
                                 "knowable_at": rows[0]["knowable_at"], "rows": len(rows)})
    register.sort(key=lambda r: (r["measure"], r["entity_id"], r["knowable_at"]))

    conn = sqlite3.connect(DB)
    geo, sets = coded_country_sets(conn)
    named = sorted(set().union(*sets.values())) if sets else []

    # explicit null rows: every country the corpus names, for each measure with no register
    have = {(r["entity_id"], r["measure"]) for r in register}
    gaps = []
    for cc in named:
        for measure in ("crude_production_capacity", "refining_capacity"):
            if (cc, measure) in have:
                continue
            gaps.append({"measure": measure, "scope": "country", "entity_id": cc,
                         "value_kbd": None, "unit": "kb/d", "knowable_at": None,
                         "reason": ("no reachable register carries this measure at country "
                                    "resolution: EI xlsx absent (403), OPEC ASB 403, EIA IES API "
                                    "keyed, EIA bulk carries none, STEO is regional for crude "
                                    "capacity and US-only for refining"),
                         "registered_fallback": "PHYSICAL_EXPOSURE_REGISTRATION.md section 2: X1 is null, not zero"})

    # coverage, computed FROM the register by the same lookup the study would use
    cov = {}
    for measure in ("crude_production_capacity", "refining_capacity"):
        n = 0
        for _, e in geo.iterrows():
            if any(lookup(register, cc, measure, e.event_date) for cc in sets[e.event_id]):
                n += 1
        cov[measure] = {"events_with_a_country_figure_published_before_the_event": n,
                        "of": int(len(geo))}

    payload = {
        "meta": {"when": t0.isoformat(timespec="seconds"),
                 "registration": "PHYSICAL_EXPOSURE_REGISTRATION.md T1, committed 66b1c30",
                 "knowable_at_rule": ("last day of the release month; STEO publishes in the first "
                                      "half, so this is conservative and cannot create look-ahead"),
                 "vintage_grid": "quarterly Jan/Apr/Jul/Oct 2015-2026 plus the current release",
                 "sources_probed": sources},
        "vintages": vintages,
        "register": register,
        "gaps": gaps,
        "coverage": cov,
        "corpus_side": {"geopolitical_events": int(len(geo)),
                        "with_a_coded_country": sum(1 for v in sets.values() if v),
                        "distinct_countries_named": len(named), "countries": named},
        "verdict": ("PARTIAL -- refining capacity is a real country row for the United States only; "
                    "crude production capacity exists at regional aggregate resolution and at no "
                    "country. Every named country without a register carries an explicit null."),
    }
    (OUT / "capacity_register.json").write_text(json.dumps(payload, indent=1, default=str))

    print(f"vintages parsed: {len(vintages)}  register rows: {len(register)}  null rows: {len(gaps)}")
    bym = {}
    for r in register:
        bym.setdefault((r["measure"], r["scope"]), set()).add(r["entity_id"])
    for (m, sc), ents in sorted(bym.items()):
        print(f"  {m:34s} [{sc:9s}] {len(ents)} entities  {sorted(ents)}")
    print(f"\ncoverage of the {len(geo)} geopolitical events:")
    for m, v in cov.items():
        print(f"  {m:34s} {v['events_with_a_country_figure_published_before_the_event']} of {v['of']}")
    conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
