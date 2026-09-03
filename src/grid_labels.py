"""grid_labels.py -- G-4: the dyad-date escalation panel, and the probe that decides whether it is worth building.

Registered first, in data/grid/G4_REGISTRATION.md (2026-09-03). Read that file before this one; every
rule below names the clause it implements.

The idea. The corpus has 313 events and the power block wants ~1,200 reads. G-1 and G-2 closed the
backward route (admitting six pre-1974 records buys zero scored reads). The remaining route is
density: make the unit of observation a DYAD-DATE, not an event. The IES-90 labels were never limited
to our events -- COW MID, COW War, ICB and UCDP GED cover every dyad and every date they reach.

What this file does NOT do. It does not build the full 1987-2026 panel. Registration §5 says the probe
is published and read first, and §5.1 fixes the degeneracy test before the numbers. It opens oil.db
read-only and writes no table. It does not touch src/walk*.py or data/walk_forward/** (B's, this
session).

The scorer is src/state/ies90.score_event, reused UNCHANGED. It already carries OUTCOME_MAPPING
Amendment 4 across COW War and GED, so the ongoing-conflict defect the brief warns about is not
inherited: a record that already covered the whole of the pre-window asserts nothing new about the
window and contributes NO level, rather than a false zero.

Run:  python3 src/grid_labels.py            the registered probe (1998, 2018, 2024)
Out:  data/grid/g/PROBE.json, data/grid/g/PROBE.md
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "state"))

import ies90 as I          # noqa: E402  the scorer, reused unchanged
import countries as C      # noqa: E402
from engine.pre1987_candidates import STATES  # noqa: E402  the registered producer/transit roles

OUT_JSON = ROOT / "data" / "grid" / "g" / "PROBE.json"
OUT_MD = ROOT / "data" / "grid" / "g" / "PROBE.md"
RAW = ROOT / "data" / "state" / "raw"

# ---- §1 the grid ------------------------------------------------------------------------------
PROBE_YEARS = (1998, 2018, 2024)          # §5, registered for their coverage regime
ACT_LOOKBACK_DAYS = 1825                  # §2 clause 2: five calendar years
ACT_SENSITIVITY = (365, 730, 1825, 3652)  # §2.1, pre-declared; five years stays primary
DEGENERATE_SHARE = 0.95                   # §5.1

# ---- §4.1 release dates, read from the tree's .meta.json sidecars, never from memory ----------
RELEASE_FILES = {
    "war": ("cow_war", "Inter-StateWarData_v4.0.csv.meta.json"),
    "war_intra": ("cow_war", "Intra-StateWarData_v4.1.csv.meta.json"),
    "midi": ("cow_mid", "MID-5-Data-and-Supporting-Materials.zip.meta.json"),
    "mid": ("cow_mid", "dyadic_mid_4.03_update.zip.meta.json"),
    "icb": ("icb", "icb_dyads_v16.csv.meta.json"),
    "ged": (None, None),                  # cached JSON, no sidecar
}


def release_dates():
    """§4.1. Last-Modified per dataset where the tree records one; else None. No date is guessed."""
    out = {}
    for src, (d, f) in RELEASE_FILES.items():
        iso, how = None, "no sidecar in the tree"
        if d:
            p = RAW / d / f
            if p.exists():
                lm = (json.loads(p.read_text()) or {}).get("last_modified")
                if lm:
                    iso = pd.Timestamp(lm).tz_localize(None).date().isoformat()
                    how = f"HTTP Last-Modified of {d}/{f.replace('.meta.json', '')}"
                else:
                    how = f"{d}/{f.replace('.meta.json', '')}: host serves no Last-Modified"
        out[src] = {"release": iso, "how": how}
    # §4.1: where unknown, a LOWER bound on release = coverage end + 1 day, which gives an UPPER
    # bound on VR-1 survival. Labelled, never presented as the release date.
    for src, v in out.items():
        cov_hi = I.COVER[src][1]
        lb = (dt.date.fromisoformat(cov_hi) + dt.timedelta(days=1)).isoformat()
        v["release_lower_bound"] = v["release"] or lb
        v["bounded"] = v["release"] is None
    return out


# ---- §2 the entity and dyad universe ----------------------------------------------------------

def oil_relevant():
    """§2 clause 1: register entities whose STATES role contains producer or transit."""
    out = {}
    for cc, (name, roles) in STATES.items():
        e = C.from_ccode(cc)
        if e and e in C.ALL and ("producer" in roles or "transit" in roles):
            out.setdefault(e, set()).update(r for r in roles.split(",") if r in ("producer", "transit"))
    return out


def all_oil_dyads(ents):
    es = sorted(ents)
    return [frozenset((a, b)) for i, a in enumerate(es) for b in es[i + 1:]]


# ---- §2 clause 2: dated dyadic records, from the four dyadic-capable sources -------------------

def dyadic_spells(src):
    """{frozenset(pair): [(start, end, source), ...]} from MIDI, COW inter-state War, ICB and dyadic
    MID. GED is excluded by §2: the cache has no dyad field and cannot say two states clashed."""
    out = defaultdict(list)

    # dyadic MID 4.03 -- one row per (dispute, dyad), already deduped by ies90.dedupe_mid
    mid = src["mid"]
    for r in mid.itertuples(index=False):
        end = r.end if pd.notna(r.end) else r.start
        if pd.notna(r.start):
            out[r.pair].append((r.start, max(end, r.start), "mid"))

    # MIDI 5.0 incidents -- participants on opposite sides
    inc, parts = src["midi"], src["midip"]
    for r in inc.itertuples(index=False):
        ps = parts.get(int(r.incidnum), [])
        side = {}
        for e, s in ps:
            side.setdefault(e, s)
        es = sorted(side)
        for i, a in enumerate(es):
            for b in es[i + 1:]:
                if side[a] != side[b]:
                    out[frozenset((a, b))].append((r.start, r.end, "midi"))

    # COW inter-state War v4.0 -- participants on opposite sides, per war
    by_war = defaultdict(list)
    for p in src["war"]["inter"]:
        by_war[p["war"]].append(p)
    for wn, ps in by_war.items():
        side = {p["ent"]: p["side"] for p in ps}
        spells = [sp for pp in ps for sp in pp["spells"]]
        if not spells:
            continue
        lo, hi = min(s for s, _ in spells), max(e for _, e in spells)
        es = sorted(side)
        for i, a in enumerate(es):
            for b in es[i + 1:]:
                if side[a] != side[b]:
                    out[frozenset((a, b))].append((lo, hi, "war"))

    # ICB v16 -- both states are actors in the same crisis
    sysd, members = src["icb"], src["icb_members"]
    for c in sysd.itertuples(index=False):
        mem = sorted(members.get(int(c.crisno), set()))
        if pd.isna(c.trigdate) or pd.isna(c.termdate):
            continue
        for i, a in enumerate(mem):
            for b in mem[i + 1:]:
                out[frozenset((a, b))].append((c.trigdate, c.termdate, "icb"))
    return out


def active_at(t, spells, dyads, lookback=ACT_LOOKBACK_DAYS, vr3=False):
    """§2 clause 2 (and §4 VR-3). A dyad is active at t when some dyadic record's spell intersects
    A_w = [t - lookback, t - 1]. Under vr3 only records whose spell ENDS strictly before t count --
    a dyad admitted on a record still running at t is a dyad selected on the future."""
    t = pd.Timestamp(t)
    lo, hi = t - pd.Timedelta(days=lookback), t - pd.Timedelta(days=1)
    out = []
    for p in dyads:
        for st, en, _s in spells.get(p, ()):
            if st <= hi and en >= lo and (not vr3 or en < t):
                out.append(p)
                break
    return out


# ---- §4 the vintage stamp ---------------------------------------------------------------------

# A1.2: what each rule's level rests on, and therefore when it became knowable
ONSET_RULES = ("MID.pair.onset", "MID.single.onset", "ICB.pair.onset", "ICB.single.onset")
WAR_RULES = ("WAR.inter.pair", "WAR.inter.single", "WAR.intra.location")
WINDOW_RULES = ("GED.location.ge25", "GED.location.ge250", "NONE.covered")


def _span(rec):
    """(start, end) of a record's dated span, from its `dates` string. Multiple spans -> outer hull."""
    ds = str(rec.get("dates") or "")
    lo = hi = None
    for part in ds.replace(";", " ").split():
        if ".." not in part:
            continue
        a, b = part.split("..", 1)
        try:
            a, b = dt.date.fromisoformat(a[:10]), dt.date.fromisoformat(b[:10])
        except ValueError:
            continue
        lo = a if lo is None or a < lo else lo
        hi = b if hi is None or b > hi else hi
    return lo, hi


