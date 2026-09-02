# BUILD_V2 — execution directive for the Situation Engine
Read CLAUDE.md, then NORTH_STAR.md (the purpose and the use), then
RIPPLE_ENGINE_V2_SPEC.md (the target), then this.
Supersedes UNIFIED_PLATFORM_BRIEF.md and TASK_BRIEF_PLATFORM.md. Goal:
make acceptance criteria A1–A10 in the spec TRUE, core first, depth second.
Use bound: significant developments, horizons of weeks to quarters; no
intraday data, no trading signals, no entries/exits anywhere in the build.
One commit per slice; acceptance green after every phase; STOP at Joe-
gates; publish every result as computed. Timeline target: core (B1–B5)
in days; depth (B6) immediately after.

## B0 — Register before building (½ day)
- Codebook amendment (committed BEFORE any coding): the Situation Record
  fields (spec §4.1) with written per-field criteria and the rule
  "sourced or unknown; never from outcomes." Scenario taxonomy (spec
  §4.2) and outcome-observation rule (+30/+90 days, sourced).
- Pre-register the walk-forward protocol (spec §5): windows, scores,
  baseline, promotion rule. Commit. JOE-GATE: field definitions — Joe
  approves/edits, then proceed.

## B1 — Situation records for the existing corpus (A1) (1–2 days)
- Schema: add physical + geopolitical blocks to `events` (nullable,
  "unknown" default) + a per-field source column.
- Caged extractor codes every corpus event from its sources; anything
  not supported by a source stays "unknown." Outcome branch observed
  from sources at +30/+90d for every event.
- Actor response propensity computed from the corpus (per actor: share
  of situations that escalated), not hand-coded.
- JOE-GATE: borderline codings queue (extractor confidence < threshold).
  Blanket approval permitted with a 20-event spot audit recorded.

## B1.5 — Big Moves, market-defined significance (A11) (1 day; parallel with B1)
- Register thresholds FIRST (commit before computing): top 5% of 20/60-
  day moves per asset, curve-flip rule, vol-regime-break rule, product-
  spread rule, flow-drop rule; window for attribution (event knowable
  within −5..+20d of episode start).
- `src/big_moves.py`: detect episodes per asset (1987+ daily; 1970+
  monthly where series exist), attribute to corpus events or mark NO
  IDENTIFIED EVENT, compute P(big move | class) and P(class | big move)
  with n → data/big_moves.json. Publish as computed.
- Rebase `src/materiality.py` (B4) on P(big move | class) vs the everyday
  base rate. The "what has ever changed this market" table becomes the
  Big Moves page (B4).
- JOE-GATE: read the attribution list; anything he can source that the
  extractor missed goes through the normal admission gates, not by hand.

## B2 — Layer G, the Escalation Model (A2, A3) (1 day)
- `src/situation.py`: similarity metric over the geopolitical block
  (documented, weights = uniform priors, displayed); retrieval of top-k
  analogs; "no adequate precedent" when max similarity < threshold or
  conditioned n < 8 (unit-tested both ways); branch base rates from the
  conditioned subset with n; hierarchical fallback with flag.
- Likeness/difference table generator: field-by-field then-vs-now,
  each difference tagged with the branch it shifts and evidence status
  ("measured: subset rate, n" or "judgment, unmeasured").

