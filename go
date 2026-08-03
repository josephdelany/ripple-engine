#!/usr/bin/env bash
#
# go -- the one-command launcher. Bring the whole engine up.
#
#   ./go            rebuild the reads, open the daily digest, start the cockpit on :5050
#   ./go --refresh  also pull fresh data first (network), then the above
#   ./go --build    rebuild the reads + digest only, no server (for cron / a quick refresh)
#
# Everything is local and free. Ctrl+C stops the cockpit.

cd "$(dirname "$0")" || exit 1

if [ "$1" = "--refresh" ]; then
  echo "==> refreshing data (free feeds; network)…"
  python3 src/refresh.py || echo "   (refresh had issues; continuing with cached data)"
  shift
fi

echo "==> rebuilding the reads from data/oil.db…"
# order matters: claims -> state read -> corroboration -> ripple map -> graph -> supply-chain ->
# apt conditioning -> gaps -> resolving record -> registry -> the so-what wire -> the digest.
STEPS=(
  "validate.py claims"
  "engine_read.py"
  "corroborate.py"
  "cross_asset_conditioned.py"
  "propagation_graph.py"
  "supply_chain.py"
  "domain_conditioning.py"
  "gaps.py"
  "edge_battery.py"
  "read_backtest.py"
  "signal_registry.py"
  "sowhat.py"
  "holdout.py"
  "calibration_report.py"
  "evaluate.py"
  "evidence.py"
  "coverage.py"
  "status.py"
)
for s in "${STEPS[@]}"; do
  if python3 src/$s >/dev/null 2>&1; then echo "   ok  $s"; else echo "   WARN  $s (skipped)"; fi
done
python3 src/digest.py >/dev/null 2>&1 && echo "   ok  digest.py"

if [ "$1" = "--build" ]; then
  echo "==> build complete (no server). data/digest.html + data/*.json refreshed."
  exit 0
fi

echo "==> opening the daily read…"
open data/digest.html 2>/dev/null || echo "   (open data/digest.html in your browser)"

echo "==> starting the cockpit at http://127.0.0.1:5050  (connect it in OpenBB Workspace; Ctrl+C to stop)"
exec python3 src/backend.py
