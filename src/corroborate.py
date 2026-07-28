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

# --- the weight-of-evidence model (engine-chosen constants, tunable, to calibrate) ---
PRIOR_PROB = 0.10            # base rate that a raw alert marks a real, significant event
# Decibans added by the 1st, 2nd, ... INDEPENDENT source (diminishing returns).
ADDL_DECIBANS = [6, 5, 4, 3, 2, 1]
CAP_PROB = 0.97             # never claim certainty -- correlated evidence is real
SIM_THRESHOLD = 72         # rapidfuzz token_sort_ratio to call two headlines "same event"


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


def score(n_independent):
    """Weight-of-evidence -> (decibans, probability, confidence tag) for a cluster
    backed by n_independent sources. Diminishing returns; capped below certainty."""
    db = _prob_to_db(PRIOR_PROB)
    for i in range(n_independent):
        db += ADDL_DECIBANS[i] if i < len(ADDL_DECIBANS) else 0
    p = min(_db_to_prob(db), CAP_PROB)
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


def _flagged(path, key, flag):
    """Slugs in a signal JSON whose 'flag' == flag (portwatch/firms readers)."""
    if not path.exists():
        return set()
    try:
        items = json.loads(path.read_text()).get(key, [])
    except (ValueError, OSError):
        return set()
    return {c["slug"] for c in items if c.get("flag") == flag}


def corroborate_situation(conn, sid, disrupted=None, elevated=None):
    """Cluster + score a situation's atoms. Cross-modal votes add independence:
    a physical-flow disruption (PortWatch ships stopped) or a satellite thermal
    anomaly (FIRMS fire at a named facility) that matches a cluster is far stronger
    than news alone. Sorted most-corroborated first."""
    disrupted = disrupted if disrupted is not None else disrupted_chokepoints()
    elevated = elevated if elevated is not None else elevated_facilities()
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
        db, p, tag = score(n_indep)
        rep = max(c, key=lambda a: len(a.get("headline") or ""))  # fullest headline
        events.append({
            "headline": rep["headline"], "kind": rep["kind"],
            "n_atoms": len(c), "n_independent_sources": n_indep,
            "sources": domains[:8], "modalities": modalities,
            "confidence": p, "confidence_db": db, "tag": tag,
            "latest_ts": max(a["ts"] for a in c)[:10]})
    events.sort(key=lambda e: (e["confidence"], e["n_atoms"]), reverse=True)
    return events


def load_situations():
    if not SIT_CONFIG.exists():
        return []
    import yaml
    return (yaml.safe_load(SIT_CONFIG.read_text()) or {}).get("situations", [])


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    report = {}
    for sit in load_situations():
        if sit.get("status") == "closed":
            continue
        report[sit["situation_id"]] = corroborate_situation(conn, sit["situation_id"])
    conn.close()
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now,
         "method": "weight-of-evidence over independent domains (v1, heuristic; "
                   "to be calibrated). Correlated reprints collapse; certainty capped.",
         "situations": report}, indent=2))
    total = sum(len(v) for v in report.values())
    print(f"corroborate -- scored {total} event clusters across "
          f"{len(report)} situation(s).")
    for sid, evs in report.items():
        conf = [e for e in evs if e["tag"] in ("corroborated", "likely")]
        print(f"  {sid}: {len(evs)} events, {len(conf)} likely+ corroborated")
        for e in conf[:4]:
            print(f"     [{e['tag']:>12} {e['confidence']:.2f}] "
                  f"{e['n_independent_sources']}src  {e['headline'][:50]}")


if __name__ == "__main__":
    main()
