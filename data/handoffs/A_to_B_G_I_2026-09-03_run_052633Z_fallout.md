# A → B, G, I — 2026-09-03: three reds that arrived with `walk_20260903T052633Z`

Found while wiring the desk to the new run under Joe's brief. None is in a file A owns; none is
patched here. A's own screen and spec tests are green (83 passed across ten files).

Full suite on this tree: **850 passed, 7 failed, 13 skipped, 1 xfailed.** The seven are the three
groups below.

---

## 1 → B: the new run DROPPED `diagnostic_hostile` from `summary.json` (4 reds)

`tests/test_diagnostic_hostile.py` fails four times with `KeyError: 'diagnostic_hostile'`.

- `data/walk_forward/summary.json` at run `052633Z` has these top-level keys:
  `G_joint_across_tiers, big_moves_knew, data_state, determinism, fdr, figures, filtration_audit,
  generated_at, leakage_test, limits, menu, permutation, placebo, power, protocol, regime_blocks,
  registered, run_id, seal_check, spec_curve, tiers, verdict`
- **`diagnostic_hostile` is not among them.** It was present under `003422Z` — those same four tests
  passed on this tree earlier today, and `tests/conftest.py` lists the file in the DB-free CI gate,
  so it runs everywhere and would have been caught in CI too.
- The block is produced by `src/engine/diagnostic_hostile.py` (Amendment K).

This is not a stale test. **The run published less than the previous run did**, and Amendment K's
diagnostic — whose registered point is that it is present, labelled, and gates nothing — is now
absent from the published object. Either the writer stopped being called in the 052633Z path or it
raised and was swallowed.

Worth checking before the next run seals: the archive keeps `scores/weights/reads.jsonl.gz` but
**not** `summary.json`, so once another run supersedes this one there is no archived summary to
diff against. That makes a silently dropped key unrecoverable after the fact.

## 2 → G: `test_g6_2_the_run_is_pinned_to_the_published_one` is pinned to the old run (1 red)

    AssertionError: the pinned run is no longer the one summary.json publishes
    assert 'walk_20260903T052633Z' == 'walk_20260903T003422Z'

The test is doing exactly what it was written to do. It needs re-pinning to `052633Z`, together with
any number in `docs/g/**` that was read from `003422Z`. A did not re-pin it: which numbers in the
era-confound work move with the run is G's call, not a find-and-replace.

Note the headline that moved, in case it changes G's reading: escalation vs climatology went from
skill −0.097, CI [−0.180, −0.018] (**excludes** zero) to −0.084, CI [−0.175, **+0.004**], *p* 0.076,
n 100 — it now **crosses** zero. Price vs climatology is unchanged in state (−0.074, CI
[−0.140, −0.021], *p* 0.011). Persistence gap −0.304.

## 3 → I: two untraceable numbers entered the published documents (1 red)

    2 number(s) entered the published documents that cannot be traced to any declared path:
        README.md  614
        docs/BRIEF.md  614

`tests/test_citation_guard.py::test_citation_guard_unsourced_has_not_grown`. The guard is working;
`614` appears in both documents with no declared path behind it. Either register the object that
holds it in `src/citation_guard.RUN_OBJECTS`, or accept it and regenerate. Unrelated to the run.

A's three design documents live in `docs/design/` and are outside the guard's `DOCUMENTS` list
(`README.md`, `docs/BRIEF.md`, `docs/PAPER_DRAFT.md`, `docs/EXPLAIN.md`, `OPEN_ITEMS.md`), so this
is not A's text.

---

## What A changed, so you can rule it out

`src/api_v2.py` (read-only `/api/desk`), `src/app.html`, `tests/test_record_bar.py`,
`tests/test_sentences.py`, `docs/design/DESIGN_AMENDMENT_2.md`. Nothing writes to
`data/walk_forward/**`, `summary.json`, the corpus, or any published document.
