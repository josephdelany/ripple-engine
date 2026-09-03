"""situation_vintage.py -- G-3: derive `knowable_at` for the five source-coded situation
fields from the DATED primary documents the dossiers cite.

Registered first, in docs/g/G3_REGISTRATION.md (2026-09-03). Read that file before this one:
every rule below is clause (e.N) of section 3 or 4 there, and the clause id is named in the
code at the point it is applied.

The problem. WORLD_STATE_FRAMEWORK.md Amendment A gives every situation field a knowable_at
by four rules; rule (c) dates a corpus-derived field or an undated URL to the CODING RUN
(2026-09-02), which is after every event in the corpus, so the field vanishes at t. The
published starting position is data/state/situation_knowable.json: 786 situation values,
60 kept, 726 dropped. WALK_FORWARD_PROTOCOL.md Amendment H binds the engine to those dates
for five fields (read.py:109) -- actor, target, conflict_scope, tempo, asset_role.

The remedy Amendment A rule 3 names is "a per-field contemporaneous source with its own
date". Sessions E and G have written 41 dossiers to the SPINE_REGISTRATION standard, each
carrying a Sources table with a transcribed document date and an Entities section naming
each entity, its role, and which source names it. This script turns those into knowable_at
dates, and publishes every decision -- including every refusal -- so a reader who cannot
read code can check any row against the dossier it came from.

WHAT THIS DOES NOT DO. It opens oil.db READ-ONLY and writes no table (SPINE_REGISTRATION
section 5: never write to events, data/events.csv or situation_state). Rule (e) is PROPOSED
to session A, whose document WORLD_STATE_FRAMEWORK.md is. Until A adopts it, situation_state
is unchanged and this is a computed proposal plus a handoff.

Run:  python3 src/situation_vintage.py
Out:  docs/g/SITUATION_VINTAGE.json, docs/g/SITUATION_VINTAGE.md
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
DOSSIERS = ROOT / "data" / "dossiers"
OUT_JSON = ROOT / "docs" / "g" / "SITUATION_VINTAGE.json"
OUT_MD = ROOT / "docs" / "g" / "SITUATION_VINTAGE.md"
BASELINE = ROOT / "data" / "state" / "situation_knowable.json"

# the five fields WALK_FORWARD_PROTOCOL Amendment H binds the engine to (read.py:109)
FIELDS = ("actor", "target", "conflict_scope", "tempo", "asset_role")
# situation_record.py:_conflict_scope -- abs(days) <= 120, symmetric, so half the input postdates t
CONFLICT_SCOPE_WINDOW_DAYS = 120
# situation_record.py:GEO_TYPES -- the classes _parties/_conflict_scope/_observe_outcome apply to
GEO_TYPES = {"conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions"}

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
_M = "|".join(MONTHS)

# (e.1) exactly four recognised forms, tried in this order; nothing else is a date
_FORM_1 = re.compile(rf"\b({_M})\s+(\d{{1,2}}),\s*((?:1[89]|20)\d{{2}})\b", re.I)   # October 7, 1973
_FORM_2 = re.compile(rf"\b(\d{{1,2}})\s+({_M})\s+((?:1[89]|20)\d{{2}})\b", re.I)    # 4 December 1997
_FORM_3 = re.compile(rf"\b({_M})\s+((?:1[89]|20)\d{{2}})\b", re.I)                  # February 2011
_FORM_4 = re.compile(r"\b((?:1[89]|20)\d{2})\b")                                    # 1998
# (e.1) a cell holding any of these is not parsed at all, even where it also holds a year
UNPARSEABLE_TOKENS = ("n/a", "undated", "archival description", "case study text")
# (A1.1) "c." as a bare substring also matches "U.S." and "D.C."; the clause meant circa, so it is
# a `c.` immediately followed by a year and nothing else
_CIRCA = re.compile(r"\bc\.\s*(?:1[89]|20)\d{2}\b", re.I)
# (e.5) the closed negation list; runs only in the direction of exclusion
NEGATIONS = (
    "not confirmed", "no source retrieved", "not independently confirmed", "does not propose",
    "not proposing", "proposed addition", "proposes reclassifying", "missing, not invented",
    "gap", "not named", "no source", "cannot be confirmed", "not usable", "never opened",
    "not asserted", "flags the role", "not confirmed by any source",
)
_MARKER = re.compile(r"\[?\bS(\d+[a-z]?)\b\]?")
_LEAD_ENTITY = re.compile(r"^\s*[-*]\s*\*{0,2}`([^`]+)`")


def _eom(year, month):
    return (dt.date(year + (month == 12), (month % 12) + 1, 1) - dt.timedelta(days=1))


def parse_doc_date(cell):
    """(e.1) The LATEST parseable date in one `Doc. date` cell, or None.

    A cell that names only a month or only a year resolves to that period's LAST day: it
    establishes nothing earlier. The latest date in the cell is taken because a cell reading
    "Signed May 6, 1995; published May 9, 1995" is established as a whole only on 9 May."""
    if cell is None:
        return None, "empty"
    s = str(cell).strip()
    if not s:
        return None, "empty"
    low = s.lower()
    for tok in UNPARSEABLE_TOKENS:
        if tok in low:
            return None, f"unparseable token '{tok}'"
    if _CIRCA.search(s):                                   # (A1.1) circa, e.g. "c. 2022"
        return None, "unparseable token 'c. <year>' (circa)"
    cands = []
    for m in _FORM_1.finditer(s):
        try:
            cands.append((dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))), "form1"))
        except ValueError:
            pass
    for m in _FORM_2.finditer(s):
        try:
            cands.append((dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))), "form2"))
        except ValueError:
            pass
    if not cands:                                     # forms 3 and 4 only when no full date is present
        for m in _FORM_3.finditer(s):
            cands.append((_eom(int(m.group(2)), MONTHS[m.group(1).lower()]), "form3 (end of month)"))
    if not cands:
        for m in _FORM_4.finditer(s):
            cands.append((dt.date(int(m.group(1)), 12, 31), "form4 (end of year)"))
    if not cands:
        return None, "no recognised form"
    d, form = max(cands, key=lambda c: c[0])          # latest within the cell
    return d.isoformat(), form


# ------------------------------------------------------------------ reading a dossier

def read_dossier(path):
    """{'sources': {marker: {...}}, 'entities': [ {entity_id, text, markers} ], 'declared_knowable_at': str|None}"""
    txt = path.read_text()
    sources, entities = {}, []
    for line in txt.split("\n"):
        if line.startswith("| S"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 6:
                mk = c[0].lstrip("S").strip()
                iso, form = parse_doc_date(c[4])
                sources[mk] = {"marker": c[0], "role": c[1], "publisher": c[2][:120],
                               "doc_date_cell": c[4], "doc_date": iso, "parse": form, "url": c[5]}
    m = re.search(r"\n##\s*Entities\s*\n(.*?)(?:\n##\s|\Z)", txt, re.S)
    if m:
        cur = None
        for line in m.group(1).split("\n"):
            lead = _LEAD_ENTITY.match(line)
            if lead:
                cur = {"entity_id": lead.group(1).strip(), "text": line.strip()}
                entities.append(cur)
            elif cur is not None and line.strip() and not line.startswith(("-", "*")):
                cur["text"] += " " + line.strip()     # a bullet wrapped onto the next line
            elif line.strip().startswith(("-", "*")):
                cur = None                            # a bullet with no backticked entity (a Gap note)
    for e in entities:
        e["markers"] = sorted({mm.group(1) for mm in _MARKER.finditer(e["text"])})
    k = re.search(r"\n##\s*Knowable at\s*\n(.*?)(?:\n##\s|\Z)", txt, re.S)
    declared = None
    if k:
        kd = re.search(r"\b((?:1[89]|20)\d{2}-\d{2}-\d{2})\b", k.group(1))
        declared = kd.group(1) if kd else None
    return {"sources": sources, "entities": entities, "declared_knowable_at": declared}


def bullets_for(doss, entity_id):
    """(A1.2) Every bullet whose leading backticked token is this entity_id. Four dossiers give an
    entity two bullets, one per role, because they flag a role duplication in the record."""
    return [e for e in doss["entities"] if e["entity_id"] == entity_id]


def bullet_for(doss, entity_id, role_words=None):
    """(A1.2) With a role required, the bullet carrying that role word in its first 160 characters;
    if none does, the first bullet, so the rejection is reported against something real."""
    bs = bullets_for(doss, entity_id)
    if not bs:
        return None
    if role_words:
        for b in bs:
            head = b["text"][:160].lower()
            if any(w in head for w in role_words):
                return b
    return bs[0]


def negated(text):
    """(e.5) the first negation phrase present, or None."""
    low = text.lower()
    for n in NEGATIONS:
        if n in low:
            return n
    return None


def receipt(doss, entity_id, event_date, role_words=None, require_role=True):
    """(e.2) Build a receipt for one coded entity. Returns (knowable_at|None, detail dict)."""
    b = bullet_for(doss, entity_id, role_words if require_role else None)
    d = {"entity_id": entity_id, "bullet": None, "markers": [], "dates": {},
         "n_bullets": len(bullets_for(doss, entity_id))}
    if b is None:
        d["reject"] = "(e.2 i) no bullet in the dossier names this entity_id"
        return None, d
    d["bullet"] = b["text"][:300]
    if require_role and role_words:
        head = b["text"][:160].lower()
        if not any(w in head for w in role_words):
            d["reject"] = f"(e.2 ii) no role word {role_words} in the bullet's first 160 characters"
            return None, d
    neg = negated(b["text"])
    if neg:
        d["reject"] = f"(e.2 iv) negation phrase present: '{neg}'"
        return None, d
    if not b["markers"]:
        d["reject"] = "(e.2 iii) the bullet cites no source marker"
        return None, d
    d["markers"] = b["markers"]
    dated = {}
    for mk in b["markers"]:
        s = doss["sources"].get(mk)
        if s is None:
            d["dates"][mk] = {"doc_date": None, "cell": None, "parse": "marker not in the source table"}
            continue
        d["dates"][mk] = {"doc_date": s["doc_date"], "cell": s["doc_date_cell"], "parse": s["parse"], "role": s["role"][:40]}
        if s["doc_date"]:
            dated[mk] = s["doc_date"]
    if not dated:
        d["reject"] = "(e.2) no cited source has a parseable Doc. date"
        return None, d
    earliest = min(dated.values())
    if not require_role:
        # (A1.2) no role word to disambiguate: EVERY bullet for this entity must pass (e.2 iii)/(e.2 iv),
        # and the entity's date is the LATEST of the per-bullet earliest dates -- the non-cherry-picking
        # direction, since a second bullet can only make the field later or reject it, never earlier.
        for other in bullets_for(doss, entity_id):
            if other is b:
                continue
            neg2 = negated(other["text"])
            if neg2:
                d["reject"] = (f"(A1.2) a second bullet for this entity carries a negation phrase: "
                               f"'{neg2}' -- {other['text'][:160]}")
                return None, d
            if not other["markers"]:
                d["reject"] = ("(A1.2) a second bullet for this entity cites no source marker -- "
                               + other["text"][:160])
                return None, d
            od = [doss["sources"][m]["doc_date"] for m in other["markers"]
                  if m in doss["sources"] and doss["sources"][m]["doc_date"]]
            if not od:
                d["reject"] = ("(A1.2) a second bullet for this entity cites no source with a parseable "
                               "Doc. date -- " + other["text"][:160])
                return None, d
            earliest = max(earliest, min(od))
    d["earliest_doc_date"] = earliest
    d["clamped"] = earliest < event_date                                   # (e.6)
    return max(earliest, event_date), d


# ------------------------------------------------------------------ the corpus side

def load_corpus(conn):
    cols = {r[1] for r in conn.execute("PRAGMA table_info(events)")}
    need = {"sr_actor", "sr_target", "sr_conflict_scope", "sr_tempo", "sr_asset_role", "sr_json", "added_at"}
    if not need <= cols:
        sys.exit(f"events is missing {sorted(need - cols)} -- run src/situation_record.py first")
    ev = {}
    for r in conn.execute("SELECT event_id, event_date, type, added_at, sr_actor, sr_target, "
                          "sr_conflict_scope, sr_tempo, sr_asset_role, sr_json FROM events"):
        ev[r[0]] = {"event_id": r[0], "event_date": r[1][:10], "type": r[2], "added_at": (r[3] or "")[:10],
                    "actor": r[4], "target": r[5], "conflict_scope": r[6], "tempo": r[7],
                    "asset_role": r[8], "sr_json": r[9]}
    roles = defaultdict(lambda: defaultdict(set))
    for eid, en, role in conn.execute("SELECT event_id, entity_id, role FROM event_entities"):
        roles[eid][role or "mention"].add(en)
    return ev, roles


def is_unknown(v):
    return v in (None, "", "unknown")


# --- Amendment A, re-implemented here so the BEFORE column is computed and not copied ------
_URL_DATE = re.compile(r"/((?:19|20)\d{2})/(\d{2})/(\d{2})/|((?:19|20)\d{2})-(\d{2})-(\d{2})")


def amendment_a(source, event_date, added_at):
    """src/state/situation_state.py:knowable_at -- session A's rules (a)-(d), reproduced verbatim in
    behaviour so this script's BEFORE column can be checked against data/state/situation_knowable.json
    rather than taken on trust."""
    if source in (None, "", "null"):
        return "unknown", "d:null"
    s = str(source)
    if s.startswith("http"):
        m = _URL_DATE.search(s)
        if m:
            y, mo, d = (m.group(1), m.group(2), m.group(3)) if m.group(1) else (m.group(4), m.group(5), m.group(6))
            try:
                return dt.date(int(y), int(mo), int(d)).isoformat(), "a:url_date"
            except ValueError:
                pass
        return (added_at or "") or "unknown", "c:coding_date(undated url)"
    if s.startswith("corpus:observed"):
        return (dt.date.fromisoformat(event_date) + dt.timedelta(days=90)).isoformat(), "b:window_close"
    if s.startswith("corpus:"):
        return (added_at or "") or "unknown", "c:coding_date(corpus-derived)"
    return (added_at or "") or "unknown", "c:coding_date(other)"


# ------------------------------------------------------------------ the derivation

def derive(conn):
    ev, roles = load_corpus(conn)
    doss_files = {p.stem: p for p in sorted(DOSSIERS.glob("*.md"))}
    dossiers = {k: read_dossier(p) for k, p in doss_files.items()}
    rows, audit = [], []

    for eid, e in sorted(ev.items(), key=lambda kv: kv[1]["event_date"]):
        edate = e["event_date"]
        srcs = {}
        if e["sr_json"]:
            try:
                srcs = json.loads(e["sr_json"]).get("sources") or {}
            except ValueError:
                srcs = {}
        doss = dossiers.get(eid)
        # _parties(): targets fall back to `location` when there is no `target` row
        A = {x for x in roles[eid].get("actor", set())}
        T = {x for x in roles[eid].get("target", set())} or {x for x in roles[eid].get("location", set())}
        used_location = not roles[eid].get("target") and bool(roles[eid].get("location"))
        dyad = A | T

        for f in FIELDS:
            val = e[f]
            if is_unknown(val):
                continue                                   # not a situation value; not in the 786
            before, before_rule = amendment_a(srcs.get(f), edate, e["added_at"])
            row = {"event_id": eid, "event_date": edate, "type": e["type"], "field": f, "value": val,
                   "before": before, "before_rule": before_rule, "has_dossier": doss is not None,
                   "after": before, "after_rule": before_rule, "detail": None}

            if f == "conflict_scope":                      # (e.8) -- corpus-wide, dossier or not
                row["after"] = (dt.date.fromisoformat(edate)
                                + dt.timedelta(days=CONFLICT_SCOPE_WINDOW_DAYS)).isoformat()
                row["after_rule"] = "e.8:forward_window(+120d)"
                row["detail"] = {"reason": "situation_record._conflict_scope counts same-dyad events at "
                                           "abs(days) <= 120; half the input postdates t. No document date can "
                                           "move this."}
                rows.append(row); continue

            if doss is None:
                row["detail"] = {"reject": "(e.0) no dossier for this event"}
                rows.append(row); continue

            if f in ("actor", "target"):
                words = ("actor",) if f == "actor" else (("target", "location") if used_location else ("target",))
                ka, d = receipt(doss, val, edate, role_words=words)
                d["role_words_required"] = list(words)
            elif f == "tempo":
                if not dyad:
                    ka, d = None, {"reject": "(e.3) the event has no dyad in event_entities"}
                else:
                    per, worst, blocked = {}, None, None
                    for en in sorted(dyad):
                        k, dd = receipt(doss, en, edate, require_role=False)
                        per[en] = dd
                        if k is None:
                            blocked = blocked or f"{en}: {dd.get('reject')}"
                        elif worst is None or k > worst:
                            worst = k
                    ka = None if blocked else worst
                    d = {"dyad": sorted(dyad), "per_member": per,
                         "reject": (f"(e.3) a dyad member has no receipt -- {blocked}" if blocked else None)}
            else:                                          # asset_role -- (e.4)
                chokes = sorted(x for x in (set().union(*roles[eid].values()) if roles[eid] else set())
                                if x.startswith("chokepoint."))
                if not chokes:
                    ka, d = None, {"reject": "(e.4) the value rests on the class alone "
                                             "(type == chokepoint_disruption, no chokepoint.* entity); no receipt"}
                else:
                    ka, d, chosen = None, None, None
                    for cp in chokes:                      # any chokepoint entity with a receipt serves
                        k, dd = receipt(doss, cp, edate, require_role=False)
                        if k is not None:
                            ka, d, chosen = k, dd, cp
                            break
                        d = dd
                    if ka is None:
                        d = dict(d or {}, reject=f"(e.4) no chokepoint entity {chokes} has a receipt: "
                                                 f"{(d or {}).get('reject')}")

            if ka is not None:
                row["after"] = ka
                row["after_rule"] = "e.2:dossier_doc_date" if f in ("actor", "target") else (
                    "e.3:dossier_dyad_date" if f == "tempo" else "e.4:dossier_chokepoint_date")
            row["detail"] = d
            rows.append(row)
            audit.append({**{k: row[k] for k in ("event_id", "event_date", "field", "value",
                                                 "before", "before_rule", "after", "after_rule")},
                          "declared_knowable_at": doss["declared_knowable_at"], "detail": d})
    return ev, rows, audit, dossiers


def kept(row, key):
    """A value survives the join iff its date is <= the event date and is not 'unknown'
    (WORLD_STATE_FRAMEWORK Amendment A rule 2, as situation_state.situation_rows_at applies it)."""
    d = row[key]
    return d != "unknown" and d <= row["event_date"]


def summarise(ev, rows):
    n_ev = len(ev)
    tot = len(rows)
    before_k = [r for r in rows if kept(r, "before")]
    after_k = [r for r in rows if kept(r, "after")]
    by_field = {}
    for f in FIELDS:
        rs = [r for r in rows if r["field"] == f]
        by_field[f] = {"values": len(rs),
                       "kept_before": sum(1 for r in rs if kept(r, "before")),
                       "kept_after": sum(1 for r in rs if kept(r, "after"))}
    ev_before = {r["event_id"] for r in before_k}
    ev_after = {r["event_id"] for r in after_k}
    moved_later = [r for r in rows if r["after"] != "unknown" and r["before"] != "unknown"
                   and r["after"] > r["before"]]
    moved_earlier = [r for r in rows if r["after"] != "unknown" and r["before"] != "unknown"
                     and r["after"] < r["before"]]
    lost = [r for r in rows if kept(r, "before") and not kept(r, "after")]
    gained = [r for r in rows if kept(r, "after") and not kept(r, "before")]
    doss_rows = [r for r in rows if r["has_dossier"]]
    # Amendment 2 (registered after the numbers; gates nothing): the alternative reading in which
    # knowable_at is the EARLIEST date any receipt establishes, so (a)/(c) and (e) combine by min.
    for r in rows:
        cands = [d for d in (r["before"], r["after"]) if d != "unknown"]
        r["diag_min"] = max(min(cands), r["event_date"]) if cands else "unknown"
    diag_k = [r for r in rows if r["diag_min"] != "unknown" and r["diag_min"] <= r["event_date"]]
    rules_before, rules_after = defaultdict(int), defaultdict(int)
    for r in rows:
        rules_before[r["before_rule"]] += 1
        rules_after[r["after_rule"]] += 1
    rejects = defaultdict(int)
    for r in rows:
        d = r["detail"] or {}
        if isinstance(d, dict) and d.get("reject"):
            rejects[re.sub(r"--.*", "--", str(d["reject"]))[:110]] += 1
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "registration": "docs/g/G3_REGISTRATION.md (2026-09-03)",
        "n_events": n_ev, "n_situation_values": tot,
        "before": {"kept": len(before_k), "dropped": tot - len(before_k),
                   "events_with_a_field_at_t": len(ev_before),
                   "events_with_no_field_at_t": n_ev - len(ev_before), "rules": dict(rules_before)},
        "after": {"kept": len(after_k), "dropped": tot - len(after_k),
                  "events_with_a_field_at_t": len(ev_after),
                  "events_with_no_field_at_t": n_ev - len(ev_after), "rules": dict(rules_after)},
        "delta": {"values_gained": len(gained), "values_lost": len(lost),
                  "net": len(after_k) - len(before_k),
                  "events_gained": len(ev_after - ev_before), "events_lost": len(ev_before - ev_after)},
        "moved_later": len(moved_later), "moved_earlier": len(moved_earlier),
        "by_field": by_field,
        "dossier_events": {"n": len({r["event_id"] for r in doss_rows}), "values": len(doss_rows),
                           "kept_before": sum(1 for r in doss_rows if kept(r, "before")),
                           "kept_after": sum(1 for r in doss_rows if kept(r, "after"))},
        "diagnostic_min_of_a_and_e": {
            "registered": False,
            "note": "G3_REGISTRATION Amendment 2: min(rule (a)/(c), rule (e)) with the (e.6) clamp. "
                    "A diagnostic; it does not move the registered count above.",
            "kept": len(diag_k), "dropped": tot - len(diag_k),
            "events_with_a_field_at_t": len({r["event_id"] for r in diag_k}),
            "vs_registered_after": len(diag_k) - len(after_k)},
        "conflict_scope_reclassified": sum(1 for r in rows if r["after_rule"].startswith("e.8")),
        "rejection_reasons": dict(sorted(rejects.items(), key=lambda kv: -kv[1])),
        "lost_rows": [{k: r[k] for k in ("event_id", "field", "value", "before", "before_rule", "after", "after_rule")}
                      for r in lost],
        "gained_rows": [{k: r[k] for k in ("event_id", "field", "value", "before", "before_rule", "after", "after_rule")}
                        for r in gained],
    }


def check_baseline(summary):
    """The BEFORE column is recomputed here, not copied. It must reproduce session A's published file."""
    if not BASELINE.exists():
        return {"checked": False, "reason": "data/state/situation_knowable.json not in the tree"}
    b = json.loads(BASELINE.read_text())
    got = {"events": summary["n_events"], "kept": summary["before"]["kept"],
           "dropped_after_t": summary["before"]["dropped"],
           "events_with_no_situation_field_at_t": summary["before"]["events_with_no_field_at_t"],
           "values": summary["n_situation_values"],
           "knowable_at_rules": summary["before"]["rules"]}
    want = {k: b[k] for k in got if k in b}
    want["values"] = sum(b["knowable_at_rules"].values())
    return {"checked": True, "published": want, "recomputed": got,
            "agrees": all(want[k] == got[k] for k in want)}


