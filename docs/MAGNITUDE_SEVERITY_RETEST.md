# `severity_dose_response`: RETRACTED

*2026-09-03, Session C. The re-test registered in `MAGNITUDE_REGISTRATION.md` §5 and sealed at
`8cb9d3d` — verdict words fixed **before** this ran. Computed by `src/magnitude_severity_retest.py`,
which imports its estimator from `src/ripple_lp.py`. Results in `data/magnitude/severity_retest.json`.
`data/edge_battery.json` is **not edited**; the status is reported for the owning session, exactly as
Amendment B did with the six `propagation_edges`.*

## The claim, as published

`data/edge_battery.json` carries, as **`validated: true`**:

> "high-severity (4-5) events ripple harder into oil than low-severity (1-2): a monotone
> dose-response"

**amp +5.079 [+1.003, +9.364]**, n = 116 (76 high / 40 low), permutation p = 0.0303, survives
BH-FDR at q = 0.10 (rank q = 0.079), **fails Bonferroni** (adjusted 0.394). The object is
mean |CAR+20| in Brent for severity ≥ 4 minus the same for severity ≤ 2.

## Verdict

| test | n | estimate | placebo | verdict |
|---|---|---|---|---|
| **A — the claim as published, vs a state-matched placebo** | 52 high / 39 low | **+2.071 [−4.067, +8.209]** | 95.8th pct, **inside** | **NULL** |
| B — the same events as ripple cells, Brent h = 20 | 50 high | −1.391 [−6.451, +3.670] | 10.2 | NULL |
| B — " | 37 low | −2.248 [−7.904, +3.408] | 2.6 | NULL |

**Registered status: RETRACTED.** Permutation p on the de-overlapped sample is **0.269**, against the
published 0.030.

Test B is worth reading beside it: estimated as ordinary ripple cells, both severity groups have a
**negative** 20-day Brent response, and the *low*-severity group's is the larger in absolute value
(−2.25 versus −1.39). That is the dose-response pointing the wrong way, at n's that cannot support
reading it either.

---

## Why it did not survive: two defects, both inflating significance

### 1. The registered one — it never looks at a non-event day

The published test compares **events to other events**. A world in which nothing transmits, but
severe events happen during wars and crises while mild ones happen on quiet days, passes it: |CAR| is
larger in volatile periods whether or not the event did anything. This is the same defect on which
v2 §3 retracted five of six `propagation_edges` — the repo had already conceded it as red-team
attack #2, *"it cannot tell them apart."*

The re-test builds the null the published test never did: for each real event, draw a pseudo-event
matched on **that event's own (VIX decile, GPR decile) at t−1** from days at least 30 days from any
event, and take the same high-minus-low difference. The spread of that distribution is the gap the
**state mix alone** produces.

| | observed | matched-placebo null |
|---|---|---|
| high-minus-low mean \|CAR+20\| | **+2.071** | mean −0.090, central 95% **[−2.306, +2.192]** |

The observed gap sits at the **95.8th percentile** — inside the placebo distribution, and the
registered threshold is 97.5. **The volatility and geopolitical-risk mix of severe events accounts
for the gap.** Nothing needs to have rippled.

### 2. A second defect, found while replicating the published n

`edge_battery._oil_type_frame` clusters **within event type**, and its comment explains why: the
neighbouring test compares chokepoint events against sanctions events, and clustering all types
together let a chokepoint within 35 days of a sanction be cannibalised, "starving the chokepoint arm
to n=3". That is the correct unit *for that test*. `severity_dose_response` inherits the same frame
unchanged — but **its grouping variable is severity, not type**, so two high-severity events of
different types ten days apart both survive as independent observations.

| severity arm | raw events | clustered **within type** (used) | clustered **within severity group** (required) |
|---|---|---|---|
| high, ≥ 4 | 106 | **92** | **56** |
| low, ≤ 2 | 49 | 48 | 41 |

