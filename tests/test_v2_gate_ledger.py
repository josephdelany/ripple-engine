"""Tests for the materiality gate, Big Moves detection and the claim ledger (v2 day-1)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import big_moves as BM          # noqa: E402
import ledger as L              # noqa: E402
import materiality as M         # noqa: E402

SUMMARY = {
    "brent": {"label": "Brent", "everyday_base_rate_pct": 20.0,
              "p_big_given_class": {"opec_decision": [10, 40], "sanctions": [4, 40], "tiny": [3, 4],
                                    "policy_response": [20, 40]}},
    "diesel_crack": {"label": "Diesel crack", "everyday_base_rate_pct": 20.0,
                     "p_big_given_class": {"opec_decision": [8, 40], "sanctions": [4, 40], "tiny": [3, 4],
                                           "policy_response": [20, 40]}},
}


def test_gate_material_inline_noise():
    assert M.gate("opec_decision", SUMMARY)["significance"] == "MATERIAL"      # 25% vs 20% = 1.25x
    assert M.gate("sanctions", SUMMARY)["significance"] == "NOISE"             # 10% vs 20% = 0.5x
    assert M.gate(None, SUMMARY)["significance"] == "NOISE"
    assert M.gate("never_seen", SUMMARY)["significance"] == "NOISE"


def test_gate_thin_and_endogenous_never_material():
    g = M.gate("tiny", SUMMARY)                                                 # 75% but n=4
    assert g["significance"] != "MATERIAL" and "thin" in g["flags"]
    g = M.gate("policy_response", SUMMARY)                                      # 50% vs 20% but endogenous
    assert g["significance"] == "IN_LINE" and "endogenous" in g["flags"]


def test_attention_flags():
    assert M.flags_for("IN_LINE", 95) == ["LOUD_QUIET"]
    assert M.flags_for("MATERIAL", 20) == ["QUIET_LOUD"]
    assert M.flags_for("MATERIAL", 95) == []
    assert M.flags_for("NOISE", None) == []


def test_big_moves_detects_a_planted_shock_and_dates_onset():
    idx = pd.bdate_range("2000-01-03", periods=1500)
    rng = np.random.default_rng(1)
    p = 50 * np.exp(np.cumsum(rng.normal(0, 0.004, len(idx))))
    p[800:830] *= np.linspace(1, 1.6, 30)                    # a 60% run over 30 days from position 800
    p[830:] *= 1.6
    s = pd.Series(p, index=idx)
    eps = BM.episodes_for(s, "price")
    assert eps, "planted shock not detected"
    big = max(eps, key=lambda e: abs(e["change"]))
    assert big["sign"] == "+" and abs(pd.Timestamp(big["onset"]) - idx[799]).days <= 5
    assert big["change"] > 40


def test_big_moves_attribution_lag_and_anticipated():
    eps = [{"onset": "2020-02-19", "end": "2020-04-21", "change": -85.0, "sign": "-", "window": 60,
            "windows": [60], "from_": 59.7, "to": 9.1, "threshold": 0.3, "days": 62}]
    ev = pd.DataFrame({"event_id": ["a", "b", "c"], "event_date": pd.to_datetime(["2020-02-14", "2020-03-11", "2020-05-01"]),
                       "type": ["x", "y", "z"], "title": ["before", "during", "after"]})
    out = BM.attribute(eps, ev)[0]["events"]
    assert [e["id"] for e in out] == ["a", "b"]                # 'after' is outside the window
    assert out[0]["lag_days"] == -5 and not out[0]["anticipated"]
    assert out[1]["lag_days"] == 21 and out[1]["anticipated"]


def test_type_claim_kinds():
    t = L.type_claim("The strike could send Brent past $110 a barrel.", "infrastructure_attack", [], "hypothetical")
    assert t["kind"] == "level" and t["level"] == 110 and t["checkable"]
    t = L.type_claim("Oil prices will plunge on the news.", "opec_decision")
    assert t["kind"] == "direction" and t["direction"] == "down"
    t = L.type_claim("Iran will retaliate against Gulf shipping.", "conflict_escalation", ["country.iran"])
    assert t["kind"] == "escalation" and t["horizon_days"] == 90
    t = L.type_claim("Exports from the terminal have halted.", "infrastructure_attack")
    assert t["kind"] == "flow"
    t = L.type_claim("The regime cannot survive this.", "conflict_escalation")
    assert t["kind"] == "uncheckable" and not t["checkable"]


def test_verdict_cutoffs():
    assert L._cut(0.7, 20) == "SUPPORTED"
    assert L._cut(0.5, 20) == "MIXED"
    assert L._cut(0.3, 20) == "UNSUPPORTED"
    assert L._cut(0.9, 5) == "THIN"


def test_ledger_log_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "LEDGER_DIR", tmp_path)
    monkeypatch.setattr(L, "CLAIMS", tmp_path / "claims.jsonl")
    monkeypatch.setattr(L, "RESOLUTIONS", tmp_path / "resolutions.jsonl")
    c = L.type_claim("Oil will rise.", "opec_decision")
    c["verdict"] = {"verdict": "MIXED", "r": 0.5, "n": 40}
    L.log_claims("s1", "test", "2026-01-01", [c], price_at_knowable=80.0)
    L.log_claims("s1", "test", "2026-01-01", [c], price_at_knowable=80.0)
    assert len(L._rows(L.CLAIMS)) == 1
