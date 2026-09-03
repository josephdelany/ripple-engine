"""
g_monthly_gap.py -- Session G, G-1. The monthly-tier gap arithmetic and the pre-1987
candidate screen, per data/candidates/G1_REGISTRATION.md (registered 2026-09-02, BEFORE
this code, with Amendment 1 on intra-state severity also registered before the run).

What it answers, in one sentence: how many more monthly-tier events the corpus needs
before the tier has 30 scored reads under the registered burn-in of 8, and which rows of
the blind pre-1987 admission sheet are strong enough and sourceable enough to be worth the
research.

Reads:  data/oil.db (READ-ONLY, opened with mode=ro), data/candidates/pre1987_candidates.csv
        (the BLIND sheet), data/big_moves/wti_monthly.json.
Never opens: data/candidates/pre1987_candidates_outcomes.csv (G1_REGISTRATION section 3;
        the ranking must not see the realized price move).
Writes: data/candidates/G1_GAP.md, data/candidates/G1_GAP.json,
        data/candidates/pre1987_ranked.csv. Nothing enters events.

Run:  python3 src/g_monthly_gap.py
"""
from __future__ import annotations

import csv
import json
import random
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "engine"))
DATA = ROOT / "data"
OUT = DATA / "candidates"

# --- the registered parameters, quoted from the code they come from -----------------
BURN_IN = 8                 # src/walk.py:69
MIN_TIER_N = 30             # src/walk.py:71 registered min_tier_n, used at src/walk.py:603
G_HORIZON_DAYS = 90         # src/engine/read.py g_closed_by
P_HORIZON_M = 3             # src/engine/read.py TIERS["monthly"]["horizon"]
GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
ALL_TYPES = GEO_TYPES + ("policy_response", "opec_decision", "demand_shock")
TIER_END = "1987-01-01"     # monthly tier: everything before daily_start
SEED = 19900802             # the walk's registered seed (Amendment I), reused for the allocation draw

# the registered producer/transit/consumer state set lives in session B's sheet builder;
# it is IMPORTED read-only rather than copied, so the two can never drift apart
import pre1987_candidates as PC   # noqa: E402  (src/engine on the path)

STATES = PC.STATES
NAME_TO_CC = {v[0]: k for k, v in STATES.items()}
ROLE = {k: v[1] for k, v in STATES.items()}


# ------------------------------------------------------------------ the corpus, as it is
def monthly_corpus(conn):
    """The monthly tier as the walk sees it: date, class, and whether an IES-90 level exists."""
    lvl = {e: v for e, v in conn.execute(
        "SELECT event_id, value FROM event_outcomes WHERE source='ies90' AND field='level'")}
    rows = []
    for eid, d, t in conn.execute(
            "SELECT event_id, event_date, type FROM events WHERE event_date < ? ORDER BY event_date", (TIER_END,)):
        rows.append({"event_id": eid, "date": pd.Timestamp(d), "type": t,
                     "labelled": eid in lvl, "admitted": True})
    return rows


def scored(events):
    """The registered predicate, re-applied on real dates (G1_REGISTRATION section 2(iii)).

    src/walk.py:276  burn_in_ok = len(g_pool if geo else p_pool) >= 8
    src/engine/read.py:201  pool = same class, event_date < as_of, window closed by as_of
                            (geo: date+90d <= as_of AND an IES-90 level exists;
                             non-geo: same tier and the +3m price observation is dated <= as_of)
    """
    ev = sorted(events, key=lambda e: e["date"])
    out = []
    for i, e in enumerate(ev):
        geo = e["type"] in GEO_TYPES
        pool = 0
        for f in ev[:i]:
            if f["type"] != e["type"] or f["date"] >= e["date"]:
                continue
            if geo:
                if f["labelled"] and f["date"] + pd.Timedelta(days=G_HORIZON_DAYS) <= e["date"]:
                    pool += 1
            else:
                if f["date"] + pd.DateOffset(months=P_HORIZON_M) <= e["date"]:
                    pool += 1
        out.append(dict(e, n_pool=pool, burn_in_ok=pool >= BURN_IN))
    return out


