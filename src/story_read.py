"""story_read.py -- the Story Page object (NORTH_STAR §2): one development read as a desk reads it.

Order is the desk's order and nothing else is on the page:
  0 significance   -- MATERIAL / IN LINE / NOISE from the market-defined gate (materiality.py)
  1 is it priced?  -- price since knowable vs the analog fan (median, IQR, dated tails); flow side
  2 is it right?   -- the story's claims verbatim, typed and given a measured verdict (ledger.py)
  3 the tail       -- escalation branches from Layer G (escalation.py), then-vs-now table
  4 where it goes  -- measured pass-through per hop for this class, read from data/ripple/irf.json
                     (registered local projections; DESIGN.md Amendment 1). Nulls are shown, never dropped.
  5 trust          -- walk-forward stamp (as computed, labelled), retrieval quality, freshness, sources

Inputs: a pasted headline/paragraph/URL (live) or a corpus event_id (historical, point-in-time).
Every number carries its n and the file/module it came from. Nothing is generated prose.
"""
import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import escalation as ES           # noqa: E402
import ledger as L                # noqa: E402
import materiality as M           # noqa: E402
import propagate as P             # noqa: E402
import reader as R                # noqa: E402  the caged reader (Amendment 3) -- replaces deconstruct/triage here

BRENT = "fred.DCOILBRENTEU"
MONTHLY = "fred.WTISPLC"          # 1946+ monthly spine (BIG_MOVES_REGISTRATION.md Amendment 3)
HORIZON = 20                      # trading days, daily tier
HORIZON_M = 3                     # months, monthly tier
GEO = set(ES.GEO_TYPES)


def _price(conn, sid=BRENT):
    return L._price(conn, sid)


def _domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "") if url else None
    except Exception:
        return None


def _load(name):
    try:
        return json.load(open(DATA / name))
    except Exception:
        return {}


# ----------------------------------------------------------------------------- 1. priced?

def priced(conn, etype, knowable, exclude_event=None):
    """Brent since knowable (simple % from the first trading day on/after) beside the analog fan:
    every class event's +0..+20 trading-day % path -> median, IQR, min/max per day, dated tails."""
    s = _price(conn)
    k = pd.Timestamp(knowable)
    resolution, H, sid = "daily", HORIZON, BRENT
    if k < s.index[0]:                                  # before daily Brent: stand on the monthly spine
        sm = _price(conn, MONTHLY)
        if not sm.empty and k >= sm.index[0]:
            s, resolution, H, sid = sm, "monthly", HORIZON_M, MONTHLY
    pos = s.index.searchsorted(k)
    out = {"series": sid, "knowable": str(k.date()), "horizon_td": H, "resolution": resolution,
           "horizon_label": f"+{H} {'trading days' if resolution == 'daily' else 'months'}"}
    HORIZON_ = H
    if pos >= len(s):
        pos = len(s) - 1                              # live story after the last print: price as of the last observation
        out["price_note"] = f"price series ends {s.index[-1].date()}; path starts at the next refresh"
    if pos < len(s):
        p0 = float(s.iloc[pos])
        path = s.iloc[pos:pos + HORIZON_ + 1]
        out["price_at_knowable"] = round(p0, 2)
        out["price_now"] = round(float(s.iloc[-1]), 2)
        out["as_of"] = str(s.index[-1].date())
        out["path_pct"] = [round(float(v / p0 - 1) * 100, 2) for v in path]
        out["days_elapsed"] = len(path) - 1
        out["complete"] = len(path) == HORIZON_ + 1
    else:
        out.update(price_at_knowable=None, path_pct=[], days_elapsed=0, complete=False)
    paths, tails = [], []
    for eid, d, title in conn.execute("SELECT event_id, event_date, title FROM events WHERE type=?", (etype,)):
        if eid == exclude_event:
            continue
        if pd.Timestamp(d) < s.index[0]:
            continue                                  # predates the price series: no path exists
        p = s.index.searchsorted(pd.Timestamp(d))
        if p >= len(s) or p + HORIZON_ >= len(s) or pd.Timestamp(d) >= k:
            continue                                  # point-in-time: only analogs knowable before k
        q0 = float(s.iloc[p]); arr = (s.iloc[p:p + HORIZON_ + 1].to_numpy() / q0 - 1) * 100
        paths.append(arr); tails.append((eid, d, title, float(arr[-1])))
    if paths:
        A = np.vstack(paths)
        out["fan"] = {"n": len(paths), "median": np.round(np.median(A, 0), 2).tolist(),
                      "p25": np.round(np.percentile(A, 25, 0), 2).tolist(),
                      "p75": np.round(np.percentile(A, 75, 0), 2).tolist(),
                      "min": np.round(A.min(0), 2).tolist(), "max": np.round(A.max(0), 2).tolist()}
        tails.sort(key=lambda t: t[3])
        out["tails"] = {"low": {"event_id": tails[0][0], "date": tails[0][1], "title": tails[0][2], "chg_pct": round(tails[0][3], 1)},
                        "high": {"event_id": tails[-1][0], "date": tails[-1][1], "title": tails[-1][2], "chg_pct": round(tails[-1][3], 1)}}
        if out.get("path_pct"):
            d = out["days_elapsed"]
            med = out["fan"]["median"][d]
            out["now_vs_median_pct"] = round(out["path_pct"][-1] - med, 2)
            up_share = float((A[:, d] > 0).mean())
            out["share_up_at_day"] = round(up_share, 2)
    else:
        out["fan"] = None
    return out


