"""challenge.py -- the CHALLENGE loop on the Story page (CLAIM_LEDGER_REGISTRATION.md, Amendment 4).

The analyst conditions the situation record -- actor, target, conflict_scope, tempo, alliance,
diplomatic, target_capacity -- from the coded vocabulary, and the engine re-reads Layer G
(escalation.read) with those fields overridden. Same engine, same thresholds. Returns:
  * the conditioned subset: n, branch counts, the analog list (every member at/above COND_SIM);
  * the price side for exactly that subset: Brent +20 trading days via ledger.class_outcomes,
    filtered to the subset's event ids, point-in-time for corpus events;
  * a comparison row against the unconditioned read;
  * per-field coverage (how many corpus records carry a coded value), so a condition on an
    uncoded field is shown to be inert rather than pretending to bite.
States: CONDITIONED (n >= 8) · THIN (n < 8; counts shown, not a call) · NO PRECEDENT (no analog at
or above RETRIEVE_MIN) · REFUSED (a value outside the vocabulary; nothing runs).
Every challenge, refused ones included, is appended verbatim to data/ledger/challenges.jsonl.

Run:  python3 src/challenge.py abqaiq_attack_2019 actor=country.usa
"""
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
LEDGER_DIR = DATA / "ledger"
CHALLENGES = LEDGER_DIR / "challenges.jsonl"
STORIES = DATA / "reader" / "stories"            # live-story context persisted by story_read
sys.path.insert(0, str(Path(__file__).resolve().parent))
import escalation as ES                          # noqa: E402
import ledger as L                               # noqa: E402

REGISTRATION = "CLAIM_LEDGER_REGISTRATION.md Amendment 4"
FIELDS = ("actor", "target", "conflict_scope", "tempo", "alliance", "diplomatic", "target_capacity")
COL = {f: f"sr_{f}" for f in FIELDS}
# SITUATION_CODEBOOK_V2.md enums; actor/target take any id coded in the corpus (see vocab())
CODEBOOK = {
    "conflict_scope": ["isolated", "campaign", "war"],
    "tempo": ["first", "nth"],
    "alliance": ["none", "diplomatic", "material", "military"],
    "diplomatic": ["talks", "sanctions", "ceasefire", "none"],
    "target_capacity": ["none", "limited", "significant"],
}
MAX_NOTE = 2000


# ----------------------------------------------------------------------------- vocabulary + coverage

def vocab(conn):
    """Per field: the allowed values (codebook enum + values actually coded) and coverage k/N over
    the geopolitical corpus. Deterministic; read from the DB, never invented."""
    geo = ",".join("?" * len(ES.GEO_TYPES))
    N = conn.execute(f"SELECT count(*) FROM events WHERE type IN ({geo})", ES.GEO_TYPES).fetchone()[0]
    out = {"n_records": N, "fields": {}}
    for f in FIELDS:
        col = COL[f]
        rows = conn.execute(f"SELECT {col}, count(*) FROM events WHERE type IN ({geo}) AND {col} IS NOT NULL "
                            f"AND {col} != 'unknown' GROUP BY {col} ORDER BY count(*) DESC", ES.GEO_TYPES).fetchall()
        coded = {v: k for v, k in rows}
        allowed = list(CODEBOOK.get(f, [])) + [v for v in coded if v not in CODEBOOK.get(f, [])]
        out["fields"][f] = {"allowed": allowed, "coded": coded, "coverage": int(sum(coded.values())), "of": N}
    return out


def validate(conditions, voc):
    """(clean, errors). A condition outside the coded fields/vocabulary is an error; nothing is repaired."""
    clean, errors = {}, []
    for f, v in (conditions or {}).items():
        if f not in FIELDS:
            errors.append(f"'{f}' is not a conditionable field (allowed: {', '.join(FIELDS)})"); continue
        allowed = voc["fields"][f]["allowed"]
        if v not in allowed:
            errors.append(f"'{v}' is not in the coded vocabulary for {f} (allowed: {', '.join(allowed) or 'none coded yet'})"); continue
        clean[f] = v
    if not clean and not errors:
        errors.append("no conditions given")
    return clean, errors