def bound(counts):
    """Section 2(i): scored reads per class can never exceed max(0, n_c - 8)."""
    per = {c: max(0, n - BURN_IN) for c, n in counts.items()}
    return per, sum(per.values())


def min_admission(counts, target=MIN_TIER_N, cap_share=None, min_classes=1):
    """Section 2(ii): the smallest total admission reaching `target` scored reads under the
    bound, by exact search over which classes are activated. Activating class c costs
    (8 - n_c) events that score nothing; after that every event scores one."""
    classes = list(ALL_TYPES)
    best = None
    for mask in range(1, 1 << len(classes)):
        act = [classes[i] for i in range(len(classes)) if mask >> i & 1]
        if len(act) < min_classes:
            continue
        waste = sum(max(0, BURN_IN - counts.get(c, 0)) for c in act)
        cap = int(target * cap_share) if cap_share else target
        if cap * len(act) < target:            # cannot spread `target` under the per-class cap
            continue
        # spread the scored reads as evenly as the cap allows
        alloc, left = {c: 0 for c in act}, target
        while left > 0:
            for c in act:
                if left and alloc[c] < cap:
                    alloc[c] += 1; left -= 1
        total = waste + target
        cand = {"total_additions": total, "classes": act, "waste": waste,
                "scored_per_class": alloc,
                "final_n_per_class": {c: counts.get(c, 0) + max(0, BURN_IN - counts.get(c, 0)) + alloc[c] for c in act}}
        if best is None or cand["total_additions"] < best["total_additions"] or (
                cand["total_additions"] == best["total_additions"] and len(act) > len(best["classes"])):
            best = cand
    return best


# ------------------------------------------------------------------ the screen (blind sheet)
CC_RE = re.compile(r"ccode\s+(\d+)")
SIDE_RE = re.compile(r"\s*\((side \d|.*?)\)\s*$")


def actors_of(cell):
    """COW ccodes named in the sheet's `actors` cell. Names resolve through the registered
    STATES table; a `ccode NNN` form outside that table is a state the register does not name
    and is kept as an unregistered code (it never satisfies P or T)."""
    ccs, unreg = set(), set()
    for part in (cell or "").split(";"):
        p = SIDE_RE.sub("", part.strip())
        m = CC_RE.search(p)
        if m:
            cc = int(m.group(1))
            (ccs if cc in STATES else unreg).add(cc)
            continue
        if p in NAME_TO_CC:
            ccs.add(NAME_TO_CC[p])
        elif p:
            unreg.add(p)
    return ccs, unreg


def severity(row):
    """V, per G1_REGISTRATION section 3.1 as amended by Amendment 1. Returns (V, why, via_amendment)."""
    d, s = row["source_detail"] or "", row["source"]
    ccs, _ = actors_of(row["actors"])
    producer = any("producer" in ROLE.get(c, "") for c in ccs)
    m = re.search(r"hihost\s+(\d)", d)
    if m and int(m.group(1)) >= 4:
        return True, f"MID hihost {m.group(1)}", False
    m = re.search(r"viol\s+(\d)", d)
    if m and int(m.group(1)) >= 3:
        return True, f"ICB viol {m.group(1)}", False
    if "inter-state" in s:
        return True, "COW inter-state war", False
    if "intra-state" in s and producer:
        return True, "COW intra-state war, producer state party (Amendment 1)", True
    return False, "", False


def load_sheet():
    rows = list(csv.DictReader(open(OUT / "pre1987_candidates.csv")))
    assert set(rows[0]) == {"event_date", "actors", "source", "source_id", "source_detail", "suggested_title"}, \
        "the sheet is not the blind one registered in REGISTRATION.md Amendment 1"
    for r in rows:
        r["date"] = pd.Timestamp(r["event_date"])
        r["cc"], r["unreg"] = actors_of(r["actors"])
        r["P"] = any("producer" in ROLE.get(c, "") for c in r["cc"])
        r["T"] = any("transit" in ROLE.get(c, "") for c in r["cc"])
        r["V"], r["V_why"], r["V_amend"] = severity(r)
        r["family"] = "ICB" if r["source"].startswith("ICB") else ("MID" if "MID" in r["source"] else "COW")
    return rows


