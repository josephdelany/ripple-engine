# K → H, 2026-09-03 — `audit_ies90.py` is now blind, so the comparison in `audit_reader.py`'s header is stale

`src/audit_reader.py`:22–24 says:

> It deliberately differs from audit_ies90.py on one point: audit_ies90 shows the engine's
> level before asking, because there Joe is checking a label against source records; here
> showing the gold or the reader's call first would anchor the very judgement being measured,
> so both are hidden until Joe has answered.

**You were right about the principle and the exception no longer holds.** Under
`OUTCOME_MAPPING.md` **Amendment 4.2** (2026-09-03, Joe's ruling), `audit_ies90.py` is blind
too: the engine's level, DEAL, `basis` and `rule_fired`, each record's `level_contributed`
and rule id, and the `event_id` are all withheld until the answer is recorded. The two tools
now behave the same way, and `audit_reader.py`'s header is the only place in the repo that
still says otherwise. Yours to correct — K did not touch it.

## The thing worth knowing beyond the doc fix

The rationale in your comment — *"there Joe is checking a label against source records"* — is
a real reading, and it is not the one `docs/AUDIT_GUIDE.md` or `WALK_FORWARD_PROTOCOL` §7
use. The guide opens *"You are the human half of an inter-rater reliability check … Cohen's κ
measures whether an independent reader agrees with the machine's mapping"*, while
`OUTCOME_MAPPING.md` A1.3 says *"Joe checks the source rows against the sources; he does not
code."* Those are two different exercises with two different validities, and the repository
was running the κ one through a display built for the checking one. Amendment 4.2 makes the
κ reading sound; it deliberately does **not** decide which exercise the §7 gate should be —
that is Joe's, in B's protocol file. Recorded as A4.2.6.

## What changed, if you want to mirror any of it

- `render_row()` is a **pure function** returning the exact lines shown before the prompt, so
  a test can assert on what the human sees rather than on what the code intends to print.
  (The old test monkeypatched `builtins.print`, which silently stopped intercepting anything
  once `show()` gained an `echo=print` default — the patch binds too late. Worth checking
  whether `test_audit_reader.py` has the same hole.)
- `tests/test_audit_blind.py` renders every live row and fails on any engine-derived level
  token. It also asserts the record **survives** redaction — an absence-only test passes
  trivially on a blank screen.
- The reveal is `--reveal`, off by default: a per-row reveal does not contaminate the row it
  follows but does contaminate the ones after it, which is a within-κ drift in the measurand.
- Rows answered under the old display are marked `superseded` with the reason and re-asked,
  never deleted.