# ----------------------------------------------------------------------------- the target

def target_for(conn, story_id):
    """The situation record the story page read from. 'event:<id>' -> the coded corpus record
    (point-in-time as_of its date); 'live:<cid>' -> the context story_read persisted."""
    if story_id.startswith("event:"):
        eid = story_id.split(":", 1)[1]
        cols = [c[1] for c in conn.execute("PRAGMA table_info(events)")]
        row = conn.execute("SELECT * FROM events WHERE event_id=?", (eid,)).fetchone()
        if not row:
            return None, None, f"unknown event {eid}"
        t = ES._rec(row, cols)
        return t, t["date"], None
    p = STORIES / f"{story_id.replace(':', '_')}.json"
    if not p.exists():
        return None, None, f"no persisted context for {story_id}; read the story first"
    ctx = json.loads(p.read_text())
    etype = ctx.get("event_class")
    t = {"event_id": None, "type": etype, "actor": "unknown", "target": "unknown", "conflict_scope": "unknown",
         "tempo": "unknown", "diplomatic": "unknown", "alliance": "unknown", "target_capacity": "unknown",
         "prior_dyad": "unknown", "propensity": None, "title": ctx.get("title")}
    for e in ctx.get("entities") or []:                     # same rule as story_read.branches
        if e.startswith("country.") and t["target"] == "unknown":
            t["target"] = e
    return t, None, None


# ----------------------------------------------------------------------------- price side

def outcomes_for_ids(conn, ids, types, as_of=None):
    """Brent +20 trading-day outcomes for exactly these event ids (ledger.class_outcomes per class,
    filtered). Returns the distribution with n, median, IQR, share up, dated tails."""
    want = set(ids)
    rows = []
    for t in sorted(set(types)):
        rows += [o for o in L.class_outcomes(conn, t, as_of=as_of) if o["event_id"] in want]
    if not rows:
        return {"n": 0, "note": "no price history for this subset"}
    a = np.array([o["chg_pct"] for o in rows])
    rows.sort(key=lambda o: o["chg_pct"])
    return {"n": len(rows), "median_pct": round(float(np.median(a)), 2),
            "p25_pct": round(float(np.percentile(a, 25)), 2), "p75_pct": round(float(np.percentile(a, 75)), 2),
            "share_up": round(float((a > 0).mean()), 3), "share_ge10": round(float((np.abs(a) >= 10).mean()), 3),
            "tails": {"low": {k: rows[0][k] for k in ("event_id", "date", "title", "chg_pct")},
                      "high": {k: rows[-1][k] for k in ("event_id", "date", "title", "chg_pct")}},
            "series": "fred.DCOILBRENTEU", "horizon_td": L.PRICE_HORIZON_TD, "bar": L._bar_price(rows)}


def _esc_rate(counts):
    n = sum(counts.values())
    return round((counts.get("LIMITED_RETALIATION", 0) + counts.get("WIDENING", 0)) / n, 3) if n else None


def _side(read, price):
    """One comparison-row side: subset n, branch counts, escalation share, price distribution."""
    sc = (read.get("subset_counts") or {}) if not read.get("no_adequate_precedent") else {}
    counts = sc.get("counts") or {}
    return {"n": sc.get("n", 0), "counts": counts, "escalated_share": _esc_rate(counts),
            "basis": (read.get("branch_rates") or {}).get("basis"),
            "price_n": price.get("n", 0), "price_median_pct": price.get("median_pct"), "price_share_up": price.get("share_up")}


# ----------------------------------------------------------------------------- the challenge

def _cid(story_id, conditions, note, at):
    return hashlib.sha1(f"{story_id}|{json.dumps(conditions, sort_keys=True)}|{note}|{at}".encode()).hexdigest()[:12]


