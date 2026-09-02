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
