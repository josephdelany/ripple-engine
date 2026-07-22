"""
scenario.py -- the SCENARIO PLAYBOOK ("if an event of type X happened today").

WHAT IT ANSWERS, per event type:
    "If an event of this type occurred TODAY, what does history + the current
     state of the system imply?"  -- as a one-page 'scenario card.'

It is NOT a forecast of whether events occur -- it says nothing about the odds of
a war or an OPEC decision. It is purely a market-CONSEQUENCE conditional: given
that such an event happens, here is what history and today's conditioning imply.
Every card carries that caveat, always.

Each card, all computed from oil.db:
  1. Analogs      -- every historical event of that type (clustered with the same
                     logic as robustness.py), with CAR+5 and CAR+20.
  2. Base rates   -- clustered mean CAR+1/+5/+10/+20, the CAR+20 min/max range,
                     and n. Small n is shouted, not whispered.
  3. Conditioning -- today's amplifier states from the engine-read logic
                     (H1 VIX, H2 inventories; H3 always FENCED, it failed
                     pre-registration), and, for whichever amplifiers are ON, the
                     REGISTERED amplification number (never recomputed).
  4. A caveat     -- conditional on occurrence; the engine does not forecast events.

This module CONSUMES existing machinery (clustering, CAR, amplifier logic) by
import -- it forks nothing and re-tests nothing.

Run:  python3 src/scenario.py conflict_escalation      # one card
      python3 src/scenario.py --all                    # all cards + data/playbook.md
"""

import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd

# Reuse -- do NOT re-implement -- clustering, CAR, and the amplifier logic.
from engine_read import (build_clustered_events, amplifier_status, latest_reading,
                         load_registered_verdicts, HYP_LABEL)
from robustness import REGISTERED
from event_study import load_returns, HORIZONS
from derive_signals import load_wide, build_signals
from load_events import VALID_TYPES

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
REGISTERED_RESULTS = ROOT / "data" / "registered_run_results.txt"
MD_OUT = ROOT / "data" / "playbook.md"

SMALL_N_ANECDOTE = 3     # at or below this: shout "anecdote, not statistics"
SMALL_N_INDICATIVE = 8   # at or below this: "small sample, indicative only"

CAVEAT = ("CAVEAT: this card is conditional on an event of this type OCCURRING. "
          "The engine does NOT forecast whether -- or when -- such an event occurs.")


def load_registered_amplifications():
    """Read the pre-registered verdict AND clustered amplification (pp) per
    hypothesis from the registered record. These are the numbers we CITE for an
    ON amplifier -- read from the frozen record, never recomputed here."""
    out = {}
    if REGISTERED_RESULTS.exists():
        pat = r"(H[123])\s+(HOLDS|FAILS)\s+\(clustered\s+([+-][\d.]+)\s*pp"
        for m in re.finditer(pat, REGISTERED_RESULTS.read_text()):
            out.setdefault(m.group(1), {"verdict": m.group(2), "amp_pp": m.group(3)})
    return out


def n_flag(n):
    """Turn a sample size into an honesty label -- loud when the sample is thin."""
    if n == 0:
        return "n=0 -- NO HISTORICAL ANALOGS for this type"
    if n <= SMALL_N_ANECDOTE:
        return f"n={n} -- ANECDOTE, NOT STATISTICS"
    if n <= SMALL_N_INDICATIVE:
        return f"n={n} -- small sample, indicative only"
    return f"n={n}"