def stamp(rec, win_lo, win_hi):
    """A1.2: the date a record's level became knowable, by the rule that fired. None when undatable."""
    lo, hi = _span(rec)
    r = rec.get("rule") or ""
    if r in WINDOW_RULES or r.startswith("GED"):
        return win_hi + dt.timedelta(days=1)
    if r in ONSET_RULES:
        return (lo + dt.timedelta(days=1)) if lo else None
    if r in WAR_RULES or r.startswith("WAR"):
        return (max(lo, win_lo) + dt.timedelta(days=1)) if lo else None
    return (hi + dt.timedelta(days=1)) if hi else None          # .wholly, MIDI overlap, anything else


def cell_vintage(res, win_lo, win_hi):
    """VR-2 (§4, session A's WORLD_STATE_CODEBOOK Amendment 1), as corrected by Amendment 1.

    A1.1: only the records on the cell's CHOSEN basis whose level equals the chosen level -- the
    setters -- are stamped. A record on the other basis, or one that did not set the level, says
    nothing about when the level became knowable. A level-0 cell with no setter (a covering source
    that looked and found nothing) is stamped at the window's own close.
    Returns (vintage|None, [(rule, stamp)])."""
    win_lo, win_hi = pd.Timestamp(win_lo).date(), pd.Timestamp(win_hi).date()
    if res.get("level") is None:
        return None, []                                          # undated or uncovered: nothing to stamp
    basis = res.get("basis")
    recs = [r for r in res["recs"] if r.get("basis") == basis]
    setters = [r for r in recs if r.get("level") is not None and r["level"] == res["level"]]
    if not setters:                                              # A1.1 / A1.3: a true zero, no record
        return (win_hi + dt.timedelta(days=1)).isoformat(), [("NONE.covered", (win_hi + dt.timedelta(days=1)).isoformat())]
    got = []
    for r in setters:
        st = stamp(r, win_lo, win_hi)
        if st:
            got.append((r.get("rule"), st))
    if not got:
        return None, []
    vin = max(st for _r, st in got)                              # every setter must be knowable
    return vin.isoformat(), [(r, st.isoformat()) for r, st in got]


def vr1_ok(res, t, rel):
    """VR-1 (§4, strict). Every source the level rests on must have release <= t. Unknown releases
    use the coverage-end lower bound, which makes this an UPPER bound on survival. A1.1: the sources
    counted are the setters on the chosen basis, the same set VR-2 stamps."""
    if res.get("level") is None:
        return False, []
    basis = res.get("basis")
    srcs = {r["source"] for r in res["recs"]
            if r.get("basis") == basis and r.get("level") is not None and r["level"] == res["level"]}
    if not srcs:                                                  # a true zero rests on the covering sources
        srcs = set(res.get("covering") or [])
    if not srcs:
        return False, sorted(srcs)
    t = str(t)[:10]
    for s in srcs:
        key = s if s in rel else ("war" if s == "war" else s)
        r = rel.get(key, {}).get("release_lower_bound")
        if r is None or r > t:
            return False, sorted(srcs)
    return True, sorted(srcs)


# ---- the probe --------------------------------------------------------------------------------

def month_ends(year):
    return [d.date().isoformat() for d in pd.date_range(f"{year}-01-31", f"{year}-12-31", freq="ME")]


def covering_sources(t):
    return sorted(s for s in ("midi", "war", "war_intra", "icb", "mid", "ged") if I.covers(s, t))


def probe_year(year, src, spells, oil, rel, verbose=True, opposed=None):
    opposed = opposed if opposed is not None else opposed_pairs(spells)
    dyads_all = all_oil_dyads(oil)
    grid = month_ends(year)
    per_date, cells = [], []
    for t in grid:
        act = active_at(t, spells, dyads_all)
        act_vr3 = active_at(t, spells, dyads_all, vr3=True)
        sens = {str(k): len(active_at(t, spells, dyads_all, lookback=k)) for k in ACT_SENSITIVITY}
        per_date.append({"date": t, "n_active": len(act), "n_active_vr3": len(act_vr3),
                         "n_oil_dyads": len(dyads_all), "sensitivity": sens,
                         "covering_sources": covering_sources(t)})
        act_vr3_set = set(act_vr3)
        for p in act:
            a, b = sorted(p)
            A, pairs, L = {a, b}, {p}, {a, b}
            fwd = I.score_event(t, A, pairs, L, src)                                   # L over (t, t+90]
            pre_d = (pd.Timestamp(t) - pd.Timedelta(days=91)).date().isoformat()
            pre = I.score_event(pre_d, A, pairs, L, src)                               # L- over [t-90, t-1]
            b0, b1 = I.pre_window(t)                                                   # [t-90, t-1]
            vin, stamps = cell_vintage(pre, b0, b1)                                    # VR-2 on the FEATURE
            v1, v1s = vr1_ok(pre, t, rel)
            d_ies = (None if (fwd["level"] is None or pre["level"] is None)
                     else fwd["level"] - pre["level"])
            rules = set(fwd_rules := sorted(setter_rules(fwd))) | set(setter_rules(pre))
            cells.append({
                "date": t, "dyad": f"{a}|{b}",
                "L": fwd["level"], "L_ni": fwd.get("ni_reason"), "L_basis": fwd.get("basis"),
                "L_rules": fwd_rules,
                "Lpre": pre["level"], "Lpre_ni": pre.get("ni_reason"), "dIES": d_ies,
                "covering": fwd.get("covering") or [],
                "vr2_vintage": vin, "vr2_ok": bool(vin) and vin <= t, "vr2_stamps": stamps,
                "Lpre_rules": sorted({r.get("rule") for r in pre["recs"]
                                      if r.get("basis") == pre.get("basis") and r.get("level") is not None
                                      and r["level"] == pre["level"]}),
                "label_available_at": (pd.Timestamp(t) + pd.Timedelta(days=91)).date().isoformat(),  # A1.4
                "vr1_ok": v1, "vr1_sources": v1s,
                "vr3_active": p in act_vr3_set,
                "retrospective": 1,                                                    # §4.2, every cell
                "evidence_basis": (evidence_basis(rules, p, opposed) if d_ies not in (None, 0) else None),
                "L_evidence": (Lev := evidence_class_of(fwd, p, opposed)),                 # A3.3
                "Lpre_evidence": (Pev := evidence_class_of(pre, p, opposed)),
                "evidence_class": weaker(Lev, Pev),
                "L_setter_records": sorted({r["record"] for r in fwd["recs"]
                                            if r.get("basis") == fwd.get("basis")
                                            and r.get("level") is not None and r["level"] == fwd["level"]}),
            })
        if verbose:
            print(f"  {t}  active {len(act):>4}  (VR-3 {len(act_vr3):>4})  covering {','.join(covering_sources(t)) or 'NONE'}", flush=True)
    return per_date, cells


def summarise_year(year, per_date, cells):
    nL = [c for c in cells if c["L"] is not None]
    nP = [c for c in cells if c["Lpre"] is not None]
    nD = [c for c in cells if c["dIES"] is not None]
    L_dist = Counter(c["L"] for c in nL)
    P_dist = Counter(c["Lpre"] for c in nP)
    D_dist = Counter(c["dIES"] for c in nD)
    ni = Counter()
    for c in cells:
        if c["L"] is None:
            ni["L:" + (c["L_ni"] or "none")] += 1
        if c["Lpre"] is None:
            ni["Lpre:" + (c["Lpre_ni"] or "none")] += 1
    n = len(cells)
    share = lambda k, tot: (round(k / tot, 4) if tot else None)          # noqa: E731
    act = [d["n_active"] for d in per_date]
    return {
        "year": year, "grid_dates": len(per_date), "n_cells": n,
        "active_per_date": {"min": min(act) if act else 0, "max": max(act) if act else 0,
                            "mean": round(sum(act) / len(act), 1) if act else 0},
        "active_per_date_vr3": {"min": min(d["n_active_vr3"] for d in per_date) if per_date else 0,
                                "max": max(d["n_active_vr3"] for d in per_date) if per_date else 0},
        "n_oil_dyads_all": per_date[0]["n_oil_dyads"] if per_date else 0,
        "sensitivity_mean": {str(k): round(sum(d["sensitivity"][str(k)] for d in per_date) / max(len(per_date), 1), 1)
                             for k in ACT_SENSITIVITY},
        "L": {"n_defined": len(nL), "share_defined": share(len(nL), n),
              "dist": {str(k): v for k, v in sorted(L_dist.items())},
              "share_zero": share(L_dist.get(0, 0), len(nL))},
        "Lpre": {"n_defined": len(nP), "share_defined": share(len(nP), n),
                 "dist": {str(k): v for k, v in sorted(P_dist.items())},
                 "share_zero": share(P_dist.get(0, 0), len(nP))},
        "dIES": {"n_defined": len(nD), "share_defined": share(len(nD), n),
                 "dist": {str(k): v for k, v in sorted(D_dist.items())},
                 "share_zero": share(D_dist.get(0, 0), len(nD))},
        "no_independent_outcome": dict(ni),
        "vintage": {
            "VR1_strict_release": {"n": sum(1 for c in cells if c["vr1_ok"]), "share": share(sum(1 for c in cells if c["vr1_ok"]), n),
                                   "note": "upper bound: unknown releases use coverage_end + 1 day (§4.1)"},
            "VR2_event_knowability": {"n": sum(1 for c in cells if c["vr2_ok"]), "share": share(sum(1 for c in cells if c["vr2_ok"]), n),
                                      "note": "session A's registered convention (WORLD_STATE_CODEBOOK Amendment 1)"},
            "VR3_selection": {"n_cells_from_vr3_active": sum(1 for c in cells if c["vr3_active"]),
                              "share": share(sum(1 for c in cells if c["vr3_active"]), n),
                              "note": "dyads admitted only on records whose spell ends strictly before t"},
            "retrospective_share": 1.0,
            "VR2_breakdown": dict(Counter(
                ("knowable at t" if c["vr2_ok"] else
                 ("stamped after t" if c["vr2_vintage"] else
                  ("no level to stamp (%s)" % (c["Lpre_ni"] or "none")))) for c in cells)),
        },
        "evidence_basis_of_nonzero_dIES": dict(Counter(
            c["evidence_basis"] for c in cells if c["evidence_basis"])),
        "n_nonzero_dIES": sum(1 for c in cells if c["dIES"] not in (None, 0)),
        "n_distinct_dyads_nonzero": len({c["dyad"] for c in cells if c["dIES"] not in (None, 0)}),
        "covering_mix": {",".join(d["covering_sources"]) or "NONE": 0 for d in per_date} | dict(
            Counter(",".join(d["covering_sources"]) or "NONE" for d in per_date)),
    }


