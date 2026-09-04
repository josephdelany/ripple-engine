> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A status snapshot of the legacy engine. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# State of the engine — v2 after-picture (Situation Engine)

Built per BUILD_V2 (B0→B8), one commit per slice, against RIPPLE_ENGINE_V2_SPEC. Run
`python3 src/acceptance_v2.py` for the live A1–A8 check. Honest status: **6/8 PASS, 2 PARTIAL,
0 FAIL.**

## A1–A8 (verify by running)
- **A1 situation records — PASS.** 313/313 events carry physical+geo blocks, sourced-or-unknown,
  `sr_json` with per-field sources; 20-event spot audit (`data/situation_audit.md`); borderline
  queue for the human gate (`data/borderline_codings.csv`).
- **A2 retrieval — PASS.** `escalation.read` returns ranked analogs + likeness/difference;
  NO ADEQUATE PRECEDENT fires below threshold; 4 unit tests (`tests/test_escalation.py`).
- **A3 scenario tree — PASS.** Conditioned branch rates with n, hierarchical fallback + thin
  flag; historical frequencies only.
- **A4 propagation — PASS.** `propagate.py` per-branch chain hops with n, PRICE vs FLOW, the
  realized-disruption fraction (the "conflict doesn't stop trade" number).
- **A5 walk-forward — PASS.** Two registered windows; escalation conditioning **VALIDATED
  out-of-sample in both** (W1 G-skill +0.043, W2 +0.143); magnitude conditioning an honest
  null. `src/walk_forward.py` → `data/walk_forward/summary.json`; on the Back-test console;
  every Read card stamped.
- **A6 live loop — PARTIAL.** Watcher cadence set to 15 min; intake + `/situation` inline
  decomposition exist; a live autonomous cycle needs the operator to `launchctl load` the
  agent (network). 
- **A7 integrity — PASS.** Every record carries a sources map (sourced-or-unknown); nothing
  fabricated; framework-sound retained (`src/acceptance.py`).
- **A8 deep history — PARTIAL.** 17 sourced 1970–1989 events (Hamilton NBER w16790 / EIA),
  events-only, Joe-gated; short of the ≥60 target — extractor/two-source path open, not padded.

## The instrument now (surfaces, one Apple-cohesive shell / desk.css)
The Read (`/situation_view`) — scenario tree × per-branch propagation + differencing table +
analog set + live overlay + walk-forward stamp. Trace, Terminal (38 series), Back-test
(walk-forward v2 + v1 panels), Question. All in conversation; every number one hop from a
receipt.

## Honest limits (the next pass)
Deepen to ≥60 deep-history events; deepen the differencing beyond the validated conditioners
by coding alliance/diplomatic/target-capacity from sources (currently unknown); run the live
loop to GREEN; grow toward a validated magnitude (P) edge — today it's an honest null.
