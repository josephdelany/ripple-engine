> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A claim sweep of the legacy documents, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# Stale and unsupported claims — reverse sweep

*2026-09-03, Session I. **Report only. Nothing here is fixed, and nothing in the seven
documents was edited.** Verified against the live record at run
`walk_20260903T052633Z`.*

## What this sweep did that the citation guard cannot

`src/citation_guard.py` asks: *does this number exist anywhere in the record?* That is a
weak question, and its own report says so — a value in a dozen places resolves to
whichever field happens to round to it. This sweep asks the strong one: **the sentence
names a path; does the value AT THAT PATH still say what the sentence says?**

The difference is not academic. Every row in §2 below is a number the guard scores as
present in the record, because the value exists somewhere. At its own cited path it is
wrong.

Method: for each line carrying a backticked path, resolve that path in the live
`summary.json`, collect every numeric leaf beneath it, and compare against the numbers
printed on the line. Where a number is absent from the live subtree, the same test is run
against `walk_20260903T003422Z` (recovered from `59c5ce2`) to separate *stale* — it was
true of the previous run — from *never located*.

---

## §1 The finding that matters: a published falsification has itself been falsified

**`permutation` — the claim reverses on the new run, and three documents still assert the
old direction.**

| | |
|---|---|
| README.md:143, docs/BRIEF.md:63, docs/PAPER_DRAFT.md:696, :1469 | "the label-permutation test that had rejected 'the engine is noise' at *p* = 0.002 **no longer rejects** (*p* = 0.124)" |
| live `permutation.p_value` | **0.04995** |
| live `permutation.block.p_value` | **0.04995** (the deciding rule, Amendment F.2) |
| live `permutation.iid.p_value` | 0.0589 |
| live `permutation.observed_skill` | −0.0565, not −0.066 |
| live `permutation.block.null_mean` / `null_sd` | −0.1334 / 0.0426, not −0.101 / 0.029 |

At the registered α = 0.05 the deciding block permutation now **rejects**, marginally
(0.04995 < 0.05). The documents state the opposite, and they state it as one of the two
*published falsifications* the project uses to demonstrate its own integrity.

This is not a renumbering. It is a claim that has changed sign, sitting in the paper's
abstract-level narrative in three places. It should be the first thing anyone looks at,
and it needs a human decision — a *p* of 0.04995 against a threshold of 0.05 is not a
result to restate confidently in either direction.

---

## §2 Stale magnitudes at a named path — the paper's receipts table

`docs/PAPER_DRAFT.md` lines ~1455–1476 is a Number → Path table. **It has been partially
updated: the G-vs-climatology and G-vs-persistence rows, leakage, RPS and the filtration
audit are current; the rest are on the previous run.** A half-updated receipts table is
more dangerous than a wholly stale one, because it looks maintained.

| line | the table says | live value at the cited path | path |
|---:|---|---|---|
| 1457 | 253 scored; block 2.32 | **246** scored; mean_block **2.3** | `tiers.daily.*` |
| 1460 | G vs random −0.021 *p* 0.58; vs frozen +0.007 *p* 0.029 | **−0.0156** *p* **0.730**; **+0.0372** *p* **0.0006** | `tiers.daily.G.engine_vs` |
| 1461 | G SPA p_RC **1.00**, p_SPA 0.65 | p_rc **0.564**; family SPA *p* **0.341** | `tiers.daily.G.spa` |
| 1463 | P CRPS −0.071 [−0.136, −0.017] *p* 0.016 | **−0.0738 [−0.1404, −0.0210]** *p* **0.0106** | `tiers.daily.P.engine_vs` |
| 1463 | persistence +0.129; random −0.005; frozen +0.007 | **+0.1337**; **−0.0066**; **+0.0105** | `tiers.daily.P.engine_vs` |
| 1464 | M precision 0.337 / recall 0.544 / base 0.225 | **0.315 / 0.500 / 0.228** | `tiers.daily.M.engine` |
| 1465 | M13 −0.700 [−0.940, −0.457] *p* < 0.001 | **−0.171 [−0.306, −0.019]** *p* **0.042** | `...items_vs_climatology.M13_recalibrated` |
| 1466 | Power: G **0.127** @80% | mds **0.0908**, power_at_mds **0.81** | `tiers.daily.power` |
| 1467 | Spec curve min −0.150, median −0.075, max −0.041 | **−0.1424 / −0.0769 / −0.0497** | `spec_curve.skill_distribution` |
| 1468 | Placebo −0.047 [−0.083, −0.008] | **−0.0675**; estimator is now `source_event_cluster` (Amendment N), *n* 416 | `placebo.*` |
| 1469 | Permutation observed −0.066, mean −0.101, SD 0.029, block *p* 0.124, iid 0.092 | **−0.0565 / −0.1334 / 0.0426 / 0.0500 / 0.0589** | `permutation` |
| 1470 | FDR: 34 comparisons, **31** survive | 34 comparisons, **29** survive | `fdr.family` |

**M13 deserves separate attention.** The table says −0.700 with *p* < 0.001. It is now
**−0.171 with *p* = 0.042** — a quarter of the magnitude, and a *p* that has crossed from
"overwhelming" to "marginal". The prose describing recalibration as decisively falsified
rests on the old figure.

