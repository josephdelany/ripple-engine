"""g_chokepoint_register.py -- PHYSICAL_EXPOSURE §2 T2: the chokepoint flow register, Session G.

Registered first, in docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md (2026-09-03) §§4-6.

Every figure below was retrieved in this session's own fetch log from eia.gov and is stored with the
VERBATIM sentence it was read from. Nothing is recalled, nothing is interpolated, and a chokepoint a
release does not quantify is ABSENT from that release -- never zero, never carried forward.

Reading is through src/g_vintage.py, which will not hand over a number without the date you are
claiming to be at. See that module's docstring for why.

Run:  python3 src/g_chokepoint_register.py
Out:  docs/g/CHOKEPOINT_REGISTER.json, docs/g/CHOKEPOINT_T2.json, docs/g/CHOKEPOINT_T2.md
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import g_vintage as V  # noqa: E402

OUT_REG = ROOT / "docs" / "g" / "CHOKEPOINT_REGISTER.json"
OUT_T2 = ROOT / "docs" / "g" / "CHOKEPOINT_T2.json"
OUT_MD = ROOT / "docs" / "g" / "CHOKEPOINT_T2.md"
PW_DIR = ROOT / "data" / "seed" / "ripple"
PW_LAG_DAYS = 7                       # §6: PortWatch's own ~1-week tail lag, applied
PW_WINDOW = 90                        # §6: the 90 days strictly before t

# corpus chokepoint entity -> register key. Entities EIA does not quantify are absent by design.
ENTITY_TO_KEY = {
    "chokepoint.hormuz": "hormuz",
    "chokepoint.bab_el_mandeb": "bab_el_mandeb",
    "chokepoint.suez": "suez",
    "chokepoint.suez_canal": "suez",
    "chokepoint.malacca": "malacca",
    "chokepoint.bosporus": "turkish_straits",
    "chokepoint.turkish_straits": "turkish_straits",
    "chokepoint.panama": "panama",
    "chokepoint.cape_of_good_hope": "cape_of_good_hope",
}
PW_SLUG = {"hormuz": "hormuz", "bab_el_mandeb": "bab_el_mandeb", "suez": "suez",
           "malacca": "malacca", "turkish_straits": "bosporus", "panama": "panama",
           "cape_of_good_hope": "cape_of_good_hope"}
# §6: a route, not a strait -- reported, and excluded from the rank statistic. Registered, not chosen later.
PW_RANK_EXCLUDE = ("cape_of_good_hope",)

R330 = ("EIA Today in Energy #330, 'Maritime chokepoints critical to petroleum markets'",
        "https://www.eia.gov/todayinenergy/detail.php?id=330", "2011-03-02", "2009")
R18991 = ("EIA Today in Energy #18991, 'World oil transit chokepoints critical to global energy security'",
          "https://www.eia.gov/todayinenergy/detail.php?id=18991", "2014-12-01", "2013")
R32352 = ("EIA Today in Energy #32352, 'Three important oil trade chokepoints are located around the Arabian Peninsula'",
          "https://www.eia.gov/todayinenergy/detail.php?id=32352", "2017-08-04", "2016")
R65504 = ("EIA Today in Energy #65504, 'Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint'",
          "https://www.eia.gov/todayinenergy/detail.php?id=65504", "2025-06-16", "2024")
RETRIEVED = "2026-09-03 (session fetch log)"


def _s(rel, value, quote, unit="million b/d", ref=None):
    sid, url, pub, refyr = rel
    return V.stamp(value, unit, pub, ref or refyr, sid, url, RETRIEVED, quote)


def build_register():
    """§4. Four releases. A chokepoint a release does not quantify is ABSENT from it."""
    r = defaultdict(list)
    # --- 2011-03-02, reference year 2009 -------------------------------------------------------
    r["hormuz"].append(_s(R330, 15.5, "15.5 million barrels per day (bbl/d)"))
    r["malacca"].append(_s(R330, 13.6, "13.6 million bbl/d"))
    r["suez"].append(_s(R330, 1.8, "1.8 million bbl/d"))
    r["sumed"].append(_s(R330, 1.1, "approximately 1.1 million bbl/d"))
    r["bab_el_mandeb"].append(_s(R330, 3.2, "3.2 million bbl/d"))
    r["turkish_straits"].append(_s(R330, 2.9, "approximately 2.9 million bbl/d"))
    r["panama"].append(_s(R330, 0.8, "roughly 0.8 million bbl/d"))
    r["danish_straits"].append(_s(R330, 3.3, "3.3 million bbl/d"))
    # §4: Cape of Good Hope is quantified by NO release retrieved. A registered gap, never a zero.
    r["cape_of_good_hope"].append(_s(R330, None,
                                     "the article does not provide a figure for the Cape of Good Hope"))
    # --- 2014-12-01, reference year 2013 -------------------------------------------------------
    r["hormuz"].append(_s(R18991, 17.0, "about 17 million barrels per day traveled through the Strait of Hormuz"))
    r["malacca"].append(_s(R18991, 15.2, "trade through Malacca was 15.2 million barrels per day"))
    r["world_seaborne"].append(_s(
        R18991, 56.5,
        "About 63% (56.5 million barrels per day) of the world's oil production in 2013 moved on maritime routes"))
    # --- 2017-08-04, reference year 2016 (world figure is 2015) --------------------------------
    r["hormuz"].append(_s(R32352, 18.5, "with an oil flow of 18.5 million b/d in 2016"))
    r["suez"].append(_s(R32352, 3.9,
                        "In 2016, 3.9 million b/d of crude oil and refined products transited the Suez Canal in both directions"))
    r["sumed"].append(_s(R32352, 1.6,
                         "In 2016, 1.6 million b/d of crude oil was transported through the SUMED Pipeline"))
    r["bab_el_mandeb"].append(_s(R32352, 4.8,
                                 "An estimated 4.8 million b/d of crude oil and refined petroleum products flowed through this waterway in 2016"))
    r["world_seaborne"].append(_s(
        R32352, 59.0,
        "Nearly 59 million barrels per day (b/d) of global petroleum and other liquids production moved on maritime routes in 2015",
        ref="2015"))
    # --- 2025-06-16, reference year 2024 -------------------------------------------------------
    r["hormuz"].append(_s(R65504, 20.0, "In 2024, oil flow through the strait averaged 20 million barrels per day (b/d)"))
    return dict(r)


# ----------------------------------------------------------------------------- §6 PortWatch

def load_portwatch():
    out = {}
    for key, slug in PW_SLUG.items():
        p = PW_DIR / f"portwatch.{slug}.capacity_tanker.csv"
        if not p.exists():
            continue
        rows = []
        with open(p) as f:
            for row in csv.DictReader(f):
                try:
                    rows.append((dt.date.fromisoformat(row["date"]), float(row["value"])))
                except (ValueError, KeyError):
                    continue
        out[key] = sorted(rows)
    return out


def portwatch_shares(pw, t):
    """§6. Share of the seven-chokepoint PortWatch total over the 90 days strictly before t, with
    PortWatch's own ~1-week publication lag applied so the cross-check obeys the same filtration."""
    td = dt.date.fromisoformat(str(t)[:10])
    hi = td - dt.timedelta(days=PW_LAG_DAYS)
    lo = hi - dt.timedelta(days=PW_WINDOW)
    tot = {}
    for key, rows in pw.items():
        s = sum(v for d, v in rows if lo <= d <= hi)
        if s > 0:
            tot[key] = s
    grand = sum(tot.values())
    if not grand:
        return None, {"window": [lo.isoformat(), hi.isoformat()], "note": "no PortWatch observations in window"}
    return ({k: v / grand for k, v in tot.items()},
            {"window": [lo.isoformat(), hi.isoformat()], "lag_days": PW_LAG_DAYS,
             "unit": "share of seven-chokepoint tanker capacity",
             "limit": ("PortWatch measures transiting tanker capacity (AIS); EIA measures barrels of oil. "
                       "Shares only, never levels; no conversion is asserted.")})


