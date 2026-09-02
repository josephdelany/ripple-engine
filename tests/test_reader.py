"""test_reader.py -- the caged reader (CLAIM_LEDGER_REGISTRATION.md Amendment 3) on three saved articles.

The model's outputs were recorded ONCE (2026-09-02) into tests/fixtures/reader/*.proposal.json; these
tests replay them through the cage, so the suite never calls the claude CLI (conftest sets
RIPPLE_READER=off). The no-fabrication tests mirror test_situation.py's s3b/s3c: a quote not in the
text, a level not in the quote, an out-of-vocab class or entity -- rejected, nothing repaired.
"""
import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import reader as R              # noqa: E402
import materiality as M         # noqa: E402

FX = ROOT / "tests" / "fixtures" / "reader"
URLS = {"gcaptain_tankers": "https://gcaptain.com/oil-tankers-make-fortunes-during-war-as-sinokor-dominates/",
        "opec_2025_04_03": "https://www.opec.org/pr-detail/557-03-april-2025.html",
        "freightwaves_offtopic": "https://www.freightwaves.com/news/700-pounds-of-meth-hidden-in-cucumber-load-leads-to-15-year-prison-sentences"}
# the same summary shape test_v2_gate_ledger uses: opec_decision MATERIAL, sanctions NOISE
SUMMARY = {
    "brent": {"label": "Brent", "everyday_base_rate_pct": 20.0,
              "p_big_given_class": {"opec_decision": [10, 40], "sanctions": [4, 40], "chokepoint_disruption": [12, 40]}},
    "diesel_crack": {"label": "Diesel crack", "everyday_base_rate_pct": 20.0,
                     "p_big_given_class": {"opec_decision": [8, 40], "sanctions": [4, 40], "chokepoint_disruption": [12, 40]}},
}


def _page(name):
    raw = (FX / f"{name}.html").read_text(encoding="utf-8")
    body = R.body_from_html(raw)
    return raw, body, R.title_from_html(raw, URLS[name], body)


def _proposal(name):
    return json.loads((FX / f"{name}.proposal.json").read_text())


def _read(name):
    """Replay the recorded proposal through read_story (text path) -- no CLI, no cache."""
    _raw, body, _title = _page(name)
    return R.read_story(body, proposal=_proposal(name))


@pytest.fixture(autouse=True)
def _no_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "CACHE", tmp_path / "cache")


# ---------------------------------------------------------------- titles are the page's own (rule 4)

def test_rd1_titles_are_extracted_from_the_page_not_generated():
    assert _page("gcaptain_tankers")[2] == "Oil Tankers Make Fortunes During War as Sinokor Dominates"
    # opec.org: og:title is 'Press Releases' and <title> is the site name -- the real headline sits in <article>
    assert _page("opec_2025_04_03")[2].startswith("Saudi Arabia, Russia, Iraq, UAE, Kuwait, Kazakhstan, Algeria, and Oman reaffirm")
    # the ' - FreightWaves' site suffix is removed
    assert _page("freightwaves_offtopic")[2] == "700 pounds of meth hidden in cucumber load leads to 15-year prison sentences"


def test_rd1b_pasted_text_title_is_its_first_sentence():
    p = R.prepare("Iran seized a tanker near Hormuz on Tuesday. Brent rose after the news.")
    assert p["title"] == "Iran seized a tanker near Hormuz on Tuesday." and p["url"] is None


# ---------------------------------------------------------------- the three saved articles

def test_rd2_gcaptain_tanker_piece_reads_as_a_chokepoint_story_with_roles():
    r = _read("gcaptain_tankers")
    assert r["event_class"] == "chokepoint_disruption" and r["reader"]["mode"] == "recorded"
    roles = {e["id"]: e["role"] for e in r["entities"]}
    assert roles.get("country.iran") == "actor" and roles.get("chokepoint.hormuz") == "chokepoint"
    assert "country.iran" in r["qualifying_entities"] and "chokepoint.hormuz" in r["qualifying_entities"]
    assert "Sinokor Group" in r["unmapped"]                      # a central name outside the vocab stays as text, no id
    body = _page("gcaptain_tankers")[1]
    for c in r["claims"]:
        assert R._canon(c["text"]) in R._canon(body)             # every claim verbatim
    kinds = {c["kind"] for c in r["claims"]}
    assert "flow" in kinds and "escalation" in kinds
    esc = [c for c in r["claims"] if c["kind"] == "escalation"][0]
    assert esc["checkable"] and esc["horizon_days"] == 90 and esc["horizon_unit"] == "calendar"
    for c in r["claims"]:
        if c["asset"] == "freight":
            assert not c["checkable"]                             # freight has no series yet: never checkable
            assert "no series" in c["why"] or "fabrication guard" in c["why"]   # ('$20 million' is not the number 20000000)
        if c["kind"] == "flow":
            # registered default +20 trading days, unless the quote itself states a number of days (rule 3)
            assert c["checkable"] and (c["horizon_days"] == 20 or str(c["horizon_days"]) in R._numbers(c["text"]))


