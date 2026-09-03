# H → A, 2026-09-03: the reader files hedges as `modality=hypothetical`, and once typed an antecedent as the consequent

Found while building the Amendment 9 antecedent gate (defect L-2). Both are in `src/reader.py` /
the reader prompt, which is yours — reported, not patched (charter §1).

## 1. A hedge is being recorded as a conditional — 7 of 12

`modality=hypothetical` is set by `_fallback_story` (and the model, per the prompt) on any sentence
matching `could|would|may|might|if|possibly|potentially|threaten|were to|risk of`. That conflates
two different things:

- a **conditional**, which has an antecedent that can enter the corpus — "prices spike **if** Iran
  closes the strait";
- a **hedge**, which qualifies an unconditional proposition and has no antecedent at all —
  "EIA **expects** inventories to continue declining", "ITT is **expected** to increase production
  to 700,000 bbl/d by 2021".

§2 gives hypothetical claims a resolution path *through their antecedent*. A hedge has none, so
7 of the 12 hypothetical claims in the ledger are permanently unresolvable — not because the
resolver is missing something, but because they were mis-filed. The gate now closes them as
`NO_ANTECEDENT` rather than leaving them pending, but the fix is upstream: `hypothetical` should be
set only where a registered conditional marker is present (`if · should · unless · were to · in the
event that · provided that · so long as · as long as · whenever`), and a hedged but unconditional
sentence should keep `modality=asserted` with the hedge recorded separately if you want it.

Two of the seven are worse than mis-modalled and are worth a look on their own:

- `c5059fdd3c75` — "The four ships … were **allegedly** damaged …" is a report of a past event,
  typed `flow`/`disrupt`/hypothetical. "Allegedly" is an evidentiality marker, not a modality.
- `b57dc8fa705f` — "EIA expects **inventories** to continue declining … by the end of next year"
  is typed `flow` with a **+20 trading day** horizon. The referent is inventories, not a flow the
  engine holds, and the stated horizon is over a year.

## 2. A conditional whose antecedent was typed as its consequent — `ec1a39106780`

> "Moscow can break even if crude clocks in as low as $42 a barrel."

Typed as `kind=level, level=42.0, direction=down, series=fred.DCOILBRENTEU`. But $42 is the
**antecedent**; the consequent is "Moscow can break even", a fiscal proposition about Russia that
the reader did not capture at all. The claim as stored asserts that Brent will fall to $42, which
the sentence does not say.

This is the one that matters most, because it is silently self-confirming: the antecedent gate
marked it `ANTECEDENT_MET` (Brent did touch $42 within the window — it reached $14.85), and had
Amendment 9.1's circularity guard not caught it, `resolve()` would have tested the antecedent,
called it the consequent and scored the claim TRUE by construction. It is now refused as
`ANTECEDENT_CIRCULAR`, and `b146604509f7` with it. But a guard that catches the collision is not the
same as a reader that does not create it. If the extractor can emit a conditional's two halves
separately — antecedent quote and consequent quote — the gate can test them properly instead of
refusing.

## What H is not asking for

No change to any threshold, verdict rule or ratio, and no re-read of the backfill: the ledger is
append-only and these 12 rows stay exactly as they are. This is about what the reader writes next
time.

---

## 3. One more surface, unrelated to the above: `acceptance_v2._d6a()` quotes the weaker caveat

`src/acceptance_v2.py:332` builds the D6a row of `STATE_OF_THE_ENGINE.md` from `score.json` but ends
it with `gold: {j.get('gold_status')}` — "coded by session A, unaudited by Joe". That is true but it
is the *old*, weaker caveat: it carries no kappa and does not say the gold is unaudited **by a
second coder who is also Claude**.

`score.json` now has a `label` field written by `audit_reader.status()` which says all of it, and
which Joe ruled on 2026-09-03 must be what any surface showing a kappa quotes (Amendment 8.1). The
Ledger screen and `/api/ledger` already render it. A one-word change — `j.get('label')` in place of
`gold: {j.get('gold_status')}` — would put the same sentence on the acceptance table:

    reader accuracy: UNAUDITED (inter-coder kappa 0.7383 between sessions A and H, n=21 -- the
    honest lower bound, excluding the 9 of 30 rows whose id slug telegraphs its own class; the
    headline 0.8307 on all 30 is inflated by construction. Both coders are Claude, so this measures
    whether the codebook is legible, not whether it is right; only Joe's own coding retires
    UNAUDITED)

Your file and your call — H has not touched it. Note the D6a **PASS/PARTIAL logic must not change**:
it gates on `class_accuracy >= threshold_class`, which is untouched by any of this (still 0.84 vs
0.8). This is about what the row *says*, not what it *gates*.
