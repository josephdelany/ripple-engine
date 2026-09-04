"""
test_sowhat.py -- the live so-what wire (Step 3).

Coherence: the wire assembles a decision-relevant read whose ONLY claims are validated-backbone
edges, and ranks situations by multi-modal corroboration. Run: python3 -m pytest -q tests/test_sowhat.py
"""


def test_sw1_read_is_coherent_and_only_claims_validated(tmp_path, monkeypatch):
    import sowhat
    monkeypatch.setattr(sowhat, "OUT", tmp_path / "sowhat.json")
    r = sowhat.build()
    assert r["regime"] in ("ON", "OFF", "FAILED", "UNKNOWN", "?")
    assert isinstance(r["so_what"], str) and len(r["so_what"]) > 20
    # every surfaced propagation edge is a validated-backbone edge (the wire never claims a null/trap)
    import json
    from pathlib import Path
    pg = json.loads((Path(sowhat.DATA) / "propagation_graph.json").read_text())
    validated = {e["to"] for e in pg.get("backbone_validated", [])}
    for b in r["validated_propagation"]:
        assert b["to"] in validated


def test_sw2_situations_ranked_by_corroboration(tmp_path, monkeypatch):
    import sowhat
    monkeypatch.setattr(sowhat, "OUT", tmp_path / "sowhat.json")
    r = sowhat.build()
    sits = r["active_situations"]
    if len(sits) >= 2:
        # sorted descending by (max_modality_classes, events)
        keys = [(s["max_modality_classes"], s["events"]) for s in sits]
        assert keys == sorted(keys, reverse=True)
