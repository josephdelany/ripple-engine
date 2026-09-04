> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-3 — Multiplicity review

Repo: `ripple-engine`, branch `v2-day1`, HEAD `b7c8ec1`. `src/walk.py` and `src/engine/*.py` are dirty
in the working tree; all code line numbers below are from `git show HEAD:...` (committed) versions,
saved to scratch as `walk_HEAD.py` / `inference_HEAD.py`. `data/walk_forward/summary.json` is **not**
modified in the working tree (`git status` does not list it) — it is identical to the committed HEAD
copy, and it is the file `README.md` and both gate reports cite (run `walk_20260902T182828Z`). All
counts below are from executed `python3`, scripts kept in this scratchpad
(`d3_analysis.py`, `d3_pcollect.py`, `d3_correct.py`, `d3_autocorr.py`).

`data/walk_forward/menu.json` **is** dirty (working tree has a 13th item, `M13_recalibrated`, from
Amendment C / Brief B-2 — not yet run). The committed HEAD menu.json has 12 items and matches
`summary.json.menu` exactly, so the run this report audits used 12 menu items, not 13.

---

## 1. Multiplicity count

### 1a. What actually exists in `summary.json` (executed, not by hand)

```
menu items (summary.json.menu):        12   (M01..M12; M13 exists uncommitted in menu.json, unrun)
tiers:                                   2   (monthly, daily) — monthly: 0 scored (burn-in never reached)
G score variants reported:               4   (brier[gate], log, rps, deal-binary-brier)
P score variants reported:               6   (crps[gate], pin10, pin50, pin90, sign_accuracy, PIT)
G baselines PRESENT in this run:         3   (climatology, frozen, random_analogs — persistence
                                               baseline code (Amendment B / commit b7c8ec1, HEAD) was
                                               committed AFTER this run; summary.json predates it,
                                               see §2 finding)
P baselines PRESENT in this run:         4   (climatology, persistence, random_analogs, frozen)
per-class comparisons (daily only):      7 classes × 2 tasks (G,P) = 14   (vs climatology, primary score)
regime blocks:                           3   (drop_2008, drop_2020, drop_2026)
spec-curve grid cells (n_specs):       162   (summary.json.spec_curve.n_specs, executed count)
placebo variants:                        3   (vs_random_analogs=registered null/size-matched,
                                               vs_climatology=diagnostic, fair_vs_climatology=diagnostic)
SPA joint tests:                         3   (G.spa, G.spa_vs_persistence, P.spa — each ALREADY a
                                               multiplicity-corrected test over 14 models, not a raw p)
global label-permutation test:           1   (joint across tiers, G only)
```

### 1b. Registered primary family — what decides the verdict (§7)

The code that assembles the FDR family (`walk.py`, committed HEAD, function `summarize_tier`):

```
513   fam_p, fam_labels = [], []
514   for task, key, refs in (("G", "brier", (...4 refs...)), ("P", "crps", (...4 refs...))):
517       for ref in refs:
518           rows = _paired(sc, task, key, "engine", ref)
519           blk["engine_vs"][ref] = _skill_block(rows, task, key, "engine", ref, mb, n_boot, max(lag, 0))
520           if blk["engine_vs"][ref].get("dm_p") is not None:
521               fam_p.append(blk["engine_vs"][ref]["dm_p"]); fam_labels.append(f"{tier}:{task}:engine_vs_{ref}")
525       for iid in item_ids:
526           rows = _paired(sc, task, key, iid, "climatology")
528           if blk["items_vs_climatology"][iid].get("dm_p") is not None:
529               fam_p.append(...); fam_labels.append(f"{tier}:{task}:{iid}_vs_climatology")
576   out["family_p"] = {"labels": fam_labels, "p": fam_p}
```
Aggregated across tiers and BH-corrected at `run()`:
```
1093  fam_p, fam_l = [], []
1094  for t in summary["tiers"].values():
1095      fam_p += t["family_p"]["p"]; fam_l += t["family_p"]["labels"]
1096  bh = INF.bh_fdr(fam_p, q=0.05)
1097  summary["fdr"] = {"q": 0.05, "family": [...]}
```
**The family is: engine-vs-each-present-baseline, and each menu item vs climatology, on the primary
registered score ONLY (Brier for G, CRPS for P), for every tier that has scored reads.** Executed:
daily:G contributes 3 baseline + 12 item = 15; daily:P contributes 4 baseline + 12 item = 16;
monthly contributes 0 (0 scored reads, `dm_p` is `None` everywhere) → **31**, matching
`summary.json.fdr.family` length exactly (verified: `computed registered-family size: 31 vs fdr.family
length: 31`).

