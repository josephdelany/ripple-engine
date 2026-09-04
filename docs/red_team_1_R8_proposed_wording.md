> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A working analysis or evidence record from the legacy engine. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# R8 — purpose reframe: PROPOSED wording (⛔ AWAITING JOE'S SIGN-OFF)

*Red-team-1 slice R8 (attacks 11, 12, 19) is a **wording** change and a declared
sign-off gate. Nothing in this file is applied to NORTH_STAR.md, README.md, or the
surfaces yet. It is the exact proposed text for Joe to approve, edit, or reject.
The numbers below are computed and final; only the framing awaits sign-off.*

The three factual anchors (already published, receipted):
- **No demonstrated forecast edge.** Calibration on the resolved gap ledger: n=247,
  Brier **0.2466** vs base **0.2495** → skill **0.0029** (≈1.2% relative), resolution
  **0.0042**. Indistinguishable from the base rate. (`EVALUATION.md` §3/§7.)
- **In-sample amplification is not predictive.** The miss-audit's worst gaps are all
  `regime_misread` on the same high-VIX events that drove the raw H1 number
  (`EVALUATION.md` §5; now cited in `data/evidence/hyp.H1.json`).
- **H1 and the whole validated set downgrade to SUGGESTIVE** under the one bar (R7).

---

## Proposal A — calibration framing (attack 11)
Wherever calibration is described, present it as **honest and near-baseline, with no
demonstrated forecast edge**, not as evidence of skill.

> **Calibration (honest, near-baseline).** Over 247 resolved gaps the engine scores
> Brier 0.2466 against a base rate of 0.2495 — a skill of 0.0029, statistically
> indistinguishable from zero, with resolution 0.0042 (it mostly emits 0.4 or 0.6).
> **The engine has no demonstrated forecasting edge.** It is calibrated and honest
> about that; measuring and grounding, not predicting, is its job.

## Proposal B — purpose statement (attack 11), for NORTH_STAR.md §1–§2 and README top
Reframe the engine as a **measurement and grounding instrument**, not a
predictive-edge product.

> **What this is.** A measurement-and-grounding instrument: it establishes *what
> happened* (a sourced, point-in-time event corpus), *what history says* (conditioned
> event-study distributions with honest CIs), and *what state we are in* (regime
> reads carrying their own uncertainty). It is **not** a predictive-edge product and
> makes no claim to forecast markets ahead of consensus. Its value is disciplined
> measurement, reproducibility, and a live, auditable track record — including its
> nulls and its post-review downgrades.

*(Replaces any "understand a market shift **before consensus prices it**" framing,
which the calibration does not support.)*

## Proposal C — provenance reframe (attack 19)
Everywhere `$0` / keyless / no-fabrication appears as if it were scientific virtue,
reframe it as an **integrity property**, never as evidence of correctness.

> **On provenance.** "$0 / keyless / no-fabrication" is an **integrity guarantee** —
> every number is one hop from a real, timestamped source and nothing is invented. It
> says the pipeline is *honest and reproducible*. It does **not** make any finding
> *correct*: a faithfully-computed number can still be wrong (see the red-team-1
> downgrades). Provenance and correctness are separate axes; we claim only the first.

---

### Files these edits would touch (on approval)
- `NORTH_STAR.md` §1 "THE GOAL" / §2 "DONE WELL" — Proposal B, and soften the
  "before consensus prices it" promise.
- `ripple-engine/README.md` — "The headline finding" + intro — Proposals A/B/C.
- `ripple-engine/EVALUATION.md` — calibration sections already factual; add Proposal
  A's one-line framing (via `evaluate.py`).
- Surfaces (`surface/the_brief.html` copy, `SURFACES.md`) — provenance reframe (C).

**Joe: approve / edit / reject each of A, B, C. On sign-off I apply them verbatim and
commit as `R8-apply`.**
