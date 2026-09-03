"""Brief A-5: the audit recorder never fills a row, saves after every answer (resumable), computes kappa with the
Step 4 code, passes only when every row is answered and kappa >= 0.6, and the desk reads it read-only."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import audit_ies90 as AU     # noqa: E402


def _sheet(tmp_path):
    src = ROOT / "data" / "audits" / "ies90_audit_30.csv"
    p = tmp_path / "sheet.csv"; p.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return p


def test_a5_scripted_audit_is_resumable_and_never_filled_by_code(tmp_path):
    sheet = _sheet(tmp_path); out = tmp_path / "outcome_audit.json"
    ev = AU.load_sheet(sheet)
    n = len(ev)
    assert n == 30
    # first sitting: Joe answers two rows (agreeing with the engine), skips one, quits
    ids = list(ev)
    eng = {e: ev[e]["event"]["ies90_level"] for e in ids}
    script = iter([eng[ids[0]], "n", "checked ICB", "s", eng[ids[2]], "y", "", "q"])
    o = AU.run(sheet, out, ask=lambda _: next(script), echo=lambda *_: None)
    assert o["n_done"] == 2 and o["n_rows"] == n and o["passed"] is False and o["auditor"] == "joe"
    assert [r["event_id"] for r in o["rows"]] == [ids[0], ids[2]]                 # the skipped row was not filled
    assert o["rows"][0]["joe_deal"] == 0 and o["rows"][1]["joe_deal"] == 1 and o["rows"][0]["joe_note"] == "checked ICB"
    assert json.loads(out.read_text())["n_done"] == 2                               # saved as it went
    # second sitting resumes at the first unanswered row (ids[1]) -- blank level records nothing, then quit
    script = iter(["", "q"])
    o = AU.run(sheet, out, ask=lambda _: next(script), echo=lambda *_: None)
    assert o["n_done"] == 2
    # answer everything, all agreeing -> kappa 1.0 and passed
    remaining = [e for e in ids if e not in {ids[0], ids[2]}]
    script = iter([x for e in remaining for x in (eng[e], "", "")])
    o = AU.run(sheet, out, ask=lambda _: next(script), echo=lambda *_: None)
    assert o["n_done"] == n and o["kappa"] == 1.0 and o["passed"] is True and o["dated"]
    # the desk reads the same file
    st = AU.status(sheet, out)
    assert st["status"] == "done" and st["passed"] and st["kappa"] == 1.0 and st["auditor"] == "joe"


def test_a5_kappa_is_the_step4_code_and_disagreement_fails(tmp_path):
    sheet = _sheet(tmp_path); out = tmp_path / "o.json"
    ev = AU.load_sheet(sheet); ids = list(ev)
    # Joe answers every row with level 0 -> the only agreement is on the engine's level-0 rows; kappa < 0.6 -> not passed
    script = iter([x for _ in ids for x in ("0", "", "")])
    o = AU.run(sheet, out, ask=lambda _: next(script), echo=lambda *_: None)
    import outcomes as O
    k, n_, _ = O.cohen_kappa(["0"] * len(ids), [str(ev[e]["event"]["ies90_level"]) for e in ids], labels=AU.LEVELS)
    assert o["n_done"] == len(ids) and o["kappa"] == k and o["passed"] is False


def test_a5_record_urls_point_at_the_record():
    assert AU.record_url("icb", "crisis 393 GULF WAR") == "https://www.icb.umd.edu/dataviewer/?crisno=393"
    assert "WarNum 211" in AU.record_url("war", "COW inter-state war 211 Gulf War (...)")
    assert "ucdp.uu.se/country/630" in AU.record_url("ged", "GED state-based deaths in country.iran (location, not dyad)", "country.iran")
    assert "dispute 3957" in AU.record_url("mid", "dispute 3957 IRQ-KUW")


def test_a5_desk_endpoint_reads_the_file_read_only():
    from fastapi.testclient import TestClient
    import backend
    r = TestClient(backend.app).get("/api/walk/audit")
    assert r.status_code == 200 and r.json()["status"] in ("pending", "in progress", "done") and r.json()["n_rows"] == 30


# --- OUTCOME_MAPPING Amendment 3: the hostility precondition, carried onto the sheet (2026-09-03) ------------------

def test_every_sheet_row_carries_session_F_hostility_and_none_are_dropped():
    """The published runs scored these labels, so all 30 rows stay; each says whether Amendment 3 would still score it."""
    import csv
    import ies90 as I
    rows = list(csv.DictReader(open(ROOT / "data" / "audits" / "ies90_audit_30.csv", encoding="utf-8")))
    ev = [r for r in rows if r["row_type"] == "event"]
    assert len(ev) == 30                                                   # nothing dropped for being non-hostile
    hm = I.hostility_map()
    assert len(hm) == 187                                                  # session F coded every geopolitical event
    for r in ev:
        assert r["hostility"] in ("hostile", "hostile_unattributed", "ambiguous", "non_hostile"), r["event_id"]
        assert r["hostility"] == hm[r["event_id"]][0]                      # taken from CLASS_AUDIT.md, not re-derived
        assert r["g_scorable"] == I.G_SCORABLE[r["hostility"]]
    assert any(r["hostility"] == "non_hostile" for r in ev)                # incl. abqaiq_arabian_1977, row 1
    assert next(r for r in ev if r["event_id"] == "abqaiq_arabian_1977")["hostility"] == "non_hostile"


def test_a_non_hostile_row_tells_joe_the_target_would_not_score_it():
    ev = AU.load_sheet()
    shown = []
    import builtins
    real = builtins.print
    builtins.print = lambda *a, **k: shown.append(" ".join(str(x) for x in a))
    try:
        AU.show("abqaiq_arabian_1977", ev["abqaiq_arabian_1977"], 1, 30)
    finally:
        builtins.print = real
    text = "\n".join(shown)
    assert "non_hostile" in text and "NOT G-scorable under Amendment 3" in text
    assert AU.NON_HOSTILE_NOTICE in text
    assert "no_independent_outcome" in text and "the published run scored it anyway" in text


def test_kappa_is_published_three_ways_and_the_gate_reads_all_rows(tmp_path):
    """all rows is the §7 gate because that is the set the published runs scored; the other two are diagnostics."""
    sheet = _sheet(tmp_path); out = tmp_path / "o.json"
    ev = AU.load_sheet(sheet); ids = list(ev)
    eng = {e: ev[e]["event"]["ies90_level"] for e in ids}
    script = iter([x for e in ids for x in (eng[e], "", "")])               # Joe agrees with every row
    o = AU.run(sheet, out, ask=lambda _: next(script), echo=lambda *_: None)
    kb = o["kappa_by_hostility"]
    assert set(kb) == {"all_rows", "hostile_only", "hostile_plus_ambiguous"}
    assert kb["all_rows"]["gate"] is True and kb["hostile_only"]["gate"] is False and kb["hostile_plus_ambiguous"]["gate"] is False
    assert o["kappa"] == kb["all_rows"]["kappa"]                            # the top-level figure IS the gate figure
    assert kb["all_rows"]["n"] == 30
    host = {r["event_id"]: r["hostility"] for r in o["rows"]}
    assert kb["hostile_only"]["n"] == sum(1 for h in host.values() if h == "hostile")
    assert kb["hostile_plus_ambiguous"]["n"] == sum(1 for h in host.values() if h in ("hostile", "ambiguous"))
    assert kb["hostile_only"]["n"] < kb["all_rows"]["n"]                    # the diagnostics are strict subsets
    assert all(r.get("hostility") for r in o["rows"])                       # every answered row records what it was


def test_joes_answered_row_survives_the_regeneration():
    """iran_iraq_war_1980 was answered before the sheet was regenerated with the hostility field."""
    import json
    o = json.loads((ROOT / "data" / "audits" / "outcome_audit.json").read_text())
    row = next((r for r in o["rows"] if r["event_id"] == "iran_iraq_war_1980"), None)
    assert row is not None, "Joe's answered row was lost in the regeneration"
    assert row["joe_level"] == 3 and row["engine_level"] == 3 and row["answered_at"].startswith("2026-09-03")
    assert row["hostility"] == "hostile"                                    # back-filled, his answer untouched
    assert o["auditor"] == "joe" and o["n_done"] == 1 and o["n_rows"] == 30
    assert o["sheet_hostility"] == {"non_hostile": 5, "ambiguous": 3, "hostile": 20, "hostile_unattributed": 2}
    ids = [r["event_id"] for r in __import__("csv").DictReader(open(ROOT / "data" / "audits" / "ies90_audit_30.csv", encoding="utf-8")) if r["row_type"] == "event"]
    assert "iran_iraq_war_1980" in ids and len(ids) == 30                   # still on the sheet he is working through
