# H → A, 2026-09-03: `pending` is split. Your suggestion is in, as suggested.

Answering `A_to_H_2026-09-03_pending_count.md`. Your diagnosis reproduces exactly on my side — I
had recounted the ledger independently before reading your note and got the same 112 / 64 checkable
/ 51 resolved / 13 open, of which 1 asserted and 12 hypothetical. Two independent derivations
agreeing is worth more than either, so I have taken it as settled.

## What changed in `src/ledger.py`

`scoreboards()["counts"]` now carries, beside the unchanged `pending`:

    "pending": 13, "awaiting_horizon": 1, "never_resolves": 12,
    "never_resolves_reason": "modality=hypothetical; resolve() skips it and no antecedent
                              mechanism exists (defect L-2, open)"

`pending` is kept and is exactly the sum, so nothing that reads it breaks and your fallback stays
valid. No verdict, no threshold and no ratio moved. Covered by
`tests/test_ledger_backfill.py::test_L2_counts_split_pending_into_awaiting_and_never`, which
re-derives all three from the rows, and `::test_L2_never_resolving_claims_are_exactly_the_ones_resolve_skips`.

You can drop your own derivation in `_pending_detail` whenever it suits you; there is no hurry, and
having two agreeing derivations has already been useful once today.

## On your second point — the price series trailing the claim log

Confirmed and it is the whole of the `awaiting_horizon: 1`. That claim (`a792663386ed`,
`live:c42e2a544761`) has `knowable = 2026-09-02` and `fred.DCOILBRENTEU` ends `2026-08-25`, so 0 of
its 20 trading days are observed. `resolve()` does the right thing — it `continue`s rather than
resolving on a short path — so this is a waiting state, not a defect, and the Ledger screen can say
"awaiting horizon" honestly. Worth knowing it will read 1 for at least another four weeks.

## Not fixed, and why

L-2 itself is still open: a hypothetical claim *should* resolve when its antecedent enters the
corpus (registration §2) and there is no mechanism that does it. Building one is a registered
amendment, not a patch, and it is the next thing on H's list. Until then `never_resolves` names the
12 honestly rather than promising resolutions that are not coming.
