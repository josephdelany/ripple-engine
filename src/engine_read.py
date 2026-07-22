"""
engine_read.py -- THE SYNTHESIS LAYER ("Engine Read").

WHAT IT ANSWERS, every run:
    "If a geopolitical shock landed TODAY, what does history say would happen?"

It does NOT forecast and it does NOT re-test anything. It CONSUMES two things the
rest of the engine already established, and states today's position against them:

  1. The pre-registered VERDICTS (H1 HOLDS, H2 HOLDS, H3 FAILS) -- read straight
     from data/registered_run_results.txt. A hypothesis that did not survive
     pre-registration (H3) is reported but can NEVER act as an amplifier.
  2. The historical event sample in oil.db -- clustered with the SAME logic as
     robustness.py (imported, not re-implemented). From it we take, per
     hypothesis, the event-sample median that its high/low split turns on, and
     per event type the clustered base-rate ripple (mean CAR at +1/+5/+10/+20).

The "read": for each surviving hypothesis we compare TODAY's signal value to that
historical median. If today's value sits on the amplifying side, that amplifier
is ON. Point-in-time: we only ever use the latest reading available at run time.

Outputs: data/engine_read.json (machine), data/engine_read.md (human note), and a
console report. Every number traces to a query below -- nothing is editorialised
beyond the one templated `read` sentence.

Run:  python3 src/engine_read.py
"""

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse -- do NOT fork -- the clustering + registered spec, and the event-study
# primitives. engine_read consumes this machinery; it never re-implements it.
from robustness import assign_clusters, REGISTERED, CLUSTER_DAYS
from event_study import load_returns, car_for_event, PRE, HORIZONS
from derive_signals import load_wide, build_signals, MECHANISMS

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
REGISTERED_RESULTS = ROOT / "data" / "registered_run_results.txt"
JSON_OUT = ROOT / "data" / "engine_read.json"
MD_OUT = ROOT / "data" / "engine_read.md"

# Human labels for the three registered signals (kept local so a label change
# here can never silently alter the imported analysis).
HYP_LABEL = {
    "H1": ("Market stress", "VIX percentile", "percentile"),
    "H2": ("Physical tightness", "Inventory sigma vs seasonal norm", "sigma"),
    "H3": ("Speculative positioning", "Managed-money net-long percentile", "percentile"),
}


def load_registered_verdicts():
    """The verdicts are a RESULT of the pre-registered run -- read them, never
    recompute them. Returns e.g. {'H1':'HOLDS','H2':'HOLDS','H3':'FAILS'}."""
    if not REGISTERED_RESULTS.exists():
        return {}
    txt = REGISTERED_RESULTS.read_text()
    out = {}
    for m in re.finditer(r"(H[123])\s+(HOLDS|FAILS)\s+\(clustered", txt):
        out.setdefault(m.group(1), m.group(2))     # first hit = the verdict block
    return out


def latest_reading(signals, sid):
    """Today's value for a signal and the date it is as of (point-in-time)."""
    if sid not in signals:
        return None, None
    s = signals[sid].dropna()
    if s.empty:
        return None, None
    return float(s.iloc[-1]), s.index[-1].date().isoformat()


def build_clustered_events(ret, signals, events):
    """One row per event (car path at each horizon + each registered signal at
    t-1), then collapse overlapping events with robustness.assign_clusters and
    keep the first of each cluster -- exactly the sample the verdicts were judged
    on. Returns the clustered DataFrame."""
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)  # t-1: no lookahead
        row = {"event_id": ev["event_id"], "date": ev["event_date"],
               "type": ev["type"]}
        for h in HORIZONS:
            row[f"car{h}"] = car[PRE + h]
        for _hid, sid, key, _sign, _desc in REGISTERED:
            s = signals[sid].dropna() if sid in signals else pd.Series(dtype=float)
            row[key] = s.asof(cutoff) if len(s) else np.nan
        rows.append(row)
    df = assign_clusters(pd.DataFrame(rows))            # imported clustering
    return df.groupby("cluster").first().reset_index()  # keep first of each cluster


def amplifier_status(latest, median, sign, verdict):
    """ON / OFF / FAILED / UNKNOWN.

    A failed hypothesis (H3) is NEVER an amplifier. Otherwise the amplifier is ON
    when today's value sits on the side the hypothesis predicts amplifies: the
    high side when sign>0 (H1 VIX), the low side when sign<0 (H2 tight inventories).
    """
    if verdict == "FAILS":
        return "FAILED"
    if verdict != "HOLDS" or latest is None or median is None or np.isnan(median):
        return "UNKNOWN"
    on_amplifying_side = latest >= median if sign > 0 else latest < median
    return "ON" if on_amplifying_side else "OFF"


def _ordinal(n):
    """12 -> '12th', 41 -> '41st' -- so the daily note reads naturally."""
    n = int(round(n))
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def build_read(hyps):
    """The one templated English sentence. Built only from computed statuses --
    no numbers invented, no claim made beyond ON/OFF and the value."""
    h1, h2 = hyps["H1"], hyps["H2"]
    parts = []
    if h2["latest"] is not None:
        direction = "below" if h2["latest"] < 0 else "above"
        parts.append(f"Inventories {abs(h2['latest']):.1f}σ {direction} seasonal "
                     f"norm (H2 amplifier {h2['amplifier']})")
    if h1["latest"] is not None:
        parts.append(f"VIX {_ordinal(h1['latest'])} pct (H1 {h1['amplifier']})")
    lead = "; ".join(parts) if parts else "State signals unavailable"

    physical = ("physically primed" if h2["amplifier"] == "ON"
                else "physically well-supplied")
    psych = ("psychologically stressed" if h1["amplifier"] == "ON"
             else "psychologically calm")
    tail = f"A supply shock today lands on a {physical} but {psych} market."
    return f"{lead}. {tail}"


