"""outcomes.py -- PATH Step 4 (code): independent outcomes from ICB, MID and UCDP, mapped to the four branches by
OUTCOME_MAPPING.md, and Cohen's kappa against the corpus-derived sr_outcome_90.

    event_outcomes(event_id, source, field, value, value_text, detail)

Reads events / event_entities (never writes them) and the cached ICB (icb1v16, icb2v16, dyads), COW dyadic MID
and UCDP/PRIO files. Writes event_outcomes, data/state/outcomes_kappa.json (kappa per source + pooled, the
confusion table, n, the no_independent_outcome count) and data/audits/outcome_audit_60.csv (the disagreements
for Joe's audit). Nothing in `events` changes here: the kappa < 0.6 rule fires only after the audit is recorded.

Run:  python3 src/state/outcomes.py
"""
import csv
import json
import random
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402
import icb as ICB  # noqa: E402

BRANCHES = ("CONTAINED", "LIMITED_RETALIATION", "WIDENING", "RESOLUTION_BY_DEAL")
GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
KAPPA_OUT = P.DATA / "state" / "outcomes_kappa.json"
AUDIT_OUT = P.DATA / "audits" / "outcome_audit_60.csv"
REGISTRATION = "OUTCOME_MAPPING.md (2026-09-02)"
SEED = 20260902
SCHEMA = """
CREATE TABLE IF NOT EXISTS event_outcomes (
    event_id   TEXT NOT NULL,
    source     TEXT NOT NULL,          -- icb | mid | ucdp | precedence
    field      TEXT NOT NULL,          -- branch | viol | forout | outesr | hihost | fatlev | intensity_y1 | ... | no_independent_outcome
    value      REAL,
    value_text TEXT,
    detail     TEXT,                   -- crisno/crisname, disno, conflict ids
    computed_at TEXT NOT NULL,
    PRIMARY KEY (event_id, source, field)
);
"""


def ensure_schema(conn):
    conn.executescript(SCHEMA); conn.commit()


# ----------------------------------------------------------------------------- the registered maps (§3)

def map_icb(viol, forout=None, outesr=None):
    if viol is None or pd.isna(viol):
        return None
    viol = int(viol)
    if forout is not None and not pd.isna(forout) and int(forout) in (1, 2) and viol <= 2:
        return "RESOLUTION_BY_DEAL"
    if viol == 4:
        return "WIDENING"
    if viol == 3:
        return "WIDENING" if (outesr is not None and not pd.isna(outesr) and int(outesr) == 1) else "LIMITED_RETALIATION"
    if viol == 2:
        return "LIMITED_RETALIATION"
    return "CONTAINED"


def map_mid(hihost, fatlev=None, settlmnt=None):
    if hihost is None or pd.isna(hihost):
        return None
    h = int(hihost)
    if h == 5:
        return "WIDENING"
    if h == 4:
        return "WIDENING" if (fatlev is not None and not pd.isna(fatlev) and int(fatlev) >= 3) else "LIMITED_RETALIATION"
    if h in (2, 3) and settlmnt is not None and not pd.isna(settlmnt) and int(settlmnt) == 1:
        return "RESOLUTION_BY_DEAL"
    return "CONTAINED"


def map_ucdp(i0, i1):
    i0 = int(i0 or 0); i1 = int(i1 or 0)
    if i1 == 2:
        return "WIDENING" if i0 < 2 else "LIMITED_RETALIATION"
    if i1 == 1:
        return "LIMITED_RETALIATION"
    return "CONTAINED"


# ----------------------------------------------------------------------------- kappa (§5)

def cohen_kappa(a, b, labels=BRANCHES):
    """Unweighted Cohen's kappa on paired labels; returns (kappa, n, confusion{a:{b:n}})."""
    pairs = [(x, y) for x, y in zip(a, b) if x in labels and y in labels]
    n = len(pairs)
    conf = {la: {lb: 0 for lb in labels} for la in labels}
    for x, y in pairs:
        conf[x][y] += 1
    if n == 0:
        return None, 0, conf
    po = sum(conf[l][l] for l in labels) / n
    pe = sum((sum(conf[l].values()) / n) * (sum(conf[k][l] for k in labels) / n) for l in labels)
    k = None if pe == 1 else (po - pe) / (1 - pe)
    return (None if k is None else round(k, 4)), n, conf


# ----------------------------------------------------------------------------- matching (§2)

