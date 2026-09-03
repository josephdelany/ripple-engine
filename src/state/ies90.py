"""ies90.py -- OUTCOME_MAPPING.md Amendment 1 (code): IES-90, the Independent Escalation Scale over (d, d+90].

Per geopolitical event: level 0 none / 1 threat or display / 2 use of force / 3 war, plus a DEAL flag, each from
DATED records only -- MIDI/MIDIP 5.0 incidents (1993-2014), Dyadic MID 4.03 dispute dates + hihost (to 2014; its
war=1 rows are the COW war dates used), ICB v16 trigdate/termdate + viol + forout (1918-2021), UCDP GED 26.1
state-based deaths in the location (1989-2025, location only: the cache has no dyad field), COW War v4 inter-/intra-state
war spells (Amendment 1.1: the only source that DATES a war; ICB/MID assert only what they can date). The level is the max
over the sources that COVER the window; 0 is asserted only when a covering source records nothing; no covering
source -> no_independent_outcome, never guessed. Writes event_outcomes rows with source='ies90' (other sources'
rows untouched), data/state/ies90_distribution.json and data/audits/ies90_audit_30.csv. Reads events; never
writes them. The retired sr_outcome_90 is cross-tabulated for the record only.

Run:  python3 src/state/ies90.py
"""
import csv
import json
import random
import re
import sqlite3
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402
import outcomes as O  # noqa: E402

REGISTRATION = "OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2 + 4 (2026-09-02)"
SEED = 20260902
WINDOW = 90
DIST_OUT = P.DATA / "state" / "ies90_distribution.json"
A4_OUT = P.DATA / "state" / "ies90_amendment4_counts.json"     # A4.8: before/after, computed with write=False
AUDIT_OUT = P.DATA / "audits" / "ies90_audit_30.csv"
CLASS_AUDIT = P.DATA / "spine" / "CLASS_AUDIT.md"      # session F's reading of all 187 geopolitical events
GED_CACHE = P.DATA / "cache" / "ucdp_ged_26.1.json"
MID5_ZIP = P.raw_path("cow_mid", "MID-5-Data-and-Supporting-Materials.zip")
WAR_URLS = {"inter": ("https://correlatesofwar.org/wp-content/uploads/Inter-StateWarData_v4.0.csv", "Inter-StateWarData_v4.0.csv"),
            "intra": ("https://correlatesofwar.org/wp-content/uploads/Intra-StateWarData_v4.1.csv", "Intra-StateWarData_v4.1.csv")}

SOURCES = ("midi", "war", "icb", "mid", "ged")                # tie order for level_source (A1.1)
COVER = {"midi": ("1993-01-01", "2014-12-31"), "war": ("1816-01-01", "2007-12-31"), "war_intra": ("1816-01-01", "2014-12-31"),
         "mid": ("1816-01-01", "2014-12-31"), "icb": ("1918-01-01", "2021-12-31"), "ged": ("1989-01-01", "2025-12-31")}
HOSTLEV_TO_LEVEL = {1: 0, 2: 1, 3: 1, 4: 2, 5: 3}            # MID hostility level -> IES level
VIOL_TO_LEVEL = {1: 1, 2: 2, 3: 2, 4: 3}                     # ICB violence -> IES level
GED_WAR, GED_FORCE = 250, 25                                 # deaths in 90 days: 1000*90/365 = 246.6 -> 250; UCDP floor 25
LEVEL_MEANING = {0: "none", 1: "threat or display of force", 2: "use of force", 3: "war"}
DYADIC_SOURCES = ("midi", "war", "icb", "mid")               # A2.1: can carry a pair-matched record
# A2.2: chokepoint / facility entity -> littoral or host states, added to L ONLY (never A or P)
LITTORAL = {
    "chokepoint.hormuz": ("country.iran", "country.uae", "country.omn"),
    "chokepoint.bab_el_mandeb": ("country.yemen",),                       # Djibouti, Eritrea unmapped
    "chokepoint.suez": ("country.egypt",), "chokepoint.suez_canal": ("country.egypt",),
    "chokepoint.gibraltar_strait": ("country.gbr",),                      # Spain, Morocco unmapped
    "chokepoint.malacca": ("country.indonesia",),                         # Malaysia, Singapore unmapped
    "chokepoint.taiwan_strait": ("country.taiwan", "country.china"),
    "chokepoint.libya_es_sider": ("country.libya",),
    "chokepoint.kirkuk_ceyhan_pipeline": ("country.iraq", "country.turkey"),
    "chokepoint.druzhba_pipeline": ("country.russia", "country.ukraine", "country.hungary"),   # Belarus, Poland, Slovakia, Czechia unmapped
    "chokepoint.cpc_novorossiysk": ("country.russia", "country.kazakhstan"),
}
# GED `country` string -> corpus entity, for every GED name that maps to countries.py (verified against the 126 names
# in the 26.1 cache on 2026-09-02). Names absent here are reported in the distribution file, never dropped silently.
GED_NAMES = {
    "United States of America": "country.usa", "Canada": "country.canada", "Panama": "country.panama",
    "Venezuela": "country.venezuela", "Ecuador": "country.ecuador", "Peru": "country.peru", "Argentina": "country.argentina",
    "Serbia (Yugoslavia)": "country.serbia", "Russia (Soviet Union)": "country.russia", "Ukraine": "country.ukraine",
    "Georgia": "country.georgia", "Azerbaijan": "country.azerbaijan", "Niger": "country.niger", "Guinea": "country.guinea",
    "Nigeria": "country.nigeria", "DR Congo (Zaire)": "country.congo_drc", "South Africa": "country.south_africa",
    "Libya": "country.libya", "Sudan": "country.sudan", "Iran": "country.iran", "Turkey": "country.turkey", "Iraq": "country.iraq",
    "Egypt": "country.egypt", "Lebanon": "country.lebanon", "Israel": "country.israel", "Saudi Arabia": "country.saudi_arabia",
    "Yemen (North Yemen)": "country.yemen", "Kuwait": "country.kuwait", "Qatar": "country.qatar",
    "United Arab Emirates": "country.uae", "China": "country.china", "India": "country.india", "Myanmar (Burma)": "country.myanmar",
    "Thailand": "country.thailand", "Philippines": "country.philippines", "Indonesia": "country.indonesia",
    "United Kingdom": "country.gbr", "France": "country.fra", "Germany": "country.deu", "Afghanistan": "country.afg",
    "Pakistan": "country.pak", "Syria": "country.syr", "Jordan": "country.jor", "Bahrain": "country.bhr", "Algeria": "country.dza",
    "Angola": "country.ago", "Mexico": "country.mex", "Brazil": "country.bra", "Colombia": "country.col",
}


