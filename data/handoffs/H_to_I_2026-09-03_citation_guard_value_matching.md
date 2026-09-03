# H → I, 2026-09-03: the citation guard resolved "15 of 43" to an unrelated field, and stayed green through a re-run that changed it

`tests/test_citation_guard.py` is described in `conftest.py` as "the test that goes red when a
re-run supersedes the numbers in the prose". Today's Big Moves re-run is exactly that event, and the
guard stayed green (20 passed). Reported, not patched — your tree.

## What happened

Amendment 4 re-ran Big Moves under the registered clustering rule. Brent went from **43 episodes /
15 with no identified event** to **44 / 14**. `README.md:133`, `docs/BRIEF.md:76` and
`docs/PAPER_DRAFT.md:332` all still say "15 of 43". The guard did not notice.

## Why — value matching, not path binding

`docs/citation_inventory.json` resolves README:133's `15` to:

    data/walk_forward/summary.json :: tiers.daily.G.spa.n_models

The sentence is about Brent episodes with no identifiable event. The path is the number of models in
a daily SPA test. They are unrelated; they both happen to equal 15. The same is true of the `43` on
that line. So the claim is filed RESOLVED, and
`test_citation_guard_every_in_record_claim_still_resolves` keeps passing as long as *some* leaf
anywhere in the declared record still equals 15 — regardless of whether the number the sentence is
actually about has changed.

`data/big_moves/summary.json` **is** in the declared record, so the right path was available; the
matcher simply had no reason to prefer it. The 1049 AMBIGUOUS claims in `counts` are the same
mechanism showing itself.

## And a way my own change makes this worse, which you should know about

Amendment 4 publishes BOTH rules — the registered one at the top level and the superseded one under
`as_computed`. So `data/big_moves/summary.json` now legitimately contains `n_episodes: 43` and
`no_identified_event: 15` as well as 44 and 14. A value matcher will therefore *always* be able to
resolve a stale "15 of 43", even against the correct object. Publishing the old numbers beside the
new ones was Joe's ruling and I think it is right, but it removes the last chance a value-based
guard had of catching this one.

## The ask

Bind a claim to a PATH, not a value — at minimum for the numbers the published prose leans on. A
sentence that says "of 43 largest Brent moves" should be pinned to
`data/big_moves/summary.json :: brent.n_episodes` and go red when that leaf changes, whatever else
in the record happens to equal 43. If full path binding is too big, an allow-list of the dozen
load-bearing claims would have caught today's change.

Until then the guard proves "every published number equals something in the record", which is a
weaker statement than the one `conftest.py` advertises, and I would not want Joe reading the green
as confirmation that the prose is current. He is updating the three documents by hand today; this
note is about the next re-run, not this one.
