# G-4 REGISTRATION — the dyad-date escalation panel: the grid, the "active" rule, and the vintage stamp
*2026-09-03, Session G. Registered BEFORE `src/grid_labels.py` is written and BEFORE any
count is computed (charter §2 rule 2). Nothing here writes to `events`, `event_outcomes`,
`situation_state` or `data/walk_forward/**`. B owns `src/walk*.py` and `data/walk_forward/`
this session; G writes only `data/grid/**` and `src/grid_labels.py`. Amendments are dated
and appended, never edited.*

## 0. What was read before this was written

A parser and a rule cannot be specified for data nobody has opened, so the following were
read first and are named so the order is checkable:

- `src/state/ies90.py` — `score_event(d, A, pairs, L, src)`, the `COVER` map, `window()`,
  `pre_window()`, and Amendment 4's continuation predicate `covered_by()`. **The grid reuses
  this scorer unchanged**; it already carries Amendment 4 across COW War and GED, so the
  defect the brief warns about is not inherited.
- `src/state/outcomes.py` — `load_mid`, `load_icb`, `_actors_and_pairs`, and the shape of
  `A` / `pairs` / `L`.
- `src/engine/pre1987_candidates.py` `STATES` — the registered producer/transit roles, the
  same table G-1's screen used.
- `WORLD_STATE_CODEBOOK.md` §Rules and **Amendment 1** — session A's already-registered
  resolution of exactly this vintage problem. §4 below is built on it and does not invent a
  rival convention.
- `data/state/raw/**/*.meta.json` — the HTTP `Last-Modified` of each dataset file actually
  parsed. These are the release dates used in §4, read from the tree, not recalled.
- `WALK_FORWARD_PROTOCOL.md` Amendment B.1 (the pre-window level) and Amendment J.3 (ΔIES).

**Not computed before this file was committed:** no active-set size, no marginal
distribution of L or ΔIES, and no vintage-survival count. §6's tables are produced by the
code, after this file is in git.

## 1. The grid

- **Unit of observation:** the dyad-date `(a, b, t)`, `a < b`, both in the corpus entity
  register (`src/state/countries.py`, 59 countries).
- **Grid dates:** **calendar month-ends**, 1987-01-31 … 2026-08-31. Week-ends are considered
  only if the monthly panel survives §6; they are not registered here.
- **Windows**, following the registered convention rather than the brief's shorthand:
  - **L (the forward label)** = the IES-90 level over **`(t, t+90]`** — `score_event(t)`.
  - **L⁻ (the pre-window level)** = the IES-90 level over **`[t−90, t−1]`** —
    `score_event(t − 91 days)`, exactly as `WALK_FORWARD_PROTOCOL.md` Amendment B.1 defines
    G-persistence.
  - Day `t` itself is in **neither** window. That is OUTCOME_MAPPING Amendment 4 clause A4.4,
    and it is why the brief's `[t, t+90]` is implemented as `(t, t+90]`: a rule that put day
    `t` in the forward window would let the grid date's own violence score its own label.
- **ΔIES** = `L − L⁻` on the ordered set {−3…+3}, per `WALK_FORWARD_PROTOCOL.md`
  Amendment J.3. A cell whose L **or** L⁻ is `no_independent_outcome` has **no ΔIES**; it is
  excluded and counted, never scored 0.

## 2. R-ACT — the "active dyad" rule (primary, registered before it is run)

A dyad `{a,b}` is **active at grid date t** when **both** hold:

1. **Oil relevance.** At least one of `a`, `b` has a registered role containing `producer`
   or `transit` in `pre1987_candidates.STATES`. Roles that are `consumer` only do not
   qualify.
2. **A recent dyadic record.** Some record in a **dyadic-capable** source — MIDI 5.0
   incidents, COW inter-state War v4.0, ICB v16, dyadic MID 4.03 — names `a` and `b` as
   co-parties (on **opposite sides** where the source records sides) with a dated spell
   intersecting the **activity window** `A_w = [t − 1825, t − 1]` — five calendar years,
   ending strictly before `t`.

GED is **not** admissible for clause 2: the cached UCDP GED 26.1 has no dyad field (the
loader is location-only, `ies90.score_ged` docstring), so it cannot say that two states
clashed with each other. This is a property of the cache, not of UCDP.

### 2.1 The selection effects, stated before the numbers

"Active" is a choice and it will drive the base rate. Four effects follow from R-ACT and are
registered here so none of them can be discovered later and presented as a surprise:

