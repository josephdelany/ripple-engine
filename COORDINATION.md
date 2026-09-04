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

## The result, as it now stands

The ablation changed the headline, which is what a registered ablation is for. At equal effective
sample size, market-state matching scores CRPS 8.286 against 8.422 for event class (difference
−0.136, [−0.234, −0.038], Holm *p*=0.013), and adding every usable non-market field does not
improve on market alone (+0.051, [−0.001, +0.118], Holm *p*=0.114). So the honest finding is that
recent oil-market context beats headline category as a weighting rule, the original −0.444 gap
was mostly the class arm's concentration, and the project's founding question — whether
correspondence across the wider geopolitical state helps — is untested rather than answered.
That is a smaller claim than the project set out to make and a defensible one.
