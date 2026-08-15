# Red-Team-1 — one-screen summary for Joe

**Bottom line:** the reviewer was right on the science. Answered with computation, not
argument. Every result is published, including the downgrades. Slices R0–R9 are done
and committed one-per-commit; the frozen registered record was never edited. **Three
things need your sign-off** (below) before any *wording* on the public surfaces changes.

---

## What survived vs what downgraded (under one consistent bar)
The bar (now codified, `EVALUATION.md` §0): **validated = SAR-standardized effect +
regime-block-robust CI excluding zero + permutation-FDR.** Applied to everything:

| claim | was | now |
|---|---|---|
| H1 — VIX-stress amplifies the oil ripple | validated | **SUGGESTIVE** |
| copper under a growth regime | validated | **SUGGESTIVE** *(closest miss)* |
| palladium / HY-credit / severity-dose | validated | **SUGGESTIVE** |
| CC2 — supply → gasoline crack | validated | **SUGGESTIVE** |
| CC5 — fertilizer → corn | validated | **SUGGESTIVE** |
| mispricing edge | suggestive | **SUGGESTIVE** (unchanged) |

**→ Under the honest bar, the `validated` set is empty.** The product is now: a sound
*build* + a *measurement instrument* + SUGGESTIVE signals reported with their nulls.

## Why H1 fell (the core of the review)
- Raw headline was **+5.56pp**, but |CAR| is a *volatility* quantity split by a
  *volatility* index. On BMP-standardized returns (the correct metric): **+0.25σ, CI
  includes zero** (R1).
- A **VIX-matched non-event placebo** reproduces the raw +5.56pp — so it's
  vol-clustering, not an event ripple (R2).
- SAR is **null in every regime-block cut** (drop 2008/2020/2026/all) (R3) and the
  effect **shrinks out-of-sample** to +2.92pp with a CI blowing through zero (R5).
- On the *exact frozen N=289 registered corpus*: raw +5.00pp but **SAR +0.16σ, incl. 0**.

## The good news (what's real)
- The **process** is the asset: pre-registration ordering held, nulls reported,
  receipts reconcile (`data/NUMBERS.md`), the DB rebuilds from free sources.
- **No lookahead / no splice problem** (attack 18): the VIX percentile is a trailing
  5-yr rolling rank; no H1 event predates 1991; there was never a VXO splice to worry about.
- The **crude→products value chain** transmission is descriptively strong; CC2/copper
  are the *closest* to real and are honestly labelled SUGGESTIVE, not buried.
- A **published downgrade after adversarial review** is the strongest integrity
  evidence this project can show. That's the headline now.

---

## ⛔ THREE THINGS THAT NEED YOUR SIGN-OFF
1. **Endogenous-response flag list (R4).** 25 events auto-flagged as policy reactions
   to price moves (e.g. 2008/2020 OPEC cuts). The mechanical rule over-flags some
   food/metal/COVID-era events that merely coincide with the 2020 oil crash. Review
   `data/endogenous_flags.json` and tell me which to keep flagged.
2. **Purpose-reframe wording (R8).** Exact proposed text in
   `docs/red_team_1_R8_proposed_wording.md`: (A) calibration = honest, near-baseline,
   no forecast edge; (B) purpose = *measurement & grounding instrument, not a
   predictive-edge product* (drops "before consensus prices it"); (C) provenance
   ($0/keyless/no-fabrication) = *integrity* property, never *correctness*. Approve /
   edit / reject A, B, C.
3. **Final headline wording** (proposed in `docs/red_team_1.md`): "H1 … is not
   supported … under one bar no edge is `validated`; all are SUGGESTIVE." Approve/edit.

*On your sign-off I apply the approved wording verbatim to NORTH_STAR.md / README.md /
surfaces and commit as `R8-apply` + `headline-apply`. Nothing on the public surfaces
changed without your say-so.*

## Build health (honest)
`acceptance.py` reports **DEGRADED**, for **one reason unrelated to this work**:
`engine_status = RED` from **stale/dead free data feeds** (n_dead 5, n_stale 24 —
`fred.SP500`, HY spread, expired Polymarket WTI markets). This RED **pre-dates
red-team-1** (identical at the R4 commit) — it's a data-freshness/ops issue, not a
science issue. Everything red-team-relevant is green: framework_sound ✓, 13 evidence packs
receipted ✓, no-fabrication cage ✓, and the test suite passes except that one
environmental gate (I corrected one test whose "every pack is validated" premise this
review intentionally overturned).
I did **not** paper over the RED — the freshness guard is doing its job; reviving the
feeds is a separate maintenance task (say the word and I'll run `refresh.py`). Test
suite: **150/151 pass; the single failure is `test_st2`, which only asserts
acceptance commissions — i.e. it fails *because of* the environmental engine-RED, not
any red-team change.**

## Receipts
`docs/red_team_1.md` (full disposition) · `data/NUMBERS.md` (every number) ·
`data/h1_sar.json` `placebo_vixmatched.json` `h1_regimeblock.json` `h1_subsets.json`
`h1_frozen_threshold.json` `cc2_seasonal.json` `evidentiary_bar.json` ·
packs in `data/evidence/`. Commits: R0 `4a20599` → R9 `ab8996d`.
