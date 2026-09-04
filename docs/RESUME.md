# Verified résumé and interview language

This is the only current application document for the project. Every quantitative statement below is tied to `data/structural_surface/summary.json` or `data/structural_surface/ablation/summary.json`. Do not copy claims from `docs/RESUME_AND_APPLICATION.md`, which describes a superseded experiment.

## Recommended résumé entry

**Independent Research — Testing Historical Analogy in Geopolitical Oil Markets**
Built and audited a registered walk-forward experiment testing market-state and event-label analogy rules using a 313-event catalogue (1973–2026) and 264 scored daily forecasts (2001–2026).

- Constructed a point-in-time research pipeline that seals forecasts before outcome attachment and reproduces its central artifacts byte-for-byte from a committed input bundle.
- In a registered concentration-matched ablation across 264 forecast dates, market-state matching improved mean CRPS from 8.422 to 8.286 versus event-class matching (difference −0.136; 95% bootstrap interval [−0.234, −0.038]; Holm-adjusted *p*=0.013).
- Reported that the registered event-level nonmarket aggregation did not improve on market state (difference +0.051; interval [−0.001, +0.118]; Holm-adjusted *p*=0.114), while explicitly withholding any conclusion about relational geopolitics because multi-actor values were averaged and dyadic coverage was nearly absent.
- Mechanically classified every tracked repository file, audited the components behind the central claims, and rebuilt the main experiment after identifying mismatches among the intended estimand, candidate pool, outcome definition, and recorded data availability.

If space permits only two bullets, use the first two. Keep the limitation in the interview explanation.

## One-line version

Built a registered geopolitical-analogy experiment showing that recent market-state matching outperformed event-class matching at equal forecast concentration across 264 oil-market forecasts (2001–2026).

## Thirty-second interview explanation

“Analysts often choose precedents because the event label looks familiar—closure with closure, sanction with sanction. I built a walk-forward experiment where every method saw the same prior cases and forecast the same abnormal oil return. The first result favored a combined-state rule, but that rule was much less concentrated than the class rule. I registered a follow-up that equalized concentration, and recent market state still beat event class. The audit then showed why I could not make the larger geopolitical claim: almost no dyadic state entered, and multi-actor values were averaged. So the finding is not a magic forecaster or proof of full structural analogy. It is that market context is more informative than headline category, while the relational historical question remains open.”

## Two-minute interview explanation

“The project began with a historical-method question. Commentators often compare a current crisis
with a famous precedent because both are called an embargo, war, sanction, or chokepoint
disruption. But the label does not specify the conditions that generated the earlier outcome. I
wanted to turn that concern into a falsifiable experiment.

I assembled 313 dated geopolitical and oil-policy events and built a walk-forward forecaster. At
each date, every method received exactly the same closed historical cases and predicted a
distribution for Brent's 20-return abnormal move. Forecasts were serialized and SHA-256 sealed
before outcomes were attached. The first combined-state rule beat event-class matching strongly,
but an audit found that the class rule concentrated on far fewer precedents. I registered a second
analysis that matched effective sample size. Market-state matching still performed better than
event class across 264 forecast dates: CRPS 8.286 versus 8.422, a difference of −0.136 with a 95%
interval from −0.234 to −0.038 and a Holm-adjusted p-value of 0.013.

The important qualification is that neither method clearly beat uniform historical pooling. The
state data were also too sparse and badly represented for the larger geopolitical claim: almost no
dyadic data entered, and multi-actor numeric values were averaged into one event value. I therefore
withdrew the claim that full structural analogy had been tested. The defensible result is that
recent market context is a better analogy rule than headline category at equal concentration, while
the project also demonstrates what data and controls a valid test of relational historical analogy
would require.”

The scored record begins in 2001 rather than 1973 and is concentrated in recent years; volunteer
that boundary if someone asks about historical depth. The 313-event catalogue and the 264-date
inferential sample are not interchangeable counts.

## Questions a skeptical interviewer may ask

### “Why does the result matter if the method did not beat uniform pooling?”

Because those are different propositions. The experiment rejects a common way of selecting
precedents—concentrated matching by event label—but does not establish a profitable or generally
skillful forecaster. It shows that a method can beat a familiar heuristic without beating the much
harder benchmark of using all eligible history. Reporting both prevents a comparative win from
being misrepresented as predictive validation.

### “Did you prove that geopolitical context does not matter?”

No. The usable comparison was dominated by four market fields. Leadership appeared in about half
of pairwise comparisons, dyadic state appeared in three, and multi-actor numeric values were
averaged. The study therefore cannot adjudicate the value of role-preserving relational
geopolitical context. That is an explicit untested hypothesis.

### “Why should I trust a result produced with AI assistance?”

AI accelerated implementation, but the scientific decisions were frozen in git registrations and
the claims are checked against committed outputs. I directed the agents, defined acceptance rules,
audited whether code computed the quantities described, retained negative findings, and own the
interpretation. A clean checkout reproduces the frozen artifacts byte-for-byte and runs the full
public test suite.

### “What was the hardest lesson?”

That technically correct code can answer the wrong scientific question. Candidate eligibility,
target construction, forecast concentration, actor aggregation, and availability metadata are not
implementation details; each one defines the estimand. The audit changed the headline because it
showed what the experiment had and had not actually tested.

### “What would you build next?”

I would represent disruptions as evolving episodes with explicit actor roles, anticipation,
physical flow impairment, exposure, spare capacity, inventories, rerouting, and mitigation. I would
construct the corpus under an outcome-blind inclusion rule, then compare trajectory-based analogy
with event labels, text similarity, market state, and pooling on identical support.