# ----------------------------------------------------------------------------- pure rules (A1.2)

def window(d):
    """W = (d, d+90] as (first day, last day)."""
    d = pd.Timestamp(d)
    return d + pd.Timedelta(days=1), d + pd.Timedelta(days=WINDOW)


def pre_window(d):
    """A4.2: B = [d-90, d-1], the 90 days STRICTLY BEFORE d. Day d belongs to the event and is in neither
    window (A4.4 -- the pre-Amendment-4 field ran [d-89, d] and so counted the event's own violence as 'before')."""
    d = pd.Timestamp(d)
    return d - pd.Timedelta(days=WINDOW), d - pd.Timedelta(days=1)


def covered_by(spells, lo, hi):
    """A4.2: does any one spell cover the WHOLE of [lo, hi]? (the COW / MIDI continuation test)"""
    return any(st <= pd.Timestamp(lo) and en >= pd.Timestamp(hi) for st, en in spells)


def covers(src, d):
    lo, hi = COVER[src]
    w0, w1 = window(d)
    return pd.Timestamp(lo) <= pd.Timestamp(d) and w1 <= pd.Timestamp(hi)


def ged_level(deaths):
    if deaths >= GED_WAR:
        return 3
    if deaths >= GED_FORCE:
        return 2
    return 0


def _mid_date(y, m, dd):
    """COW dates: unknown (-9) month/day -> 1; unknown year -> NaT."""
    try:
        y = int(y); m = int(m); dd = int(dd)
    except (TypeError, ValueError):
        return pd.NaT
    if y <= 0:
        return pd.NaT
    m = m if m > 0 else 1
    dd = dd if dd > 0 else 1
    return pd.Timestamp(year=y, month=min(m, 12), day=min(dd, 28))


# ----------------------------------------------------------------------------- loaders

def load_midi(zip_path=MID5_ZIP):
    """MIDI 5.0 incidents with dates, and MIDIP participants (entity, side) per incident."""
    z = zipfile.ZipFile(zip_path)
    inc = pd.read_csv(z.open("MIDI 5.0.csv"))
    par = pd.read_csv(z.open("MIDIP 5.0.csv"))
    inc["start"] = [_mid_date(y, m, d) for y, m, d in zip(inc.styear, inc.stmon, inc.stday)]
    inc["end"] = [_mid_date(y, m, d) for y, m, d in zip(inc.endyear, inc.endmon, inc.endday)]
    inc["end"] = inc["end"].fillna(inc["start"])
    inc.loc[inc["end"] < inc["start"], "end"] = inc["start"]
    inc = inc.dropna(subset=["start"])
    parts = defaultdict(list)
    for r in par.itertuples(index=False):
        e = C.from_ccode(r.ccode)
        if e:
            parts[int(r.incidnum)].append((e, int(r.sidea)))
    return inc, parts


def dedupe_mid(mid):
    """One row per (dispute, dyad): the file carries both directions and one row per dispute-year (A1.1.3).
    Max hihost; settlmnt/end/war from the last year's row."""
    mid = mid.sort_values(["disno", "year"]).copy()
    mid["key"] = [f"{int(d)}:{'|'.join(sorted(p))}" for d, p in zip(mid["disno"], mid["pair"])]
    hi = mid.groupby("key")["hihost"].max()
    start = mid.groupby("key")["start"].min()
    last = mid.drop_duplicates("key", keep="last").set_index("key")
    last["hihost"] = hi; last["start"] = start
    return last.reset_index(drop=True)


def _int(x):
    try:
        return int(x) if not pd.isna(x) else -9
    except (TypeError, ValueError):
        return -9


def _war_spell(r, y_col, m_col, d_col, ey_col, em_col, ed_col, period_end):
    """One dated spell; unknown month/day -> 1; an end coded ongoing/unknown (<= 0 or blank) -> the period end."""
    y = _int(getattr(r, y_col))
    if y <= 0:
        return None
    st = _mid_date(y, _int(getattr(r, m_col)), _int(getattr(r, d_col)))
    ey = _int(getattr(r, ey_col))
    en = _mid_date(ey, _int(getattr(r, em_col)), _int(getattr(r, ed_col))) if ey > 0 else pd.Timestamp(period_end)
    if pd.isna(st):
        return None
    return st, max(en, st)


def load_war():
    """COW War v4: inter-state participants with sides and dated spells; intra-state wars with their state parties."""
    out = {"inter": [], "intra": []}
    for kind, (url, name) in WAR_URLS.items():
        p, _ = P.fetch_file(url, P.raw_path("cow_war", name))
        df = pd.read_csv(p, encoding="latin-1")
        period_end = COVER["war" if kind == "inter" else "war_intra"][1]
        for r in df.itertuples(index=False):
            spells = [sp for sp in (_war_spell(r, "StartYear1", "StartMonth1", "StartDay1", "EndYear1", "EndMonth1", "EndDay1", period_end),
                                    _war_spell(r, "StartYear2", "StartMonth2", "StartDay2", "EndYear2", "EndMonth2", "EndDay2", period_end)) if sp]
            if kind == "inter":
                e = C.from_ccode(r.ccode)
                if e:
                    out["inter"].append({"war": int(r.WarNum), "name": r.WarName, "ent": e, "side": int(r.Side), "spells": spells})
            else:
                ents = {C.from_ccode(getattr(r, c)) for c in ("CcodeA", "CcodeB")} - {None}
                if ents:
                    out["intra"].append({"war": int(r.WarNum), "name": r.WarName, "ents": ents, "spells": spells})
    return out


