# G-1 REGISTRATION — the monthly-tier gap arithmetic and the candidate screen
*2026-09-02, Session G. Registered BEFORE the arithmetic is run and before any dossier
is written (charter §2 rule 2). Nothing in this document enters `events`, changes a
registered threshold, or re-judges any run. Amendments are dated and appended.*

## 0. The question, stated exactly

The project was conceived to stand the engine at 1971 and read forward. It cannot.
The corpus's earliest event is `yom_kippur_war_1973` (1973-10-06); the monthly tier
carries 14 reads and **0 scored** against a registered `min_tier_n` of 30
(`data/walk_forward/summary.json`, run `walk_20260903T003422Z`). This registration
fixes what "the gap" means arithmetically, so the number cannot be chosen after it
is seen, and fixes the screen that ranks `data/candidates/pre1987_candidates.csv`
(624 rows, 1946–1986) before the ranking is computed.

## 1. The scoring predicate, as built (read from the code, not from memory)

- `src/walk.py:69` — `"burn_in": 8` — "class needs >= 8 prior members with closed
  outcomes to be scored (§2)".
- `src/walk.py:276` — `burn_in_ok = len(p_pool if e["type"] not in GEO else g_pool) >= self.p["burn_in"]`.
- `src/engine/read.py:201` `Corpus.pool` — a candidate `f` enters the pool of target
  `e` at `as_of` only if `f.type == e.type` (**same class**, closed set of seven) and
  `f.event_date < as_of`, and then
  - `g_closed` iff `f.type` in `GEO_TYPES` and `g_closed_by(f, as_of)` (the IES-90
    window `(d, d+90]` has closed by `as_of`) and `f` has an IES-90 level;
  - `p_closed` iff `f.tier == e.tier` and the price window has closed by `as_of`.
- `src/engine/similarity.py:46` — `GEO_TYPES = (conflict_escalation,
  infrastructure_attack, chokepoint_disruption, sanctions)`. The three non-geo
  classes are `sanctions`' complement: `policy_response`, `opec_decision`,
  `demand_shock`.
- `src/walk.py:603` — `"permits_validation": len(sc) >= p["min_tier_n"]`, where `sc`
  is every read in the tier with `burn_in_ok` true, geo and non-geo together, and
  `min_tier_n = 30`.
- `src/engine/read.py:132` — `tier_of(date)` is `daily` from `daily_start`, else
  `monthly`; the monthly horizon is 3 months (`read.TIERS`).

Two consequences follow from the code and are registered here so they are not
re-derived later:

1. **Burn-in is per class, not per tier.** A class with 8 or fewer prior closed
   members contributes **zero** scored reads however many events the tier holds.
2. **The G pool is not tier-restricted in code** (`g_ok` has no tier test), but it is
   date-restricted, and every monthly-tier event predates every daily-tier event, so
   the pool of a monthly read contains only monthly events. The tier separation of
   protocol §2 holds by date, not by an explicit filter.

## 2. G-1a — the gap arithmetic (what will be computed)

Let `n_c` be the number of monthly-tier events of class `c`, and `a_c` the number
admitted. Three quantities are computed and published, in this order:

**(i) The upper bound.** For each class, scored reads `S_c ≤ max(0, n_c − 8)`, with
equality iff no admitted event's own read falls inside a prior member's unclosed
window. The tier bound is `Σ_c max(0, n_c − 8)`. This is a bound, labelled as one.

**(ii) The minimum admission `A*`.** The smallest `Σ_c a_c` such that
`Σ_c max(0, n_c + a_c − 8) ≥ 30`, computed by exact integer search over allocations
across the seven classes, with the achieving allocation printed. Because every
monthly class currently has `n_c ≤ 8`, each class first absorbs `8 − n_c` events
that score nothing; the search prices that. Where the minimiser concentrates in one
class it is reported as **degenerate** and a balanced alternative is reported beside
it — a tier whose 30 scored reads are one class is not a tier that can carry §6's
per-class blocks or §7's promotion rule.

**(iii) The date-aware count.** For any proposed admitted set of `(date, class)`
pairs, the predicate of §1 is re-applied on the **real dates** — 90-day IES-90
closure for geo classes, 3-month price closure for non-geo — so that clustering is
priced rather than assumed. Every scenario in §4 is reported this way as well as by
(i)/(ii), and the two numbers are published side by side even where they disagree.

**Assumption, stated.** (iii) assumes every admitted geo event receives an IES-90
level. That is checked, not assumed, by diagnostic D3 below; a candidate with no
covering source contributes to the tier's read count and **not** to any later event's
burn-in, and the count is reported both ways.

## 3. G-1b — the candidate screen (registered before it is applied)

The screen is computed on the **blind** sheet only:
`data/candidates/pre1987_candidates.csv`, columns `event_date, actors, source,
source_id, source_detail, suggested_title`.
`data/candidates/pre1987_candidates_outcomes.csv` — which carries
`inside_big_move`, `episode_id`, `monthly_move_pct`, `wti_chg_3m_pct` — **is not
opened by the screen, is not read by the ranking code, and does not appear in any
column of the ranked output.** This is REGISTRATION.md Amendment 1 (D2 finding 2,
selection on outcome by construction) applied to the ranking as well as to the sheet.

### 3.1 Strength (ex ante, from the sheet's own fields)
Parsed from `actors` (names and `ccode NNN` forms, reverse-mapped through the
registered `STATES` table in `src/engine/pre1987_candidates.py`) and from
`source_detail` (`hihost N`, `viol N`, `forout N`, war spell dates):
- **P** — at least one actor whose registered role includes `producer`.
- **T** — at least one actor whose registered role includes `transit`.
- **V** — high severity **in the source's own coding**: MID `hihost = 5`, or MID
  `hihost = 4`, or ICB `viol ≥ 3`, or a COW inter-state war record.
