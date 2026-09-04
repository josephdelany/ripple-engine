> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A claim sweep of the legacy documents, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# Findings sweep — block 1

*2026-09-03, session A. Files swept: `data/corroboration.json`, `data/predmkt.json`,
`data/criticality.json`, `data/discovery.json`, `data/sowhat.json`, `data/signal_registry.json`,
`data/gaps.json`. Grades follow `docs/OIL_FINDINGS.md`: **TESTED** (interval + multiplicity
correction where a family exists), **DESCRIPTIVE**, **NULL**, **CASE**. Report only — no published
surface was edited.*

**Headline: the most important thing in this block is not a finding, it is a contradiction.**
`data/signal_registry.json` — the project's machine-readable statement of what it currently believes
— still carries H1 as **live** with Bonferroni-surviving evidence, a claim the paper and the conceded
adversarial review **publicly retracted**. Two other files carry the same stale belief.

> **RESOLVED 2026-09-03, and the scope was larger than this sweep found.** §1's contradiction is
> fixed. A generic guard (`tests/test_retraction_guard.py`, in the DB-free CI gate) now walks every
> `data/**/*.json` and fails if a claim adjudicated as retracted or downgraded is marked live anywhere;
> `src/retractions.py` reads the verdicts from `data/evidentiary_bar.json` rather than restating them.
> Running it found **eight** affected files, not the three named here — `domain_conditioning.json` and
> `engine_read.json` were carrying the same stale beliefs and nobody had looked at them. All eight are
> marked in the propagation-graph convention: every figure kept, status changed, dated pointer added.

---

## 0. Provenance caveat that caps three of these files

| file | tracked? | consequence |
|---|---|---|
| `corroboration.json` (896 KB), `predmkt.json`, `criticality.json` | **gitignored, regenerated every run** | a result read off them is **not reproducible from the repo**. Nothing from these three can be graded above DESCRIPTIVE, and anything time-varying cannot be cited at all without pinning the `_sample` receipt. |
| `discovery.json`, `sowhat.json`, `signal_registry.json`, `gaps.json` | tracked | citable |

Cited by any document: `sowhat.json` and `signal_registry.json` appear in
`docs/red_team_2/D1_registration_audit.md`. **The other five are cited by nothing.**

---

## 1. CONTRADICTION — the signal registry still calls H1 live after the project retracted it

**This is the finding of the block.** Three sources agree H1 was downgraded; the registry did not follow.

**What the project published:**

- `data/placebo_vixmatched.json` (2026-08-15), the receipt: `raw_car.real_amp = 5.5615`,
  `raw_car.pseudo_mean = 3.0438`, `p_real_le_pseudo = 0.0695`, **`interpretation.raw_real_inside_pseudo_ci = true`**, over 2,000 pseudo samples.
- `docs/red_team_1.md` R2: *"**CONFIRMS vol-clustering.** … real +5.56pp lies **inside** the pseudo band (p=0.07 …). The raw amplification is reproduced by non-events → **not an event ripple**."* H1 is moved **validated → SUGGESTIVE**.
- `docs/PAPER_DRAFT.md` §15: *"the original headline (H1, stress amplification of +5.56pp) reproduced exactly and then fell inside a VIX-matched pseudo-event band; every previously 'validated' claim was downgraded to SUGGESTIVE."*

**What `signal_registry.json` says today:**

```
signal_id: h1_vix_conditioning        status: live
evidence:  amp 6.0412pp, 95%CI [1.557, 10.087], FDR q=0.0072,
           survives_bonferroni=True; walk-forward OOS +7.64pp
```

No mention of the placebo, of red_team_1, or of the downgrade. The registry is the only place a
consumer would look to ask "what does this project currently claim?", and it answers with a retracted
claim dressed in its strongest statistics.

Note also the amplification differs between surfaces — **6.0412pp** in the registry against
**5.5615pp** in the placebo receipt and **5.56pp** in the paper. Two numbers for one quantity, and the
larger one is the one still labelled live.

**Grade: CONTRADICTION (highest severity in this sweep).** The registry does not merely omit the
downgrade; it asserts the opposite status.

### 1b. The same stale belief in two more files

- **`discovery.json`** labels its VIX hit `"status": "re-discovered H1 (already validated)"` and its
  message reads *"Discovery re-found H1 (VIX->|CAR20|) from scratch -- a good check that the scan
  works."* H1 is not "already validated"; it is downgraded. **And the rediscovery does not answer the
  objection**: the placebo's claim is that *non-events* reproduce the amplification, which a
  correlation scan over real events cannot detect. Re-finding H1 is evidence the scan works, not
  evidence H1 survives.
- **`sowhat.json`** runs operationally on the H1 regime — `"regime": "ON"`,
  *"Regime is ON (VIX-stress elevated)"* — while simultaneously reporting
  `"validated_propagation": []`. It is conditioning the live read on a downgraded signal.

**Grade: CONTRADICTION (secondary).**

### 1c. The registry applies the vol-clustering standard unevenly

