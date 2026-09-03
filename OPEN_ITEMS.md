# Open items — the complete register

*2026-09-03. Everything outstanding, in one place, ranked by whether it changes a published
sentence. Sources: `docs/red_team_2.md`, the session handoffs in `data/handoffs/`,
`data/acceptance_dod.json`, an external review of the paper, and Cowork's own audits.
Anything not listed here is done or explicitly out of scope.*

---

## Tier 1 — changes what a published number means

**1.1 The escalation target is substantially a persistence variable.** *(red team 2
finding 3, verified 2026-09-03.)* Of 54 level-3 "war" labels, **34 (63%) already had ≥250
GED battle deaths in the 90 days before the event** — Iraq–Kuwait 1990 (905), Iraq 2003
(6,584), Ukraine 2022 (20,473), Israel–Hamas 2023 (3,835). All 54 come from COW War or
UCDP GED, the two sources Amendment 1.1's "ongoing → no level" rule was never extended to.
`deaths_ged_pre90` is stored for 168 events and used once in `ies90.py`. **Consequence:**
"did escalation follow?" is largely "was a war already running?", so the
persistence-beats-engine headline is partly mechanical. Owner **A** (register + implement),
**B** (re-run), **Cowork** (paper). *Highest priority in the project.*

**1.2 The Big Moves clustering constants are unregistered.** *(finding 2.)*
`BIG_MOVES_REGISTRATION.md` registers clustering within 60 **trading** days and no merge
step; `src/big_moves.py` clusters at 90 **calendar** days and merges same-sign clusters
within 60. No amendment covers either, and both constants landed in the same commit as the
registration, so git cannot show registered-before-computed. Owner **Joe** (ruling: amend
with the honest history, or re-run under the registered rule), then **B**.

**1.3 The placebo condition is unresolved.** *(finding 1.)* The size-matched reference the
placebo passes under exists only in an unratified amendment; against climatology it fails.
Recorded as UNRESOLVED in README and paper §9. Owner **Joe** — ratify prospectively for v3,
or withdraw. Not resolvable retroactively either way.

**1.4 The escalation result is confounded three ways by era.** Skill by era: 1987–99
+0.009 (n=2, median pool 8), 2000–09 +0.068 (n=10, pool 10), 2010–19 −0.103 (n=51, pool
18), 2020–26 −0.117 (n=87, pool 36). Pool size, base rate (0.751 → 0.659) and label basis
(100% dyadic in 1946–73 → 7% by 2015–26) all move together, and the recent era dominates
the sample. Owner **B** — stratified diagnostic, registered first, gating nothing.

## Tier 2 — the target and the corpus

**2.1 The event taxonomy conflates acts with incidents.** 33 of 187 geopolitical-class
events are not G-scorable (20 non-hostile, 13 ambiguous). A `hostility` field now records
this; the correct four-way taxonomy (interstate military / interstate coercion /
energy-geopolitical / non-state-domestic) is registered **prospectively only**. Owner
**Joe** (whether v3 re-codes), **F** (already registered).

**2.2 The historical corpus is thin.** 8 events in the 1970s, 11 in the 1980s, 16 in the
1990s, against 150 after 2010. The monthly tier needs 33 events minimum, 43 to be readable;
it has 14, 0 scored. 624 pre-1987 candidates screened. Owner **G** (dossiers), **Joe**
(admission).

**2.3 The state vector is empty once vintage binds.** 726 of 786 situation values dropped
as not-knowable; 60 kept across 313 events. Owner **G** (`situation_vintage.py`, deriving
`knowable_at` from dossier source dates).

**2.4 Post-2000 sourcing cannot be repaired by any reachable route.** 28 records have no
citable domain; 0 of 27 post-2000 encyclopaedia-only records could be replaced through
eight probed routes, because between 2000 and 2016 no free archive reaches. Documented,
not fixable. Owner — none; it is a finding.

## Tier 3 — loops that have never completed

**3.1 The claim ledger has never resolved a claim end to end.** Owner **H** (in flight).

**3.2 The reader's gold set is machine-graded.** 100 headlines coded by session A, reader
scores 84% against them, labelled unaudited and gated by nothing. Owner **H** (inter-coder
κ + `audit_reader.py`), then **Joe**.

**3.3 The challenge loop has 2 entries.** Owner **H**.

## Tier 4 — Joe's gates, which no session can close

**4.1 The IES-90 label audit.** 1 of 30 rows. D3a stays FAIL until 30 are graded and κ is
computed. Note item 1.1 may change what some rows should say — worth waiting for A's
amendment before grading the rest.

**4.2 The 13 ambiguous class rows.** Ruled terminal; no action, recorded.

**4.3 Rulings outstanding:** the Big Moves constants (1.2), the placebo reference (1.3),
whether v3 re-codes the taxonomy (2.1), pre-1987 admissions (2.2).

**4.4 `launchd` access** so the daily loop runs unattended — needed for D7's ledger days.

## Tier 5 — packaging

| deliverable | status |
|---|---|
| One-page brief | done — `docs/BRIEF.md` |
| README for a ten-second reader | done |
| Spoken versions and term glosses | done — `docs/EXPLAIN.md` |
| Resume bullets | done, corrected to 27 datasets |
| Three flagship charts | in flight — session I |
| Paper restructured to lead with the three findings | **not started** — Cowork |
| Technical appendix | partial — Appendix A plus the registrations |
| Propagation as a companion piece | partial — standalone at `docs/RIPPLE_FINDINGS.md`, still summarised in paper §11 |

## Tier 6 — housekeeping

**6.1 `acceptance_v2 --dod` reports D1 FAIL on a green suite** — substring bug, tests
`"failed" not in summary` and the line reads "1 xfailed". Owner **A**, one line.

**6.2 Eleven `TASK_BRIEF_*.md` and other scaffolding are tracked** at the repo root.
Bannered where they carry claims; not yet moved. Owner **Cowork**, low priority.

**6.3 D7:** tag `v3.0`, and either seven distinct Ledger days or a dated PATH amendment
re-scoping that plan line. Owner **Joe**.

---

## What is *not* an open item

The null itself. Three registered claims have been falsified and published — H1's
stress amplification, the calibration hypothesis, and the permutation-structure claim — and
five of six propagation edges retracted. Those are the record working, not defects in it.