def _corpus(conn):
    ev = pd.read_sql("SELECT event_id, event_date, type, title, source_url, sr_actor, sr_target, sr_outcome_90 FROM events", conn)
    ev["event_date"] = pd.to_datetime(ev["event_date"])
    ents = defaultdict(set); roles = defaultdict(lambda: defaultdict(set))
    for eid, en, role in conn.execute("SELECT event_id, entity_id, role FROM event_entities"):
        if en.startswith("country."):
            ents[eid].add(en); roles[eid][role or "mention"].add(en)
    return ev, ents, roles


def _actors_and_pairs(r, ents, roles):
    A = set(ents.get(r.event_id, set()))
    for e in (r.sr_actor, r.sr_target):
        if isinstance(e, str) and e.startswith("country."):
            A.add(e)
    P_ = set()
    if isinstance(r.sr_actor, str) and isinstance(r.sr_target, str) and r.sr_actor.startswith("country.") and r.sr_target.startswith("country.") and r.sr_actor != r.sr_target:
        P_.add(frozenset((r.sr_actor, r.sr_target)))
    rr = roles.get(r.event_id, {})
    for a in rr.get("actor", set()):
        for t in rr.get("target", set()) | rr.get("location", set()):
            if a != t:
                P_.add(frozenset((a, t)))
    if not P_ and len(A) >= 2:
        P_ = {frozenset((a, b)) for a in A for b in A if a < b}
    return A, P_


def load_icb():
    sysd = ICB.crises()
    act = pd.read_csv(P.raw_path("icb", "icb2v16.csv"), encoding="latin-1"); act.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in act.columns]
    dy = pd.read_csv(P.raw_path("icb", "icb_dyads_v16.csv"), encoding="latin-1")
    members = defaultdict(set)
    for r in act.itertuples(index=False):
        e = C.from_ccode(r.cracid)
        if e:
            members[int(r.crisno)].add(e)
    for r in dy.itertuples(index=False):
        for cc in (r.statea, r.stateb):
            e = C.from_ccode(cc)
            if e:
                members[int(r.crisno)].add(e)
    return sysd, members


def match_icb(r, A, sysd, members):
    d = r.event_date
    cands = []
    for c in sysd.itertuples(index=False):
        if pd.isna(c.trigdate) or pd.isna(c.termdate):
            continue
        if not (c.trigdate - pd.Timedelta(days=30) <= d <= c.termdate):
            continue
        if not (A & members.get(int(c.crisno), set())):
            continue
        cands.append(c)
    if not cands:
        return None
    before = [c for c in cands if c.trigdate <= d + pd.Timedelta(days=30)]
    pick = max(before, key=lambda c: c.trigdate) if before else min(cands, key=lambda c: abs((c.trigdate - d).days))
    return pick


def load_mid():
    m = pd.read_csv(P.raw_path("cow_mid", "dyadic_mid_4.03.csv"))
    m["ea"] = m["statea"].map(C.from_ccode); m["eb"] = m["stateb"].map(C.from_ccode)
    m = m.dropna(subset=["ea", "eb"])
    m["start"] = pd.to_datetime(dict(year=m.strtyr, month=m.strtmnth.clip(1, 12), day=m.strtday.clip(1, 28)), errors="coerce")
    m["end"] = pd.to_datetime(dict(year=m.endyear, month=m.endmnth.clip(1, 12), day=m.endday.clip(1, 28)), errors="coerce")
    m["pair"] = [frozenset((a, b)) for a, b in zip(m["ea"], m["eb"])]
    return m


def match_mid(r, A, pairs, mid):
    d = r.event_date
    sub = mid[mid["pair"].isin(pairs)] if pairs else mid[mid["ea"].isin(A) & mid["eb"].isin(A)]
    sub = sub[(sub["start"] - pd.Timedelta(days=30) <= d) & (d <= sub["end"] + pd.Timedelta(days=90))]
    if sub.empty:
        return None
    return sub.iloc[(sub["start"] - d).abs().argsort().iloc[0]]


def load_ucdp():
    acd = pd.read_csv(P.raw_path("ucdp", "UcdpPrioConflict_v26_1.csv"))
    rows = []
    for r in acd.itertuples(index=False):
        for tok in str(r.gwno_loc).replace(";", ",").split(","):
            tok = tok.strip()
            e = C.from_ccode(int(tok)) if tok.isdigit() else None
            if e:
                rows.append((e, int(r.year), int(r.intensity_level), int(r.conflict_id)))
    return pd.DataFrame(rows, columns=["ent", "year", "intensity", "conflict_id"])


