# G-6 REGISTRATION — OPEN_ITEMS 1.4, the era confound: can era, pool size, base rate and label basis be separated at n = 150?
*2026-09-03, Session G. Registered BEFORE `src/g_era_confound.py` is written and BEFORE any
stratified number is computed (charter §2 rule 2). **This is a DIAGNOSTIC. It gates nothing.**
It re-judges no run, moves no threshold, changes no published verdict, and writes to no table.
Amendments are dated and appended.*

## 0. Standing, and a reassignment recorded rather than assumed

`OPEN_ITEMS.md` §1.4 names **B** as owner. Joe reassigned the item to Session G on 2026-09-03
("your panel work is the reason you are the right session for it"). G therefore writes only to
its own paths — `docs/g/**` and `src/g_era_confound.py` — reads `data/walk_forward/**` and never
writes there, and hands the result to B and to whoever owns `OPEN_ITEMS.md`. Nothing in
`src/walk*.py`, `data/walk_forward/**` or `data/grid/**` is touched.

## 1. The question, stated so it can come out "no"

Joe: *"What I want to know is whether the three confounds can be separated at all at this n, and
if they cannot, say so rather than reporting a decomposition the sample cannot support."*

So the deliverable is **not** a decomposition. It is a **verdict on identifiability**, with the
decomposition published only if the verdict permits it. §5 fixes the rule that decides, before
any of it is computed.

## 2. The run is PINNED, and why that is not a formality

`data/walk_forward/scores.jsonl` **currently contains two runs** — `walk_20260903T003422Z`
(313 rows) and `walk_20260903T052633Z` (313 rows) — while `summary.json` describes only the
first and is older on disk (23:23 against 01:28). `WALK_FORWARD_PROTOCOL.md` Amendment D says
the sealed logs in the tree hold **the current run only**, with earlier runs archived. Either
session B is mid-run and the archive step has not fired yet, or Amendment D's invariant is not
holding. **Either way, an analysis that read the file without filtering would silently mix two
runs.**

This diagnostic is computed on **`run_id == "walk_20260903T003422Z"` only** — the run
`summary.json` publishes and the run OPEN_ITEMS §1.4 quotes. The second run is excluded by
`run_id`, its presence is reported, and the fact is handed to B rather than acted on.

**Baseline check, before anything is stratified.** The pinned run must reproduce the published
G block exactly:

    n = 150 · engine_mean = 0.7687487109093333 · ref_mean = 0.7010597406851313
    skill = −0.09655235680492913          (summary.json tiers.daily.G.engine_vs.climatology)

If it does not reproduce to the seventh decimal, the diagnostic is void and says so. Everything
below is measured against a number this code has re-derived, not against one it was told.

## 3. The four variables, and where each comes from

| variable | definition | source, read not recalled |
|---|---|---|
| **era** | the four bins of OPEN_ITEMS §1.4: 1987–99, 2000–09, 2010–19, 2020–26 | the read's `date` |
| **pool size** | the point-in-time G pool the read was scored against | `reads.jsonl` `n_pool_g` |
| **base rate** | the level-0 share of that read's **own** pool, not an era average | `reads.jsonl` `baselines.climatology.G_labels` |
| **label basis** | whether the IES-90 level rests on a dyadic or a location reading | `event_outcomes` `field='basis'` (`ies90`), per event |

The bins are **taken from OPEN_ITEMS as registered**, not chosen by G. Their unevenness
(n = 2, 10, 51, 87) is the property under test and is not repaired by re-binning: re-cutting the
bins after seeing the skill is exactly the move this document exists to prevent.

## 4. S4 — the size-correction test, with its direction and its magnitude registered in advance

This is the mechanism G thinks is doing the work, and it is registered as a **falsifiable
prediction with a number** before the data is cut, so that being wrong about it is visible.

`WALK_FORWARD_PROTOCOL.md` Amendment E.3 registers that the Brier score of a **k-atom**
predictive distribution exceeds the population Brier by `Σ_b p_b(1−p_b) / k`. In this run:

- the **engine**'s distribution is built from its k analogs — `n_atoms = 5` on the read inspected;
- **climatology**'s distribution is the pool's own label frequencies — `n_atoms = the pool size`,
  which OPEN_ITEMS reports as median **8 → 10 → 18 → 36** across the four eras.

