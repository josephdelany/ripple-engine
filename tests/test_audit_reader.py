"""Session H, H-3: the reader audit recorder, the blind sheet and inter-coder kappa.

The reader scores 84% against a gold set that session A coded and nobody audited. These tests hold
the two things that stop that number being quoted as if it were established: the blind sheet must
carry no answers, and the published label must keep saying UNAUDITED until Joe himself has coded a
sample. They also re-derive the A-vs-H kappa from the committed codings.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import audit_reader as AU                                              # noqa: E402

EVAL = ROOT / "data" / "reader_eval"


def _rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


@pytest.fixture(scope="module")
def gold():
    return AU.load_gold()


@pytest.fixture(scope="module")
def sheet():
    return json.loads((EVAL / "blind_sheet_30.json").read_text())


@pytest.fixture(scope="module")
def kappa():
    return json.loads((EVAL / "kappa_coders.json").read_text())


# --------------------------------------------------------------- REQ-H3-SAMPLE: the draw is registered

def test_H3_sample_is_reproducible_from_the_registered_seed(gold, sheet):
    """The 30 are a deterministic function of the seed and the gold's own ids, so the sheet cannot be
    re-drawn to a friendlier subset after the answers are known."""
    assert sheet["seed"] == AU.SEED
    assert sorted(r["id"] for r in sheet["rows"]) == AU.sample_ids(gold)
    assert len(sheet["rows"]) == AU.N_SAMPLE


def test_H3_sample_is_a_subset_of_the_gold(gold, sheet):
    ids = {str(g["id"]) for g in gold}
    assert {r["id"] for r in sheet["rows"]} <= ids


# --------------------------------------------------------------- the sheet is actually blind

def test_H3_blind_sheet_carries_no_answers(sheet):
    """A sheet that leaks the label is not a blind coding. Rows carry id, headline and source only."""
    for r in sheet["rows"]:
        assert set(r) <= {"id", "headline", "source_url"}, f"blind sheet row leaks {set(r)}"


def test_H3_blind_sheet_markdown_names_no_per_row_class(sheet):
    """No row may carry a class FIELD. Each line is exactly `- **id** — headline` and nothing else,
    so the writer cannot have appended a label without this failing."""
    md = (EVAL / "blind_sheet_30.md").read_text()
    body = [l for l in md.splitlines() if l.startswith("- **")]
    assert len(body) == len(sheet["rows"])
    expected = {f"- **{r['id']}** \u2014 {r['headline']}" for r in sheet["rows"]}
    assert set(body) == expected, "a sheet row carries something beyond its id and headline"


def test_H3_KNOWN_WEAKNESS_id_slugs_telegraph_some_classes_and_it_is_published(gold, kappa):
    """The sheet is only PARTLY blind, and the file must say so with a number.

    Nine of the thirty ids printed on the sheet contain a token of their own gold class
    ("russia_sectoral_sanctions_2014", every "opec_*"). A coder can score those without reading the
    headline, so the headline kappa is inflated by construction. This is NOT asserted away: the test
    pins the count, requires the honest lower bound to be published, and requires it to be lower than
    the headline number. If someone re-draws the sheet or renames the ids, this test tells them what
    it did to the kappa.
    """
    cav = kappa["blindness_caveat"]
    assert cav["n_telegraphed"] == 9 and cav["n_total"] == 30
    sub = cav["subset_kappa_excluding_telegraphed"]["A_vs_H"]
    assert sub["n"] == 30 - 9
    assert sub["kappa"] < kappa["pairs"]["A_vs_H"]["kappa"], (
        "excluding the telegraphed rows did not lower the kappa -- recheck the caveat")
    assert sub["kappa"] >= AU.THRESHOLD, (
        f"the honest lower bound {sub['kappa']} is below the {AU.THRESHOLD} bar; the reader label "
        "must not be quoted from the inflated number")


def test_H3_blind_sheet_writer_never_emits_a_label(tmp_path, monkeypatch):
    """Regenerate the sheet into a tmp dir and check the writer itself, not just its committed output."""
    monkeypatch.setattr(AU, "ROOT", tmp_path)
    monkeypatch.setattr(AU, "SHEET_JSON", tmp_path / "sheet.json")
    monkeypatch.setattr(AU, "SHEET_MD", tmp_path / "sheet.md")
    rows = AU.blind_sheet(echo=lambda *a, **k: None)
    for r in rows:
        assert set(r) <= {"id", "headline", "source_url"}
    written = json.loads((tmp_path / "sheet.json").read_text())
    assert all(set(r) <= {"id", "headline", "source_url"} for r in written["rows"])


# --------------------------------------------------------------- kappa re-derives, and is labelled a diagnostic

def test_H3_A_vs_H_kappa_recomputes_from_the_committed_codings(gold, kappa):
    g = {str(x["id"]): (x["gold_class"] or "none") for x in gold}
    h = {str(r["id"]): (r["class"] or "none") for r in _rows(EVAL / "coding_H.jsonl")}
    ids = [i for i in AU.sample_ids(gold) if i in h]
    a = [g[i] for i in ids]
    b = [h[i] for i in ids]
    k, n, _ = AU._kappa(a, b)
    pub = kappa["pairs"]["A_vs_H"]
    assert n == pub["n"] == len(ids)
    assert round(k, 4) == round(pub["kappa"], 4)
    agree = sum(1 for x, y in zip(a, b) if x == y)
    assert round(agree / len(ids), 4) == round(pub["raw_agreement"], 4)


def test_H3_kappa_report_is_labelled_a_legibility_check_not_an_audit(kappa):
    """Both coders are Claude. The file must say so, in terms, or the number will be read as an audit."""
    w = kappa["WARNING"]
    assert "both are Claude" in w or "are both Claude" in w
    assert "cannot retire" in w


def test_H3_coding_H_covers_the_sample_exactly(gold):
    h = _rows(EVAL / "coding_H.jsonl")
    assert {str(r["id"]) for r in h} == set(AU.sample_ids(gold))
    assert all(r["class"] in AU.CLASSES for r in h), "a coding used a class outside the registered menu"
    assert all(r.get("blind") for r in h), "a coding is not marked blind"


# --------------------------------------------------------------- the label cannot be quoted bare

def test_H3_status_says_unaudited_until_joe_has_coded(monkeypatch, tmp_path):
    """With no answers from Joe, status() must not pass and its label must say UNAUDITED."""
    monkeypatch.setattr(AU, "OUT", tmp_path / "absent.json")
    st = AU.status()
    assert st["audited_by_joe"] is False
    assert st["passed"] is False
    assert "UNAUDITED" in st["label"]
    assert st["threshold"] == AU.THRESHOLD


def test_H3_published_score_carries_the_audit_label(monkeypatch, tmp_path):
    """data/reader_eval/score.json must not publish a bare accuracy: the label travels with it."""
    s = json.loads((EVAL / "score.json").read_text())
    assert "UNAUDITED" in s["label"], "score.json publishes an accuracy without the unaudited label"
    assert s["audit"]["passed"] is False
    assert s["audit"]["audited_by_joe"] is False
    assert s["audit"]["kappa_A_vs_H"] is not None


def test_H3_a_passing_audit_requires_every_row_and_the_threshold():
    """finalize() may not mark passed on a partial sheet or below the bar (INV-6: no gate is weakened)."""
    part = AU.finalize({"rows": [{"joe_class": "sanctions", "reader_class": "sanctions",
                                  "gold_class_A": "sanctions"}]}, 30)
    assert part["passed"] is False, "passed on 1 of 30 answered"
    rows = [{"joe_class": "sanctions", "reader_class": "opec_decision", "gold_class_A": "sanctions"}
            for _ in range(4)]
    low = AU.finalize({"rows": rows}, 4)
    assert low["passed"] is False, "passed with kappa below the threshold"