def match_ucdp(r, A, roles_r, ucdp):
    locs = set(roles_r.get("location", set())) | set(roles_r.get("target", set())) or A
    y = r.event_date.year
    sub = ucdp[ucdp["ent"].isin(locs)]
    if sub.empty and not ucdp[ucdp["year"] == y].empty and y >= 1946:
        return {"i0": 0, "i1": 0, "locs": sorted(locs), "ids": []}                 # data exist for the year: no conflict there = 0
    if sub.empty:
        return None
    i0 = int(sub[sub["year"] == y - 1]["intensity"].max()) if (sub["year"] == y - 1).any() else 0
    w = sub[sub["year"].isin([y, y + 1])]
    i1 = int(w["intensity"].max()) if not w.empty else 0
    return {"i0": i0, "i1": i1, "locs": sorted(locs), "ids": sorted(w["conflict_id"].unique().tolist())}


# ----------------------------------------------------------------------------- the run

def run(conn, write=True):
    ensure_schema(conn)
    ev, ents, roles = _corpus(conn)
    sysd, members = load_icb()
    mid = load_mid()
    ucdp = load_ucdp()
    ts = P.now()
    rows, labels = [], {}
    for r in ev.itertuples(index=False):
        if r.type not in GEO_TYPES:
            continue
        A, pairs = _actors_and_pairs(r, ents, roles)
        per = {}
        c = match_icb(r, A, sysd, members)
        if c is not None:
            b = map_icb(c.viol, c.forout, c.outesr)
            per["icb"] = b
            det = f"crisno {int(c.crisno)} {c.crisname} {c.trigdate.date()}..{c.termdate.date()}"
            for f, v in (("viol", c.viol), ("sevviosy", getattr(c, "sevviosy", None)), ("forout", c.forout), ("outesr", c.outesr), ("gpinv", getattr(c, "gpinv", None)), ("globactm", getattr(c, "globactm", None))):
                if v is not None and not pd.isna(v):
                    rows.append((r.event_id, "icb", f, float(v), None, det, ts))
            if b:
                rows.append((r.event_id, "icb", "branch", None, b, det, ts))
        m = match_mid(r, A, pairs, mid)
        if m is not None:
            b = map_mid(m.hihost, m.fatlev, m.settlmnt)
            per["mid"] = b
            det = f"disno {int(m.disno)} {m.namea}-{m.nameb} {m.start.date() if pd.notna(m.start) else ''}..{m.end.date() if pd.notna(m.end) else ''}"
            for f, v in (("hihost", m.hihost), ("fatlev", m.fatlev), ("outcome", m.outcome), ("settlmnt", m.settlmnt)):
                if v is not None and not pd.isna(v):
                    rows.append((r.event_id, "mid", f, float(v), None, det, ts))
            if b:
                rows.append((r.event_id, "mid", "branch", None, b, det, ts))
        u = match_ucdp(r, A, roles.get(r.event_id, {}), ucdp)
        if u is not None:
            b = map_ucdp(u["i0"], u["i1"])
            per["ucdp"] = b
            det = f"locations {','.join(u['locs'])} conflicts {u['ids']}"
            rows.append((r.event_id, "ucdp", "intensity_y0", float(u["i0"]), None, det, ts))
            rows.append((r.event_id, "ucdp", "intensity_y1", float(u["i1"]), None, det, ts))
            rows.append((r.event_id, "ucdp", "branch", None, b, det, ts))
        prec = per.get("icb") or per.get("mid") or per.get("ucdp")
        if prec:
            src = "icb" if per.get("icb") else ("mid" if per.get("mid") else "ucdp")
            rows.append((r.event_id, "precedence", "branch", None, prec, src, ts))
        else:
            rows.append((r.event_id, "precedence", "no_independent_outcome", 1.0, None, "no ICB crisis, MID dispute or UCDP conflict-year matched", ts))
        labels[r.event_id] = {"ours": r.sr_outcome_90, **per, "precedence": prec, "type": r.type, "date": str(r.event_date.date()),
                              "title": r.title, "url": r.source_url}
    if write:
        conn.execute("DELETE FROM event_outcomes")
        conn.executemany("INSERT OR REPLACE INTO event_outcomes VALUES (?,?,?,?,?,?,?)", rows)
        conn.commit()
    return rows, labels


