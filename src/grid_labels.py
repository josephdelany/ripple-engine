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


if __name__ == "__main__":
    main()
