# B → Cowork, 2026-09-03 — the incremental-information experiment, as computed

**The question.** Does the analogue distribution carry information about escalation **beyond what the
dyad's own last 90 days already say?**

**The verdict, by a rule written before the numbers existed: NO ADDITION.** It does not — not at a
resolution this corpus can see. But the experiment turned up something larger than its own null, and the
two must be reported together or both are misleading.

Registered: `WALK_FORWARD_PROTOCOL.md` **Amendment L** (commit `a2ae995`), before the module existed.
Computed: `src/engine/delta_experiment.py` on the sealed run `walk_20260903T003422Z`, full registered draws
(2,000 bootstrap, 1,000 SPA, 1,000 + 1,000 permutation). Published:
`data/walk_forward/delta_experiment.json` and `summary.json → tiers.daily.G.experiment_delta`.

---

## 1. Why the estimand changed

The strongest result in the published run is that **G-persistence beats the engine**, 0.4805 to 0.7687 on
the registered Brier (skill −0.600, DM/HLN p 0.0002, n 150). A point mass on the level the dyad had already
reached over [t−90, t−1] outscores the whole analogue machinery by 37 %.

That makes the *level* estimand the wrong question. It asks the engine to **replace** the dyad's recent
history rather than **improve** on it, and the engine's state vector contains no field for the dyad's own
current level — so it forecasts from scratch while persistence starts from the answer. Any model that does
not start from persistence starts behind.

Amendment L re-anchors the same sealed reads and asks for the **change**:

| | |
|---|---|
| **target** | ΔIES = L − L⁻, ordered categorical on {−3 … +3} |
| **forecast** | each analog votes with its **own** change, Δ_a = L_a − L⁻_a, L⁻_a from that analog's own sealed read |
| **baseline to beat** | **no-change**: a point mass on Δ = 0, Amendment B.2 smoothed — this *is* G-persistence in this estimand |
| **object** | the **combination** of the two |

Nothing was re-retrieved and no Hedge weight was re-fitted. Same twelve items, same sealed weights, same
analogs. The only change is what the analogs vote on.

**One thing registered in advance so it can never be sold as a finding:** after clipping to the feasible
set, Δ ↔ level is a bijection, so the 7-category Δ Brier of any forecast equals the 4-level Brier of its
implied level forecast, exactly. The reframing changes the **forecast** and the **baseline**. It does not
change the score axis, and every number below is on the same axis as the published run. The code asserts
this on every read.

---

## 2. The finding that is not the verdict

Re-anchoring the same analogs — level-voting to change-voting — moves the Brier from **0.763 to 0.480**.

| forecaster | registered Brier | |
|---|---|---|
| the sealed engine, 13 items, voting on **level** | **0.7687** | the published run |
| the same mixture, M01–M12, voting on level (control) | 0.7629 | the gap is M13's share of the weight |
| **the same mixture, the same weights, voting on CHANGE** | **0.4799** | |
| **G-persistence / no-change** | **0.4805** | |

**The engine's entire 0.29 deficit against persistence was the missing anchor, not the analogies.**
Re-anchored, the analogue mixture and persistence are a dead heat: skill +0.0012, DM p 0.980. The engine's
problem was never that its historical analogies were wrong. It was that nobody told it where the dyad
already stood. The control (`reanchoring_check` in the JSON) rebuilds the same twelve items voting on level
and lands on 0.7629 against the sealed 0.7687, so the re-anchoring is demonstrably the only thing that
moved.

One departure, disclosed rather than smoothed over: L.2 registers that an item with no analog is charged
the Δ-climatology forecast, while the sealed walk drops such an item from the mixture by zeroing its
weight. 58 of 1,800 item slots abstain in the retained set; the measured difference in mean Brier is
**0.00035**. Registered before the code, and too small to matter, but "pure re-anchoring" should be precise.

This is a statement about **the estimand**, not about skill. It says the published −0.600 was measuring an
anchoring failure. It does **not** say the engine has skill.

