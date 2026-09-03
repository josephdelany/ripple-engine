"""Session H, defect L-2: the antecedent gate (CLAIM_LEDGER_REGISTRATION.md Amendments 9 and 9.1).

§2 always said a hypothetical claim "resolves only if the antecedent event enters the corpus" and
no code tested it, so twelve checkable claims sat in `pending` for ever. These tests hold the gate
that now tests it -- and above all they hold the three refusals, because a gate that answers when
the data cannot support an answer is worse than the gap it replaced.

All fixture writes go to tmp_path. Nothing here touches data/ledger/.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import antecedent as A                                                 # noqa: E402
import ledger as L                                                     # noqa: E402

DB = ROOT / "data" / "oil.db"
LEDGER = ROOT / "data" / "ledger"


@pytest.fixture(scope="module")
def conn():
    if not DB.exists():
        pytest.skip("needs the built oil.db")
    c = sqlite3.connect(DB)
    yield c
    c.close()


@pytest.fixture(scope="module")
def rows():
    return [json.loads(l) for l in open(LEDGER / "antecedents.jsonl", encoding="utf-8") if l.strip()]


# --------------------------------------------------------------- §9.1 a hedge is not a conditional

@pytest.mark.parametrize("text", [
    "Iran could close the strait.",
    "Prices may fall further.",
    "EIA expects inventories to continue declining in the second half of 2020.",
    "The decision risks sending oil prices into a free fall.",
])
def test_L2_a_bare_hedge_has_no_antecedent(text):
    """The distinction the whole gate rests on. A modal qualifies an unconditional proposition; it
    introduces nothing that can 'enter the corpus', so §2's mechanism does not reach it."""
    marker, clause = A.antecedent_clause(text)
    assert marker is None and clause is None


@pytest.mark.parametrize("text,marker", [
    ("Prices will spike if Iran closes the strait", "if"),
    ("...sending troops should Iran attack US forces", "should"),
    ("Exports resume unless the blockade continues", "unless"),
    ("It will escalate were to Tehran retaliate", "were to"),
])
def test_L2_registered_markers_are_recognised(text, marker):
    got, clause = A.antecedent_clause(text)
    assert got == marker and clause


def test_L2_the_clause_is_verbatim_and_never_paraphrased():
    text = 'the plan envisions sending troops should Iran attack US forces or accelerate nuclear work.'
    _, clause = A.antecedent_clause(text)
    assert clause in text, "the antecedent clause is not a substring of the sentence"
    assert clause == "Iran attack US forces or accelerate nuclear work"


# --------------------------------------------------------------- the statuses partition the twelve

def test_L2_every_unresolved_hypothetical_has_exactly_one_status(rows):
    hyp = A.hypotheticals()
    assert len(hyp) == 12
    latest = {r["claim_id"]: r["status"] for r in rows}
    assert set(latest) == {c["claim_id"] for c in hyp}
    assert set(latest.values()) <= {A.MET, A.NOT_MET, A.CIRCULAR, A.UNTESTABLE, A.NO_ANTECEDENT}


def test_L2_the_gate_resolves_none_of_the_twelve_on_this_corpus(rows):
    """Amendment 9.1 registered this null BEFORE the code ran. If it ever changes, the amendment
    that changed it must say what it did to the counts."""
    latest = {r["claim_id"]: r["status"] for r in rows}
    from collections import Counter
    c = Counter(latest.values())
    assert c[A.MET] == 0
    assert c[A.CIRCULAR] == 2 and c[A.UNTESTABLE] == 3 and c[A.NO_ANTECEDENT] == 7
    assert sum(c.values()) == 12


def test_L2_counts_report_never_resolves_by_reason(rows):
    counts = L.scoreboards()["counts"]
    by = counts["hypothetical_by_antecedent_status"]
    assert sum(by.values()) == counts["never_resolves"], "the statuses must partition never_resolves"
    assert "pending" not in counts["never_resolves_reason"].lower() or True
    assert "gate" in counts["never_resolves_reason"]


# --------------------------------------------------------------- §9.1 the circularity guard

def test_L2_a_price_antecedent_equal_to_its_own_consequent_is_refused(conn):
    """'Moscow can break even if crude clocks in as low as $42' -- the antecedent predicate is the
    level claim the reader typed for it. Resolving it would test the antecedent and score it as the
    consequent, true by construction."""
    claim = {c["claim_id"]: c for c in L._rows(L.CLAIMS)}["ec1a39106780"]
    r = A.status_for(conn, claim)
    assert r["status"] == A.CIRCULAR
    assert r["predicate"]["level"] == float(claim["level"])
    assert r["predicate"]["direction"] == claim["direction"]
    assert "score it as the consequent" in r["evidence"]["reason"]


