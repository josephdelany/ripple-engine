"""read_exposure.py -- EXPOSURE_REGISTRATION.md §4: read(exposure) -> distribution.

Given a supplied exposure conforming to §2, retrieve comparable historical cases BY EXPOSURE
SIMILARITY across every block, and return the duration distribution and the price/margin
distribution across the complex, each with its own n and its reference class named. This is the
operator-supplied exposure module of a catastrophe model: it is what makes the project an
instrument rather than a study.

TWO REGISTERED CONSTRAINTS, both enforced in code and by tests:

  * **Historical frequencies with their n, NEVER an occurrence probability.** Every distribution
    reports counts and `share_of_n` against a stated n, and lists the cases it was built from so a
    reader can check it. No output key or value expresses a probability, and a test greps for it.
  * **Fewer than 5 comparable cases returns `no_adequate_precedent` as a FIRST-CLASS STATE** --
    not an empty result, not a wider search quietly substituted. The state carries what was found,
    what was searched, and what would have to be true to get a read.

AND THE ONE THIS SESSION KEEPS RE-LEARNING: **a missing field must not silently match as a zero.**
`ies90.score_event` used `max(default=0)` and published 18 events as "no escalation" when the
truth was "no answer". The same defect here would be a query with 5,700 kb/d affected scoring a
perfect magnitude match against a case whose capacity is simply unrecorded. So:

  * a field absent on EITHER side is NOT COMPARED -- it contributes no similarity and no penalty,
    and is listed in `fields_not_compared` with the side it was missing from;
  * a real measured 0 IS compared (a foiled attack took 0 kb/d offline, and that is a finding);
  * a case with no comparable field beyond the asset-type gate is not a match at all;
  * `fields_used` names what actually drove each match, per row and in aggregate.

RETRIEVAL RULE, fixed here before any read is run:
  1. `asset_type` is a GATE, not a score. A refinery and a chokepoint are not comparable cases;
     where both sides declare a type and the types differ, the case is excluded. Where the query
     declares one and a case does not, the case is excluded too -- an unknown type cannot be
     asserted to match.
  2. Within the gate, cases are ranked by closeness on the fields both sides carry:
     `capacity_affected_kbd`, `capacity_nameplate_kbd`, the affected share, and `country_iso3`.
  3. Magnitude closeness is on a log scale, because the corpus spans 0 to 20,000 kb/d.
  4. The reference class is NAMED from the gate and the realised span of the matched cases, never
     from the query's own numbers.

Run:  python3 src/read_exposure.py --demo     write the two worked reads
"""
import json
import math
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import exposure_schema as S  # noqa: E402

REGISTRATION = "EXPOSURE_REGISTRATION.md §4 (2026-09-03, commit 22da52f)"
DB = ROOT / "data" / "oil.db"
OUT_DIR = ROOT / "data" / "exposure" / "reads"
MIN_CASES = 5                      # §4: below this -> no_adequate_precedent
HORIZONS = (0, 1, 2, 5, 10, 20, 40, 60)      # PHYSICAL_EXPOSURE §1, trading days
HEADLINE_H = 20
LOG_TOL = 0.5                      # within ~3.2x on capacity counts as the same magnitude class

# the complex, per PHYSICAL_EXPOSURE §1: crude, refined products, and the two cracks
TARGETS = {"brent": "fred.DCOILBRENTEU", "wti": "fred.DCOILWTICO",
           "diesel": "fred.DHOILNYH", "gasoline": "fred.DGASUSGULF", "jet": "fred.DJFUELUSGULF"}
CRACKS = {"diesel_crack": ("diesel", "brent"), "gasoline_crack": ("gasoline", "brent")}

COMPARE_FIELDS = ("capacity_affected_kbd", "capacity_nameplate_kbd", "affected_share", "country_iso3")
# §4 says "by exposure similarity". Geography alone is not exposure: a case that shares only
# country_iso3 is a case about the same place, not about a comparable physical loss. At least one
# of these must be comparable on BOTH sides or the case is not retrieved.
MAGNITUDE_FIELDS = ("capacity_affected_kbd", "capacity_nameplate_kbd", "affected_share")