def test_rd3_opec_press_release_reads_as_an_opec_decision_with_policy_claims():
    r = _read("opec_2025_04_03")
    assert r["event_class"] == "opec_decision"
    roles = {e["id"]: e["role"] for e in r["entities"]}
    assert roles.get("country.saudi_arabia") == "actor" and roles.get("country.russia") == "actor"
    assert r["qualifying_entities"]
    assert r["claims"] and all(c["kind"] == "policy" and not c["checkable"] for c in r["claims"])
    assert all("PENDING" in c["why"] for c in r["claims"])
    assert "Algeria" in r["unmapped"]                             # not in the entities table: kept as text only


def test_rd4_off_topic_story_gets_no_class_no_entities_no_claims():
    r = _read("freightwaves_offtopic")
    assert r["event_class"] is None and r["entities"] == [] and r["claims"] == [] and r["qualifying_entities"] == []
    assert M.gate(r["event_class"])["significance"] == "NOISE"


# ---------------------------------------------------------------- the cage: no fabrication (rules 1-3)

TEXT = ("Iran seized a tanker near the Strait of Hormuz on Tuesday. Analysts said Brent could climb past $95 a barrel "
        "within two weeks. Exports from Kharg Island were halted.")


def _voc():
    return R.vocab()


def test_rd5_quote_not_in_text_is_rejected_as_fabrication():
    p = {"event_class": "chokepoint_disruption", "entities": [{"id": "country.iran", "role": "actor"}], "unmapped": [],
         "claims": [{"quote": "Brent will surge to $150 immediately.", "kind": "level", "asset": "brent", "direction": "up",
                     "level": 150, "horizon_days": None, "modality": "asserted"}]}
    r = R.cage(p, TEXT, _voc())
    assert r["claims"] == []
    assert any(x["what"] == "claim" and "fabrication" in x["reason"] for x in r["rejected"])


def test_rd6_level_not_stated_in_the_quote_is_dropped_and_claim_downgraded():
    p = {"event_class": "chokepoint_disruption", "entities": [], "unmapped": [],
         "claims": [{"quote": "Analysts said Brent could climb past $95 a barrel within two weeks.", "kind": "level", "asset": "brent",
                     "direction": "up", "level": 110, "horizon_days": None, "modality": "hypothetical"}]}
    c = R.cage(p, TEXT, _voc())["claims"][0]
    assert c["level"] is None and c["kind"] == "uncheckable" and not c["checkable"] and "fabrication" in c["why"]
    # the same quote with the level it actually states is a checkable level claim at the registered horizon
    p["claims"][0]["level"] = 95
    c = R.cage(p, TEXT, _voc())["claims"][0]
    assert c["kind"] == "level" and c["level"] == 95 and c["checkable"] and c["horizon_days"] == 20 and c["modality"] == "hypothetical"


def test_rd7_horizon_is_assigned_by_the_cage_unless_the_quote_states_it():
    q = "Analysts said Brent could climb past $95 a barrel within two weeks."
    base = {"quote": q, "kind": "direction", "asset": "brent", "direction": "up", "level": None, "modality": "asserted"}
    c, _ = R.cage_claim({**base, "horizon_days": 45}, TEXT, has_actor=True)      # 45 is not in the quote
    assert c["horizon_days"] == 20
    c, _ = R.cage_claim({**base, "quote": "Exports from Kharg Island were halted.", "kind": "flow", "horizon_days": None}, TEXT, True)
    assert c["kind"] == "flow" and c["direction"] == "disrupt" and c["horizon_days"] == 20 and c["asset"] == "brent"


def test_rd8_out_of_vocab_class_entity_and_role_are_rejected_not_repaired():
    p = {"event_class": "alien_invasion",
         "entities": [{"id": "country.atlantis", "role": "actor"}, {"id": "country.iran", "role": "villain"},
                      {"id": "country.iran", "role": "actor"}],
         "unmapped": [], "claims": []}
    r = R.cage(p, TEXT, _voc())
    assert r["event_class"] is None and r["model_class"] == "alien_invasion"
    assert [e["id"] for e in r["entities"]] == ["country.iran"]
    reasons = {x["what"] for x in r["rejected"]}
    assert {"event_class", "entity", "entity_role"} <= reasons


def test_rd9_escalation_without_an_actor_and_negated_claims_are_uncheckable():
    q = "Iran seized a tanker near the Strait of Hormuz on Tuesday."
    c, _ = R.cage_claim({"quote": q, "kind": "escalation", "asset": None, "direction": "escalate", "level": None,
                         "horizon_days": None, "modality": "asserted"}, TEXT, has_actor=False)
    assert c["kind"] == "uncheckable" and not c["checkable"] and "no actor" in c["why"]
    c, _ = R.cage_claim({"quote": q, "kind": "escalation", "asset": None, "direction": "escalate", "level": None,
                         "horizon_days": None, "modality": "negated"}, TEXT, has_actor=True)
    assert c["kind"] == "uncheckable" and "negated" in c["why"]


# ---------------------------------------------------------------- the entity-aware gate (rule 5)