# ---- Amendment 2: the evidence-basis diagnostic (gates nothing) --------------------------------
SIDED_SOURCES = ("MID", "MIDI", "WAR")          # the three rule families that record which side a state was on


def setter_rules(res):
    """The rules that actually set this cell's level, on its chosen basis (Amendment 1 A1.1)."""
    if res.get("level") is None:
        return set()
    b = res.get("basis")
    return {r.get("rule") for r in res["recs"]
            if r.get("basis") == b and r.get("level") is not None and r["level"] == res["level"]}


def evidence_basis(rules, pair, opposed_pairs):
    """Amendment 2: which of the three buckets a non-zero cell's evidence falls in."""
    if any(str(r).startswith(SIDED_SOURCES) for r in rules):
        return "opposed-side evidence (MID / MIDI / COW War)"
    if any(str(r).startswith("GED") for r in rules):
        return "GED location count only (not a statement about the pair)"
    if any(str(r).startswith("ICB") for r in rules):
        return ("ICB co-actor only (may be allies)" if pair in opposed_pairs
                else "ICB co-actor only, pair NEVER opposed in MID/MIDI/COW")
    return "other"


# ---- A3.3: the evidence class as a FIELD on every cell, on a total order -----------------------
# strongest to weakest. `evidence_class` of a cell is the WEAKER of its two ends.
EVIDENCE_ORDER = ("opposed_side", "icb_co_actor", "icb_co_actor_never_opposed", "ged_location", "undefined")
SIDED_LABEL_SOURCES = ("mid", "midi", "war")          # ies90 source ids that record which side a state was on


def evidence_class_of(res, pair, opposed):
    """A3.3. Which class the evidence at ONE end (L or L-) falls in. A true zero is classified by the
    sources that were COVERING on the chosen basis -- a sided source that looked and found nothing is a
    statement about the pair; GED finding no deaths is not."""
    if res.get("level") is None:
        return "undefined"
    rules = setter_rules(res)
    if rules:
        if any(str(r).startswith(SIDED_SOURCES) for r in rules):
            return "opposed_side"
        if any(str(r).startswith("ICB") for r in rules):
            return "icb_co_actor" if pair in opposed else "icb_co_actor_never_opposed"
        if any(str(r).startswith("GED") for r in rules):
            return "ged_location"
        return "ged_location"
    # a true zero: no setter. Classify by what was covering on the chosen basis.
    cov = set(res.get("covering_dyadic") or []) if res.get("basis") == "dyadic" else set(res.get("covering") or [])
    cov = cov or set(res.get("covering") or [])
    if cov & set(SIDED_LABEL_SOURCES):
        return "opposed_side"
    if "icb" in cov:
        return "icb_co_actor" if pair in opposed else "icb_co_actor_never_opposed"
    return "ged_location"


def weaker(a, b):
    return a if EVIDENCE_ORDER.index(a) >= EVIDENCE_ORDER.index(b) else b


def opposed_pairs(spells):
    """Pairs a sided source records as opponents, anywhere in its coverage."""
    return {p for p, v in spells.items() if any(s in ("mid", "midi", "war") for _a, _b, s in v)}


# ---- §5.1 the degeneracy test, fixed before the numbers ---------------------------------------

def verdict(s1998):
    """§5.1: DEGENERATE if >= 95% of cells with a defined dIES are 0, or >= 95% of cells with a
    defined L are 0, on the 1998 probe."""
    dz = s1998["dIES"]["share_zero"]
    lz = s1998["L"]["share_zero"]
    hit = [k for k, v in (("dIES", dz), ("L", lz)) if v is not None and v >= DEGENERATE_SHARE]
    return {"degenerate": bool(hit), "on": hit, "share_zero_dIES": dz, "share_zero_L": lz,
            "threshold": DEGENERATE_SHARE,
            "rule": "G4_REGISTRATION §5.1, fixed before the numbers were computed"}


def to_md(out):
    L = []
    a = L.append
    a("# G-4 probe — the dyad-date escalation panel, three years, before anything is built")
    a("*Computed by `src/grid_labels.py` under `data/grid/G4_REGISTRATION.md`, which was committed first.*")
    a(f"*Generated {out['generated_at']}. The full panel is NOT built: registration §5 gates it on this file.*\n")

    a("## 0. The answer, in three numbers\n")
    v = out["verdict"]
    y = out["years"]["1998"]
    a(f"- **Active dyad-dates per grid date (1998, R-ACT):** {y['active_per_date']['min']}–"
      f"{y['active_per_date']['max']} (mean {y['active_per_date']['mean']}) out of "
      f"{y['n_oil_dyads_all']} oil-relevant dyads.")
    a(f"- **Degeneracy (§5.1):** {'**DEGENERATE**' if v['degenerate'] else 'not degenerate'}"
      f" — ΔIES zero share {v['share_zero_dIES']}, L zero share {v['share_zero_L']}, threshold {v['threshold']}.")
    vv = y["vintage"]
    a(f"- **Cells surviving the vintage stamp (1998):** VR-1 strict **{vv['VR1_strict_release']['n']}** "
      f"({vv['VR1_strict_release']['share']}) · VR-2 registered convention **{vv['VR2_event_knowability']['n']}** "
      f"({vv['VR2_event_knowability']['share']}) · VR-3 selection **{vv['VR3_selection']['n_cells_from_vr3_active']}** "
      f"({vv['VR3_selection']['share']}). Every cell is `retrospective = 1`.\n")

    a("## 1. Active set, by probe year\n")
    a("| year | grid dates | oil dyads | active/date (min–max, mean) | VR-3 active/date | cells |")
    a("|---|---|---|---|---|---|")
    for yr, s in out["years"].items():
        a(f"| {yr} | {s['grid_dates']} | {s['n_oil_dyads_all']} | {s['active_per_date']['min']}–"
          f"{s['active_per_date']['max']} ({s['active_per_date']['mean']}) | "
          f"{s['active_per_date_vr3']['min']}–{s['active_per_date_vr3']['max']} | {s['n_cells']} |")
    a("\n**Lookback sensitivity** (§2.1, pre-declared; five years stays primary) — mean active dyads per grid date:\n")
    a("| year | 1 y | 2 y | 5 y (primary) | 10 y | R-ACT-0 (no recency) |")
    a("|---|---|---|---|---|---|")
    for yr, s in out["years"].items():
        m = s["sensitivity_mean"]
        a(f"| {yr} | {m['365']} | {m['730']} | **{m['1825']}** | {m['3652']} | {s['n_oil_dyads_all']} |")

    a("\n## 2. The marginal distributions\n")
    for yr, s in out["years"].items():
        a(f"### {yr}\n")
        a(f"- cells: **{s['n_cells']}** · L defined on {s['L']['n_defined']} ({s['L']['share_defined']}) · "
          f"L⁻ defined on {s['Lpre']['n_defined']} ({s['Lpre']['share_defined']}) · "
          f"ΔIES defined on {s['dIES']['n_defined']} ({s['dIES']['share_defined']})")
        a(f"- **L**: {json.dumps(s['L']['dist'])} — share zero **{s['L']['share_zero']}**")
        a(f"- **L⁻**: {json.dumps(s['Lpre']['dist'])} — share zero {s['Lpre']['share_zero']}")
        a(f"- **ΔIES**: {json.dumps(s['dIES']['dist'])} — share zero **{s['dIES']['share_zero']}**")
        if s["no_independent_outcome"]:
            a(f"- undefined, by reason: {json.dumps(s['no_independent_outcome'])}")
        a("")

    a("## 3. Covering-source mix per grid date (§3, the regime table)\n")
    a("| year | mix (grid dates) |")
    a("|---|---|")
    for yr, s in out["years"].items():
        a(f"| {yr} | " + " · ".join(f"`{k}` ×{n}" for k, n in sorted(s["covering_mix"].items()) if n) + " |")

    a("\n## 4. The vintage stamp\n")
    a("| year | cells | VR-1 strict (release ≤ t) | VR-2 event knowability | VR-3 selection knowable |")
    a("|---|---|---|---|---|")
    for yr, s in out["years"].items():
        vv = s["vintage"]
        a(f"| {yr} | {s['n_cells']} | {vv['VR1_strict_release']['n']} ({vv['VR1_strict_release']['share']}) | "
          f"{vv['VR2_event_knowability']['n']} ({vv['VR2_event_knowability']['share']}) | "
          f"{vv['VR3_selection']['n_cells_from_vr3_active']} ({vv['VR3_selection']['share']}) |")
    a("\n**Release dates, read from the tree's `.meta.json` sidecars (§4.1), never from memory:**\n")
    a("| source | release | how | lower bound used by VR-1 |")
    a("|---|---|---|---|")
    for s, r in out["releases"].items():
        a(f"| `{s}` | {r['release'] or '**unknown**'} | {r['how']} | {r['release_lower_bound']}"
          f"{' (bound, not a release date)' if r['bounded'] else ''} |")
    a("\nVR-1 uses a **lower bound** on release where the host serves none, which makes its count an "
      "**upper bound** on survival: the most favourable number consistent with the evidence.\n")
    a("**Every cell carries `retrospective = 1`** (§4.2). A COW hostility level, an ICB violence code "
      "and a UCDP death estimate are later constructions, not contemporaneous records. "
      "`WORLD_STATE_CODEBOOK.md` Amendment 1: *a retrospective field alone can never make a read "
      "VALIDATED.* That is a property of the sources, not of `n`, and density does not change it.\n")

    a("## 5. What the non-zero cells actually rest on (Amendment 2 — a diagnostic; gates nothing)\n")
    a("| year | non-zero ΔIES cells | distinct dyads | evidence basis |")
    a("|---|---|---|---|")
    for yr, s_ in out["years"].items():
        eb = " · ".join(f"**{n}** {k}" for k, n in sorted(s_["evidence_basis_of_nonzero_dIES"].items(), key=lambda kv: -kv[1]))
        a(f"| {yr} | {s_['n_nonzero_dIES']} | {s_['n_distinct_dyads_nonzero']} | {eb or '—'} |")
    a("\nOnly the first bucket is evidence *about the dyad*. MID, MIDI and COW War are the three sources")
    a("that record which side a state was on, and they stop covering the grid at **2014-10-02**. After that")
    a("date the panel has no sided source at all, so a dyad-date label cannot distinguish an ally from an")
    a("adversary, and a location death-count is replicated across every dyad containing that country.\n")

    a("## 6. Verdict under the registered test (§5.1)\n")
    a(f"```\n{json.dumps(v, indent=1)}\n```")
    return "\n".join(L)