def spearman(a, b):
    import numpy as np
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return None
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    d = float(np.sqrt((ra ** 2).sum() * (rb ** 2).sum()))
    return float((ra * rb).sum() / d) if d > 0 else None


# ----------------------------------------------------------------------------- T2 per event

def corpus_events():
    conn = sqlite3.connect(f"file:{ROOT / 'data' / 'oil.db'}?mode=ro", uri=True)
    try:
        dates = {e: d[:10] for e, d in conn.execute("SELECT event_id, event_date FROM events")}
        ents = defaultdict(set)
        for e, x in conn.execute("SELECT event_id, entity_id FROM event_entities "
                                 "WHERE entity_id LIKE 'chokepoint.%'"):
            ents[e].add(x)
    finally:
        conn.close()
    return dates, ents


def build_t2(reg, dates, ents, pw):
    """§2 T2 = FLOW(k, vintage(t)) / WORLD_SEABORNE(vintage(t)), each term stamped and read through
    g_vintage. Where a term is not knowable at t, T2 is NULL -- never zero, never imputed (§4.1)."""
    rows, excluded = [], []
    for eid in sorted(ents, key=lambda e: dates[e]):
        t = dates[eid]
        for ent in sorted(ents[eid]):
            key = ENTITY_TO_KEY.get(ent)
            if key is None:
                excluded.append({"event_id": eid, "event_date": t, "entity": ent,
                                 "reason": "EIA quantifies no flow for this entity (§4)"})
                continue
            fs, fv = V.latest_value(reg, key, t)
            ws, wv = V.latest_value(reg, "world_seaborne", t)
            terms = {"flow": fs, "world_seaborne": ws}
            share = None
            reason = None
            if fs is None:
                reason = "no release published on or before t quantifies this chokepoint"
            elif fv is None:
                reason = "the latest release covering this chokepoint records a gap, not a figure (§4)"
            elif ws is None or wv in (None, 0):
                reason = "no world seaborne denominator published on or before t (§4.1: null, not imputed)"
            else:
                share = fv / wv
            pws, pwmeta = portwatch_shares(pw, t)
            rows.append({
                "event_id": eid, "event_date": t, "chokepoint": key, "entity": ent,
                "flow_mbd": fv, "world_seaborne_mbd": wv, "T2_share": share,
                "null_reason": reason, "terms": terms, "zeroed_nulls": False,
                "portwatch_share": (None if not pws else pws.get(key)),
                "portwatch_meta": pwmeta,
            })
            if share is None:
                excluded.append({"event_id": eid, "event_date": t, "entity": ent, "reason": reason})
    return rows, excluded


