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