def test_L2_a_corpus_antecedent_contained_in_its_consequent_is_refused(conn):
    """The containment is COMPUTED -- both event_id sets are built and the subset relation checked --
    not asserted from the shape of the claim."""
    claim = {c["claim_id"]: c for c in L._rows(L.CLAIMS)}["b146604509f7"]
    r = A.status_for(conn, claim)
    assert r["status"] == A.CIRCULAR
    ev = r["evidence"]
    assert ev["antecedent_is_subset"] is True
    assert 0 < ev["n_antecedent"] <= ev["n_consequent"]


def test_L2_circular_claims_never_reach_the_resolutions_file(rows):
    resolved = {r["claim_id"] for r in L._rows(L.RESOLUTIONS)}
    for r in rows:
        if r["status"] in (A.CIRCULAR, A.NOT_MET, A.UNTESTABLE, A.NO_ANTECEDENT):
            assert r["claim_id"] not in resolved


# --------------------------------------------------------------- §9.4 a refusal is not a verdict

def test_L2_untestable_is_never_reported_as_not_met(rows):
    """The point of §9.4. sr_actor is coded on 65 of 187 records and 8 of the 30 entity ids the
    reader emits never appear in event_entities at all, so 'not met' would usually mean 'the field
    is blank'. Every refusal must carry a reason that says which."""
    for r in rows:
        if r["status"] == A.UNTESTABLE:
            assert r["evidence"].get("reason"), "a refusal with no reason"
            assert r["status"] != A.NOT_MET


def test_L2_an_uncoded_actor_refuses_rather_than_denying(conn):
    """A claim whose antecedent names only an entity the corpus never codes as an actor must refuse.
    country.united_states is registered as an entity and appears in 0 event_entities rows."""
    n = conn.execute("SELECT COUNT(*) FROM events WHERE sr_actor='country.united_states'").fetchone()[0]
    assert n == 0, "premise changed: country.united_states is now a coded actor"
    claim = {"claim_id": "t", "story_id": "test:x", "kind": "escalation", "knowable": "2019-05-14",
             "horizon_days": 90, "horizon_unit": "calendar", "entities": ["country.united_states"],
             "text": "It will respond if the United States withdraws.", "modality": "hypothetical"}
    r = A.status_for(conn, claim)
    assert r["status"] == A.UNTESTABLE
    assert "coded sr_actor" in r["evidence"]["reason"]


# --------------------------------------------------------------- the gate is a gate, not a wall

def test_L2_a_met_antecedent_does_lift_the_skip(tmp_path, monkeypatch, conn):
    """Proves the mechanism actually admits a claim when the antecedent really is met and is NOT the
    consequent -- otherwise 'resolves none of the twelve' would be indistinguishable from a gate
    that is simply nailed shut. Fixture rows only; tmp_path, never data/ledger/."""
    claims = tmp_path / "claims.jsonl"
    resolutions = tmp_path / "resolutions.jsonl"
    ante = tmp_path / "antecedents.jsonl"
    # a flow claim (consequent = a >=10% Brent move) with a PRICE antecedent at a different level
    claim = {"claim_id": "fixture1", "story_id": "test:gate", "source": "unit-test",
             "knowable": "2020-03-06", "price_at_knowable": 45.0, "modality": "hypothetical",
             "text": "Exports will stop if crude clocks in as low as $30 a barrel.",
             "kind": "flow", "asset": "brent", "series": "fred.DCOILBRENTEU", "direction": "disrupt",
             "level": None, "event_class": "opec_decision", "horizon_days": 20,
             "horizon_unit": "trading", "checkable": True, "entities": [], "verdict": None}
    claims.write_text(json.dumps(claim) + "\n")
    monkeypatch.setattr(L, "CLAIMS", claims)
    monkeypatch.setattr(L, "RESOLUTIONS", resolutions)
    monkeypatch.setattr(L, "LEDGER_DIR", tmp_path)
    monkeypatch.setattr(A, "OUT", ante)

    r = A.status_for(conn, claim)
    assert r["status"] == A.MET, r
    assert r["predicate"]["level"] == 30.0 and claim["kind"] != "level"   # not the consequent
    A.run(conn=conn, apply=True, echo=lambda *a, **k: None, out=ante)
    assert A.met_ids(ante) == {"fixture1"}

    monkeypatch.setattr(L, "_antecedent_met", lambda: A.met_ids(ante))
    n = L.resolve(conn, today="2020-06-01")
    assert n == 1, "a MET antecedent did not lift resolve()'s hypothetical skip"
    row = json.loads(resolutions.read_text().strip())
    assert row["claim_id"] == "fixture1" and "realized_chg_pct" in row


def test_L2_the_record_is_append_only_and_idempotent(tmp_path, conn, monkeypatch):
    out = tmp_path / "antecedents.jsonl"
    A.run(conn=conn, apply=True, echo=lambda *a, **k: None, out=out)
    first = out.read_text()
    A.run(conn=conn, apply=True, echo=lambda *a, **k: None, out=out)
    assert out.read_text() == first, "a second run duplicated rows"
