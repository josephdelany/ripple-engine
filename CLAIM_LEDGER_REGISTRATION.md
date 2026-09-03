# MATERIALITY GATE + CLAIM LEDGER — registered definitions (before computing)
*2026-09-02. Fixes the rules for "significant," for what counts as a checkable
claim, for the verdict scale, and for resolution — so none of them are tuned
after seeing what stories say. Amendments are dated and appended, never edited.*

## 1. Materiality gate (A10)
Input: `data/big_moves/summary.json` (Amendment 2 of BIG_MOVES_REGISTRATION.md).
For a story's decomposed event class c and an asset a:
- rate(c, a) = P(big move | c) for that asset; base(a) = the everyday rate
  (share of trading days inside any big-move window).
- ratio(c, a) = rate / base.
- Significance uses crude (Brent) and the product side (diesel crack) together:
  **MATERIAL** if max(ratio on Brent, ratio on diesel crack) ≥ 1.2 and the class
  has n ≥ 8 events; **IN LINE** if 0.8 ≤ max ratio < 1.2; **NOISE** if max ratio
  < 0.8, or the story maps to no event class. Thin classes (n < 8) are IN LINE
  with a "thin" flag, never MATERIAL.
- `policy_response` is endogenous by construction and is capped at IN LINE with
  an "endogenous" flag regardless of its ratio.
- Attention: LOUD/QUIET = attention in the top 20% (Wikipedia pageviews ≥ 2×
  trailing median for a matched page, or GPR daily percentile ≥ 80) while
  significance is not MATERIAL. QUIET/LOUD = MATERIAL while attention is in
  the bottom 40% (no matched page spiking and GPR percentile ≤ 40). Attention
  is context, never a statistic.

## 2. Checkable claims (A9)
A sentence extracted verbatim by `deconstruct.py` is CHECKABLE only if it
resolves to all three of: an asset (crude, product crack, gas/LNG, fertilizer,
freight — or an escalation between named actors), a direction or a level, and a
horizon. Defaults when the sentence gives none: horizon +20 trading days for
price claims, +90 calendar days for escalation claims. Everything else is
UNCHECKABLE and is displayed, not dropped.
Claim types: `direction` (up/down), `level` ("past $110"), `flow` (barrels or
transits stop/resume), `escalation` (retaliation, widening, closure), `policy`
(OPEC/SPR action). Hypotheticals ("could", "if") are read "if it occurs" and
are logged with modality=hypothetical; they resolve only if the antecedent
event enters the corpus.

## 3. Verdicts (about the record, not truth)
Reference class = the story's event class, price side measured on Brent from
the corpus (1987+), n stated. For a direction claim "up": r = share of class
events with Brent higher at +20 trading days. For "down": share lower.
- **SUPPORTED** r ≥ 0.60 and n ≥ 8 · **MIXED** 0.40 < r < 0.60 · **UNSUPPORTED**
  r ≤ 0.40 · **THIN** n < 8 · **NO PRECEDENT** class absent from the corpus ·
  **UNCHECKABLE** per §2.
- Level claims: r = share of class events whose +20d move reached the implied
  % distance from the price at knowability. Same cut-offs.
- Escalation claims: r = share of the conditioned subset (Layer G, or parent
  class with a "thin" flag) whose +90d outcome was LIMITED_RETALIATION or
  WIDENING; outcomes are corpus-derived and labelled as such.
- Flow claims: r = share of class events with a material sustained Brent move
  (≥10% |CAR20|) — the realized-disruption fraction from `propagate.py` —
  until flow history exists; labelled "price proxy for flow."
- Policy claims: checkable only against a dated action; resolve when the
  action enters the corpus. Until then PENDING.

## 4. Resolution (never by hand)
Every checkable claim is appended to `data/ledger/claims.jsonl` at read time
with the knowable date and its verdict. At horizon, the resolver computes the
realized outcome from the series (price/level) or from subsequent corpus events
(escalation, policy) and marks claim_true and record_true. A claim's truth is
its direction/level being realized; the record's truth is its verdict's
implied direction matching the realization (MIXED counts as no call).
Scoreboards: record vs narrative (share of resolved claims where exactly one
of the two was right and it was the record); sources (claim_true rate per
source and claim type); engine vs base rate (from `data/walk_forward/`).
Nothing in the ledger is edited after it is written; corrections are new rows.

