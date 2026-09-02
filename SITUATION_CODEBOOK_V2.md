# Situation Record codebook (v2) — REGISTERED before coding

Codebook amendment for RIPPLE_ENGINE_V2_SPEC §4.1–4.2. Committed **before** any event is
coded (register-then-run; git timestamp is the seal). Governs how every corpus event — and
every live intake item — is turned into a Situation Record.

## Master coding rules (apply to every field)
1. **Sourced or `unknown`.** Every field is coded from a citable source (URL / named report)
   recorded in a per-field source column, or left `unknown`. No field is ever guessed.
2. **Never from outcomes.** A field describes the state *as known at/around the event date*
   (point-in-time). It is never inferred backwards from how the market or conflict resolved.
   Hindsight is a coding error.
3. **Human-gated.** The caged extractor proposes; codings below a confidence threshold go to
   the borderline queue for the analyst (B1 Joe-gate). Nothing enters canon un-gated.
4. **Enums are closed.** Values outside the listed vocabulary are `unknown` (or queued), never
   invented.

## PHYSICAL block (what was hit; the supply side)
| field | type | criteria | source |
|---|---|---|---|
| `asset_hit` | text | the specific named asset (facility, terminal, field, vessel). `unknown` if the source names no specific asset. | required if not unknown |
| `asset_role` | enum {export_terminal, processing, chokepoint, pipeline, production_field, refinery, storage, other} | the asset's function in the oil system, per source/asset reference. | required if not unknown |
| `outputs_affected` | list<commodity> | the products/commodities the asset produces or handles that are put at risk (e.g. crude, LNG, helium, naphtha). From the asset's known outputs, not speculation. | ref |
| `output_share` | ordinal {negligible, minor, moderate, major, critical} | approximate share of national/regional/global supply the asset represents, bucketed; cite the share figure. | required if coded |
| `volume_at_risk` | number (mb/d) + basis | barrels/day plausibly interrupted, from a source; else `unknown`. Stored with its basis string. | required if coded |
| `spare_capacity_at_time` | number/ordinal | OPEC/market spare capacity available at the event date (EIA/OPEC), point-in-time. | EIA/OPEC |
| `substitutes_at_time` | text/ordinal {none, limited, ample} | availability of rerouting/substitute supply at the time. | ref |
| `downstream_chain` | derived | the value-chain path from the affected output, taken from the ripple graph — **auto-derived, not hand-coded** (so it is not a source-coded field). | graph |

## GEOPOLITICAL block (who, and the state of the world)
| field | type | criteria | source |
|---|---|---|---|
| `actor` | entity | the party taking the action (striker / sanctioner / decider). | required if not unknown |
| `target` | entity | the party acted upon. | required if not unknown |
| `actor_response_propensity` | derived (0–1) | the actor's own historical share of situations that escalated (LIMITED/ WIDENING) — **computed from the corpus in B1, never hand-coded**; shown with n. | corpus |
| `target_response_capacity` | ordinal {none, limited, significant} | the target's sourced military/economic capacity to respond at the time. | ref |
| `alliance_engagement` | enum {none, diplomatic, material, military} | the highest level at which third-party allies/coalitions were engaged at the event date. | ref |
| `conflict_scope` | enum {isolated, campaign, war} | isolated incident vs an ongoing campaign vs a declared/de-facto war, at the event date. | ref |
| `tempo` | enum {first, nth} | first clash in this actor→target dyad within the situation, or a repeat. | derived+ref |
| `diplomatic_state` | enum {talks, sanctions, ceasefire, none} | the dominant diplomatic posture between the parties at the event date. | ref |
| `prior_outcome_in_dyad` | enum {CONTAINED, LIMITED_RETALIATION, WIDENING, RESOLUTION_BY_DEAL, none} | the realized branch of the most recent prior clash in this dyad (a link to a prior record), or `none`. | corpus |

## MARKET / POLICY block (retained, already derived)
`vix_pct`, `inv_sigma`, `cot_pct`, `gpr`, `curve`, `spr_posture`, `opec_posture` — read
point-in-time from `oil.db`/`belief_state`. Already sourced by the existing pipeline.

## Scenario taxonomy (Layer G outcome branches)
Exactly four mutually-exclusive, collectively-exhaustive branches, observed from sources at
**+30 and +90 calendar days** after the event (the geopolitical outcome, NOT the market move):
- **CONTAINED** — no material military response; the situation stays localized or de-escalates without further strikes.
- **LIMITED_RETALIATION** — a bounded, proportional response (a counter-strike / reprisal) that does not widen beyond the dyad.
- **WIDENING** — escalation drawing in additional actors, theaters, or a sustained campaign.
- **RESOLUTION_BY_DEAL** — a negotiated de-escalation: ceasefire, agreement, or sanctions/diplomatic settlement.

**Outcome-observation rule.** Code the *dominant observed state* at +30d and at +90d from
sources (two independent where possible). If the two horizons differ, both are stored (the
+90d is the headline branch). If unresolved or under-sourced, `unknown` — never assigned to
fit a pattern. The branch is the realized *geopolitical* outcome; the market reaction is Layer
P's separate, measured object.

## What is NOT in a Situation Record
Any price/flow reaction (that is Layer P, measured from series, never coded here); any
probability of occurrence; any field derived from the outcome. Keeping these out is what makes
the record a clean, point-in-time input the walk-forward can trust.