def kappa_report(labels):
    out = {"registration": REGISTRATION, "generated_at": P.now(), "n_geopolitical_events": len(labels), "sources": {}}
    ours = {e: v["ours"] for e, v in labels.items() if v["ours"] in BRANCHES}
    for src in ("icb", "mid", "ucdp", "precedence"):
        pairs = [(ours[e], v[src]) for e, v in labels.items() if e in ours and v.get(src) in BRANCHES]
        k, n, conf = cohen_kappa([a for a, _ in pairs], [b for _, b in pairs])
        agree = sum(1 for a, b in pairs if a == b)
        out["sources"][src] = {"kappa": k, "n": n, "agreement_pct": round(100 * agree / n, 1) if n else None, "confusion_ours_x_theirs": conf,
                               "theirs_distribution": dict(Counter(b for _, b in pairs))}
    out["no_independent_outcome"] = sum(1 for v in labels.values() if not v["precedence"])
    out["ours_unknown"] = sum(1 for v in labels.values() if v["ours"] not in BRANCHES)
    k = out["sources"]["precedence"]["kappa"]
    out["decision_rule"] = {"threshold": 0.6, "kappa_precedence": k,
                            "would_replace_branches": (k is not None and k < 0.6),
                            "status": "awaiting Joe's audit (data/audits/outcome_audit_60.csv); no branch changed"}
    return out


def audit_sheet(labels, n=60, seed=SEED):
    """The disagreements, stratified proportionally by class x era (largest remainder), seeded."""
    dis = [(e, v) for e, v in labels.items() if v["ours"] in BRANCHES and v["precedence"] in BRANCHES and v["ours"] != v["precedence"]]
    strata = defaultdict(list)
    for e, v in dis:
        strata[(v["type"], "1946-86" if v["date"] < "1987-01-01" else "1987->")].append((e, v))
    rng = random.Random(seed)
    total = len(dis)
    pick = []
    if total <= n:
        pick = dis
    else:
        quota = {k: n * len(vs) / total for k, vs in strata.items()}
        base = {k: int(q) for k, q in quota.items()}
        rem = n - sum(base.values())
        for k in sorted(quota, key=lambda k: quota[k] - base[k], reverse=True)[:rem]:
            base[k] += 1
        for k, vs in strata.items():
            vs = sorted(vs, key=lambda x: x[0]); rng.shuffle(vs)
            pick += vs[:base[k]]
    pick.sort(key=lambda x: x[1]["date"])
    return pick, total


def write_audit(pick, total, conn):
    AUDIT_OUT.parent.mkdir(parents=True, exist_ok=True)
    det = defaultdict(dict)
    for eid, src, f, v, vt, d in conn.execute("SELECT event_id, source, field, value, value_text, detail FROM event_outcomes"):
        det[eid][f"{src}.{f}"] = vt if vt is not None else v
        det[eid][f"{src}.detail"] = d
    cols = ["event_id", "event_date", "class", "title", "source_url", "our_branch_sr_outcome_90", "independent_branch", "independent_source",
            "icb_branch", "icb_detail", "icb_viol", "icb_forout", "icb_outesr", "mid_branch", "mid_detail", "mid_hihost", "mid_fatlev", "mid_settlmnt",
            "ucdp_branch", "ucdp_detail", "ucdp_intensity_y0", "ucdp_intensity_y1", "joe_branch", "joe_note"]
    with open(AUDIT_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cols)
        for e, v in pick:
            d = det.get(e, {})
            w.writerow([e, v["date"], v["type"], v["title"], v["url"], v["ours"], v["precedence"], d.get("precedence.detail"),
                        v.get("icb"), d.get("icb.detail"), d.get("icb.viol"), d.get("icb.forout"), d.get("icb.outesr"),
                        v.get("mid"), d.get("mid.detail"), d.get("mid.hihost"), d.get("mid.fatlev"), d.get("mid.settlmnt"),
                        v.get("ucdp"), d.get("ucdp.detail"), d.get("ucdp.intensity_y0"), d.get("ucdp.intensity_y1"), "", ""])
    return len(pick), total


def main():
    conn = sqlite3.connect(P.DB)
    try:
        rows, labels = run(conn)
        rep = kappa_report(labels)
        pick, total = audit_sheet(labels)
        n_written, _ = write_audit(pick, total, conn)
    finally:
        conn.close()
    rep["audit"] = {"file": str(AUDIT_OUT.relative_to(P.ROOT)), "rows": n_written, "disagreements_total": total, "seed": SEED}
    KAPPA_OUT.write_text(json.dumps(rep, indent=1, default=str))
    print(f"event_outcomes: {len(rows)} rows for {len(labels)} geopolitical events; no independent outcome: {rep['no_independent_outcome']}; ours unknown: {rep['ours_unknown']}")
    for src, s in rep["sources"].items():
        print(f"  {src:11s} kappa {s['kappa']}  n={s['n']}  agreement {s['agreement_pct']}%  theirs {s['theirs_distribution']}")
    print(f"  decision rule: {rep['decision_rule']}")
    print(f"  audit sheet: {n_written} of {total} disagreements -> {AUDIT_OUT}")


if __name__ == "__main__":
    main()
