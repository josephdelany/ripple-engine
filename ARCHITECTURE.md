# The instrument: four modules, and what each one is worth

*2026-09-03. What this project is, stated in the architecture it has always implied. Written after
the exposure attempt, so the status of each module is measured rather than asserted.*

---

## The design

The goal was a history-trained instrument over the petroleum complex — crude, refined products,
cracks, gas and LNG, fertilizer, freight — that reads an event, places it against the historical
record, and produces a distribution over what follows.

That design has a name and a standard decomposition. It is the architecture of a **catastrophe
model**, which resolves into four modules ([NAIC](https://content.naic.org/cipr-topics/catastrophe-models-property);
[CAS](https://www.casact.org/sites/default/files/old/las_2019_reinsurance_bootcamp_sigona.pdf)):
**hazard**, **vulnerability**, **exposure**, **financial**. And its retrieval step is
**reference class forecasting** in Flyvbjerg's sense — identify a class of comparable prior cases,
establish the distribution over that class, place the new case in it — a method developed from
Kahneman's work on optimism bias and formally endorsed by the American Planning Association in 2005
([Flyvbjerg et al.](https://arxiv.org/pdf/1710.09419)).

Naming the architecture matters for one reason above all: **in a catastrophe model the exposure
module is supplied by the user, not shipped by the model.** RMS and Verisk do not distribute a
register of every building on earth; the client supplies the portfolio and the model supplies the
hazard catalogue, the damage functions and the financial translation. A petroleum instrument that
asks its operator "which facility, what capacity, what criticality" is therefore not incomplete. It
is built the way instruments of this class are built.

---

## Module status, measured

| module | what it supplies | status |
|---|---|---|
| **Hazard** | the event catalogue and reference-class retrieval | **BUILT.** 313 dated events 1956–2026; walk-forward protocol with reads sealed by hash before outcome lookup; state-conditioned retrieval at *k* = 12; Hedge online re-weighting. Tested against four baselines under DM, stationary bootstrap, SPA, permutation, FDR and a 162-cell specification curve. |
| **Financial** | volume-days lost → price and margin response across the complex | **BUILT.** 53-node propagation chain (crude → products → cracks → gas/LNG → fertilizer → freight → credit), 772 series, six scored grid targets, local projections with cluster-collapsed inference. |
| **Exposure** | which asset, what capacity, what criticality | **SCHEMA BUILT, POPULATION MEASURED AND LARGELY UNRECOVERABLE.** See below. |
| **Vulnerability** | capacity damaged → duration of outage | **BLOCKED ON EXPOSURE.** Registered as a two-stage model; the registered gate of 30 COMPLETE cases was not met. |

---

## What the exposure attempt found, and why it is a result rather than a gap

`EXPOSURE_REGISTRATION.md` specified six required fields per event with an absolute rule: **every
figure names a source and a date, or the field stays `unknown`.** Six independent sessions
researched 75 physical-disruption events — 48 infrastructure attacks and 27 chokepoint disruptions
— with every route logged.

**Result: 8 COMPLETE of 75 (11%), 46 partial, 21 empty.** The registered gate was 30. It was not
met, and §5's consequence stands: Stage 1 is descriptive only and no verdict issues.

The five walls, each found independently and each logged:

**1. Category mismatch.** Roughly 40% of the 75 have no point asset by construction — tanker
attacks, sector-wide labour strikes, naval escort operations, multi-refinery aggregate rows. The
schema has no vessel `asset_type`, and a ship has a cargo in barrels, not a throughput in barrels
per day. **The denominator was never 75.**

**2. Units are not comparable across reporting conventions.** Russian operators publish refinery
capacity in **tonnes per year** and never in barrels per day. Every b/d figure in circulation is a
Western conversion at an unstated barrels-per-tonne factor — which is why published figures for the
same plant disagree (240 vs "around 250" for Tuapse; 314 vs 300 for Volgograd). Selecting one is an
assumption wearing a source's clothes.

**3. The two fields that define vulnerability are exactly the two the belligerents contest.**
`capacity_affected_kbd` and `days_to_full_restore` are what an operator minimises and an attacker
maximises. Volgograd, February 2024: Lukoil reported operations unaffected; the regional governor
reported a blaze; Reuters' sources reported CDU-1 damaged, ~40% of the plant, ~140 kb/d; a Ukrainian
defence source claimed the fire was organised by SBU drones. **Neither figure is independently
verifiable and both cannot be recorded, so the field stays unknown.**

**4. Restoration dates are forecasts, not confirmations.** Abqaiq 2019 — the best-documented event
in the corpus, with Aramco publishing nameplate, affected volume and partial restore directly —
still failed to reach COMPLETE. Every source gives an *expectation* ("by the end of September") and
none confirms a realised date. A near-fill from the energy minister's 3 October statement was caught
and rejected: he reported capacity at **11.3 mb/d against a pre-event maximum sustainable 12**, so
at day 19 capacity was demonstrably *not* restored. **The most transparent operator in the industry
does not publish the field the model needs.**

**5. The contemporaneous archive is unreachable for the historical arm.** For 1977–2006:
web.archive.org does not resolve for this client, a purpose-built pipeline-attack register fails on
a TLS certificate mismatch, and the contemporaneous wire copy returns 403 and 404. **Block A
returned zero COMPLETE of 13** — and that is an archival finding, not a research failure.

**Two sourced zeroes are worth naming**, because they are data and not gaps: Shaybah and Ras Tanura
were attacks that struck and changed nothing — *"no interruptions to Saudi Aramco's oil
operations"*, *"no casualties or property loss"*. They are the low end of the vulnerability
distribution and any honest model needs them.

---

## What this establishes

The project's thesis requires a physically-denominated magnitude. Session C's Stage 0 established
that the alternative — a 0/1 event flag — carries no incremental information about the response
(band covering zero at −1.572, against +2.230 for a continuous measure of the same events on the
same 44 days, with the flag collapsing to −0.483 when both are present).

This attempt establishes the complement: **for conflict-caused disruptions, the physical magnitude
is not recoverable from public sources.** Not expensive, not slow — *not recoverable*, for five
specific and independently-encountered reasons. Belligerents contest the two fields that matter,
units are not comparable, restoration is announced as forecast, the archive is closed, and a large
share of the events have no point asset at all.

**That is a complete answer to the thesis question, and it generalises beyond this project.** Any
geopolitical supply-risk product built on public data meets the same five walls. The honest
conclusion is not that the instrument was built badly, but that **the layer it depends on does not
exist in the public record, and now there is a measurement of how far short it falls: 11%.**

---

## What remains buildable, and where the instrument does work

- **The hazard and financial modules are built and tested.** They are the two-thirds of the
  architecture that public data supports.
- **The exposure module works as designed when an operator supplies it** — which is the standard
  arrangement in this class of model, and the reason the live read is a real capability rather than
  a placeholder.
- **The vulnerability module can be fitted on a reference class the record does support.** Where
  cause is a covariate rather than a filter, accident-caused outages — hurricanes, fires, technical
  failures — are publicly tracked with confirmed restoration dates, consistent units and no
  belligerent contesting the figures. The **contrast in completion rates between accident-caused and
  attack-caused disruptions is itself a measurement of the information environment of conflict.**
