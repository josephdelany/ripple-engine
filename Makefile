# Makefile -- D-6 replication target: rebuild data/walk_forward/summary.json from a clean clone.
#
# `make reproduce` runs the FULL registered draws (src/walk.py without --fast: n_boot 2000,
# n_spa_boot 1000, n_perm 1000, random_draws 25, placebo_reps 5 -- REGISTERED in src/walk.py).
#
# THE OFFLINE CHAIN, PRECISELY (see D6_replication.md for the full writeup):
#   data/oil.db is NOT committed (.gitignore: `data/*.db`) and repro.sh's steps 2-7 rebuild it
#   from FRED (keyless but networked), the EIA Open Data v2 API (networked + needs EIA_API_KEY),
#   CFTC COT (networked) and the GPR .xls (networked). src/state/ies90.py -- which src/walk.py's
#   engine/persistence.py calls at read time for the G-persistence baseline -- additionally needs
#   correlatesofwar.org (networked, live in load_war()) and files under data/state/raw/ and
#   data/cache/ that are committed nowhere (both gitignored) and are, per
#   data/gates/release_check_2026-09-02.md §3, partly licence-gated for OTHER loaders in
#   src/state/*.py (ei_review: EI xlsx behind a 403 to scripts; eia_intl: EIA_API_KEY; gsdb: GSDB
#   R5 by request; nyt: NYT_API_KEY; vdem: V-Dem v16 form-served; dots: IMF DOTS refuses scripted
#   pulls). None of that touches ies90/COW/UCDP directly, but it establishes the pattern: this
#   corpus is built from a mix of free-but-networked, keyed and licence-restricted sources, and a
#   clean `git clone` alone reaches none of them.
#
#   What IS committed and offline-only: data/events.csv, data/state/*.csv (situation_log, reads,
#   forecasts -- src/import_state.py refills a rebuilt DB from these), data/walk_forward/menu.json,
#   data/seed/ (data/seed/wtisplc_monthly.txt), data/seed_library/. That is enough to refresh the
#   `events` table on top of an already-built database (stages `db` and `events` below), but not
#   enough to build oil.db itself, and not enough to source the G-persistence baseline's raw
#   inputs.
#
# REPRO_DB=/path/to/oil.db is the documented fallback: an already-built oil.db is copied in as
# data/oil.db (never committed -- .gitignore already excludes it) purely so the WALK STAGE can
# still be timed end to end. If REPRO_DB's own data/ directory has state/raw, cache or state/local
# siblings, those are copied too, because engine/persistence.py's G-persistence baseline calls
# src/state/ies90.py's load_sources() at read time, which needs them; absent, engine/read.py's
# _persistence() catches the failure and every read falls back to climatology (n_persistence_fallback
# counted, never silent) -- honest, but not a faithful timing/output match to a run that had them.
#
# Safety: refuses to run if the working tree has uncommitted changes to tracked files (a shared
# tree in use is always dirty; a fresh clone is clean), unless REPRO_FORCE=1 -- so this is never
# fired by accident against a shared working tree's ledger. reads.jsonl is committed and
# append-only (see the top of src/walk.py): in a clean clone the walk appends a sixth run's
# records beside the five committed ones; that is expected, and tests/test_reproduce.py matches
# the new run's reads to the committed run by (tier, event_id), not by position.

SHELL := /bin/bash
REPRO_DB ?=
REPRO_FORCE ?= 0
PY := python3

.PHONY: reproduce reproduce-central test-public test-full verify-submission

# Authoritative public-product reproducer. This target is offline and uses only the committed,
# transparent input bundle. It must reproduce the three frozen scientific artifacts byte-for-byte.
reproduce-central:
	$(PY) src/reproduce_structural_surface.py

# The maintained fast public-product check. The complete research suite remains available with
# `python3 -m pytest -q` and includes loaders and guards for superseded publications.
test-public:
	$(PY) -m pytest -q tests/test_structural_surface_experiment.py tests/test_structural_surface_demo.py tests/test_public_claim_guard.py tests/test_verify_submission.py
	$(PY) src/public_claim_guard.py