### 1c. "Everything reported" — executed count

Recursively collecting every `dm_p` / `p_value` leaf in `summary.json` (excluding the `fdr` block
itself, to avoid re-counting its 31 duplicates), deduplicating the one true duplicate (`placebo.dm_p`
top-level is a copy of `placebo.vs_random_analogs.dm_p`):

```
spec_curve.rows dm_p:                         162
everything else with a p-value (dm_p/p_value):  80   (baselines×score-variants, per-class, items×2
                                                        score variants, diagnostic_fair, pinball,
                                                        G_joint_across_tiers, permutation, regime
                                                        blocks×2 tasks, placebo×3)
------------------------------------------------------
TOTAL distinct p-value-bearing comparisons:    242
```
plus 3 SPA joint p-values (already internally multiplicity-corrected, so not folded into the 242).

### 1d. The naive fully-crossed formula the task asked for

`menu(12) × tiers(2) × targets(10 reported score variants) × baselines(4, protocol max) ×
regime_blocks(3) × spec_curve_cells(162) × placebo(3)`:

```
12 × 2 × 10 × 4 × 3 × 162 × 3 = 1,399,680
```
This product is a **ceiling, not a real count** — the axes are not actually fully crossed in the
design (spec-curve varies burn-in/k/horizon/cluster/threshold against climatology only, not against
all 4 baselines; placebo is P-only; DEAL and RPS are G-only; regime blocks are computed once per task,
not per baseline). It is reported because the task asked for it; the number that matters is **31
(registered) vs 242 (everything with a p-value in the file) vs 1 (the target the protocol's own §6
narrative singles out per headline sentence)**.

---

## 2. What the FDR block actually covers

**Covered (31 comparisons, q = 0.05, primary score only):**
- G Brier: engine vs {climatology, frozen, random_analogs} + 12 menu items vs climatology
- P CRPS: engine vs {climatology, persistence, random_analogs, frozen} + 12 menu items vs climatology