## What I personally did

- Designed the research question as an executable comparison rather than a narrative analogy exercise.
- Built the event catalogue, state-data infrastructure, walk-forward evaluation, sealing, scoring, and reproduction workflow with AI coding assistance under a git-based registration discipline.
- Conducted an adversarial claim audit and retained negative and qualified findings instead of optimizing the story for significance.
- Reduced a sprawling research system to one inspectable experiment, one methods paper, and one demonstration.

Be explicit about AI assistance if asked. A defensible formulation is: “I directed multiple coding agents, designed the registrations and acceptance rules, audited their outputs against code and data, and own the final research judgments.” Do not imply that every line was typed manually.

## Second project — physical disruption measurement (v3, branch `research/v3`)

A separate, self-contained piece of work. Every number ties to `data/v3/` and
`docs/audit/V3_LINKAGE_FEASIBILITY.md`.

**Independent Research — Measuring Physical Disruption of Maritime Oil Chokepoints**
Built a preregistered, event-blind detector for tanker-transit impairment at seven maritime
chokepoints from IMF PortWatch daily data (58,779 observations, 2019–2026).

- Preregistered the detection rule — trailing-median baseline, threshold, duration and recovery
  criteria — and committed it before writing the detector; the threshold was derived from the
  input's own noise distribution rather than from any outcome.
- Enforced blinding mechanically: automated tests walk the detector's dependency graph and fail if
  it can reach the event catalogue, any price series, or any known episode date. Blind to all of
  them, it independently recovered the Ever Given grounding, the Red Sea shipping crisis at two
  chokepoints simultaneously, the Panama Canal drought and a Hormuz closure.
- Found that **13 of 39 detected impairment episodes (33%), including a 51-day Panama Canal
  episode, occur on routes for which a 313-event geopolitical catalogue contains no eligible
  event** — a coverage gap that holds under any linkage rule, since linkage requires a shared route.
- Reported the intended event-linkage analysis as **not identifiable** with the current catalogue,
  documenting three specific failure modes rather than reporting an unusable proportion, and
  declining to widen a registered window after observing that it would have captured the largest
  episode.

### One-line version

Built a preregistered, event-blind instrument measuring physical disruption at maritime oil
chokepoints, and showed that a third of the disruption it detects falls outside a curated
geopolitical event catalogue entirely.

### Thirty-second explanation

“Commentary about oil treats geopolitical events as the thing that disrupts supply. I wanted to
measure the disruption directly instead of inferring it from headlines, so I built a detector over
IMF vessel-transit data that finds sustained declines in tanker traffic through chokepoints. I
registered the rule before writing the code and enforced with tests that the detector cannot see
the event list, so when it independently recovered the Ever Given and the Red Sea crisis I knew
that wasn't circular. The result I trust is a coverage one: a third of what it detects, including
a fifty-one-day Panama Canal episode caused by drought, has no corresponding geopolitical event at
all. The linkage analysis I actually set out to run turned out not to be identifiable with the
catalogue I have, and I reported that rather than a number I couldn't defend.”

### What must be said alongside it

- This is a **measurement instrument and a coverage result**, not a forecasting result. No price
  data was analysed.
- Episode **counts** are sensitive to the detector's parameters (16–195 across the nine
  preregistered sensitivity cells). The large episodes are stable across all nine; the count is not.
- The catalogue is **not a census of declarations**. Unmatched episodes are “not matched to this
  catalogue” — never “undeclared”, “silent” or “ignored”.
- The registration discloses that a preliminary below-baseline count had been seen before it was
  written, so the phase is **registered but not blind**.

## Claims not to make

- “The engine predicts oil prices” or “beats simple baselines.”
- “Structural analogy is validated.”
- “The experiment compared the full geopolitical state.”
- “The experiment showed that geopolitical or relational state adds no value.”
- “The method proved historical analogies work.”
- “The 2026 Hormuz demonstration was a live forecast.”
- “All historical state information was unavailable.”
- Any result copied from a superseded document without a fresh claim-level check.

## Numbers to remember

| quantity | value | source |
|---|---:|---|
| catalogue | 313 events | input bundle and summary |
| scored dates | 264 | `summary.json:n_inferential_dates` |
| structural CRPS | 8.341 | `summary.json:mean_loss.structural` |
| surface CRPS | 8.784 | `summary.json:mean_loss.surface` |
| structural − surface | −0.444 | `summary.json:mean_loss_diff_structural_minus_surface` |
| 95% interval | [−0.613, −0.269] | `summary.json:ci95` |
| structure − uniform | −0.049 | `summary.json:diagnostics_non_verdict.abnormal.20.structural_vs_uniform.mean_diff` |
| corresponding interval | [−0.112, +0.012] | same block, `ci95` |
| matched market CRPS | 8.286 | `ablation/summary.json:mean_loss.market_matched` |
| matched class CRPS | 8.422 | `ablation/summary.json:mean_loss.surface_matched` |
| matched market − class | −0.136 | `ablation/summary.json:primary_explanatory.market_minus_surface_matched.mean_diff` |
| corresponding interval | [−0.234, −0.038] | same block, `ci95` |
| Holm-adjusted *p* | 0.013 | same block, `dm_p_holm` |
| combined − market | +0.051 | `ablation/summary.json:primary_explanatory.combined_minus_market_matched.mean_diff` |

CRPS is a proper score for a predictive distribution; lower is better. Explain the comparison and limitation before discussing the *p*-value.
