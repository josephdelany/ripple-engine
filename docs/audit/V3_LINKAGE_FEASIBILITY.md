# v3 linkage feasibility — can catalogue events be tied to detected impairment?

*2026-09-04. Run once, under `registrations/DISRUPTION_REALIZATION.md` §15–§17, against the frozen
episode table. No parameter was changed after seeing these numbers.*

Sources: UN Global Platform; IMF PortWatch.

## Verdict

**Linkage is identifiable but the registered rule is not fit for purpose. Its proportions must not
be quoted as findings.**

The geography mapping exists, is deterministic, and is exogenous — it was built by earlier sessions
for other purposes and predates all v3 work. That part of the design holds. What fails is the
**temporal** rule: it links an event to an episode only when the episode *starts* inside a 17-day
window around the event, and that rule cannot represent how these disruptions actually occur.

## The registered numbers, reported as computed

| quantity | value | 95% Wilson |
|---|---|---|
| **A** — eligible catalogue events linked to an episode | **4 / 17 = 0.235** | [0.096, 0.473] |
| **B** — detected episodes linked to an eligible event | **4 / 39 = 0.103** | [0.041, 0.236] |

Identical under the strict `[d, d+14]` window, so the two-day lead flagged in §24 changes nothing.

### Corrected eligibility attrition

The registration's §15 chain (313 → 171 → 75 → 21 → 18) was **arithmetically wrong** and is
corrected here rather than quietly restated. It counted only events dated 2019 or later at the
route-mapping step and then subtracted only the three 2019 events, missing both the seven
pre-2019 route-mapped events and the 2020-01-03 Soleimani event, which falls before the
2020-01-31 detection start.

| stage | events |
|---|---:|
| catalogue total | 313 |
| carrying a `role='location'` entity mapped to a PortWatch route | **28** |
| dated before the 2020-01-31 detection start (excluded) | 11 |
| **eligible** | **17** |

## Why the rule fails, with the evidence

The nearest episode to each eligible event, by offset in days between episode start and event date:

| event | route | offset | linked? |
|---|---|---:|---|
| Ever Given blocks the Suez Canal (2021-03-23) | suez | **0** | yes |
| Houthi drone strike triggers Red Sea diversions (2023-12-15) | bab_el_mandeb | +13 | yes |
| Houthis set tanker Sounion ablaze (2024-08-21) | bab_el_mandeb | +8 | yes |
| Houthis resume Red Sea attacks (2025-07-06) | bab_el_mandeb | +13 | yes |
| **Iran declares the Strait of Hormuz closed (2026-03-04)** | hormuz | **−3** | **no** |
| Houthi attacks disrupt Red Sea shipping (2023-12-01) | bab_el_mandeb | +27 | no |
| Houthis seize Galaxy Leader (2023-11-19) | bab_el_mandeb | +39 | no |
| US/UK first airstrikes on Houthi targets (2024-01-11) | bab_el_mandeb | −14 | no |
| Houthi missile hits Marlin Luanda (2024-01-26) | bab_el_mandeb | −29 | no |
| Houthi missile cripples Rubymar (2024-02-18) | bab_el_mandeb | −52 | no |

Three distinct failure modes, none of which is about physical reality:

**1. Anticipatory diversion misses by one day.** The Hormuz closure is the single largest episode in
the data — 183 days at 100% impairment — and it does not link. Tanker traffic collapsed on
2026-03-01, three days *before* the declaration. The registered lead is two days. The largest
disruption in the record is excluded by a one-day margin.

This is precisely the parameter §24 flagged as the one that prior observation could have
influenced. **It has not been widened.** Widening it now, having seen that it would capture the
Hormuz closure, is the post-hoc tuning this design exists to prevent.

**2. Slow-onset disruption falls outside a 14-day lag.** The Red Sea campaign was declared through
November and December 2023; sustained impairment at Bab el-Mandeb begins 2023-12-28. Two of the
three declaring events sit 27 and 39 days ahead of onset. A fortnight is too short for a
disruption that builds as shipowners progressively reroute.

**3. Events inside an ongoing episode can never link.** The rule requires the episode to *start* in
the window, so of the four Houthi events falling *within* the 242-day Bab el-Mandeb episode, none
count. One long episode absorbs a cluster of declarations and links to at most one of them.

Failure mode 3 also drives **B** down mechanically: 39 episodes cannot link to 17 events at better
than 17/39 even if every event linked to a distinct episode, and clustering makes the true ceiling
much lower. **B is close to uninformative by construction.**

## What may and may not be said

**May be said.** Under a preregistered onset-window rule, 4 of 17 eligible catalogue events on
PortWatch-covered routes are followed by the onset of a detected impairment episode within the
registered window; 35 of 39 detected episodes have no eligible catalogue event whose window
contains their onset.

**May not be said.** That roughly a quarter of declared disruptions are real. That most impairment
is undeclared, silent, unexpected, or ignored by analysts. Any causal statement. Any generalisation
beyond these 17 events, these 6 routes, and 2020–2026.

Unmatched episodes are **"not matched to the current event catalogue"** and nothing stronger. The
catalogue is curated, is not a census of declarations, and contains no entry for the 2023–24 Panama
Canal drought — which the detector found as 8 separate episodes including a 51-day one. That
absence is a property of the catalogue, not of the world.

## What a defensible linkage rule would need

For a future registration, written before it is run:

1. **Episode-overlap linkage, not onset linkage.** An event links if it falls within the episode's
   span, or within a registered window of its onset. This fixes failure mode 3.
2. **An asymmetric window justified by shipping response time**, derived from a source independent
   of these episodes — diversion decisions are made over weeks, so a 14-day lag is unmotivated.
3. **Explicit handling of event clusters.** Declare in advance whether an episode may link to many
   events, and whether A is computed per event or per cluster.
4. **A larger eligible set.** 17 events cannot support inference under any rule. The binding
   constraint is that only 28 of 313 catalogue events carry a route-mapped `location` entity. The
   highest-value data task is coding route geography for the remaining catalogue, under a written
   rule, before any further linkage is attempted.

## Status of this phase

Phase 1 (blind detection) is complete and reproducible. Phase 2 is **attempted and reported as
not usable**. The detector, its output, and its provenance stand on their own; the linkage
proportions above are published for auditability and are explicitly not results.