**NOT in the family** (confirmed by reading the code paths that build `fam_p` — none of these blocks
ever append to it):
| comparison | where it's computed | in family? |
|---|---|---|
| RPS engine vs random_analogs (p=0.001, "the only G comparison that clears p<0.05" per `release_check_2026-09-02.md`) | `walk.py:542-547` (`blk["rps"]`, separate block) | **NO** |
| G label-permutation p = 0.008 | `walk.py:593-681` (`permutation_test`), attached at `run()` line 1099, `summary["permutation"]`, never touches `fam_p` | **NO** |
| P engine vs persistence, DM p < 0.001 ("beats persistence") | `walk.py:514-521`, task=P, ref="persistence" (P's `refs` tuple includes it) | **YES** — this is comparison #16 in the family (`daily:P:engine_vs_persistence`, p=1.18e-11) |
| The 162 spec-curve cells | `walk.py` `spec_curve()`, separate function, `summary["spec_curve"]` | **NO** |
| Placebo (vs_random_analogs / vs_climatology / fair) | `walk.py` `placebo()`, separate function | **NO** |
| DEAL binary Brier, log score, pinball, per-class, diagnostic_fair (size-corrected) | all computed in `summarize_tier` but in blocks that never append to `fam_p` (lines 533-536, 539-540, 549-554, 558-560, 522-524) | **NO** |

**A finding independent of the multiplicity question**: `summary.json.tiers.daily.G.engine_vs` has
only 3 keys (`climatology`, `frozen`, `random_analogs`) — **no `persistence` key at all**, and
`spa_vs_persistence` / `n_persistence_fallback` are absent from the G block, even though committed
HEAD's `walk.py` (this exact commit, `b7c8ec1`, "Brief B-1... G-persistence, the fourth G baseline")
computes all of them. `git log --oneline -- data/walk_forward/summary.json` shows the file was last
written by commit `d3df9af` (run `182828Z`), which is the **parent** of `b7c8ec1`; `git show --stat
b7c8ec1` touches only `src/engine/persistence.py`, `src/engine/read.py`, `src/walk.py`,
`tests/conftest.py`, `tests/test_walk_baselines.py` — **not** `data/walk_forward/summary.json`. The
commit message itself says "(code)". So: **the G-persistence baseline is committed code that has never
been run** — `summary.json`, `README.md` and both gate files all describe a walk that predates it. This
means the FDR family's absence of `daily:G:engine_vs_persistence` isn't a deliberate exclusion — the
data doesn't exist yet for this published run.

---

## 3. Recomputed family-wise correction (executed)

BH (Benjamini–Hochberg, q=0.05), Holm and Bonferroni (α=0.05), computed with full (unrounded) `dm_p`
pulled from the JSON tree (not the 5-dp values printed in `fdr.family`).

### (a) Registered family as the code defines it, n=31

| rank | comparison | p | BH q | BH | Holm | Holm | Bonf | Bonf |
|---|---|---|---|---|---|---|---|---|
| 1 | daily:P:engine_vs_persistence | 1.18e-11 | 0.00000 | **True** | 0.00000 | **True** | 0.00000 | **True** |
| 2 | daily:P:M06_uniform_k5_vs_climatology | 1.20e-05 | 0.00019 | **True** | 0.00036 | **True** | 0.00037 | **True** |
| 3 | daily:P:M02_situation_only_vs_climatology | 0.00233 | 0.02411 | **True** | 0.06767 | False | 0.07234 | False |
| 4 | daily:P:M09_uniform_strict_050_vs_climatology | 0.01529 | 0.09043 | False | — | False | — | False |
| … 27 more, all False … |

**BH survivors: 3/31. Holm survivors: 2/31. Bonferroni survivors: 2/31** — all three are P (price CRPS)
comparisons; **no G comparison survives any correction**, registered or not.

### (b) Full reported set (non-spec-curve p-values, n=80, deduplicated)

| rank | comparison | p | BH q | BH | Holm | Bonf |
|---|---|---|---|---|---|---|
| 1 | daily:P:engine_vs_persistence | 1.18e-11 | 0.00000 | **True** | **True** | **True** |
| 2 | placebo.vs_climatology | 2.31e-06 | 0.00009 | **True** | **True** | **True** |
| 3 | daily:P:items_vs_climatology.M06_uniform_k5 | 1.20e-05 | 0.00032 | **True** | **True** | **True** |
| 4 | daily:G:rps.engine_vs.random_analogs | 5.37e-04 | 0.01074 | **True** | **True** | **True** |
| 5 | daily:G:diagnostic_fair.rps_engine_vs_climatology | 9.57e-04 | 0.01532 | **True** | False | False |
| 6 | daily:P:items_vs_climatology.M02_situation_only | 0.00233 | 0.03111 | **True** | False | False |
| 7 | permutation (G, p=0.008) | 0.00799 | 0.09134 | **False** | False | False |

**BH survivors: 6/80. Holm survivors: 4/80. Bonferroni survivors: 4/80.** Two of the 6 BH survivors are
labelled `"registered": false` diagnostics in the file itself (`placebo.vs_climatology` and
`diagnostic_fair.rps_engine_vs_climatology`) — both are known to carry a mechanical small-sample bias
under the null (Amendment A.4/A.5; see §2 caution below), not evidence of anything. Removing those two
leaves **4 substantive survivors**: P-vs-persistence, the two P items (M06, M02), and G RPS-vs-random-
analogs.

### (c) Full reported set including all 162 spec-curve cells (n=242, for reference)

BH survivors: 33/242 (mostly spec-curve rows at specific grid points — expected, since spec-curve is a
published *distribution*, not individually gated, per protocol design). Holm/Bonferroni: 18/242.

### README sentence-by-sentence

| README sentence | p cited | in registered family? | survives BH(a) 31? | survives BH(b) 80? | survives Holm/Bonf? |
|---|---|---|---|---|---|
| "It beats persistence (+0.16, p < 0.001)" | 1.18e-11 | **Yes** (#16 of 31) | **Yes** | **Yes** | **Yes** |
| "A label-permutation test rejects 'the engine is noise' (p 0.008)" | 0.008 | **No** — never enters `fam_p` | n/a | **No** (BH q=0.091) | **No** |
| (release_check, not README) "RPS vs random analogs... the only G comparison that clears p < 0.05" | 0.001 | **No** — RPS block never enters `fam_p` | n/a | **Yes** nominally (BH q=0.011) — but see §4/§2: not a registered score, no SPA run on it | **Yes** (Holm/Bonf) |

**"Beats persistence" is the one sentence in the README that is genuinely robust to every multiplicity
correction tried here**, registered or not. It should be read with one caveat unrelated to
multiplicity: the persistence baseline is a **single-atom (point) forecast** (`n_atoms: 1` in every
sealed `scores.jsonl` row for `persistence.P`) being compared on CRPS to the engine's multi-atom analog
distribution. Protocol Amendment A.5 already documents and corrects for exactly this mechanical bias
for the *climatology* comparison (a k=8 engine distribution scored against climatology's ~10k-atom
distribution is biased **against** the engine by `E|X-X'|/2k`); the same Ferro-2014 mechanism runs in
the **opposite** direction here — a k=1 persistence forecast is mechanically biased against
*persistence*, i.e. mechanically inflates the engine's apparent win — and no `diagnostic_fair`-style
correction exists for `engine_vs_persistence` anywhere in `summary.json` (`diagnostic_fair` only covers
`engine_vs_climatology` and `frozen_vs_climatology`). This is not a multiplicity problem and not
something D-3 was scoped to fix, but it directly bears on how much weight "beats persistence" should
carry, and it is not disclosed next to the sentence.

The permutation p=0.008 does not survive being pooled with the other ~80 reported comparisons at the
same q the protocol uses everywhere else (0.05). It was never registered into a family to be corrected
in the first place (§2) — it is reported and interpreted on its own.

---

## 4. Post-hoc "best menu item" (M07) and SPA

`verdict.rules["M07_uniform_k12:G"]["status"] == "SUGGESTIVE"` (no `"/ null"` suffix — the only menu
item with a positive point-estimate skill), with `daily:skill>0: True` but `daily:dm_p<0.05: False`,
`daily:spa_p<0.05: False`. `tiers.daily.G.spa.best_model == "M07_uniform_k12"`, `p_spa = 0.793`.

**Is choosing "best = M07" post hoc covered by SPA?** Yes, and correctly: `walk.py:566`
(`blk["spa"] = _spa_block(sc, task, key, "climatology", item_ids + ["engine", "frozen"], n_spa, mb)`)
runs Hansen's SPA over all 14 models (12 items + engine + frozen) against climatology on the *primary
registered score*, which is exactly the "best of many, tried post hoc" scenario protocol §6 describes.
`p_spa = 0.793` rejects "some model beats climatology" — i.e., **the fact that M07 has the best point
estimate among 12 tries is explicitly tested and found not distinguishable from chance.** This is the
one part of the design working as intended.

**Gap**: SPA is run only on the primary score (Brier for G, CRPS for P) — `walk.py:566` uses `key`,
which is `"brier"`/`"crps"`. There is **no SPA test over the RPS item comparisons**
(`tiers.daily.G.rps.items_vs_climatology`, 12 more p-values, best there is
`M07_uniform_k12` again at p=0.0256 — the same item "winning" on a second, unprotected score). If
someone picked "best RPS item" the way the desk already surfaces "best Brier item," there is no
registered guard against it.

**Desk exposure**: `grep` of committed `src/api_v2.py`, `src/app.html`, `src/story_read.py`:
- `src/api_v2.py:206-221` (`/api/walk/summary`) passes the **whole** `summary.json` through except each
  tier's `items_vs_climatology` table — but `verdict.rules` is a top-level key, not nested under
  `tiers`, so it is **not** filtered; the raw per-item verdict rows (including M07's bare `"SUGGESTIVE"`
  next to 11 siblings reading `"SUGGESTIVE / null"`) are served as-is by the API.
- `src/app.html:307` and `src/story_read.py:207` both surface `best_model` **only** paired with its
  `p_spa`/`SPA p` value in the same string (`"SPA p ${...} (best ${...})"`), so the one narrated
  surface never shows M07 without the p=0.793 that sinks it. No template in `app.html` iterates
  `verdict.rules` per item, so the bare `"SUGGESTIVE"` status is reachable only by a viewer reading
  `/api/walk/summary`'s raw JSON directly, not through any narrated desk surface.

---

## 5. Dependence: does the permutation test respect clustering?

`tiers.daily.dependence = {"cluster_days": 35, "mean_block": 2.32, "hac_lag": 1}` (from
`_mean_block(dates, cluster_days=35)`, `walk.py:510-512`). This `mean_block`/`hac_lag` **is** used by
every DM/HLN test: `_skill_block(..., mb, n_boot, max(lag, 0))` is called with `lag = round(mean_block)
- 1 = 1` throughout `summarize_tier`, and `dm_test` (`engine/inference.py:96-115`) feeds it straight
into Newey–West HAC variance. So **the DM/HLN family (the 31-comparison FDR family, §2/§3) is
dependence-corrected**, if modestly (1 lag).

The **label-permutation test is not.** Reading `permutation_test` (`walk.py:593-681`), the resampling
step is:
```
671  for _ in range(n_perm):
672      lp = lab.copy()
673      for cls_, idxs in groups.items():
674          idxs = np.array(idxs)
675          lp[idxs] = lab[idxs][rng.permutation(len(idxs))]
676      null.append(skill_for(lp)[0])
```
`groups` partitions all touched event ids **by event class only** (`conflict_escalation`,
`sanctions`, `infrastructure_attack`, `chokepoint_disruption`); within a class, `rng.permutation`
shuffles labels **i.i.d.**, with no reference anywhere in this function to `dates`, `cluster_days`, or
block structure — despite `dates` being computed two lines earlier (line 634) and available. This
directly contradicts protocol §2's own registered clustering rule ("reads within 35 days are one
cluster") and §6's instruction that the **stationary block bootstrap** (already implemented and used
for the DM/SPA tests, `engine/inference.py:120-134`) govern "all intervals" — the permutation test uses
plain `rng.permutation`, never `stationary_bootstrap`.

**Quantified** (executed on `scores.jsonl`, run `182828Z`, daily tier, 150 scored geopolitical reads,
date-ordered): the IES-90 level sequence has lag-1 autocorrelation **+0.17**, and rises again at
lag-5/6/7 (**+0.19 / +0.28 / +0.27**) — crises visibly cluster and their coded levels move together
over adjacent weeks-to-months, exactly the dependence structure §2's 35-day clustering rule exists to
capture. **62% of consecutive scored reads fall within 35 days of each other** (median gap 21 days),
so the "cluster" unit the protocol registered is the typical case, not the exception, for this
sequence.

Why this matters for p=0.008: i.i.d. within-class permutation treats each of the 150 labels as
exchangeable independently of its neighbors. With true positive serial correlation in the label
sequence, the *actual* sampling distribution of "skill under a genuinely structureless world" is wider
than the one the code's null distribution produces (i.i.d. shuffles wash out real runs faster than
block-preserving shuffles would), which pushes small effects further into the tail than they would sit
under a block permutation — i.e. **the reported p=0.008 is very plausibly anti-conservative** (too
small) given the measured autocorrelation. This is a direction-and-magnitude judgment, not a
recomputed p-value — properly checking it needs a block-permutation rerun (permute intact ~35-day
windows, not individual ids), which was out of scope here (read-only review, `walk.py` not run).