def crosscheck(rows, reg, pw):
    """§6. Rank agreement between the EIA shares and the PortWatch shares, per event date with
    PortWatch coverage. Cape of Good Hope excluded from the statistic by registration, and reported."""
    out = []
    seen = set()
    for r in rows:
        t = r["event_date"]
        if t < "2019-01-01" or t in seen:
            continue
        seen.add(t)
        pws, meta = portwatch_shares(pw, t)
        if not pws:
            continue
        eia = {}
        _ws, wv = V.latest_value(reg, "world_seaborne", t)
        for key in PW_SLUG:
            s, v = V.latest_value(reg, key, t)
            if v is not None and wv:
                eia[key] = v / wv
        common = [k for k in sorted(set(eia) & set(pws)) if k not in PW_RANK_EXCLUDE]
        rho = spearman([eia[k] for k in common], [pws[k] for k in common]) if len(common) >= 3 else None
        out.append({"date": t, "n_common": len(common), "chokepoints": common,
                    "spearman_rank": rho,
                    "eia_share": {k: round(eia[k], 4) for k in sorted(eia)},
                    "portwatch_share": {k: round(pws[k], 4) for k in sorted(pws)},
                    "excluded_from_rank": list(PW_RANK_EXCLUDE), "meta": meta})
    return out


def to_md(o):
    L, a = [], None
    a = L.append
    au, cov = o["filtration_audit"], o["coverage"]
    a("# T2 — the chokepoint flow register, and what the corpus can actually carry")
    a("*Built by `src/g_chokepoint_register.py` under `docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md`,")
    a(f"which was committed first. Generated {o['generated_at']}.*\n")
    a("> **Every value in this study is read through `src/g_vintage.py`, which will not return a")
    a("> number without the date you are claiming to be at.** There is no `.value` accessor and no")
    a("> default `t`. A capacity or flow value that could be read without its publication date would")
    a("> be a schema error, not a documentation lapse.\n")
    a("## 0. The filtration audit — Amendment F.1's standing\n")
    a(f"- terms checked **{au['terms_checked']}** over **{au['rows']}** rows · violations "
      f"**{au['violations']}** · `asserted`: **{au['asserted']}** · study voided: **{au['voided']}**")
    a(f"- {au['rule']}")
    if au["first_violation"]:
        a(f"- first violation: `{json.dumps(au['first_violation'], default=str)}`")
    a("")
    a("## 1. The finding, before the register: T2 is a 25-event variable in a 313-event corpus\n")
    a("| | events |")
    a("|---|---|")
    a(f"| corpus | **{cov['n_events']}** ({cov['span'][0]} … {cov['span'][1]}) |")
    a(f"| predate the first EIA release ({cov['first_release']}) — no T2 term possible | {cov['n_before_first_release']} ({cov['pct_before']}%) |")
    a(f"| name any chokepoint entity | {cov['n_naming_a_chokepoint']} |")
    a(f"| …of which name an entity EIA does not quantify | {cov['n_entity_not_quantified']} |")
    a(f"| …of which predate the first release | {cov['n_named_but_pre_release']} |")
    a(f"| **T2 constructible** | **{cov['n_t2_constructible']}** |")
    a(f"\nAnd the chokepoints the corpus actually names: {json.dumps(cov['entities_named'])}.")
    a(f"**{cov['n_never_named']} of the seven** — {', '.join(cov['never_named'])} — are named by **zero**")
    a("corpus events, so their register entries exist for future use and contribute nothing today.\n")
    a("Whatever T2 shows, it cannot carry a corpus-wide claim. This is a design fact, established")
    a("before any estimate, and it belongs beside §5's verdict words rather than after them.\n")
    a("## 2. The register — four EIA releases, each figure with the sentence it was read from\n")
    a("| chokepoint | published | ref | value (million b/d) | source |")
    a("|---|---|---|---|---|")
    for key, entries in sorted(o["register_full"].items()):
        for e in sorted(entries, key=lambda x: x["published"]):
            val = "**gap — no figure**" if e["value"] is None else f"{e['value']}"
            a(f"| `{key}` | {e['published']} | {e['reference_period']} | {val} | {e['source_id'].split(',')[0]} |")
    a("\n`cape_of_good_hope` is quantified by **no** release retrieved. It is a registered gap, never")
    a("a zero (§4). No figure is carried forward from one release to another, and no denominator is")
    a("back-derived from a rounded share (§4.1).\n")
    a("## 3. T2 per event\n")
    a("| event | date | chokepoint | flow | world seaborne | **T2 share** | if null, why |")
    a("|---|---|---|---|---|---|---|")
    for r in o["t2"]:
        sh = "—" if r["T2_share"] is None else f"**{r['T2_share']:.4f}**"
        a(f"| `{r['event_id']}` | {r['event_date']} | {r['chokepoint']} | "
          f"{'—' if r['flow_mbd'] is None else r['flow_mbd']} | "
          f"{'—' if r['world_seaborne_mbd'] is None else r['world_seaborne_mbd']} | {sh} | "
          f"{r['null_reason'] or ''} |")
    a(f"\n**{o['n_with_share']} of {len(o['t2'])} event-chokepoint rows carry a T2 share.**\n")
    a("## 4. PortWatch cross-check (§6) — shares, never levels; gates nothing\n")
    cc = o["crosscheck"]
    if not cc:
        a("No event date has PortWatch coverage under the registered lag.")
    else:
        a("| date | n chokepoints | Spearman rank (EIA vs PortWatch) |")
        a("|---|---|---|")
        for c in cc:
            rho = c["spearman_rank"]
            a(f"| {c['date']} | {c['n_common']} | " + ("—" if rho is None else f"{rho:+.3f}") + " |")
        a(f"\n{cc[0]['meta']['limit']}")
        a(f"\n`cape_of_good_hope` is excluded from the rank statistic by registration (§6): it is a route,")
        a("not a strait, and a transit count there is not comparable to a chokepoint flow.")
    return "\n".join(L)