def load_ged(path=GED_CACHE):
    """Per entity: sorted dates and cumulative state-based deaths (tov 1) and other deaths (tov 2/3).
    Returns (series, unmapped names, n events, date range)."""
    ev = json.loads(Path(path).read_text())
    names = Counter(e["country"] for e in ev)
    unmapped = sorted(n for n in names if n not in GED_NAMES)
    by = defaultdict(lambda: {"state": defaultdict(float), "other": defaultdict(float)})
    for e in ev:
        ent = GED_NAMES.get(e["country"])
        if not ent:
            continue
        kind = "state" if int(e.get("tov") or 0) == 1 else "other"
        by[ent][kind][e["date_start"][:10]] += float(e.get("best") or 0)
    series = {}
    for ent, kinds in by.items():
        series[ent] = {}
        for kind, dd in kinds.items():
            dates = np.array(sorted(dd), dtype="datetime64[D]")
            cum = np.concatenate([[0.0], np.cumsum([dd[str(x)] for x in dates])])
            series[ent][kind] = (dates, cum)
    rng = (min(e["date_start"] for e in ev)[:10], max(e["date_start"] for e in ev)[:10]) if ev else (None, None)
    return series, unmapped, len(ev), rng


def ged_sum(series, ents, lo, hi, kind="state"):
    """Sum of deaths with date_start in [lo, hi] over the entities."""
    tot = 0.0
    lo64, hi64 = np.datetime64(pd.Timestamp(lo).date()), np.datetime64(pd.Timestamp(hi).date())
    for ent in ents:
        s = series.get(ent, {}).get(kind)
        if not s:
            continue
        dates, cum = s
        tot += cum[np.searchsorted(dates, hi64, side="right")] - cum[np.searchsorted(dates, lo64, side="left")]
    return tot


# ----------------------------------------------------------------------------- per-source scoring (A1.2 table)

def score_midi(d, A, pairs, inc, parts):
    w0, w1 = window(d)
    sub = inc[(inc["start"] <= w1) & (inc["end"] >= w0)]
    hits = []
    for r in sub.itertuples(index=False):
        ps = parts.get(int(r.incidnum), [])
        side = {e: s for e, s in ps}
        if pairs:
            ok = any(a in side and b in side and side[a] != side[b] for a, b in (tuple(p) for p in pairs))
        else:
            ok = bool(set(side) & A)
        if ok:
            hits.append(r)
    b0, b1 = pre_window(d)
    basis = "dyadic" if pairs else "location"
    recs, level = [], 0
    for r in hits:
        lv = HOSTLEV_TO_LEVEL.get(int(r.hostlev), 0)
        # A4.2: an incident that already covered the whole of B asserts nothing new about W (expected never to fire --
        # MIDI incidents are days long -- but the predicate is the same one for all five sources).
        cont = lv > 0 and covered_by([(r.start, r.end)], b0, b1)
        rule = "MIDI.continuation" if cont else f"MIDI.{'pair' if pairs else 'single'}.overlap"
        code = f"hostlev {int(r.hostlev)} fatality {int(r.fatality)} action {int(r.action)}"
        if cont:
            code += "; incident covers all of B -> undated-for-W (A4.2, no level)"
        recs.append({"source": "midi", "basis": basis, "rule": rule, "record": f"incident {int(r.incidnum)} (dispute {int(r.dispnum)})",
                     "dates": f"{r.start.date()}..{r.end.date()}", "code": code, "level": None if cont else lv})
        if not cont:
            level = max(level, lv)
    return level, recs


def score_war(d, A, pairs, L, war, cover_inter=True, cover_intra=True):
    """A1.1.1: a COW war spell overlapping W -> 3. Inter-state: a pair in P on opposite sides (any participant in A
    when P is empty); intra-state: a state party in L.
    A4.2: unless the spell also covers the WHOLE of B = [d-90, d-1] -- a war that was already running at this level
    across the preceding 90 days asserts nothing about this event, so the record is undated-for-W and sets no level.
    A spell that starts at, just before, or inside W is an ONSET and keeps level 3 (Yom Kippur 1973, Kuwait 1990,
    Iraq 2003, Ukraine 2022 all keep it)."""
    w0, w1 = window(d)
    b0, b1 = pre_window(d)
    level, recs = 0, []
    if cover_inter:
        by_war = defaultdict(list)
        for p in war["inter"]:
            if any(st <= w1 and en >= w0 for st, en in p["spells"]):
                by_war[p["war"]].append(p)
        for wn, ps in by_war.items():
            side = {p["ent"]: p["side"] for p in ps}
            if pairs:
                ok = any(a in side and b in side and side[a] != side[b] for a, b in (tuple(x) for x in pairs))
            else:
                ok = bool(set(side) & A)
            if ok:
                spells = [sp for pp in ps for sp in pp["spells"]]
                cont = covered_by(spells, b0, b1)                      # A4.2: the war already ran across the whole of B
                sp = "; ".join(f"{st.date()}..{en.date()}" for st, en in ps[0]["spells"])
                recs.append({"source": "war", "basis": "dyadic" if pairs else "location",
                             "rule": "WAR.inter.continuation" if cont else f"WAR.inter.{'pair' if pairs else 'single'}",
                             "record": f"COW inter-state war {wn} {ps[0]['name']} ({', '.join(f'{e}:side{s_}' for e, s_ in sorted(side.items()))})",
                             "dates": sp,
                             "code": "war spell covers all of B -> undated-for-W (A4.2, no level)" if cont else "war spell overlaps W",
                             "level": None if cont else 3})
                if not cont:
                    level = 3
    if cover_intra:
        for p in war["intra"]:
            if p["ents"] & set(L) and any(st <= w1 and en >= w0 for st, en in p["spells"]):
                cont = covered_by(p["spells"], b0, b1)                 # A4.2
                recs.append({"source": "war", "basis": "location",
                             "rule": "WAR.intra.continuation" if cont else "WAR.intra.location",
                             "record": f"COW intra-state war {p['war']} {p['name']} (state party {','.join(sorted(p['ents']))})",
                             "dates": "; ".join(f"{st.date()}..{en.date()}" for st, en in p["spells"]),
                             "code": "war spell covers all of B -> undated-for-W (A4.2, no level)" if cont else "war spell overlaps W (location)",
                             "level": None if cont else 3})
                if not cont:
                    level = 3
    return level, recs