def test_rd10_material_needs_a_tracked_petro_entity_in_a_gate_role():
    ent = lambda i, r: {"id": i, "name": i, "type": i.split(".")[0], "role": r}     # noqa: E731
    assert R.qualifying_entities([ent("country.usa", "mention")]) == []              # keyword presence is not enough
    assert R.qualifying_entities([ent("country.usa", "actor")]) == ["country.usa"]
    assert R.qualifying_entities([ent("commodity.gold", "asset")]) == []              # tracked, but not petro
    assert R.qualifying_entities([ent("commodity.brent", "asset")]) == ["commodity.brent"]
    assert R.qualifying_entities([ent("chokepoint.hormuz", "location")]) == []        # location-only does not qualify
    assert R.qualifying_entities([ent("institution.imf", "actor")]) == []
    assert R.qualifying_entities([ent("institution.opec", "actor")]) == ["institution.opec"]
    # under the labelled regex fallback roles are unknown: presence counts (Amendment 2), still labelled
    assert R.qualifying_entities([ent("country.usa", "mention")], mode="regex_fallback") == ["country.usa"]


def test_rd11_feed_shows_material_only_with_a_qualifying_entity(tmp_path, monkeypatch):
    import feed_build as FB
    rec = json.loads((FX / "headlines.proposal.json").read_text())
    heads = rec["headlines"]
    by_head = {}
    for h, it in zip(heads, rec["items"]):
        by_head[h] = {"event_class": it["event_class"], "entities": it["entities"], "unmapped": [],
                      "claims": [it["claim"]] if it.get("claim") else []}
    # a fourth headline: MATERIAL class but the only entity is a mention -> shown IN LINE, flagged no_entity
    weak = "OPEC ministers gather in Vienna as delegates arrive for talks"
    by_head[weak] = {"event_class": "opec_decision", "entities": [{"id": "institution.opec", "role": "mention"}], "unmapped": [], "claims": []}
    heads = heads + [weak]
    real = R.read_headlines
    monkeypatch.setattr(R, "read_headlines", lambda hs, **kw: real(hs, proposals=[by_head[h] for h in hs], **kw))
    monkeypatch.setattr(M, "load_summary", lambda path=None: SUMMARY)
    monkeypatch.setattr(FB, "DATA", tmp_path)
    with open(tmp_path / "alert_queue.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp_utc", "source", "headline", "url", "matched_entities", "matched_keywords", "heuristic_type", "amp_context", "status"])
        w.writeheader()
        for i, h in enumerate(heads):
            w.writerow({"timestamp_utc": f"2026-09-02T0{i}:00:00+00:00", "source": "test", "headline": h, "url": f"http://x/{i}", "status": "new"})
    import sqlite3
    conn = sqlite3.connect(R.DB)
    try:
        fd = FB.build_feed(conn)
    finally:
        conn.close()
    mat = {i["headline"]: i for i in fd["material"]}
    inl = {i["headline"]: i for i in fd["in_line"]}
    noise = {i["headline"]: i for i in fd["noise"]}
    opec_head = [h for h in heads if "reaffirm" in h][0]
    assert opec_head in mat and mat[opec_head]["event_class"] == "opec_decision" and "institution.opec" in mat[opec_head]["qualifying_entities"]
    assert weak in inl and "no_entity" in inl[weak]["gate_flags"]
    assert all(h in noise for h in heads if "meth" in h or "Fortunes" in h)          # no class -> NOISE shelf, visible
    assert fd["counts"]["reader"] == {"recorded": 4} and "Amendments 1-3" in fd["gate"]


# ---------------------------------------------------------------- the fallback is labelled (rule 6)

def test_rd12_without_the_cli_the_read_is_a_labelled_regex_fallback(monkeypatch):
    monkeypatch.setenv("RIPPLE_READER", "off")
    r = R.read_story("Iran seized a tanker in the Strait of Hormuz; Brent could climb past $95 a barrel.")
    assert r["reader"]["mode"] == "regex_fallback" and r["reader"]["error"]
    assert r["event_class"] == "chokepoint_disruption"
    assert all(e["role"] == "mention" for e in r["entities"])
    assert any(c["kind"] == "level" and c["level"] == 95 for c in r["claims"])


def test_rd13_story_page_carries_the_reader_and_the_entity_rule(monkeypatch):
    import story_read as SR
    import ledger as L
    _raw, body, _t = _page("gcaptain_tankers")
    monkeypatch.setattr(R, "read_story", lambda arg, **kw: _orig(arg, proposal=_proposal("gcaptain_tankers"), **kw))
    s = SR.read(arg=body, log=False)
    assert s["reader"]["mode"] == "recorded" and s["event_class"] == "chokepoint_disruption"
    assert s["qualifying_entities"] and s["roles"] and s["unmapped"]
    assert s["title"].startswith("A ship off the port of Aden")       # pasted text: first sentence, not generated
    for c in s["claims"]:
        assert c["verdict"]["verdict"] in ("SUPPORTED", "MIXED", "UNSUPPORTED", "THIN", "NO PRECEDENT", "UNCHECKABLE")
        assert R._canon(c["text"]) in R._canon(body)


_orig = R.read_story
