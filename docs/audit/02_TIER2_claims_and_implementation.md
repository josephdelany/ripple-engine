# Tier 2 — Published claims that fail, and implementation choices that weaken inference

---

## B1 — The anticipation finding is mostly definitional

**Claimed.** Median 31-day lag; *"in half of attributed Brent episodes every attributed event was
already public more than 20 trading days before the move began."*

**Defect.** `src/big_moves.py:92` sets `onset = win.idxmin() if up else win.idxmax()` — **the onset
is the price extreme, selected ex post**, so it precedes everything in the episode by construction.
Line 185 flags `anticipated` when an event falls >20 days after that onset.

**Measured.** Median episode duration **76 days**; **100% of episodes exceed 20 days**. A uniform
within-episode null yields **55% flagged anticipated by construction**. Observed: **69%** of 77.

**Verdict.** Excess ≈2.5σ on a crude unclustered test. **Withdraw as published.** Restate as a
modest excess over the mechanical baseline, or test properly (see R6).

---

## B2 — Red Sea / Hormuz has no control and the pre-trend runs against it

**Claimed.** Flow −56.6%, reroutes +101.8%, Brent −4.9% ⇒ *"a reroutable closure is a freight event."*

**Measured from the project's own price table.** Brent fell **−14.8% during Q4 2023, before the
attacks** (91.2 → 77.7). Across the attack window itself, Dec 2023 – Mar 2024, Brent **rose +9.5%**
(78.7 → 86.2).

**Verdict.** The −4.9% is a windowing choice against a strongly falling pre-trend driven by demand
weakness and non-OPEC supply. No detrending, no counterfactual, *n* = 2. **Demote to an
illustration with the pre-trend stated in the same sentence.** The mechanism may well be right; the
evidence does not establish it.

---

## B3 — Pass-through asymmetry is a replication presented as a discovery

**Claimed.** *"The strongest and least expected result in the project."*

**Reality.** Asymmetric transmission from crude to products is among the most studied phenomena in
energy economics — Bacon (1991) coined "rockets and feathers"; Borenstein, Cameron & Gilbert (1997,
*QJE*) is canonical; there is a large subsequent literature and multiple meta-analyses.

**Verdict.** The result is real and survives BH-FDR at h = 20 for propane (*q* < 0.0001), Gulf
gasoline (0.0094) and NYH gasoline (0.0266). It is **not new**. Reposition as replication on spot
rather than retail, and state what differs in the specification.

---

## B4 — The model family lacks diversity, weakening Hedge, SPA and the Reality Check

**Where.** `data/walk_forward/menu.json`.

- **M02, M04, M10** weight the `situation` block — **empty for 84% of events**. Substantially inert.
- **M01 / M06 / M07** differ only in *k* (8, 5, 12).
- **M08 / M09** differ only in the retrieval threshold (0.30, 0.50).

**Consequence.** Hedge over near-redundant experts converges to uniform — the sampled sealed read
shows all thirteen weights at exactly **0.076923 = 1/13**. SPA and White's Reality Check have little
power to discriminate within a family this homogeneous. And *"fitting does not beat frozen"*
(+0.0013, *p* = 0.820) is partly a statement about a family with nothing to choose between, not
about learning.

**Fix.** Disclose the family's redundancy where SPA results are reported. A genuinely diverse family
would need structurally different retrieval rules, not parameter variants.

---

## B5 — Vintage is enforced on the situation block but not on revision-prone market series

**Where.** `observations.as_of` equals `obs_date` for the EIA series (crude/distillate/gasoline
stocks, refinery utilisation).

**Problem.** EIA weekly inventories are first published several days *after* the week they describe,
and are subsequently revised. Stamping the observation date as the knowable date assumes the value
was available on the day it describes.

**Why it matters here specifically.** `inv_sigma` is in `MARKET_SERIES` and is one of only **three**
fields in the "physical" block. After Amendment H emptied the situation block, the market block is
what the paper leans on — **so the block presented as clean carries a mild look-ahead of its own.**

**Fix.** Either lag the stocks series by its publication delay, or disclose. Cost: 30 m to disclose.

---

## B6 — Percentile bootstrap intervals on a ratio statistic

**Where.** `src/engine/inference.py:137` `bootstrap_ci` uses percentile intervals; the statistic is
`skill = 1 − engine/ref`, a ratio.

**Problem.** Percentile bootstrap has known coverage problems for skewed statistics, and ratios are
skewed. BCa or a bias-corrected interval would be more accurate.

**Severity.** Low. Unlikely to change a verdict, but a referee will mention it. Disclose or upgrade.