def score_mid(d, A, pairs, mid):
    w0, w1 = window(d)
    if pairs:
        sub = mid[mid["pair"].isin(pairs)]
    else:
        sub = mid[mid["ea"].isin(A) | mid["eb"].isin(A)]
    end = sub["end"].fillna(sub["start"])
    sub = sub[(sub["start"] <= w1) & (end >= w0)]
    level, deal, recs = 0, 0, []
    for r in sub.itertuples(index=False):
        h = int(r.hihost)
        e = r.end if pd.notna(r.end) else r.start
        kind = "pair" if pairs else "single"
        if w0 <= r.start and e <= w1:
            lv, how, rule = HOSTLEV_TO_LEVEL.get(h, 0), "wholly inside W", f"MID.{kind}.wholly"
        elif w0 <= r.start <= w1:
            lv, how, rule = 1, f"starts in W, ends after (onset dated -> 1; hihost {h} is the undated peak)", f"MID.{kind}.onset"
        else:
            lv, how, rule = None, "ongoing at d, force undated in W (no level)", f"MID.{kind}.ongoing"
        fired = w0 <= e <= w1 and int(r.settlmnt or 0) == 1
        deal = deal or int(fired)
        if lv is not None:
            level = max(level, lv)
        recs.append({"source": "mid", "basis": "dyadic" if pairs else "location", "rule": rule,
                     "record": f"dispute {int(r.disno)} {r.namea}-{r.nameb}" + (" [COW war]" if int(getattr(r, "war", 0) or 0) == 1 else ""),
                     "dates": f"{r.start.date()}..{e.date()}", "code": f"hihost {h} settlmnt {int(r.settlmnt) if pd.notna(r.settlmnt) else '?'} ({how})" + ("; negotiated end in W -> DEAL" if fired else ""),
                     "level": lv})
    return level, deal, recs


def score_icb(d, A, sysd, members, pairs=None):
    w0, w1 = window(d)
    level, deal, recs = 0, 0, []
    pairs = pairs or set()
    for c in sysd.itertuples(index=False):
        mem = members.get(int(c.crisno), set())
        if pd.isna(c.trigdate) or pd.isna(c.termdate) or not (A & mem):
            continue
        if not (c.trigdate <= w1 and c.termdate >= w0):
            continue
        dy = any(set(p) <= mem for p in pairs)                       # A2.1: both members of a pair are crisis actors
        kind = "pair" if dy else "single"
        viol = int(c.viol) if pd.notna(c.viol) else None
        if w0 <= c.trigdate and c.termdate <= w1 and viol:
            lv, how, rule = VIOL_TO_LEVEL.get(viol, 1), "wholly inside W", f"ICB.{kind}.wholly"
        elif w0 <= c.trigdate <= w1:
            lv, how, rule = 1, f"triggered in W, ends after (onset dated -> 1; viol {viol} is the undated peak)", f"ICB.{kind}.onset"
        else:
            lv, how, rule = None, "ongoing at d, violence undated in W (no level)", f"ICB.{kind}.ongoing"
        forout = int(c.forout) if pd.notna(c.forout) else None
        fired = w0 <= c.termdate <= w1 and forout in (1, 2)
        deal = deal or int(fired)
        if lv is not None:
            level = max(level, lv)
        recs.append({"source": "icb", "basis": "dyadic" if dy else "location", "rule": rule,
                     "record": f"crisis {int(c.crisno)} {c.crisname}", "dates": f"{c.trigdate.date()}..{c.termdate.date()}",
                     "code": f"viol {viol} forout {forout} ({how})" + ("; agreement ends crisis in W -> DEAL" if fired else ""), "level": lv})
    return level, deal, recs


def score_ged(d, L, series):
    """A4.2 / A4.4. W = (d, d+90]; B = [d-90, d-1]; day d is in NEITHER and is reported on its own (deaths_ged_on_d).
    A GED level is a CONTINUATION when the same registered ladder already reached it over B -- the war was running
    at this level before the event, so the count in W asserts nothing new about the event. delta_level applies the
    same ladder to the increment and is a published diagnostic, never the G target (A4.4)."""
    w0, w1 = window(d)
    b0, b1 = pre_window(d)
    d = pd.Timestamp(d)
    d90 = ged_sum(series, L, w0, w1, "state")
    pre = ged_sum(series, L, b0, b1, "state")
    on_d = ged_sum(series, L, d, d, "state")
    other = ged_sum(series, L, w0, w1, "other")
    lv = ged_level(d90)
    delta = d90 - pre
    delta_lv = ged_level(max(0.0, delta))
    cont = lv > 0 and ged_level(pre) >= lv
    if cont:
        rule = "GED.location.continuation"
    elif lv == 3:
        rule = "GED.location.ge250"
    elif lv == 2:
        rule = "GED.location.ge25"
    else:
        rule = "NONE.covered"                                          # < 25 in W: a covering source with a dated view, nothing in it
    code = (f"best {d90:.0f} in W (B [{b0.date()}..{b1.date()}] {pre:.0f}; on d {on_d:.0f}; "
            f"delta {delta:+.0f} -> delta_level {delta_lv}; one-sided/non-state {other:.0f})")
    if cont:
        code += f"; B already at level {lv} -> undated-for-W (A4.2, no level)"
    recs = [{"source": "ged", "basis": "location", "rule": rule, "record": f"GED state-based deaths in {','.join(sorted(L))} (location, not dyad)",
             "dates": f"{w0.date()}..{w1.date()}", "code": code, "level": None if cont else lv}]
    deaths = {"deaths_ged_90": d90, "deaths_ged_pre90": pre, "deaths_ged_on_d": on_d,
              "deaths_ged_delta": delta, "deaths_ged_other_90": other}
    return (None if cont else lv), delta_lv, deaths, recs