`realized_vol_magnitude` is held at `experimental` with the note *"likely volatility clustering --
needs the standardization defeater before promotion."* That is the **same confound** the placebo used
to defeat H1. The registry knows the standard, applies it to the candidate, and does not apply it to
the live signal. **Grade: CONTRADICTION (internal to one file).**

---

## 2. [NULL — and the most useful methodological result here] The strongest raw correlation in the discovery scan reverses sign out of sample

`discovery.json`: a falsification-first scan over 28 candidates at FDR *q* = 0.10; 4 pass FDR, 3 are
reported as survivors. The one that passes FDR and is **dropped**:

| feature → outcome | in-sample *r* | *n* | perm *p* | BH *q* | **out-of-sample *r*** | OOS holds |
|---|---:|---:|---:|---:|---:|---|
| `derived.cot_pct` → `abs_car20` | **−0.397** | 54 | 0.0026 | **0.0364 ✓** | **+0.194** | **false** |

It is the **largest |r| in the entire scan** and comfortably FDR-significant, and its sign **flips**
out of sample. It is dropped by the scan's own OOS gate — the gate working exactly as designed.

This deserves publication because it is a clean, self-generated demonstration of the project's own
central thesis about in-sample screening, and it costs nothing to state. **Grade: NULL** (a test run
and not sustained).

Corroborating it from a second direction: `signal_registry.json` records **H3 (crowded positioning
amplifies)** at amp **−8.05pp, 95% CI [−13.97, −2.18]**. Two independent routes find COT negatively
related to ripple magnitude, and neither survives.

**A wording objection on H3.** The registry's evidence string says *"CI excludes 0=True (was
small-sample noise at n=20)"*. Calling an interval that excludes zero "noise" is a characterisation
the interval does not support. Under `BRIEF_SKELETON.md`'s registered rule — *"holds if the clustered
amplification exceeds +5pp **in the predicted direction**"* — H3 fails because it is **−8pp, the wrong
direction**, not because it is noise. The correct statement is available and stronger; the file
should use it. **Grade: DESCRIPTIVE defect.**

---

## 3. [DESCRIPTIVE] The gap ledger has no aggregate skill, and large separation in its tails

`gaps.json`, 248 gaps, 247 scored: the engine's H1-conditioned turbulence view against OVX, Brier-scored.

**Aggregate: null.** Brier 0.2450 against a base-rate Brier of 0.2495 — **skill vs base = 0.0045**.

**Tails: not null.** Turbulence base rate 52.2%.

| gap direction | *n* | turbulence rate | Wilson 95% | Brier |
|---|---:|---:|---|---:|
| **under-priced risk** | 15 | **93.3%** | [70.2, 98.8] | 0.173 |
| aligned | 213 | 52.1% | [45.4, 58.7] | 0.254 |
| **over-priced fear** | 19 | **21.1%** | [8.5, 43.3] | 0.202 |

Under-priced minus over-priced is **+72.2 pp**, and **the two intervals do not overlap** (70.2 against
43.3). The aggregate null is driven by the 213 "aligned" cases where the engine is saying nothing;
the 34 cases where it takes a position separate sharply.

**Why this is DESCRIPTIVE and not TESTED:** no multiplicity correction over the direction split, no
out-of-sample validation, small *n* in both tails, and the direction categories are defined from the
same data they are scored on. It is a striking rate difference of exactly the kind
`OIL_FINDINGS.md` §4 already flags as "testable, not yet tested".

**It is unreported, and it is the most promotable thing in this block** — it needs an OOS split, not a
new idea.

### 3b. The H1 regime split, and why it is not independent evidence

*Pre-registration gate checked first:* `CLAUDE.md` bars summarising the conditioned H1/H2/H3
comparison until VIX, EIA inventories and COT are all loaded. All three are present in `data/oil.db`
(`fred.VIXCLS` 9,264 obs; `eia.crude_stocks_xspr` / `distillate_stocks` / `gasoline_stocks` /
`spr_stocks`; `derived.cot_pct` 7,030 obs), so the gate is discharged.

| regime | *n* | turbulence rate | CI 95% |
|---|---:|---:|---|
| turbulent (ON) | 140 | 58.6% | [50.3, 66.4] |
| calm (OFF) | 107 | 43.9% | [34.9, 53.4] |

ON − OFF = **+14.7 pp**, which exceeds the registered +5pp rule — **but the intervals overlap** (ON
lower 50.3 < OFF upper 53.4), and, decisively, **§1's placebo objection applies to this too**: if
VIX-matched non-events reproduce the amplification, a VIX-conditioned regime split on real events
inherits the same confound. **Grade: DESCRIPTIVE, and not independent evidence for H1.**

---

## 4. [DESCRIPTIVE] `corroboration.json` — two defects in the corroboration scoring

896 KB, gitignored, cited by nothing. Method: *"weight-of-evidence over independent domains +
cross-modal votes … Correlated reprints collapse; certainty capped; multi-modal = confirmed beyond
headlines."*

