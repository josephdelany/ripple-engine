# K → F, 2026-09-03 — the Amendment 4 rebuild has landed and `CLASS_AUDIT.md`'s copied columns are stale

`event_outcomes` (source `ies90`) was rebuilt to OUTCOME_MAPPING **Amendment 4** on Joe's
ruling of 2026-09-03. The pre-rebuild record is tagged **`record-pre-amendment-4`**
(annotated tag `5a2c58f` → `18561e2`), so nothing is lost.

**`tests/test_hostility.py::test_rows_match_the_database` is RED and it is yours.** Session K
did not touch it, `data/spine/CLASS_AUDIT.md`, or anything else of F's. This note is the
handoff §1 of the charter asks for.

## 1. What is stale, exactly

Your hostility coding — the hand reading, the thing the audit exists for — is **not**
affected. What is stale is the three columns the audit *copies* from `event_outcomes`:

| column | rows disagreeing with the rebuilt DB | of |
|---|---:|---:|
| `level` | **59** | 187 |
| `basis` | **52** | 187 |
| `rule_fired` | **62** | 187 |

The 59 are exactly the 59 label changes Amendment 4 makes. First failure the test hits:
`kharg_strikes_1985`, audit says level 3, DB now says `no_independent_outcome`. Others:
`iraq_kharg_1986` 3 → none, `kuwait_oil_fires_1991` 3 → none, `iraq_pipeline_north_2004`
3 → 1, `nigeria_nda_*_2016` 3 → none, `ukr_odesa_strike_2023` 3 → none.

The full before/after per event, with the rule that fired, is in
`data/state/ies90_amendment4_counts.json` → `rows_changed.rows`.

## 2. What this does to Amendment 3's own impact figures (§5, §6)

CLASS_AUDIT §5–§6 report the precondition's impact against **the 150 daily-tier scored G
reads** of the pre-amendment run — "27 of 150 (18.0%)", level-0 share "42.0% → 36.8%". That
denominator no longer exists. Measured against the rebuilt target, over the 172 scored daily
G reads in the sealed run:

- **49 of 172 (28%)** now leave the G target under Amendment 4 alone.
- **53 of 172** now have no knowable L⁻, so B.3 sends them to climatology.

Do **not** recompute §5–§6 against a new run until B has made one; those sections are about a
run that stands as published (A3.5 and A4.7 both).

## 3. The number that matters for the paper: the two rules barely overlap

Computed today against the rebuilt table and your `CLASS_AUDIT.md` coding:

| | events |
|---|---:|
| Amendment 3 would exclude (`non_hostile` + `ambiguous`) | 33 |
| Amendment 4 excludes (`undated` 52 + `uncovered` 3) | 55 |
| **excluded by BOTH** | **3** |
| union — no G target under either rule | **85** |
| **G-scorable under both** | **102 of 187** |

The three in the intersection are `drc_cobalt_ban_2025`, `druzhba_contamination_2019`,
`iraq_nasiriya_2019`. **A naive sum (33 + 55 = 88) overstates the exclusion by 3.** The two
rules are near-disjoint, which is the evidence for A4.9's claim that they are orthogonal:
Amendment 3 removes events with no adversary, Amendment 4 removes events whose sources
cannot date an escalation. Of the 102 survivors, 101 are `hostile` and 1 is
`hostile_unattributed`.

Worth noting for §A3.1's two worked examples: `druzhba_contamination_2019` is now removed by
Amendment 4 as well, but **`iran_oilworkers_strike_1978` is not** — it keeps level 3, because
the Iranian Revolution's intra-state spell began 58 days before the event and so does not
cover the whole of B. Your precondition is the only rule that catches it. That is the
cleanest published case for why both rules are needed.

## 4. What K suggests (not does)

The `level` / `basis` / `rule_fired` columns are a *copy* of a computed table, so refreshing
them is mechanical and is not a re-coding of anything you read by hand. K has not done it:
`data/spine/CLASS_AUDIT.md` and `tests/test_hostility.py` are yours under SESSION_CHARTER §1,
and a copied column is still your file. The test failing is the correct behaviour — it is a
staleness detector and it detected staleness.

If it helps: the rebuilt values for all 187 events are one query —
`SELECT event_id, field, value, value_text FROM event_outcomes WHERE source='ies90' AND
field IN ('level','basis','rule_fired')`.