## B3 — Layer P, propagation per branch (A4) (½–1 day)
- `src/propagate.py`: given a branch, walk the ripple graph from the
  hit asset's physical channel; at each hop the measured edge (existing
  cross_asset/edges), PRICE and FLOW separately, n and range shown.
  The "realized disruption fraction" for the analog set is computed and
  shown (the conflict-doesn't-stop-trade number).

## B3.5 — The Claim Ledger (A9) (1 day)
- Register (commit BEFORE coding) the claim schema: checkable = asset +
  direction/magnitude/flow/escalation + horizon; horizons +20/+60 trading
  days, +30/+90 calendar days for escalation; resolution rules from data
  only; verdict scale SUPPORTED / MIXED / UNSUPPORTED / THIN (n<8) / NO
  PRECEDENT / UNCHECKABLE.
- Upgrade `src/deconstruct.py`: type each extracted claim (verbatim,
  extractive), attach horizon, map to its reference class (hierarchical
  fallback with flag), emit the verdict with the frequency and n.
- `src/ledger.py`: append-only log of every claim read (point-in-time
  stamp, source, verdict, reference class); scheduled resolver at
  horizon; scoreboards: engine vs base rate, record vs narrative, per-
  source and per-claim-type with n. Nothing hand-resolved, ever.
- Corpus-article pilot: claim-extract the `source_url` article of each
  corpus event (fetch; if unreachable, "unavailable" — never substitute),
  resolve against measured CARs → publish record-vs-narrative with N.
  JOE-GATE: read the pilot number and its 10 worst disagreements before
  it goes on any surface.

## B4 — Feed and Story Page (A2–A4, A10 surfaced) (1–1½ days)
- Materiality gate (`src/materiality.py`): MATERIAL / IN LINE / NOISE per
  story from the class-CI-vs-baseline-CI test + situation-taxonomy match.
  NOISE shelved, visible, unranked.
- Attention series for LOUD/QUIET and QUIET/LOUD flags: GDELT counts and
  pageviews already in the reference tier; document the threshold.
- FEED: market-state strip (each asset vs its 50-year distribution;
  analog regimes), then material stories ranked by narrative-vs-record
  gap, flags, one-line record read; NOISE shelf collapsed.
- BIG MOVES page: 50-year timeline per asset from data/big_moves.json,
  filter by asset/move type, click → event → analogs.
- The Record bar: one shared component (outcome distribution after
  analogs, dated tails as ticks) used wherever a frequency appears.
- STORY PAGE (replaces the Desk's card): significance and why →
  is it priced (since-knowable vs analog paths, premium vs realized) →
  claim verdicts → branch table → propagation per branch → trust stamp
  (engine class score placeholder until B5 + source record from the
  Ledger) → Notes & Draft → export. Also the paste/URL door. Trace shows
  the same object in depth. LEDGER page: the three scoreboards.

## B5 — The walk-forward backbone (A5) (1–2 days)
- `src/walk_forward.py`: point-in-time replay per the registered
  protocol; two windows; G-score (Brier over branches) and P-score
  (magnitude/sign error given realized branch); baseline = unconditioned
  class rate; outputs data/walk_forward/ with per-situation logs;
  Backtest console shows both windows; every Desk card stamped with its
  class score. Promotion rule enforced in code: conditioners stay
  SUGGESTIVE unless they beat baseline OOS in both windows.
- Wire to the scheduler (quarterly re-score) and to acceptance.

## B6 — Deep history tier (A8) (1–2 days, may run in parallel after B1)
- Extend Layer G's corpus to 1970 with events only: sweep Hamilton
  (NBER w16790), EIA chronology, and one policy timeline; caged
  extractor proposes; two-source rule; Joe-gated. Target ≥60 sourced
  events 1970–1989 with situation records and observed outcomes.
  Price-layer analyses remain 1987+; the engine labels pre-1987 analogs
  "escalation precedent only (no price data)."

## B7 — Continuous intake (A6) (½ day)
- Watcher as a 15-minute launchd agent; each intake decomposed (asset →
  outputs → chain) and passed through B2–B4 inline; Desk feed always
  fresh. Install; document; verify one autonomous cycle end to end.

## B8 — Close (A7)
- Acceptance extended to check A1–A10 explicitly (`acceptance.py`
  prints each). Regenerate docs (STATE_OF_THE_ENGINE, README,
  DATA_DICTIONARY). Tag v2.0. Report a one-page status against A1–A10.

## Hard bounds
$0/keyless; sourced-or-unknown (never fabricate a field); no occurrence
probabilities (historical frequencies only); frozen registered records
untouched; every promotion earns it through B5; all Joe-gates honored;
every displayed number one hop from its receipt.
