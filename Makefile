SHELL := /bin/bash
PY := python3

.PHONY: reproduce reproduce-central reproduce-ablation test-public test-full verify-submission verify-v3-foundation

# Both public analyses reproduce offline from the committed transparent bundle and fail unless
# every rebuilt artifact matches its frozen SHA-256 manifest.
reproduce: reproduce-central reproduce-ablation

reproduce-central:
	$(PY) src/reproduce_structural_surface.py

reproduce-ablation:
	$(PY) src/reproduce_structural_component_ablation.py

# The slim public tree contains only maintained scientific and release tests, so these targets
# intentionally collect the same complete suite. No historical tests are hidden outside this gate;
# they remain at tag full-research-archive-2026-09-03 with their recorded 1,038-pass receipt.
test-public:
	$(PY) -m pytest -q
	$(PY) src/public_claim_guard.py

test-full:
	$(PY) -m pytest -q

# v3 research foundation (research/v3 branch only). Runs the detector tests, rebuilds the episode
# table and the sensitivity grid, and fails on any drift in the frozen v3 outputs. The blinding
# tests inside it fail on prohibited event-catalogue or price access from the detector.
verify-v3-foundation:
	$(PY) -m pytest -q tests/test_disruption_episodes.py tests/test_disruption_blinding.py \
		tests/test_disruption_provenance.py tests/test_disruption_linkage.py
	$(PY) src/disruption_episodes.py --report
	$(PY) src/disruption_sensitivity.py
	git diff --exit-code -- data/v3/

verify-submission: reproduce test-full
	$(PY) src/public_claim_guard.py
	$(PY) src/verify_submission.py
	$(PY) src/doc_status_guard.py
	$(PY) src/classify_public_product.py
	git diff --exit-code -- docs/audit/FILE_CLASSIFICATION.csv
	test -z "$$(git status --porcelain)" || { git status --short; echo "verification mutated the checkout" >&2; exit 1; }
