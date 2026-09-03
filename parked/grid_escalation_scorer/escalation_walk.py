"""
escalation_walk.py -- GRID_STUDY_REGISTRATION.md Part IV (2026-09-03): the escalation arm, 1987-2014.

Registered before this file existed (commit 38a9177). B builds NO dyad-date panel: session G builds it
(`data/grid/g/G4_REGISTRATION.md` Amendment 3) and B applies the strict subset at scoring time on a field
that is already there (G's A3.3). This module is the scored study on top of G's panel.

THE THREE LIMITS ARE PROPERTIES OF THE CONSTRUCTION, NOT CAVEATS ON A RESULT (§4.1). Every summary this
module writes carries all three in the same object as every skill number:

  span_ends 2014-09-30   the last sided source ends 2014-12-31 and ies90.covers needs t + 90 <= that, so no
                         number here describes the world after 2014 or what a live engine would do
  ceiling SUGGESTIVE     every cell is retrospective = 1; WORLD_STATE_CODEBOOK Amendment 1 says a
                         retrospective field alone can never make a read VALIDATED. n does not touch this --
                         which is the sharpest thing to say about a study whose whole purpose was more n
  panel_type recurrence  the active set admits a dyad only after a recorded clash, so this scores
                         continuation and de-escalation and NEVER onset

It reads G's PANEL and never `event_outcomes` or `ies90.score_event`, so it is not blocked by the walk
freeze of 2026-09-03 (§4.9) -- and it is written that way on purpose, so the freeze cannot be broken
through this door.

Run:  python3 src/engine/grid/escalation_walk.py        (gated: exits cleanly until G's panel lands)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from engine import scoring as SC              # noqa: E402
from engine import inference as INF           # noqa: E402
from engine import delta_experiment as DX     # noqa: E402  (Amendment L's registered Δ machinery)
from engine.grid import power_arithmetic as PA  # noqa: E402
import walk as W                              # noqa: E402

PANEL_DIR = ROOT / "data" / "grid" / "g"
OUT_DIR = ROOT / "data" / "grid" / "escalation"

SPAN_END = "2014-09-30"                 # §4.1.1, and G's A3.1 arithmetic
DEGENERACY_BAR = 0.95                   # §4.7, G's §5.1
MIN_TIER_N = W.REGISTERED["min_tier_n"]
CLUSTER_DAYS = W.REGISTERED["cluster_days"]
SEED = W.REGISTERED["seeds"]["bootstrap_and_spa"]
STRICT = "opposed_side"                 # §4.5, G's A3.3
EVIDENCE_ORDER = ("opposed_side", "icb_co_actor", "icb_co_actor_never_opposed", "ged_location", "undefined")

# The limits travel in the same object as every number (§4.1). Not a footnote, not a README line.
LIMITS = {
    "span_ends": SPAN_END,
    "span_rule": "ies90.covers needs t + 90 <= the source coverage end; MID / MIDI / COW War end "
                 "2014-12-31, so 2014-09-30 is the last month-end that clears it. No number here "
                 "describes the world after 2014 or what a live engine would do.",
    "ceiling": "SUGGESTIVE",
    "ceiling_rule": "every cell is retrospective = 1; WORLD_STATE_CODEBOOK.md Amendment 1 -- a "
                    "retrospective field alone can never make a read VALIDATED. n does not touch this.",
    "panel_type": "recurrence",
    "panel_type_rule": "the active set admits a dyad only after a recorded clash, so a quiet dyad that "
                       "goes to war is absent at every date before its first record. This scores "
                       "continuation and de-escalation and NEVER onset. Describing this arm as "
                       "forecasting the outbreak of conflict is forbidden (§4.1.3).",
}

# §4.0: B reads G's panel through a declared contract. Concept -> the column names B will accept.
SCHEMA = {
    "date": ("date", "grid_date", "t", "as_of"),
    "dyad": ("dyad", "dyad_id", "pair"),
    "level": ("L", "level", "ies90_level", "l"),
    "level_pre": ("Lpre", "L_pre", "level_pre", "lpre"),
    "delta": ("dIES", "delta", "delta_ies", "d_ies"),
    "evidence_class": ("evidence_class", "evidence", "basis_class"),
    "active_vr3": ("vr3", "VR3", "active_vr3", "vr3_active"),
    "admit_record_end": ("admit_record_end", "admitting_record_end", "active_record_end"),
}


def _rel(p: Path) -> str:
    """Repo-relative where possible; absolute otherwise (a test fixture lives outside the tree)."""
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def panel_path():
    for name in ("PANEL.parquet", "PANEL.csv.gz", "PANEL.csv"):
        p = PANEL_DIR / name
        if p.exists():
            return p
    return None


def load_panel(path=None):
    """Read G's panel through §4.0's contract, and fail LOUDLY and specifically if it does not match."""
    path = path or panel_path()
    if path is None:
        raise FileNotFoundError(
            f"G's panel is not in the tree yet. Part IV is gated on it (§4.0): expected one of "
            f"PANEL.parquet / PANEL.csv.gz / PANEL.csv under {PANEL_DIR}. B does not build a panel.")
    df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path, low_memory=False)
    cols, missing = {}, []
    for concept, names in SCHEMA.items():
        hit = next((n for n in names if n in df.columns), None)
        if hit is None:
            missing.append(f"{concept} (tried {', '.join(names)})")
        else:
            cols[concept] = hit
    if missing:
        raise KeyError("G's panel does not carry: " + "; ".join(missing) +
                       f". Columns present: {sorted(df.columns)}. Fix the SCHEMA map in this module or "
                       "send a handoff to G -- do not rename G's file.")
    out = df.rename(columns={v: k for k, v in cols.items()})
    out["date"] = pd.to_datetime(out["date"])
    return out[out["date"] <= pd.Timestamp(SPAN_END)].reset_index(drop=True), path


# ---------------------------------------------------------------- §4.8 the VR-3 assertion

def assert_vr3(df):
    """§4.8: G's probe caught 39 of 335 cells in 2018 admitted on a record still running at t. B inherits
    the fix by CONSTRUCTION and asserts it rather than trusting it. One violation voids the run."""
    if "active_vr3" in df:
        bad_flag = int((~df["active_vr3"].astype(bool)).sum())
    else:
        bad_flag = 0
    ends = pd.to_datetime(df["admit_record_end"], errors="coerce")
    still_running = ends.isna() | (ends >= df["date"])
    n_bad = int(still_running.sum())
    return {"n_cells": int(len(df)), "n_not_vr3_flagged": bad_flag,
            "n_admitting_record_not_closed_before_t": n_bad,
            "asserted": bool(n_bad == 0 and bad_flag == 0),
            "rule": "§4.8: every admitted cell's admitting record ends STRICTLY before t. A single "
                    "violation voids the run, as Amendment F.1 does for the event walk.",
            "first_violation": (None if n_bad == 0 else
                                df.loc[still_running, ["date", "dyad"]].head(1).to_dict("records"))}


# ---------------------------------------------------------------- §4.7 the tripwire

def share_zero(df, col="delta"):
    v = pd.to_numeric(df[col], errors="coerce").dropna()
    return float((v == 0).mean()) if len(v) else float("nan")


def tripwire(df):
    """§4.7: share-zero per year and over the window, on both targets and both subsets, BEFORE any skill
    number. A breach of the registered 0.95 bar is reported to Joe immediately; the slice is never dropped
    and the bar is never moved (INV-6)."""
    out = {"bar": DEGENERACY_BAR, "rule": "§4.7 / G §5.1: >= 95 % zeros is degenerate. A breach anywhere in "
                                          "the window is reported to Joe BEFORE any skill number computed "
                                          "on the breaching slice. The slice is not dropped and the bar is "
                                          "not moved.", "breaches": []}
    subsets = {"full": df, "strict": df[df["evidence_class"] == STRICT]}
    for sname, sub in subsets.items():
        if not len(sub):
            continue
        for target in ("delta", "level"):
            out[f"{sname}|{target}|window"] = round(share_zero(sub, target), 5)
            by_year = {}
            for y, g in sub.groupby(sub["date"].dt.year):
                s = share_zero(g, target)
                by_year[str(int(y))] = round(s, 5) if s == s else None
                if s == s and s >= DEGENERACY_BAR:
                    out["breaches"].append({"subset": sname, "target": target, "year": int(y),
                                            "share_zero": round(s, 5), "n": int(len(g))})
            out[f"{sname}|{target}|by_year"] = by_year
    out["breached"] = bool(out["breaches"])
    return out


# ---------------------------------------------------------------- §4.6 effective n

def effective_n(df, value="delta"):
    """Part II's machinery unchanged: the two-way dyad x date design effect with the registered 1.5x
    tie-break against the separable form, the larger used. The informative-cell count sits beside it,
    because n_eff on a mostly-zero panel is a CEILING and not an estimate (§4.6)."""
    piv = df.pivot_table(index="date", columns="dyad", values=value, aggfunc="first")
    X = piv.to_numpy(float)
    covered = np.ones(X.shape[0], bool)
    tw = PA.two_way_cluster_deff(X, covered)
    dates = [str(d.date()) for d in piv.index]
    mb = W._mean_block(dates, CLUSTER_DAYS)
    lag = max(int(round(mb)) - 1, 0)
    y = np.nanmean(X, axis=1)
    t_blk = PA.deff_block(y, mb, lag, "escalation|row_mean")
    varying = [j for j in range(X.shape[1]) if np.nanstd(X[:, j]) > 0]
    d_eff = (PA.eff_width(np.nan_to_num(pd.DataFrame(X[:, varying]).corr(min_periods=30).to_numpy(), nan=0.0))
             if len(varying) > 1 else float(len(varying)))
    n_cells = int(np.isfinite(X).sum())
    t_eff = X.shape[0] / t_blk["deff_used"]
    deff_sep = n_cells / max(t_eff * d_eff, 1e-9)
    deff_two = (tw or {}).get("deff_two_way")
    fired = bool(deff_two and max(deff_sep, deff_two) / max(min(deff_sep, deff_two), 1e-9) > PA.DEFF_TIEBREAK)
    deff_used = max(deff_sep, deff_two) if fired else deff_sep
    floored = bool(deff_used < PA.DEFF_FLOOR)
    deff_used = max(deff_used, PA.DEFF_FLOOR)   # n_eff may never exceed n_nominal
    v = pd.to_numeric(df[value], errors="coerce")
    return {"n_nominal_cells": n_cells, "n_dates": int(X.shape[0]), "n_dyads": int(X.shape[1]),
            "n_dyads_with_variation": len(varying), "informative_cells": int((v != 0).sum()),
            "deff_separable": round(float(deff_sep), 3), "deff_two_way": deff_two,
            "tiebreak_fired": fired, "deff_used": round(float(deff_used), 3),
            "deff_floored_at_1": floored,
            "n_eff": round(n_cells / deff_used, 1) if deff_used else None,
            "mean_block": round(mb, 2), "hac_lag": lag,
            "ceiling_warning": "n_eff on a panel that is overwhelmingly zeros is driven by the zeros' "
                               "dependence structure, not by the information. Read informative_cells "
                               "beside it; n_eff is a ceiling, not an estimate (§4.6)."}


# ---------------------------------------------------------------- the run

def compute(panel=None):
    df, path = load_panel(panel)
    vr3 = assert_vr3(df)
    trip = tripwire(df)
    out = {
        "study": "GRID_STUDY_REGISTRATION.md Part IV (2026-09-03)",
        "unit": "dyad-date",
        "limits": LIMITS,                       # §4.1: in the same object as every number
        "panel_source": _rel(path),
        "panel_owner": "session G (data/grid/g/G4_REGISTRATION.md Amendment 3); B builds no panel (§4.0)",
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "vr3_assertion": vr3,
        "tripwire": trip,
        "evidence_mix": {k: int(v) for k, v in Counter(df["evidence_class"]).items()},
        "reads_walk_forward": False,
        "walk_freeze": "§4.9: this arm reads G's PANEL and never event_outcomes or ies90.score_event, so "
                       "the src/walk.py freeze of 2026-09-03 is not broken through this door.",
    }
    if not vr3["asserted"]:
        out["status"] = "VOID -- the VR-3 assertion failed (§4.8); no score is computed"
        return out
    if trip["breached"]:
        out["status"] = ("TRIPWIRE -- share-zero passed the registered 0.95 bar; §4.7 requires this be "
                         "reported to Joe BEFORE any skill number on the breaching slice")
    for name, sub in (("full", df), ("strict", df[df["evidence_class"] == STRICT])):
        if len(sub) < MIN_TIER_N:
            out[f"n_eff_{name}"] = {"note": f"only {len(sub)} cells; below min_tier_n {MIN_TIER_N}"}
            continue
        out[f"n_eff_{name}"] = {t: effective_n(sub, t) for t in ("delta", "level")}
    out.setdefault("status", "READY -- panel accepted, assertions passed; scoring follows")
    return out


def main():
    if panel_path() is None:
        print(json.dumps({"gated": True, "reason": "G's PANEL is not in the tree yet (§4.0)",
                          "expected_under": _rel(PANEL_DIR),
                          "limits": LIMITS}, indent=1))
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = compute()
    (OUT_DIR / "summary.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str)[:4000])


if __name__ == "__main__":
    main()
