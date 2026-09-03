# F → B, 2026-09-02 — the hostility precondition: the blocking condition, and the numbers
*Supersedes the first version of this file, which covered only two of the four geopolitical
classes and gave numbers three times too small. Both changes are in §3.*

## 1. THE BLOCKING CONDITION — read this before anything else
**Do not implement the precondition for any geopolitical class until all four are coded.**

Implementing it while only some classes carry `hostility` would exclude non-hostile events
from the coded classes and silently keep them in the uncoded ones. That is **worse than
today**, because today's defect is uniform and visible, whereas a half-applied precondition
produces a G target that means different things in different classes and shows nothing in the
output to say so. Registered as `OUTCOME_MAPPING.md` Amendment 3.1 §2.

**Outstanding count: 0 of 4 classes.** All four geopolitical classes are now coded — 187
events, published in `data/spine/CLASS_AUDIT.md` §3:

| class | events | coded | hostile | h-unattributed | ambiguous | non_hostile |
|---|---:|---|---:|---:|---:|---:|
| `infrastructure_attack` | 48 | ✅ | 40 | 3 | 2 | 3 |
| `chokepoint_disruption` | 27 | ✅ | 18 | 0 | 3 | 6 |
| `conflict_escalation` | 55 | ✅ | 44 | 0 | 3 | 8 |
| `sanctions` | 57 | ✅ | 49 | 0 | 5 | 3 |
| **all four** | **187** | **✅** | **151** | **3** | **13** | **20** |

At the previous handoff this table read **112 outstanding** (`conflict_escalation` and
`sanctions` unread); that is what the condition was blocking on, and it is now clear. The
condition itself stays in force for any *new* geopolitical class or any class re-scoped by a
future codebook amendment.

**Nothing is outstanding.** Correcting the previous version of this file, which listed the
13 `ambiguous` events as awaiting Joe:
- **The 13 `ambiguous` events are RULED and closed** (2026-09-02, `OUTCOME_MAPPING.md`
  Amendment 3.3). `ambiguous` is a **terminal value**, not a pending decision: the record does
  not settle them and adjudicating anyway would supply a fact the evidence lacks. They stay
  `ambiguous`, stay out of G-scoring, and **are not a to-do for you or anyone else** — do not
  put them on a checklist, a gate report or a surface as outstanding. Only new evidence in the
  record moves one (a source that settles a cause, or an E patch unbundling a row that holds
  two acts), never a judgement call.
  **What this obliges you to do when you implement:** publish the G level-0 share **with and
  without** the `ambiguous` events, per Amendment 3.3 §2 — in `summary.json` and on any surface
  reporting a G outcome distribution. The registered rule excludes them, so the headline share
  is the one that drops only `non_hostile`; the other bound goes beside it, never instead of it.
- **The other three types** (`opec_decision`, `demand_shock`, `policy_response`) carry no
  `hostility` and never will — they are already outside G-scoring, which is why the field is
  null-and-not-applicable there. That is not an outstanding item either.
- **The eleven misplaced events keep their classes** (ruling 2, same date): eight mining
  strikes stay `conflict_escalation`, three producer export bans stay `sanctions`. Do not
  re-class them, and do not expect a patch that does. The correct placement is a v3 codebook
  item applied prospectively only; `tests/test_hostility.py::
  test_the_eleven_misplaced_events_keep_their_classes` fails if anyone moves one.

## 2. What to implement (v3)
`OUTCOME_MAPPING.md` Amendments 3, 3.1, 3.2 and `EVENTS_CODEBOOK.md` amendment 2026-09-02
(the field, approved by Joe).
- IES-90 gains a `hostility` value per geopolitical event. `non_hostile` and `ambiguous`
  return `no_independent_outcome` **before any source is consulted**; `hostile` and
  `hostile_unattributed` are scored as now, the latter flagged.
- **Do not treat `hostile` as "violent".** Amendment 3.2(b): a sanction lifted, a waiver, a
  deal signed is `hostile` (a dated act inside an identified adversarial dyad) and carries
  **`de_escalatory = 1`**. Nine rows are marked. Excluding them would delete exactly the
  events the DEAL flag measures and bias the corpus toward escalation by construction.
- `no_independent_outcome` already has a path through your code; this widens what feeds it.
  Nothing else changes — no window, no source, no precedence rule, no level mapping.
- `tests/test_hostility.py::test_the_audit_applies_nothing` asserts there is no `hostility`
  field in `event_outcomes` today. It is the tripwire: when you implement, it fails on
  purpose, and the fix is to re-state CLASS_AUDIT §6 against the new run — not to delete it.

## 3. The numbers — REVISED, and materially larger than the first handoff said
Set: the 150 daily-tier scored G reads of the current published run (`burn_in_ok`, engine and
climatology G both scored), matching `summary.json` `/tiers/daily/G/engine_vs/climatology/n`.
You re-ran the walk during this session; the run id changed and none of these figures did.
The audit and its test read the run out of `scores.jsonl` rather than naming it.

