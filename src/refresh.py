"""
refresh.py -- ONE command that brings the whole engine up to date.

WHY THIS EXISTS:
The engine has half a dozen little fetchers. Running them by hand, in order,
remembering which one failed -- that is how an engine quietly rots. This is the
single orchestrator. It runs every ingestion step in order, and -- this is the
important part -- it ISOLATES each step: if one fails, the others still run, and
the failure is written down loudly, never swallowed. Silent failure is this
project's historic killer; this file is the answer to it.

Each step runs as its own subprocess (so a crash in one cannot take down the
orchestrator), is timed, and its net rows-written is measured from the database
itself (not by trusting the step's own printout). Every step appends a line to
data/refresh_log.csv and the run ends with a clean summary table.

This script always exits 0 even if steps failed -- the failures are recorded in
the log and it is heartbeat.py's job to raise the alarm. That way the scheduled
`refresh.py && heartbeat.py` still reaches the health check.

Run:  python3 src/refresh.py
"""

import csv
import subprocess
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
LOG = ROOT / "data" / "refresh_log.csv"
PY = sys.executable

STEP_TIMEOUT = 900   # seconds; fetch_cot pulls ~20 zip archives, so be generous

# (step name, script, which table its "rows written" is measured against)
STEPS = [
    ("fetch_prices",   "src/fetch_prices.py",   "prices"),
    ("fetch_series",   "src/fetch_series.py",   "observations"),
    ("fetch_eia",      "src/fetch_eia.py",      "observations"),
    # Physical oil fundamentals (Cushing, refinery utilization, SPR) -- stats-safe.
    ("fetch_eia_fund", "src/fetch_eia_fundamentals.py", "observations"),
    ("fetch_cot",      "src/fetch_cot.py",      "observations"),
    ("fetch_gpr",      "src/fetch_gpr.py",      "observations"),
    # Prediction-market odds (Polymarket, free) -- the priced-probability anchor.
    # DISPLAY/context only; never feeds the registered statistics.
    ("fetch_predmkt",  "src/fetch_predmkt.py",  "observations"),
    # IMF PortWatch chokepoint transits (free) -- the physical-flow modality.
    ("fetch_portwatch", "src/fetch_portwatch.py", "observations"),
    # Wikipedia pageview attention (free) -- the attention modality (context).
    ("fetch_wiki",     "src/fetch_wiki_attention.py", "observations"),
    # NASA FIRMS satellite fire near oil facilities -- overhead/thermal modality.
    # Dormant until FIRMS_KEY is set; skips cleanly otherwise.
    ("fetch_firms",    "src/fetch_firms.py",    "observations"),
    # GDELT DOC coverage tone (free) -- the media-sentiment modality (context).
    ("fetch_gdelt_tone", "src/fetch_gdelt_tone.py", "observations"),
    ("derive_signals", "src/derive_signals.py", "observations"),
    ("load_events",    "src/load_events.py",    "events"),
    # Record keeper: link any situation atom whose source_url now matches a
    # freshly-gated coded event (read-of-events / update-of-log only).
    ("backfill_promo",  "src/backfill_promotions.py", "situation_log"),
    # Synthesis read. Writes engine_read.json/.md (files, not DB rows) -> 0 rows
    # by design; the point is that every refresh ends with a fresh Engine Read.
    ("engine_read",    "src/engine_read.py",    "observations"),
    # regenerate the scenario playbook with today's conditioning (file output).
    ("scenario",       "src/scenario.py --all", "observations"),
    # Situation Memory: attach watcher alerts into per-conflict timelines and
    # render the dossiers. Consumes engine_read.json (must run after it).
    ("situation",      "src/situation.py",      "situation_log"),
    # Corroboration brain: cluster the timeline into events + score confidence by
    # independent-source convergence (weight-of-evidence). File output, 0 DB rows.
    ("corroborate",    "src/corroborate.py",    "observations"),
    # Autonomous analyst (eyes): deterministic divergences between what the
    # engine sees and what the market prices. File output.
    ("divergence",     "src/divergence.py",     "observations"),
    # Strategic-commodity criticality: which critical commodities are under
    # stress because a key producer is in an active situation. File output.
    ("criticality",    "src/criticality.py",    "observations"),
    # Oil/energy propagation graph: which transmission paths (trigger->choke->
    # downstream market) are LIVE given active situations. File output.
    ("propagation",    "src/propagation.py",    "observations"),
    # Risk-vs-priced divergence read: is the oil market pricing the geopolitical
    # risk in the air? (GPR percentile vs Brent-vol percentile). File output.
    ("gpr_signal",     "src/gpr_signal.py",     "observations"),
    # Analogue probability function: kNN over the 511-event seed library -> the
    # historical playbook for each active situation. File output.
    ("analogue",       "src/analogue.py",       "observations"),
    # Calibration loop: log corroboration predictions, gate-confirm, score
    # reliability (Brier) -- calibrates the weights as labels accrue.
    ("calibrate_corr", "src/calibrate_corroboration.py", "observations"),
    # Record keeper: resolve any logged read whose 20-day window has elapsed and
    # score the engine's magnitude calibration (realized - expected).
    ("resolve_reads",   "src/resolve_reads.py",  "reads"),
    # cross-asset propagation map. Writes edge rows (one per event x asset).
    ("cross_asset",    "src/cross_asset.py",    "edges"),
    # TRUE FINAL step: render The Daily so the static front page is always fresh
    # after the pipeline. File output (digest.html), so measured rows is 0.
    ("digest",         "src/digest.py",         "observations"),
]