def episodes(rows):
    """M, per section 3.1: records within +/-31 days of each other sharing >= 1 registered actor
    are one episode. Single-linkage over that relation, so a chain of near-simultaneous records
    of the same clash collapses once."""
    rows = sorted(rows, key=lambda r: r["date"])
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i

    for i, a in enumerate(rows):
        for j in range(i + 1, len(rows)):
            b = rows[j]
            if (b["date"] - a["date"]).days > 31:
                break
            if a["cc"] & b["cc"]:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    groups = defaultdict(list)
    for i, r in enumerate(rows):
        groups[find(i)].append(r)
    eps = []
    for members in groups.values():
        members.sort(key=lambda r: r["date"])
        fams = {m["family"] for m in members}
        cc = set().union(*[m["cc"] for m in members])
        V = [m for m in members if m["V"]]
        ep = {"date": members[0]["date"], "n_records": len(members), "families": sorted(fams),
              "multi_source": len(fams) >= 2, "cc": sorted(cc),
              "P": any(m["P"] for m in members), "T": any(m["T"] for m in members),
              "V": bool(V), "V_why": "; ".join(sorted({m["V_why"] for m in V})),
              "V_amend_only": bool(V) and all(m["V_amend"] for m in V),
              "records": [f'{m["source"]}|{m["source_id"]}' for m in members],
              "label": " / ".join(sorted({(m["source_detail"] or "").split(";")[0].strip() for m in members})[:3]),
              "actors": " / ".join(sorted({STATES[c][0] for c in cc})[:6])}
        ep["tier"] = ("A" if (ep["P"] and ep["V"] and ep["multi_source"])
                      else "B" if ((ep["P"] or ep["T"]) and ep["V"]) else "C")
        eps.append(ep)
    return sorted(eps, key=lambda e: e["date"])


# ------------------------------------------------------------------ diagnostics
def d1_big_moves():
    j = json.load(open(DATA / "big_moves" / "wti_monthly.json"))
    inside = [e for e in j["episodes"] if e["onset"] < TIER_END]
    covered = set()
    for e in inside:
        for y in range(pd.Timestamp(e["onset"]).year, pd.Timestamp(e["end"]).year + 1):
            covered.add(y)
    gap = [y for y in range(1946, 1987) if y not in covered]
    return {"n_episodes_1946_1986": len(inside),
            "episodes": [{"onset": e["onset"], "end": e["end"], "change_pct": round(e["change"], 1)} for e in inside],
            "years_covered": sorted(covered),
            "longest_uncovered_run": _longest_run(gap), "n_years_uncovered": len(gap),
            "n_episodes_total": j["n_episodes"]}


def _longest_run(years):
    best = cur = []
    for y in years:
        cur = cur + [y] if cur and y == cur[-1] + 1 else [y]
        if len(cur) > len(best):
            best = cur
    return [best[0], best[-1], len(best)] if best else None


def d2_wtisplc(conn):
    """Is the pre-1973 monthly P target a traded price? Registered before the numbers were seen."""
    df = pd.DataFrame(conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id='fred.WTISPLC' ORDER BY obs_date").fetchall(),
        columns=["obs_date", "value"])
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    df["chg3"] = df["value"].pct_change(P_HORIZON_M) * 100
    eras = {"1946-01..1972-12": ("1946-01-01", "1972-12-31"),
            "1973-01..1986-12": ("1973-01-01", "1986-12-31"),
            "1987-01..2026-07": ("1987-01-01", "2026-12-31")}
    out = {}
    for k, (a, b) in eras.items():
        s = df[(df.obs_date >= a) & (df.obs_date <= b)]
        c = s["chg3"].dropna()
        out[k] = {"n_months": int(len(s)), "n_3m_changes": int(len(c)),
                  "distinct_price_levels": int(s["value"].nunique()),
                  "mean_abs_chg3_pct": round(float(c.abs().mean()), 3),
                  "sd_chg3_pct": round(float(c.std()), 3),
                  "iqr_chg3_pct": round(float(c.quantile(.75) - c.quantile(.25)), 3),
                  "share_abs_chg3_ge_10pct": round(float((c.abs() >= 10).mean()), 4),
                  "share_chg3_exactly_zero": round(float((c == 0).mean()), 4)}
    return out