def _append(row):
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    with open(CHALLENGES, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(conn, story_id, conditions, note="", log=True):
    """Run one challenge. Always logs (refusals included). Returns the result dict."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    note = (note or "")[:MAX_NOTE]
    voc = vocab(conn)
    clean, errors = validate(conditions, voc)
    target, as_of, terr = target_for(conn, story_id)
    if terr:
        errors.append(terr)
    row = {"challenge_id": _cid(story_id, conditions or {}, note, now), "story_id": story_id, "logged_at": now,
           "knowable": as_of, "conditions": conditions or {}, "note": note, "registration": REGISTRATION}
    if errors:
        res = {**row, "status": "REFUSED", "errors": errors, "vocab": voc}
        if log:
            _append({**row, "status": "REFUSED", "errors": errors})
        return res
    if target.get("type") not in ES.GEO_TYPES:
        res = {**row, "status": "REFUSED", "errors": [f"'{target.get('type')}' is not a geopolitical class; escalation branches do not apply"]}
        if log:
            _append(res)
        return res

    base = ES.read(conn, target, as_of=as_of)
    cond_target = {**target, **clean}
    cond = ES.read(conn, cond_target, as_of=as_of)

    coverage = {f: {"coverage": voc["fields"][f]["coverage"], "of": voc["fields"][f]["of"]} for f in clean}
    flags = [f"field_uncoded:{f}" for f, c in coverage.items() if c["coverage"] == 0]

    if cond.get("no_adequate_precedent"):
        status = "NO PRECEDENT"
    elif cond["conditioned_n"] < ES.COND_MIN_N:
        status = "THIN"
    else:
        status = "CONDITIONED"

    subset = cond.get("subset") or []
    base_subset = base.get("subset") or []
    price_c = outcomes_for_ids(conn, [s["event_id"] for s in subset], [s["type"] for s in subset], as_of=as_of) if subset else {"n": 0}
    price_b = outcomes_for_ids(conn, [s["event_id"] for s in base_subset], [s["type"] for s in base_subset], as_of=as_of) if base_subset else {"n": 0}

    comparison = {"unconditioned": _side(base, price_b), "conditioned": _side(cond, price_c)}
    u, c = comparison["unconditioned"], comparison["conditioned"]
    comparison["delta"] = {"n": c["n"] - u["n"],
                           "escalated_share": (round(c["escalated_share"] - u["escalated_share"], 3)
                                               if c["escalated_share"] is not None and u["escalated_share"] is not None else None),
                           "price_median_pct": (round(c["price_median_pct"] - u["price_median_pct"], 2)
                                                if c["price_median_pct"] is not None and u["price_median_pct"] is not None else None)}
    res = {**row, "status": status, "flags": flags, "field_coverage": coverage, "conditions_applied": clean,
           "target": {k: target.get(k) for k in ("event_id", "type", *FIELDS)},
           "conditioned_target": {k: cond_target.get(k) for k in ("type", *FIELDS)},
           "subset": {"n": len(subset), "counts": (cond.get("subset_counts") or {}).get("counts", {}),
                      "analogs": subset, "max_similarity": cond.get("max_similarity"), "threshold": ES.RETRIEVE_MIN},
           "branch_rates": cond.get("branch_rates"), "price": price_c, "comparison": comparison,
           "outcome_label": "outcomes at +90d are corpus-derived (subsequent corpus events), not source-audited",
           "thresholds": {"RETRIEVE_MIN": ES.RETRIEVE_MIN, "COND_SIM": ES.COND_SIM, "COND_MIN_N": ES.COND_MIN_N}}
    if log:
        _append({**row, "status": status, "flags": flags, "conditions_applied": clean, "n": len(subset),
                 "counts": res["subset"]["counts"], "price_n": price_c.get("n", 0), "price_median_pct": price_c.get("median_pct"),
                 "unconditioned_n": u["n"], "unconditioned_price_median_pct": u["price_median_pct"]})
    return res


def rows():
    try:
        return [json.loads(l) for l in open(CHALLENGES, encoding="utf-8") if l.strip()]
    except OSError:
        return []


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(0)
    sid = sys.argv[1] if ":" in sys.argv[1] else f"event:{sys.argv[1]}"
    conds = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    conn = sqlite3.connect(DB)
    try:
        r = run(conn, sid, conds, log=False)
    finally:
        conn.close()
    print(json.dumps({k: r[k] for k in r if k not in ("vocab",)}, indent=1, default=str)[:4000])