| | n | level-0 | share |
|---|---:|---:|---:|
| as published | 150 | 63 | **42.0%** |
| less the 17 `non_hostile` | 133 | 49 | **36.8%** |
| less the 10 `ambiguous` as well | 123 | 40 | **32.5%** |
| less the 2 `hostile_unattributed` as well | 121 | 40 | **33.1%** |

**27 of 150 affected (18.0%)**, by class: `chokepoint_disruption` 6 of 17 (35%),
`conflict_escalation` 10 of 46 (22%), `sanctions` 8 of 49 (16%), `infrastructure_attack`
3 of 38 (8%).

**Correction to the first handoff.** It reported 9 of 150 (6.0%) and 42.0% → 41.0%, from the
two classes then audited, and said the effect on the headline was small. Across all four it is
27 of 150 and 42.0% → 36.8%. The two-class figures were right for two classes; the conclusion
drawn from them was not safe to generalise. Please do not carry the old numbers into a run
note or a figure.

**The part that matters most for your side of the work:** climatology is estimated from this
outcome distribution, so removing the non-hostile reads moves **the baseline the engine is
scored against**, by about five points of level-0 mass — not only the engine's own score. The
skill comparison changes on both sides, and in which direction cannot be known until you
re-run. Nothing in the audit claims a direction, and the paper text handed to Cowork claims
none either.

Three reads carry a non-zero level for an event with no adversary, and they are the
qualitative damage rather than the count: `drc_cobalt_ban_2025` at **level 3, war** (a cobalt
export suspension to defend a collapsed price, off GED deaths in the DRC),
`druzhba_contamination_2019` at level 2, `kurdistan_ceyhan_halt_2023` at level 2.

Six further affected events sit outside the 150 on tier or burn-in (`abqaiq_arabian_1977`,
`iran_oilworkers_strike_1978`, `shah_leaves_iran_1979`, `earnest_will_1987`,
`suez_tropic_brilliance_2004`, `libya_jathran_blockade_2013`) and are still **retrieved as
analogues** — the 1978 oil-workers' strike sits in the precedent set carrying level 3, war.

## 4. What you must NOT do
Amendment 3 §A3.5: **the published run is not re-scored.** `reads.jsonl` is sealed against the
target as it stood; re-scoring under a later definition breaks the seal and lets a definition
be chosen once its effect on the score is known. The run stands as published, with its n and
its scores. Post-amendment runs are reported separately and never pooled with it.

Surface note required by §A3.5 wherever this run's G results appear:
> scored before Amendment 3; includes 17 non-hostile events for which the G target is
> undefined (27 counting ambiguous) — `data/spine/CLASS_AUDIT.md` §6

Every figure above recomputes in `tests/test_hostility.py::
test_section_6_impact_recomputes_from_the_sealed_scores`, which reads your scores file and
never writes to it.

— Session F

---

## 5. One small thing found while checking the audit against the DB
`rule_fired` is not stable across runs when two rules of the **same source** tie. Between two
of your runs today, `bridgeton_mine_strike_1987` moved from
`WAR.intra.location,WAR.inter.single` to `WAR.inter.single,WAR.intra.location` — same level,
same rules, different order. Amendment 2 §A2.3 fixes the tie order *between* sources (MIDI,
war, ICB, MID, GED) but says nothing about the order *within* one, so both strings satisfy
the registration and neither is wrong.

No result depends on it and nothing needs fixing urgently. It is worth a line because
`rule_fired` is a published receipt column: anything that diffs two runs' receipts will show
a spurious change here. Sorting within a source (or a one-line note in A2.3 that the order
within a source is unspecified) would settle it. `tests/test_hostility.py` now compares
`rule_fired` as a set for this reason, so a real change still fails the test and a re-ordering
does not.

— Session F

---

## 6. A red test in your area, found by the full suite (not caused by this session)
`tests/test_walk_read_archive.py::test_the_hashes_the_demo_pages_quote_are_the_ones_tested`
fails, in isolation and in the full run:

```
AssertionError: docs/demos/ no longer quotes {'8b7277ff28fc', '5bc0293dd2d9', 'aed201938e98'}
```

`DEMO_HASHES` (three read hashes the test pins) are no longer among the hashes quoted in
`docs/demos/`. The likely cause is the re-run: new run, new sealed reads, new hashes, and the
demo pages still carry the previous set — the same boundary your own `95451c6` was about.

Session F did not touch it and cannot fix it: `tests/test_walk_read_archive.py`, `src/walk.py`,
`data/walk_forward/**` and `docs/demos/` are yours. Nothing in F's commits can reach a read
hash — they touch `data/spine/CLASS_AUDIT.md`, `tests/test_hostility.py`, this handoff,
`OUTCOME_MAPPING.md`, `EVENTS_CODEBOOK.md` and `SESSION_CHARTER.md` only. Flagging it because
SESSION_CHARTER §2.7 makes a red test a stop, and this one is currently the only one in the
suite (442 passed, 1 failed).

— Session F