Thirty-six overlapping same-severity episodes were counted as independent. The unit of dependence for
a severity comparison is the episode; clustering within type does not de-overlap the severity arms.
This is the same class of error as the unit-of-dependence defect found in the grid price arm
(`a7fbae9`) — an n that counts correlated observations as independent, which narrows every interval —
and it is not carelessness: it is a fix that was right for one test being inherited by a neighbouring
test where it is not.

Both defects push the same way. Correcting either weakens the claim; correcting both removes it.

---

## The severity column: my own Tier 1 report was wrong, and here is the correction

`MAGNITUDE_REGISTRATION.md` §5 reported that **102 of 313** events sit exactly on the deterministic
`SEV_BAND` value `admit_events.py` assigns to auto-admitted candidates, and called that "an upper
bound on how many are class-imputed". It was correctly *labelled* an upper bound. Resolved, the true
count is different:

| check | result |
|---|---|
| events whose severity equals its class's `SEV_BAND` value | 102 |
| `data/extract/admission_log.csv` exists? | **no** |
| current events carrying an `AUTO-ADMIT` rec_reason | **0** |
| current events found in `candidate_review.csv` | 32 — **all `joe_decision=approve`** |
| **demonstrably class-imputed severities in the live corpus** | **0** |

**The defect is latent, not live.** The mechanism exists in `admit_events.py` and *would* put a
measured and an inferred value in one column — which is what INV-5 forbids — but it has not run
against this corpus. The 102 overlap is what chance predicts: `SEV_BAND`'s values are 3 and 2, which
are the modal severities of a 1–5 ordinal.

**The live issue is different and simpler.** `severity` carries no per-value source anywhere. It is
**uniformly analyst judgement** — not mixed, so not an INV-5 violation, but **inferred throughout**,
and it may never be read as a measured magnitude. Under `MAGNITUDE_REGISTRATION.md` §2.1's ruling it
is therefore admissible only as a labelled-inferred ordinal comparator, and never as M-Q.

### The registered robustness split turns out to be one-sided, and must not be read as the cleaner number

§5 registered that every severity result be reported twice — all events, and hand-coded only. With
provenance resolved, "hand-coded" is *all* events, so the split was run on the strictest reading of
the original concern instead: excluding the 102 on-band events. **That split is not neutral for this
test**, and the reason is arithmetic:

`SEV_BAND`'s values are {2, 3}. Severity 3 is in neither group (high is ≥ 4, low is ≤ 2), and
severity 2 is in the **low** group only. So the split removes **14 low-severity events and zero
high-severity events**.

| split | n high | n low | diff | perm p | placebo pct |
|---|---|---|---|---|---|
| all events | 52 | 39 | +2.071 [−4.067, +8.209] | 0.269 | 95.8 |
| off-band only | 52 | **28** | +4.223 [−0.162, +8.609] | 0.064 | 100.0 |

The off-band estimate is larger **because the restriction strips the low arm and cannot touch the
high arm**. Its band still covers zero and it is reported for completeness, but it is an artefact of
a one-sided filter and is not evidence for the claim. Recording this is the point of running both.

---

## What this does not say

- It does not say severity is meaningless. It says this test, at this n, with a state-matched null,
  cannot distinguish a severity dose-response from severe events happening in volatile times.
- It does not re-open the six `propagation_edges`; those were ruled on separately.
- It does not touch `data/edge_battery.json`. Two of the three claims that file lists as `validated`
  (`copper_growth`, `hy_credit_stress`) are **state-conditioned amplification** edges scored by the
  same gate, and this re-test says nothing about them individually — but they share the defect that
  gate has, and the same treatment is available to whoever owns them.

## Provenance

Run `2026-09-03`, seed 19900802, 500 placebo draws, 10,000 permutations. Estimator imported from
`src/ripple_lp.py`. Every number above is in `data/magnitude/severity_retest.json`:
`published_claim`, `severity_provenance`, `clustering_unit_check`,
`test_a_claim_as_published.{all_events,off_class_band_only}`, `test_b_ripple_cells`, `verdict`.
Tests: `tests/test_magnitude_severity_retest.py`.