- **It is a recurrence panel, not an onset panel.** Clause 2 conditions on recorded conflict
  in the preceding five years, so a dyad that was quiet for five years and then goes to war
  is **excluded from the grid at every date before its first record**. Any skill measured on
  this panel is skill at *continuation and de-escalation*, never at *onset*. The single most
  valuable thing a forecaster could do — see a war coming in a quiet dyad — is outside what
  this panel can score, by construction.
- **The selector and the target share a data-generating process.** Clause 2 selects on the
  same four sources that produce L. A dyad enters because a source recorded it, and a source
  that records a dyad tends to record it again. This inflates persistence and **flatters the
  no-change baseline** of Amendment J.3, which is the baseline the engine must beat. Any
  ΔIES result on this panel must be read against that.
- **The base rate is not the world's.** Clause 1 restricts to oil-relevant states. The panel
  cannot speak about non-oil dyads, and its L distribution is not the interstate base rate.
- **The five-year lookback is arbitrary.** It is registered at 1825 days. The probe reports
  the active-set size at **1, 2, 5 and 10 years** as a pre-declared sensitivity. Five years
  stays the primary whatever the sensitivity shows; the others are diagnostics.

### 2.2 R-ACT-0 — the no-selection comparator (diagnostic; never replaces R-ACT)

Clause 1 alone: **every** oil-relevant dyad at **every** grid date, with no recency
condition. This is the honest base rate inside the oil universe and the only way to see how
much clause 2 moves it. It is reported beside R-ACT and does not become the rule whatever
the numbers say.

## 3. The label, and the coverage regimes the grid cannot escape

L and L⁻ come from `ies90.score_event` unchanged: max over the covering sources of the dated
level, Amendment 4's continuation rule applied, `no_independent_outcome` where every record
on the chosen basis is undated-for-the-window, and `None` where no source covers.

`ies90.covers(src, d)` requires `d + 90 ≤ hi`, so each source's **last usable grid date** is
its coverage end minus 90 days. From the `COVER` map as built:

| source | coverage ends | last usable grid date |
|---|---|---|
| COW inter-state War v4.0 | 2007-12-31 | **2007-10-02** |
| MIDI 5.0 · dyadic MID 4.03 · COW intra-state War v4.1 | 2014-12-31 | **2014-10-02** |
| ICB v16 | 2021-12-31 | **2021-10-02** |
| UCDP GED 26.1 | 2025-12-31 | **2025-10-02** |

Registered as a consequence, before it is counted: **the label's definition changes three
times across the grid.** 1987–2007 has five covering sources and a dyadic basis; 2008–2014
has four; 2015–2021 has ICB and GED only; 2022–2025 has **GED alone**, which is
location-based, not dyadic, and covers only the 49 of 59 register entities its name map
reaches; from **2025-10-02 no source covers at all.** A panel whose label is a five-source
dyadic maximum in 1995 and a one-source location count in 2023 is not measuring one thing,
and a walk-forward run across that boundary is scoring a non-stationary target. §6 reports
the covering-source mix per grid date so the size of this is visible rather than argued.

## 4. The vintage stamp — three rules, all three reported

`WORLD_STATE_CODEBOOK.md` **Amendment 1** already met this problem and ruled on it: taking
`vintage` = the dataset's release date "made every historical value invisible … Seen in the
first run and rejected as a definition error." G does not overturn session A's ruling; it
applies it, and reports the strict reading beside it because the brief asks for that number.