def d3_labels(rows):
    """Which IES-90 sources cover each candidate's date (src/state/ies90.py COVER)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("ies90_ro", ROOT / "src" / "state" / "ies90.py")
    cover = {"midi": ("1993-01-01", "2014-12-31"), "war": ("1816-01-01", "2007-12-31"),
             "war_intra": ("1816-01-01", "2014-12-31"), "mid": ("1816-01-01", "2014-12-31"),
             "icb": ("1918-01-01", "2021-12-31"), "ged": ("1989-01-01", "2025-12-31")}
    try:                                    # read the real table if the module imports cleanly
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); cover = m.COVER
    except Exception as ex:
        print(f"[g_monthly_gap] ies90 COVER read from the registered copy ({ex})", file=sys.stderr)
    n_cov = Counter()
    for r in rows:
        d = str(r["date"].date())
        srcs = [s for s, (a, b) in cover.items() if a <= d <= b]
        n_cov[len(srcs) > 0] += 1
    return {"cover_windows": {k: list(v) for k, v in cover.items()},
            "n_rows": len(rows), "n_with_a_covering_source": n_cov[True],
            "n_with_none": n_cov[False],
            "note": "coverage of the DATE only; whether a source holds a record for the "
                    "event's own actors is decided by ies90.score_event at admission"}


# ------------------------------------------------------------------ scenarios
def scenario_dates(eps, tiers, n):
    return [e["date"] for e in eps if e["tier"] in tiers][:n]


def run_scenario(base, dates, classes, rng=None):
    """Date-aware recount: add events on `dates`, assigned to `classes` (round-robin, or at
    random when rng is given), then re-apply the registered predicate."""
    add = []
    for i, d in enumerate(dates):
        c = rng.choice(classes) if rng else classes[i % len(classes)]
        add.append({"event_id": f"cand_{i}", "date": d, "type": c, "labelled": True, "admitted": False})
    res = scored(base + add)
    return sum(1 for r in res if r["burn_in_ok"]), res


def grow_until(base, pool_dates, classes, target=MIN_TIER_N, rng=None):
    """The smallest prefix of `pool_dates` that reaches `target` scored reads."""
    for n in range(1, len(pool_dates) + 1):
        got, _ = run_scenario(base, pool_dates[:n], classes, rng)
        if got >= target:
            return n, got
    got, _ = run_scenario(base, pool_dates, classes, rng)
    return None, got


def main():
    conn = sqlite3.connect(f"file:{DATA/'oil.db'}?mode=ro", uri=True)
    base = monthly_corpus(conn)
    counts = Counter(e["type"] for e in base)
    counts = {c: counts.get(c, 0) for c in ALL_TYPES}

    cur = scored(base)
    n_now = sum(1 for r in cur if r["burn_in_ok"])
    per_bound, tier_bound = bound(counts)

    rows = load_sheet()
    eps = episodes(rows)
    by_tier = Counter(e["tier"] for e in eps)
    amend_only = [e for e in eps if e["tier"] in ("A", "B") and e["V_amend_only"]]

    res = {
        "registration": "data/candidates/G1_REGISTRATION.md (2026-09-02) + Amendment 1",
        "generated_at": pd.Timestamp.utcnow().isoformat(),
        "registered_parameters": {"burn_in": BURN_IN, "min_tier_n": MIN_TIER_N,
                                  "g_horizon_days": G_HORIZON_DAYS, "p_horizon_months": P_HORIZON_M,
                                  "geo_types": list(GEO_TYPES), "tier_end": TIER_END},
        "corpus_now": {"n_monthly_events": len(base), "n_scored_now": n_now,
                       "per_class": counts, "earliest": str(min(e["date"] for e in base).date()),
                       "events": [{"event_id": r["event_id"], "date": str(r["date"].date()), "type": r["type"],
                                   "labelled": r["labelled"], "n_pool": r["n_pool"]} for r in cur]},
        "bound": {"per_class": per_bound, "tier_total": tier_bound},
        "min_admission_concentrated": min_admission(counts),
        "min_admission_balanced": min_admission(counts, cap_share=0.5, min_classes=3),
        "min_admission_all_seven": min_admission(counts, min_classes=7),
        "screen": {"n_sheet_rows": len(rows), "n_episodes": len(eps),
                   "by_tier": dict(by_tier),
                   "n_tierAB_only_via_amendment1": len(amend_only)},
        "diagnostics": {"D1_big_moves_1946_1986": d1_big_moves(),
                        "D2_wtisplc_by_era": d2_wtisplc(conn),
                        "D3_ies90_date_coverage": d3_labels(rows)},
    }

    # scenario 2: concentrated in the class with the most existing members
    top_class = max(counts, key=lambda c: counts[c])
    poolA = scenario_dates(eps, ("A",), 400)
    poolAB = scenario_dates(eps, ("A", "B"), 400)
    n_needed, got = grow_until(base, poolA, [top_class])
    res["scenario_2_concentrated"] = {
        "class": top_class, "pool": "Tier A episode dates, in date order",
        "n_admitted_to_reach_30": n_needed, "scored": got,
        "bound_says": min_admission(counts)["total_additions"],
        "degenerate": True,
        "note": "one class carries the whole tier; section 6's per-class blocks and section 7's "
                "promotion rule cannot be run on it"}

    # scenario 3: balanced over the three cheapest classes, illustrative allocation + a seeded draw
    bal = min_admission(counts, cap_share=0.5, min_classes=3)
    cls = bal["classes"]
    n_needed_b, got_b = grow_until(base, poolA, cls)
    rng = random.Random(SEED)
    draws = []
    for _ in range(200):
        n_, g_ = grow_until(base, poolA, cls, rng=rng)
        draws.append(n_ if n_ else len(poolA) + 1)
    res["scenario_3_balanced"] = {
        "classes": cls, "bound_says": bal["total_additions"],
        "n_admitted_to_reach_30_roundrobin": n_needed_b, "scored": got_b,
        "random_allocation_seed": SEED,
        "random_allocation_n_admitted": {"min": min(draws), "median": int(pd.Series(draws).median()),
                                         "max": max(draws), "n_draws": len(draws)},
        "note": "class assignment is Joe's at admission; the round-robin is illustrative and the "
                "seeded draw prices the assignment uncertainty"}

    # scenario 4: what the archive can reach -- Tier A only, and Tier A+B
    res["scenario_4_reachable"] = {
        "n_tierA_episodes": by_tier.get("A", 0), "n_tierAB_episodes": by_tier.get("A", 0) + by_tier.get("B", 0),
        "tierA_enough_for_concentrated": by_tier.get("A", 0) >= (n_needed or 10 ** 9),
        "n_admitted_to_reach_30_tierAB_balanced": grow_until(base, poolAB, cls)[0],
        "note": "counts of episodes that PASS THE SCREEN, not of episodes proven sourceable; "
                "route_tested in pre1987_ranked.csv is the only sourceability evidence"}

    # scenario 5 (Amendment 2): admission confined to the window in which the P target moves
    P_ALIVE = pd.Timestamp("1973-01-01")
    era = lambda e: "pre1973" if e["date"] < P_ALIVE else "1973_1986"
    res["scenario_5_p_alive"] = {"registered": "G1_REGISTRATION.md Amendment 2",
                                 "episodes_by_tier_and_era": {f"{t}:{er}": sum(1 for e in eps if e["tier"] == t and era(e) == er)
                                                              for t in ("A", "B", "C") for er in ("pre1973", "1973_1986")}}
    for name, tiers in (("tierA", ("A",)), ("tierAB", ("A", "B"))):
        pool = [e["date"] for e in eps if e["tier"] in tiers and e["date"] >= P_ALIVE]
        conc_n, conc_scored = grow_until(base, pool, [top_class])
        bal_n, bal_scored = grow_until(base, pool, cls)
        rng2 = random.Random(SEED)
        draw = [grow_until(base, pool, cls, rng=rng2)[0] for _ in range(200)]
        res["scenario_5_p_alive"][name] = {
            "n_pool": len(pool), "concentrated_n_admitted": conc_n, "concentrated_scored": conc_scored,
            "balanced_roundrobin_n_admitted": bal_n, "balanced_scored": bal_scored,
            "balanced_random_n_admitted": (None if any(x is None for x in draw) else
                                           {"min": min(draw), "median": int(pd.Series(draw).median()), "max": max(draw)})}

    # the named pre-1974 episodes of the brief: is each one visible to the sheet at all?
    NAMED = [("Suez nationalisation and closure", "1956-07-26", {651, 666, 220, 200}),
             ("Six-Day War and canal closure", "1967-06-05", {651, 666, 652, 663}),
             ("Libya posted-price confrontation / nationalisation", "1970-09-01", {620}),
             ("Tehran and Tripoli agreements", "1971-02-14", {630, 620, 645, 670, 690}),
             ("Iraq Petroleum Company nationalisation", "1972-06-01", {645})]
    probe = []
    for title, d, want in NAMED:
        d = pd.Timestamp(d)
        hits = [r for r in rows if abs((r["date"] - d).days) <= 45 and (r["cc"] & want)]
        probe.append({"episode": title, "date": str(d.date()),
                      "n_sheet_rows_within_45d_with_a_named_actor": len(hits),
                      "rows": [f'{r["event_date"]} {r["source"]} {r["source_id"]}: {(r["source_detail"] or "")[:70]}' for r in hits[:6]]})
    res["named_episode_probe"] = {
        "rule": "any sheet row dated within +/-45 days of the episode whose registered actor set "
                "intersects the episode's states; the sheet's three sources are militarised-dispute "
                "registries, so a commercial episode can be absent even when the state is at issue",
        "episodes": probe}

    (OUT / "G1_GAP.json").write_text(json.dumps(res, indent=1, default=str))

    with open(OUT / "pre1987_ranked.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "tier", "date", "actors", "label", "n_records", "families", "multi_source",
                    "producer", "transit", "severity_why", "via_amendment_1", "records",
                    "route_predicted", "route_tested"])
        ranked = sorted(eps, key=lambda e: ({"A": 0, "B": 1, "C": 2}[e["tier"]], e["date"]))
        for i, e in enumerate(ranked, 1):
            w.writerow([i, e["tier"], str(e["date"].date()), e["actors"], e["label"], e["n_records"],
                        "+".join(e["families"]), int(e["multi_source"]), int(e["P"]), int(e["T"]),
                        e["V_why"], int(e["V_amend_only"]), " ; ".join(e["records"]), "", ""])

    print(json.dumps({k: v for k, v in res.items() if k not in ("corpus_now", "diagnostics")}, indent=1, default=str))
    print("\nD1:", json.dumps(res["diagnostics"]["D1_big_moves_1946_1986"], indent=1)[:900])
    print("\nD2:", json.dumps(res["diagnostics"]["D2_wtisplc_by_era"], indent=1))
    print("\nD3:", json.dumps(res["diagnostics"]["D3_ies90_date_coverage"]["n_with_a_covering_source"]))


if __name__ == "__main__":
    main()