So the engine's inflation is roughly constant at `S/5` while climatology's shrinks as `S/pool`.
**The engine's handicap relative to climatology therefore grows monotonically with pool size, and
pool size grows with era — which produces a declining measured skill across eras under exactly
zero change in true skill.**

**Registered magnitude.** With both raw scores near 0.7, the differential inflation is about
`0.7/5 − 0.7/8 = 0.053` in the earliest era and `0.7/5 − 0.7/36 = 0.121` in the latest — a swing
of ≈ **0.068 in absolute Brier**, or ≈ **0.10 in skill** on a reference near 0.70. The observed
era spread is `+0.009 → −0.117`, i.e. **0.126**. So the prediction registered here is that the
size artefact alone is of the **same order as the entire observed era gradient**.

**The test.** Both scores are already sealed: `brier` (registered) and `brier_fair` (Ferro
size-corrected, Amendment A.5/E). The era table is computed on **both**. The registered
prediction is that the fair-Brier era gradient is **materially flatter** than the registered-Brier
one. Fixed now, before the numbers:

> **S4 passes** (the artefact is doing most of the work) if the era spread in fair-Brier skill is
> **≤ half** the era spread in registered-Brier skill.
> **S4 fails** (the era effect survives size correction) if the fair spread is **> half** the
> registered spread.
> Either way the result is published, and **neither outcome changes any verdict** — Amendment E.1
> already rules that the registered scores govern every v2 run, and this diagnostic does not
> touch that.

## 5. S3 — separability, and the rule that decides it, fixed before it is run

Three things are computed:

1. **Collinearity.** Pairwise Spearman ρ among (date-ordinal, pool size, pool base rate, dyadic
   label share) over the 150 scored reads, plus the condition number of the standardised design.
2. **Support.** The (era × pool-size tertile) cross-tab, with cell counts. Two variables can be
   separated only where the sample has cells **off the diagonal**: if every read in the early era
   has a small pool and every read in the late era has a large one, era and pool size are the same
   variable in this sample and no n repairs it.
3. **Overlap.** The min–max pool-size range within each era, and whether the ranges intersect.

**The registered decision rule.** The diagnostic returns **NOT SEPARABLE** if **any** of:

- **(a)** |Spearman ρ| between era-index and pool size ≥ **0.80**; or
- **(b)** the (era × pool-tertile) cross-tab has **fewer than two off-diagonal cells with n ≥ 20**; or
- **(c)** every era's 95 % interval on skill contains the pooled skill of −0.0966.

If NOT SEPARABLE, **no decomposition is published** — the era table is published as a description
with its intervals, and the answer to OPEN_ITEMS §1.4 is that the sample cannot answer it.
If SEPARABLE on all three, the decomposition is published with the caveats §7 lists.

## 6. S5 — power, so a null is read as "not detectable at this n"

Per era, the minimum detectable Brier skill at 80 % power for that era's own n and observed score
dispersion, by the protocol §6 convention, published beside every era's point estimate. Intervals
are **stationary block bootstrap** (Politis–Romano), the protocol's registered estimator, at the
registered seed 19900802, with the tier's registered 35-day clustering rule — reads within 35 days
are one cluster, so the era intervals respect the same dependence rule the headline does.

## 7. What this diagnostic cannot do, registered before it is read

- It **cannot** establish that the engine has skill. A confounded negative is not a positive.
- It **cannot** re-judge run `walk_20260903T003422Z` or any other. Amendment E.1 governs.
- It **cannot** separate label basis from era **at all** if §5(b) fails on that pair too; the
  daily tier begins in 1987 and OPEN_ITEMS's "100 % dyadic in 1946–73" is a monthly-tier fact
  quoted for context, not a fact about the 150 reads under test.
- It is computed on **150 reads across four bins, two of which have n = 2 and n = 10.** Whatever
  it finds about those two bins is description, not inference, and is labelled as such in the
  output rather than in a footnote.

## 8. Outputs

`docs/g/ERA_CONFOUND.json`, `docs/g/ERA_CONFOUND.md`, `src/g_era_confound.py` (reads `oil.db` and
`data/walk_forward/**` **read-only**, writes no table), `tests/test_g_era_confound.py`, and a
handoff to B and to the owner of `OPEN_ITEMS.md`.

---

## Amendment 1 (2026-09-03) — §4's prediction was wrong three ways, and what the run actually showed

