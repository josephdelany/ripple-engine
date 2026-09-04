> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# PHYSICAL EXPOSURE — registration, written before any code

*2026-09-03. Registered by Cowork before `src/exposure.py` exists. The project's rule holds: this
document is committed first, and the verdict words below are fixed before a number is computed.*

---

## §0 Why this study exists

Stage 0 (`MAGNITUDE_REGISTRATION.md`, sealed `8cb9d3d`) established, on the 44 days that are both
a corpus `opec_decision` event and a Känzig announcement day, that a **0/1 event flag carries no
incremental information** about the price response (band covers zero, −1.572) while a **continuous
measure of the same events does** (+2.230, excludes zero), and that the flag **collapses to
−0.483** once the continuous measure is present. Our own `severity` ordinal fails too, and
Amendment C-1 bars it from serving as a magnitude.

Stage 0 could not construct a magnitude for non-OPEC classes: *magnitude is belief, not barrels.*
**This study constructs the barrels.**

It is also the study the project's stated thesis requires. `docs/VISION_AND_BUILD.md` establishes
that the built environment vector is 13 macro-financial fields and 4 dyad flags, and that the
missing layer is physical — capacity at risk, facility criticality, outage duration. This
registration builds the part of that layer reachable from data already in the tree or licensed
locally, and **registers the remainder as unobserved rather than skipping it silently.**

## §1 The estimand

For each corpus event *i* at date *t*, a **continuous, physically-denominated exposure** `X_i`,
and the question: **does `X_i` carry information about the response of the petroleum complex that
the class dummy does not?**

Targets, in the order they are scored — the response is across the complex, not crude alone:
crude (Brent, WTI) · refined products (diesel, gasoline, jet) · **cracks** (diesel, gasoline) ·
gas/LNG (Henry Hub, propane) · fertilizer · freight proxy. Horizons *h* ∈ {0, 1, 2, 5, 10, 20, 40, 60}
trading days, headline **h = 20**.

## §2 The exposure construction — mechanical, no judgement

Three tiers. **Every term is read from a register published strictly before *t*.** No term is
coded per event by a human, so the severity-ordinal failure cannot recur through this variable.

**T1 — country capacity exposure.**
`X1_i = Σ over countries c in the event's coded location/actor set of CAP(c, vintage(t))`
where `CAP` is crude production capacity and, separately, refining capacity, in kb/d, from the
most recent register with a publication date `≤ t`. Reported in kb/d and as share of world.

**T2 — chokepoint exposure.**
`X2_i = FLOW(k, vintage(t)) / WORLD_SEABORNE(vintage(t))` for chokepoint *k*, where `FLOW` comes
from the last EIA *World Oil Transit Chokepoints* release before *t*, cross-checked against
PortWatch transits where PortWatch covers the date (2019→).

**T3 — the buffer, and the variable this study is really about.**
`X3_i = X1_i / SPARE(t)` where `SPARE` is `spare_capacity_opec` (EIA STEO Table 3d, monthly,
2003→, already loaded). **Dimensionless: the share of the world's spare capacity that this
disruption would consume.** This is the conditional the project's thesis asserts — the same
physical event matters differently depending on the buffer — and it is the primary regressor.

**Registered fallbacks.** Where `SPARE(t)` predates 2003, T3 is **null, not zero**, and the event
is excluded from T3 estimation and counted in the exclusion table. Where a country has no capacity
register before *t*, `X1` is **null, not zero**. Sourced-or-unknown applies to this variable as to
every other.

## §3 The vintage rule for capacity registers — the trap this must avoid

Capacity registers are annual and published with a lag. **A register's `knowable_at` is its
publication date, not its reference year.** The 2019 EI Statistical Review, published mid-2020,
may not inform a 2019 forecast. Capacity changes slowly, so using the last *published* figure is
both defensible and conservative. `WORLD_STATE_CODEBOOK.md` Amendment 1 governs, and every
exposure value carries its register's publication date. **A filtration test asserts no exposure
value derives from a register published after its event date.**

## §4 The four registered comparisons

Estimated as local projections on the corpus event dates, cluster-collapsed before inference, at
the unit of dependence the interval audit requires — **the source event, not the cell**.

| | regressor | tests |
|---|---|---|
| **A** | class dummy (status quo) | the current design |
| **B** | exposure `X3` (share of buffer consumed) | does physical magnitude carry information? |
| **C** | both together | does the dummy survive in the presence of magnitude? |
| **D** | exposure `X1` alone (unnormalised kb/d) | is the *normalisation by the buffer* doing the work, or the raw size? |

## §5 The verdict rule — fixed now, before any number

- **MAGNITUDE CARRIES** iff **B** beats **A** on the headline horizon with a band excluding zero,
  **and** the dummy's coefficient in **C** moves toward zero. *(This is the Stage 0 pattern,
  applied to a physical rather than a belief-based magnitude.)*
- **BUFFER MATTERS** iff **B** (normalised) beats **D** (unnormalised). This is the specific claim
  of the project's thesis and it is separately falsifiable.
- **NO ADDITION** iff B's band covers zero. **This is a permitted outcome and it is not a
  failure of the study** — it would close the loop Stage 0 opened, by showing that a properly
  constructed physical magnitude does not rescue the design either.
- Every result is reported with BH-FDR across the family and against a state-matched placebo.
  Nothing here can make anything VALIDATED: §7's label audit is unpassed.

## §6 Registered as UNOBSERVED, so the chain is tested with a named hole

The thesis includes a political-to-market channel: *mutual-defence pact → militarisation →
war-risk insurance → freight cost → price.* Two links are not measurable with available data:

- **war-risk insurance premia** — Lloyd's/commercial, not public
- **tanker freight rates** — BDTI/BCTI are licensed (established by session C)

The measurable substitutes are ATOP obligations plus any newer pact as state features, and
**PortWatch reroute distance** as a freight proxy. **The chain is therefore tested with two
unobserved links, and that is stated rather than skipped.** Registered prediction: if the
insurance/freight channel is material, exposure should predict the *reroute* response more
strongly than the *price* response — which is the Red Sea/Hormuz asymmetry, generalised and made
falsifiable.

## §7 Also registered as out of scope today

Facility-level capacity (no free global register), outage duration (no register), and
petrochemicals/plastics beyond fertilizer (Joe's scoping decision, 2026-09-03). Named so that
their absence is a recorded boundary rather than an implied capability.

## §8 What is being predicted, in advance, so it can be wrong

Cowork's expectation, written before the code: **T3 beats the dummy on the crack targets and not
on crude flat price**, because the Big Moves census already shows geopolitical classes 1.9–2.5×
more concentrated in large diesel-crack moves than in large crude moves, and because Red Sea vs
Hormuz shows physical disruption reaching price only when it cannot be rerouted. If T3 fails on
cracks too, the physical-magnitude hypothesis is in serious trouble and the honest conclusion is
that this corpus's events are not supply shocks — which R2 already suggests, at r = −0.023 with
the identified supply shock over 614 months.