def score_event(d, A, pairs, L, src):
    """All sources for one event. Returns the dict that becomes the ies90 rows."""
    out = {"levels": {}, "recs": [], "deal": None, "deaths": {}, "delta_level": None, "delta_basis": None}
    deal_seen = False
    if A and covers("midi", d):
        lv, recs = score_midi(d, A, pairs, src["midi"], src["midip"]); out["levels"]["midi"] = lv; out["recs"] += recs
    ci, cn = bool(A) and covers("war", d), bool(L) and covers("war_intra", d)
    if ci or cn:
        lv, recs = score_war(d, A, pairs, L, src["war"], ci, cn); out["levels"]["war"] = lv; out["recs"] += recs
    if A and covers("icb", d):
        lv, dl, recs = score_icb(d, A, src["icb"], src["icb_members"], pairs); out["levels"]["icb"] = lv; out["recs"] += recs
        deal_seen = True; out["deal"] = max(out["deal"] or 0, dl)
    if A and covers("mid", d):
        lv, dl, recs = score_mid(d, A, pairs, src["mid"]); out["levels"]["mid"] = lv; out["recs"] += recs
        deal_seen = True; out["deal"] = max(out["deal"] or 0, dl)
    if L and covers("ged", d):
        lv, delta_lv, deaths, recs = score_ged(d, L, src["ged"])
        out["levels"]["ged"] = lv; out["recs"] += recs; out["deaths"] = deaths
        out["delta_level"], out["delta_basis"] = delta_lv, "location"          # A4.4: a diagnostic, never the G target
    if not deal_seen:
        out["deal"] = None
    covering = [s for s in SOURCES if s in out["levels"]]
    out["covering"] = covering
    # A4.2: each covering source contributes its DATED level; None means it recorded something it could not place in W
    # (ongoing at d, or a continuation across the whole of B); 0 means it looked at W and found nothing.
    for sname in covering:
        srecs = [x for x in out["recs"] if x["source"] == sname]
        dated = [x for x in srecs if x["level"] is not None]
        out["levels"][sname] = max((x["level"] for x in dated), default=None if srecs else 0)
    # A2.1 dyadic precedence: a dyadic-capable source covering W with P non-empty decides; location evidence is kept beside it
    dy_cov = [s for s in covering if s in DYADIC_SOURCES and pairs and (s != "war" or covers("war", d))]
    out["covering_dyadic"], out["covering_location"] = dy_cov, [s for s in covering if s not in dy_cov]
    by_basis = lambda b: [x for x in out["recs"] if x.get("basis") == b]                       # noqa: E731
    dated = lambda rs: [x for x in rs if x["level"] is not None]                               # noqa: E731
    undated = lambda rs: [x for x in rs if x["level"] is None]                                 # noqa: E731
    loc, dy = by_basis("location"), by_basis("dyadic")
    # A4.2 rule 2 applied to the location reading too, so level_location is never a false zero either
    out["level_location"] = (max((x["level"] for x in dated(loc)), default=None if loc else 0)
                             if out["covering_location"] else None)
    chosen = dy if dy_cov else loc
    out["basis"] = ("dyadic" if dy_cov else "location") if covering else None
    out["ni_reason"] = None
    if not covering:                                        # A4.2 rule 4 -- unchanged
        out["level"], setters, out["ni_reason"] = None, [], "uncovered"
    elif dated(chosen):                                     # A4.2 rule 1 -- unchanged
        out["level"] = max(x["level"] for x in dated(chosen))
        setters = [x for x in dated(chosen) if x["level"] == out["level"]]
    elif undated(chosen):                                   # A4.2 rule 2 -- the ongoing/continuation exclusion
        out["level"], setters, out["ni_reason"] = None, [], "undated"
    else:                                                   # A4.2 rule 3 -- a true zero
        out["level"], setters = 0, []
    if out["level"] is None:
        out["level_source"] = []
        out["rule_fired"] = ["UNCOVERED"] if out["ni_reason"] == "uncovered" else ["UNDATED.continuation"]
    elif out["level"] == 0 and not setters:
        out["level_source"], out["rule_fired"] = list(dy_cov or covering), ["NONE.covered"]
    else:
        out["level_source"] = [s for s in SOURCES if any(x["source"] == s for x in setters)]
        out["rule_fired"] = sorted({x["rule"] for x in setters}, key=lambda r: [i for i, s in enumerate(SOURCES) if r.lower().startswith(s[:3])] or [9])
    return out


# ----------------------------------------------------------------------------- the run

def load_sources():
    sysd, members = O.load_icb()
    mid = dedupe_mid(O.load_mid())
    inc, parts = load_midi()
    war = load_war()
    ged, unmapped, n_ged, rng = load_ged()
    return {"icb": sysd, "icb_members": members, "mid": mid, "midi": inc, "midip": parts, "ged": ged, "war": war,
            "ged_unmapped": unmapped, "ged_n": n_ged, "ged_range": rng}