Rows verified as **current**, for completeness: G Brier −0.084 [−0.175, +0.004] *p* 0.076,
means 0.710 / 0.655, *n* 100; G vs persistence −0.304 [−0.821, −0.030] *p* 0.025, ref mean
0.545, 50 fallbacks / 96 known; G RPS clim −0.003, random +0.056, persistence −0.175;
leakage G 0.710 → 0.597, P 8.30 → 8.00; filtration audit 15,241 checks (the six
`filtration_audit.checks` counters do sum to 15,241).

---

## §3 Stale prose outside the table

**README.md:141–147 — the Amendment L / "NO ADDITION" paragraph is on the old run.**
`data/walk_forward/delta_experiment.json` now carries `derived_from_run`
`walk_20260903T052633Z`, and its numbers moved:

| README says | live in `delta_experiment.json` |
|---|---|
| "+0.034 Brier skill" | `vs_no_change.brier.C1_fixed_0.5.skill` = **+0.0505** |
| "DM *p* = 0.181" | `...C1_fixed_0.5.dm_p` = **0.243** |
| "not detectable at *n* = 150" | `...C1_fixed_0.5.n` = **89** |
| "scores 0.4626 against 0.4643" | `scores.C1_fixed_0.5.brier` = **0.4693**; `scores.climatology.brier` = **0.4905** |
| "moves the mixture from 0.682 to 0.506 against persistence's 0.494" | `scores.no_change.brier` = **0.4942** ✓; the 0.506 figure does not match any `scores.*.brier` |

The registered verdict label itself — **NO ADDITION** — is unchanged in the object, so the
*conclusion* survives; every number supporting it does not.

**docs/BRIEF.md is current** at its headline table (−0.084 / −0.304 / +0.134, run stamped,
*n* = 100) and is the only one of the seven that stamps its run in the document. That is
the pattern the others should copy.

---

## §4 No locatable source

- **`docs/ARCHITECTURE.md` does not exist.** It is named in this sweep's brief; there is
  no such file in the tree. Either it was never written or it has been renamed, and
  anything citing it cites nothing.
- **`docs/EXPLAIN.md` carries 11 numeric claims and cites no data path at all** — zero
  backticked file or JSON references in the document. It is spoken-word material, so this
  may be intentional, but it means nothing in it is checkable and its numbers cannot be
  swept. It currently repeats "262 of my 313 events" and the pool figures, which are
  affected by the Amendment 4 rebuild.
- **`docs/HOW_TO_TALK_ABOUT_IT.md` carries ~36 numeric claims behind a single backticked
  path.** Same exposure.
- **`docs/OIL_FINDINGS.md` carries ~91 numeric claims behind 8 paths.** Not swept in
  detail here — see §6.

---

## §5 Asserted as tested, without an interval or a multiplicity correction

- `docs/OIL_FINDINGS.md:37` — "significant across three light-end products." No interval,
  no *p*, no multiplicity correction on the line, and "three products" is itself a family.
  **Not verified against `data/ripple/irf.json` in this pass** — flagged for a reader, not
  asserted as wrong.
- `docs/PAPER_DRAFT.md:1473` — the receipts row "H1 +5.56pp and its placebo downgrade"
  cites `docs/red_team_1.md`, a prose document, not a data object. A magnitude whose
  receipt is another narrative document cannot be checked by any automated guard.
- `docs/PAPER_DRAFT.md:1453` — the spine-audit row cites `data/spine/AUDIT.md`, likewise a
  document rather than data.

`docs/HOW_TO_TALK_ABOUT_IT.md:71` — "on price the engine *is* significantly worse than the
base rate" — **checks out**: `tiers.daily.P.engine_vs.climatology` is −0.0738,
CI [−0.1404, −0.0210], excluding zero.

---

## §6 What this sweep did not cover, stated so the gaps are not mistaken for clean bills

- Only lines carrying a **backticked path** were path-checked. A stale number in a
  sentence that names no source is invisible to this method, by construction — which is
  most of `EXPLAIN.md` and `HOW_TO_TALK_ABOUT_IT.md`.
- Claims resolving to `data/ripple/irf.json`, `data/big_moves/*`, `data/spine/AUDIT.md`,
  `oil.db` and `data/candidates/*.csv` were **not** re-verified; only `summary.json` and
  `delta_experiment.json` paths were.
- `docs/OIL_FINDINGS.md` was counted, not swept line by line.
- Two rows resolved with `{a,b}` brace alternation in their path
  (`tiers.daily.G.engine_vs.{random_analogs,frozen}`,
  `tiers.daily.{G,P}.diagnostic_fair`); I resolved those by hand rather than by tool, so
  they carry the same confidence as the rest of §2 but not the same mechanism.
- **This is a report by one session reading one run.** It has not been independently
  checked, and §1 in particular turns on a *p*-value of 0.04995 against a threshold of
  0.05, which is exactly the kind of margin that should not be settled by one reader.

---

*Written by Session I. Nothing in the seven documents was edited. `docs/sweep/` is a new
directory; this file is its only occupant.*