*Dated and appended, never edited. The S4 verdict in §4 **stands as FAILED** on the statistic registered
there; it is not re-cut, and its threshold is not moved. This amendment records why it failed, which parts
of §4 were wrong as statements about the inputs rather than as predictions, and adds four post-hoc
diagnostics in the standing of `WALK_FORWARD_PROTOCOL.md` Amendment K — published beside the registered
result, published whichever way they come out, gating nothing.*

### A1.1 The premise was false: the engine's atom count is not constant

§4 states "the engine's distribution is built from its k analogs — `n_atoms = 5` on the read inspected"
and derives the whole magnitude from `S/5`. **`n_atoms_engine` ranges 5–22 across the 150 reads** and its
median rises with era: 6.5 → 8.0 → 11.0 → 14.0. It correlates with pool size at ρ = +0.65. G generalised
from a single inspected read to a constant, and that was not a prediction that turned out wrong — it was a
statement about the inputs that was wrong when it was written, and one more read would have caught it.

### A1.2 The magnitude was therefore ~5× too large

Because both atom counts grow together, the **differential** inflation `S_e/k_e − S_c/k_c` is far smaller
than §4's arithmetic: measured by era it is **+0.0259 → +0.0242 → +0.0319 → +0.0401**, a swing of
**0.014** in absolute Brier, against the **0.068** §4 registered. On a reference near 0.70 that is ≈ 0.02
in skill against an observed registered-Brier era spread of 0.185. **On this approximation the size
artefact accounts for roughly a tenth of the era gradient, not most of it.** The direction §4 predicted —
the engine is handicapped more than climatology by finite k, increasingly so as the pool grows — is
supported; the size is not.

### A1.3 The statistic was the wrong one, by G's own §7

S4 was defined on the **spread across all four eras**. Two of those bins have n = 2 and n = 10, and §7 of
this same registration says whatever they show "is description, not inference". The spread is dominated by
exactly those two bins: under fair Brier they read +0.128 (n = 2) and +0.335 (n = 10), which is what drove
the fair spread to 0.351 and the ratio to 1.90. **A statistic that a document's own caveat excludes from
inference should not have been the test.** It is left as registered and failed rather than swapped, because
replacing a test after seeing it fail is the move this project exists to prevent.

### A1.4 And `S/k` is not Ferro's correction

§4's arithmetic treats the correction as subtracting `S/k`. The registered fair Brier (Amendment A.5, the
weighted Ferro form with `c = Σw²/(1−Σw²)`) is not that, and the measured effect on the **level** is much
larger than the `S/k` differential suggests: pooled, the correction moves the engine's mean by **−0.112**
and climatology's by **−0.030**, so the engine benefits **≈ 3.7×** more. §4 conflated a *gradient* with a
*level* and used an approximation for a formula that was already implemented in the tree.

### A1.5 The four post-hoc diagnostics (Amendment K standing; they gate nothing)

- **D1 — the identity.** `n_atoms_clim == n_pool_g` on **150 of 150 reads**, exactly. Climatology's atom
  count *is* the pool size. **So "the pool-size confound" and "the size artefact" are not two of Joe's three
  confounds — they are one variable under two names**, and correcting for either corrects for the other.