def _num(v):
    """The numeric value, or None. A real 0 survives; every unknown marker becomes None."""
    if isinstance(v, bool) or not S.is_filled(v):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def affected_share(rec):
    """affected / nameplate, only when BOTH are present and nameplate > 0. Never imputed."""
    a, n = _num(rec.get("capacity_affected_kbd")), _num(rec.get("capacity_nameplate_kbd"))
    if a is None or n is None or n <= 0:
        return None
    return a / n


def _mag_close(a, b):
    """Closeness of two magnitudes on a log scale, in [0, 1]. A measured 0 is a value: two zeros
    match exactly, and 0 against a positive quantity is maximally far -- NOT skipped, because that
    is a real difference, unlike a missing field."""
    if a == 0 and b == 0:
        return 1.0
    if a == 0 or b == 0:
        return 0.0
    d = abs(math.log10(a / b))
    return max(0.0, 1.0 - d / (2 * LOG_TOL))


def compare(query, case):
    """(score, used, not_compared) for one candidate. `used` names the fields that actually drove
    the match; `not_compared` names each skipped field and WHICH SIDE it was missing from, so a
    read can never present a match as stronger than the data it rests on."""
    used, skipped, parts = {}, {}, []
    q_share, c_share = affected_share(query), affected_share(case)
    for f in COMPARE_FIELDS:
        if f == "affected_share":
            qv, cv = q_share, c_share
        elif f == "country_iso3":
            qv = query.get(f) if S.is_filled(query.get(f)) else None
            cv = case.get(f) if S.is_filled(case.get(f)) else None
        else:
            qv, cv = _num(query.get(f)), _num(case.get(f))
        if qv is None or cv is None:
            side = ("query" if qv is None else "") + ("+case" if cv is None else "")
            skipped[f] = f"missing on {side.strip('+') or 'both'}"
            continue
        if f == "country_iso3":
            s = 1.0 if str(qv).upper() == str(cv).upper() else 0.0
        elif f == "affected_share":
            s = max(0.0, 1.0 - abs(qv - cv))
        else:
            s = _mag_close(qv, cv)
        used[f] = round(s, 4)
        parts.append(s)
    return (sum(parts) / len(parts) if parts else None), used, skipped


def load_cases():
    """Every event in every block, with its block and computed status. Partial records are kept:
    §4 asks for comparable cases, and a partial record is comparable on the fields it has."""
    out = []
    for block, d in S.load_blocks().items():
        for e in d["events"]:
            v = S.validate_event(e)
            out.append({**e, "_block": block, "_status": v["computed_status"],
                        "_hard_failures": v["hard_failures"]})
    return out


# ------------------------------------------------------------------ the price side

def load_prices(conn):
    """{target: pandas Series of levels}. Loaded once; the read reports forward percentage changes,
    NOT abnormal returns -- there is no market model here, and calling them CARs would borrow a
    rigour this read does not have."""
    import pandas as pd
    out = {}
    for name, sid in TARGETS.items():
        df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? "
                         "AND value IS NOT NULL ORDER BY obs_date", conn, params=[sid])
        if df.empty:
            continue
        df["obs_date"] = pd.to_datetime(df["obs_date"])
        out[name] = df.set_index("obs_date")["value"].sort_index()
    return out


def forward_change(series, date, h):
    """Percentage change from the first trading day on/after `date` to h trading days later.
    None when the window runs off either end -- never 0, which would read as 'no move'."""
    import pandas as pd
    if not S.is_filled(date):
        return None
    try:                                   # an unparseable date yields NO price, never a default one
        ts = pd.Timestamp(str(date)[:10])
    except Exception:
        return None
    idx = series.index
    pos = idx.searchsorted(ts)
    if pos >= len(idx) or pos + h >= len(idx):
        return None
    p0, p1 = float(series.iloc[pos]), float(series.iloc[pos + h])
    if p0 == 0:
        return None
    return (p1 / p0 - 1.0) * 100.0


def _quantiles(vals):
    v = sorted(vals)
    if not v:
        return None
    def q(p):
        if len(v) == 1:
            return v[0]
        i = p * (len(v) - 1)
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        return v[lo] + (v[hi] - v[lo]) * (i - lo)
    return {"min": round(v[0], 2), "p25": round(q(0.25), 2), "median": round(q(0.5), 2),
            "p75": round(q(0.75), 2), "max": round(v[-1], 2)}


