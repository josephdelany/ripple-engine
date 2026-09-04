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

## Completion ledger — this phase

- [x] Coordination channel restored and lanes recorded.
- [ ] Field composition disclosed in `docs/PAPER.md` §2–§3 and §6 (Claude).
- [ ] Provenance boundary checked, documented and cited in paper/README (Claude).
- [ ] Document status machine-enforced; 154 banners added (Claude).
- [ ] Test count reconciled to one run across `SUBMISSION_STATUS.md` and `PUBLIC_PRODUCT_CLOSURE.md` (Claude).
- [ ] Machine verdict regenerated under Amendment 3 (Codex; code landed 509cf5a/57e44fd, `summary.json` not yet regenerated).
- [ ] Component/concentration ablation registered, run, frozen (Codex; in flight).
- [ ] Headline and résumé rewritten from the ablation result (Claude, blocked on Codex).
- [ ] `make verify-submission` green with zero worktree drift; new annotated tag.
- [ ] 30-row label audit — **Joe's gate**, per `SESSION_CHARTER.md` §6. Nothing rises above SUGGESTIVE without it.
