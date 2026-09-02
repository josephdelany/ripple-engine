"""state_of_engine.py -- write STATE_OF_THE_ENGINE.md from the LIVE database and the published receipts.

Generated, never hand-typed (like DATA_DICTIONARY.md), so it cannot drift from what the engine holds:
corpus counts, series/observations, engine status, the state panel (status.json), independent outcomes
(IES-90 distribution), the walk (summary.json verdict), and PATH.md §3 D1-D7 as last recorded by
`python3 src/acceptance_v2.py --dod` (data/acceptance_dod.json). Every number carries its receipt path.
The hand-written 2026-08-04 after-picture is preserved at docs/STATE_OF_THE_ENGINE_2026-08-04.md.

Run:  python3 src/state_of_engine.py
"""
import json
import sqlite3
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "STATE_OF_THE_ENGINE.md"
GEO = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")


def _json(rel):
    p = ROOT / rel
    return json.loads(p.read_text()) if p.exists() else {}


def _n(x):
    return x if isinstance(x, int) else len(x or [])


def _git():
    try:
        return subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"], cwd=ROOT, capture_output=True, text=True).stdout.strip()[:120]
    except Exception:
        return "?"


def main():
    conn = sqlite3.connect(DB)
    q = lambda sql, *a: conn.execute(sql, a).fetchall()  # noqa: E731
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    L = [f"# STATE OF THE ENGINE — generated {now}", "",
         "_Generated from the live `data/oil.db` and the published receipts by `src/state_of_engine.py` — not hand-typed. "
         "Every number names its receipt. The 2026-08-04 hand-written after-picture is kept at `docs/STATE_OF_THE_ENGINE_2026-08-04.md`._",
         "", f"HEAD: `{_git()}`", ""]

    # --- corpus
    n_ev = q("SELECT COUNT(*) FROM events")[0][0]
    by_type = q("SELECT type, COUNT(*) FROM events GROUP BY 1 ORDER BY 2 DESC")
    dec = Counter(d[:3] + "0s" for (d,) in q("SELECT event_date FROM events WHERE type IN (?,?,?,?)", *GEO))
    L += ["## 1. Corpus (`events`, receipt: `data/events.csv`, `DATA_DICTIONARY.md`)", "",
          f"- {n_ev} events; by type: " + ", ".join(f"{t} {n}" for t, n in by_type),
          f"- geopolitical events by decade: " + ", ".join(f"{k} {v}" for k, v in sorted(dec.items())),
          f"- `sr_*` situation-record columns: corpus-derived; `sr_outcome_90` / `sr_outcome_30` RETIRED as outcomes (OUTCOME_MAPPING.md Amendment 1)", ""]

    # --- data
    n_series, n_obs = q("SELECT COUNT(*) FROM series")[0][0], q("SELECT COUNT(*) FROM observations")[0][0]
    es = _json("data/engine_status.json")
    fr = es.get("freshness") or {}
    L += ["## 2. Data (`series`, `observations`; receipts: `data/engine_status.json`, `data/health_status.json`)", "",
          f"- {n_series} series, {n_obs:,} observations; last obs {q('SELECT MAX(obs_date) FROM observations')[0][0]}",
          f"- engine status **{es.get('verdict', '?')}** at {es.get('generated_at', '?')[:16]}: {'; '.join(es.get('reasons') or [])}",
          f"- freshness: {fr.get('n_dead', '?')} DEAD, {fr.get('n_stale', '?')} STALE (heartbeat); integrity findings: `data/integrity_report.txt`", ""]

    # --- state panel
    st = _json("data/state/status.json")
    fields_map = st.get("fields") or {}
    loaders = st.get("loaders") or {str((v or {}).get("source", ""))[:40] for v in fields_map.values()} - {""}   # distinct sources behind the loaded fields
    L += ["## 3. World state (`state_panel`; receipt: `data/state/status.json`, `WORLD_STATE_CODEBOOK.md`)", "",
          f"- {q('SELECT COUNT(*) FROM state_panel')[0][0]:,} panel rows from {len(loaders)} loaders (status {st.get('generated_at', '?')[:10]}); "
          f"fields loaded {_n(st.get('fields_loaded'))} / registered {_n(st.get('fields_registered'))}; unloaded: {_n(st.get('fields_unloaded'))}",
          f"- licence-restricted inputs live in `data/state/local/` (never committed; README there); keyless raw downloads in `data/state/raw/` (gitignored, rebuilt by loaders)", ""]

    # --- outcomes
    d = _json("data/state/ies90_distribution.json")
    k = _json("data/state/outcomes_kappa.json")
    a2 = d.get("amendment_2") or {}
    L += ["## 4. Independent outcomes — IES-90 (`event_outcomes` source='ies90'; receipts: `data/state/ies90_distribution.json`, `OUTCOME_MAPPING.md`)", "",
          f"- registration: {d.get('registration', '?')}; {d.get('n_geopolitical_events', '?')} geopolitical events; level counts {d.get('level_counts')}",
          f"- by basis (Amendment 2): {a2.get('level_by_basis')}",
          f"- coverage by source: {d.get('coverage_events_by_source')}; uncovered (no_independent_outcome): {(d.get('no_independent_outcome') or {}).get('total')}",
          f"- GED is location-only (no dyad field in the cache); {len((d.get('ged') or {}).get('unmapped_country_names') or [])} GED names unmapped (listed in the file)",
          f"- audit for Joe: `{(d.get('audit') or {}).get('file')}` — {(d.get('audit') or {}).get('events')} events / {(d.get('audit') or {}).get('source_rows')} source rows; Joe's record: `data/audits/outcome_audit.json` {'present' if (ROOT / 'data/audits/outcome_audit.json').exists() else 'ABSENT'}",
          f"- for the record: Step 4 kappa vs the retired label — precedence κ {((k.get('sources') or {}).get('precedence') or {}).get('kappa')} (n {((k.get('sources') or {}).get('precedence') or {}).get('n')}); `data/state/outcomes_kappa.json`, `data/audits/outcome_audit_60.csv`", ""]

    # --- walk
    w = _json("data/walk_forward/summary.json")
    tiers = w.get("tiers") or {}
    v = w.get("verdict") or {}
    lines = ["## 5. The walk (receipt: `data/walk_forward/summary.json`, `WALK_FORWARD_PROTOCOL.md`)", "",
             f"- run `{w.get('run_id', '?')}` generated {str(w.get('generated_at', '?'))[:16]}; G target: {(w.get('registered') or {}).get('g_target', '?')}"]
    for t, tt in tiers.items():
        g = ((tt.get("G") or {}).get("engine_vs") or {}).get("climatology") or {}
        lines.append(f"- {t} tier: {tt.get('n_reads')} reads, {tt.get('n_scored_burn_in')} scored after burn-in, horizon {tt.get('horizon')} {tt.get('unit')}; "
                     f"G skill vs climatology {g.get('skill')} (dm_p {g.get('dm_p')}); permits validation: {tt.get('permits_validation')}")
    lines += [f"- engine:G verdict: {((v.get('rules') or {}).get('engine:G') or {}).get('status', '?')}; engine:P: {((v.get('rules') or {}).get('engine:P') or {}).get('status', '?')}; audit flag: {v.get('audit_passed')}",
              f"- leakage test asserted: {(w.get('leakage_test') or {}).get('asserted')} ({(w.get('leakage_test') or {}).get('verdict')}); placebo skill {((w.get('placebo') or {}).get('vs_random_analogs') or {}).get('skill')}; permutation p {(w.get('permutation') or {}).get('p_value')}", ""]
    L += lines

    # --- D1-D7
    dod = _json("data/acceptance_dod.json")
    L += ["## 6. Definition of done — PATH.md §3 D1–D7 (receipt: `data/acceptance_dod.json`, `python3 src/acceptance_v2.py --dod`)", ""]
    if dod:
        L.append(f"_recorded {dod.get('generated_at', '?')[:16]}{' (fast: D1 not run)' if dod.get('fast') else ''}_")
        L += ["", "| item | status | evidence | note |", "|---|---|---|---|"]
        for it in dod.get("items", []):
            L.append(f"| {it['name']} | **{it['status']}** | `{it['evidence']}` | {it['note'].replace('|', '/')} |")
        c = dod.get("counts") or {}
        L += ["", f"{c.get('PASS', 0)}/7 PASS, {c.get('PARTIAL', 0)} PARTIAL, {c.get('FAIL', 0)} FAIL. The product is finished only when all seven PASS (SESSION_CHARTER.md §5); no surface says it is.", ""]
    else:
        L += ["_not recorded — run `python3 src/acceptance_v2.py --dod`_", ""]

    conn.close()
    OUT.write_text("\n".join(L) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(L)} lines)")


if __name__ == "__main__":
    main()