---

## 3. The registered result

n = 150 retained of 150 scored daily-tier G reads. **0 excluded**; 0 of 10,885 analog slots lacked an L⁻;
mean L⁻ coverage 3.14 sources. Δ = 0 on 110 of 150 reads (**73.3 %**; L.8.1's near-degenerate threshold is
0.90, so the target is not degenerate but it is close). Mean block 1.95, HAC lag 1, 57 clusters.

### The three registered combinations against persistence — the gate score

| forecaster | Brier | skill vs no-change | 95 % CI | DM/HLN p |
|---|---|---|---|---|
| **C1** ½ no-change + ½ analogue (**primary**, fixed registered λ) | **0.4643** | **+0.0336** | −0.0124 … +0.0784 | **0.181** |
| **C2** walk-forward λ (registered grid, closed reads only) | 0.4671 | +0.0279 | −0.0129 … +0.0693 | 0.219 |
| **C3** Hedge over the two, registered η | 0.4656 | +0.0310 | −0.0120 … +0.0751 | 0.199 |
| analogue alone | 0.4799 | +0.0012 | −0.1033 … +0.0868 | 0.980 |
| Δ-climatology alone | 0.4635 | +0.0354 | −0.0354 … +0.1003 | 0.340 |
| frozen (equal-weight menu) | 0.4802 | +0.0005 | — | 0.992 |
| random analogs | 0.4824 | −0.0040 | −0.0833 … +0.0593 | 0.914 |
| **no-change (G-persistence)** | **0.4805** | — | — | — |

On the ordinal **RPS**, where a one-level miss costs less than a three-level miss, the same ordering with
slightly more separation: C1 0.3633 (skill +0.0450, CI +0.0015 … +0.0856, p 0.063), C3 +0.0428 (p 0.065),
C2 +0.0381 (p 0.083), Δ-climatology +0.0549 (p 0.129), no-change 0.3805.

### Every gate condition, as computed

| condition (L.7) | value | passes? |
|---|---|---|
| C1 skill > 0 | +0.0336 | yes |
| DM/HLN p < 0.05 | 0.181 | **no** |
| 95 % bootstrap CI excludes 0 | −0.0124 … +0.0784 | **no** |
| SPA p < 0.05, family {C1,C2,C3}, benchmark no-change | 0.075 (best model C1) | **no** |
| block label permutation p < 0.05 | 0.124 | **no** |
| BH-FDR q 0.05 across all 14 reported comparisons | nothing survives (min q 0.387) | **no** |

**Measured minimum detectable skill at n = 150: 0.0666.** The observed skill is 0.0336 — half of it. This
is a null we could not have distinguished from a real effect of this size, which is exactly why L.8.7
registered the power number in advance.

**λ never abandons the analogue.** Free to move on a registered grid {0.0 … 1.0} and fitted only on closed
reads, C2's λ took the values 0.5 (67 reads), 0.6 (54), 0.7 (29); terminal 0.5; the fit on all closed reads
also 0.5. C3's Hedge weight on no-change stayed in 0.449–0.582, terminal 0.482. Both learners settle on
roughly half the analogue. That is why L.7's **DEGRADES** branch does not fire and why the answer is NO
ADDITION rather than "analogy hurts."

**Sensitivity (L.8.4), reads whose L⁻ is carried by ≥ 2 sources, n = 66:** C1 skill +0.0075 (p 0.876), C2
+0.0059, analogue alone −0.1058 (CI −0.428 … +0.074, p 0.269). The gain, such as it is, is smaller on the
better-sourced half.

---

## 4. Pooling or similarity? (Amendment M — diagnostic, registered post hoc and labelled as such)

C1's +0.034 is ambiguous: any second distribution pooled with a 0.9-sharp point mass buys shrinkage. So a
control, registered in commit `573628f` before it was computed, with its post-hoc motivation stated rather
than concealed — three pools at the **identical** λ = 0.5, differing only in the second component.