def main():
    print("loading sources ...", flush=True)
    src = I.load_sources()
    oil = oil_relevant()
    spells = dyadic_spells(src)
    rel = release_dates()
    print(f"oil-relevant entities {len(oil)}; dyads with >=1 dated dyadic record {len(spells)}", flush=True)
    years, raw, allcells = {}, {}, {}
    for yr in PROBE_YEARS:
        print(f"probe {yr}:", flush=True)
        per_date, cells = probe_year(yr, src, spells, oil, rel)
        years[str(yr)] = summarise_year(yr, per_date, cells)
        raw[str(yr)] = {"per_date": per_date, "n_cells": len(cells)}
        allcells[str(yr)] = cells                                        # A1.6: every cell, checkable
    out = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "registration": "data/grid/G4_REGISTRATION.md (2026-09-03)",
           "oil_relevant_entities": sorted(oil), "n_oil_relevant_entities": len(oil),
           "releases": rel, "years": years, "per_date": raw, "cells": allcells,
           "verdict": verdict(years["1998"])}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=1, default=str))
    OUT_MD.write_text(to_md(out))
    print(json.dumps({"verdict": out["verdict"],
                      "years": {y: {k: s[k] for k in ("n_cells", "active_per_date", "L", "dIES", "vintage")}
                                for y, s in years.items()}}, indent=1, default=str))
    return out


# (entrypoint dispatch is at the foot of the file)


# ================================================================================================
# A3 — THE BUILD. Registered in G4_REGISTRATION Amendment 3 before this code was written.
# Span 1987-01-31 .. 2014-09-30 (333 month-ends), VR-3 active set, evidence basis as a FIELD.
# Nothing is filtered out of the panel; the strict subset is a selection on `evidence_class`.
# ================================================================================================

PANEL_START, PANEL_END = "1987-01-31", "2014-09-30"      # A3.1: the last month-end with t+90 <= 2014-12-31
PANEL_DIR = ROOT / "data" / "grid" / "g"
LIMITS = [
    "1. It never reaches the present. The panel ends 2014-09-30 because its last sided source does "
    "(MID / MIDI / COW intra-state War end 2014-12-31 and ies90.covers needs t+90 <= that). No number "
    "computed on this panel describes the world after 2014, and it cannot be the panel a live engine reads.",
    "2. It can never carry VALIDATED. Every cell is retrospective = 1: a COW hostility level, an ICB "
    "violence code and a UCDP death estimate are later constructions, not contemporaneous records. "
    "WORLD_STATE_CODEBOOK.md Amendment 1 -- a retrospective field alone can never make a read VALIDATED. "
    "This is a property of the sources and n does not touch it.",
    "3. It never scores onset. R-ACT admits a dyad only after a recorded clash, so a dyad quiet for five "
    "years that goes to war is absent from the grid at every date before its first record. Skill measured "
    "here is skill at continuation and de-escalation, never at onset.",
]


def panel_dates(start=PANEL_START, end=PANEL_END):
    return [d.date().isoformat() for d in pd.date_range(start, end, freq="ME")]


def build_panel(src=None, verbose=True):
    """A3: the panel, 1987-2014, on the VR-3 active set. Returns (cells, per_date)."""
    src = src or I.load_sources()
    oil = oil_relevant()
    spells = dyadic_spells(src)
    opposed = opposed_pairs(spells)
    rel = release_dates()
    dyads_all = all_oil_dyads(oil)
    dates = panel_dates()
    cells, per_date = [], []
    for i, t in enumerate(dates):
        act_ract = active_at(t, spells, dyads_all)                       # published beside, A3.2
        act = active_at(t, spells, dyads_all, vr3=True)                  # A3.2: the panel's active set
        cov = covering_sources(t)
        per_date.append({"date": t, "n_active_vr3": len(act), "n_active_ract": len(act_ract),
                         "covering_sources": cov})
        b0, b1 = I.pre_window(t)
        pre_d = (pd.Timestamp(t) - pd.Timedelta(days=91)).date().isoformat()
        for p in act:
            a, b = sorted(p)
            A, pairs, L = {a, b}, {p}, {a, b}
            fwd = I.score_event(t, A, pairs, L, src)
            pre = I.score_event(pre_d, A, pairs, L, src)
            vin, stamps = cell_vintage(pre, b0, b1)
            v1, _v1s = vr1_ok(pre, t, rel)
            d_ies = (None if (fwd["level"] is None or pre["level"] is None) else fwd["level"] - pre["level"])
            fwd_rules, pre_rules = sorted(setter_rules(fwd)), sorted(setter_rules(pre))
            Lev, Pev = evidence_class_of(fwd, p, opposed), evidence_class_of(pre, p, opposed)
            cells.append({
                "date": t, "dyad_a": a, "dyad_b": b, "dyad": f"{a}|{b}",
                "L": fwd["level"], "L_ni": fwd.get("ni_reason"), "L_basis": fwd.get("basis"),
                "Lpre": pre["level"], "Lpre_ni": pre.get("ni_reason"), "dIES": d_ies,
                "L_rules": ",".join(fwd_rules), "Lpre_rules": ",".join(pre_rules),
                "L_records": "; ".join(sorted({r["record"] for r in fwd["recs"]
                                               if r.get("basis") == fwd.get("basis") and r.get("level") is not None
                                               and r["level"] == fwd["level"]})),
                "L_evidence": Lev, "Lpre_evidence": Pev, "evidence_class": weaker(Lev, Pev),   # A3.3
                "covering": ",".join(fwd.get("covering") or []),
                "vr1_ok": v1, "vr2_vintage": vin, "vr2_ok": bool(vin) and vin <= t,
                "label_available_at": (pd.Timestamp(t) + pd.Timedelta(days=91)).date().isoformat(),
                "retrospective": 1,
            })
        if verbose and (i % 24 == 0 or i == len(dates) - 1):
            print(f"  {t}  cells so far {len(cells):>6}  active {len(act):>3} (R-ACT {len(act_ract):>3})  "
                  f"covering {','.join(cov) or 'NONE'}", flush=True)
    return cells, per_date, {"releases": rel, "opposed_pairs": len(opposed),
                             "n_oil_dyads": len(dyads_all), "spells": spells}