def flow_side(conn, etype):
    pw = _load("portwatch.json")
    prop = P.propagate(conn, event_type=etype) if etype else {}
    return {"chokepoints": [{"chokepoint": c.get("chokepoint"), "flag": c.get("flag"), "pct_of_median": c.get("pct_of_median"),
                             "latest_date": c.get("latest_date")} for c in (pw.get("chokepoints") or [])],
            "flow_now_pct_vs_base": prop.get("flow_now"),
            "realized_disruption_fraction_pct": prop.get("realized_disruption_fraction_pct"),
            "contributing_n": prop.get("contributing_n"),
            "reading": prop.get("reading"), "caveat": prop.get("caveat")}


# ----------------------------------------------------------------------------- 4. where does it travel?
# DESIGN.md §3.1 band 5 + Amendment 1 (2026-09-03). This band used to come from propagate.py, which
# conditioned its contributing events on sr_outcome_90 -- a label retired at κ≈0 (OUTCOME_MAPPING.md
# Amendment 1). Nothing may condition on a retired label, so the band now reads the registered local
# projections instead. This code computes NOTHING: it selects, labels and orders rows that were
# estimated once under the sealed registration (RIPPLE_REGISTRATION.md + Amendments A, B).

RIPPLE_IRF = DATA / "ripple" / "irf.json"
IRF_SPEC, IRF_SAMPLE = "total", "full"    # Amendment 1 A1.1: the only verdict-bearing cut
IRF_MIN_N = 15                            # RIPPLE_REGISTRATION [2.5] MIN_N, quoted in the caption
# Amendment 1 A1.4 -- the hop ladder, in display order. Hop keys are as written in irf.json.
HOP_LADDER = [("0", "crude"), ("1", "refined products & cracks"), ("2", "physical flow & stocks"),
              ("3", "gas & LNG"), ("4", "fertiliser & coal"), ("x", "macro cross-asset"),
              ("e", "equity proxies")]
_IRF = {}


def _irf_doc():
    """Load data/ripple/irf.json once per process (2.6 MB), re-reading only if the file changes."""
    try:
        m = RIPPLE_IRF.stat().st_mtime
    except OSError:
        return None
    if _IRF.get("mtime") != m:
        try:
            _IRF["doc"] = json.loads(RIPPLE_IRF.read_text())
        except Exception:
            return None
        _IRF["mtime"] = m
    return _IRF.get("doc")