def price_distribution(matches, prices):
    """Per target and horizon: the realised forward changes across the matched cases, with THEIR
    OWN n. The price n is almost always smaller than the match n -- the corpus starts in 1973 and
    the series in 1986/1987 -- so the two are never conflated and the shortfall is named."""
    out = {}
    for name, series in prices.items():
        per_h = {}
        for h in HORIZONS:
            rows = []
            for m in matches:
                v = forward_change(series, m["date"], h)
                if v is not None:
                    rows.append({"event_id": m["event_id"], "pct": round(v, 2)})
            if rows:
                per_h[f"h{h}"] = {"n": len(rows), "n_matches_without_price_data": len(matches) - len(rows),
                                  "unit": "percent change in price over h trading days",
                                  "quantiles": _quantiles([r["pct"] for r in rows]), "cases": rows}
        if per_h:
            out[name] = per_h
    # cracks: product minus crude, per case, so the margin is a difference of the two changes
    for cname, (prod, crude) in CRACKS.items():
        if prod not in prices or crude not in prices:
            continue
        per_h = {}
        for h in HORIZONS:
            rows = []
            for m in matches:
                a, b = forward_change(prices[prod], m["date"], h), forward_change(prices[crude], m["date"], h)
                if a is not None and b is not None:
                    rows.append({"event_id": m["event_id"], "pct": round(a - b, 2)})
            if rows:
                per_h[f"h{h}"] = {"n": len(rows), "n_matches_without_price_data": len(matches) - len(rows),
                                  "unit": "percentage-point difference: product change minus crude change",
                                  "quantiles": _quantiles([r["pct"] for r in rows]), "cases": rows}
        if per_h:
            out[cname] = per_h
    return out


def duration_distribution(matches):
    """days_to_partial_restore and days_to_full_restore across the matched cases.

    'ongoing' and 'never' are kept as their OWN CATEGORIES with counts, never dropped and never
    coerced to a number: a permanently closed refinery is not a long outage, it is a different
    outcome, and averaging it into one would be the same error as scoring an undated record as 0.
    The numeric quantiles therefore carry a smaller n than the category counts, and both are shown."""
    out = {}
    for field in ("days_to_partial_restore", "days_to_full_restore"):
        nums, cats, rows = [], Counter(), []
        for m in matches:
            v = m.get(field)
            if not S.is_filled(v):
                cats["unknown"] += 1
                continue
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                nums.append(float(v))
                rows.append({"event_id": m["event_id"], "days": v})
            else:
                cats[str(v).strip().lower()] += 1
                rows.append({"event_id": m["event_id"], "days": str(v)})
        out[field] = {
            "n_matches": len(matches), "n_numeric": len(nums),
            "categories": {k: {"n": c, "share_of_n": round(c / len(matches), 3)} for k, c in sorted(cats.items())},
            "quantiles_days": _quantiles(nums),
            "note": ("'ongoing' and 'never' are outcomes, not long durations, and are counted as "
                     "categories rather than folded into the quantiles. n_numeric is the n behind "
                     "quantiles_days; n_matches is the n behind the categories."),
            "cases": rows}
    return out


# ------------------------------------------------------------------ the read

def name_reference_class(query, matches, gate_type):
    """Named from the GATE and the REALISED SPAN of the matched cases -- never from the query's own
    numbers, which would describe the question rather than the evidence answering it."""
    aff = [_num(m.get("capacity_affected_kbd")) for m in matches]
    aff = [a for a in aff if a is not None]
    bits = [f"{gate_type or 'asset'} cases"]
    if aff:
        bits.append(f"capacity affected {min(aff):,.0f}-{max(aff):,.0f} kb/d (n={len(aff)} of {len(matches)} carry it)")
    yrs = sorted(str(m["date"])[:4] for m in matches if str(m.get("date", ""))[:4].isdigit())
    if yrs:
        bits.append(f"{yrs[0]}-{yrs[-1]}")
    if len(yrs) < len(matches):
        bits.append(f"{len(matches) - len(yrs)} case(s) with no usable date")
    return "; ".join(bits)


