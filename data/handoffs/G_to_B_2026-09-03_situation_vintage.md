# G → B, 2026-09-03 — the situation fields' `knowable_at`, recomputed from dossier document dates

Registered first in `docs/g/G3_REGISTRATION.md` (+ Amendments 1 and 2), computed by
`src/situation_vintage.py`, published in full at `docs/g/SITUATION_VINTAGE.{md,json}`.
Session G writes to no table. Rule (e) is a **proposal to session A**, whose document
`WORLD_STATE_FRAMEWORK.md` Amendment A is; until A adopts it, `situation_state` is
unchanged and none of this is yet visible to `read.py`. **Nothing below re-judges any run.**

## 1. The numbers

`WALK_FORWARD_PROTOCOL.md` Amendment H binds `read.py:_apply_knowable` to five fields.
Across 313 events those five carry **786** coded values.

| | values | kept at t | dropped at t | events with ≥1 field at t |
|---|---|---|---|---|
| Amendment A, as published (`data/state/situation_knowable.json`) | 786 | **60** | 726 | **51** of 313 |
| with rule (e) | 786 | **83** | 703 | **62** of 313 |
| *diagnostic only, gates nothing (Amdt 2)* | 786 | *86* | *700* | *64* of 313 |

Net **+23** values (26 gained, 3 lost). **+11** events net gain a situation field at t
(13 gain, 2 lose their last one). Per field:

| field | values | kept before | kept after |
|---|---|---|---|
| `actor` | 153 | 28 | **38** |
| `target` | 220 | 32 | **38** |
| `tempo` | 187 | 0 | **7** |
| `conflict_scope` | 184 | 0 | **0** — and structurally cannot be more; see §3 |
| `asset_role` | 42 | 0 | **0** — no dossier carries a usable receipt for a chokepoint entity |

Restricted to the 35 events that have a dossier: 113 values, **3 kept before → 26 kept after**.

The BEFORE column is **recomputed** from Amendment A's rules in G's own code and reproduces
session A's published file exactly (313 / 60 / 726 / 262, and all three rule counts). That check
is asserted in `tests/test_g_situation_vintage.py`; if it ever fails, the AFTER number is void.

## 2. What this is worth, and what it is not

It is worth 23 values on 313 events. It does **not** move the corpus off "mostly blind at t":
251 of 313 events still have no situation field at their own date, so most reads are still
retrieved on the market block alone, exactly as Amendment H said they would be. The gain is
concentrated in the dossier-covered episodes — Kuwait 1990, Desert Storm, ILSA, Desert Fox,
the hostage crisis — which are the reads a reader will look at first. **278 of 313 events have
no dossier at all**, and that (not the rule) is the binding constraint: 514 of the 786 values
were refused for `(e.0) no dossier for this event`.

## 3. Finding 1 — `conflict_scope` reads 120 days into the future, and always has

`src/situation_record.py:_conflict_scope` codes `isolated`/`campaign`/`war` from the count of
same-dyad geopolitical events at **`abs(days) <= 120`** — a symmetric window. Half its input
postdates t. Consequences, in order of how much they should worry you:

1. **`events.sr_conflict_scope` is a contaminated column.** Any surface that reads it directly,
   rather than through the vintage-filtered join, is showing a field computed from the 120 days
   *after* the event. `read.py` does not (Amendment H routes it through `situation_state`), and
   Amendment A's rule (c) has been dropping it for the accidental reason that its source string
   starts `corpus:`. That is luck, not a guard.
2. **No amount of sourcing can fix it.** Rule (e.8) therefore dates it `event_date + 120 days`
   for the whole corpus — its own information horizon, replacing rule (c)'s arbitrary coding
   date. This **cannot raise** the kept count and is reported separately from the coverage gain.
3. **`conflict_scope` can never be a target-side feature of any read.** It is available only as
   an analog-side feature, and only 120 days after the analog's own date. If any menu item
   weights it for the target, that item is weighting a field that is always `None` at t — worth
   checking against `data/walk_forward/menu.json`, which is yours.

## 4. Finding 2 — the join loses a field twice, so 726 understates the cost

`src/state/situation_state.py:join()` calls `situation_rows_at(conn, eid, edate)` and inserts
**only the kept rows**. A field not knowable at the event's own date never reaches
`situation_state`. But `read.py:_load_panel` selects *all* vintages and `_apply_knowable`
filters them by `as_of` — the engine is built to receive rows it is never sent. So a field that
was not knowable at an event's own date, but *is* knowable years later when that event is
retrieved as an **analog**, is invisible then too. The analog side of the retrieval is losing
fields it is entitled to.

This is session A's file and G has not touched it. It matters to you because it changes what
"+23" means: under a join that stored every row with its vintage, the same 786 values would also
serve the analog side, where far more than 83 of them are legitimately visible.

## 5. Finding 3 — `tempo` is corpus-relative and the rule does not repair that

`tempo` is `first`/`nth` from the corpus's own prior events. Rule (e) can date it; it cannot make
"first" mean first in the world rather than first in a 313-event sample. Every `tempo` gain here
is `nth`, which is the robust direction (a prior clash was found, and finding one cannot be an
artefact of incompleteness). A `first` that rests on corpus silence is not evidence of a first
clash, and none is claimed.

## 6. What G asks of B

Nothing blocking. Three things to know when the next run is planned:
- if A adopts rule (e), the situation block's coverage at t moves 60 → 83 and
  `data_state`'s "events with no situation field at t" moves 262 → 251;
- `conflict_scope` should be treated as analog-side-only in the menu and in any future
  similarity weighting, on §3 rather than on this rule;
- the honest headline stays what Amendment H already said: the point-in-time engine is nearly
  blind on the situation block, and the remedy is dossiers, not code. 278 events need one.