def _irf_cell(row):
    """One registered cell at its OWN headline horizon, in the absence language (Amendment 1 A1.2-A1.3).

    The verdict is copied verbatim from the file -- this function never decides one. Colour and caption
    are the registered mapping, so a null looks composed rather than broken (DESIGN.md §2).
    """
    h = next((x for x in row["irf"] if x["h"] == row["headline_h"]), None) or {}
    n, v, fragile = row.get("n_events"), row.get("verdict"), bool(row.get("fragile"))
    if v == "TRANSMITTING":
        state, colour = "excludes_zero", "green"
        caption = ("The 95% interval excludes zero under both standard errors, and the estimate sits "
                   "outside the state-matched placebo band.")
    elif v == "INSUFFICIENT":
        state, colour = "insufficient", "hatch"        # hatched, never coloured: insufficient ≠ null
        caption = f"insufficient (n={n}): below the registered minimum of {IRF_MIN_N} events."
    elif v == "NULL":                                  # the commonest state, and the finding
        state, colour = "crosses_zero", "neutral"
        caption = ("Reported null and flagged fragile: the EHW interval excludes zero, Newey–West does not."
                   if fragile else
                   "The interval crosses zero: no effect distinguishable from none at this sample size.")
    else:
        # The file carries no verdict for this cell. A1.2 says the verdict is verbatim from the file and
        # the band never decides one -- so an absent verdict is reported as absent, NOT captioned as a
        # null. Saying "the interval crosses zero" here would be the desk asserting a result the record
        # does not contain (charter §2 rule 1). Unreachable for the seven corpus classes as the file
        # stands (371/371 cells carry a verdict); it is here so a re-run that drops one is visible.
        state, colour = "no_verdict", "hatch"
        caption = (f"No verdict recorded for this cell in {RIPPLE_IRF.name}: it is shown, uncoloured, "
                   "rather than being reported as a null.")
    return {
        # Evidence tier (Amendment 1 A1.2): the estimate, its band, its n, its verdict
        "node": row["node"], "series_id": row["series_id"], "freq": row["freq"], "h": row["headline_h"],
        "unit": "%" if row["transform"] in ("log", "log1p") else "index points",
        "estimate": h.get("beta"), "lo95": h.get("lo95"), "hi95": h.get("hi95"), "n": n,
        "verdict": v, "fragile": fragile, "state": state, "colour": colour, "caption": caption,
        "zero_line": True,                             # §2: the zero rule is drawn on every cell
        # Provenance tier only -- never the headline band
        "lo90": h.get("lo90"), "hi90": h.get("hi90"), "se_ehw": h.get("se_ehw"), "se_nw": h.get("se_nw"),
        "p_ehw": h.get("p_ehw"), "T": h.get("T"), "transform": row["transform"],
        "placebo_percentile": (row.get("placebo") or {}).get("percentile"),
        "bh_q10_reject": row.get("bh_q10_reject"),
    }