def to_md(summary, base, rows, audit):
    L = []
    a = L.append
    a("# G-3 — the situation fields' `knowable_at`, derived from dossier document dates")
    a("*Computed by `src/situation_vintage.py` under `docs/g/G3_REGISTRATION.md`, which was committed first.*")
    a(f"*Generated {summary['generated_at']}. Nothing here is written to `events` or `situation_state`.*\n")
    a("## 0. The BEFORE column is recomputed, not copied\n")
    a("Session A's rules (a)–(d) are re-implemented in this script and run against the same database, so the")
    a("baseline can be checked rather than trusted. Against `data/state/situation_knowable.json`:\n")
    a(f"    published:  {json.dumps(base.get('published'))}")
    a(f"    recomputed: {json.dumps(base.get('recomputed'))}")
    a(f"    agrees:     {base.get('agrees')}\n")
    a("## 1. Before and after\n")
    a("| | situation values | kept at t | dropped at t | events with ≥1 field at t |")
    a("|---|---|---|---|---|")
    for k, lab in (("before", "Amendment A, as published"), ("after", "with rule (e)")):
        s = summary[k]
        a(f"| {lab} | {summary['n_situation_values']} | **{s['kept']}** | {s['dropped']} | "
          f"{s['events_with_a_field_at_t']} of {summary['n_events']} |")
    dg = summary["diagnostic_min_of_a_and_e"]
    a(f"| *diagnostic, not registered:* min of (a)/(c) and (e) | {summary['n_situation_values']} | "
      f"*{dg['kept']}* | {dg['dropped']} | {dg['events_with_a_field_at_t']} of {summary['n_events']} |")
    d = summary["delta"]
    a(f"\nThe diagnostic row is Amendment 2 and **gates nothing**: it prices the (e.0) choice to let a")
    a(f"transcribed document date override a date read out of a URL path, at {dg['vs_registered_after']:+d} values.\n")
    a(f"Net **{d['net']:+d}** values ({d['values_gained']} gained, {d['values_lost']} lost); "
      f"**{d['events_gained']:+d}** events gain a field at t, {d['events_lost']} lose their last one.\n")
    a("## 2. By field\n")
    a("| field | values | kept before | kept after | change |")
    a("|---|---|---|---|---|")
    for f, v in summary["by_field"].items():
        a(f"| `{f}` | {v['values']} | {v['kept_before']} | {v['kept_after']} | "
          f"{v['kept_after'] - v['kept_before']:+d} |")
    a(f"\n`conflict_scope`: {summary['conflict_scope_reclassified']} values reclassified by (e.8) from the coding")
    a("date to `event_date + 120 days`. This is a **correction, not a recovery** — it cannot raise the kept")
    a("count, and it says the field can never be a target-side feature of any read, at any level of sourcing.\n")
    a("## 3. Which rule dated each value\n")
    a("| rule | before | after |")
    a("|---|---|---|")
    for r in sorted(set(summary["before"]["rules"]) | set(summary["after"]["rules"])):
        a(f"| `{r}` | {summary['before']['rules'].get(r, 0)} | {summary['after']['rules'].get(r, 0)} |")
    a("\n## 4. Why rule (e) did not fire, where it did not\n")
    a("| count | clause and reason |")
    a("|---|---|")
    for k, v in summary["rejection_reasons"].items():
        a(f"| {v} | {k} |")
    if summary["lost_rows"]:
        a("\n## 5. Values rule (e) moved LATER than Amendment A gave them (the losses)\n")
        a("| event | field | value | before | after |")
        a("|---|---|---|---|---|")
        for r in summary["lost_rows"]:
            a(f"| `{r['event_id']}` | {r['field']} | {r['value']} | {r['before']} ({r['before_rule']}) | {r['after']} ({r['after_rule']}) |")
    if summary["gained_rows"]:
        a("\n## 6. Values rule (e) recovered\n")
        a("| event | field | value | before | after |")
        a("|---|---|---|---|---|")
        for r in summary["gained_rows"]:
            a(f"| `{r['event_id']}` | {r['field']} | {r['value']} | {r['before']} ({r['before_rule']}) | {r['after']} |")
    a("\n## 7. The audit table — every decision, against the dossier text it came from\n")
    a("One row per field rule (e) was **considered** for, derived or not. Open")
    a("`data/dossiers/<event_id>.md`, find the quoted bullet, and check the decision follows.")
    a("Registration §6: finding nothing wrong here is not evidence that it is right.\n")
    for r in audit:
        det = r["detail"] or {}
        a(f"### `{r['event_id']}` · {r['event_date']} · `{r['field']}` = `{r['value']}`")
        a(f"- before: **{r['before']}** ({r['before_rule']}) → after: **{r['after']}** ({r['after_rule']})")
        if r.get("declared_knowable_at"):
            a(f"- the dossier's own `## Knowable at` asserts **{r['declared_knowable_at']}** "
              f"(an inference; rule (e.7) uses the document, not the assertion)")
        if det.get("bullet"):
            a(f"- dossier bullet, verbatim: `{det['bullet']}`")
        if det.get("dates"):
            for mk, dd in det["dates"].items():
                a(f"  - S{mk}: `{dd.get('cell')}` → **{dd.get('doc_date')}** ({dd.get('parse')})")
        if det.get("earliest_doc_date"):
            a(f"- earliest cited document: **{det['earliest_doc_date']}**"
              + (" (before the event date; clamped to it by (e.6))" if det.get("clamped") else ""))
        if det.get("per_member"):
            for en, dd in det["per_member"].items():
                a(f"  - dyad member `{en}`: " + (dd.get("reject") or f"earliest {dd.get('earliest_doc_date')}"))
        if det.get("reject"):
            a(f"- **not derived:** {det['reject']}")
        if det.get("reason"):
            a(f"- {det['reason']}")
        a("")
    return "\n".join(L)


def main():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)      # read-only: this script writes no table
    try:
        ev, rows, audit, dossiers = derive(conn)
    finally:
        conn.close()
    summary = summarise(ev, rows)
    base = check_baseline(summary)
    summary["baseline_check"] = base
    summary["dossiers_read"] = {k: {"n_sources": len(v["sources"]),
                                    "n_sources_dated": sum(1 for s in v["sources"].values() if s["doc_date"]),
                                    "n_entity_bullets": len(v["entities"]),
                                    "declared_knowable_at": v["declared_knowable_at"],
                                    "in_events": k in ev} for k, v in sorted(dossiers.items())}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({**summary, "rows": rows}, indent=1, default=str))
    OUT_MD.write_text(to_md(summary, base, rows, audit))
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("lost_rows", "gained_rows", "dossiers_read", "rejection_reasons")},
                     indent=1, default=str))
    if not base.get("agrees", False):
        print("\nWARNING: the recomputed BEFORE column does not reproduce data/state/situation_knowable.json")
        print(json.dumps(base, indent=1))
    return summary


if __name__ == "__main__":
    main()
