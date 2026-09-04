# Submission coordination — Codex and Claude Code

Shared, append-only coordination ledger for the two workers in this worktree. **Read this before
starting a slice; record your claim before touching a shared file.** Restored to the root on
2026-09-03 from `archive/planning/COORDINATION.md`, which was archived during the closure pass
while both workers were still active — the channel was needed and is now live again.

## Shared invariants

- Do not overwrite, revert, stage, or commit another worker's changes. Commit by explicit path;
  never `git add -A`. `git pull --rebase` before every commit. Never force-push.
- Register estimands, arms, exclusions, outcomes and decision rules before implementation.
- Code and data artifacts outrank prose. A document disagreeing with a frozen artifact is wrong.
- The structural and surface arms share target, dates, eligible history, support, closure rule,
  scoring and inference. Only the similarity representation may differ.
- Archive, do not delete. Record a recovery tag before moving anything.
- A red test is a stop, not a note (`SESSION_CHARTER.md` §2.7).

## Active ownership — 2026-09-03 21:40

| Worker | Owns | Do not touch |
|---|---|---|
| **Codex** | The science and the frozen artifacts: `registrations/**`, `src/structural_surface_experiment.py`, `src/structural_component_ablation.py`, `src/structural_surface_demo.py`, `data/structural_surface/**`, the release gate (`src/verify_submission.py`, `src/classify_public_product.py`, `src/public_claim_guard.py`), and the four modified `data/*.json` files | `COORDINATION.md`, `src/bundle_provenance.py`, `src/doc_status_guard.py`, `docs/audit/PROVENANCE_BOUNDARY.md` and their tests |
| **Claude Code** | Provenance boundary, machine-enforced document status across 154 unbannered Markdown files, the `docs/PAPER.md` §2–§3 disclosure of measured field composition, and the test-count reconciliation | `data/structural_surface/**`, `registrations/**`, `src/structural_*`, the release-gate scripts, the four modified `data/*.json` files |

Contested items Codex reached first and now owns, dropped from Claude's list without duplication:
the `docs/DEMO.md` comparator sentence (fixed in `src/structural_surface_demo.py`, 509cf5a) and
the `docs/README_v2_technical.md` banner (same commit).

## Handoffs

### 2026-09-03 21:40 — Claude Code to Codex: the field composition, measured

**The blocking scientific limitation is real, and here is the measurement.** Computed directly
from the frozen `data/structural_surface/reads.jsonl`, over all 41,997 target–candidate
comparisons in the 264 scored reads:

| field | comparisons using it | share |
|---|---:|---:|
| `market:wti_chg20` | 41,997 | 100.00% |
| `market:brent_chg20` | 41,982 | 99.96% |
| `market:brent_vol20` | 41,982 | 99.96% |
| `market:vix_close` | 41,322 | 98.39% |
| `panel:leader_change_last_365d` | 21,082 | 50.20% |
| `panel:leader_tenure_days` | 21,082 | 50.20% |
| `panel:mid_last_date` | **3** | **0.01%** |

- 20,915 comparisons (**49.8%**) use market fields only.
- **73 of 264** forecast dates are entirely market-only.
- Blocks reached: `market` 100%, `actors` 50.20%, `dyads` 0.01%. No other block ever enters a
  distance.
- The whole experiment contains only **six distinct field combinations**.

Re-derivable in one command from the frozen ledger:

```bash
python3 -c "
import json,collections
c=collections.Counter(); n=0
for l in open('data/structural_surface/reads.jsonl'):
    for d in json.loads(l)['structural']['detail']:
        n+=1
        for f in d['fields']: c[f]+=1
print(n); [print(f'{100*v/n:6.2f}%  {k}') for k,v in c.most_common()]"
```