def travel(etype):
    """Band 5, 'Where does it travel?' -- the measured pass-through for this story's class.

    Returns EVERY registered cell for the class (53 of them), nulls included. The band is never
    filtered by verdict or by whether an interval looks interesting: where a hop is null we say so,
    because the absence is the finding (DESIGN.md Amendment 1 A1.1, A1.4).
    """
    src = "data/ripple/irf.json"
    doc = _irf_doc()
    if not doc:
        return {"available": False, "source": src,
                "note": f"{src} not present; run: python3 src/ripple_lp.py"}
    meta = doc.get("meta") or {}
    prov = {"source": src, "registration": meta.get("registration"), "run_when": meta.get("when"),
            "seed": meta.get("seed"), "n_placebo": meta.get("n_placebo"),
            "spec": IRF_SPEC, "sample": IRF_SAMPLE}
    if not etype:
        return {"available": False, **prov,
                "note": "no event class: this band is conditioned on the story's class"}
    rows = [r for r in (doc.get("rows") or [])
            if r.get("shock") == etype and r.get("spec") == IRF_SPEC and r.get("sample") == IRF_SAMPLE]
    if not rows:
        return {"available": False, "shock": etype, **prov,
                "note": f"'{etype}' is not a registered shock set in {src}; no cells were estimated for it"}
    hops, cells = [], []
    for key, label in HOP_LADDER:
        got = [_irf_cell(r) for r in rows if str(r.get("hop")) == key]   # file order = registration order
        if got:
            hops.append({"hop": key, "label": label, "cells": got})
            cells += got
    counts = {k: sum(1 for c in cells if c["verdict"] == k) for k in ("TRANSMITTING", "NULL", "INSUFFICIENT")}
    # a cell the file left unverdicted is counted as such, never folded into NULL (see _irf_cell)
    counts["NO_VERDICT"] = sum(1 for c in cells if c["state"] == "no_verdict")
    counts["FRAGILE"] = sum(1 for c in cells if c["fragile"])
    counts["cells"] = len(cells)
    k = counts["TRANSMITTING"]
    out = {"available": True, "shock": etype, **prov, "hops": hops, "counts": counts, "zero_line": True,
           # Finding tier (A1.4): a count, never an adjective. k=0 is stated in words, not left blank.
           "finding": (f"No cell transmits for this class: all {counts['cells']} registered cells are "
                       f"null or insufficient." if k == 0 else
                       f"{k} of {counts['cells']} registered cells transmit for this class."),
           "label": ("lag-augmented local projections, 95% EHW HC1 band, placebo-controlled against "
                     f"{meta.get('n_placebo')} state-matched pseudo-events; verdicts TRANSMITTING / "
                     "NULL / INSUFFICIENT as registered"),
           "caveat": ("Every registered cell for this class is shown, nulls included: the band is never "
                      "filtered by verdict (DESIGN.md Amendment 1 A1.1).")}
    if len(cells) != len(rows):        # a new hop key in the registration must not silently drop rows
        out["note"] = (f"{len(rows) - len(cells)} of {len(rows)} cells sit outside the registered hop "
                       f"ladder and are NOT shown; extend HOP_LADDER (DESIGN.md Amendment 1 A1.4)")
    return out


# ----------------------------------------------------------------------------- 3. branches

def branches(conn, etype, event_id=None, entities=None, as_of=None):
    if etype not in GEO:
        return {"applicable": False, "note": f"'{etype}' is not a geopolitical class; escalation branches do not apply."}
    if event_id:
        r = ES.read_event(conn, event_id, as_of=as_of)
        basis_note = "conditioned on the event's coded situation record (point-in-time)"
    else:
        target = {"event_id": None, "type": etype, "actor": "unknown", "target": "unknown", "conflict_scope": "unknown",
                  "tempo": "unknown", "diplomatic": "unknown", "alliance": "unknown", "target_capacity": "unknown",
                  "prior_dyad": "unknown", "propensity": None}
        # a live story carries no coded situation fields yet -> class-only conditioning, said so
        for e in entities or []:
            if e.startswith("country.") and target["target"] == "unknown":
                target["target"] = e
        r = ES.read(conn, target, as_of=as_of)
        basis_note = "live story: situation fields not yet coded -> conditioned on class" + (" + target" if target["target"] != "unknown" else "") + " only"
    r["basis_note"] = basis_note
    # Brief A-2 (2026-09-02): sr_outcome_90 is RETIRED (OUTCOME_MAPPING.md Amendment 1). The corpus-derived branch rates
    # stay on the page only under the retired label; the live read is the IES-90 distribution from the engine block
    # (story["engine"]["G"], added by read() below once the engine block exists).
    r["outcome_label"] = "retired: sr_outcome_90, κ≈0 vs ICB/MID/UCDP (OUTCOME_MAPPING.md Amendment 1, 2026-09-02) — corpus-derived, not an outcome"
    r["retired"] = True
    r["applicable"] = True
    return r


# ----------------------------------------------------------------------------- 1b. what the market already knew (CLAIM_LEDGER_REGISTRATION Amendment 5)

