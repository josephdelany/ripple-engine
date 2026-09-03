"""ledger.py -- the Claim Ledger (NORTH_STAR §4, spec §7.1, A9).

Every checkable claim the engine reads is appended, point-in-time, to
data/ledger/claims.jsonl with its verdict; at horizon it resolves FROM DATA
(price series) or from subsequent corpus events (escalation) -- never by hand.
Rules: CLAIM_LEDGER_REGISTRATION.md §2-§4. Nothing here is edited after it is
written; corrections are new rows.

Public surface:
  type_claim(sentence, event_class, entities, modality)  -> typed claim (pure)
  verdict_for(conn, ret, claim, price_at_knowable)       -> verdict (measured)
  log_claims(story_id, source, knowable, claims)         -> ids
  resolve(conn)                                          -> n newly resolved
  scoreboards(conn)                                      -> the three boards
"""
import hashlib
import json
import re
import sqlite3
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
LEDGER_DIR = DATA / "ledger"
CLAIMS = LEDGER_DIR / "claims.jsonl"
RESOLUTIONS = LEDGER_DIR / "resolutions.jsonl"

SUPPORTED, MIXED, UNSUPPORTED = 0.60, 0.40, 0.40
MIN_N = 8
PRICE_HORIZON_TD = 20            # trading days
ESCALATION_HORIZON_CD = 90       # calendar days
LEVEL_TOL = 0.0                  # a level claim resolves true if the level is touched at or before horizon

UP = re.compile(r"\b(soar|surge|spike|jump|rally|climb|rise|rising|higher|gain|push(?:ed|es)? (?:up|higher|past|above|toward)|top|breach|exceed|above|past \$|beyond \$)\b", re.I)
DOWN = re.compile(r"\b(plunge|fall|falling|drop|slide|collapse|tumble|sink|lower|decline|slump|crash|ease|below|back toward|toward \$?[0-9]{2}\b)\b", re.I)
LEVEL = re.compile(r"\$\s?(\d{2,3})(?:\s?(?:a|per)\s?barrel|/bbl|/b)?", re.I)
ASSET = [
    ("brent", re.compile(r"\b(brent|oil|crude|barrel|wti|petroleum)\b", re.I), "fred.DCOILBRENTEU"),
    ("diesel_crack", re.compile(r"\b(diesel|distillate|jet fuel|gasoil|refining margin|crack spread)\b", re.I), "derived.diesel_crack"),
    ("gas", re.compile(r"\b(lng|natural gas|henry hub|ttf|jkm|gas price)\b", re.I), "fred.DHHNGSP"),
    ("fertilizer", re.compile(r"\b(fertili[sz]er|urea|ammonia|nitrogen)\b", re.I), "fred.PCU325311325311"),
    ("freight", re.compile(r"\b(freight|tanker rate|shipping rate|vlcc|insurance premium)\b", re.I), None),
]
FLOW = re.compile(r"\b(halt|halts|halted|stop|stops|stopped|shut|shuts|cut off|block|blocks|blocked|close|closes|closed|closure|reroute|suspend|resume|resumes|reopen)\b.*\b(export|exports|shipping|tanker|transit|flows?|barrels|production|output|strait|canal|pipeline)\b|\b(export|exports|shipping|tankers?|transits?|flows?|production|output|strait|canal|pipeline)\b.*\b(halt|halts|halted|stop|stops|stopped|shut|shuts|cut off|block|blocks|blocked|close|closes|closed|closure|reroute|suspend|resume|resumes|reopen)\b", re.I)
ESC = re.compile(r"\b(retaliat\w*|escalat\w*|strike back|respond militarily|widen\w*|regional war|all-out war|attack\w* (?:on|against)|close the strait|target\w* (?:shipping|tankers|gulf)|hit back|counterattack\w*)\b", re.I)
MODAL = re.compile(r"\b(will|would|could|may|might|likely|expected|expect|threaten\w*|vow\w*|warn\w*|plan\w*|poised|set to|risk of|raises? the risk)\b", re.I)
ESC_STRONG = re.compile(r"\b(retaliat\w*|escalat\w*|hit back|strike back|counterattack\w*|close the strait|widen\w*)\b", re.I)
POLICY = re.compile(r"\b(opec\+?|spr|strategic petroleum reserve|emergency release|production cut|output cut|quota|ceasefire|sanctions? (?:relief|lifted|waiver))\b", re.I)