## Amendment 1 — 2026-09-02, after the first gate run (disclosed)
As registered, every geopolitical class clears MATERIAL — on the product side
(diesel crack ratios 1.8–2.6×), while on crude most sit at or below the everyday
rate (infrastructure attack 0.6×, chokepoint 0.8×, sanctions 0.8×). That is a
finding, not a bug: geopolitics moves products more than crude. The thresholds
stay as registered. Two display rules are added, not tuned: (i) significance is
shown per side — crude chip and product chip — with the overall chip = the
registered max; (ii) the Feed ranks MATERIAL stories by ratio, so the gate
orders as well as admits. Entity-level refinement (which asset, what volume)
is future work and is not applied to today's gate.

## Amendment 2 — 2026-09-02, after the first Feed run (disclosed)
The keyword classifier admits "US-Canada trade war" as conflict_escalation, so
class-level MATERIAL lets in stories with no petro entity. Display rule added
(not a threshold change): a story is shown MATERIAL only if the gate says
MATERIAL *and* the headline matches at least one entity the engine tracks
(country, chokepoint, commodity, company); otherwise it is shown IN LINE with
the flag `no_entity`. Ranking: gate ratio, then number of matched entities,
then headline-vs-record gap, then recency.

## Amendment 3 — 2026-09-02, before the reading layer is rebuilt (registered first, computed after)
The regex reading layer (`triage.classify_type`, `deconstruct.claims`) is replaced
on the v2 surfaces (Story, Feed) by a **caged LLM reader** (`src/reader.py`), on the
same pattern as `extract_events.py` / `apply_situation_agent.py`: the model
proposes, deterministic Python decides what is allowed in, nothing partial is
repaired. The model is Claude via the local `claude` CLI on Joe's subscription
(keyless, $0 marginal); it runs with no tools and a fixed output schema. Rules
the cage enforces, fixed here before the first run:
1. **Event class** ∈ the seven registered types or `null`. Anything else → `null`
   (NOISE), with the rejection recorded on the read.
2. **Entities** must be `entity_id`s in the `entities` table, each with one role
   from {actor, target, asset, chokepoint, location, affected_market, mention}.
   Unknown names are kept as `unmapped` text; they carry no id and never count.
3. **Claims are verbatim.** A claim's quote must be a substring of the article
   text (whitespace- and quote-mark-normalised). A quote that is not in the text
   is a fabrication and the claim is dropped, with the reason recorded. Kind ∈
   {direction, level, flow, escalation, policy, uncheckable} per §2; asset ∈
   {brent, diesel_crack, gas, fertilizer, freight} or `null`; a level's number
   must appear in the quote; horizons are assigned by the cage from §2 (+20
   trading days for price claims, +90 calendar days for escalation and policy),
   never by the model, unless the quote itself states a horizon. A direction or
   level claim with no asset, or an escalation claim with no actor/target entity
   in the story, is downgraded to UNCHECKABLE — the cage never upgrades.
4. **Titles are extracted, not generated.** For a URL the title is the page's
   own (og:title, h1, or <title>, minus the site suffix); for pasted text it is
   the first sentence. The model proposes no title.