def icb_replication(cells):
    """A3.6, measured over the whole panel: for every ICB crisis that SETS a level, how many distinct
    dyads it sets it for. This is the general form of the gbr|usa finding, counted rather than argued."""
    by_crisis = defaultdict(set)
    for c in cells:
        if not c["L_records"] or "ICB" not in (c["L_rules"] or ""):
            continue
        for recname in c["L_records"].split("; "):
            if recname.startswith("crisis "):
                by_crisis[recname].add(c["dyad"])
    counts = sorted(((len(v), k, sorted(v)) for k, v in by_crisis.items()), reverse=True)
    dist = Counter(n for n, _k, _v in counts)
    n_pairs = lambda k: k * (k - 1) // 2                                        # noqa: E731
    return {
        "n_crises_setting_a_level": len(counts),
        "dyads_per_crisis": {"max": counts[0][0] if counts else 0,
                             "mean": round(sum(n for n, _k, _v in counts) / max(len(counts), 1), 2),
                             "distribution": {str(k): v for k, v in sorted(dist.items())}},
        "cells_set_by_icb": sum(1 for c in cells if "ICB" in (c["L_rules"] or "")),
        "top": [{"crisis": k, "n_dyads": n, "dyads": v} for n, k, v in counts[:12]],
        "note": ("A crisis with k register actors on the grid sets a level for up to k(k-1)/2 dyads, "
                 "because ICB records crisis ACTORS and not sides. k=4 -> 6 dyads."),
        "k_to_pairs": {str(k): n_pairs(k) for k in range(2, 9)},
    }


def summarise_panel(cells, per_date, meta):
    nL = [c for c in cells if c["L"] is not None]
    nD = [c for c in cells if c["dIES"] is not None]
    strict = [c for c in cells if c["evidence_class"] == "opposed_side"]
    strictD = [c for c in strict if c["dIES"] is not None]
    share = lambda k, tot: (round(k / tot, 4) if tot else None)                 # noqa: E731
    by_year = defaultdict(lambda: {"cells": 0, "dIES_defined": 0, "dIES_nonzero": 0})
    for c in cells:
        y = by_year[c["date"][:4]]
        y["cells"] += 1
        if c["dIES"] is not None:
            y["dIES_defined"] += 1
            y["dIES_nonzero"] += int(c["dIES"] != 0)
    return {
        "span": {"start": PANEL_START, "end": PANEL_END, "grid_dates": len(per_date), "freq": "month-end"},
        "limits": LIMITS,
        "size": {"cells": len(cells), "distinct_dyads": len({c["dyad"] for c in cells}),
                 "oil_dyads_possible": meta["n_oil_dyads"],
                 "active_per_date_vr3": {"min": min(d["n_active_vr3"] for d in per_date),
                                         "max": max(d["n_active_vr3"] for d in per_date),
                                         "mean": round(sum(d["n_active_vr3"] for d in per_date) / len(per_date), 1)},
                 "active_per_date_ract": {"mean": round(sum(d["n_active_ract"] for d in per_date) / len(per_date), 1)},
                 "cells_dropped_by_VR3": sum(d["n_active_ract"] - d["n_active_vr3"] for d in per_date)},
        "L": {"n_defined": len(nL), "share_defined": share(len(nL), len(cells)),
              "dist": {str(k): v for k, v in sorted(Counter(c["L"] for c in nL).items())},
              "share_zero": share(sum(1 for c in nL if c["L"] == 0), len(nL))},
        "dIES": {"n_defined": len(nD), "share_defined": share(len(nD), len(cells)),
                 "dist": {str(k): v for k, v in sorted(Counter(c["dIES"] for c in nD).items())},
                 "share_zero": share(sum(1 for c in nD if c["dIES"] == 0), len(nD)),
                 "n_nonzero": sum(1 for c in nD if c["dIES"] != 0)},
        "evidence_class": dict(Counter(c["evidence_class"] for c in cells)),
        "evidence_class_of_nonzero_dIES": dict(Counter(c["evidence_class"] for c in nD if c["dIES"] != 0)),
        "strict_subset": {
            "cells": len(strict), "share_of_panel": share(len(strict), len(cells)),
            "dIES_defined": len(strictD), "dIES_nonzero": sum(1 for c in strictD if c["dIES"] != 0),
            "dIES_share_zero": share(sum(1 for c in strictD if c["dIES"] == 0), len(strictD)),
            "dIES_dist": {str(k): v for k, v in sorted(Counter(c["dIES"] for c in strictD).items())},
            "distinct_dyads": len({c["dyad"] for c in strict}),
            "last_date": max((c["date"] for c in strict), default=None)},
        "no_independent_outcome": dict(Counter(
            ("L:" + (c["L_ni"] or "none")) for c in cells if c["L"] is None)) | dict(Counter(
            ("Lpre:" + (c["Lpre_ni"] or "none")) for c in cells if c["Lpre"] is None)),
        "vintage": {"VR1_strict_release": {"n": sum(1 for c in cells if c["vr1_ok"]),
                                           "share": share(sum(1 for c in cells if c["vr1_ok"]), len(cells))},
                    "VR2_event_knowability": {"n": sum(1 for c in cells if c["vr2_ok"]),
                                              "share": share(sum(1 for c in cells if c["vr2_ok"]), len(cells))},
                    "retrospective_share": 1.0},
        "covering_mix_by_grid_date": dict(Counter(",".join(d["covering_sources"]) or "NONE" for d in per_date)),
        "by_year": {k: v for k, v in sorted(by_year.items())},
        "releases": meta["releases"],
    }


