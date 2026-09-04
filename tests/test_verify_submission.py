import verify_submission as V
import reproduce_structural_component_ablation as RA


def test_authoritative_local_links_resolve():
    assert V.broken_links() == []


def test_ablation_reproducer_names_every_frozen_output():
    expected = __import__("json").loads((RA.A.OUT / "manifest.json").read_text())["outputs"]
    assert set(expected) == {"scores.jsonl", "summary.json"}
