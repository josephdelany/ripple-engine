import verify_submission as V
import reproduce_structural_component_ablation as RA


def test_authoritative_local_links_resolve():
    assert V.broken_links() == []


def test_ablation_reproducer_names_every_frozen_output():
    expected = __import__("json").loads((RA.A.OUT / "manifest.json").read_text())["outputs"]
    assert set(expected) == {"scores.jsonl", "summary.json"}


def test_citation_metadata_names_the_release():
    cff = (V.ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert f'version: "{V.RELEASE_VERSION}"' in cff
    assert f'date-released: "{V.RELEASE_DATE}"' in cff