# Complete repository suite; this and plain `pytest -q` are the release gate.
test-full:
	$(PY) -m pytest -q

verify-submission: reproduce-central test-full
	$(PY) src/public_claim_guard.py
	$(PY) src/verify_submission.py
	$(PY) src/classify_public_product.py
	git diff --exit-code -- docs/audit/FILE_CLASSIFICATION.csv

reproduce:
	@set -euo pipefail; \
	TOTAL_START=$$(date +%s); \
	echo "==== guard ===="; \
	if [ "$(REPRO_FORCE)" != "1" ] && [ -n "$$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then \
		echo "REFUSING: this working tree has uncommitted changes to tracked files -- it looks like a" >&2; \
		echo "shared/main tree in use, not a fresh clone. The walk appends to the sealed ledger" >&2; \
		echo "data/walk_forward/reads.jsonl. Re-run in a clean 'git clone', or pass REPRO_FORCE=1" >&2; \
		echo "if you are certain this tree is disposable." >&2; \
		exit 1; \
	fi; \
	echo "guard: ok"; \
	echo; echo "==== stage 0/3: schema (init_db, offline, idempotent) ===="; \
	T0=$$(date +%s); \
	$(PY) src/init_db.py; \
	echo "stage 0/3 (init_db): $$(( $$(date +%s) - T0 ))s"; \
	echo; echo "==== stage 1/3: database ===="; \
	T0=$$(date +%s); \
	if [ -z "$(REPRO_DB)" ]; then \
		echo "REPRO_DB not set: data/oil.db is not committed and the full repro.sh chain needs" >&2; \
		echo "network access (FRED/EIA/CFTC/GPR), an EIA_API_KEY, and (for the G-persistence" >&2; \
		echo "baseline) correlatesofwar.org plus data/state/raw/ + data/cache/, none of which a" >&2; \
		echo "clean clone has. Re-run with REPRO_DB=/path/to/an/already-built/oil.db to time the" >&2; \
		echo "walk stage against a real database (documented fallback; see header of this file)." >&2; \
		exit 1; \
	fi; \
	test -f "$(REPRO_DB)" || { echo "ERROR: REPRO_DB=$(REPRO_DB) does not exist" >&2; exit 1; }; \
	mkdir -p data; \
	cp "$(REPRO_DB)" data/oil.db; \
	echo "copied $(REPRO_DB) -> data/oil.db ($$(du -h data/oil.db | cut -f1))"; \
	SRC_DATA=$$(cd "$$(dirname "$(REPRO_DB)")" && pwd); \
	for d in state/raw cache state/local; do \
		if [ -e "$$SRC_DATA/$$d" ] && [ ! -e "data/$$d" ]; then \
			echo "also copying $$d/ (offline source cache for engine/persistence.py's G-persistence baseline)"; \
			mkdir -p "data/$$(dirname $$d)"; \
			cp -R "$$SRC_DATA/$$d" "data/$$d"; \
		fi; \
	done; \
	echo "stage 1/3 (database): $$(( $$(date +%s) - T0 ))s"; \
	echo; echo "==== stage 2/3: events (load_events.py + import_state.py; offline, committed CSVs only) ===="; \
	T0=$$(date +%s); \
	$(PY) src/load_events.py; \
	$(PY) src/import_state.py; \
	echo "stage 2/3 (events): $$(( $$(date +%s) - T0 ))s"; \
	echo; echo "==== stage 3/3: the walk (src/walk.py, FULL registered draws -- no --fast) ===="; \
	T0=$$(date +%s); \
	$(PY) src/walk.py; \
	echo "stage 3/3 (walk): $$(( $$(date +%s) - T0 ))s"; \
	echo; echo "==== reproduce: total $$(( $$(date +%s) - TOTAL_START ))s ===="; \
	echo "data/walk_forward/summary.json written"