- **M** — multi-source: the same episode appears in ≥ 2 of {ICB, COW, MID} with
  trigger dates within ±31 days and at least one actor in common.

Tiers, fixed here:
- **Tier A (strong)** — `P` and `V` and `M`.
- **Tier B** — (`P` or `T`) and `V`, single-source.
- **Tier C** — everything else.

Duplicates across sources are collapsed into one **episode** by the `M` rule before
tiering; the episode keeps every constituent record's `(source, source_id)` so Joe
can check each source's own row.

### 3.2 Primary-sourceability (predicted, then tested)
No screen can honestly declare a 1956 crisis "primary-sourceable" without attempting
the retrieval (SPINE_REGISTRATION §5: never cite what was not fetched in this
session's own fetch log). So sourceability is reported in two separate columns that
are never merged:
- **`route_predicted`** — the route class the episode's date and actor set imply:
  `FRUS` (US involvement, volume published), `APP` (American Presidency Project:
  presidential address, message, proclamation), `FEDREG` (Federal Register
  codification: executive orders), `UNPK` (`peacekeeping.un.org` mission histories,
  Amendment 1 A.1), `NBER`/scholarly (**secondary only, never primary**), or `none`.
  This is a prediction and is labelled as one in the output.
- **`route_tested`** — blank unless a retrieval was attempted in this session, then
  `retrieved` or the failure as returned (HTTP status, or "no document"). Only
  episodes with `route_tested = retrieved` may be called primary-sourceable.

## 4. Scenarios reported (all published as computed)
1. **Status quo** — the 14 events: bound, `A*`, date-aware count.
2. **`A*` concentrated** — the minimiser of §2(ii), flagged degenerate.
3. **Balanced** — the smallest admission that puts ≥ 30 scored reads in the tier with
   **no class contributing more than half** of them, and with ≥ 3 classes scoring.
4. **Reachable** — scenario 3 restricted to Tier A episodes whose `route_predicted`
   is a primary route, i.e. what the archive can actually support. If this scenario
   cannot reach 30, that is the answer and it is published as the answer.

## 5. Diagnostics (registered now; published whichever way they come out; gate nothing)
- **D1 — the monthly Big Moves 1946–1986.** The episodes of
  `data/big_moves/wti_monthly.json` inside the range, with the years they cover and
  the years they do not.
- **D2 — is the pre-1973 monthly P target a traded price?** The distribution of
  3-month percent changes in `fred.WTISPLC` by era (1946-01..1972-12, 1973-01..1986-12,
  1987-01..2026-07): n, mean |change|, sd, IQR, share of months with |change| ≥ 10 %,
  and the count of distinct price levels. Reason registered in advance: the monthly
  tier's P target is this series; US wellhead crude was an administered posted price
  under Texas Railroad Commission prorationing for most of the first era, and if the
  series barely moves there then a monthly-tier P score before 1973 measures an
  administrative process, not a market. This is a statement about the *instrument*,
  registered before the numbers are seen.
- **D3 — IES-90 label availability pre-1987.** Per `src/state/ies90.py` `COVER`,
  which of `midi`(1993–2014), `war`(1816–2007), `war_intra`(1816–2014),
  `mid`(1816–2014), `icb`(1918–2021), `ged`(1989–2025) cover each candidate's date;
  the share of sheet rows with ≥ 1 covering source.

## 6. The objection, registered before the work rather than after it

The brief that commissioned this work asks for dossiers "prioritising ones inside a
monthly WTI Big Move". **Admitting events conditional on the realized price move is
selection on the outcome**, and it is the same defect `REGISTRATION.md` Amendment 1
was written to remove from the sheet. Its consequence is specific, not decorative: the
walk's P climatology baseline is the unconditional outcome distribution of the class's
prior members (`src/walk.py:262`, `clim_P`), so a corpus admitted for having moved the
price inflates that baseline's dispersion, and both the engine's CRPS and the skill
score computed against it become uninterpretable — the engine would be scored against
a climatology it helped select. The materiality (M) precision/recall block is
corrupted directly, since Big-Move membership is exactly its label.

Session G therefore does the following, and says so where anyone can see it:
- the ranking of §3 uses **no** outcome field;
- the five episodes named in the brief (Suez 1956, the Six-Day War 1967, Libya 1970,
  Tehran/Tripoli 1971, Iraq Petroleum 1972) are worked because **Joe named them on
  historical grounds**, which is a prior, not a peek at the price;
- Big-Move overlap is reported as a **diagnostic column in the report only**, after
  the ranking, never as a ranking key;
- if Joe wants Big-Move-conditioned admission anyway, the way to have it without
  destroying the P tier is stratified admission with a recorded inclusion
  probability per stratum, so climatology can be reweighted. That is a decision for
  him and would need its own registration and an ADR-equivalent note here.

## 7. Outputs
- `src/g_monthly_gap.py` — the code, reading `data/oil.db` **read-only** and the blind
  sheet; writes nothing to any registered table.
- `data/candidates/G1_GAP.md` — the arithmetic and the scenarios, as computed.
- `data/candidates/G1_GAP.json` — the same numbers, machine-readable.
- `data/candidates/pre1987_ranked.csv` — the episode ranking with the screen's
  columns, `route_predicted`, and `route_tested`.

## 8. What this registration does not do
It does not admit an event. It does not write to `events`, `data/events.csv`,
`situation_state` or `event_outcomes`. It does not change `burn_in`, `min_tier_n`,
the tier split, the horizon, or any registered threshold — a gap that is closed by
lowering the bar is INV-6 territory and is not on the table. It does not open
`pre1987_candidates_outcomes.csv`.
