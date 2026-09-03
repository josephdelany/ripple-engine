# F → Cowork, 2026-09-02 — for the paper's limitations section

Copy-ready. Every number below recomputes from `data/walk_forward/scores.jsonl` under
`tests/test_hostility.py`; the full audit is `data/spine/CLASS_AUDIT.md`, the rule is
`OUTCOME_MAPPING.md` Amendment 3.

## The limitation, stated
The geopolitical outcome (IES-90) asks what escalation an independent source recorded in the
90 days after an event. It never asks whether the event was a hostile act. Two of the four
geopolitical classes — `infrastructure_attack` and `chokepoint_disruption` — are coded by
*what was disrupted*, not by *who did it*, so they contain accidents, natural hazards,
industrial failures, a labour strike and a criminal contamination alongside attacks. For
those events the outcome is not noisy but **undefined**: with no adversary there is no dyad,
and the measure falls back to whatever violence the covering sources recorded in the country
during the window.

An audit of all 75 events in the two classes (published in full, event by event, with
evidence) found **9 non-hostile events and 5 whose character is genuinely contested.** All 9
non-hostile events carry an escalation level today. The two most damaging cases are a 1978
oil-workers' strike scored **level 3, war** — from the Iranian Revolution's war spell
overlapping the window — and the 2019 Druzhba pipeline contamination, injected to cover an
oil theft, scored **level 2, use of force**, from unrelated deaths in Russia.

**Of the 150 scored geopolitical reads in the walk, 9 (6.0%) are affected** — 6 non-hostile,
3 contested. Excluding the 6 moves the level-0 share of outcomes from **42.0% (63/150) to
41.0% (59/144)**; excluding the contested three as well gives **39.7% (56/141)**.

The defect was found after the walk was run and sealed. It is **not corrected in the results
reported here**: re-scoring a sealed run under a target definition written later would allow
the definition to be chosen once its effect on the score is known. The precondition — an
event is scorable on the geopolitical target only where the record shows a hostile act by an
identified party — is registered as a dated amendment and takes effect in the next run,
which will be reported separately and not pooled with this one.

## Three points to keep, if the section is cut for length
1. **Direction and size.** The correction removes reads, never adds them; n falls by 6 (4%)
   and the level-0 share by about one point. It is a specification error of moderate size,
   not a result-reversing one.
2. **It is not a level-0 story.** Four of the six removed reads are level 0, but so is 42% of
   the whole set. The damage is the two that are *not* zero, where a location fallback
   manufactured escalation out of events that had no adversary at all.
3. **A keyword scan understates it by half.** The defect was first measured by scanning for
   hazard words and found 4 clear cases; reading all 75 records found 9. The two worst cases
   (the strike, the contamination) contain no hazard word. Any similar audit in this paper or
   another should say whether it read the records or scanned them.

## One sentence, if that is all there is room for
> Of the 150 scored geopolitical reads, 9 (6.0%) concern events — storms, groundings, a
> blackout, a strike, a mine collapse, a criminal pipeline contamination, an arbitration
> award — for which the escalation target is undefined; the defect is documented and
> corrected forward rather than retroactively, and excluding those reads moves the level-0
> outcome share from 42.0% to 41.0%.

— Session F