def build_playbook():
    """Compute today's conditioning (once, global) and a card per event type."""
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql(
        "SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    conn.close()

    clustered = build_clustered_events(ret, signals, events)   # imported clustering
    verdicts = load_registered_verdicts()                       # imported (frozen record)
    reg_amps = load_registered_amplifications()

    # --- Today's conditioning: point-in-time amplifier states (global) ---
    conditioning, read_dates = [], []
    for hid, sid, key, sign, _desc in REGISTERED:
        latest, as_of = latest_reading(signals, sid)
        if as_of:
            read_dates.append(as_of)
        col = clustered[clustered[key].notna()]
        median = float(col[key].median()) if len(col) else None   # split threshold
        verdict = verdicts.get(hid, "UNKNOWN")
        amp = amplifier_status(latest, median, sign, verdict)      # imported logic
        conditioning.append({
            "hid": hid, "label": HYP_LABEL[hid][0], "signal": sid,
            "latest": None if latest is None else round(latest, 2),
            "median": None if median is None else round(median, 2),
            "verdict": verdict, "amplifier": amp,
            "reg_amp_pp": reg_amps.get(hid, {}).get("amp_pp"),
        })
    as_of = max(read_dates) if read_dates else None

    # --- One card per event type ---
    cards = []
    for etype in sorted(VALID_TYPES):
        grp = clustered[clustered["type"] == etype].sort_values("date")
        n = len(grp)
        analogs = [{"event_id": r.event_id, "date": r.date,
                    "car5": round(r.car5 * 100, 1), "car20": round(r.car20 * 100, 1)}
                   for r in grp.itertuples()]
        base = {}
        if n:
            for h in HORIZONS:
                base[f"car{h}"] = round(grp[f"car{h}"].mean() * 100, 1)
            base["car20_min"] = round(grp["car20"].min() * 100, 1)
            base["car20_max"] = round(grp["car20"].max() * 100, 1)
        cards.append({"type": etype, "n": n, "analogs": analogs, "base": base})
    cards.sort(key=lambda c: c["n"], reverse=True)   # best-evidenced first
    return {"as_of": as_of, "conditioning": conditioning, "cards": cards}


def conditioning_summary(conditioning):
    """One compact line of today's amplifier context (used in the widget)."""
    bits = []
    for c in conditioning:
        if c["amplifier"] == "ON":
            bits.append(f"{c['hid']} ON({c['reg_amp_pp'] or '?'}pp)")
        elif c["amplifier"] == "FAILED":
            bits.append(f"{c['hid']} FENCED")
        else:
            bits.append(f"{c['hid']} {c['amplifier']}")
    return ", ".join(bits)


# ---------------------------------------------------------------- console output

def print_conditioning(conditioning, as_of):
    print(f"TODAY'S CONDITIONING (point-in-time, as of {as_of})")
    for c in conditioning:
        line = f"  {c['hid']} {c['label']:<24}{c['amplifier']:<7}"
        if c["latest"] is not None and c["median"] is not None:
            line += f" (latest {c['latest']} vs event-median {c['median']})"
        if c["amplifier"] == "ON" and c["reg_amp_pp"]:
            line += (f"  -> registered clustered amplification {c['reg_amp_pp']}pp "
                     f"on |CAR+20| (n=20, {c['verdict']})")
        if c["amplifier"] == "FAILED":
            line += "  [fenced off -- failed pre-registration; never applied]"
        print(line)


def print_card(card, conditioning, as_of):
    et, n, b = card["type"], card["n"], card["base"]
    print("=" * 76)
    print(f'SCENARIO -- {et}   "if an event of this type happened today"')
    print("=" * 76)

    print("\nANALOGS (clustered historical events of this type)")
    if n:
        print(f"  {'event_id':<32}{'date':<12}{'CAR+5':>9}{'CAR+20':>9}")
        for a in card["analogs"]:
            print(f"  {a['event_id'][:31]:<32}{a['date']:<12}"
                  f"{a['car5']:>+8.1f}%{a['car20']:>+8.1f}%")
    else:
        print("  (none in the dataset)")

    print("\nBASE RATES (clustered mean, this type)")
    if n:
        print(f"  CAR+1 {b['car1']:+.1f}%   CAR+5 {b['car5']:+.1f}%   "
              f"CAR+10 {b['car10']:+.1f}%   CAR+20 {b['car20']:+.1f}%")
        print(f"  CAR+20 range: [{b['car20_min']:+.1f}%, {b['car20_max']:+.1f}%]")
    print(f"  >>> {n_flag(n)} <<<")

    print()
    print_conditioning(conditioning, as_of)
    print(f"\n{CAVEAT}")


# --------------------------------------------------------------- markdown output

def write_md(pb):
    L = [f"# Scenario Playbook -- {pb['as_of']}", "",
         "_If an event of each type occurred today: historical analogs, base rates, "
         "and today's market conditioning. **Conditional on occurrence** -- the "
         "engine does not forecast whether events happen._", "",
         "## Today's conditioning (point-in-time)", ""]
    for c in pb["conditioning"]:
        extra = ""
        if c["amplifier"] == "ON" and c["reg_amp_pp"]:
            extra = (f" -- registered clustered amplification {c['reg_amp_pp']}pp "
                     f"on |CAR+20| (n=20)")
        elif c["amplifier"] == "FAILED":
            extra = " -- fenced off (failed pre-registration)"
        L.append(f"- **{c['hid']} {c['label']}**: **{c['amplifier']}** "
                 f"(latest {c['latest']} vs median {c['median']}){extra}")
    L.append("")

    for card in pb["cards"]:
        et, n, b = card["type"], card["n"], card["base"]
        L += [f"## {et}", "", f"**{n_flag(n)}**", ""]
        if n:
            L += ["| CAR+1 | CAR+5 | CAR+10 | CAR+20 | CAR+20 range |",
                  "|---|---|---|---|---|",
                  f"| {b['car1']:+.1f}% | {b['car5']:+.1f}% | {b['car10']:+.1f}% "
                  f"| {b['car20']:+.1f}% | [{b['car20_min']:+.1f}%, {b['car20_max']:+.1f}%] |",
                  "", "Analogs:", "",
                  "| event | date | CAR+5 | CAR+20 |", "|---|---|---|---|"]
            for a in card["analogs"]:
                L.append(f"| {a['event_id']} | {a['date']} | {a['car5']:+.1f}% "
                         f"| {a['car20']:+.1f}% |")
        else:
            L.append("_No historical analogs of this type in the dataset._")
        L += ["", f"_{CAVEAT}_", ""]
    MD_OUT.write_text("\n".join(L))


def main():
    args = sys.argv[1:]
    pb = build_playbook()

    if args and args[0] == "--all":
        for card in pb["cards"]:
            print_card(card, pb["conditioning"], pb["as_of"])
            print()
        write_md(pb)
        print(f"Wrote {MD_OUT}")
        return

    if len(args) == 1 and args[0] in VALID_TYPES:
        card = next(c for c in pb["cards"] if c["type"] == args[0])
        print_card(card, pb["conditioning"], pb["as_of"])
        return

    print("Usage: python3 src/scenario.py <event_type> | --all")
    print("Event types:", ", ".join(sorted(VALID_TYPES)))


if __name__ == "__main__":
    main()