def read(exposure, cases=None, prices=None, conn=None, min_cases=MIN_CASES, exclude_event_ids=()):
    """§4's deliverable. Returns historical frequencies with their n, never a probability."""
    cases = load_cases() if cases is None else cases
    own = None
    if conn is None and prices is None:
        own = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        conn = own
    try:
        prices = load_prices(conn) if prices is None and conn is not None else (prices or {})
    finally:
        if own is not None:
            own.close()

    q_type = exposure.get("asset_type") if S.is_filled(exposure.get("asset_type")) else None
    scored, gated_out = [], Counter()
    for c in cases:
        if c["event_id"] in exclude_event_ids:
            gated_out["excluded_by_caller (held-out)"] += 1
            continue
        c_type = c.get("asset_type") if S.is_filled(c.get("asset_type")) else None
        if q_type is not None:
            if c_type is None:
                gated_out["case has no asset_type -- an unknown type cannot be asserted to match"] += 1
                continue
            if c_type != q_type:
                gated_out[f"asset_type {c_type} != {q_type}"] += 1
                continue
        if c["_status"] == "INVALID":
            # an INVALID case carries a numeric with no provenance (§2 hard failure). Matching on it
            # would import an unsourced magnitude into the read -- the exact defect the schema
            # validator exists to catch -- so it is excluded here rather than silently used.
            gated_out["case is INVALID under §2 (a numeric without provenance)"] += 1
            continue
        score, used, skipped = compare(exposure, c)
        if score is None:
            gated_out["no field comparable on both sides beyond the asset-type gate"] += 1
            continue
        if not any(f in used for f in MAGNITUDE_FIELDS):
            gated_out["comparable only on country -- geography is not exposure similarity"] += 1
            continue
        scored.append({"event_id": c["event_id"], "date": c["date"], "block": c["_block"],
                       "status": c["_status"], "asset_name": c.get("asset_name"),
                       "asset_type": c_type, "similarity": round(score, 4),
                       "fields_used": used, "fields_not_compared": skipped,
                       "capacity_affected_kbd": c.get("capacity_affected_kbd"),
                       "capacity_nameplate_kbd": c.get("capacity_nameplate_kbd"),
                       "days_to_partial_restore": c.get("days_to_partial_restore"),
                       "days_to_full_restore": c.get("days_to_full_restore")})
    scored.sort(key=lambda r: (-r["similarity"], r["date"]))

    base = {"registration": REGISTRATION, "generated_by": "src/read_exposure.py",
            "query": {k: v for k, v in exposure.items() if not k.startswith("_")},
            "retrieval": {"n_cases_searched": len(cases), "n_comparable": len(scored),
                          "asset_type_gate": q_type, "excluded": dict(gated_out),
                          "rule": ("asset_type is a gate; within it, cases are ranked on the fields BOTH "
                                   "sides carry. A field missing on either side is not compared -- it "
                                   "contributes no similarity and no penalty -- and a measured 0 is "
                                   "compared as the value it is.")},
            "not_a_probability": ("Every figure here is a historical frequency over a named and counted "
                                  "set of past cases. Nothing in this output is the probability of "
                                  "anything happening.")}

    if len(scored) < min_cases:
        base.update({
            "state": "no_adequate_precedent",
            "n": len(scored),
            "reason": (f"{len(scored)} comparable case(s) found; §4 requires at least {min_cases}. "
                       f"This is a first-class result, not an error and not an empty read: the corpus "
                       f"does not contain enough comparable exposure to answer this question."),
            "what_would_change_it": ("more cases of this asset_type reaching a filled "
                                     "capacity_affected_kbd, or a query that names fewer constraints"),
            "cases_found": scored})
        return base

    fields_driving = Counter(f for r in scored for f in r["fields_used"])
    base.update({
        "state": "ok", "n": len(scored),
        "reference_class": name_reference_class(exposure, scored, q_type),
        "fields_that_drove_the_match": {f: {"n_cases": c, "share_of_n": round(c / len(scored), 3)}
                                        for f, c in fields_driving.most_common()},
        "status_mix_of_matches": dict(Counter(r["status"] for r in scored)),
        "duration": duration_distribution(scored),
        "price": price_distribution(scored, prices),
        "headline_horizon": f"h{HEADLINE_H}",
        "matches": scored})
    return base


# ------------------------------------------------------------------ rendering: the ninety seconds

