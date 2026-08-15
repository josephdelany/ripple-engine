"""
regime_block.py -- R3: dependence honestly (red-team attacks 7 & 8, CONCEDED).

The frozen study clusters only same-type events within 35 days, so the six distinct
2008 events (Jan SA-power .. Dec Oran, all >35d apart) count as six independent
episodes inside ONE oil collapse. The cluster bootstrap therefore over-counts
effective N, and the CI leans on a few crisis regimes and post-registration
outliers (2026 Iran |CAR| ~50).

This lens recomputes H1 -- on the SAR headline metric (R1) AND the raw |CAR|
secondary -- dropping whole REGIME BLOCKS: 2008, 2020, 2026, and all three; plus a
5%-winsorized variant. If the (already null) SAR CI stays null and the raw CI
collapses when 2008/2026 are removed, attacks 7-8 are confirmed. Publish either way.

ADDITIVE: reads DB, writes data/h1_regimeblock.json. Frozen record untouched.

Run:  python3 src/regime_block.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

import research
import sar_lens
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
HORIZON = 20


def _scenario(conn, events, drop_years, label):
    """Gate H1 (raw + SAR) on the corpus with drop_years removed as whole blocks."""
    yr = pd.to_datetime(events["event_date"]).dt.year
    sub = events[~yr.isin(drop_years)] if drop_years else events
    raw = sar_lens._mags(conn, sub, HORIZON, standardized=False)
    sar = sar_lens._mags(conn, sub, HORIZON, standardized=True)
    m_raw, s_raw = sar_lens._episodes(conn, sub, raw)
    m_sar, s_sar = sar_lens._episodes(conn, sub, sar)
    if m_sar is None:
        return {"label": label, "dropped": sorted(drop_years), "ok": False, "reason": "too few episodes"}
    return {"label": label, "dropped": sorted(drop_years), "ok": True,
            "sar": sar_lens._gate(m_sar, s_sar), "raw": sar_lens._gate(m_raw, s_raw)}


def _winsorized(conn, events, label, pct=5):
    """Full corpus, but magnitudes winsorized at [pct, 100-pct] before the split (limits leverage)."""
    raw = sar_lens._mags(conn, events, HORIZON, standardized=False)
    sar = sar_lens._mags(conn, events, HORIZON, standardized=True)
    m_raw, s_raw = sar_lens._episodes(conn, events, raw)
    m_sar, s_sar = sar_lens._episodes(conn, events, sar)

    def wz(m):
        lo, hi = np.percentile(m, [pct, 100 - pct])
        return np.clip(m, lo, hi)

    return {"label": label, "pct": pct, "ok": True,
            "sar": sar_lens._gate(wz(m_sar), s_sar), "raw": sar_lens._gate(wz(m_raw), s_raw)}


def run():
    conn = sqlite3.connect(DB)
    events = research._events(conn)
    scenarios = [
        _scenario(conn, events, set(), "full"),
        _scenario(conn, events, {2008}, "drop_2008"),
        _scenario(conn, events, {2020}, "drop_2020"),
        _scenario(conn, events, {2026}, "drop_2026"),
        _scenario(conn, events, {2008, 2020, 2026}, "drop_all_three"),
    ]
    win = _winsorized(conn, events, "winsorized_5pct")
    conn.close()

    def line(r, key):
        g = r.get(key)
        if not g:
            return None
        return {"amp": g["amp"], "ci95": g["ci95"], "perm_p": g["perm_p"],
                "ci_excludes_zero": g["ci_excludes_zero"], "n_episodes": g["n_episodes"]}

    out = {
        "lens": "R3_regime_block",
        "attacks": [7, 8],
        "headline_metric": "SAR (|SCAR+20| high-minus-low, unitless)",
        "scenarios_sar": {r["label"]: line(r, "sar") for r in scenarios if r.get("ok")},
        "scenarios_raw_secondary": {r["label"]: line(r, "raw") for r in scenarios if r.get("ok")},
        "winsorized_5pct": {"sar": win["sar"], "raw": win["raw"]},
        "verdict": None,
    }
    sar_full = out["scenarios_sar"]["full"]
    any_sar_survives = any(v and v["ci_excludes_zero"] for v in out["scenarios_sar"].values())
    out["verdict"] = (
        "SAR CI includes zero in EVERY regime-block scenario -> H1 amplification is not robust and not "
        "supported on the standardized metric." if not any_sar_survives else
        "Some SAR scenario CI excludes zero -> see which; H1 partially survives.")
    (ROOT / "data" / "h1_regimeblock.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