---

## 6. Monthly tier

`tiers.monthly = {"n_reads": 14, "n_scored_burn_in": 0, "permits_validation": False}`;
`verdict.tiers_permitting_validation == ["daily"]` only; `G_joint_across_tiers.n == 150` (equal to the
daily-only geo count — monthly contributes 0 rows because `burn_in_ok` is `False` for every monthly
read). `grep -in monthly README.md` returns only two lines describing the raw data spine ("a monthly
price spine back to 1946... monthly WTI since 1946") — **no prediction claim, skill number, or p-value
anywhere in the README is derived from the monthly tier.** This part of the design is working exactly
as documented (§9: "the monthly tier can describe, not validate").

---

## FINDINGS, ranked by whether they put a published sentence at risk

**1. "It beats persistence (+0.16, p < 0.001)" — survives every multiplicity correction tried
(registered family, full reported set, BH/Holm/Bonferroni), but the comparison itself is not corrected
for the same k-atom CRPS bias the protocol already applies to the climatology comparison.**
Evidence: §3(a)/(b) tables; persistence forecasts are `n_atoms: 1` point masses in every sealed score
row; Amendment A.5 (`WALK_FORWARD_PROTOCOL.md`) derives and corrects this exact mechanism
(`E|X-X'|/2k`) for `engine_vs_climatology` only; `diagnostic_fair` has no `engine_vs_persistence`
variant. This doesn't make the sentence false — it means the sentence's effect size is not yet known
free of a documented, already-instrumented bias. Not a multiplicity finding, but it is the one thing
standing between "genuinely robust" and "genuinely robust to a biased comparison."

**2. "A label-permutation test rejects 'the engine is noise' (p 0.008)" is the README's most exposed
sentence.** It is (a) not in the registered FDR family at all — never corrected against the other ~31–
242 comparisons the same run produces (§2); (b) when pooled with the other 79 reported p-values and
BH-corrected at the protocol's own q=0.05, it does not survive (BH q=0.091, §3b); (c) its null
distribution is generated by i.i.d. within-class label shuffling that ignores the registered 35-day
clustering rule the DM tests do respect, against a label sequence that is measurably autocorrelated
(lag-1 = +0.17, §5) — the direction of that mismatch is anti-conservative. Three independent reasons to
distrust the precision of "0.008" as stated, none of which the README discloses.

**3. Release-check's "RPS vs random analogs... the only G comparison that clears p < 0.05" (p=0.001,
not in README but quoted verbatim in `data/gates/release_check_2026-09-02.md` and flagged there as "not
a registered gate") nominally survives BH/Holm/Bonferroni when pooled with everything else reported —
but it was never eligible for the registered family (RPS isn't the gate score), and no SPA test was run
on the RPS-item family the way it was on the Brier-item family (§4), so if RPS is ever promoted to a
gate (protocol A.2 leaves this open), the same post-hoc-best-item exposure that SPA currently catches
for Brier (M07, §4) is currently uncaught for RPS.**

**4. `data/walk_forward/summary.json` — the file `README.md` and both `data/gates/*` reports cite —
predates the G-persistence baseline that is committed at HEAD (`b7c8ec1`).** `G.engine_vs` has 3 keys,
not the 4 the current code and the current protocol (Amendment B) both specify; `G:engine_vs_persistence`
is absent from the FDR family not by exclusion but because it doesn't exist in this run yet. This
doesn't put a specific README sentence at risk today (no G-persistence number is quoted anywhere), but
it means "four baselines for G" (claimed as done in the `b7c8ec1` commit message and Amendment B) is not
yet true of any published number, and the next `python3 src/walk.py` run will change the registered
family from 31 comparisons to something larger without anyone having re-derived the count.

**5. M07_uniform_k12 is the one menu item whose `verdict.rules` status omits `"/ null"`
(`"SUGGESTIVE"` vs. every sibling's `"SUGGESTIVE / null"`), and it is served as-is by `/api/walk/summary`
(the endpoint filters `items_vs_climatology` but not `verdict.rules`), reachable by anyone reading the
raw API response rather than the narrated desk pages.** No template in `app.html`/`story_read.py`
iterates `verdict.rules` per item, and both places that do surface `best_model` pair it with the p_spa
value that sinks it (§4), so this is a latent exposure, not an active one — but it is a published number
one JSON fetch away from being read as "M07 is suggestive" without its 0.793 SPA p-value attached.

---

## What this review did not do
- Did not re-run `src/walk.py` (repo instruction: never run it) — the anti-conservative-permutation
  claim (§5) is a direction/magnitude argument from measured autocorrelation, not a recomputed
  block-permutation p-value; a proper check needs a rerun with `rng.permutation` replaced by a
  block-preserving shuffle.
- Did not verify `weights.jsonl` / Hedge learning-curve internals — out of D-3's scope (multiplicity
  only).
- Did not check `src/audit_ies90.py` or the label-audit pipeline (§1 filtration/audit) — out of scope.