def panel_md(s, icb):
    L = []
    a = L.append
    a("# The dyad-date escalation panel, 1987–2014 — size and marginals, before anything is scored")
    a("*Built by `src/grid_labels.py` under `data/grid/g/G4_REGISTRATION.md` Amendments 3–5, which were")
    a("committed first. Nothing here is a score, a forecast or a skill. No cell is filtered out.*\n")
    if s.get("cite"):
        a("> **Cite this panel as:** " + s["cite"] + "\n")
    a("## The three limits, first, because they are properties of the construction and not caveats\n")
    for x in s["limits"]:
        a(f"> **{x}**\n")
    a("## 1. Size\n")
    z = s["size"]
    c = z["cells"] if isinstance(z["cells"], dict) else {"nominal": z["cells"], "n_eff_two_way": None,
                                                        "n_eff_block": None, "informative": None}
    a(f"- **{c['nominal']:,} cells nominal — n_eff {c['n_eff_two_way']:,.0f}** (two-way cluster on "
      f"date × dyad, A5.2; block estimator {c['n_eff_block']:,.0f}), of which **{c['informative']:,} "
      f"informative** (non-zero ΔIES). Over **{s['span']['grid_dates']} month-ends** "
      f"({s['span']['start']} … {s['span']['end']}), on **{z['distinct_dyads']} distinct dyads** "
      f"of {z['oil_dyads_possible']} oil-relevant pairs.")
    a("- *Nominal overstates: the panel is 90 % zeros and heavily clustered. Quote the pair.*")
    a(f"- active dyads per grid date (VR-3): {z['active_per_date_vr3']['min']}–{z['active_per_date_vr3']['max']} "
      f"(mean {z['active_per_date_vr3']['mean']}); under plain R-ACT the mean is "
      f"{z['active_per_date_ract']['mean']}, so **VR-3 removes {z['cells_dropped_by_VR3']:,} dyad-dates** "
      f"that were selected on a record still running at t.")
    dd = s["dIES"]["n_defined"]
    dd = dd if isinstance(dd, dict) else {"nominal": dd, "n_eff_two_way": None}
    a(f"- L defined on {s['L']['n_defined']:,} ({s['L']['share_defined']}) · "
      f"ΔIES defined on **{dd['nominal']:,} nominal / n_eff {dd['n_eff_two_way']:,.0f}** "
      f"({s['dIES']['share_defined']})\n")
    a("## 2. The ΔIES marginal — the number B needs before scoring\n")
    a("| ΔIES | " + " | ".join(s["dIES"]["dist"].keys()) + " |")
    a("|---" * (len(s["dIES"]["dist"]) + 1) + "|")
    a("| cells | " + " | ".join(f"{v:,}" for v in s["dIES"]["dist"].values()) + " |")
    tot = nom(s["dIES"]["n_defined"])
    a("| share | " + " | ".join(f"{v / tot:.4f}" for v in s["dIES"]["dist"].values()) + " |")
    a(f"\n**{tot:,} defined (n_eff {(s['dIES']['n_defined'] or {}).get('n_eff_two_way', 0):,.0f}), "
      f"{s['dIES']['n_nonzero']:,} non-zero, "
      f"share zero {s['dIES']['share_zero']}.** L: {json.dumps(s['L']['dist'])}, share zero {s['L']['share_zero']}.\n")
    a("## 3. Evidence class — a FIELD on every cell (A3.3), never a filter\n")
    a("| class | all cells | of the non-zero ΔIES cells |")
    a("|---|---|---|")
    for k in EVIDENCE_ORDER:
        a(f"| `{k}` | {s['evidence_class'].get(k, 0):,} | {s['evidence_class_of_nonzero_dIES'].get(k, 0):,} |")
    ss = s["strict_subset"]
    sc = ss["cells"] if isinstance(ss["cells"], dict) else {"nominal": ss["cells"], "n_eff_two_way": None}
    a(f"\n**The strict subset** (`evidence_class == opposed_side`): **{sc['nominal']:,} cells nominal, "
      f"n_eff {sc['n_eff_two_way']:,.0f}** "
      f"({ss['share_of_panel']} of the panel) on {ss['distinct_dyads']} dyads, last date {ss['last_date']}; "
      f"ΔIES defined on {ss['dIES_defined']:,}, **{ss['dIES_nonzero']:,} non-zero**, share zero "
      f"{ss['dIES_share_zero']}. ΔIES: {json.dumps(ss['dIES_dist'])}\n")
    a("This is the subset the scored study runs on. It is a selection on a field that is already there; "
      "the diagnostic runs on the full panel. Nothing is rebuilt to move between them.\n")
    a("## 4. The ICB replication, measured over the whole panel (A3.6)\n")
    a(f"- ICB sets a level on **{icb['cells_set_by_icb']:,} cells**, from "
      f"**{icb['n_crises_setting_a_level']} distinct crises**.")
    a(f"- dyads per crisis: max **{icb['dyads_per_crisis']['max']}**, mean {icb['dyads_per_crisis']['mean']}; "
      f"distribution {json.dumps(icb['dyads_per_crisis']['distribution'])}")
    a(f"- {icb['note']}\n")
    a("| crisis | n dyads | the dyads |")
    a("|---|---|---|")
    for r in icb["top"][:8]:
        a(f"| {r['crisis']} | **{r['n_dyads']}** | "
          + ", ".join(x.replace("country.", "").replace("|", "–") for x in r["dyads"]) + " |")
    a("\nSee `ICB_DYADIC_REPLICATION.md` for the write-up.\n")
    a("## 5. Vintage and coverage\n")
    v = s["vintage"]
    a(f"- VR-1 strict (dataset release ≤ t): **{v['VR1_strict_release']['n']}** "
      f"({v['VR1_strict_release']['share']}) — as on the probe, and an upper bound.")
    a(f"- VR-2 (session A's registered convention): {v['VR2_event_knowability']['n']:,} "
      f"({v['VR2_event_knowability']['share']}).")
    a(f"- every cell `retrospective = 1`.")
    a(f"- covering-source mix over the {s['span']['grid_dates']} grid dates: "
      + " · ".join(f"`{k}` ×{n}" for k, n in sorted(s['covering_mix_by_grid_date'].items())))
    a(f"\n- undefined, by reason: {json.dumps(s['no_independent_outcome'])}")
    return "\n".join(L)


