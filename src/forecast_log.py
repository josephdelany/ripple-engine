"""
forecast_log.py -- the ACCOUNTABILITY layer. Log forecasts, score them honestly.

THE POINT (read this):
Measuring the past is easy; being right about the future is the only thing that
matters, and the only way to know if you are is to WRITE DOWN a probability
BEFORE the event and score it afterwards. This tool does exactly that and nothing
more. It does not predict for you. It records YOUR judgment, benchmarks it against
the market's implied odds (Kalshi), and keeps a Brier-scored track record so you
cannot fool yourself about your own accuracy.

A forecast without stated reasoning is not loggable here -- "I felt like it" is
not a track record. The notes field is mandatory.

Uses the EXISTING `forecasts` table (see init_db.py) -- no new tables, no schema
changes. made_at / resolved_at give every row provenance.

Usage:
  python3 src/forecast_log.py add               # interactive: log a new forecast
  python3 src/forecast_log.py resolve <id> <0|1># record what actually happened
  python3 src/forecast_log.py score             # the scored track record
"""

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# Same-directory import; works because sys.path[0] is src/ when run as a script.
from fetch_kalshi import market_price

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ask(prompt):
    """Prompt and return the stripped input."""
    return input(prompt).strip()


def ask_required(prompt):
    """Prompt until the user gives a non-empty answer (used for the mandatory fields)."""
    while True:
        v = ask(prompt)
        if v:
            return v
        print("  -- required. Please enter a value (or Ctrl+C to abort).")


def ask_prob(prompt):
    """Prompt for a probability in [0, 1], re-asking until it's valid."""
    while True:
        raw = ask(prompt)
        try:
            p = float(raw)
        except ValueError:
            print("  -- enter a number between 0 and 1 (e.g. 0.35).")
            continue
        if 0.0 <= p <= 1.0:
            return p
        print("  -- probability must be between 0 and 1.")


def cmd_add():
    """Interactively log one forecast."""
    print("Log a new forecast. Ctrl+C to abort; nothing is saved until the end.\n")
    question = ask_required("Question (what are you forecasting?): ")
    horizon = ask_required("Resolve-by date or horizon (e.g. 2026-12-31): ")
    my_prob = ask_prob("YOUR probability it happens (0-1): ")

    ticker = ask("Kalshi ticker to benchmark against (optional, Enter to skip): ")
    market_prob, market_source = None, None
    if ticker:
        market_source = ticker
        try:
            market_prob = market_price(ticker)
        except Exception as e:  # network/HTTP issues shouldn't lose the forecast
            print(f"  -- couldn't reach Kalshi ({type(e).__name__}); "
                  f"saving the ticker with no market price.")
        if market_prob is None:
            print("  -- no live price for that ticker (illiquid or wrong ticker); "
                  "saved with market_prob blank.")
        else:
            print(f"  -- Kalshi implied probability: {market_prob:.2%}")

    # Reasoning is MANDATORY: a forecast you can't justify is not a track record.
    notes = ask_required("Your REASONING (required -- why this probability?): ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO forecasts "
        "(made_at, question, horizon, my_prob, market_prob, market_source, "
        " resolved_at, outcome, notes) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (now_iso(), question, horizon, my_prob, market_prob, market_source,
         None, None, notes),
    )
    conn.commit()
    fid = cur.lastrowid
    conn.close()
    print(f"\nLogged forecast #{fid}. Resolve it later with: "
          f"python3 src/forecast_log.py resolve {fid} <0|1>")


def cmd_resolve(args):
    """Record the real outcome of a forecast."""
    if len(args) != 2:
        print("Usage: python3 src/forecast_log.py resolve <id> <0|1>")
        return
    try:
        fid, outcome = int(args[0]), int(args[1])
    except ValueError:
        print("  id must be an integer and outcome must be 0 or 1.")
        return
    if outcome not in (0, 1):
        print("  outcome must be 0 (did not happen) or 1 (happened).")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    row = cur.execute("SELECT question, resolved_at FROM forecasts "
                      "WHERE forecast_id = ?", (fid,)).fetchone()
    if row is None:
        print(f"  no forecast with id {fid}.")
        conn.close()
        return
    if row[1] is not None:
        print(f"  note: forecast #{fid} was already resolved at {row[1]}; updating it.")
    cur.execute("UPDATE forecasts SET outcome = ?, resolved_at = ? "
                "WHERE forecast_id = ?", (outcome, now_iso(), fid))
    conn.commit()
    conn.close()
    print(f"Resolved #{fid} ({row[0][:60]}) as outcome={outcome}.")


