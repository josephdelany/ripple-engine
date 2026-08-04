#!/usr/bin/env bash
# repro.sh -- rebuild data/oil.db FROM ZERO, with a plain echo of every step.
#
# From a fresh clone this reconstructs the whole database: schema, every free
# data fetch, the human-approved event corpus, the derived signals, and the
# analyses -- in the one order that works. Every number in every paper is
# reproducible by running this against the committed inputs.
#
# It builds oil.db relative to the current directory, so it can be run in a
# scratch copy of the repo without touching the real database (that is how its
# own receipt, data/repro_log.txt, is produced).
#
# Usage:  bash repro.sh
set -e
step() { echo; echo "==== $* ===="; }

step "1/22  schema (init_db)";            python3 src/init_db.py
step "2/22  Brent & WTI prices (FRED)";   python3 src/fetch_prices.py
step "3/22  macro series (FRED)";         python3 src/fetch_series.py
step "4/22  value chain (V1: fuels/petchem/fertilizer PPIs, TTF, JKM)"; python3 src/fetch_value_chain.py
step "5/22  EIA crude inventories";       python3 src/fetch_eia.py
step "6/22  CFTC Commitment of Traders";  python3 src/fetch_cot.py
step "7/22  Geopolitical Risk index";     python3 src/fetch_gpr.py
step "8/22  event corpus (load_events)";  python3 src/load_events.py
step "8b/22 restore durable memory";      python3 src/import_state.py
step "9/22  quiet comparison set";        python3 src/load_quiet.py
step "10/22 derived signals (incl. V1 cracks)"; python3 src/derive_signals.py
step "11/22 event study";                 python3 src/event_study.py
step "12/22 conditioned study";           python3 src/conditioned_study.py
step "13/22 robustness";                  python3 src/robustness.py
step "14/22 cross-asset edges";           python3 src/cross_asset.py
step "15/22 value-chain CHAIN VIEW (V1)";  python3 src/chain_view.py
step "16/22 cross-chain battery (V3)";     python3 src/cross_chain.py
step "17/22 data dictionary";             python3 src/data_dictionary.py
# V-Q rigor lenses (additive; reproduce the H1 robustness receipts from Brent/VIX/events above).
step "18/22 H1 spec curve (V-Q2)";        python3 src/spec_curve.py
step "19/22 H1 influence (V-Q3)";         python3 src/influence.py
step "20/22 H1 temporal hold-out (V-Q4)"; python3 src/holdout.py
step "21/22 quarterly calibration (V-Q4)";python3 src/calibration_report.py
step "22/22 vintage check (V-Q1)";        python3 src/vintage_check.py

echo; echo "==== repro complete: data/oil.db rebuilt from zero ===="