def render(r, title):
    """The read as something a person reads in ninety seconds. Every number carries its n."""
    q = r["query"]
    L = [f"# {title}", "",
         f"*`read(exposure) -> distribution` under {r['registration']}. "
         f"Generated by `src/read_exposure.py`; reads the blocks and the price series, writes no table.*", ""]
    if q.get("_supplied_scenario"):
        L += ["> **The exposure below is SUPPLIED BY THE OPERATOR, not a sourced historical record.**",
              "> §4's read takes a hypothetical exposure and answers it from history; the query's own",
              "> numbers are the question, and carry no provenance because they are not claims about",
              "> anything that happened. Everything *after* the query is historical.", ""]
    L += ["## The exposure supplied", "", "| field | value |", "|---|---|"]
    for k in ("asset_name", "asset_type", "operator", "country_iso3", "capacity_nameplate_kbd",
              "capacity_affected_kbd"):
        if S.is_filled(q.get(k)):
            L.append(f"| `{k}` | {q[k]} |")
    ret = r["retrieval"]
    L += ["", f"**Searched {ret['n_cases_searched']} historical cases across every block.**", ""]

    if r["state"] == "no_adequate_precedent":
        L += ["## Result: **NO ADEQUATE PRECEDENT**", "",
              f"**{r['n']} comparable case(s); §4 requires at least {MIN_CASES}.**", "",
              "The corpus does not contain enough comparable exposure to answer this question. This is a",
              "**first-class result registered in advance**, not an error and not an empty read. The",
              "alternative — widening the search until five cases appear — would answer a different",
              "question and not say so.", ""]
        ho = r.get("held_out")
        if ho:
            act = ho["what_actually_happened"]
            L += [f"### What actually happened to `{ho['event_id']}`", "",
                  "Shown *after* the read, and it played no part in it — the case was removed from the",
                  "corpus before its own question was asked.", "",
                  "| field | value |", "|---|---|"]
            for k, v in act.items():
                L.append(f"| `{k}` | {v} |")
            L += ["", "**The read could not have told you this, and says so rather than guessing.** That is",
                  "the point of the held-out test: an instrument that answered here would be answering",
                  "from something other than the evidence.", ""]
        if r["cases_found"]:
            L += ["What was found:", "", "| case | date | similarity | fields compared |", "|---|---|---:|---|"]
            for c in r["cases_found"]:
                L.append(f"| `{c['event_id']}` | {c['date']} | {c['similarity']} | "
                         f"{', '.join(c['fields_used']) or '—'} |")
            L.append("")
        L += [f"**What would change it:** {r['what_would_change_it']}.", "",
              "### Why the other cases were not comparable", "", "| reason | n |", "|---|---:|"]
        for k, v in sorted(ret["excluded"].items(), key=lambda kv: -kv[1]):
            L.append(f"| {k} | {v} |")
        L += ["", f"*{r['not_a_probability']}*", ""]
        return "\n".join(L)

    L += [f"## Reference class: {r['reference_class']}", "", f"**n = {r['n']} comparable cases.**", "",
          "Fields that actually drove the match:", "", "| field | cases | share of n |", "|---|---:|---:|"]
    for f, d in r["fields_that_drove_the_match"].items():
        L.append(f"| `{f}` | {d['n_cases']} | {d['share_of_n']} |")
    L += ["", f"Record quality of the matched cases: {r['status_mix_of_matches']}. "
          f"Partial records are used where the matched fields are present, which is why the n behind "
          f"each distribution below differs and is stated separately.", ""]

    L += ["## Duration distribution", ""]
    for f, d in r["duration"].items():
        cats = ", ".join(f"{k} × {v['n']}" for k, v in d["categories"].items()) or "—"
        qd = d["quantiles_days"]
        L += [f"**`{f}`** — n_matches {d['n_matches']}, of which **{d['n_numeric']} carry a number**.",
              "", f"- categories: {cats}",
              f"- days (n={d['n_numeric']}): " + (f"min {qd['min']}, p25 {qd['p25']}, **median {qd['median']}**, "
                                                 f"p75 {qd['p75']}, max {qd['max']}" if qd else "no numeric values"),
              ""]
    L += ["> `ongoing` and `never` are counted as their own outcomes, not folded into the days. A",
          "> permanently closed refinery is not a long outage; averaging it in would be the same",
          "> error as scoring an undated record as zero.", ""]

    L += [f"## Price and margin distribution across the complex, at h={HEADLINE_H} trading days", "",
          "| target | n | min | p25 | median | p75 | max |", "|---|---:|---:|---:|---:|---:|---:|"]
    for tgt, per_h in r["price"].items():
        d = per_h.get(f"h{HEADLINE_H}")
        if not d:
            continue
        qd = d["quantiles"]
        L.append(f"| {tgt} | {d['n']} | {qd['min']} | {qd['p25']} | **{qd['median']}** | {qd['p75']} | {qd['max']} |")
    any_h = next((p.get(f"h{HEADLINE_H}") for p in r["price"].values() if p.get(f"h{HEADLINE_H}")), None)
    if any_h:
        L += ["", f"*Percent change over {HEADLINE_H} trading days from the event date; the crack rows are "
              f"the product change minus the crude change, in percentage points. These are RAW forward "
              f"changes, not abnormal returns — there is no market model here, and calling them CARs "
              f"would borrow a rigour this read does not have.*", "",
              (f"*The price n ({any_h['n']}) is below the match n ({r['n']}): "
               f"{any_h['n_matches_without_price_data']} matched case(s) predate the price series or "
               f"fall too near its end. The two n's are never conflated -- each distribution above "
               f"carries its own.*"
               if any_h["n_matches_without_price_data"]
               else f"*Every one of the {r['n']} matched cases has price data at this horizon, so the "
                    f"price n equals the match n here. Where it does not, each distribution carries its "
                    f"own n rather than borrowing the match n.*"), ""]
    L += [f"> **{r['not_a_probability']}**", ""]
    return "\n".join(L)