| situation | multi-modal / events | rate | Wilson 95% | top item's modalities | top confidence |
|---|---:|---:|---|---:|---:|
| israel_iran_war_2025 | 249/528 | 47.2% | [42.9, 51.4] | 3 | 0.778 |
| israel_lebanon_hezbollah | 214/451 | 47.5% | [42.9, 52.1] | 3 | 0.778 |
| russia_ukraine_war | 24/147 | 16.3% | [11.2, 23.1] | 2 | **0.933** |
| china_taiwan_tension | 4/63 | 6.3% | [2.5, 15.2] | 2 | **0.933** |

**Defect 1 — the same headline is the top item for two different situations.** *"Iran war live:
Tehran–Oman talks on Hormuz 'positive'; ship hit in Red Sea"* is the top-corroborated item for **both**
`israel_iran_war_2025` **and** `israel_lebanon_hezbollah`. The method's stated protection is that
"correlated reprints collapse"; an Iran-war headline ranking as the strongest evidence for the
Israel–Lebanon situation is the failure that protection exists to prevent.

**Defect 2 — confidence is not monotone in corroboration breadth.** A **2-modality** GDELT
auto-signal scores **0.933**, above a **3-modality** corroborated item at **0.778**. For a file whose
thesis is "multi-modal = confirmed beyond headlines", the score ranks a narrower item above a broader
one.

Related, and substantive: the top item for `russia_ukraine_war` is
*"[GDELT] UNITED ARAB EMIRATES / RUSSIAN: fight/clash signal"* — a machine-generated dyad ping that is
not a Russia–Ukraine event. **Grade: DESCRIPTIVE defect ×2.** No published document relies on this
file, so nothing downstream is currently wrong; the risk is if it is ever promoted.

---

## 5. [DESCRIPTIVE] `sowhat.json` — an unreconciled denominator

`base_rate_ripple_by_type` reports CAR by event class on *n* = 29 (OPEC), 16 (sanctions), 15
(conflict escalation), 14 (policy response), 7 (demand shock), 7 (infrastructure attack). The same
classes elsewhere in the project carry *n* = 51, 55, 50, 56, 17, 45
(`big_moves/summary.json`, `p_big_given_class`).

Two files report a per-class quantity over the same corpus with denominators differing by up to
**6×** (infrastructure attack, 7 against 45) and neither states which subset it is on. Whichever is
right, a reader comparing them is misled. **Grade: DESCRIPTIVE defect.** Not a contradiction of a
published claim, because nothing published cites `sowhat.json`'s rates.

Also worth recording plainly: `"validated_propagation": []` — the file's own answer to what the
engine can currently claim about propagation is *nothing*, which is consistent with
`OIL_FINDINGS.md` §9.

---

## 6. No findings: `criticality.json`, `predmkt.json`

Both are explicitly and correctly self-labelled **DISPLAY/context**, and neither feeds a statistic.

- **`criticality.json`** — a sourced reference table (USGS MCS 2025, `criticality.yaml`): China at 99%
  of gallium and critical for 9 commodities, Netherlands 100% of EUV lithography, Taiwan 92% of
  advanced semiconductors. Its own note: *"DISPLAY/context; transmission magnitude is a later
  calibrated step."* Nothing to promote. Worth one observation: this is **critical-minerals scope, not
  oil**, and it is the only place that scope appears.
- **`predmkt.json`** — 169 Polymarket markets, self-labelled *"never fed to the registered
  statistics … thin markets are unreliable."* One datum is striking enough to record: *"Strait of
  Hormuz traffic returns to normal by August 31?"* trades at **prob 0.0005** on **$17.9M volume**.
  Risk-neutral and display-only, so **CASE at best** — but a market that liquid pricing normalisation
  at 5 basis points is a market-implied statement about the 2026 closure that no document mentions.

---

## 7. What to do, in order

1. **Reconcile `signal_registry.json` with the published downgrade.** H1's status is `live` and
   should not be. Whoever owns the registry should either demote it to SUGGESTIVE with the placebo
   receipt attached, or publish the argument that defeats the placebo. Also fix `discovery.json`'s
   "already validated" label and `sowhat.json`'s regime conditioning. **Nothing else in this list
   matters as much.**
2. **Reconcile the two H1 amplification figures**, 6.0412pp against 5.5615pp.
3. **Promote the COT sign-reversal** (§2) into `OIL_FINDINGS.md` as a NULL. It is free and it argues
   the project's own case.
4. **Give the gap-ledger tails an out-of-sample split** (§3). It is the most promotable unreported
   result in this block.
5. Re-word H3's "small-sample noise" to the registered-rule statement (§2).
6. Fix the two `corroboration.json` scoring defects before that file is ever cited (§4).
7. State which subset `sowhat.json`'s per-class *n* is on (§5).

## 8. Receipts

`data/signal_registry.json` · `data/discovery.json` · `data/gaps.json` · `data/sowhat.json` ·
`data/corroboration.json` · `data/criticality.json` · `data/predmkt.json` ·
`data/placebo_vixmatched.json` · `docs/red_team_1.md` R2 and its status table ·
`docs/PAPER_DRAFT.md` §15 · `BRIEF_SKELETON.md` §decision rule · `data/big_moves/summary.json` ·
`data/oil.db` for the state-variable check. Wilson 95% intervals computed in this pass, not stored.