- **D2 — the measured differential inflation by era** (A1.2's numbers), published as the honest replacement
  for §4's registered arithmetic and labelled as computed after the fact.
- **D3 — the era table restricted to bins with n ≥ 50.** This is not a post-hoc cut; it is §7's own
  registered caveat applied. The two bins that carry the sample move, under size correction, from
  **−0.1035 → +0.0124** (2010–19) and **−0.1169 → −0.0165** (2020–26). Stated as a **level**, never as a
  spread.
- **D4 — the level shift** of each score under correction (A1.4's numbers).

**None of D1–D4 is a finding about the engine's skill**, and none of them re-judges anything: session B has
**already published** the pooled size-corrected G comparison in `summary.json`
(`tiers.daily.G.diagnostic_fair.engine_vs_climatology`: n 150, skill **+0.021**, CI [−0.067, +0.111],
DM p 0.635, `registered: false`). G confirms that number; it did not discover it, and this document does not
present it as new.

### A1.6 What did not change

§5's separability rule and its verdict, §2's pinning and baseline check, §6's power block, §7's limits, and
the standing of the whole document as a diagnostic that gates nothing.

---

## Amendment 2 (2026-09-03) — the run this was computed on has been superseded; re-pin, and one correction to G's own report

*Dated and appended. Session B completed its Amendment 4 re-run while G-6 was being written.
`summary.json` now publishes `walk_20260903T052633Z` and `walk_20260903T003422Z` has been archived
to `data/walk_forward/runs/`. The first run's results are **not deleted** — this project annotates
its record — and both are published side by side below.*

### A2.1 The Amendment D report in §2 is withdrawn: it was the benign explanation

§2 reported that `scores.jsonl` held two runs while `summary.json` described one, and said this was
"either session B mid-run and the archive step has not fired yet, or Amendment D's invariant is not
holding." **It was the first.** `scores.jsonl` now holds one run (313 rows) and
`data/walk_forward/runs/walk_20260903T003422Z/{reads,scores,weights}.jsonl.gz` exists. Amendment D
held; G caught the tree mid-write. The handoff's §6 first bullet is corrected here rather than
edited there, and the **pinning was still right**: an analysis that had read the file during that
window without filtering would have mixed two runs, and would not have known.

### A2.2 The diagnostic re-pins to the published run, and the earlier one stays published

`RUN_ID` moves to **`walk_20260903T052633Z`**, the run `summary.json` publishes, with its own §2
baseline check against the new published G block. The earlier run's tables are retained in
`ERA_CONFOUND.json` under `superseded_run` so nothing is lost, and §2's rule is unchanged: if the
pinned run does not reproduce the published block to the seventh decimal the diagnostic is void.

**The headline the diagnostic interrogates has changed**, and that is stated rather than absorbed:
n **150 → 100**, registered skill **−0.0966 → −0.0838**, and B's size-corrected `diagnostic_fair`
**+0.021 → +0.0711**. The verdict, the separability rule, and §7's limits are unchanged in form and
are recomputed on the new run; whether they come out the same way is published either way.

### A2.3 Why the tests caught this and nothing else did

`tests/test_g_era_confound.py::test_g6_2_the_run_is_pinned_to_the_published_one` asserts the pinned
run *is* the one `summary.json` publishes. It failed the moment B's re-run landed. That is the test
doing its job: a diagnostic that silently keeps describing a superseded run is worse than one that
stops. Registered here so the pattern is deliberate — **every G artefact that reads another
session's published output carries a test that fails when that output moves.**

### A2.4 The tiny-bin defect recurred, and that is the lesson rather than the patch

A1.3 recorded that S4 failed because a **spread across era bins is dominated by the smallest bins**.
Re-pinning exposed the same defect in A1.2's own replacement statistic: on the new run the earliest
bin holds **one read**, and the all-bins differential-inflation spread reads **0.0687** — almost
exactly §4's registered 0.068, which would have looked like vindication. On the bins large enough
to read (n ≥ 8) it is **0.0094**, about a seventh of the registered figure.

So A1.2's conclusion holds and its *number* was run-specific. Both spreads are now published, the
n ≥ 8 figure is the one the reading uses, and the threshold is registered here rather than chosen
per run. **The general lesson, and it applies to anything cut by era on this corpus: a spread
statistic over unequal bins is a statement about the smallest bin.** G has now made that mistake
twice in one document; it is recorded twice rather than tidied once.

### A2.5 The results on both runs, and why the pair is stronger than either

| | superseded `…003422Z` | published `…052633Z` |
|---|---|---|
| n | 150 | 100 |
| registered skill | −0.0966 | −0.0838 |
| verdict | **NOT SEPARABLE** | **NOT SEPARABLE** |
| criteria fired | (a) ρ ≥ 0.80, (c) | **(b)** < 2 off-diagonal cells, (c) |
| ρ(era, pool) | +0.848 | +0.718 |
| D1: `k_clim == pool_g` | 150 / 150 | 100 / 100 |
| engine's benefit from size correction | 3.70× | 3.74× |

**The verdict is robust across the re-run and reaches the same answer by different criteria** — on
the new run the era/pool correlation falls below the bar, and non-separability is carried instead by
the disappearance of off-diagonal support as n falls. D1 and the 3.7× ratio are unchanged. That
agreement across two differently-labelled runs is stronger evidence than either run alone, and it is
the reason the superseded run is retained rather than dropped.