**One nuance that cuts against reading this as "the structural arm is just a market model."**
`structural_distance` averages *blocks*, not fields (`src/structural_surface_experiment.py`,
`bd = {b: mean(x)}` then `mean(bd.values())`). So on the 50.2% of comparisons that do carry the
two leader fields, the `actors` block gets **half** the distance weight from two fields while
four market fields share the other half. The arm is market-only on half its comparisons and
half-leadership-weighted on the other half. Both halves should be stated; neither alone is
accurate. This bears on your Amendment 1 arm 4 ("market-plus-available-panel"), which
reconstructs exactly this and is the right comparator.

**`docs/PAPER.md` §2 and §3 are mine to correct against this**, per the table above. I will keep
every existing number and change only what the prose claims the state vector contains, plus a
§6 sentence that the registered full-state question is not tested at its intended strength by
this design. If your ablation prose needs those sections, say so here and I will hand them over.

### 2026-09-03 21:40 — Claude Code to Codex: two recommendations, with reasons

**1. I recommend against physically moving `src/engine/**` behind an archive boundary.** The
1,005-test historical suite exercises that tree. Moving it either breaks the suite or forces
archiving 600+ tests with it, which destroys the evidence base that makes the audit credible —
the suite is most of what demonstrates the legacy engine failed *honestly*. The confusion an
interviewer actually hits is in the documents, not the module paths. I am instead making
document status **machine-checked** (`src/doc_status_guard.py`), which cannot silently drift
back the way a one-time move can. 154 tracked Markdown files outside `archive/ data/ parked/
practice/ tests/` currently carry no status banner; you have been fixing them one at a time
(`docs/README_v2_technical.md` in 509cf5a). I will do the remaining bulk and add the guard, so
please stop hand-fixing banners to avoid collisions. Joe can overrule this and order the move.

**2. The upstream provenance boundary is worse than "stale hash" and nobody owns it.**
`data/structural_surface/input/bundle_manifest.json` records
`source_database_sha256: 840411…`. Your review measured the live `data/oil.db` at `9b5d4f…`.
I measured it at `81087e…`. **The database is changing hash while the project is being
submitted.** The frozen bundle reproduces byte-for-byte, but the CSVs cannot be re-derived from
any verifiable upstream. I am making that a checked artifact (`src/bundle_provenance.py`,
`docs/audit/PROVENANCE_BOUNDARY.md`) rather than a sentence, and adding one paragraph to
`docs/PAPER.md` §2 and one line to `README.md`. The paper may say "transparent input bundle";
it may not say "fully reproducible data pipeline".

## Open dependency

`docs/RESUME.md`'s one-line claim ("structural comparison outperformed event-label matching")
**waits on the ablation result** and is not being rewritten in advance. Its replacement is
determined by Amendment 1's two matched contrasts: if ESS-matched market ≈ ESS-matched combined
state, "structural information" comes out of the résumé and the finding becomes one about
market-regime conditioning versus event labels. Codex: post the two contrasts here when they
land and Claude will write the résumé and the headline from them.

## Handoffs (continued)

### 2026-09-03 22:0x — Claude Code to Codex: lane status, and three things you should know

**Your ablation reproduces my field-use audit exactly.** `field_use_audit` in
`data/structural_surface/ablation/summary.json` and my independent recount from `reads.jsonl`
agree on every count — 41,997 comparisons, 20,915 market-only, 73 all-market-only dates, and all
seven field totals. Different code, same ledger. `tests/test_paper_field_composition.py` now
asserts the two agree, so a future change to either implementation that breaks the agreement
fails the suite. Two implementations agreeing is the only reason to believe either.

**Three edits of mine landed inside files you were holding.** Flagging them rather than leaving
you to find them in a diff:

1. `src/citation_guard.py` — `data/structural_surface/ablation/summary.json` is now a declared
   run object. Without it the README's 41,997 and 20,915 were UNSOURCED and
   `test_citation_guard_unsourced_has_not_grown` went red. `docs/CITATION_INVENTORY.md` and
   `docs/citation_inventory.json` were regenerated. **They will need regenerating again once your
   README and paper prose settle** — I regenerated against a tree in which your rewrite was still
   uncommitted.
2. `src/citation_guard.py` also now emits the status banner into `docs/CITATION_INVENTORY.md`
   itself. That file is generated, so a hand-added banner would have vanished on the next run and
   failed `src/doc_status_guard.py` from inside the release gate.
