"""
corroborate.py -- the corroboration brain (v1): turn a noisy timeline into
confidence-scored events by triangulation.

THE PRINCIPLE: an event is credible when INDEPENDENT sources converge on it; a lone
report is noise. So we (1) cluster a situation's atoms that describe the same event
(collapsing near-duplicate headlines), (2) count how many INDEPENDENT sources back
each cluster -- distinct domains, so twenty reprints of one wire story count once --
and (3) score confidence with weight-of-evidence in decibans (independent evidence
ADDS in log-odds), capped so correlated evidence can never manufacture certainty.

This is deterministic Python -- no LLM in the scoring. The weights are engine-chosen,
tagged as such, and tunable; they will be calibrated later against the reads ledger
(Brier). It reads only situation_log (already sourced/tagged) and writes a report;
it changes no beliefs and touches no gate.

The design is multi-modal ready: a cluster's evidence is a set of (source, modality)
units, so E2 (NASA FIRMS thermal) and prediction markets can add non-news evidence
units later -- cross-modality convergence is the strongest signal of all.

Run:  python3 src/corroborate.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SIT_CONFIG = ROOT / "data" / "situations.yaml"
PORTWATCH = ROOT / "data" / "portwatch.json"
FIRMS = ROOT / "data" / "firms.json"
OUT = ROOT / "data" / "corroboration.json"

# Headline terms -> chokepoint slug, so a physical disruption can corroborate a
# news cluster about that chokepoint (cross-modal convergence, the strongest signal).
CHOKEPOINT_TERMS = {"hormuz": "hormuz", "bab el-mandeb": "bab_el_mandeb",
                    "bab al-mandeb": "bab_el_mandeb", "red sea": "bab_el_mandeb",
                    "suez": "suez"}
# Facility terms -> FIRMS slug (oil infra only; chokepoints stay physical-flow's job,
# so the two modalities never vote on the same location = no double-count).
FACILITY_TERMS = {"abqaiq": "abqaiq", "ras tanura": "ras_tanura",
                  "khurais": "khurais", "kharg": "kharg",
                  "ras laffan": "ras_laffan", "jamnagar": "jamnagar"}

# --- the weight-of-evidence model -----------------------------------------------
# These are the CALIBRATABLE layer. They start as engine-chosen constants and are
# refined by calibrate_corroboration.py against resolved outcomes (the human gate),
# written to data/corroboration_weights.json. Read that file if present so learned
# weights survive across runs; fall back to these defaults otherwise.
WEIGHTS_FILE = ROOT / "data" / "corroboration_weights.json"
DEFAULT_WEIGHTS = {
    "prior_prob": 0.10,          # base rate that a raw alert marks a real event
    "addl_decibans": [6, 5, 4, 3, 2, 1],   # weight of the 1st,2nd,... indep source
    "cap_prob": 0.97,            # never claim certainty (correlated evidence is real)
}
SIM_THRESHOLD = 72         # rapidfuzz token_sort_ratio to call two headlines "same event"
# Back-compat references to the default weights (score() uses the loaded weights).
PRIOR_PROB = DEFAULT_WEIGHTS["prior_prob"]
ADDL_DECIBANS = DEFAULT_WEIGHTS["addl_decibans"]
CAP_PROB = DEFAULT_WEIGHTS["cap_prob"]


def load_weights():
    """The calibratable weights: learned file over defaults."""
    w = dict(DEFAULT_WEIGHTS)
    if WEIGHTS_FILE.exists():
        try:
            w.update({k: v for k, v in json.loads(WEIGHTS_FILE.read_text()).items()
                      if k in DEFAULT_WEIGHTS})
        except (ValueError, OSError):
            pass
    return w


_WEIGHTS = load_weights()


def _domain(url):
    """Registrable-ish domain from a URL (the independence key). '' if unparseable."""
    try:
        net = urlparse(url).netloc.lower()
        return net[4:] if net.startswith("www.") else net
    except (ValueError, AttributeError):
        return ""


def _prob_to_db(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    import math
    return 10.0 * math.log10(p / (1 - p))


def _db_to_prob(db):
    odds = 10.0 ** (db / 10.0)
    return odds / (1.0 + odds)


def cluster_atoms(atoms, threshold=SIM_THRESHOLD):
    """Greedy-cluster atoms whose headlines describe the same event. Atoms are
    dicts with at least 'headline'. Pure function (testable, no I/O)."""
    clusters = []
    for a in atoms:
        h = a.get("headline") or ""
        for c in clusters:
            if fuzz.token_sort_ratio(h, c[0].get("headline") or "") >= threshold:
                c.append(a)
                break
        else:
            clusters.append([a])
    return clusters


def score(n_independent, weights=None):
    """Weight-of-evidence -> (decibans, probability, confidence tag) for a cluster
    backed by n_independent sources. Diminishing returns; capped below certainty.
    Uses the calibratable weights (learned file, or defaults)."""
    w = weights or _WEIGHTS
    addl = w["addl_decibans"]
    db = _prob_to_db(w["prior_prob"])
    for i in range(n_independent):
        db += addl[i] if i < len(addl) else 0
    p = min(_db_to_prob(db), w["cap_prob"])
    tag = ("corroborated" if p >= 0.75 else "likely" if p >= 0.45
           else "possible" if p >= 0.25 else "unverified")
    return round(db, 1), round(p, 3), tag


def disrupted_chokepoints():
    """Chokepoint slugs PortWatch currently flags 'reduced' (physical disruption)."""
    return _flagged(PORTWATCH, "chokepoints", "reduced")


def elevated_facilities():
    """Facility slugs FIRMS currently flags 'elevated' (thermal anomaly / strike)."""
    return _flagged(FIRMS, "facilities", "elevated")


def _physical_hit(cluster, disrupted):
    """Does a physical disruption corroborate this news cluster? Returns the
    chokepoint slug if any headline names a chokepoint that PortWatch flags reduced."""
    text = " ".join((a.get("headline") or "").lower() for a in cluster)
    for term, slug in CHOKEPOINT_TERMS.items():
        if term in text and slug in disrupted:
            return slug
    return None


def _thermal_hit(cluster, elevated):
    """Does a satellite thermal anomaly corroborate this cluster? Returns the
    facility slug if any headline names a facility FIRMS flags elevated (a strike)."""
    text = " ".join((a.get("headline") or "").lower() for a in cluster)
    for term, slug in FACILITY_TERMS.items():
        if term in text and slug in elevated:
            return slug
    return None


def _priced_hit(cluster, moved_markets):
    """Does a PREDICTION MARKET that has repriced corroborate this cluster? A 4th, independent
    modality: if the market is quietly repricing the same subject the news cluster names, that is
    money moving on the story -- far stronger than headlines alone. Returns the market question."""
    text = " ".join((a.get("headline") or "").lower() for a in cluster)
    terms = list(CHOKEPOINT_TERMS) + list(FACILITY_TERMS) + ["iran", "israel", "opec", "oil", "crude"]
    for m in moved_markets or []:
        q = (m.get("market") or m.get("question") or "").lower()
        if not q:
            continue
        if any(t in text and t in q for t in terms):
            return m.get("market") or m.get("question")
    return None


def _flagged(path, key, flag):
    """Slugs in a signal JSON whose 'flag' == flag (portwatch/firms readers)."""
    if not path.exists():
        return set()
    try:
        items = json.loads(path.read_text()).get(key, [])
    except (ValueError, OSError):
        return set()
    return {c["slug"] for c in items if c.get("flag") == flag}


def corroborate_situation(conn, sid, disrupted=None, elevated=None, moved=None):
    """Cluster + score a situation's atoms. Cross-modal votes add independence:
    a physical-flow disruption (PortWatch ships stopped), a satellite thermal anomaly
    (FIRMS fire at a named facility), or a repricing PREDICTION MARKET (money moving)
    that matches a cluster is far stronger than news alone. Sorted most-corroborated first.
    Each event carries `modality_classes` -- the count of distinct evidence TYPES (news /
    physical / thermal / priced) -- the anti-attention-noise metric: confirmation, not headlines."""
    disrupted = disrupted if disrupted is not None else disrupted_chokepoints()
    elevated = elevated if elevated is not None else elevated_facilities()
    moved = moved or []
    rows = conn.execute(
        "SELECT ts, kind, headline, source_url FROM situation_log "
        "WHERE situation_id=? ORDER BY ts DESC, log_id DESC", (sid,)).fetchall()
    atoms = [{"ts": ts, "kind": k, "headline": h, "source_url": u}
             for ts, k, h, u in rows]
    events = []
    for c in cluster_atoms(atoms):
        domains = sorted({_domain(a["source_url"]) for a in c if a["source_url"]})
        modalities = ["news"]
        n_indep = len(domains)
        phys = _physical_hit(c, disrupted)
        if phys:                       # cross-modal physical corroboration
            n_indep += 1
            modalities.append(f"physical:portwatch:{phys}")
        therm = _thermal_hit(c, elevated)
        if therm:                      # cross-modal satellite-thermal corroboration
            n_indep += 1
            modalities.append(f"thermal:firms:{therm}")
        priced = _priced_hit(c, moved)
        if priced:                     # cross-modal prediction-market corroboration (money moving)
            n_indep += 1
            modalities.append(f"priced:market:{priced[:40]}")
        classes = sorted({m.split(":")[0] for m in modalities})
        db, p, tag = score(n_indep)
        rep = max(c, key=lambda a: len(a.get("headline") or ""))  # fullest headline
        events.append({
            "headline": rep["headline"], "kind": rep["kind"],
            "n_atoms": len(c), "n_independent_sources": n_indep,
            "sources": domains[:8], "modalities": modalities,
            "modality_classes": classes, "n_modality_classes": len(classes),
            "multi_modal": len(classes) >= 2,       # confirmed beyond headlines
            "source_urls": sorted({a["source_url"] for a in c if a["source_url"]})[:10],
            "confidence": p, "confidence_db": db, "tag": tag,
            "latest_ts": max(a["ts"] for a in c)[:10]})
    events.sort(key=lambda e: (e["n_modality_classes"], e["confidence"], e["n_atoms"]), reverse=True)
    return events


def convergence_summary(events):
    """Per-situation headline: how many events are MULTI-MODAL (confirmed beyond news), and the
    best modality-class count. The differentiator vs attention-only products in one number."""
    if not events:
        return {"n_events": 0, "n_multi_modal": 0, "max_modality_classes": 0, "top": None}
    top = max(events, key=lambda e: (e["n_modality_classes"], e["confidence"]))
    return {"n_events": len(events),
            "n_multi_modal": sum(1 for e in events if e["multi_modal"]),
            "max_modality_classes": top["n_modality_classes"],
            "top": {"headline": top.get("headline", ""), "tag": top.get("tag", ""),
                    "modality_classes": top["modality_classes"], "confidence": top.get("confidence")}}


def load_situations():
    if not SIT_CONFIG.exists():
        return []
    import yaml
    return (yaml.safe_load(SIT_CONFIG.read_text()) or {}).get("situations", [])


def _moved_markets():
    """Prediction markets that have repriced (the priced modality), via the divergence detector."""
    try:
        import divergence
        conn = sqlite3.connect(DB)
        movers = divergence.market_movers(conn)
        conn.close()
        return movers
    except Exception:
        return []


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    moved = _moved_markets()
    conn = sqlite3.connect(DB)
    report, summary = {}, {}
    for sit in load_situations():
        if sit.get("status") == "closed":
            continue
        evs = corroborate_situation(conn, sit["situation_id"], moved=moved)
        report[sit["situation_id"]] = evs
        summary[sit["situation_id"]] = convergence_summary(evs)
    conn.close()
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now,
         "method": "weight-of-evidence over independent domains + cross-modal votes (news / "
                   "physical PortWatch / thermal FIRMS / priced markets). Correlated reprints "
                   "collapse; certainty capped; multi-modal = confirmed beyond headlines.",
         "situations": report, "convergence": summary}, indent=2))
    total = sum(len(v) for v in report.values())
    print(f"corroborate -- scored {total} event clusters across {len(report)} situation(s).")
    for sid, evs in report.items():
        cs = summary[sid]
        print(f"  {sid}: {len(evs)} events, {cs['n_multi_modal']} multi-modal "
              f"(max {cs['max_modality_classes']} modality classes)")
        for e in [e for e in evs if e["multi_modal"]][:4]:
            print(f"     [{e['tag']:>12} {e['confidence']:.2f}] classes={e['modality_classes']}  "
                  f"{e['headline'][:46]}")


if __name__ == "__main__":
    main()