def run(conn, src=None, write=True):
    O.ensure_schema(conn)
    src = src or load_sources()
    ev, ents, roles = O._corpus(conn)
    ents_all = defaultdict(set)
    for eid, en in conn.execute("SELECT event_id, entity_id FROM event_entities"):
        ents_all[eid].add(en)
    prec = dict(conn.execute("SELECT event_id, date_precision FROM events"))
    ts = P.now()
    rows, results = [], {}
    for r in ev.itertuples(index=False):
        if r.type not in O.GEO_TYPES:
            continue
        A, pairs = O._actors_and_pairs(r, ents, roles)
        rr = roles.get(r.event_id, {})
        L = (set(rr.get("location", set())) | set(rr.get("target", set()))) or set(A)
        lit = {e: LITTORAL[e] for e in ents_all.get(r.event_id, set()) if e in LITTORAL}     # A2.2: location only
        for e, states in lit.items():
            L |= set(states)
        res = score_event(r.event_date, A, pairs, L, src)
        res["littoral"] = lit
        res.update({"type": r.type, "date": str(r.event_date.date()), "title": r.title, "url": r.source_url,
                    "ours": r.sr_outcome_90, "precision": prec.get(r.event_id) or "day", "A": sorted(A), "L": sorted(L)})
        results[r.event_id] = res
        detail = " | ".join(f"{x['source']}: {x['record']} {x['dates']} {x['code']}" for x in res["recs"]) or "no record in any covering source"
        if res["level"] is None:
            if res.get("ni_reason") == "undated":
                why = ("A4.2 rule 2: every record on the " + str(res["basis"]) + " basis is undated-for-W "
                       "(ongoing at d, or a continuation across the whole of B). The G target is not defined for "
                       "this event; it is excluded and counted, never scored 0. | " + detail)
            else:
                why = "no source covers (d, d+90]" if (A or res["L"]) else "no mapped country on the event"
            rows.append((r.event_id, "ies90", "no_independent_outcome", 1.0, None, why, ts))
            rows.append((r.event_id, "ies90", "rule_fired", None, ",".join(res["rule_fired"]),
                         "Amendment 4" if res.get("ni_reason") == "undated" else "Amendment 2", ts))
        else:
            rows.append((r.event_id, "ies90", "level", float(res["level"]), LEVEL_MEANING[res["level"]], detail, ts))
            rows.append((r.event_id, "ies90", "level_source", None, ",".join(res["level_source"]), detail, ts))
            rows.append((r.event_id, "ies90", "basis", None, res["basis"], "Amendment 2: dyadic precedence" if res["basis"] == "dyadic" else "Amendment 2: no dyadic-capable source covers W" + (" (littoral map: " + ",".join(sorted(lit)) + ")" if lit else ""), ts))
            rows.append((r.event_id, "ies90", "rule_fired", None, ",".join(res["rule_fired"]), "Amendment 2", ts))
            if res["level_location"] is not None:
                rows.append((r.event_id, "ies90", "level_location", float(res["level_location"]), None, "max over location-basis records (GED, COW intra-state, single-country matches)", ts))
        rows.append((r.event_id, "ies90", "covering", None, ",".join(res["covering"]) or None, f"date_precision {res['precision']}", ts))
        rows.append((r.event_id, "ies90", "covering_dyadic", None, ",".join(res["covering_dyadic"]) or None, "Amendment 2", ts))
        rows.append((r.event_id, "ies90", "covering_location", None, ",".join(res["covering_location"]) or None, "Amendment 2", ts))
        for s, lv in res["levels"].items():
            # A4.2: a null level_<source> is not a zero -- the source recorded something it could not date inside W
            rows.append((r.event_id, "ies90", f"level_{s}", None if lv is None else float(lv),
                         "undated-for-W" if lv is None else None,
                         " | ".join(f"{x['record']} {x['dates']} {x['code']}" for x in res["recs"] if x["source"] == s) or "none in W", ts))
        if res["deal"] is not None:
            rows.append((r.event_id, "ies90", "deal", float(res["deal"]), None, "ICB forout 1/2 termination or MID settlmnt 1 end in W", ts))
        for f, v in res["deaths"].items():
            rows.append((r.event_id, "ies90", f, float(v), None, "GED 26.1 state-based unless 'other'; location countries " + ",".join(res["L"])
                         + ("; W = (d, d+90]" if f in ("deaths_ged_90", "deaths_ged_other_90") else
                            "; B = [d-90, d-1], strictly before d (A4.4)" if f == "deaths_ged_pre90" else
                            "; day d only, in neither window (A4.4)" if f == "deaths_ged_on_d" else
                            "; D(W) - D(B) (A4.4)"), ts))
        if res.get("delta_level") is not None:
            # A4.4: a published diagnostic, NOT the G target. No score is computed against it under Amendment 4.
            rows.append((r.event_id, "ies90", "delta_level", float(res["delta_level"]), LEVEL_MEANING[res["delta_level"]],
                         "A4.4 diagnostic: the registered ladder applied to max(0, D(W) - D(B)); never the G target", ts))
            rows.append((r.event_id, "ies90", "delta_basis", None, res["delta_basis"], "A4.4: GED is a location source", ts))
    if write:
        conn.execute("DELETE FROM event_outcomes WHERE source = 'ies90'")
        conn.executemany("INSERT OR REPLACE INTO event_outcomes VALUES (?,?,?,?,?,?,?)", rows)
        conn.commit()
    return rows, results


def hostility_map(path=CLASS_AUDIT):
    """{event_id: (hostility, note)} from session F's CLASS_AUDIT.md per-class tables. The precondition is registered
    in OUTCOME_MAPPING.md Amendment 3 §A3.3 and the field is canon in EVENTS_CODEBOOK.md; this only reads it, so the
    audit sheet can tell Joe which rows the registered target would no longer score. Absent file -> {}."""
    p = Path(path)
    if not p.exists():
        return {}
    out, inside = {}, False
    for ln in p.read_text().splitlines():
        if re.match(r"^\|\s*event_id\s*\|\s*date\s*\|\s*hostility\s*\|", ln):
            inside = True
            continue
        if inside:
            if not ln.startswith("|"):
                inside = False
                continue
            if re.match(r"^\|[\s\-:|]+\|$", ln):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 3:
                eid = cells[0].strip("`").strip()
                raw = cells[2].strip().strip("*").strip("`").strip()
                base = raw.split("**")[0].split("·")[0].strip() or raw
                note = raw[len(base):].strip(" *·") if raw != base else ""
                if eid and base:
                    out[eid] = (base, note)
    return out


G_SCORABLE = {"hostile": "yes", "hostile_unattributed": "yes, flagged", "ambiguous": "contested", "non_hostile": "NO"}


def _decade(date):
    return date[:3] + "0s"


def distribution(results, src):
    lvl = lambda v: "null" if v["level"] is None else str(v["level"])  # noqa: E731
    by_dec, by_cls, deal_dec, noind_dec = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), Counter()
    cover = Counter(); cross = defaultdict(Counter); basis = defaultdict(Counter); rules = Counter(); lit = Counter()
    for v in results.values():
        basis[str(v.get("basis"))][lvl(v)] += 1
        for r in v.get("rule_fired", []):
            rules[r] += 1
        for e in (v.get("littoral") or {}):
            lit[e] += 1
        by_dec[_decade(v["date"])][lvl(v)] += 1
        by_cls[v["type"]][lvl(v)] += 1
        if v["deal"] is not None:
            deal_dec[_decade(v["date"])][str(v["deal"])] += 1
        if v["level"] is None:
            noind_dec[_decade(v["date"])] += 1
        for s in v["covering"]:
            cover[s] += 1
        cross[str(v["ours"])][lvl(v)] += 1
    n = len(results)
    return {"registration": REGISTRATION, "generated_at": P.now(), "window_days": WINDOW, "n_geopolitical_events": n,
            "levels": LEVEL_MEANING, "level_counts": dict(Counter(lvl(v) for v in results.values())),
            "by_decade": {k: dict(v) for k, v in sorted(by_dec.items())}, "by_class": {k: dict(v) for k, v in sorted(by_cls.items())},
            "deal_by_decade": {k: dict(v) for k, v in sorted(deal_dec.items())},
            "no_independent_outcome": {"total": sum(noind_dec.values()), "by_decade": dict(sorted(noind_dec.items()))},
            "coverage_events_by_source": dict(cover), "source_periods": COVER,
            "amendment_2": {"level_by_basis": {k: dict(v) for k, v in sorted(basis.items())}, "rule_fired": dict(sorted(rules.items())),
                            "littoral_events_by_entity": dict(lit), "littoral_map": {k: list(v) for k, v in LITTORAL.items()}},
            "cow_war": {"inter_participant_rows": len(src["war"]["inter"]), "intra_war_rows": len(src["war"]["intra"])},
            "ged": {"cache": str(GED_CACHE.relative_to(P.ROOT)), "n_events": src["ged_n"], "date_range": src["ged_range"],
                    "location_only": True, "unmapped_country_names": src["ged_unmapped"]},
            "for_the_record_only": {"note": "sr_outcome_90 is retired (Amendment 1); this table is not a score",
                                    "retired_sr_outcome_90_x_ies90": {k: dict(v) for k, v in sorted(cross.items())}}}


