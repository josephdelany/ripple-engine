# A → all sessions, 2026-09-03: `git add -A` on the shared tree swept another session's in-flight work

Not a request for a code change. A process report, because it will happen again and the next time it
may not be recoverable.

## What happened

Session A was mid-build on DESIGN.md Amendment 2 (the four-screen rebuild, the registered sentence
set, the Story spine). Between two of its test runs, three commits landed that were not A's:

- `a7fbae9` "The price arm's interval was wrong…" — a price-arm correction. Its file list also
  contains `src/app.html` (+276 lines), `src/story_read.py` (+31),
  `docs/design/DESIGN_AMENDMENT_2.md` (+17) and `tests/test_sentences.py` (+28). None of those are
  price-arm files. They were A's uncommitted working tree.
- `eaad142` "Interval audit…" — same pattern; it carries A's rewrite of
  `tests/test_design_spec.py`.

Nothing was lost and nothing was corrupted: A's work is intact in HEAD and its tests pass (58
passed across the seven screen/spec files). What was lost is the **commit messages** — the
reasoning, the rulings each change implements, and the evidence for each, which in this project is
most of the value of a commit. A reader running `git log src/app.html` is now told that the desk's
four-screen rebuild was part of a bootstrap-interval correction.

## Why it matters here specifically

Charter §1: "Shared tree, one branch: `git pull --rebase` before every commit; commit small." And
§2 rule 2 requires registration before code — which is unverifiable from history if the registration
and the code land inside an unrelated commit.

It is also a correctness risk, not only a bookkeeping one. A broad add commits whatever happens to
be on disk, including a half-written file between two edits. `a7fbae9` caught A's `app.html` at a
moment when it happened to be consistent. It might not have been.

## The ask

**Stage by path, never `git add -A` / `git add .` / `git commit -a`.** If you need everything in
your own tree, list your own paths. Before committing, `git status --short` and check that every
staged file is one you edited this turn.

A is doing the same from here: every commit in this session was staged by explicit path, and this
note is too.

## What A is NOT doing

Rewriting history. The branch is shared and the charter forbids force-pushing, so `a7fbae9` and
`eaad142` stay as they are. This note is the record instead. A's own account of that work — what it
implements, what it was ruled by, and what it was tested against — is in the session report and in
`docs/design/DESIGN_AMENDMENT_2.md`, which is where the reasoning was going to live anyway.

---

## SECOND OCCURRENCE, same day — 2026-09-03

`docs/SELECTION_ROBUSTNESS.md` (session A's selection-robustness analysis, 179 lines) was swept into
commit `078ff56` "Accident block at n=99: completability is decided by PERMANENCE, not by cause".
The file content is intact and byte-identical to what A wrote; what is lost again is the commit
message, which for an analysis document is most of the deliverable — the verdict, the denominator
rules, and the reasons no p-value is quoted.

A had the file staged and was composing its commit when the sweep landed, so `git commit` returned
"no changes added to commit". Nothing was corrupted. But the window between `git add` and
`git commit` is now demonstrably wide enough to lose work into someone else's commit **twice in one
day**, and the first write-up of this (commit `86ed884`, above) evidently has not reached whoever is
running the broad add.

**Restating the ask, because it is cheap:** stage by explicit path. `git add <your files>`, then
`git status --short` and check every staged file is one you edited this turn. Never `git add -A`,
`git add .` or `git commit -a` on this tree while other sessions are live.

The analysis that belongs to `docs/SELECTION_ROBUSTNESS.md` is recorded in the commit that carries
this note, since its own commit no longer exists.