CLAUSE_SPLIT = re.compile(r",\s*(?:and|but|while|as)\s+|;\s+", re.I)


def split_clauses(sentence):
    """Split a compound sentence into clauses when more than one claim signal is present, so
    'Iran will retaliate, and fertilizer prices will spike' yields two typed claims. Pure."""
    parts = [p.strip() for p in CLAUSE_SPLIT.split(sentence) if p and p.strip()]
    if len(parts) < 2:
        return [sentence.strip()]
    signals = sum(1 for p in parts if ESC.search(p) or FLOW.search(p) or (_asset(p)[0] and (UP.search(p) or DOWN.search(p))))
    return parts if signals >= 2 else [sentence.strip()]


def _asset(sentence):
    for key, pat, sid in ASSET:
        if pat.search(sentence):
            return key, sid
    return None, None


def type_claim(sentence, event_class=None, entities=None, modality="asserted"):
    """Type one verbatim sentence per CLAIM_LEDGER_REGISTRATION.md §2. Pure; unit-tested.
    Returns dict(kind, asset, series, direction, level, horizon, checkable, why)."""
    s = sentence.strip()
    asset, sid = _asset(s)
    lvl = LEVEL.search(s)
    up, down = bool(UP.search(s)), bool(DOWN.search(s))
    base = {"text": s, "event_class": event_class, "modality": modality, "entities": entities or []}
    if ESC.search(s) and (MODAL.search(s) or ESC_STRONG.search(s)) and not (asset and (up or down)):
        return {**base, "kind": "escalation", "asset": "escalation", "series": None, "direction": "escalate",
                "level": None, "horizon_days": ESCALATION_HORIZON_CD, "horizon_unit": "calendar",
                "checkable": True, "why": "escalation claim between actors; resolves on +90d corpus outcome"}
    if FLOW.search(s):
        return {**base, "kind": "flow", "asset": asset or "brent", "series": sid or "fred.DCOILBRENTEU",
                "direction": "disrupt", "level": None, "horizon_days": PRICE_HORIZON_TD, "horizon_unit": "trading",
                "checkable": True, "why": "flow claim (barrels/transits stop or resume); price proxy until flow history exists"}
    if asset and lvl and (up or down or True):
        level = float(lvl.group(1))
        return {**base, "kind": "level", "asset": asset, "series": sid, "direction": "up" if not down else "down",
                "level": level, "horizon_days": PRICE_HORIZON_TD, "horizon_unit": "trading",
                "checkable": True, "why": f"level claim: ${level:.0f} on {asset} within +20 trading days"}
    if asset and (up != down):
        return {**base, "kind": "direction", "asset": asset, "series": sid, "direction": "up" if up else "down",
                "level": None, "horizon_days": PRICE_HORIZON_TD, "horizon_unit": "trading",
                "checkable": bool(sid), "why": f"direction claim on {asset} at +20 trading days" if sid else "asset has no series yet"}
    if POLICY.search(s):
        return {**base, "kind": "policy", "asset": "policy", "series": None, "direction": None, "level": None,
                "horizon_days": ESCALATION_HORIZON_CD, "horizon_unit": "calendar", "checkable": False,
                "why": "policy claim; checkable only against a dated action entering the corpus (PENDING)"}
    return {**base, "kind": "uncheckable", "asset": asset, "series": sid, "direction": None, "level": None,
            "horizon_days": None, "horizon_unit": None, "checkable": False,
            "why": "no asset + direction/level + horizon in the sentence"}


# ----------------------------------------------------------------------------- measured verdicts