def coverage(dates, ents, reg):
    first = min(e["published"] for entries in reg.values() for e in entries)
    named = set(ents)
    not_q = {e for e in named if all(ENTITY_TO_KEY.get(x) is None for x in ents[e])}
    pre = {e for e in named if dates[e] < first}
    seven = set(PW_SLUG)
    used = {ENTITY_TO_KEY[x] for e in named for x in ents[e] if x in ENTITY_TO_KEY}
    ok = {e for e in named if e not in pre and any(x in ENTITY_TO_KEY for x in ents[e])}
    ds = sorted(dates.values())
    return {"n_events": len(dates), "span": [ds[0], ds[-1]], "first_release": first,
            "n_before_first_release": sum(1 for d in dates.values() if d < first),
            "pct_before": round(100 * sum(1 for d in dates.values() if d < first) / len(dates), 1),
            "n_naming_a_chokepoint": len(named), "n_entity_not_quantified": len(not_q),
            "n_named_but_pre_release": len(pre & {e for e in named if any(x in ENTITY_TO_KEY for x in ents[e])}),
            "n_t2_constructible": len(ok),
            "entities_named": {k: sum(1 for e in named for x in ents[e] if x == k)
                               for k in sorted({x for e in named for x in ents[e]})},
            "never_named": sorted(seven - used), "n_never_named": len(seven - used)}


def main():
    reg = build_register()
    dates, ents = corpus_events()
    pw = load_portwatch()
    rows, excluded = build_t2(reg, dates, ents, pw)
    audit = V.filtration_audit(rows)                      # §3, F.1 standing
    out = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "registration": "docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md (2026-09-03)",
        "gates": "nothing; this builds a register and a variable, it estimates nothing.",
        "filtration_audit": audit,
        "coverage": coverage(dates, ents, reg),
        "register_provenance": V.register_summary(reg),
        "register_full": reg,
        "t2": rows, "excluded": excluded,
        "n_with_share": sum(1 for r in rows if r["T2_share"] is not None),
        "crosscheck": crosscheck(rows, reg, pw),
        "portwatch_files": sorted(pw),
    }
    OUT_REG.parent.mkdir(parents=True, exist_ok=True)
    OUT_REG.write_text(V.dumps({"register": reg, "provenance": out["register_provenance"]}))
    OUT_T2.write_text(V.dumps(out))
    OUT_MD.write_text(to_md(out))
    print(V.dumps({k: out[k] for k in ("filtration_audit", "coverage", "n_with_share")}))
    return out


if __name__ == "__main__":
    main()
