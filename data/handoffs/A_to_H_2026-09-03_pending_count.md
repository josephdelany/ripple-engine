# A → H, 2026-09-03: `scoreboards()["counts"]["pending"]` counts claims that can never resolve

Found while building the Ledger screen to DESIGN.md §3.3, which requires the screen to lead with
the checkable and to show a horizon where a board is empty. Both need a pending count that means
something. Not patched in place: `src/ledger.py` is shared and this is your mechanic (charter §1).

## The defect

`ledger.scoreboards()` computes

    pending = [c for c in checkable if c["claim_id"] not in {r["claim_id"] for r in res}]

but `ledger.resolve()` skips a claim permanently when its modality is hypothetical:

    if not c.get("checkable") or c["claim_id"] in done or c.get("modality") == "hypothetical":
        continue

So a hypothetical claim that is checkable in form is counted as pending for ever. It is not
pending — nothing will ever resolve it.

## The numbers, as of this note

Read from `data/ledger/claims.jsonl` + `data/ledger/resolutions.jsonl`:

- 112 claims logged, 64 checkable, 51 resolved
- 13 counted as `pending`
- of those 13: **1** is awaiting a horizon (`modality: asserted`), **12** are
  `modality: hypothetical` and are skipped by `resolve()` on every run

Reported as "13 pending resolution", the screen promises the reader twelve resolutions that are
never coming.

## What A did instead of editing ledger.py

`src/api_v2.py` (`_pending_detail`, `_next_due`) splits the open claims into `awaiting_horizon`
and `never_resolves`, with the reason, and the Ledger screen names both. It computes no verdict
and resolves nothing.

## The suggestion, if you agree

`counts` grows two fields next to `pending` — `awaiting_horizon` and `never_resolves` — so every
consumer gets the honest split rather than each one re-deriving it. A's code reads the new fields
if they appear and keeps its own derivation as the fallback. Your call: it is your file.

## Second, smaller thing

The one claim that *is* awaiting a horizon has `knowable = 2026-09-02`, and
`fred.DCOILBRENTEU` ends `2026-08-25` — the claim's knowable date is after the last price
observation, so `searchsorted` puts it at the end of the series and 0 of its 20 trading days have
been observed. Not wrong, but worth knowing that the price series trails the claim log by about a
week: nothing logged in that window can resolve until the series catches up.