def _price(conn, sid):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                     "ORDER BY obs_date, as_of", conn, params=(sid,))
    df = df.drop_duplicates("obs_date", keep="last")
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    return df.set_index("obs_date")["value"].astype(float)


def class_outcomes(conn, event_class, sid="fred.DCOILBRENTEU", horizon=PRICE_HORIZON_TD, as_of=None):
    """For every corpus event of the class: simple % change of the series from the first
    trading day on/after the event date to +horizon trading days. Point-in-time if as_of."""
    s = _price(conn, sid)
    if len(s) > 10 and (s.index[-1] - s.index[0]).days / len(s) > 3:
        horizon = 3                       # monthly series: three observations (~one quarter), stated on the card
    q = "SELECT event_id, event_date, title FROM events WHERE type=?"
    args = [event_class]
    if as_of:
        q += " AND event_date < ?"; args.append(str(as_of))
    out = []
    for eid, d, title in conn.execute(q, args):
        if pd.Timestamp(d) < s.index[0]:
            continue                      # event predates the series: no outcome exists (never the series' first window)
        pos = s.index.searchsorted(pd.Timestamp(d))
        if pos + horizon >= len(s) or pos >= len(s):
            continue
        p0, p1 = float(s.iloc[pos]), float(s.iloc[pos + horizon])
        path = (s.iloc[pos:pos + horizon + 1].to_numpy() / p0 - 1) * 100
        out.append({"event_id": eid, "date": d, "title": title, "chg_pct": round((p1 / p0 - 1) * 100, 2),
                    "max_pct": round(float(path.max()), 2), "min_pct": round(float(path.min()), 2)})
    return out


def _is_daily(conn, sid):
    s = _price(conn, sid)
    return not (len(s) > 10 and (s.index[-1] - s.index[0]).days / len(s) > 3)


def _cut(r, n):
    if n < MIN_N:
        return "THIN"
    if r >= SUPPORTED:
        return "SUPPORTED"
    if r <= UNSUPPORTED:
        return "UNSUPPORTED"
    return "MIXED"


def verdict_for(conn, claim, price_at_knowable=None, as_of=None, escalation_read=None):
    """Measured verdict for a typed claim (registration §3). Returns dict(verdict, r, n, k, basis, bar)."""
    ec = claim.get("event_class")
    if not claim.get("checkable"):
        return {"verdict": "UNCHECKABLE", "r": None, "n": None, "k": None, "basis": claim.get("why")}
    if not ec:
        return {"verdict": "NO PRECEDENT", "r": None, "n": 0, "k": 0, "basis": "story maps to no event class"}
    kind = claim["kind"]
    if kind == "escalation":
        er = escalation_read or {}
        br = er.get("branch_rates") or {}
        n = br.get("n") or 0
        rates = br.get("rates") or {}
        r = (rates.get("LIMITED_RETALIATION") or 0) + (rates.get("WIDENING") or 0)
        if er.get("no_adequate_precedent"):
            return {"verdict": "NO PRECEDENT", "r": None, "n": 0, "k": 0, "basis": "no adequate geopolitical precedent"}
        return {"verdict": _cut(r, n), "r": round(r, 3), "n": n, "k": int(round(r * n)),
                "basis": f"{br.get('basis', 'class')} +90d outcomes (corpus-derived)", "bar": _bar_escalation(br)}
    sid = claim.get("series") or "fred.DCOILBRENTEU"
    outs = class_outcomes(conn, ec, sid=sid, as_of=as_of)
    n = len(outs)
    if n == 0:
        return {"verdict": "NO PRECEDENT", "r": None, "n": 0, "k": 0, "basis": f"no {ec} events with {sid} history"}
    if kind == "direction":
        k = sum(1 for o in outs if (o["chg_pct"] > 0) == (claim["direction"] == "up"))
    elif kind == "level":
        if not price_at_knowable:
            return {"verdict": "UNCHECKABLE", "r": None, "n": n, "k": None, "basis": "no price at knowability"}
        need = (claim["level"] / price_at_knowable - 1) * 100
        claim["direction"] = "up" if need >= 0 else "down"        # a level above the current price is an up-claim
        k = sum(1 for o in outs if (o["max_pct"] >= need if need >= 0 else o["min_pct"] <= need))
        claim["implied_move_pct"] = round(need, 1)
    elif kind == "flow":
        k = sum(1 for o in outs if abs(o["chg_pct"]) >= 10)
    else:
        return {"verdict": "UNCHECKABLE", "r": None, "n": n, "k": None, "basis": claim.get("why")}
    r = k / n
    return {"verdict": _cut(r, n), "r": round(r, 3), "n": n, "k": k,
            "basis": f"{ec} events, {sid.split('.')[-1]} at +{PRICE_HORIZON_TD} trading days" if len(outs) and _is_daily(conn, sid) else f"{ec} events, {sid.split('.')[-1]} at +3 months",
            "bar": _bar_price(outs)}


