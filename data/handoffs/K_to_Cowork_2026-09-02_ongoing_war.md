# K → Cowork, 2026-09-02 — Amendment 4 for the paper: what the escalation target was measuring, and what it measures now

Source of truth: `OUTCOME_MAPPING.md` **Amendment 4** (registered at commit `c74ccd6`,
before the code). Counts: `data/state/ies90_amendment4_counts.json`. Persistence overlap:
`data/state/ies90_amendment4_persistence_overlap.json`. This is red team 2 finding 3 /
Tier A5. **Nothing here re-scores anything**; no number in the paper changes because of
this text, and the published runs stand.

## 1. The sentence the paper currently cannot support

The escalation target (IES-90) asked what level of violence a source recorded in
W = (d, d+90] near an event. It never asked whether that violence had anything to do with
the event. Amendment 1.1 had fixed this for ICB and Dyadic MID — a crisis or dispute
already running at `d` yields no level — and the fix was never extended to COW War or UCDP
GED. **All 54 level-3 "war" labels came from exactly those two unfixed sources.**

So a large share of "escalation to war in the 90 days after the event" was **a war that was
already running before the event**, and the persistence baseline is built from the same
sources. Target and baseline therefore shared variance *by construction*, and
"persistence beats the engine for escalation" (−0.469, run 193022Z −0.467) was partly a
statement about that construction rather than about historical analogy.

## 2. Two corrections to the version of this in `docs/red_team_2.md`

Both were found by re-deriving the finding rather than repeating it, and both are recorded
in §A4.1.

1. **`deaths_ged_pre90` was summed over `[d−89, d]` — including the event day itself.** For
   an event whose own day is the violent one, most of the "before" figure *is* the event.
   Recomputed strictly before `d`: Ukraine 2022 **20,473 → 79** (20,394 on the day itself);
   Israel–Hamas 2023 **3,835 → 28**; Israel–Iran 2025 **959 → 4**; `me_rough_rider_2025`
   **537 → 173**. The two headline examples of "a war already running" are the opposite —
   they are war **onsets**, and level 3 on them is correct. The GED count is **27 of 38**
   with ≥ 250 deaths genuinely before the event, **not 31**. Do not print "four in five".
2. **The same defect exists with the sign reversed and was not reported.** An undated
   "ongoing" record produced *no level*, which then fell through to **level 0 = "none"**.
   `soleimani_strike_2020` was labelled "no escalation" while UCDP recorded 177 deaths in
   the window against 0 before — the location evidence discarded by dyadic precedence, the
   dyadic evidence undated. (Amendment 4's own §A4.1(iii) put 18 events in this class;
   computing the rule showed only **3** were true false-zeros, and §A4.10 corrects that
   figure. `abqaiq_attack_2019` is *correctly* level 0: UCDP looked at Saudi Arabia across
   the window and found 1 death.)

## 3. The counts to quote

| level | before | after Amendment 4 |
|---|---:|---:|
| 0 none | 76 | 73 |
| 1 threat or display | 6 | 9 |
| 2 use of force | 48 | 30 |
| 3 war | **54** | **20** |
| `no_independent_outcome` | 3 | **55** |
| **events with a level** | **184** | **132** |

**59 of 187 labels change; 52 become `no_independent_outcome`.** The G target loses 28 % of
its n, **and it loses it non-randomly** — disproportionately the big wartime oil shocks.
The limitations section has to say that, not just report a smaller n: after Amendment 4 the
escalation target is defined on *events that did not occur inside a conflict already
running at the same level*, which is a narrower claim than "escalation".

## 4. The honest version of the persistence sentence

Measured (§A4.11), not asserted. Target and baseline recomputed under both rule sets:
shared rank variance ρ² **0.640 → 0.407**; on the 120 events scorable under both rules,
**0.484 → 0.407**. So **about a third of the fall is the rule and the rest is selection.**

> The escalation target was partly, not wholly, an artefact of the labelling rule. After
> the rule is corrected, 41 % of its rank variance is still shared with a persistence
> forecast and 73 % of its labels are still exactly what persistence would have said —
> which is a real property of conflict, not a defect. The published comparison stands as
> published; whether the engine beats persistence on the corrected target is a separate
> run, reported separately.

Three things not to write:
- **Do not present a corrected result.** §A4.7: no published run is re-scored, and the
  pre- and post-amendment runs are never pooled.
- **Do not call the null overturned or confirmed by this.** The G/P null does not move
  here; what moves is what "escalation" and "beats persistence" *mean*.
- **Do not merge Amendment 4's exclusions with Amendment 3's** (Session F's hostility
  precondition). They are orthogonal rules and the counts stay separate.

## 5. One more limitation to carry

UCDP GED remains a **location** source — deaths in the country, not deaths between the
event's actors — because the cached extract has no dyad field and there is no `UCDP_TOKEN`
in this environment. Amendment 4 narrows that weakness (an increment in the location is
closer to an event effect than a level in the location) and does not close it. §A4.9 lists
what the amendment explicitly does **not** fix.
