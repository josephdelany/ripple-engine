"""
admission_rule.py -- the REGISTERED auto-admit rule for the corpus (VISION_ROADMAP V2.1).

Registered as a codebook amendment (EVENTS_CODEBOOK.md, 2026-08-03) BEFORE any backfill was run.
This module IS that rule, in code -- one deterministic gate, no LLM in the decision. A candidate is
AUTO-ADMITTED into the causal corpus iff ALL of:

  G1  two-plus independent sources -- >= 2 source URLs from DIFFERENT publishers (registrable domains).
  G2  date precision == 'day'      -- exact date only (no week/month) so point-in-time is unambiguous.
  G3  clean entity match           -- >= 1 well-formed entity (entity_id:role) whose id is in-vocab.
  G4  passes the no-fabrication cage -- in-vocab event type, real http(s) sources, not future-dated.
  G5  not a cluster-duplicate      -- not within CLUSTER_DAYS of an existing SAME-TYPE corpus event.

Anything failing one or more gates is NOT admitted -- it goes to the BORDERLINE QUEUE for Joe, tagged
with which gates it failed. Auto-admit only under this rule; the cage never weakens. GDELT single-
source items fail G1 by construction -- they belong to the reference tier, never the corpus.

This module only DECIDES; it never writes canon. Canon is still written through the sanctioned
apply_review.py + load_events.py path (the codebook gate is re-applied there).
"""

from datetime import datetime

from load_events import VALID_TYPES
from two_source_backfill import registrable_domain

CLUSTER_DAYS = 35          # matches robustness.CLUSTER_DAYS -- same-window same-type = duplicate
KNOWN_ENTITY_PREFIXES = ("country.", "commodity.", "chokepoint.", "institution.", "macro.",
                         "location.", "company.", "supplychain.")


def _sources(candidate):
    """The candidate's source URLs, from an explicit list or a delimited source_url field."""
    if candidate.get("sources"):
        urls = candidate["sources"]
    else:
        raw = candidate.get("source_url") or ""
        urls = [u for u in raw.replace(";", "|").replace(" ", "|").split("|") if u.strip()]
    return [u.strip() for u in urls if u.strip()]


def _independent(urls):
    """Distinct registrable domains among well-formed http(s) URLs (independence = different publisher)."""
    doms = set()
    for u in urls:
        if u.startswith("http://") or u.startswith("https://"):
            d = registrable_domain(u)
            if d:
                doms.add(d)
    return doms


def _entities_ok(candidate):
    """G3: at least one well-formed 'entity_id:role' whose id has a known vocab prefix."""
    raw = (candidate.get("entities") or "").strip()
    if not raw:
        return False
    for part in raw.split(";"):
        part = part.strip()
        if ":" not in part:
            continue
        eid = part.split(":", 1)[0].strip()
        if any(eid.startswith(p) for p in KNOWN_ENTITY_PREFIXES):
            return True
    return False


def _cage_ok(candidate, today):
    """G4: no-fabrication cage -- in-vocab type, real http(s) sources, a parseable non-future date."""
    if candidate.get("type") not in VALID_TYPES:
        return False, "type not in codebook vocab"
    urls = _sources(candidate)
    if not urls or not all(u.startswith("http://") or u.startswith("https://") for u in urls):
        return False, "a source is missing or not a real http(s) URL"
    d = (candidate.get("event_date") or "")[:10]
    try:
        ed = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return False, "event_date unparseable"
    if ed > today:
        return False, "event_date is in the future (lookahead)"
    return True, ""


def _cluster_dup(candidate, existing):
    """G5: within CLUSTER_DAYS of an existing SAME-TYPE corpus event -> duplicate."""
    d = (candidate.get("event_date") or "")[:10]
    try:
        ed = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return True                                   # unparseable -> treat as dup-fail (fail-closed)
    for xdate, xtype in existing:
        if xtype != candidate.get("type"):
            continue
        try:
            xd = datetime.strptime((xdate or "")[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        if abs((ed - xd).days) <= CLUSTER_DAYS:
            return True
    return False


def evaluate(candidate, existing, today):
    """Return {verdict: 'AUTO_ADMIT'|'BORDERLINE', gates: {...bool}, reasons: [...]}.
    `existing` is [(event_date, type)] of the current corpus (for G5). `today` is a date."""
    urls = _sources(candidate)
    doms = _independent(urls)
    cage_ok, cage_reason = _cage_ok(candidate, today)
    gates = {
        "G1_two_independent_sources": len(doms) >= 2,
        "G2_date_precision_day": (candidate.get("date_precision") or "").strip() == "day",
        "G3_clean_entity_match": _entities_ok(candidate),
        "G4_passes_cage": cage_ok,
        "G5_not_cluster_duplicate": not _cluster_dup(candidate, existing),
    }
    reasons = []
    if not gates["G1_two_independent_sources"]:
        reasons.append(f"G1: only {len(doms)} independent source(s) (need >= 2)")
    if not gates["G2_date_precision_day"]:
        reasons.append(f"G2: date_precision '{candidate.get('date_precision')}' != day")
    if not gates["G3_clean_entity_match"]:
        reasons.append("G3: no well-formed in-vocab entity")
    if not gates["G4_passes_cage"]:
        reasons.append(f"G4: {cage_reason}")
    if not gates["G5_not_cluster_duplicate"]:
        reasons.append(f"G5: cluster-duplicate of an existing same-type event (<= {CLUSTER_DAYS}d)")
    verdict = "AUTO_ADMIT" if all(gates.values()) else "BORDERLINE"
    return {"verdict": verdict, "gates": gates, "reasons": reasons}
