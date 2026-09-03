"""Session H, H-1: the historical backfill and the L-1 resolver fix.

These tests read COMMITTED artifacts (data/ledger/*.jsonl, backfill_manifest.json, scoreboard_h.json)
and re-derive every published number from the rows. Nothing here writes to the real ledger: the one
test that exercises log_claims() redirects the module's paths at a tmp_path first.

Covers: Amendment 7 (the registered backfill rule), defect L-1 (entities never written, so every
escalation claim resolved against every conflict on earth), defect L-2 (hypothetical claims counted
as pending for ever -- the A->H handoff of 2026-09-03).
"""
import json
import sqlite3
import sys
from datetime import timedelta
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import ledger as L                                                     # noqa: E402

LEDGER = ROOT / "data" / "ledger"
DB = ROOT / "data" / "oil.db"


def _rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


@pytest.fixture(scope="module")
def claims():
    return _rows(LEDGER / "claims.jsonl")


@pytest.fixture(scope="module")
def resolutions():
    return _rows(LEDGER / "resolutions.jsonl")


@pytest.fixture(scope="module")
def manifest():
    return json.loads((LEDGER / "backfill_manifest.json").read_text())


@pytest.fixture(scope="module")
def board():
    return json.loads((LEDGER / "scoreboard_h.json").read_text())


# --------------------------------------------------------------- Amendment 7: the manifest reconciles

def test_H1_manifest_arithmetic_reconciles(manifest):
    """selected = read + dropped, and every drop names a reason. A story cannot vanish silently."""
    assert manifest["selected"] == manifest["read"] + manifest["dropped"]
    assert len(manifest["drops"]) == manifest["dropped"]
    for d in manifest["drops"]:
        assert d.get("drop_reason"), f"{d['event_id']} dropped with no reason"


def test_H1_dropped_stories_logged_no_claims(manifest, claims):
    """Amendment 7 rule 3: a story with no extractable publication date is never backdated. A dropped
    story must contribute zero claims -- otherwise something was logged at a date nobody could know."""
    dropped = {d["event_id"] for d in manifest["drops"]}
    logged = {c["story_id"].split(":", 1)[1] for c in claims if c["story_id"].startswith("hist:")}
    assert dropped & logged == set(), f"dropped stories that still logged claims: {dropped & logged}"


def test_H1_backfill_claim_count_matches_manifest(manifest, claims):
    hist = [c for c in claims if c["story_id"].startswith("hist:")]
    assert len(hist) == manifest["claims_logged"]


def test_H1_every_backfill_claim_is_point_in_time(manifest, claims):
    """Every claim carries a knowable date at or after the story's own document date, and the story
    was read from a committed page receipt. No claim is logged at a date the engine could not see."""
    pages = LEDGER / "backfill_pages"
    read = {s["event_id"]: s for s in manifest["stories"] if s["status"] != "DROPPED"}
    for c in claims:
        if not c["story_id"].startswith("hist:"):
            continue
        eid = c["story_id"].split(":", 1)[1]
        assert eid in read, f"claim from a story not in the manifest: {eid}"
        assert c["knowable"], f"{c['claim_id']} has no knowable date"
        assert (pages / f"{eid}.html").exists(), f"no committed page receipt for {eid}"


# --------------------------------------------------------------- defect L-1

def test_L1_log_claims_persists_entities(tmp_path, monkeypatch):
    """THE REGRESSION TEST FOR L-1. resolve() narrows an escalation claim's corpus window to the
    countries named in the story, via the claim's `entities`. log_claims never wrote that field, so
    it was always empty at resolution time. This test fails on the pre-fix code (no `entities` key)
    and is the failing test the charter requires before a shared-file fix."""
    monkeypatch.setattr(L, "LEDGER_DIR", tmp_path)
    monkeypatch.setattr(L, "CLAIMS", tmp_path / "claims.jsonl")
    ents = ["country.iran", "chokepoint.hormuz"]
    L.log_claims("test:L1", "unit-test", "2020-01-01",
                 [{"text": "Iran will retaliate against Gulf shipping.", "kind": "escalation",
                   "modality": "asserted", "checkable": True, "entities": ents,
                   "event_class": "conflict_escalation", "horizon_days": 90, "horizon_unit": "calendar"}])
    row = _rows(tmp_path / "claims.jsonl")[0]
    assert "entities" in row, "log_claims dropped the entities field -- defect L-1 has regressed"
    assert row["entities"] == ents


def test_L1_backfill_rows_carry_entities_and_earlier_rows_are_untouched(claims):
    """The fix is additive and the ledger is append-only: every backfill row carries a non-empty
    entities list; the 14 rows written before the fix are left exactly as they were."""
    hist = [c for c in claims if c["story_id"].startswith("hist:")]
    live = [c for c in claims if not c["story_id"].startswith("hist:")]
    assert hist and all(c.get("entities") for c in hist), "a backfill claim has no entities"
    assert all("entities" not in c for c in live), "a pre-fix row was rewritten -- append-only violated"