- **VR-2 (PRIMARY — session A's registered convention).** A cell's `vintage` is the date its
  evidence became knowable under the source's own publication convention: for an
  event-resolution record (a dispute, a crisis, a war spell, a death count), **the day after
  the record's dated spell ends**. A cell is knowable at `t` when every record its level
  rests on has `vintage ≤ t`. `release` is recorded separately on every cell (§4.1).
  Records still running at `t` have no end date to stamp — and Amendment 4's continuation
  rule already refuses to date them, so the two rules agree rather than conflict.
- **VR-1 (STRICT — the reading the brief asks about).** A cell is knowable at `t` only when
  the **dataset release** that supplies each record satisfies `release ≤ t`. Reported as a
  count, not adopted.
- **VR-3 (SELECTION knowability — new here, and the one neither VR-1 nor VR-2 covers).**
  R-ACT clause 2 must be decidable at `t` from records knowable at `t`. A dyad admitted to
  the grid on the strength of a record whose spell **ends after `t`** is a dyad selected on
  the future, and it would poison the base rate silently rather than loudly. VR-3 recomputes
  the active set admitting only records with spell end `< t`, and the probe publishes both
  sizes.

### 4.1 `release` — from the tree, not from memory

Read from the `.meta.json` sidecars beside each parsed file (`P.fetch_file`'s recorded HTTP
`Last-Modified`):

| dataset | file | release (`Last-Modified`) |
|---|---|---|
| COW inter-state War v4.0 | `Inter-StateWarData_v4.0.csv` | **2022-07-12** |
| COW intra-state War v4.1 | `Intra-StateWarData_v4.1.csv` | **2022-07-12** |
| MID 5.0 (MIDI/MIDIP) | `MID-5-Data-and-Supporting-Materials.zip` | **2022-07-11** |
| dyadic MID 4.03 | `dyadic_mid_4.03_update.zip` | **2025-04-06** |
| ICB v16 | Box shared links | **null** — the host serves no `Last-Modified` |
| UCDP GED 26.1 | `data/cache/ucdp_ged_26.1.json` | no sidecar; version string `26.1` |

Where a release date is unknown (ICB, GED), VR-1 uses a **lower bound**: the dataset cannot
have been released before its own coverage ended, so `release_lower_bound = coverage_end +
1 day`. A lower bound on the release gives an **upper bound** on VR-1 survival, so the
number VR-1 publishes is the most favourable one consistent with the evidence, and is
labelled as such. No release date is guessed.

### 4.2 `retrospective` — registered now, because it decides what the panel can ever be worth

Codebook Amendment 1: `retrospective = 1` "when the series is a later *construction* rather
than a contemporaneous record". A COW hostility level, an ICB violence code and a UCDP
best-estimate death count are all later constructions: the *incident* was contemporaneous,
the *coding* was not. **Every cell of this panel is therefore `retrospective = 1`, on every
source, at every date.** Amendment 1's own consequence follows and is registered here rather
than discovered later: "a retrospective field alone can never make a read VALIDATED." A
panel built entirely from retrospective codings can support description, ranking and
diagnosis; under the rule already on the books it cannot on its own carry a VALIDATED
verdict, however large `n` becomes. **Density does not fix that, because the problem is not
n.**

## 5. The probe — registered before it is run

The full panel is **not** built until §6 is published and read. The probe is three years of
month-ends, chosen for their **coverage regime** (§3) and not for anything about their
outcomes, which are not known to this registration:

- **1998** — primary. All five sources cover; the dyadic basis is available.
- **2018** — secondary. ICB and GED only; MID, MIDI and COW War have stopped covering.
- **2024** — secondary, a boundary check. GED alone covers, and location-only.

For each probe year the probe publishes, per grid date and pooled:
1. `|ACTIVE(t)|` under R-ACT, and under R-ACT-0, and under R-ACT at lookbacks 1/2/5/10 y;
2. the marginal distribution of **L**, of **L⁻**, and of **ΔIES**, with the share of cells
   that are `no_independent_outcome` at either end and therefore have no ΔIES;
3. **cells surviving VR-1**, **VR-2** and **VR-3**, each as a count and a share;
4. the covering-source mix per grid date.

### 5.1 The degeneracy test, fixed before the numbers are seen

The brief sets the bar: *"if it is 95 % zeros the panel is degenerate and the whole route
fails."* Registered as a decision rule, so it is not reinterpreted afterwards:

> **DEGENERATE** if, on the 1998 probe, ≥ 95 % of cells with a defined ΔIES have ΔIES = 0,
> **or** ≥ 95 % of cells with a defined L have L = 0.

If the panel is DEGENERATE the finding is published as the answer and the full panel is not
built. If it is not, §6 still gates the build on VR-1/VR-2/VR-3 and on §3's regime table,
and the recommendation is made on all four together, not on `n` alone.

## 6. Outputs

`data/grid/PROBE.json` (machine-readable, every count), `data/grid/PROBE.md` (the tables and
the verdict), `src/grid_labels.py` (the code; opens `oil.db` read-only, writes no table),
`tests/test_g_grid_labels.py`. A handoff to B is written **after** §6 is read, not before.

## 7. What this registration does not do

It does not build the full panel. It does not change `ies90.py`, `COVER`, the IES ladder, any
threshold, or OUTCOME_MAPPING. It does not touch `src/walk*.py` or `data/walk_forward/**`. It
does not admit any event. It makes no claim that a dyad-date panel is the right unit — only
that if it is built, this is how, and these are the numbers that decide.

---

## Amendment 1 (2026-09-03) — three defects in §4's VR-2 stamp, found by reading the probe's own rejections

*Dated and appended before the corrected code (charter §2 rule 4). The first probe run is superseded
by the second; both are published in `PROBE.md` so the effect is visible and not asserted. §4's
three-rule structure, VR-1, VR-3, §2's active rule, §3's regime table and §5.1's degeneracy test are
unchanged — this amendment corrects only **how a cell's VR-2 vintage is computed**, and its direction
is stated below.*

The first implementation stamped a cell from **every** record `ies90.score_event` returned, using the
**end** of each record's dated span. Decomposing the 1998 rejections showed it wrong three ways, and
all three make it **too strict** — VR-2 survival was understated, never overstated.

### A1.1 It stamped records that did not set the level, and on the wrong basis

`score_event` returns records on both the **dyadic** and the **location** basis, and applies dyadic
precedence when choosing the level (OUTCOME_MAPPING Amendment 2.1). The stamp ignored that. Example
from the run: at `t = 1998-01-31` the dyad `country.canada|country.usa` was stamped `1998-02-24`
because the United States is an actor in an ICB crisis running `1997-11-13..1998-02-23` — a crisis
that has nothing to do with Canada, on the location basis, and which did **not** set that cell's
level. Corrected: **only the records on the cell's chosen `basis` whose level equals the chosen level
(the setters) are stamped.** A level-0 cell with no setter — a covering source that looked and found
nothing (`NONE.covered`) — is stamped at the window's own close, which is what "nothing happened in
this window" becomes knowable on.

### A1.2 It dated `.onset` rules from the end of the record, not the onset

`score_mid` and `score_icb` assign level 1 under their `.onset` rules precisely because the dispute or
crisis **starts** inside the window and its peak is undated within it. The level therefore rests on
the onset and is knowable then. The stamp used the record's end. Example from the run: at
`t = 1998-01-31` the dyad `country.gbr|country.iraq` carried `MID.pair.onset 1997-11-14..2003-05-02`
and was stamped **2003-05-03** — five years late, for a level asserted by a dispute that began in
November 1997. Corrected, per rule id:

| rule | what the level rests on | stamp |
|---|---|---|
| `MID.*.onset`, `ICB.*.onset` | the dated onset inside the window | **spell start + 1 day** |
| `MID.*.wholly`, `ICB.*.wholly` | the record's peak (`hihost` / `viol`), known only when it closes | spell end + 1 day |
| `MIDI.*.overlap` | an incident, days long | spell end + 1 day |
| `WAR.inter.*`, `WAR.intra.*` | a war spell **overlapping** the window → level 3 | max(spell start, window start) + 1 day |
| `GED.location.ge25`, `ge250` | a cumulative count over the whole window | window end + 1 day |
| `NONE.covered` | a covering source with a dated view and nothing in it | window end + 1 day |
| `*.continuation` | nothing (Amendment 4 refuses to date it) | not stamped; sets no level |

### A1.3 `NONE.covered` was treated as a record

It is not a record; it is the absence of one. It is now stamped at the window close under A1.1 rather
than carried as evidence with a span.

### A1.4 What is added, not corrected

Every cell now also carries **`label_available_at` = `t + 91 days`** — the day after the forward
window `(t, t+90]` closes. This is not a filter: §4 already rules that vintage binds on the features
and the selection, never on the target. It is recorded because a walk over this grid must know when
each label can first be scored, and because it makes the one-quarter lag between a read and its score
explicit rather than implicit.

### A1.5 Direction, stated

All three corrections **raise** VR-2 survival and none can lower it. That is not a reason to trust the
new number more; it is a reason to publish both, which `PROBE.md` §4 does. **VR-1 is unaffected** —
it is decided by dataset release dates, not by which record set the level — and VR-1's count was, and
remains, the number the brief asked for.

### A1.6 The cells are published

`PROBE.json` now carries every cell (825 of them across the three probe years) with its dyad, date,
L, L⁻, ΔIES, the rules that fired, the stamp each rule produced, and the VR-1/VR-2/VR-3 decision.
A reader can take any row and check the decision against `ies90.py`'s rule ids without running
anything. Registration §6's audit obligation, met at the cell level.

---

## Amendment 2 (2026-09-03) — the evidence-basis diagnostic. Registered AFTER the first probe, gates nothing.

*Written after the corrected probe was read, and it says so. It adds a DIAGNOSTIC in the standing of
`WALK_FORWARD_PROTOCOL.md` Amendment K: published beside the registered counts, published whichever
way it comes out, and it moves no registered number and no verdict. §5.1's degeneracy test is
untouched and is decided on the registered shares alone.*

**Why it was written.** The probe's non-zero ΔIES cells turned out to concentrate on very few dyads —
in 2018, all 43 came from six pairwise combinations of the same four states. Reading two of them
against `ies90.py` showed two mechanisms that a dyad-date grid creates and an event corpus does not:

- **ICB records crisis *actors*, not sides.** `score_icb`'s dyadic test is `both members are actors
  in the same crisis`. For a corpus event that is safe, because `_actors_and_pairs` builds the pair
  from the event's coded **actor** and **target** roles. On a grid the pair is supplied mechanically,
  so **two allies in the same crisis read as a dyad in conflict with each other.** Verified: at
  `t = 2018-01-31` the dyad `country.gbr|country.usa` scores **IES level 3 on the dyadic basis** from
  `ICB.pair.wholly`, ICB crisis 489 *SYRIA CHEMICAL WEAPONS III*, `viol 4` — the United Kingdom and
  the United States, co-belligerents, recorded as at war with one another.
- **GED is a location count, replicated across every dyad containing that location.** Verified: at
  `t = 2024-03-31` the dyad `country.iran|country.uae` scores level 2 from `GED.location.ge25`, 42
  state-based deaths — deaths inside Iran, from Iran's own conflicts, with no UAE involvement. Every
  dyad containing Iran receives the same level from the same deaths.

**What the diagnostic computes.** For every cell with a non-zero ΔIES, the union of the setter rules
behind L and L⁻ is classified into exactly one of three buckets:

1. **opposed-side evidence** — at least one setter is a MID, MIDI or COW War rule, the three sources
   that record which side a state was on;
2. **ICB co-actor only** — every setter is an ICB rule, so the pair is attested only as co-actors in
   one crisis and may be allies. Sub-flagged when the pair has **never** appeared as opponents in
   MID, MIDI or COW War anywhere in the sources' whole coverage;
3. **GED location count only** — every setter is a GED rule, so the level is a death count in one or
   both countries and is not a statement about the pair at all.

Bucket 1 is the only one in which the cell is evidence about the dyad. Buckets 2 and 3 are published
as counts, not removed: removing them would be a post-hoc filter, and the point of the diagnostic is
to price the panel, not to improve it.

**Limit, stated.** Bucket 2 is a *risk* flag, not a verdict on each cell: ICB co-actors are sometimes
genuine opponents, and the diagnostic cannot tell which without a sides field ICB does not have. It
counts how much of the panel's signal rests on evidence that **cannot distinguish an ally from an
adversary**, which is the honest question, and it does not claim every such cell is wrong.

---

## Amendment 3 (2026-09-03) — the build, as Joe ruled it: 1987–2014, VR-3, evidence as a field

*Registered before the build code (charter §2 rule 2). Joe's ruling of 2026-09-03, after reading
`PROBE.md`: build the panel for **1987–2014**, on the **VR-3 active set**, with the **evidence basis
beside every result**, and the three limits registered **up front**. This amendment fixes what is
built; §§1–4 and Amendments 1–2 are unchanged and still govern the windows, the label, the stamps
and the diagnostic. Ownership is settled: session B keeps `data/grid/**`; Session G writes to
`data/grid/g/**` and `src/grid_labels.py`, and this file moved there in the same commit.*

### A3.1 The span, and the arithmetic that fixes it

Month-ends **1987-01-31 … 2014-09-30**, 333 grid dates. The end is not a preference: `ies90.covers`
requires `t + 90 ≤` the source's coverage end, MID / MIDI / COW intra-state War end 2014-12-31, and
`2014-09-30 + 90 = 2014-12-29` is the last month-end that clears it (`2014-10-31 + 90 = 2015-01-29`
does not). **The 90-day horizon costs a quarter at every source's upper edge**, and the panel ends
where its last sided source does.

### A3.2 The active set is VR-3, not R-ACT

The panel's active set is R-ACT **with the VR-3 restriction applied** (§4): a dyad enters at `t` only
on records whose spell **ends strictly before `t`**. The probe measured what this costs and what it
prevents: 39 of 335 cells in 2018 (11.6 %) were admitted on a record still running at `t`. Those are
dyads selected on the future. `n_active` under plain R-ACT is still published beside it, so the size
of the restriction is visible.

### A3.3 Evidence basis is a FIELD on every cell, never a filter

Joe's ruling: *"Carry the evidence basis as a FIELD, not a filter … then the scored study can be run
on the strict subset and the diagnostic on the full panel, without rebuilding anything."* Registered
accordingly. **No cell is ever removed from the panel by its evidence basis.** Every cell carries
three fields:

- **`L_evidence`** and **`Lpre_evidence`** — the class of what set that end's level;
- **`evidence_class`** — the **weaker** of the two, under the total order registered below.

Amendment 2 classified only the non-zero cells. That was enough to price the panel and is not enough
to build on, because a **zero** also rests on evidence and the evidence differs in kind: a zero
recorded while MID and MIDI were covering is a sided source saying *no dispute*, which is a statement
about the pair; a zero while only GED covers is *no deaths in either country*, which is not. The
classes, and their order from strongest to weakest:

| class | when it fires | is it a statement about the pair? |
|---|---|---|
| `opposed_side` | a setter is a MID / MIDI / COW War rule, **or** the cell is a true zero and a sided source was covering on the chosen basis | **yes** |
| `icb_co_actor` | every setter is an ICB rule, and the pair has been opponents in a sided source somewhere in its history | only if they were adversaries here, which ICB cannot say |
| `icb_co_actor_never_opposed` | as above, and the pair has **never** been recorded as opponents in MID / MIDI / COW War | **probably not** |
| `ged_location` | every setter is a GED rule, **or** the cell is a true zero and only GED was covering | **no** — a country-window death count |
| `undefined` | the level is `no_independent_outcome` at that end | — |

`evidence_class` is the weaker end under `opposed_side > icb_co_actor > icb_co_actor_never_opposed >
ged_location > undefined`. **The strict subset is `evidence_class == opposed_side`**, and it is a
selection B applies at scoring time, on a field that is already there.

### A3.4 The three limits, registered before the panel exists

Carried in `PANEL.json.limits`, printed at the head of `PANEL.md`, and repeated in the handoff. They
are not caveats added to a result; they are properties of the construction, known now:

1. **It never reaches the present.** The panel ends 2014-09-30 because its last sided source does. It
   cannot be the panel a live engine reads from, and no number computed on it describes the world
   after 2014.
2. **It can never carry VALIDATED.** Every cell is `retrospective = 1` (§4.2) — a COW hostility level,
   an ICB violence code and a UCDP death estimate are later constructions, not contemporaneous
   records. `WORLD_STATE_CODEBOOK.md` Amendment 1: *a retrospective field alone can never make a read
   VALIDATED.* This is a property of the sources and **`n` does not touch it.**
3. **It never scores onset.** R-ACT admits a dyad only after a recorded clash (§2.1), so a dyad quiet
   for five years that goes to war is absent from the grid at every date before its first record.
   Skill measured here is skill at **continuation and de-escalation**. The forecaster's most valuable
   act — seeing a war coming in a quiet dyad — is outside what this panel can score, by construction.

### A3.5 What is published

- `data/grid/g/PANEL.parquet` (or `.csv.gz` where pyarrow is absent) — one row per dyad-date, every
  field, the whole panel, nothing filtered.
- `data/grid/g/PANEL.json` — the marginals, the size, the limits, the evidence-class cross-tabs, the
  covering-source mix by year, and the VR-1/VR-2/VR-3 counts on the full span.
- `data/grid/g/PANEL.md` — the same for a reader, limits first.
- `data/grid/g/ICB_DYADIC_REPLICATION.md` — the finding of A3.6, written to be lifted into the paper.

### A3.6 The ICB replication finding is written up, not just applied

Joe's ruling: *"it is publishable … a concrete, checkable statement about how a standard dataset
behaves when used dyadically."* Registered as a deliverable of this build rather than a footnote:
the note names the ICB crisis id, the six dyads, the rule that fired, and the general form of the
error, and it states the scope of the claim — that this is a property of using an **actor-list**
crisis dataset dyadically, not an error in ICB, which never claimed to record sides.

The note also carries the **measured** replication count over the whole 1987–2014 panel, which the
probe could not give from three years: for every ICB crisis that sets a level on any cell, how many
distinct dyads it sets, and the distribution of that count. That number is computed by the build and
is not known to this amendment.

### A3.7 What this amendment does not do

It does not score anything, fit anything, or compute a skill. It does not filter the panel. It does
not change §5.1's degeneracy test, which was decided on the probe and stands. It does not touch
`src/walk*.py`, `data/walk_forward/**` or `data/grid/**` outside `data/grid/g/**`.