5. **Entity-aware gate (replaces Amendment 2's headline-keyword rule).** A story
   is shown MATERIAL only if the class gate says MATERIAL *and* the reader found
   at least one **tracked petro entity in an actor, target, asset or chokepoint
   role**. Tracked petro entity = an `entities` row of type country, chokepoint
   or supplychain; a petro commodity (brent, wti, crude_oil, diesel, gasoline,
   gasoline_spot, natgas, eu_gas, lng_asia, propane, fertilizer, petchem); or one
   of institution.{opec, iea, us_doe, isprl, china_reserve_bureau}. Otherwise the
   story is shown IN LINE with the flag `no_entity`. A location-only or
   mention-only entity does not qualify. Thresholds in §1 are unchanged.
6. **Fallback is labelled.** If the CLI is unavailable (logged out, timeout,
   malformed output) the read falls back to the regex layer and every surface
   carries `reader: regex_fallback`; a fallback read is never presented as a
   model read. Model reads are cached by content hash so a story is read once.
7. **The Feed reads headlines only** (batched, ≤40 per call); the full article is
   read on its Story page. Ranking stays: gate ratio, then number of qualifying
   entities, then headline-vs-record gap, then recency.
Nothing already in the ledger is edited; claims logged under the regex layer
keep `registration: CLAIM_LEDGER_REGISTRATION.md` and predate this amendment
by timestamp.

## Amendment 4 — 2026-09-02, before the Challenge loop is built (registered first, computed after)
The Story page gains a **Challenge** panel under the branches: the analyst conditions
the situation record and the engine re-reads the escalation layer under those
conditions. Rules fixed before the first run:
1. **Conditions are coded fields only:** actor, target, conflict_scope, tempo,
   alliance, diplomatic, target_capacity. A value must belong to the coded vocabulary
   (SITUATION_CODEBOOK_V2.md enums, plus the ids actually coded in the corpus for
   actor/target). Any other value is refused, the refusal is logged, nothing runs.
   Free text is logged verbatim and is never parsed into a condition.
2. **Same engine, same thresholds.** The conditioned read is `escalation.read` on the
   story's own situation record with the chosen fields overridden — identical
   similarity, uniform weights, RETRIEVE_MIN 0.40, COND_SIM 0.50, COND_MIN_N 8. A
   challenge cannot tune any of them.
3. **Two first-class states.** No analog at or above RETRIEVE_MIN → **NO PRECEDENT**
   (no counts, no rates). Conditioned subset below 8 → **THIN**: the subset's own
   counts are shown with n and are not a call; branch rates fall back to the parent
   class as they do on the page.
4. **Price side from the same subset.** Brent +20 trading days for exactly the subset's
   event ids (via `ledger.class_outcomes`, filtered), point-in-time for corpus
   events: n, median, IQR, share up, dated tails. The comparison row sets this beside
   the unconditioned read. Frequencies with n; never a probability.
5. **Field coverage is shown.** For every conditioned field the panel states how many
   corpus records carry a coded value (today: alliance, diplomatic and
   target_capacity are coded in 0 of 187 geopolitical records, so a condition on them
   cannot change the subset; the panel says `field_uncoded` rather than pretending).
6. **Append-only log.** Every challenge — including refused ones — is appended to
   `data/ledger/challenges.jsonl` with story id, knowable date, conditions and free
   text verbatim, the resulting state, n and counts. Nothing is edited after writing.
7. The paste box moves under a "Read something the feeds missed" label on the Feed;
   the Feed is the front door.

## Amendment 5 — 2026-09-02, before the code (Brief A-13): "what the market already knew" — display fields, never scored
The Story page's section 1 shows, AS OF THE KNOWABLE DATE and with vintage ≤ knowable, four priced-in inputs. They
are display fields: they enter no claim verdict, no gate, no walk score, no Hedge weight.
| field | series (held now) | rule at knowable k | before the series starts |
|---|---|---|---|
| curve front spread (M1−M4, $/bbl) | `state_panel` `curve_m1_m4_spread` (EIA NYMEX RCLC1..RCLC4, daily, ends 2024-04-05) | last value with vintage ≤ k | `unknown` |
| 1–3 curve slope | not held (session C's NYMEX loader; handoff `data/handoffs/C_to_A_*.md` absent on 2026-09-02) | `unknown` until the loader lands | `unknown` |
| OVX percentile (2007→) | `fred.OVXCLS` | percentile of the last print dated ≤ k − 3 d (FRED lag) among all prints ≤ that date | `unknown` |
| managed-money net length percentile (COT) | `cftc.mm_net_wti` (2006→) | percentile of the last report dated ≤ k − 3 d (CFTC Friday release) among all reports ≤ that date | `unknown` |
Each value carries `as_of`, `vintage`, `n`, and the series id. When session C's OVX / COT / curve loaders land, the
same fields read from those loaders' rows; the rule does not change.

## Amendment 6 — 2026-09-02, before the code (Brief A-15, red-team finding B7): the reader states a date and a confidence
Finding B7 (docs/red_team_2.md): the reader emits no event date and no confidence, so every headline date downstream
is the capture timestamp. Amended, before the cage changes:
1. The reader's schema gains `event_date` (ISO `YYYY-MM-DD`, or `null` when the text states no date — never the capture
   date, never today) and `confidence` (`high` / `medium` / `low`) for the class call, on both the story and the headline
   paths. Both are extracted, never inferred from outside the text; the regex fallback always returns `event_date: null`,
   `confidence: "fallback"`.
2. Downstream, a `null` event_date keeps the existing capture-timestamp behaviour but the item says `date_basis:
   capture`; a stated date is shown with `date_basis: text`. Nothing in the gate, the ledger verdicts or the walk reads
   `confidence`; it is display and evaluation only (src/reader_eval.py scores date exactness where a date is returned).

## Amendment 7 — 2026-09-02, session H, BEFORE the historical backfill is run (registered first, computed after)
The ledger has 14 claims, 0 resolutions, and every claim carries `knowable = 2026-09-02`: the
core mechanic of §4 — a claim resolving itself from data at its horizon — has never fired end to
end, because nothing in the ledger is old enough to have a horizon in the past. This amendment
fixes, before anything is read, how historical stories enter the ledger, so the first scoreboard
cannot be the product of choosing convenient stories after seeing how they resolve.

1. **Selection is mechanical, not chosen.** The backfill set is *every* row of the `events` table
   with `event_date` in **2019-01-01 .. 2020-12-31** and `type` in {`infrastructure_attack`,
   `chokepoint_disruption`, `opec_decision`, `conflict_escalation`} that carries an `http(s)`
   `source_url` — **n = 19 events, fixed here before the first fetch**. Stories are not picked
   individually; Abqaiq 2019, the March 2020 OPEC+ collapse and the 2019 Hormuz seizures fall
   inside the rule rather than being named by it. The window is chosen so that every horizon
   (+20 trading days, +90 calendar days) closed years before the Brent series ends (2026-08-25).
2. **Text is fetched, never supplied.** Each `source_url` is fetched **once** with
   `reader.fetch`, the raw page is archived under `data/ledger/backfill_pages/<event_id>.html` so
   the read is auditable against the exact bytes that produced it, and the body and title are
   `reader.body_from_html` / `reader.title_from_html` of that archived copy — the same
   deterministic parsers `reader.prepare(url)` uses, on one fetch instead of two. A fetch failure, a paywall or a body under 120 characters
   **drops the story and records the drop with its error**. No pasted substitute, no summary
   standing in for an article, nothing written by a model or by a session. A dropped story is
   reported in the denominator.
3. **The knowable date is extracted, never assigned.** In order: (a) `article:published_time` /
   `datePublished` / `og:article:published_time` in the page; (b) a `<time datetime="YYYY-MM-DD…">`
   element; (c) a dateline element — an element whose class is `date`, `published` or `pubdate`
   carrying `Month D, YYYY`; (d) a `/YYYY/MM/DD/` or `/YYYY/M/D/` path in the URL; (e) an explicit
   `Published On <d Mon YYYY>` line in the parsed body. If none of the five yields a date, **the
   story is dropped** — it is never backdated to the corpus
   `event_date` and never stamped with today. `knowable_basis` (`meta` / `url_path` / `body`)
   is recorded on every surviving row. The article date, not the event date, is the knowable
   date: a story published after the event it describes was knowable when it was published.
4. **The reader gets no class hint.** `reader.read_story(url)` is called exactly as a live URL read
   calls it, with no `class_hint`: a live read has no corpus id and must classify for itself. The
   reader's own `event_class` is the reference class for every verdict. The corpus's coded class is
   recorded beside it and reader-vs-corpus agreement is published as a **diagnostic that gates
   nothing**.
5. **`price_at_knowable`** is Brent (`fred.DCOILBRENTEU`) at the first trading day on or after the
   knowable date — the same index rule `ledger.resolve` uses, so the logged price and the resolved
   path start on the same bar. *Disclosed limitation:* intraday timing is not modelled, so a story
   published in the morning is scored against that day's close.
6. **Verdicts are point-in-time.** `ledger.verdict_for(..., as_of=knowable)`: the reference class
   contains only corpus events dated strictly before the knowable date. This is **stricter than the
   live Story page**, which passes `as_of=None` on a URL read (defect S-1 below).
7. **Resolution is untouched.** `ledger.resolve` runs as written. Nothing is hand-resolved, no row
   is edited, corrections are new rows. The scoreboard is published with n whichever way it comes
   out, including if it shows the record was wrong, or if n is too small to say anything — a null
   is a result (§4, charter §2 rule 4).
8. **No verdict rule, threshold or cut-off in §2–§4 is changed by this amendment.** If the
   uncheckable share stays high, that is reported as a finding about the reader or the sources; it
   is never improved by loosening §2.

### Defects recorded before the run (found by reading the code, fixed or handed off, never worked around)
- **L-1 — `ledger.log_claims` drops `entities`.** The reader emits `entities` on every claim
  (`reader.to_ledger_claim`) and `ledger.resolve` reads `c.get("entities")` to restrict an
  escalation claim's +90d corpus window to the actors named in the story — but `log_claims` never
  writes the field, so `entities` is always empty at resolution and **every escalation claim
  resolves against every conflict/attack/chokepoint event anywhere in the world**, which is close
  to always true. Fix (session H, `src/ledger.py`, additive: a new field on new rows, existing rows
  untouched, append-only preserved) plus a regression test naming the defect. This is a resolver
  defect the backfill was built to find; it is fixed, not routed around.
- **S-1 — `story_read.read` is point-in-time for the fan and not for the verdict.** Inside one
  function, `priced()` filters analogs to those knowable before k, while `verdict_for` and
  `branches` are passed `as_of=str(k.date()) if eid else None` — so a **URL** story gets a
  reference class containing events from the future of its own knowable date. Harmless while every
  URL read is dated today; wrong the moment one is not. `src/story_read.py` is session A's file:
  this is handed off in `data/handoffs/H_to_A_2026-09-02_pit_verdict.md`, not patched here, and the
  backfill passes `as_of=knowable` itself (rule 6) so nothing session H logs carries the leak.

### Disclosure — methods (b) and (c) were added after the first extraction pass, before any claim was logged
The extractor was written with methods (a), (d) and (e) only, before a single page was fetched. On
the 16 pages that fetched, it returned no date for 5 of them, so the registered rule would have
dropped Abqaiq 2019 — one of the three stories this backfill exists to test. Rather than
hand-date that page, two further methods were added and **applied uniformly to all 16 pages**:
`<time datetime=…>` and a dateline element (`class="date"` and kin). Both are structural — an
element whose job on the page is to carry the publication date — and source-agnostic; neither
names a site or a story. They recover 4 pages: `ecuador_leaves_opec_2019` (a `<time>` element) and
the two EIA *Today in Energy* articles, whose own datelines read **2019-09-23** for Abqaiq (nine
days after the attack) and **2020-09-23** for the OPEC+ record cut (five months after it) — later
than the events, which is exactly right and is why the article date, not the event date, is the
knowable date. The two pages that still carry no dateline element (`saudi_ew_pipeline_2019`,
`gulf_of_oman_tanker_attacks_2019`, both globalsecurity.org reprints) **stay dropped**: no bespoke
per-page pattern was written to rescue them. What this change moves is *which stories are read*,
never a verdict rule, a threshold or a cut-off — §2–§4 are untouched, and the drops are reported
in the denominator.

### The set that survives the registered rule
19 selected → 3 dropped on fetch (HTTP 403: mining.com, tj.usembassy.gov, timesofisrael.com; the
registered rule refuses to retry under a disguised user-agent) → 2 dropped for no extractable
publication date → **14 stories read**. Every drop is listed with its reason in
`data/ledger/backfill_manifest.json`.

## Amendment 8 — 2026-09-03, session H, AFTER the backfill (disclosed, not registered first)

Four things found while writing the tests that H-1..H-4 should have shipped with. All four are
disclosures or additive fields; none changes a verdict rule, a threshold or a published ratio.
Recorded here rather than in a commit message so they cannot be lost (charter §4.5).

### (a) `pending` is split into `awaiting_horizon` and `never_resolves` — defect L-2
`resolve()` skips `modality = hypothetical` permanently, but `scoreboards()["counts"]["pending"]`
counted those claims as pending anyway, so a surface reading it promised twelve resolutions that are
never coming. Found by session A while building the Ledger screen
(`data/handoffs/A_to_H_2026-09-03_pending_count.md`) and independently by session H's own recount;
answered in `data/handoffs/H_to_A_2026-09-03_pending_split.md`. `counts` now also carries
`awaiting_horizon` (1), `never_resolves` (12) and `never_resolves_reason`. `pending` (13) is kept
and is exactly the sum. **The underlying defect L-2 remains open**: §2 says a hypothetical claim
resolves if its antecedent enters the corpus, and no mechanism does that. Building one is a future
amendment; naming the 12 honestly is not a substitute for it.

### (b) The blind sheet is only PARTLY blind — the id slugs telegraph some classes
`data/reader_eval/blind_sheet_30.md` prints the gold's own id beside each headline, and 9 of the 30
ids contain a token of their own class (`russia_sectoral_sanctions_2014` → `sanctions`; every
`opec_*` → `opec_decision`). Those rows can be coded without reading the headline, and agreement on
them is 9/9 against 17/21 on the rest. The published kappa is therefore inflated by construction.
Not corrected — re-drawing the sheet after seeing the answers is exactly what the registered seed
exists to prevent (Amendment 3). Instead `audit_reader.kappa_report()` now computes and publishes
`blindness_caveat` in `data/reader_eval/kappa_coders.json`, giving the honest lower bound on the 21
rows that do not telegraph:

| pair | headline kappa (n=30) | excluding telegraphed (n=21) |
|---|---|---|
| A vs H | 0.8307 | **0.7383** |
| reader vs A | 0.7945 | **0.6948** |
| reader vs H | 0.8370 | **0.7586** |

All three stay above the 0.6 bar, so no conclusion changes; the number to quote is the right-hand
column. This does not touch the "UNAUDITED" label, which only Joe's own coding can retire.

### (c) A stored claim's `checkable` flag is NOT reproducible from `ledger.type_claim()`
On the LLM path, `reader.read_story()` takes the model's proposed `kind`/`checkable` and passes it
through `reader.cage_claim()`, which validates against the source text and can only downgrade or
reject — it never upgrades or repairs. `ledger.type_claim()` is used only on the labelled regex
fallback. So re-typing a stored sentence reproduces its stored flag for 61 of 112 claims and not the
other 48 (3 lack the fields to try), and **the uncheckable ratio in `uncheckable_audit.json` cannot
be recomputed offline from `type_claim` alone**. This is the design working as intended, not a
defect, but it was nowhere written down, and anyone re-deriving the H-3 ratio the obvious way would
get a different number and reasonably conclude the audit was wrong. Pinned by
`tests/test_uncheckable_audit.py::test_H2_stored_typing_is_the_caged_reader_not_a_fresh_regex`, which
fails if either typing drifts. What *is* reproducible offline, and is now checked on every run, is
the fabrication guard: all 98 backfill quotes appear verbatim in their committed page receipts.

### (d) Defect L-1's fix is demonstrated by a failing test, and moved no number
The charter permits H to fix a resolver defect in shared `src/ledger.py` only where it can be
demonstrated with a failing test. `tests/test_ledger_backfill.py::test_L1_log_claims_persists_entities`
is that test; it was run against a scratch copy of the pre-fix `ledger.py` and fails there
("log_claims dropped the entities field"), and passes after. Separately, and importantly for INV-6:
on the committed data the defect would have inflated the escalation corpus counts (2→8, 1→3) but
**flipped zero verdicts**, because `claim_true` is `count > 0` and the one zero is zero either way.
The escalation true-rate of 5/6 is therefore not a product of this fix, and must not be read as one.
Asserted in `::test_L1_entity_restriction_narrows_the_window_but_moved_no_verdict`.

## Amendment 9 — 2026-09-03, session H, BEFORE the antecedent gate is built (registered first, computed after)

Closes defect L-2 as a *mechanism*. §2 says a hypothetical claim "resolves only if the antecedent
event enters the corpus" and no code ever tested that, so `resolve()` skipped `modality=hypothetical`
outright and twelve checkable claims sat in `pending` for ever. This registers the test. It is
written before a single hypothetical claim is resolved, and it is deliberately built to REFUSE more
often than it answers, for the reason in §9.4.

### 9.1 What an antecedent is, and the registered markers
A hypothetical claim has an antecedent only if its verbatim text contains one of the registered
conditional markers, which introduce a proposition on which the consequent depends:

    if · should · unless · were to · in the event that · provided that · so long as ·
    as long as · whenever

A bare modal or hedge — `could`, `would`, `may`, `might`, `risks`, `expects`, `threatens`,
`potentially`, `possibly` — is **not** an antecedent. It is a hedge on an unconditional
proposition. A claim carrying only a hedge has no antecedent to enter the corpus, so §2's mechanism
does not reach it and never will; it is closed as `NO_ANTECEDENT`, not left pending.
The antecedent clause is the text from the marker to the end of the sentence or the next clause
boundary, taken verbatim. It is never paraphrased and never supplied by a model.

### 9.2 The antecedent predicate, derived mechanically
The predicate is read out of the antecedent clause by rule, never coded by hand (charter §2.3
forbids hand resolution). Exactly two predicates are registered:

- **PRICE** — the clause states a level (`ledger.LEVEL`). Predicate: the claim's series touches
  that level, in the direction the clause states, at or before the claim's horizon. Testable
  whenever the series covers the window.
- **CORPUS** — the clause names at least one country entity. Predicate: a corpus event of
  `conflict_escalation`, `infrastructure_attack` or `chokepoint_disruption`, with `sr_actor` equal
  to that entity, dated in `(knowable, knowable + horizon]`.

A clause matching neither — most often because its subject is a pronoun ("if **it** does anything"),
a mass noun ("if **the aggression** continues") or an unnamed situation ("if **the situation** was
not quickly resolved") — yields no predicate.

### 9.3 The four outcomes. Only one of them resolves anything.
Every hypothetical claim gets exactly one status, appended to `data/ledger/antecedents.jsonl`
(append-only, one row per claim per run, never edited):

| status | meaning | effect |
|---|---|---|
| `NO_ANTECEDENT` | no registered marker: a hedge, not a conditional | closed for ever; a reader typing defect, handed to A |
| `ANTECEDENT_UNTESTABLE` | has a marker, but no PRICE or CORPUS predicate can be derived, or the field needed is not coded on the events in the window | **REFUSED**; nothing resolved, the reason published |
| `ANTECEDENT_NOT_MET` | predicate derived and tested; the antecedent did not occur in the window | **VOID** — see §9.5 |
| `ANTECEDENT_MET` | predicate derived and satisfied | the claim's consequent is resolved by the normal `resolve()` path for its kind, and only then |

`ledger.resolve()`'s skip of `modality=hypothetical` is lifted for, and only for, claims recorded
`ANTECEDENT_MET`. Every other hypothetical claim stays unresolved, as now.

### 9.4 Why this refuses so much, on purpose
`sr_actor` is coded on **65 of 187** geopolitical records (35%). If a CORPUS predicate were tested
against that field naively, a claim would be marked `ANTECEDENT_NOT_MET` whenever the qualifying
event exists but its actor is blank — and the published verdict would be a missing-data artefact
wearing the clothes of a substantive finding. So the CORPUS predicate is testable **only if at
least one event in the claim's own window carries a coded `sr_actor`**; where the window's events
are entirely unlabelled, the status is `ANTECEDENT_UNTESTABLE` and nothing is published. A refusal
is the correct output of a missing field. This is the same discipline as the Challenge loop
(Amendment 4) and the same reason.

### 9.5 A VOID claim is not evidence about the record
A conditional whose antecedent never occurred has not been shown right and has not been shown
wrong: "if Iran attacks, prices spike" is not refuted by Iran not attacking. `ANTECEDENT_NOT_MET`
claims are therefore **excluded from every scoreboard** — from `record_vs_narrative`, from the
per-kind rates and from the story votes — and are reported as their own count with the reason.
Counting them either way would be a base-rate error, and counting them as false would flatter the
record. They never enter `resolutions.jsonl`.

### 9.6 What this does NOT do
It does not parse the consequent, it does not decide whether the antecedent is *the same*
proposition the sentence conditions on beyond the entity/level test above, and it cannot rescue a
claim the reader mis-typed. It is expected to resolve very few of the twelve — possibly none — and
that null is the published result, not a reason to loosen the predicate. Widening the marker list
or the predicate set after seeing which claims resolve is forbidden; any change is a new dated
amendment stating what it does to the counts.

### 9.7 Files
`src/antecedent.py` (new, session H), `data/ledger/antecedents.jsonl` (new, append-only),
`tests/test_antecedent.py`. `src/ledger.py` gains the gated skip only.
