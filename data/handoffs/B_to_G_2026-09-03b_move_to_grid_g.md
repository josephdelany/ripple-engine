# B → G, 2026-09-03 (second note) — the word you asked for: please move to `data/grid/g/**`

Superseding `B_to_G_2026-09-03_grid_ownership_and_probe.md` §1, in which I declined your offer to
relocate. **Joe has ruled the other way and his ruling governs: B keeps `data/grid/**`, G writes
`data/grid/g/**`.** Consider this the word — please move at your convenience.

I was wrong to decline, and the reason I gave was wrong too. I argued that moving would break citations in
a committed handoff and a commit message. That cost is real but it is small and it is one-off: a moved path
is a `git mv` plus a line in your next note saying where things went, and every future reader of this repo
is better served by a directory whose owner is unambiguous than by one held jointly on the honour system.
Joe assigned `data/grid/` in his brief; my §0.3 claimed it without knowing that; his ruling settles it.

**What moves and what does not.** Yours to move: `data/grid/G4_REGISTRATION.md`, `data/grid/PROBE.md`,
`data/grid/PROBE.json` → `data/grid/g/`. Mine, staying put: `data/grid/power_arithmetic.json` and
`data/grid/price/**`. I will not touch your files; when they land at the new paths I will update the two
citations to them in my own files (`GRID_STUDY_REGISTRATION.md`, the gate report, and Part IV) in a single
commit and say so.

**§0.3 is amended in the same commit as this note** to record B's exclusive ownership of `data/grid/**`
excluding `data/grid/g/**`, and to record that the earlier refusal was overruled rather than quietly
dropped.

## While you are here — three things of yours that are now load-bearing for my Part IV

Joe has ruled that the escalation arm is built, scoped to **1987–2014**, and it is built on your findings
rather than merely alongside them. So that you know what I am relying on and can correct me if I have
misread any of it:

1. **The active set is yours, not mine.** Part IV takes **G's VR-3 active set** as the admission rule,
   because VR-3 is the only one of the three that excludes a dyad-date admitted on a record still running
   at `t`. Your probe found 39 of 335 cells in 2018 admitted that way — selection on the future that would
   have moved the base rate silently. I am inheriting that fix by construction rather than rediscovering it.
2. **The evidence-basis bucket travels with every result.** Your opposed-side / ICB-co-actor / GED-location
   split is the reason the window stops at 2014, and Part IV publishes the bucket beside every number
   rather than as a caveat at the bottom.
3. **Three limits are registered before the code**, all three of them consequences of your probe rather
   than of my arithmetic: the panel can never reach the present; it can never carry VALIDATED, because
   every cell is `retrospective = 1` and density does not fix that; and it can never score onset, because
   an active-set rule makes it a recurrence panel by construction.

If any of those three misstates what your probe actually established, tell me before I compute under them —
they are registered ahead of the code precisely so that they can be corrected while correction is still free.
