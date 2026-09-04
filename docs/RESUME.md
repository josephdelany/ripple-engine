# Verified résumé and interview language

This is the only current application document for the project. Every quantitative statement below is tied to `data/structural_surface/summary.json`. Do not copy claims from `docs/RESUME_AND_APPLICATION.md`, which describes a superseded experiment.

## Recommended résumé entry

**Independent Research — Structural Historical Analogy for Geopolitical Oil Shocks**  
Built and audited a registered walk-forward experiment comparing structural state similarity with event-class matching across 313 geopolitical and oil-policy events (1973–2026).

- Constructed a point-in-time research pipeline that seals forecasts before outcome attachment and reproduces its central artifacts byte-for-byte from a committed input bundle.
- Across 264 forecast dates, structural weighting improved mean CRPS from 8.784 to 8.341 versus surface-class matching (paired difference −0.444; 95% bootstrap interval [−0.613, −0.269]).
- Found that structural weighting did not distinguishably beat uniform historical pooling at the registered 20-day horizon (difference −0.049; 95% interval [−0.112, +0.012]), indicating that event-label filtering—not lack of historical breadth—caused most of the surface method’s deficit.
- Mechanically classified every tracked repository file, audited the components behind the central claims, and rebuilt the main experiment after identifying mismatches among the intended estimand, candidate pool, outcome definition, and recorded data availability.

If space permits only two bullets, use the first and third. The third contains the decision-relevant finding and its limitation.

## One-line version

Built a registered geopolitical-analogy experiment showing that structural comparison outperformed event-label matching across 264 oil-market forecasts, while remaining statistically indistinguishable from uniform historical pooling.

## Thirty-second interview explanation

“Analysts often choose precedents because the event label looks familiar—closure with closure, sanction with sanction. I built a walk-forward experiment where a surface method and a structural-state method saw exactly the same prior cases and forecast the same abnormal oil return. Structure beat the surface labels clearly, but it did not clearly beat simply pooling all eligible history. So the useful finding is not that I built a magic oil forecaster. It is that narrowing precedent by the headline category can throw away useful cases and make judgment worse. The audit was as important as the result: several earlier claims were withdrawn when I found that the code’s quantity did not match the prose.”

## What I personally did

- Designed the research question as an executable comparison rather than a narrative analogy exercise.
- Built the event catalogue, state-data infrastructure, walk-forward evaluation, sealing, scoring, and reproduction workflow with AI coding assistance under a git-based registration discipline.
- Conducted an adversarial claim audit and retained negative and qualified findings instead of optimizing the story for significance.
- Reduced a sprawling research system to one inspectable experiment, one methods paper, and one demonstration.

Be explicit about AI assistance if asked. A defensible formulation is: “I directed multiple coding agents, designed the registrations and acceptance rules, audited their outputs against code and data, and own the final research judgments.” Do not imply that every line was typed manually.

## Claims not to make

- “The engine predicts oil prices” or “beats simple baselines.”
- “Structural analogy is validated.”
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

CRPS is a proper score for a predictive distribution; lower is better. Explain the comparison and limitation before discussing the *p*-value.