def _pct_at(conn, sid, k, lag_days):
    """Percentile of the last print dated <= k - lag among all prints <= that date; unknown before the series starts."""
    s = _price(conn, sid)
    if s.empty:
        return {"value": None, "status": "unknown", "note": f"{sid} not held"}
    cut = pd.Timestamp(k) - pd.Timedelta(days=lag_days)
    h = s[s.index <= cut]
    if h.empty:
        return {"value": None, "status": "unknown", "note": f"{sid} starts {s.index[0].date()}", "series": sid}
    v = float(h.iloc[-1])
    return {"value": round(v, 2), "percentile": round(float((h < v).mean() * 100), 1), "as_of": str(h.index[-1].date()),
            "vintage": str((h.index[-1] + pd.Timedelta(days=lag_days)).date()), "n": int(len(h)), "series": sid, "status": "ok"}


def priced_in(conn, knowable):
    """Display fields only (Amendment 5): never scored, never gated."""
    k = pd.Timestamp(knowable)
    out = {"label": "what the market already knew at the knowable date (display fields, CLAIM_LEDGER_REGISTRATION.md Amendment 5; not scored)",
           "knowable": str(k.date())}
    row = conn.execute("SELECT obs_date, value, vintage FROM state_panel WHERE field='curve_m1_m4_spread' AND entity_id='world' AND vintage<=? ORDER BY obs_date DESC LIMIT 1",
                       (str(k.date()),)).fetchone()
    if row and (k - pd.Timestamp(row[0])).days > 30:
        out["curve_front_spread_m1_m4"] = {"value": None, "status": "unknown", "note": f"last NYMEX curve print {row[0]} is more than 30 days before the knowable date (series ends 2024-04-05; session C's loader not landed)"}
    else:
        out["curve_front_spread_m1_m4"] = ({"value": round(row[1], 2), "as_of": row[0], "vintage": row[2], "unit": "USD/bbl", "series": "state_panel curve_m1_m4_spread", "status": "ok"}
                                           if row else {"value": None, "status": "unknown", "note": "no NYMEX curve print with vintage <= knowable (series 1983-04..2024-04)"})
    out["curve_slope_1_3"] = {"value": None, "status": "unknown", "note": "contracts 1-3 not held; session C's NYMEX loader (handoff C_to_A) not landed"}
    out["ovx_percentile"] = _pct_at(conn, "fred.OVXCLS", k, 3)
    out["cot_managed_money_net_percentile"] = _pct_at(conn, "cftc.mm_net_wti", k, 3)
    return out


# ----------------------------------------------------------------------------- 3b. the state-vector engine (PATH Step 7)

_ENGINE = {}


def _engine_block(event_id, knowable):
    """engine.read for a corpus event, point-in-time; slimmed for the page. Never raises."""
    try:
        import engine.read as R
        import engine.similarity as S
        from _db import connect
        m = DB.stat().st_mtime
        if _ENGINE.get("mtime") != m:
            _ENGINE["corpus"] = R.Corpus.from_db(connect(read_only=True)); _ENGINE["mtime"] = m
        c = _ENGINE["corpus"]
        if event_id not in c.by_id:
            return {"available": False, "note": "event not in the engine corpus"}
        w = S.load_menu()["items"][0]
        r = R.read(c, c.by_id[event_id], as_of=str(pd.Timestamp(knowable).date()), weighting=w)
        keep = ("event_id", "date", "as_of", "tier", "k", "threshold", "max_similarity", "conditioned_n", "state", "no_adequate_precedent",
                "G", "P", "F", "M", "block_contributions", "note")
        out = {k_: r.get(k_) for k_ in keep}
        out["analogs"] = [{k_: a.get(k_) for k_ in ("event_id", "date", "title", "type", "similarity", "outcome", "deal", "n_compared", "n_unknown")}
                          for a in (r.get("analogs") or [])]
        out["differencing"] = (r.get("differencing") or [])[:3]
        prop = r.get("propagation") or {}
        out["propagation"] = {k_: v for k_, v in prop.items() if k_ in ("ALL", "caveat")}
        out["available"] = True
        out["weighting"] = w["id"]
        out["label"] = "state-vector similarity over the coded situation record + market state, point-in-time; G = IES-90 levels (independent dated codings)"
        return out
    except Exception as e:                                                # the page must render even if the engine cannot
        return {"available": False, "note": f"engine unavailable: {e.__class__.__name__}"}