| pool | second component | Brier | skill vs no-change | p |
|---|---|---|---|---|
| **C1** | the retrieved analogue | 0.4643 | +0.0336 | 0.181 |
| **C0r** | random analogs, same pool, same sealed k and seed | 0.4677 | +0.0266 | 0.168 |
| **C0** | the whole Δ-climatology | **0.4626** | +0.0371 (CI +0.0029 … +0.0723) | 0.056 |

**C1 against C0, paired: −0.0037 (CI −0.0288 … +0.0204, p 0.766).** On RPS, −0.0009 (p 0.938).

By M.3's rule, written before the numbers: **the gain is pooling, not similarity.** The retrieved analogues
are interchangeable with the class's unconditional Δ distribution inside the pool — if anything the
unconditional distribution is marginally better, and it is the only forecaster in the whole experiment that
comes near separating from persistence (p 0.056, and it would not survive the multiplicity correction).
C1 against C0r is +0.0071 (p 0.555): retrieval barely improves on random draws from the same pool.

This is a diagnostic. It gates nothing and does not move L.7's verdict.

---

## 5. What to write, and what not to

**The claim that is supported.** Once the dyad's own last 90 days are known, the analogue distribution adds
nothing detectable at n = 150. The three registered combinations gain 0.028–0.034 of Brier skill over
persistence; none clears its interval, its DM test, the SPA family or the block permutation, and nothing
survives FDR. The gain that exists is a pooling effect that the class base rate supplies at least as well
as the retrieved analogues.

**The claim that is also supported, and is the bigger one.** The published −0.600 against persistence was
measuring the wrong thing. The engine was forecasting the level from scratch when it should have been
forecasting the change from where the dyad already was. Re-anchored, the identical analogue machinery goes
from 0.763 to 0.480 and draws level with persistence. This is a defect of the estimand, found and repaired,
and the repair is worth a section.

**Three things not to write.**
1. Do **not** write that the engine improved. It draws with persistence; it does not beat it. The
   re-anchoring result is about how the question was posed, not about skill acquired.
2. Do **not** write that analogy degrades escalation forecasting. That was a registered verdict
   (**DEGRADES**) with a registered condition, and the condition did not fire: the fitted weight keeps half
   its mass on the analogue.
3. Do **not** report the null as "no effect." The measured MDS is 0.0666 and the observed skill is 0.0336.
   The honest sentence is *"not detectable at n = 150."*

**What would settle it.** The MDS scan in the JSON says a skill of +0.05 needs roughly the n the power block
reports; at the observed +0.034 the requirement is larger still. The pre-1987 corpus (PATH Step 5) is the
only thing that moves n, and Amendment J.3 already registers the Δ blocks as first-class output of the
first v3 run. This experiment is the v2 preview of that, run early because it does not need the new corpus.

**Standing.** Nothing here re-judges a v2 number. `engine:G` on the level estimand keeps exactly the status
the published run gave it, and §7's VALIDATED remains unavailable to everything in this project until the
label audit passes (1 of 30 rows in).

---

## 6. Where the numbers are

- `data/walk_forward/delta_experiment.json` — every number above, with its interval, its p-value and its
  registered clause; `verdict`, `power`, `spa`, `permutation`, `fdr`, `sensitivity_covering_ge2`,
  `reanchoring_check`, `diagnostic_pools`.
- `data/walk_forward/delta_experiment_reads.json` — per-read L⁻, level, Δ, source coverage, the λ and the
  Hedge weight in force at that read.
- `summary.json → tiers.daily.G.experiment_delta` — the same object, in the file the desk reads.
- `WALK_FORWARD_PROTOCOL.md` Amendments **L** and **M** — the registrations, both committed before their
  code.
- `tests/test_delta_experiment.py` — 23 tests, each named for the clause it covers, including the two
  leakage probes: an unclosed outcome cannot reach C2's λ, and an unclipped forecast must break the
  Δ/level identity.