def compute():
    """Do all the reads/queries and return the full result dict."""
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql(
        "SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    conn.close()

    verdicts = load_registered_verdicts()
    clustered = build_clustered_events(ret, signals, events)

    # --- Per-hypothesis amplifier status ---
    hyps = {}
    read_dates = []
    for hid, sid, key, sign, _desc in REGISTERED:
        latest, as_of = latest_reading(signals, sid)
        if as_of:
            read_dates.append(as_of)
        # The threshold is the median of the clustered event sample -- the exact
        # value robustness.split() divides high/low on (v[col].median()).
        col = clustered[clustered[key].notna()]
        median = float(col[key].median()) if len(col) else None
        verdict = verdicts.get(hid, "UNKNOWN")
        amp = amplifier_status(latest, median, sign, verdict)
        label, signal_name, unit = HYP_LABEL[hid]
        hyps[hid] = {
            "hypothesis": hid,
            "label": label,
            "signal": sid,
            "signal_name": signal_name,
            "unit": unit,
            "latest": None if latest is None else round(latest, 2),
            "as_of_reading": as_of,
            "event_median": None if median is None else round(median, 2),
            "direction": "high amplifies" if sign > 0 else "low (tight) amplifies",
            "verdict": verdict,
            "amplifier": amp,
        }

    # --- Clustered base rate per event type (mean CAR at each horizon, %) ---
    base_rates = []
    for etype, grp in clustered.groupby("type"):
        row = {"type": etype, "n": int(len(grp))}
        for h in HORIZONS:
            row[f"car{h}"] = round(float(grp[f"car{h}"].mean()) * 100, 1)
        base_rates.append(row)
    base_rates.sort(key=lambda r: r["n"], reverse=True)

    as_of = max(read_dates) if read_dates else datetime.now(timezone.utc).date().isoformat()
    result = {
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "clustered_event_n": int(len(clustered)),
        "hypotheses": hyps,
        "base_rates": base_rates,
        "read": build_read(hyps),
        "note": ("Amplifier thresholds/base rates computed from data/oil.db with "
                 "robustness.py clustering; verdicts consumed from the pre-registered "
                 "record. H3 failed pre-registration and is never an amplifier. "
                 "This is a conditional read of history, not a forecast."),
    }
    return result


def write_md(r):
    """The human daily note -- same content as the JSON, every number from a query."""
    lines = [f"# Engine Read — {r['as_of']}", "",
             f"> {r['read']}", "",
             f"*Generated {r['generated_at']} from data/oil.db "
             f"(clustered event sample n={r['clustered_event_n']}).*", "",
             "## Amplifier status (registered hypotheses)", "",
             "| Hyp | What | Latest (as of) | Event-sample median | Verdict | Amplifier |",
             "|-----|------|----------------|---------------------|---------|-----------|"]
    for hid in ("H1", "H2", "H3"):
        h = r["hypotheses"][hid]
        latest = "n/a" if h["latest"] is None else f"{h['latest']} ({h['as_of_reading']})"
        med = "n/a" if h["event_median"] is None else h["event_median"]
        lines.append(f"| {hid} | {h['label']} ({h['unit']}) | {latest} | {med} "
                     f"| {h['verdict']} | **{h['amplifier']}** |")
    lines += ["", "_H3 is shown for completeness only: it failed pre-registration "
              "and is never used as an amplifier._", "",
              "## Historical base rates — clustered mean CAR by event type", "",
              "| Event type | n | CAR+1 | CAR+5 | CAR+10 | CAR+20 |",
              "|------------|---|-------|-------|--------|--------|"]
    for b in r["base_rates"]:
        lines.append(f"| {b['type']} | {b['n']} | {b['car1']:+.1f}% | {b['car5']:+.1f}% "
                     f"| {b['car10']:+.1f}% | {b['car20']:+.1f}% |")
    lines += ["", f"_{r['note']}_", ""]
    MD_OUT.write_text("\n".join(lines))


def print_console(r):
    print("=" * 72)
    print(f"ENGINE READ  —  as of {r['as_of']}   (clustered n={r['clustered_event_n']})")
    print("=" * 72)
    print(f"\n  {r['read']}\n")
    print("  AMPLIFIER STATUS (verdicts from the pre-registered record)")
    print("  " + "-" * 68)
    print(f"  {'hyp':<5}{'what':<22}{'latest':>10}{'median':>10}{'verdict':>9}{'amp':>8}")
    for hid in ("H1", "H2", "H3"):
        h = r["hypotheses"][hid]
        latest = "n/a" if h["latest"] is None else f"{h['latest']}"
        med = "n/a" if h["event_median"] is None else f"{h['event_median']}"
        print(f"  {hid:<5}{h['label']:<22}{latest:>10}{med:>10}"
              f"{h['verdict']:>9}{h['amplifier']:>8}")
    print("\n  CLUSTERED BASE-RATE RIPPLE by event type (mean CAR)")
    print("  " + "-" * 68)
    print(f"  {'event type':<24}{'n':>3}{'CAR+1':>9}{'CAR+5':>9}{'CAR+10':>9}{'CAR+20':>9}")
    for b in r["base_rates"]:
        print(f"  {b['type']:<24}{b['n']:>3}{b['car1']:>+8.1f}%{b['car5']:>+8.1f}%"
              f"{b['car10']:>+8.1f}%{b['car20']:>+8.1f}%")
    print(f"\n  Wrote {JSON_OUT.name} and {MD_OUT.name}")
    print(f"  {r['note']}")


def main():
    r = compute()
    JSON_OUT.write_text(json.dumps(r, indent=2))
    write_md(r)
    print_console(r)


if __name__ == "__main__":
    main()