def brier(prob, outcome):
    """Brier score for a single binary forecast: lower is better, 0 is perfect."""
    return (prob - outcome) ** 2


def cmd_score():
    """Print the full log and, for resolved forecasts, the Brier scoreboard."""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT forecast_id, made_at, question, horizon, my_prob, market_prob, "
        "       outcome FROM forecasts ORDER BY forecast_id").fetchall()
    conn.close()

    if not rows:
        print("The forecast log is empty. Make the first one:\n"
              "  python3 src/forecast_log.py add")
        return

    print("=" * 100)
    print("FORECAST LOG")
    print("=" * 100)
    hdr = (f"{'id':>3}  {'made':<11}{'question':<40}"
           f"{'mine':>6}{'market':>8}{'out':>5}{'brier':>8}")
    print(hdr)
    print("-" * 100)
    resolved = []
    for fid, made_at, q, horizon, my_prob, market_prob, outcome in rows:
        made = (made_at or "")[:10]
        mp = f"{market_prob:.2f}" if market_prob is not None else "  -"
        if outcome is None:
            out_s, br_s = "  -", "pending"
        else:
            out_s = str(outcome)
            br_s = f"{brier(my_prob, outcome):.3f}"
            resolved.append((my_prob, market_prob, outcome))
        print(f"{fid:>3}  {made:<11}{(q or '')[:39]:<40}"
              f"{my_prob:>6.2f}{mp:>8}{out_s:>5}{br_s:>8}")

    print("-" * 100)
    if not resolved:
        print("\nNothing resolved yet, so there is no score to report. That is normal --\n"
              "track records take calendar time. Resolve forecasts as their dates arrive:\n"
              "  python3 src/forecast_log.py resolve <id> <0|1>")
        return

    # --- The scoreboard: your Brier vs the market vs the naive 0.5 baseline ---
    n = len(resolved)
    my_mean = sum(brier(p, o) for p, _, o in resolved) / n
    # The market is only a fair benchmark on questions where it actually had a price.
    market_pairs = [(mp, o) for _, mp, o in resolved if mp is not None]
    naive_mean = sum(brier(0.5, o) for _, _, o in resolved) / n  # = 0.25 always

    print(f"\nBRIER SCOREBOARD  (lower is better; 0 = perfect, 0.25 = a coin flip)")
    print(f"  resolved forecasts:            {n}")
    print(f"  YOUR mean Brier:               {my_mean:.3f}")
    if market_pairs:
        market_mean = sum(brier(mp, o) for mp, o in market_pairs) / len(market_pairs)
        print(f"  market mean Brier (n={len(market_pairs):<2}):        {market_mean:.3f}"
              f"   <- same questions, where Kalshi had a price")
        edge = market_mean - my_mean
        verdict = "you beat the market" if edge > 0 else \
                  "the market beat you" if edge < 0 else "dead level with the market"
        print(f"  -> {verdict} by {abs(edge):.3f} Brier on those questions")
    else:
        print(f"  market mean Brier:             n/a  (no resolved forecast had a Kalshi price)")
    print(f"  naive 0.5 baseline:            {naive_mean:.3f}")
    print(f"\n  Beating 0.25 means you carry information. Beating the market column\n"
          f"  is the harder, realer test -- and only meaningful once n is large.")


USAGE = ("Usage:\n"
         "  python3 src/forecast_log.py add\n"
         "  python3 src/forecast_log.py resolve <id> <0|1>\n"
         "  python3 src/forecast_log.py score")


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "add":
        cmd_add()
    elif cmd == "resolve":
        cmd_resolve(rest)
    elif cmd == "score":
        cmd_score()
    else:
        print(f"Unknown command '{cmd}'.\n{USAGE}")


if __name__ == "__main__":
    main()