# ----------------------------------------------------------------------------- Amendment 4: before / after (A4.8)

# A4.5, written into the amendment BEFORE this code ran. Scored against the outcome below, right or wrong.
A4_PREDICTION = {"3": {"point": 15, "lo": 14, "hi": 24}, "2": {"point": 34, "lo": 30, "hi": 42},
                 "1": {"point": 6, "lo": 5, "hi": 8}, "0": {"point": 58, "lo": 55, "hi": 62},
                 "no_independent_outcome": {"point": 62, "lo": 50, "hi": 75},
                 "events_with_a_level": {"point": 122, "lo": 110, "hi": 135}}
CONTINUATION_RULES = ("WAR.inter.continuation", "WAR.intra.continuation", "GED.location.continuation",
                      "MIDI.continuation", "ICB.pair.ongoing", "ICB.single.ongoing", "MID.pair.ongoing", "MID.single.ongoing")


def _before(conn):
    """The ies90 labels as they stand in event_outcomes -- i.e. pre-Amendment-4. Read-only."""
    q = lambda f: dict(conn.execute("SELECT event_id, value FROM event_outcomes WHERE source='ies90' AND field=?", (f,)))  # noqa: E731
    qt = lambda f: dict(conn.execute("SELECT event_id, value_text FROM event_outcomes WHERE source='ies90' AND field=?", (f,)))  # noqa: E731
    lv, ni, srcs = q("level"), q("no_independent_outcome"), qt("level_source")
    out = {}
    for eid in set(lv) | set(ni):
        out[eid] = {"level": None if eid in ni else int(lv[eid]), "level_source": srcs.get(eid, "")}
    return out


def amendment4_counts(conn, results):
    """A4.8: the level distribution before and after Amendment 4, by level, source, rule, basis and decade, plus the
    continuation counts and the A4.5 prediction scored against the outcome. Computed from a write=False run: not one
    row of event_outcomes is touched (A4.6)."""
    before = _before(conn)
    lvl = lambda v: "no_independent_outcome" if v["level"] is None else str(v["level"])       # noqa: E731
    b_counts = Counter("no_independent_outcome" if v["level"] is None else str(v["level"]) for v in before.values())
    a_counts = Counter(lvl(v) for v in results.values())

    moved, cont_by_src, cont_by_rule = [], Counter(), Counter()
    for eid, v in sorted(results.items(), key=lambda kv: kv[1]["date"]):
        for x in v["recs"]:
            if x.get("rule") in CONTINUATION_RULES:
                cont_by_src[x["source"]] += 1
                cont_by_rule[x["rule"]] += 1
        b = before.get(eid)
        if b is None:
            continue
        if lvl(v) != ("no_independent_outcome" if b["level"] is None else str(b["level"])):
            moved.append({"event_id": eid, "date": v["date"], "class": v["type"], "title": v["title"],
                          "from": "no_independent_outcome" if b["level"] is None else b["level"],
                          "from_source": b["level_source"], "to": "no_independent_outcome" if v["level"] is None else v["level"],
                          "to_source": ",".join(v["level_source"]), "rule_fired": ",".join(v["rule_fired"]),
                          "reason": v.get("ni_reason"), "level_location": v.get("level_location"),
                          "delta_level": v.get("delta_level")})

    def split(sel):
        c = defaultdict(Counter)
        for v in results.values():
            c[sel(v)][lvl(v)] += 1
        return {k: dict(sorted(x.items())) for k, x in sorted(c.items(), key=lambda kv: str(kv[0]))}

    n_before_level = sum(v for k, v in b_counts.items() if k != "no_independent_outcome")
    n_after_level = sum(v for k, v in a_counts.items() if k != "no_independent_outcome")
    pred = {}
    for k, exp in A4_PREDICTION.items():
        got = n_after_level if k == "events_with_a_level" else a_counts.get(k, 0)
        pred[k] = {"predicted": exp["point"], "interval": [exp["lo"], exp["hi"]], "observed": got,
                   "inside_interval": exp["lo"] <= got <= exp["hi"], "error": got - exp["point"]}

    return {"registration": REGISTRATION, "amendment": "OUTCOME_MAPPING.md Amendment 4 (2026-09-02)",
            "generated_at": P.now(), "window_days": WINDOW,
            "not_written_to_db": "computed with ies90.run(conn, write=False); event_outcomes is unchanged (A4.6)",
            "not_retroactive": "published runs stand; this governs the next run (A4.7)",
            "n_geopolitical_events": len(results),
            "level_counts_before": dict(sorted(b_counts.items())), "level_counts_after": dict(sorted(a_counts.items())),
            "events_with_a_level": {"before": n_before_level, "after": n_after_level, "removed": n_before_level - n_after_level},
            "prediction_A4_5_scored": pred,
            "continuation_records_by_source": dict(sorted(cont_by_src.items())),
            "continuation_records_by_rule": dict(sorted(cont_by_rule.items())),
            "after_by_source": split(lambda v: ",".join(v["level_source"]) or "-"),
            "after_by_rule_fired": split(lambda v: ",".join(v["rule_fired"])),
            "after_by_basis": split(lambda v: str(v["basis"])),
            "after_by_class": split(lambda v: v["type"]),
            "after_by_decade": split(lambda v: _decade(v["date"])),
            "no_independent_outcome_reason": dict(sorted(Counter(v.get("ni_reason") or "-" for v in results.values() if v["level"] is None).items())),
            "delta_level_counts": dict(sorted(Counter(str(v.get("delta_level")) for v in results.values()).items())),
            "delta_level_note": "A4.4 diagnostic, never the G target; no score is computed against it under Amendment 4",
            "rows_changed": {"n": len(moved), "rows": moved}}


