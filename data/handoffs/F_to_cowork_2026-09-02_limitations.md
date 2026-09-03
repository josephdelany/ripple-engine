# F → Cowork, 2026-09-02 — for the paper's limitations section
*Supersedes the first version, which covered two of the four geopolitical classes and gave an
affected fraction three times too small. **Do not use the earlier numbers.** Every figure
below recomputes from `data/walk_forward/scores.jsonl` under `tests/test_hostility.py`; the
full audit is `data/spine/CLASS_AUDIT.md`, the rules are `OUTCOME_MAPPING.md` Amendments 3,
3.1 and 3.2, and the field is `EVENTS_CODEBOOK.md` amendment 2026-09-02.*

## The limitation, stated
The geopolitical outcome (IES-90) asks what escalation an independent source recorded in the
90 days after an event. It never asks whether the event was an adversarial act. The event
classes are coded by **what was disrupted**, not by **who did it**, so the four classes
treated as geopolitical contain accidents, natural hazards, industrial failures, labour
strikes, community blockades, a criminal contamination, an arbitration award and producer
price-management export bans, alongside attacks, invasions and sanctions. For those events
the outcome is not noisy but **undefined**: with no adversary there is no dyad, and the
measure falls back to whatever violence the covering sources recorded in the country during
the window.

An audit of all **187 events in the four geopolitical classes** — every record read against
its own evidence, published event by event — found **20 non-hostile events and 13 whose
character the record does not settle: 33 of 187 (18%) for which the target is undefined.**
The clearest cases: a 1978 oil-workers' strike scored **level 3, war**, from the Iranian
Revolution's war spell overlapping the window; the 2019 Druzhba pipeline contamination,
injected to cover an oil theft, scored **level 2, use of force**; and a 2025 suspension of
Congolese cobalt exports taken to defend a nine-year-low price, scored **level 3, war**, from
unrelated deaths in the DRC.

**Of the 150 scored geopolitical reads in the walk, 27 (18.0%) are affected** — 17 non-hostile,
10 contested. Excluding the 17 moves the level-0 share of outcomes from **42.0% (63/150) to
36.8% (49/133)**; excluding the contested ten as well gives **32.5% (40/123)**.

The defect was found after the walk was run and sealed. It is **not corrected in the results
reported here**: re-scoring a sealed run under a target definition written later would allow
the definition to be chosen once its effect on the score is known. The precondition — an event
is scorable on the geopolitical target only where the record shows an adversarial act by an
identified party — is registered as a dated amendment and takes effect in the next run, which
will be reported separately and not pooled with this one.

## Four points to keep, if the section is cut for length
1. **Direction and size.** The correction removes reads, never adds them: n falls from 150 to
   133 (11%) and the level-0 share by five points. It is a substantial specification error,
   not a marginal one.
2. **It moves the baseline, not only the score.** Climatology is estimated from this outcome
   distribution, so removing the undefined reads changes what the engine is compared against
   as well as what it is scored on. The limitation applies to both sides of the skill
   comparison, and **the paper should claim no direction** — which way it runs is not known
   until the corrected run exists.
3. **A keyword scan understates it by two thirds.** The defect was first measured by scanning
   for hazard words in two classes and found 4 clear cases; reading all 187 records found 20.
   The worst cases — a strike, a criminal contamination, a price-support export ban — contain
   no hazard word. Any audit of this kind should state whether it read the records or scanned
   them.
4. **The problem is not where the class names suggest.** `infrastructure_attack`, the class
   named for attacks, is the cleanest at 8% of its scored reads affected. The worst is
   `chokepoint_disruption` at 35% — a class defined by a *place*, so anything that stops
   traffic through it qualifies — then `conflict_escalation` at 22%, high because eight
   Chilean and Peruvian mining strikes are filed in it.

## One sentence, if that is all there is room for
> Of the 150 scored geopolitical reads, 27 (18.0%) concern events — storms, groundings, a
> blackout, mining strikes, a mine collapse, a criminal pipeline contamination, an arbitration
> award, producer export bans — for which the escalation target is undefined; the defect is
> documented and corrected forward rather than retroactively, and excluding the 17 clearest
> moves the level-0 outcome share from 42.0% to 36.8%, which shifts the climatological
> baseline as well as the engine's score.

## How to describe the thirteen contested events
Not as "unresolved", "pending review" or "awaiting adjudication" — they are none of those.
`ambiguous` is a **terminal coding** under the project's sourced-or-unknown rule (ruled
2026-09-02, `OUTCOME_MAPPING.md` Amendment 3.3): the record does not settle whether the event
was an adversarial act, and deciding anyway would supply a fact the evidence lacks. The
correct phrasing is that the audit **reports** thirteen events whose character the record does
not determine, and **publishes the outcome share both with and without them** — 36.8% under
the registered rule, 32.5% with the thirteen also out of the denominator — rather than
choosing between the two. If the section has room for only one number it is **36.8%**, and it
must be labelled as excluding the non-hostile events only.

## A note on how to cite this
The audit is a **hand coding** — a reading of each record, like the codebook's severity and
surprise scales — not an automated classification, and the paper should say so. It is
published in full, one row per event with its evidence, so a reader can dispute any row; the
13 contested events are named as contested rather than assigned; and eight codings that turn
on facts outside the corpus carry their external sources. What is machine-checked is that the
coding is complete, that it matches the database, that its totals are its own rows added up,
and that the impact figures recompute from the sealed scores file.

— Session F