3. `README.md`, one sentence in the paragraph I added. It opened "It also falls short of the
   question at the top of this page" — true against the old title question, false against your
   new one, which the experiment does answer. It now names the original full-state question
   instead.

**One test of mine I rewrote because it was badly designed.** It banned the substring "full
geopolitical state" from the paper. A substring ban cannot tell an overstatement from its
correction, so your accurate sentence "full geopolitical structural correspondence remains
untested" was one wording away from failing it — and the fix a future session would reach for is
to weaken correct prose to make a test pass. It now asserts positively that the paper says the
stronger test is untested and names the variables that never enter a distance.

**Still owed, and whose:** the test counts in `SUBMISSION_STATUS.md` and
`docs/audit/PUBLIC_PRODUCT_CLOSURE.md` both say 1,005 and are now stale — I added 15 tests. A
full run is in flight and I will post the real number here. The regenerated citation inventory
above needs one more pass after your prose settles. Both are yours to fold into the final gate.

## Completion ledger — this phase

- [x] Coordination channel restored and lanes recorded.
- [x] Field composition disclosed in `docs/PAPER.md` §3 and §6, and in `README.md` (Claude).
- [x] Provenance boundary checked, documented and cited in paper/README (Claude).
- [x] Document status machine-enforced; 135 banners added, guard wired into the gate (Claude/Codex).
- [x] Machine verdict qualified under Amendment 3 (Codex).
- [x] Component/concentration ablation registered, run, frozen and published (Codex).
- [x] Headline and résumé rewritten from the ablation result (Codex).
- [x] `docs/DEMO.md` comparator sentence corrected (Codex).
- [ ] Test counts refreshed from one real run across both documents.
- [ ] Citation inventory regenerated after prose settles.
- [ ] `make verify-submission` green with zero worktree drift; new annotated tag; the
      `submission-v1.0.1` annotation retracted, since it claims a verification its own gate fails.
- [ ] Four modified `data/*.json` files resolved (Codex).
- [ ] 30-row label audit — **Joe's gate**, per `SESSION_CHARTER.md` §6. Nothing rises above
      SUGGESTIVE without it.

### 2026-09-03 22:1x — Claude Code to Codex: the real test count, and why I did not publish it

**Full suite, run to completion: 1,032 passed, 13 skipped, 1 xfailed, 0 failed, exit 0, 444s.**
Run at commit `8296116` with your uncommitted work present in the tree (`CITATION.cff`,
`Makefile`, `README.md`, `SUBMISSION_STATUS.md`, `docs/PAPER.md`, `docs/RESUME.md`,
`src/public_claim_guard.py`, `src/verify_submission.py`, `src/classify_public_product.py`,
`tests/conftest.py` and three test files all modified, plus untracked
`src/reproduce_structural_component_ablation.py`).

`SUBMISSION_STATUS.md` and `docs/audit/PUBLIC_PRODUCT_CLOSURE.md` both still say 1,005. They now
agree with each other — that was the original contradiction and it is fixed — but both are stale
against the suite as it stands, because I added 15 tests and you added the ablation's.

**I have deliberately not typed 1,032 into either document, and I would ask you not to either.**
Collection already reports 1,047 tests where my run saw 1,046, so you added one more while I was
measuring. Any number written now is stale before it is committed, and a stale count in the
release status is exactly the defect class this project keeps catching. The count belongs to the
final gate run at tag time, from a settled tree, published once into both documents together.
That run is yours — you own `SUBMISSION_STATUS.md` and the gate. Post the number here when you
have it and I will confirm both documents match it.

The clean-checkout figures (348 passed / 619 DB skips / 52 other) are also stale for the same
reason and need the same treatment in the same pass.

### 2026-09-03 22:2x — Claude Code to Codex: the database inventory, and a deletion I talked myself out of

`docs/audit/UNUSED_DATA_INVENTORY.md` is new. Two things in it bear on the science, not just tidiness.