def table_count(metric):
    """Current row count of the table a step writes to (0 if it doesn't exist yet)."""
    try:
        conn = sqlite3.connect(DB)
        try:
            return conn.execute(f"SELECT COUNT(*) FROM {metric}").fetchone()[0]
        finally:
            conn.close()
    except sqlite3.Error:
        return 0


def run_step(name, script, metric):
    """Run one step in isolation. Returns a result dict; never raises."""
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    before = table_count(metric)
    t0 = time.perf_counter()
    status, detail_err = "OK", ""
    try:
        # script may carry args (e.g. "src/scenario.py --all"); split into argv.
        proc = subprocess.run(
            [PY, *script.split()], cwd=ROOT, capture_output=True, text=True,
            timeout=STEP_TIMEOUT)
        if proc.returncode != 0:
            status = "FAILED"
            # Prefer stderr; fall back to the tail of stdout.
            msg = (proc.stderr or proc.stdout or "").strip()
            detail_err = msg.splitlines()[-1] if msg else f"exit code {proc.returncode}"
    except subprocess.TimeoutExpired:
        status = "FAILED"
        detail_err = f"timeout after {STEP_TIMEOUT}s"
    except Exception as e:                       # e.g. python missing, OS error
        status = "FAILED"
        detail_err = f"{type(e).__name__}: {e}"
    dur = time.perf_counter() - t0
    after = table_count(metric)
    rows = after - before                        # net rows written to the DB

    if status == "OK":
        detail = f"started={started} dur={dur:.1f}s rows_added={rows} ({metric})"
    else:
        detail = f"started={started} dur={dur:.1f}s ERROR: {detail_err[:300]}"
    return {"name": name, "status": status, "dur": dur, "rows": rows,
            "metric": metric, "detail": detail, "err": detail_err}


def main():
    run_id = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"Ripple Engine refresh -- {run_id}")
    print("Running each step in isolation; a failure in one will not stop the rest.\n")

    steps = list(STEPS)
    if "--figures" in sys.argv:          # optional heavy step, off by default
        steps.append(("figures", "src/figures.py", "observations"))

    results = []
    for name, script, metric in steps:
        print(f"  -> {name:<14} ...", end="", flush=True)
        r = run_step(name, script, metric)
        results.append(r)
        if r["status"] == "OK":
            print(f" OK   {r['dur']:>5.1f}s  +{r['rows']} rows")
        else:
            print(f" FAILED  {r['dur']:>5.1f}s  {r['err'][:80]}")

    # --- Append to the log (one row per step; run_id is shared so heartbeat can
    #     find "the last run" as the rows sharing the newest timestamp). ---
    new_file = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp", "step", "status", "detail"])
        for r in results:
            w.writerow([run_id, r["name"], r["status"], r["detail"]])

    # --- Clean end-of-run summary ---
    ok = sum(1 for r in results if r["status"] == "OK")
    failed = len(results) - ok
    print("\n" + "=" * 68)
    print(f"REFRESH SUMMARY   {ok} OK / {failed} FAILED")
    print("=" * 68)
    print(f"  {'step':<15}{'status':<9}{'dur':>7}{'rows':>8}   note")
    print("  " + "-" * 64)
    for r in results:
        note = "" if r["status"] == "OK" else r["err"][:34]
        print(f"  {r['name']:<15}{r['status']:<9}{r['dur']:>6.1f}s{r['rows']:>8}   {note}")
    print("  " + "-" * 64)
    print(f"  Log: {LOG}")
    if failed:
        print(f"  {failed} step(s) FAILED -- heartbeat.py will flag this run.")
    print("\nNext: python3 src/heartbeat.py   (freshness + health check)")

    # Always exit 0 so a chained heartbeat still runs. Failures live in the log.
    sys.exit(0)


if __name__ == "__main__":
    main()