def _bar_price(outs):
    n = len(outs)
    dn = sum(1 for o in outs if o["chg_pct"] <= -2)
    up = sum(1 for o in outs if o["chg_pct"] >= 2)
    flat = n - dn - up
    tails = sorted(outs, key=lambda o: o["chg_pct"])
    return {"down": dn, "flat": flat, "up": up, "n": n,
            "tails": [{"date": tails[0]["date"], "title": tails[0]["title"], "chg_pct": tails[0]["chg_pct"]},
                      {"date": tails[-1]["date"], "title": tails[-1]["title"], "chg_pct": tails[-1]["chg_pct"]}] if n else []}


def _bar_escalation(br):
    c = br.get("counts") or {}
    return {"contained": c.get("CONTAINED", 0) + c.get("RESOLUTION_BY_DEAL", 0),
            "escalated": c.get("LIMITED_RETALIATION", 0) + c.get("WIDENING", 0), "n": br.get("n", 0)}


# ----------------------------------------------------------------------------- the log

def _cid(story_id, text):
    return hashlib.sha1(f"{story_id}|{text}".encode()).hexdigest()[:12]


def log_claims(story_id, source, knowable, claims, price_at_knowable=None, url=None):
    """Append checkable claims (and uncheckable ones, for the record) point-in-time. Idempotent
    per (story, sentence): re-reading a story does not duplicate rows."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    existing = {r["claim_id"] for r in _rows(CLAIMS)}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ids = []
    with open(CLAIMS, "a", encoding="utf-8") as f:
        for c in claims:
            cid = _cid(story_id, c["text"])
            ids.append(cid)
            if cid in existing:
                continue
            row = {"claim_id": cid, "story_id": story_id, "source": source, "url": url, "logged_at": now,
                   "knowable": str(knowable)[:10], "price_at_knowable": price_at_knowable,
                   "text": c["text"], "kind": c["kind"], "asset": c.get("asset"), "series": c.get("series"),
                   "direction": c.get("direction"), "level": c.get("level"), "modality": c.get("modality"),
                   # Amendment 7 defect L-1: resolve() restricts an escalation claim's +90d corpus window to the
                   # actors named in the story via c["entities"]. log_claims never wrote the field, so entities was
                   # always empty at resolution and every escalation claim resolved against every conflict,
                   # infrastructure-attack and chokepoint event on earth -- close to always true. Additive: new
                   # rows carry it, rows written before this fix are untouched (append-only).
                   "entities": list(c.get("entities") or []),
                   "event_class": c.get("event_class"), "horizon_days": c.get("horizon_days"),
                   "horizon_unit": c.get("horizon_unit"), "checkable": c.get("checkable"),
                   "verdict": (c.get("verdict") or {}).get("verdict"), "r": (c.get("verdict") or {}).get("r"),
                   "n": (c.get("verdict") or {}).get("n"), "registration": "CLAIM_LEDGER_REGISTRATION.md"}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return ids


def _rows(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def resolve(conn, today=None):
    """Resolve every checkable claim past its horizon, from data. Appends to resolutions.jsonl."""
    today = pd.Timestamp(today or date.today())
    done = {r["claim_id"] for r in _rows(RESOLUTIONS)}
    new = 0
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESOLUTIONS, "a", encoding="utf-8") as f:
        for c in _rows(CLAIMS):
            if not c.get("checkable") or c["claim_id"] in done or c.get("modality") == "hypothetical":
                continue
            k0 = pd.Timestamp(c["knowable"])
            res = None
            if c["kind"] in ("direction", "level", "flow"):
                s = _price(conn, c["series"] or "fred.DCOILBRENTEU")
                pos = s.index.searchsorted(k0)
                if pos + c["horizon_days"] >= len(s):
                    continue                                   # not yet resolvable
                p0 = float(s.iloc[pos]); path = s.iloc[pos:pos + c["horizon_days"] + 1]
                chg = (float(path.iloc[-1]) / p0 - 1) * 100
                if c["kind"] == "direction":
                    claim_true = (chg > 0) if c["direction"] == "up" else (chg < 0)
                elif c["kind"] == "level":
                    claim_true = bool(path.max() >= c["level"]) if c["direction"] == "up" else bool(path.min() <= c["level"])
                else:
                    claim_true = abs(chg) >= 10
                res = {"realized_chg_pct": round(chg, 2), "resolved_on": str(path.index[-1].date())}
            elif c["kind"] == "escalation":
                if today < k0 + timedelta(days=c["horizon_days"]):
                    continue
                ents = tuple(e for e in (c.get("entities") or []) if e.startswith("country."))
                q = ("SELECT COUNT(*) FROM events e JOIN event_entities ee ON ee.event_id=e.event_id "
                     "WHERE e.event_date > ? AND e.event_date <= ? AND e.type IN ('conflict_escalation',"
                     "'infrastructure_attack','chokepoint_disruption')")
                args = [str(k0.date()), str((k0 + timedelta(days=c["horizon_days"])).date())]
                if ents:
                    q += f" AND ee.entity_id IN ({','.join('?' * len(ents))})"; args += list(ents)
                cnt = conn.execute(q, args).fetchone()[0]
                claim_true = cnt > 0
                res = {"subsequent_corpus_events": int(cnt), "resolved_on": str((k0 + timedelta(days=c["horizon_days"])).date()),
                       "basis": "corpus-derived"}
            else:
                continue
            v = c.get("verdict")
            record_call = {"SUPPORTED": True, "UNSUPPORTED": False}.get(v)       # MIXED/THIN = no call
            record_true = None if record_call is None else (record_call == claim_true)
            row = {"claim_id": c["claim_id"], "story_id": c["story_id"], "source": c.get("source"), "kind": c["kind"],
                   "claim_true": bool(claim_true), "record_call": record_call, "record_true": record_true,
                   "resolved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **res}
            f.write(json.dumps(row) + "\n"); new += 1
    return new


def scoreboards(conn=None):
    """The three boards. Young boards say so instead of pretending."""
    claims = _rows(CLAIMS); res = _rows(RESOLUTIONS)
    checkable = [c for c in claims if c.get("checkable")]
    wf = {}
    try:
        wf = json.load(open(DATA / "walk_forward" / "summary.json"))
    except Exception:
        pass
    engine = []
    for w, d in (wf.get("windows") or {}).items():                      # legacy two-window summary (pre-protocol)
        engine.append({"window": w, "test_window": d.get("test_window"), "n": d.get("n_scored"),
                       "G_brier_conditioned": d.get("G_brier_conditioned"), "G_brier_baseline": d.get("G_brier_baseline"),
                       "G_skill": d.get("G_skill"), "P_mae_conditioned": d.get("P_mae_conditioned"),
                       "P_mae_baseline": d.get("P_mae_baseline"), "P_skill": d.get("P_skill")})
    walk = None
    if wf.get("tiers"):                                                  # WALK_FORWARD_PROTOCOL summary (src/walk.py)
        walk = {"run_id": wf.get("run_id"), "generated_at": wf.get("generated_at"), "protocol": wf.get("protocol"),
                "verdict": {k: (wf.get("verdict") or {}).get(k) for k in ("G_conditioning", "P_conditioning", "audit_passed")},
                "tiers": {}}
        for t, d in wf["tiers"].items():
            row = {"n_reads": d.get("n_reads"), "n_scored": d.get("n_scored_burn_in"), "permits_validation": d.get("permits_validation")}
            for task in ("G", "P"):
                ev = (d.get(task) or {}).get("engine_vs") or {}
                row[task] = {ref: {k: v.get(k) for k in ("n", "skill", "ci95", "dm_p")} for ref, v in ev.items() if isinstance(v, dict)}
                row[task]["score"] = (d.get(task) or {}).get("score")
                sp = (d.get(task) or {}).get("spa") or {}
                row[task]["spa_p"] = sp.get("p_spa")
            walk["tiers"][t] = row
        walk["permutation_p"] = (wf.get("permutation") or {}).get("p_value")
        walk["placebo_null_holds"] = (wf.get("placebo") or {}).get("null_holds")
        walk["leakage"] = wf.get("leakage")
        walk["registered"] = {k: (wf.get("registered") or {}).get(k) for k in ("n_boot", "n_perm", "n_spa_boot", "burn_in", "k_max")}
    called = [r for r in res if r.get("record_true") is not None]
    rvn = {"resolved": len(res), "with_record_call": len(called),
           "record_right": sum(1 for r in called if r["record_true"]),
           "narrative_right": sum(1 for r in called if r["claim_true"]),
           "record_only_right": sum(1 for r in called if r["record_true"] and not r["claim_true"]),
           "narrative_only_right": sum(1 for r in called if r["claim_true"] and not r["record_true"]),
           "status": "seeding" if len(called) < MIN_N else "live"}
    by_src = {}
    for r in res:
        key = (r.get("source") or "unknown", r.get("kind"))
        b = by_src.setdefault(key, {"source": key[0], "kind": key[1], "n": 0, "true": 0})
        b["n"] += 1; b["true"] += 1 if r["claim_true"] else 0
    sources = sorted(by_src.values(), key=lambda b: -b["n"])
    for b in sources:
        b["true_rate"] = round(b["true"] / b["n"], 2)
    pending = [c for c in checkable if c["claim_id"] not in {r["claim_id"] for r in res}]
    return {"engine": {"rows": engine, "walk": walk, "verdict": (wf.get("verdict") or {}), "protocol": wf.get("protocol"),
                       "label": ("G target = IES-90 (independent dated codings; OUTCOME_MAPPING.md); 30-event audit pending"
                                 if walk else "outcomes are corpus-derived (situation records observe subsequent corpus events); "
                                              "not yet audited against fresh sources")},
            "record_vs_narrative": rvn,
            "sources": sources,
            "counts": {"claims_logged": len(claims), "checkable": len(checkable), "resolved": len(res), "pending": len(pending)},
            "registration": "CLAIM_LEDGER_REGISTRATION.md",
            "note": "Nothing here is hand-edited. Boards below n=8 are labelled seeding."}


if __name__ == "__main__":
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == "resolve":
        _c = sqlite3.connect(DB); print(f"newly resolved: {resolve(_c)}"); _c.close(); raise SystemExit(0)
    for s in ["Analysts say the strike could send Brent past $110 a barrel within weeks.",
              "Iran will retaliate against Gulf shipping.", "Fertilizer prices will spike.",
              "The regime cannot survive this.", "Tankers stopped transiting the strait."]:
        t = type_claim(s, "infrastructure_attack", ["country.iran"])
        print(t["kind"], t["checkable"], "|", s)
    c = sqlite3.connect(DB)
    print(json.dumps(scoreboards(c)["counts"]))