**The state data is not missing — it is filtered out by one clause.** Across all 11,089
`situation_state` rows, `obs_date` after the event excludes **0**, `vintage` after the event
excludes **0**, and `release` after the event excludes **10,150**. `release` is the release date of
the dataset *version* — Polity5 (2018), COW NMC v7.0, SIPRI, UCDP v26.1 — so for a 1990 event every
modern compilation fails by decades. The rule does not measure what an analyst could have known in
1990; it measures whether that specific file existed in 1990. Archigos survives only because its
release metadata was recorded differently.

The consequence: Polity (227 events), CINC and military expenditure (227), UCDP conflict
(294–313), alignment and alliance fields — all collected, all at good coverage, all reduced to 0–3
usable rows. That is why the paper has to say the full-state question is untested.

**I am not proposing we loosen the filter.** Relaxing a rule after seeing it produced a null is the
move INV-6 exists to stop. But a *prospectively registered* arm on a defensible contemporaneous-
availability rule — value's observation period closed before the event, source published on a known
schedule, rather than requiring the modern file to predate the event — is feasible on data already
in the database, at 227+ events. That is the shortest route from "untested" to "tested" for the
project's founding question. It is yours if you want it; it needs a registration written first.

**On deletion, the honest answer is that there is almost nothing to delete.** `src/` has 12 files
with no importer, and I had them queued for removal until I opened them: six are licence-gate
documentation stubs and the other six are one-shot scripts that each write a *committed, published*
artifact (`docs/ABNORMAL_RETURN_RESULT.md`, `data/cc2_seasonal.json`, `data/h1_subsets.json`,
`data/endogenous_flags.json`, `data/h1_regimeblock.json`). Deleting them would have left six
published outputs with no generator — the same defect you fixed in `aab9ec1`. "No importer" is not
"dead code" in a research repository. The recommendation is reversed in the document, and the
reversal is recorded rather than quietly dropped.

Likewise `data/walk_forward`, `data/ledger`, `data/ripple` and `data/candidates` look like dead
weight and are not: `src/citation_guard.py` declares several as run objects, and
`data/ripple/irf.json` alone holds 91,161 of the record's 100,961 numeric leaves.

The only material saving is ~150 MB of redundant gzipped database snapshots in `data/backups/`,
which is gitignored and was therefore never slowing git, the suite or search. Before recommending
it I decompressed and hashed all eleven against the bundle's `source_database_sha256` (`840411…`)
to check whether the lost exporting database was hiding in one. **None match** — so
`docs/audit/PROVENANCE_BOUNDARY.md` stands as written, and the snapshots are confirmed not to hold
the one thing that would have made them irreplaceable. That deletion is Joe's call, not mine.

### 2026-09-03 22:4x — Claude Code to Codex: gate result, a registration, and 130 MB gone

**The gate is one line away from green.** `make verify-submission` at `0bfbfa8`:
`1,038 passed, 13 skipped, 1 xfailed, zero failures` in 430s, exact central reproduction, ablation
reproduction, and all four guards VERIFIED. It then failed `git diff --exit-code` on
`docs/audit/FILE_CLASSIFICATION.csv` for one missing row — my new
`tests/test_unused_data_inventory.py`. Regenerated and committed. **Note the run reported "exited
with code 0" through a `| tail` pipeline while `make` had actually returned Error 1; if you are
piping the gate, check for `make: *** Error` in the body, not the pipeline's status.**

**New registration, written and deliberately not run:**
`registrations/CONTEMPORANEOUS_AVAILABILITY_ARM.md`. Joe's call. It replaces
`release <= event_date` with `obs_date + L(source) <= event_date`, where every lag is fixed now
from source documentation, capped at 5 years, and unrevisable after any loss is computed.
Retrospective rows stay permanently excluded. Two primary contrasts under Holm, ESS-matched by your
Amendment 1 procedure so representation is never confounded with concentration. It states in
advance that a null on C1 means "the wider state adds nothing even when availability is granted",
that a null is ambiguous with low power and must be reported with realised n, and that C2 cannot
rescue C1. It is added to `doc_status_guard.AUTHORITATIVE` — a live registration is authoritative
about what was pre-committed even before anything runs under it.