# ----------------------------------------------------------------------------- 5. trust

def _wf_rows(wf):
    """Brief A-2: the trust rows, every value straight from data/walk_forward/summary.json (tiers.daily + top level)."""
    d = (wf.get("tiers") or {}).get("daily") or {}
    g = ((d.get("G") or {}).get("engine_vs") or {}).get("climatology") or {}
    p = ((d.get("P") or {}).get("engine_vs") or {}).get("climatology") or {}
    spa = (d.get("G") or {}).get("spa") or {}
    pl = (wf.get("placebo") or {}).get("vs_random_analogs") or {}
    perm = wf.get("permutation") or {}
    rules = (wf.get("verdict") or {}).get("rules") or {}
    rows = [
        {"metric": "G Brier skill vs climatology", "value": g.get("skill"), "ci95": g.get("ci95"), "dm_p": g.get("dm_p"), "n": g.get("n"), "path": "tiers.daily.G.engine_vs.climatology"},
        {"metric": "G SPA p (best of the menu vs climatology)", "value": spa.get("p_spa"), "best_model": spa.get("best_model"), "n": spa.get("T"), "path": "tiers.daily.G.spa"},
        {"metric": "P CRPS skill vs climatology", "value": p.get("skill"), "ci95": p.get("ci95"), "dm_p": p.get("dm_p"), "n": p.get("n"), "path": "tiers.daily.P.engine_vs.climatology"},
        {"metric": "Placebo skill (size-matched, vs random analogs)", "value": pl.get("skill"), "ci95": pl.get("ci95"), "covers_zero": pl.get("covers_zero"), "path": "placebo.vs_random_analogs"},
        {"metric": "Permutation p (G skill vs label shuffles)", "value": perm.get("p_value"), "n": perm.get("n_reads"), "path": "permutation.p_value"},
    ]
    return rows, {"engine:G": (rules.get("engine:G") or {}).get("status"), "engine:P": (rules.get("engine:P") or {}).get("status")}


def trust(conn, etype, br):
    wf = _load("walk_forward/summary.json")
    st = _load("engine_status.json")
    rows, statuses = _wf_rows(wf)
    run_id = wf.get("run_id")
    return {"walk_forward": {"rows": rows, "statuses": statuses, "run_id": run_id, "verdict": wf.get("verdict"), "protocol": wf.get("protocol"),
                             "n_scored_daily": ((wf.get("tiers") or {}).get("daily") or {}).get("n_scored_burn_in"),
                             "label": f"IES-90 (ICB/MID/War/UCDP), run {run_id}, protocol §7"},
            "retrieval": {"conditioned_n": (br or {}).get("conditioned_n"), "basis": ((br or {}).get("branch_rates") or {}).get("basis"),
                          "no_adequate_precedent": (br or {}).get("no_adequate_precedent")},
            "freshness": {"status": st.get("status") or st.get("light"), "as_of": st.get("as_of") or st.get("generated_at")}}


# ----------------------------------------------------------------------------- the read