def build_main():
    print("loading sources ...", flush=True)
    src = I.load_sources()
    print(f"building the panel {PANEL_START} .. {PANEL_END} ...", flush=True)
    cells, per_date, meta = build_panel(src)
    s = summarise_panel(cells, per_date, meta)
    s["icb_replication"] = icb_replication(cells)
    PANEL_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(cells)
    try:
        df.to_parquet(PANEL_DIR / "PANEL.parquet", index=False)
        wrote = "PANEL.parquet"
    except Exception as e:                                    # pyarrow absent: csv.gz, same columns
        df.to_csv(PANEL_DIR / "PANEL.csv.gz", index=False, compression="gzip")
        wrote = f"PANEL.csv.gz ({type(e).__name__})"
    s["panel_file"] = wrote
    s["generated_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    s["registration"] = "data/grid/g/G4_REGISTRATION.md Amendments 3-5 (2026-09-03)"
    s = finalize(s, df, meta["spells"])                       # A5.4: checks, then the single writer
    print(s["cite"])
    return s




# ---- A3 addendum: density over time, and the cost of the ICB co-actor ACTIVITY rule ------------
# Computed from the built panel (seconds), so the 25-minute build is not re-run to add a block.
# The activity effect is distinct from the LABEL effect of Amendment 2 / A3.6: ICB's co-actor
# pairing does not only fabricate levels for ally pairs, it fabricates ACTIVITY -- a crisis with k
# register actors makes k(k-1)/2 dyads "active" for the whole lookback, five years.

SHADOW_WINDOW = (1991, 1995)          # measured below, not assumed; the years are read off the density series


def panel_addendum():
    s = json.loads((PANEL_DIR / "PANEL.json").read_text())
    df = pd.read_parquet(PANEL_DIR / "PANEL.parquet") if (PANEL_DIR / "PANEL.parquet").exists() \
        else pd.read_csv(PANEL_DIR / "PANEL.csv.gz")
    df["year"] = df["date"].str[:4].astype(int)
    per_date = df.groupby("date").size()
    by_year = df.groupby("year").size() / df.groupby("year")["date"].nunique()
    lo, hi = SHADOW_WINDOW
    w, rest = df[df.year.between(lo, hi)], df[~df.year.between(lo, hi)]
    rate = lambda x: (round(float(((x.dIES.notna()) & (x.dIES != 0)).sum() / max(int(x.dIES.notna().sum()), 1)), 4))  # noqa: E731
    s["density"] = {
        "cells_per_grid_date": {"min": int(per_date.min()), "max": int(per_date.max()),
                                "mean": round(float(per_date.mean()), 1)},
        "mean_cells_per_grid_date_by_year": {str(k): round(float(v), 1) for k, v in by_year.items()},
        "note": ("The panel's own n is NOT uniform. The density quadruples 1991-1995 and falls back. "
                 "That is the ICB co-actor rule acting on the ACTIVE SET, not on the label: a crisis "
                 "with k register actors makes k(k-1)/2 dyads active for the full five-year lookback."),
    }
    s["icb_activity_shadow"] = {
        "window": f"{lo}-{hi}",
        "cells": int(len(w)), "share_of_panel": round(float(len(w) / len(df)), 4),
        "dIES_nonzero_in_window": int(((w.dIES.notna()) & (w.dIES != 0)).sum()),
        "dIES_nonzero_outside": int(((rest.dIES.notna()) & (rest.dIES != 0)).sum()),
        "nonzero_rate_in_window": rate(w), "nonzero_rate_outside": rate(rest),
        "distinct_dyads_in_window": int(w.dyad.nunique()),
        "distinct_dyads_only_in_window": int(len(set(w.dyad) - set(rest.dyad))),
        "evidence_class_in_window": {k: int(v) for k, v in w.evidence_class.value_counts().items()},
        "reading": ("It adds rows, not coverage: every dyad active in the window is active elsewhere too. "
                    "It supplies its share of the panel's rows and a far smaller share of its non-zero "
                    "cells, so nominal n and informative n diverge here more than anywhere else."),
    }
    write_panel(s, df)
    print(json.dumps({"density": s["density"]["cells_per_grid_date"],
                      "icb_activity_shadow": s["icb_activity_shadow"]}, indent=1, default=str))
    return s


def addendum_md(s):
    L, a = [], None
    a = L.append
    d, sh = s["density"], s["icb_activity_shadow"]
    a("## 6. The panel's own n is not uniform, and one crisis supplies nearly half of it\n")
    a(f"Cells per grid date: {d['cells_per_grid_date']['min']}–{d['cells_per_grid_date']['max']} "
      f"(mean {d['cells_per_grid_date']['mean']}). By year:\n")
    ys = list(s["density"]["mean_cells_per_grid_date_by_year"].items())
    a("| year | " + " | ".join(k for k, _v in ys) + " |")
    a("|---" * (len(ys) + 1) + "|")
    a("| cells/date | " + " | ".join(str(v) for _k, v in ys) + " |")
    a(f"\n**{sh['cells']:,} of the panel's cells ({sh['share_of_panel']:.1%}) fall in {sh['window']}**, where the "
      f"density quadruples. {d['note']}\n")
    a("This is the **activity** limb of the ICB co-actor defect, and it is distinct from the **label** limb "
      "of §4: here ICB does not fabricate a level, it fabricates a dyad-date's *existence*. The labels in "
      f"that block are mostly sided ({sh['evidence_class_in_window'].get('opposed_side', 0):,} `opposed_side`) "
      "and mostly zero:\n")
    a("| | cells | non-zero ΔIES | non-zero rate |")
    a("|---|---|---|---|")
    a(f"| {sh['window']} | {sh['cells']:,} | {sh['dIES_nonzero_in_window']:,} | **{sh['nonzero_rate_in_window']}** |")
    a(f"| all other years | {nom(s['size']['cells']) - sh['cells']:,} | {sh['dIES_nonzero_outside']:,} | "
      f"**{sh['nonzero_rate_outside']}** |")
    a(f"\n{sh['reading']} It adds **{sh['distinct_dyads_only_in_window']}** dyads that appear nowhere else.\n")
    a("**For whoever scores this panel:** the block is not wrong — the dyad-dates are real and their labels "
      "are sided — but it is a low-information half of the sample created by a selection rule, and any "
      "estimate that weights cells equally weights it accordingly. It is left in the panel, flagged, and "
      "never removed by G (A3.3: evidence basis is a field, not a filter).")
    return "\n".join(L)




# ================================================================================================
# Amendment 4 — the three checks B handed back when Part IV was withdrawn.
# A4.1 the share-zero tripwire · A4.2 VR-3 as an assertion · A4.3 effective n beside nominal.
# B's designs, adopted with attribution; B's functions are CALLED, never copied, so a later
# correction to them reaches this panel too (as B's deff_block floor correction did).
# ================================================================================================

DEGENERATE_BAR = DEGENERATE_SHARE           # §5.1's 0.95, unchanged and never moved


def share_zero_tripwire(df):
    """A4.1. Share-zero per year and over the span, on dIES and on the level, full panel and the
    opposed_side subset -- eight series -- against §5.1's 0.95 bar. A breach is reported; the slice
    is never dropped and the bar is never moved."""
    out, breaches = {}, []
    strict = df[df.evidence_class == "opposed_side"]
    for scope, d in (("full_panel", df), ("opposed_side", strict)):
        for field in ("dIES", "L"):
            v = d[d[field].notna()]
            overall = (float((v[field] == 0).mean()) if len(v) else None)
            per_year = {}
            for y, g in v.groupby(v["date"].str[:4]):
                s = float((g[field] == 0).mean())
                per_year[y] = {"n": int(len(g)), "share_zero": round(s, 4),
                               "breach": bool(s >= DEGENERATE_BAR)}
                if s >= DEGENERATE_BAR:
                    breaches.append({"scope": scope, "field": field, "year": y,
                                     "share_zero": round(s, 4), "n": int(len(g))})
            key = f"{scope}.{field}"
            out[key] = {"n_defined": int(len(v)),
                        "share_zero_overall": (round(overall, 4) if overall is not None else None),
                        "breach_overall": bool(overall is not None and overall >= DEGENERATE_BAR),
                        "per_year": per_year}
            if overall is not None and overall >= DEGENERATE_BAR:
                breaches.append({"scope": scope, "field": field, "year": "ALL",
                                 "share_zero": round(overall, 4), "n": int(len(v))})
    return {"bar": DEGENERATE_BAR, "rule": ("G4_REGISTRATION §5.1 (bar) + A4.1 (slices). A breach is "
                                            "reported, the slice is never dropped, the bar is never moved."),
            "n_breaches": len(breaches), "breaches": breaches, "series": out}


def admission_audit(df, spells, lookback=ACT_LOOKBACK_DAYS):
    """A4.2. VR-3 as an ASSERTION, on an independent path over the BUILT file: every cell's dyad must
    be admitted at its date by at least one record whose spell ends STRICTLY BEFORE t. One violation
    voids the panel (Amendment F.1's standing)."""
    checked = viol = 0
    first = None
    for (t, dyad), _g in df.groupby(["date", "dyad"]):
        a, b = dyad.split("|")
        p = frozenset((a, b))
        ts = pd.Timestamp(t)
        lo, hi = ts - pd.Timedelta(days=lookback), ts - pd.Timedelta(days=1)
        ok = any(st <= hi and en >= lo and en < ts for st, en, _s in spells.get(p, ()))
        checked += 1
        if not ok:
            viol += 1
            first = first or {"date": t, "dyad": dyad,
                              "spells": [(str(st.date()), str(en.date()), s) for st, en, s in spells.get(p, ())][:4]}
    return {"rule": ("A4.2: every admitted cell's admitting record ends strictly before t. "
                     "One violation voids the panel (WALK_FORWARD_PROTOCOL Amendment F.1 standing)."),
            "cells_checked": checked, "violations": viol, "first_violation": first,
            "asserted": viol == 0}


def effective_n(df):
    """A4.3. n_eff beside n_nominal, from session B's power_arithmetic (called, not copied).
    LIMIT, stated with its direction: DEFF belongs to the score-differential series and this panel
    has no scores, so it is computed on the OUTCOME. A score differential carries the forecaster's
    own error too, so its correlations should be no larger -- the outcome-based DEFF is an UPPER
    bound and the n_eff published here is a FLOOR."""
    sys.path.insert(0, str(ROOT / "src"))
    from engine.grid import power_arithmetic as PA
    out = {"limit": effective_n.__doc__.split("LIMIT, stated with its direction: ")[1].replace("\n    ", " "),
           "source": "src/engine/grid/power_arithmetic.py (session B); functions called, never copied"}
    # Reconciliation with session B's own escalation-panel DEFF, read from B's published file rather
    # than recalled, because a reader seeing 1.5 here and 56-79 there will assume one of us is wrong.
    pa = ROOT / "data" / "grid" / "power_arithmetic.json"
    if pa.exists():
        try:
            b = json.loads(pa.read_text())["escalation_panel"]["month_end"]["mid_family_2014"]
            out["reconciliation_with_B"] = {
                "B_panel": {"n_dyads": b.get("n_dyads"), "n_dyads_with_any_variation": b.get("n_dyads_with_any_variation"),
                            "n_nominal_cells": b.get("n_nominal_cells"), "share_level_0": b.get("share_level_0"),
                            "D_eff": b.get("D_eff"), "informative_cells": b.get("informative_cells")},
                "G_panel": {"n_dyads": None, "n_nominal_cells": None},          # filled below
                "why_they_differ": (
                    "They are different objects, not different answers. B's escalation panel is the FULL "
                    "cross -- every register dyad at every grid date, no active rule -- so it carries dyads "
                    "that are constant zero for the whole span, and a constant series is perfectly "
                    "autocorrelated, which is what drives its DEFF up. B's own file records only "
                    f"{b.get('n_dyads_with_any_variation')} of {b.get('n_dyads')} dyads with ANY variation. "
                    "G's panel is the ACTIVE-SET panel (R-ACT + VR-3), which excludes those dyads by "
                    "construction, so its DEFF is far lower and is the DEFF of the panel G actually built. "
                    "Neither number transfers to the other panel."),
                "shared_warning": (
                    "B's warning applies to G's panel too, at a smaller share: a cell whose outcome both a "
                    "forecaster and its climatology get right carries no power to DISCRIMINATE between them. "
                    "G's panel is 90.3 % zeros against B's 96.8 %, so the informative count -- the non-zero "
                    "cells -- is the number to read, not n_eff."),
            }
        except (KeyError, ValueError):
            pass
    for scope, d in (("full_panel", df), ("opposed_side", df[df.evidence_class == "opposed_side"])):
        v = d[d["dIES"].notna()]
        if len(v) < 10:
            out[scope] = {"n_nominal": int(len(v)), "note": "too few cells"}
            continue
        piv = v.pivot_table(index="date", columns="dyad", values="dIES", aggfunc="first")
        X = piv.to_numpy(dtype=float)
        # B's two_way_cluster_deff takes `covered` as a ROW mask over grid dates (Z = X[covered] must
        # stay 2-D); NaN cells -- a dyad not active at a date -- are handled inside it.
        covered = np.ones(X.shape[0], dtype=bool)
        tw = PA.two_way_cluster_deff(X, covered)
        stacked = v.sort_values(["date", "dyad"])["dIES"].to_numpy(dtype=float)
        blk = PA.deff_block(stacked, mean_block=3, lag=3, label=f"dIES stacked ({scope})")
        n = int(len(v))
        deff_tw = (tw or {}).get("deff_two_way")
        rows = {"n_nominal": n,
                "two_way_cluster": tw,
                "block": blk,
                "n_eff_two_way": (round(n / max(deff_tw, 1.0), 1) if deff_tw else None),
                "n_eff_block": round(n / max(blk["deff_used"], 1.0), 1),
                "n_nonzero_nominal": int((v["dIES"] != 0).sum())}
        out[scope] = rows
    if "reconciliation_with_B" in out:
        v = out.get("full_panel") or {}
        out["reconciliation_with_B"]["G_panel"] = {
            "n_dyads": int(df.dyad.nunique()), "n_nominal_cells": int(len(df)),
            "share_level_0": round(float((df.loc[df.L.notna(), "L"] == 0).mean()), 5),
            "D_eff_two_way": (v.get("two_way_cluster") or {}).get("deff_two_way"),
            "informative_cells": v.get("n_nonzero_nominal")}
    return out


def panel_checks():
    """Run A4.1-A4.3 over the built panel and fold them into PANEL.json / PANEL.md."""
    s = json.loads((PANEL_DIR / "PANEL.json").read_text())
    df = pd.read_parquet(PANEL_DIR / "PANEL.parquet") if (PANEL_DIR / "PANEL.parquet").exists() \
        else pd.read_csv(PANEL_DIR / "PANEL.csv.gz")
    spells = dyadic_spells(I.load_sources())
    s = finalize(s, df, spells)                                 # A4.1-A4.3 then the single writer
    print(json.dumps({"admission_audit": {k: v for k, v in s["admission_audit"].items() if k != "first_violation"},
                      "tripwire": {"n_breaches": s["share_zero_tripwire"]["n_breaches"],
                                   "breaches": s["share_zero_tripwire"]["breaches"][:8]},
                      "effective_n": {k: {kk: vv for kk, vv in v.items()
                                          if kk in ("n_nominal", "n_eff_two_way", "n_eff_block", "n_nonzero_nominal")}
                                      for k, v in s["effective_n"].items() if isinstance(v, dict) and "n_nominal" in v}},
                     indent=1, default=str))
    return s


def checks_md(s):
    L, a = [], None
    a = L.append
    tw, aa, en = s["share_zero_tripwire"], s["admission_audit"], s["effective_n"]
    a("## 7. The three checks the panel owes (Amendment 4 — session B's designs, adopted)\n")
    a(f"### 7.1 Share-zero tripwire — bar {tw['bar']}, never moved\n")
    a("| series | n defined | share zero | breach? |")
    a("|---|---|---|---|")
    for k, v in tw["series"].items():
        a(f"| `{k}` | {v['n_defined']:,} | **{v['share_zero_overall']}** | "
          f"{'**YES**' if v['breach_overall'] else 'no'} |")
    if tw["n_breaches"]:
        a(f"\n**{tw['n_breaches']} breach(es) of the 0.95 bar, reported and not dropped:**\n")
        a("| scope | field | year | n | share zero |")
        a("|---|---|---|---|---|")
        for b in tw["breaches"]:
            a(f"| {b['scope']} | {b['field']} | **{b['year']}** | {b['n']:,} | **{b['share_zero']}** |")
        a("\nThe slice stays in the panel and the bar stays at 0.95 (A4.1). A year that breaches is a "
          "fact about that year, published as one.")
    else:
        a("\nNo slice breaches the bar.")
    a(f"\n### 7.2 Admission audit — VR-3 asserted, not trusted\n")
    a(f"- cells checked: **{aa['cells_checked']:,}** · violations: **{aa['violations']}** · "
      f"`asserted`: **{aa['asserted']}**")
    a(f"- {aa['rule']}")
    if aa["first_violation"]:
        a(f"- first violation: `{json.dumps(aa['first_violation'])}`")
    a(f"\n### 7.3 Effective n beside nominal\n")
    a("| scope | n nominal | non-zero | DEFF two-way (date × dyad) | n_eff two-way | DEFF block | n_eff block |")
    a("|---|---|---|---|---|---|---|")
    for scope in ("full_panel", "opposed_side"):
        v = en.get(scope) or {}
        if "n_nominal" not in v:
            continue
        tww = (v.get("two_way_cluster") or {}).get("deff_two_way")
        blk = v.get("block") or {}
        a(f"| `{scope}` | {v['n_nominal']:,} | {v['n_nonzero_nominal']:,} | {tww} | "
          f"**{v['n_eff_two_way']}** | {blk.get('deff_used')}"
          f"{' (floored)' if blk.get('deff_floored_at_1') else ''} | **{v['n_eff_block']}** |")
    a(f"\n**Limit, with its direction:** {en['limit']}")
    a(f"\nComputed by calling `{en['source']}`.")
    r = en.get("reconciliation_with_B")
    if r:
        a("\n**Reconciling with session B's DEFF of ~56–79 on *its* escalation panel** — a reader seeing 1.5 "
          "here and 56 there will assume one of us is wrong, so both are printed with their panels:\n")
        a("| | dyads | dyads with any variation | cells | share level 0 | DEFF | informative cells |")
        a("|---|---|---|---|---|---|---|")
        b_, g_ = r["B_panel"], r["G_panel"]
        a(f"| B, full cross | {b_['n_dyads']} | {b_['n_dyads_with_any_variation']} | {b_['n_nominal_cells']:,} | "
          f"{b_['share_level_0']} | {b_['D_eff']} | {b_['informative_cells']:,} |")
        a(f"| G, active set | {g_['n_dyads']} | {g_['n_dyads']} (all, by construction) | {g_['n_nominal_cells']:,} | "
          f"{g_['share_level_0']} | {g_['D_eff_two_way']} | {g_['informative_cells']:,} |")
        a(f"\n{r['why_they_differ']}\n")
        a(f"**{r['shared_warning']}**")
    return "\n".join(L)


if __name__ == "__main__":
    if "--build" in sys.argv:
        build_main()
    elif "--addendum" in sys.argv:
        panel_addendum()
    elif "--checks" in sys.argv:
        panel_checks()
    else:
        main()


# ================================================================================================
# Amendment 5 — the effective count is not optional. The nominal count stops existing as a scalar,
# one generated citation line leads every file, and a test enforces both. Joe, 2026-09-03:
# "Make the effective number impossible to omit."
# ================================================================================================

PAIR_NOTE = ("nominal overstates. n_eff is the two-way cluster on (date, dyad) -- A5.2 -- and is the "
             "number to quote; `informative` is the non-zero count, which is what actually discriminates.")


def paired(nominal, en_scope, informative=None):
    """A5.1: a headline count is an OBJECT carrying its effective companions, never a bare integer.
    A reader that wants the nominal must take the pair or get a KeyError."""
    return {"nominal": int(nominal),
            "n_eff_two_way": (en_scope or {}).get("n_eff_two_way"),
            "n_eff_block": (en_scope or {}).get("n_eff_block"),
            "informative": (int(informative) if informative is not None
                            else (en_scope or {}).get("n_nonzero_nominal")),
            "note": PAIR_NOTE}


def cite_line(s):
    """A5.3: the sentence a reader in a hurry copies. Generated, never typed."""
    c, sp = s["size"]["cells"], s["span"]
    return (f"{c['nominal']:,} dyad-date cells (n_eff {c['n_eff_two_way']:,.0f} by two-way cluster on "
            f"date x dyad; {c['informative']:,} informative), {sp['start']} to {sp['end']}, "
            f"{s['size']['distinct_dyads']} dyads. Quoting the nominal count alone overstates this panel.")


def apply_amendment_5(s):
    """A5.1 + A5.3, applied to a finished summary before it is written. Idempotent."""
    en = s.get("effective_n") or {}
    full, strict = en.get("full_panel") or {}, en.get("opposed_side") or {}
    if not isinstance(s["size"]["cells"], dict):
        s["size"]["cells"] = paired(s["size"]["cells"], full, s["dIES"]["n_nonzero"])
    if not isinstance(s["dIES"]["n_defined"], dict):
        s["dIES"]["n_defined"] = paired(s["dIES"]["n_defined"], full, s["dIES"]["n_nonzero"])
    if not isinstance(s["strict_subset"]["cells"], dict):
        s["strict_subset"]["cells"] = paired(s["strict_subset"]["cells"], strict,
                                             s["strict_subset"]["dIES_nonzero"])
    s["cite"] = cite_line(s)
    s["amendment_5"] = ("A5: the nominal count does not exist as a scalar in this file. Every headline "
                        "count is a paired object and `cite` carries both numbers. Enforced by "
                        "tests/test_g_grid_labels.py, not by care.")
    return s


def nom(x):
    """Read a headline count that may be a paired object (A5.1) or a plain int (pre-A5)."""
    return int(x["nominal"]) if isinstance(x, dict) else int(x)


def write_panel(s, df=None):
    """A5.4: the ONLY writer. It applies Amendment 5 first, so there is no code path that publishes a
    panel with a nominal count and no effective count beside it."""
    s = apply_amendment_5(s)
    PANEL_DIR.mkdir(parents=True, exist_ok=True)
    (PANEL_DIR / "PANEL.json").write_text(json.dumps(s, indent=1, default=str))
    body = panel_md(s, s["icb_replication"])
    if "icb_activity_shadow" in s:
        body += "\n\n" + addendum_md(s)
    if "share_zero_tripwire" in s:
        body += "\n\n" + checks_md(s)
    (PANEL_DIR / "PANEL.md").write_text(body)
    return s


def finalize(s, df, spells):
    """A5.4: run A4.1-A4.3, then write. Every publication path goes through here."""
    s["share_zero_tripwire"] = share_zero_tripwire(df)
    s["admission_audit"] = admission_audit(df, spells)
    s["effective_n"] = effective_n(df)
    s["amendment_4"] = ("A4.1-A4.3 are session B's designs, offered in "
                        "data/handoffs/B_to_G_2026-09-03c_part_iv_withdrawn.md and adopted with attribution.")
    return write_panel(s, df)