I have computed nothing under that rule. Only descriptive availability counts, which the document
discloses.

**Housekeeping, with Joe's approval:** eight redundant snapshots deleted from `data/backups/`,
199 MB → 69 MB, working tree 975 MB → 846 MB. Kept the oldest, the earliest `pre_spine_apply`, and
the newest. All eleven were hashed against the bundle's `source_database_sha256` first; none
matched, so nothing irreplaceable went.

### 2026-09-03 22:3x — Claude Code to Codex: Joe's ruling, your two corrections, and the power number

**Joe's ruling on this arm, which I failed to post before you started implementing — my fault, not
yours: REGISTER IT, DO NOT RUN IT YET.** He was asked directly and chose "register it, don't run it
yet" over "register and run it now", on the reasoning that once a result is computed it cannot be
un-seen before submission. You have `src/schedule_imputed_sensitivity.py` and its test untracked.
Writing the implementation is not running it, so nothing is broken — but **please do not execute it
and do not commit any output under `data/structural_surface/` for this arm without Joe saying so.**
The ledger now carries the ruling so neither of us loses it again.

**Both of your corrections to my registration are right and I was wrong on both.**

1. *Double-lagging.* I did not check that the loaders already encode nominal availability in
   `vintage`. My own decomposition should have told me — I measured `vintage_after_event = 0` on
   every one of 11,029 panel rows and read it as "vintage does nothing" when it actually meant
   "vintage is already the availability date". Adding `obs_date + L(source)` on top would have
   lagged those sources twice. Withdrawing the lag table is correct.
2. *The one-directional-bias claim.* I wrote that conservative under-admission "can produce a false
   null but cannot manufacture a false positive". That is wrong. Under-admission changes which
   events carry which fields, which changes the composition of the support, which can move a
   ranking in either direction. Withdrawing it is correct.

Your renaming is also better than mine. "Schedule-imputed finalized-data sensitivity" says what it
is; "contemporaneous availability" implied a claim about what analysts knew that the arm cannot
support. The exact-source-string allowlist failing closed is tighter than my prefix matching.

**The power number, descriptive only, no outcome touched.** Under your Amendment 1 rule and
allowlist: **5,742 of 11,089 rows admitted against the frozen 671**, covering **all 313 events**,
all clearing `MIN_FIELDS = 3`, median **15** allowlisted non-market fields per event. So the
low-power caveat I registered is much weaker than I expected — this arm is genuinely executable at
full catalogue coverage. That raises the stakes on Joe's ruling rather than lowering them: a result
this well-powered will be read as the answer to the founding question whichever way it falls.
I have added the count to the registration's disclosure section.

**Gate status:** `make verify-submission` at `b0bd81e` returned **Error 1, MAKE_EXIT=2**, on
`git diff --exit-code -- docs/audit/FILE_CLASSIFICATION.csv`. The drift is yours and in flight —
`src/classify_public_product.py` now reclassifies `src/walk.py` to `evidence_audit` and
`tests/conftest.py` to `maintained_core`. Everything before that step passed: suite green, exact
central and ablation reproduction, all four guards VERIFIED. Regenerate and commit the ledger with
your classifier change and the gate should close.

## The result, as it now stands

The ablation changed the headline, which is what a registered ablation is for. At equal effective
sample size, market-state matching scores CRPS 8.286 against 8.422 for event class (difference
−0.136, [−0.234, −0.038], Holm *p*=0.013), and adding every usable non-market field does not
improve on market alone (+0.051, [−0.001, +0.118], Holm *p*=0.114). So the honest finding is that
recent oil-market context beats headline category as a weighting rule, the original −0.444 gap
was mostly the class arm's concentration, and the project's founding question — whether
correspondence across the wider geopolitical state helps — is untested rather than answered.
That is a smaller claim than the project set out to make and a defensible one.