def read(arg=None, event_id=None, knowable=None, log=True):
    conn = sqlite3.connect(DB)
    try:
        if event_id:
            row = conn.execute("SELECT event_id, event_date, type, title, description, source_url FROM events WHERE event_id=?",
                               (event_id,)).fetchone()
            if not row:
                return {"error": f"unknown event {event_id}"}
            eid, edate, etype, title, desc, url = row
            text = f"{title}. {desc or ''}"
            ents = [r[0] for r in conn.execute("SELECT entity_id FROM event_entities WHERE event_id=?", (eid,))]
            knowable = edate
            # the coded class is the corpus's, never the model's; the reader only supplies typed claims
            rr = R.read_story(text, class_hint=etype, conn=conn)
            source = _domain(url); was_url = False; scope = None; article_type = "corpus event"
            story_id = f"event:{eid}"
            entity_ok = True                                  # an admitted corpus event passed the human gate
        else:
            rr = R.read_story(arg, conn=conn)
            etype = rr["event_class"]
            ents = [e["id"] for e in rr["entities"]]
            url = rr["url"]; title = rr["title"]; desc = None
            source = _domain(url) or "pasted"; was_url = rr["was_url"]; scope = None if etype else "off_topic"
            article_type = "live story"
            knowable = knowable or date.today().isoformat()
            story_id = "live:" + L._cid(source or "pasted", (arg or "")[:400])
            eid = None
            entity_ok = bool(rr["qualifying_entities"])
        cs = rr["claims"]
        k = pd.Timestamp(knowable)
        gate = M.gate(etype)
        if gate["significance"] == "MATERIAL" and not entity_ok:       # Amendment 3 rule 5: entity-aware gate
            gate = {**gate, "significance": "IN_LINE", "flags": list(gate.get("flags") or []) + ["no_entity"],
                    "why": gate["why"] + " Shown IN LINE: no tracked petro entity in an actor/target/asset/chokepoint role."}
        att = M.attention(ents)
        flags = M.flags_for(gate["significance"], att.get("score"))
        pr = priced(conn, etype, k, exclude_event=eid) if etype else {"fan": None, "knowable": str(k.date())}
        br = branches(conn, etype, event_id=eid, entities=ents, as_of=str(k.date()) if eid else None) if etype else {"applicable": False, "note": "no event class"}
        p0 = pr.get("price_at_knowable")
        claims = []
        for t in cs:                                              # already typed + caged by the reader
            t["event_class"] = t.get("event_class") or etype
            if pr.get("resolution") == "monthly" and t.get("series") in (None, BRENT):
                t["series"] = MONTHLY                                    # stand on the monthly spine, say so
            v = L.verdict_for(conn, t, price_at_knowable=p0, as_of=str(k.date()) if eid else None,
                              escalation_read=br if br.get("applicable") else None)
            if pr.get("resolution") == "monthly" and v.get("basis"):
                v["basis"] += " — monthly resolution"
            t["verdict"] = v
            claims.append(t)
        story = {
            "story_id": story_id, "event_id": eid, "title": title, "description": desc, "url": url, "source": source,
            "article_type": article_type, "scope": scope, "was_url": was_url,
            "knowable": str(k.date()), "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event_class": etype, "entities": ents,
            "roles": rr["entities"], "unmapped": rr["unmapped"], "qualifying_entities": rr["qualifying_entities"],
            "reader": rr["reader"], "rejected": rr["rejected"],
            "significance": {**gate, "attention": att, "flags": flags},
            "priced": pr,
            "priced_in": priced_in(conn, k),
            "flow": flow_side(conn, etype) if etype else {},
            "claims": claims,
            "n_checkable": sum(1 for c in claims if c["checkable"]),
            "branches": br,
            # DESIGN.md §3.1 band 5 + Amendment 1: the registered local projections for this class,
            # every cell including the nulls. Nothing here conditions on the retired sr_outcome_90.
            "propagation": travel(etype),
            "trust": trust(conn, etype, br),
            "engine": _engine_block(eid, k) if eid else {"available": False,
                                                          "note": "live stories are read on class + entities; the state-vector engine needs a coded situation record (PATH Step 9)"},
            "sources_board": [b for b in L.scoreboards(conn)["sources"] if b["source"] == source],
            "registrations": ["CLAIM_LEDGER_REGISTRATION.md", "BIG_MOVES_REGISTRATION.md", "PRE_REGISTRATION_V2.md"],
        }
        # Brief A-2: the live escalation read is the IES-90 distribution among the engine's analogs (independent dated
        # codings), shown beside the retired corpus-derived rates, with n. Absent when the engine block is unavailable.
        eg = (story.get("engine") or {}).get("G") if isinstance(story.get("engine"), dict) else None
        if isinstance(story.get("branches"), dict) and story["branches"].get("applicable"):
            if isinstance(eg, dict) and eg.get("n"):
                story["branches"]["ies90"] = {"n": eg.get("n"), "counts": eg.get("counts"), "rates": eg.get("rates"), "levels": eg.get("levels"),
                                              "deal": eg.get("deal"), "source": "event_outcomes source='ies90' (OUTCOME_MAPPING.md Amendments 1-2)",
                                              "label": f"IES-90 level frequencies among the engine's analogs, n={eg.get('n')} (live read; independent dated codings)"}
            else:
                story["branches"]["ies90"] = {"n": 0, "label": "IES-90 read unavailable: " + str((story.get("engine") or {}).get("note") or "engine block absent")}
        if log and not eid:
            story["ledger_ids"] = L.log_claims(story_id, source, k.date(), claims, price_at_knowable=p0, url=url)
        if not eid:
            # persist the live story's context so the Challenge loop can rebuild its target later (Amendment 4)
            sd = DATA / "reader" / "stories"
            sd.mkdir(parents=True, exist_ok=True)
            (sd / f"{story_id.replace(':', '_')}.json").write_text(json.dumps(
                {"story_id": story_id, "title": title, "event_class": etype, "entities": ents, "knowable": str(k.date()),
                 "url": url, "read_at": story["read_at"]}, ensure_ascii=False))
        return story
    finally:
        conn.close()