def audit_pick(results, n=30, seed=SEED):
    """30 events with a level, stratified by level x decade (largest remainder), seeded."""
    pool = [(e, v) for e, v in results.items() if v["level"] is not None]
    strata = defaultdict(list)
    for e, v in pool:
        strata[(v["level"], _decade(v["date"]))].append((e, v))
    rng = random.Random(seed)
    total = len(pool)
    if total <= n:
        pick = pool
    else:
        quota = {k: n * len(vs) / total for k, vs in strata.items()}
        base = {k: int(q) for k, q in quota.items()}
        rem = n - sum(base.values())
        for k in sorted(quota, key=lambda k: (quota[k] - base[k], str(k)), reverse=True)[:rem]:
            base[k] += 1
        pick = []
        for k in sorted(strata, key=str):
            vs = sorted(strata[k], key=lambda x: x[0]); rng.shuffle(vs)
            pick += vs[:base[k]]
    pick.sort(key=lambda x: (x[1]["date"], x[0]))
    return pick, total


AUDIT_COLS = ["row_type", "event_id", "event_date", "date_precision", "class", "hostility", "g_scorable", "hostility_note", "title", "source_url",
              "ies90_level", "ies90_level_meaning", "ies90_deal", "basis", "rule_fired", "level_source", "covering_dyadic", "covering_location",
              "countries_A", "location_L", "littoral_from", "src", "record_basis", "record_rule", "record", "record_dates", "code_and_rule",
              "level_contributed", "joe_check", "joe_note"]


def write_audit(pick, path=AUDIT_OUT, hostility=None):
    """The 30-row sheet. Every row carries session F's hostility coding (CLASS_AUDIT.md) so Joe can see which rows
    OUTCOME_MAPPING Amendment 3 would no longer score. The rows are NOT dropped: the published runs scored these
    labels, so the audit has to cover what was actually used."""
    hostility = hostility_map() if hostility is None else hostility
    path.parent.mkdir(parents=True, exist_ok=True)
    n_src = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(AUDIT_COLS)
        for e, v in pick:
            host, hnote = hostility.get(e, ("not_coded", "not in CLASS_AUDIT.md"))
            head = [e, v["date"], v["precision"], v["type"], host, G_SCORABLE.get(host, "?"), hnote, v["title"], v["url"], v["level"], LEVEL_MEANING[v["level"]],
                    "" if v["deal"] is None else v["deal"], v["basis"], ",".join(v["rule_fired"]), ",".join(v["level_source"]),
                    ",".join(v["covering_dyadic"]), ",".join(v["covering_location"]), ",".join(v["A"]), ",".join(v["L"]),
                    ";".join(f"{k}->{','.join(s)}" for k, s in sorted((v.get("littoral") or {}).items()))]
            w.writerow(["event"] + head + [""] * 9)
            recs = v["recs"] or [{"source": ",".join(v["covering"]), "basis": v["basis"], "rule": "NONE.covered", "record": "no record in W", "dates": "", "code": "level 0 asserted from coverage", "level": 0}]
            for x in recs:
                w.writerow(["source"] + head + [x["source"], x.get("basis", ""), x.get("rule") or "", x["record"], x["dates"], x["code"], "" if x["level"] is None else x["level"], "", ""])
                n_src += 1
    return len(pick), n_src


def main():
    """Default: rebuild the ies90 rows in event_outcomes. `--counts`: compute everything and write NOTHING to the
    database, publishing only data/state/ies90_amendment4_counts.json (A4.6 -- Session K does not move the target
    while another session holds an experiment open on it; the rebuild is a separate, announced step)."""
    counts_only = "--counts" in sys.argv
    src = load_sources()
    conn = sqlite3.connect(P.DB)
    try:
        rows, results = run(conn, src, write=not counts_only)
        if counts_only:
            a4 = amendment4_counts(conn, results)
            A4_OUT.parent.mkdir(parents=True, exist_ok=True)
            A4_OUT.write_text(json.dumps(a4, indent=1, default=str))
            print(f"Amendment 4, computed with write=False (event_outcomes untouched) -> {A4_OUT}")
            print(f"  before {a4['level_counts_before']}")
            print(f"  after  {a4['level_counts_after']}")
            print(f"  events with a level: {a4['events_with_a_level']}")
            print(f"  rows changed: {a4['rows_changed']['n']}; no_independent_outcome by reason {a4['no_independent_outcome_reason']}")
            print(f"  continuation records by rule: {a4['continuation_records_by_rule']}")
            print(f"  delta_level (A4.4 diagnostic): {a4['delta_level_counts']}")
            print("  A4.5 prediction, scored:")
            for k, v in a4["prediction_A4_5_scored"].items():
                print(f"    {k:<24} predicted {v['predicted']:>4} {str(v['interval']):<12} observed {v['observed']:>4}"
                      f"  {'INSIDE' if v['inside_interval'] else 'OUTSIDE'} (err {v['error']:+d})")
            return
    finally:
        conn.close()
    dist = distribution(results, src)
    pick, total = audit_pick(results)
    n_ev, n_src = write_audit(pick)
    dist["audit"] = {"file": str(AUDIT_OUT.relative_to(P.ROOT)), "events": n_ev, "source_rows": n_src, "pool_with_level": total, "seed": SEED,
                     "strata": "level x decade, largest remainder"}
    DIST_OUT.write_text(json.dumps(dist, indent=1, default=str))
    print(f"ies90: {len(rows)} rows for {len(results)} geopolitical events; levels {dist['level_counts']}; "
          f"no_independent_outcome {dist['no_independent_outcome']['total']}; coverage {dist['coverage_events_by_source']}")
    for dec, c in dist["by_decade"].items():
        print(f"  {dec}: {dict(sorted(c.items()))}")
    print(f"  GED unmapped names: {len(src['ged_unmapped'])}; audit: {n_ev} events / {n_src} source rows -> {AUDIT_OUT}")


if __name__ == "__main__":
    main()