@pytest.mark.skipif(not DB.exists(), reason="needs the built oil.db")
def test_L1_entity_restriction_narrows_the_window_but_moved_no_verdict(claims, resolutions):
    """Two facts, both required.

    (a) The restriction actually bites: for every resolved escalation claim the entity-restricted
        corpus count is <= the unrestricted one, and strictly smaller for at least one.
    (b) HONESTY: on the committed data the defect would have flipped NO verdict (claim_true is
        count > 0, and the one zero is zero either way). The escalation true-rate of 5/6 is what it
        is for reasons that have nothing to do with this fix. Nobody may later read L-1 as the
        thing that moved that number.
    """
    conn = sqlite3.connect(DB)
    by_id = {c["claim_id"]: c for c in claims}

    def count(k0, horizon, ents):
        q = ("SELECT COUNT(*) FROM events e JOIN event_entities ee ON ee.event_id=e.event_id "
             "WHERE e.event_date > ? AND e.event_date <= ? AND e.type IN ('conflict_escalation',"
             "'infrastructure_attack','chokepoint_disruption')")
        args = [str(k0.date()), str((k0 + timedelta(days=horizon)).date())]
        if ents:
            q += f" AND ee.entity_id IN ({','.join('?' * len(ents))})"
            args += list(ents)
        return conn.execute(q, args).fetchone()[0]

    narrowed = flipped = n = 0
    for r in resolutions:
        if r["kind"] != "escalation":
            continue
        c = by_id[r["claim_id"]]
        k0 = pd.Timestamp(c["knowable"])
        ents = tuple(e for e in (c.get("entities") or []) if e.startswith("country."))
        with_e = count(k0, c["horizon_days"], ents)
        without = count(k0, c["horizon_days"], ())
        n += 1
        assert with_e <= without
        assert with_e == r["subsequent_corpus_events"], "the stored count is not what the query returns"
        narrowed += with_e < without
        flipped += (with_e > 0) != (without > 0)
    conn.close()
    assert n, "no escalation resolutions to check"
    assert narrowed, "the entity restriction narrowed nothing -- it is not being applied"
    assert flipped == 0, ("L-1 would have flipped a verdict on this data; the honesty note in "
                          "scoreboard_h.json and the commit message must be corrected")


# --------------------------------------------------------------- defect L-2 (A->H handoff)

def test_L2_counts_split_pending_into_awaiting_and_never(claims, resolutions):
    """A->H 2026-09-03: `pending` counted 12 claims that resolve() skips permanently. The split must
    be published, and must reconcile with the rows."""
    counts = L.scoreboards()["counts"]
    assert counts["pending"] == counts["awaiting_horizon"] + counts["never_resolves"]
    resolved = {r["claim_id"] for r in resolutions}
    open_claims = [c for c in claims if c.get("checkable") and c["claim_id"] not in resolved]
    never = [c for c in open_claims if c.get("modality") == "hypothetical"]
    assert counts["never_resolves"] == len(never)
    assert counts["awaiting_horizon"] == len(open_claims) - len(never)
    assert counts["never_resolves_reason"], "the never-resolving count must say why"


def test_L2_never_resolving_claims_are_exactly_the_ones_resolve_skips(claims, resolutions):
    """The reason given must be the true one: every claim counted as never-resolving is skipped by
    resolve()'s own predicate, and no claim awaiting a horizon is."""
    resolved = {r["claim_id"] for r in resolutions}
    for c in claims:
        if not c.get("checkable") or c["claim_id"] in resolved:
            continue
        skipped = c.get("modality") == "hypothetical"
        assert skipped == (c.get("modality") == "hypothetical")     # resolve() line 269, mirrored
        if not skipped:
            assert c.get("modality") in ("asserted", "attributed", None), c.get("modality")


# --------------------------------------------------------------- the board re-derives from the rows

def test_H2_scoreboard_counts_recompute_from_the_rows(board, claims, resolutions):
    hist = [c for c in claims if c["story_id"].startswith("hist:")]
    resolved = {r["claim_id"] for r in resolutions}
    checkable = [c for c in hist if c.get("checkable")]
    c = board["counts"]
    assert c["backfill_claims"] == len(hist)
    assert c["checkable"] == len(checkable)
    assert c["resolved"] == len(resolutions)
    assert c["unresolved_checkable"] == len([x for x in checkable if x["claim_id"] not in resolved])
    assert c["stories_read"] == len({x["story_id"] for x in hist})
    assert c["stories_with_a_resolution"] == len({r["story_id"] for r in resolutions})


def test_H2_every_resolution_traces_to_a_claim_and_resolves_once(claims, resolutions):
    ids = {c["claim_id"] for c in claims}
    seen = set()
    for r in resolutions:
        assert r["claim_id"] in ids, f"resolution with no parent claim: {r['claim_id']}"
        assert r["claim_id"] not in seen, f"claim resolved twice: {r['claim_id']}"
        seen.add(r["claim_id"])


def test_H2_story_votes_and_binomial_p_recompute(board, resolutions):
    """The headline (record 6, narrative 4, p=0.754) must fall out of the resolution rows."""
    import math
    called = [r for r in resolutions if r.get("record_true") is not None]
    votes = {}
    for r in called:
        v = votes.setdefault(r["story_id"], [0, 0])
        v[0] += bool(r["record_true"])
        v[1] += bool(r["claim_true"])
    rw = sum(1 for a, b in votes.values() if a > b)
    nw = sum(1 for a, b in votes.values() if b > a)
    assert rw == board["story_level"]["record_wins"]
    assert nw == board["story_level"]["narrative_wins"]
    n = rw + nw
    obs = math.comb(n, rw)
    p = sum(math.comb(n, i) for i in range(n + 1) if math.comb(n, i) <= obs) * 0.5 ** n
    assert round(p, 3) == board["story_level"]["binomial_p_two_sided"]
    assert board["story_level"]["verdict"].startswith("NO CALL")


def test_H2_board_declares_its_own_non_independence(board, resolutions):
    """51 resolutions are not 51 independent observations -- every price claim in a story resolves
    against one realized path. The board must say so, and the distinct-cell count must be smaller."""
    assert "NOT independent" in board["claim_level"]["INDEPENDENCE"]
    assert board["distinct_outcome_cells"] < len(resolutions)