def _print(s):
    sig = s["significance"]
    print(f"\n{s['title'][:90]}\n  class={s['event_class']} knowable={s['knowable']} source={s['source']}")
    print(f"  SIGNIFICANCE {sig['significance']} {sig.get('flags')} -- {sig.get('why')}")
    pr = s["priced"]
    if pr.get("fan"):
        print(f"  PRICED: Brent {pr['price_at_knowable']} at knowable; +{pr['days_elapsed']}d path {pr['path_pct'][-1]:+.1f}% "
              f"vs analog median {pr['fan']['median'][pr['days_elapsed']]:+.1f}% (n={pr['fan']['n']}); tails "
              f"{pr['tails']['low']['chg_pct']}% ({pr['tails']['low']['date'][:4]}) .. {pr['tails']['high']['chg_pct']}% ({pr['tails']['high']['date'][:4]})")
    fl = s["flow"]
    print(f"  FLOW: realized disruption {fl.get('realized_disruption_fraction_pct')}% of {fl.get('contributing_n')}; now {fl.get('flow_now_pct_vs_base')}")
    for c in s["claims"]:
        v = c["verdict"]
        print(f"  CLAIM [{c['kind']:11s}] {v['verdict']:12s} r={v.get('r')} n={v.get('n')} :: {c['text'][:80]}")
    b = s["branches"]
    if b.get("applicable"):
        br = b.get("branch_rates") or {}
        print(f"  BRANCHES ({br.get('basis')}, n={br.get('n')}): {br.get('counts')} -- {b.get('basis_note')}")
        for a in (b.get("analogs") or [])[:3]:
            print(f"    analog {a['date']} sim={a['similarity']} {a['outcome_90']} :: {a['title'][:60]}")
    tv = s["propagation"]
    if tv.get("available"):
        print(f"  TRAVEL: {tv['finding']}  [{tv['source']}]")
        for hop in tv["hops"]:
            for c in hop["cells"]:
                est = f"{c['estimate']:+.3f}{c['unit'][0] if c['unit'] == '%' else ''}" if c["estimate"] is not None else "no estimate"
                band = f"[{c['lo95']:+.3f}, {c['hi95']:+.3f}]" if c["lo95"] is not None else "no band"
                flag = " (FRAGILE)" if c["fragile"] else ""
                print(f"    hop {hop['hop']:<2} {c['node']:<24} {est:>12} {band:>22} "
                      f"n={c['n']:<3} {c['verdict']}{flag}")
    else:
        print(f"  TRAVEL: unavailable -- {tv.get('note')}")
    print(f"  TRUST: {s['trust']['walk_forward']['verdict']}")


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "abqaiq_attack_2019"
    s = read(event_id=a) if not a.strip().startswith(("http", " ")) and " " not in a.strip() else read(arg=a, log=False)
    _print(s)