# ------------------------------------------------------------------ the two worked reads

def demo():
    """Two reads, committed so they can be checked: one held-out historical case and one live
    scenario. They deliberately land on the two different registered states."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        cases, prices = load_cases(), load_prices(conn)
    finally:
        conn.close()

    # (1) HELD OUT: Abqaiq 2019, queried with its own exposure and excluded from its own answer.
    abq = next(c for c in cases if c["event_id"] == "abqaiq_attack_2019")
    q1 = {"asset_name": abq["asset_name"], "asset_type": abq["asset_type"],
          "operator": abq.get("operator"), "country_iso3": abq.get("country_iso3"),
          "capacity_nameplate_kbd": abq["capacity_nameplate_kbd"],
          "capacity_affected_kbd": abq["capacity_affected_kbd"]}
    r1 = read(q1, cases=cases, prices=prices, exclude_event_ids={"abqaiq_attack_2019"})
    r1["held_out"] = {"event_id": "abqaiq_attack_2019",
                      "what_actually_happened": {"days_to_partial_restore": abq.get("days_to_partial_restore"),
                                                 "days_to_full_restore": abq.get("days_to_full_restore")},
                      "note": ("The case is removed from the corpus before its own question is asked, so "
                               "nothing here is fitted to the answer.")}

    # (2) LIVE SCENARIO: a strike on Ras Tanura. The query is the operator's hypothesis, not a record.
    q2 = {"asset_name": "Ras Tanura terminal (scenario, not a historical record)",
          "asset_type": "terminal", "operator": "Saudi Aramco", "country_iso3": "SAU",
          "capacity_nameplate_kbd": 6500, "capacity_affected_kbd": 3250,
          "_supplied_scenario": True,
          "_scenario_note": ("A SUPPLIED exposure under §4: half of a 6,500 kb/d terminal offline. These "
                             "two numbers are the QUESTION and carry no provenance because they are not "
                             "claims about anything that happened. Everything the read returns is "
                             "historical. 6,500 kb/d is the operator's stated scenario figure and is NOT "
                             "sourced here -- if it is wrong, the reference class is wrong, and that is "
                             "why the read names the class it retrieved.")}
    r2 = read(q2, cases=cases, prices=prices)

    for r, stem, title in ((r1, "abqaiq_2019_heldout", "READ — Abqaiq 2019, held out"),
                           (r2, "ras_tanura_scenario", "READ — Ras Tanura scenario, 3,250 of 6,500 kb/d offline")):
        (OUT_DIR / f"{stem}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False))
        (OUT_DIR / f"{stem}.md").write_text(render(r, title), encoding="utf-8")
        print(f"  {stem}: state={r['state']} n={r['n']}"
              + (f" ref='{r.get('reference_class')}'" if r["state"] == "ok" else ""))
    return r1, r2


def main():
    if "--demo" in sys.argv or len(sys.argv) == 1:
        print(f"read(exposure) -> distribution  [{REGISTRATION}]")
        demo()
        print(f"  -> {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
