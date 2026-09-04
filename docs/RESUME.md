# Verified résumé and interview language

This is the only current application document for the project. Every quantitative statement below is tied to `data/structural_surface/summary.json` or `data/structural_surface/ablation/summary.json`. Do not copy claims from `docs/RESUME_AND_APPLICATION.md`, which describes a superseded experiment.

## Recommended résumé entry

**Independent Research — Testing Historical Analogy in Geopolitical Oil Markets**
Built and audited a registered walk-forward experiment testing market-state and event-label analogy rules across 313 geopolitical and oil-policy events (1973–2026).

- Constructed a point-in-time research pipeline that seals forecasts before outcome attachment and reproduces its central artifacts byte-for-byte from a committed input bundle.
- In a registered concentration-matched ablation across 264 forecast dates, market-state matching improved mean CRPS from 8.422 to 8.286 versus event-class matching (difference −0.136; 95% bootstrap interval [−0.234, −0.038]; Holm-adjusted *p*=0.013).
- Found no demonstrated increment from the available leadership/dyadic fields beyond market state (difference +0.051; interval [−0.001, +0.118]; Holm-adjusted *p*=0.114), and reported that the original combined-state arm did not beat uniform pooling.
- Mechanically classified every tracked repository file, audited the components behind the central claims, and rebuilt the main experiment after identifying mismatches among the intended estimand, candidate pool, outcome definition, and recorded data availability.

If space permits only two bullets, use the first two. Keep the limitation in the interview explanation.

## One-line version

Built a registered geopolitical-analogy experiment showing that recent market-state matching outperformed event-class matching at equal forecast concentration across 264 oil-market forecasts.

## Thirty-second interview explanation

“Analysts often choose precedents because the event label looks familiar—closure with closure, sanction with sanction. I built a walk-forward experiment where every method saw the same prior cases and forecast the same abnormal oil return. The first result favored a combined-state rule, but that rule was much less concentrated than the class rule. I registered a follow-up that equalized concentration. Recent market state still beat event class; the sparse leadership and dyadic fields added no demonstrated value. So the finding is not a magic forecaster or proof of full structural analogy. It is that market context is more informative than headline category for choosing how to weight precedent.”

## What I personally did

- Designed the research question as an executable comparison rather than a narrative analogy exercise.
- Built the event catalogue, state-data infrastructure, walk-forward evaluation, sealing, scoring, and reproduction workflow with AI coding assistance under a git-based registration discipline.
- Conducted an adversarial claim audit and retained negative and qualified findings instead of optimizing the story for significance.
- Reduced a sprawling research system to one inspectable experiment, one methods paper, and one demonstration.

Be explicit about AI assistance if asked. A defensible formulation is: “I directed multiple coding agents, designed the registrations and acceptance rules, audited their outputs against code and data, and own the final research judgments.” Do not imply that every line was typed manually.

## Claims not to make

- “The engine predicts oil prices” or “beats simple baselines.”
- “Structural analogy is validated.”
- “The experiment compared the full geopolitical state.”
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
