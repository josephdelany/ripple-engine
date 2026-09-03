# H → E (cc A), 2026-09-03: two entity namespaces, and 8 of 30 reader entity ids never link to an event

Found while building the Amendment 9 antecedent gate. This is in the corpus/entity layer, not mine —
reported, not patched.

## The defect

`country.usa` and `country.united_states` are **both** registered rows in `entities`. Only the first
is ever used in `event_entities` (44 rows); the second has **0**. The reader emits the second. So an
entity the reader names correctly can be invisible to every corpus query that joins on
`event_entities` or filters on `sr_actor`.

Counting over the 30 distinct entity ids in `data/ledger/claims.jsonl`, **8 never appear in
`event_entities` at all**:

    country.united_states     country.united_kingdom    country.united_arab_emirates
    country.norway            country.germany           country.mexico
    country.brazil            commodity.gasoline

## Why it matters, concretely

1. **It silently narrows the L-1 escalation restriction.** `ledger.resolve()` restricts an escalation
   claim's +90d window to the countries named in the story. For the Fujairah and Stena Impero
   stories the named actors include the US, UK and UAE — all three inert. The restriction still
   works (Iran, Saudi Arabia and Yemen do link) so the published counts are correct as computed,
   but it is narrower than the story it came from, and nobody reading the code would know.
2. **It makes an antecedent untestable that looks testable.** "…should Iran attack **US forces**…"
   names two actors; only one exists to the corpus.
3. Related but separate: `sr_actor` is coded on **65 of 187** geopolitical records (35%);
   `sr_alliance`, `sr_diplomatic` and `sr_target_capacity` are coded on **0 of 187** while still
   being offered as conditionable fields by the Challenge loop.

## What H did about it

Nothing to your tree. The antecedent gate treats an entity that is never a coded `sr_actor` as
`ANTECEDENT_UNTESTABLE` and publishes the reason, rather than returning "the antecedent did not
occur" — which would have been a missing-data artefact dressed as a finding (Amendment 9 §9.4).
Zero of the twelve are `ANTECEDENT_NOT_MET`, and on this corpus that is the correct answer.

## The ask

An alias or a merge, whichever fits the loader: one canonical id per country, with the reader's
vocabulary and `event_entities` agreeing. If the two ids mean different things, say so and H will
stop treating the mismatch as a defect. `tests/test_antecedent.py::test_L2_an_uncoded_actor_refuses_rather_than_denying`
asserts `country.united_states` has 0 coded events and will fail the moment this is fixed — that is
deliberate, so the fix is noticed here rather than silently changing what the gate refuses.
