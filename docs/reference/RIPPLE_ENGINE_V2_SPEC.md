> **REFERENCE — SPECIFICATION, NOT A RESULT.** A specification or codebook for the legacy engine's data and rules. It claims no finding; the authoritative result is in [`PAPER.md`](../PAPER.md).

# RIPPLE ENGINE v2 — Concept and Technical Plan of Operation
*The situation engine for the oil economy. Written 2026-09-01 for a
technical evaluator. Every claim here is either built, specified with an
acceptance test, or labeled as future.*

## 1. Purpose
*Governed by NORTH_STAR.md: how a financier reads the news about the petro
economy — every story read against the record and the live market, each
claim scored, every source kept honest, the engine kept score. For
significant developments and the capital decisions they force; not for
day trading.*
A historically-backed intelligence instrument for investors in oil
production, trade, and petro-products (fuels, LNG, fertilizer,
petrochemicals). Given any development — a strike, a sanction, an OPEC
decision, an analyst's claim — it returns the measured weight of
decomposed history, conditioned on the geopolitical and market state
then versus now, propagated through the physical value chain, read
against the live market, and scored over time against what actually
happened. It is the disciplined outside view: the strongest second
opinion in the room, with every link traceable. It does not claim to
predict; it claims to measure, condition, and keep score.

## 2. Scientific basis (a synthesis of four validated methods)
- Structured Analogies (Green & Armstrong 2007): list analogs, rate
  similarity, match outcomes → forecast. Tested on conflict situations:
  unaided experts 32%, structured analogies 46%, 60% with ≥2 analogs and
  direct experience. → the engine's retrieval + differencing.
- Reference Class Forecasting (Kahneman, Tversky; Flyvbjerg): the outside
  view — a reference class of similar cases, its outcome distribution,
  then adjustment for the case at hand. → base rates + adjustment.
- Analysis of Competing Hypotheses (Heuer, CIA): hypotheses × evidence
  matrix built to disconfirm. → the scenario tree with evidence status.
- ViEWS (Uppsala): conflict forecasts sealed until outcomes are known,
  scored strictly out-of-sample against UCDP. → the walk-forward backbone.
Novelty: their combination, wired to a measured propagation graph of the
oil economy. Each component is peer-reviewed; the instrument is new.

## 3. Architecture — four organs on one spine
Spine: the RIPPLE GRAPH — assets, entities, events joined by MEASURED
transmission edges (event studies per event × asset; ~7,900 edges).
1. Live data, ripple-aligned (38+ series: crude, products, cracks, LNG,
   fertilizer, transits, macro; refreshed daily).
2. History, ripple-aligned: the verified event corpus, each event
   decomposed and joined to its measured reactions, flow side and price
   side separately.
3. Live intake & categorizer: continuous ingestion (news, APIs, market
   announcements), classification to type + entities, decomposition to
   the ripple level, handed to the engine. Intake ≠ corpus: nothing
   enters the historical record without the admission gates.
4. The Situation Engine (the quant heart) — §4.
Binding rule: every number on screen is one hop from (a) a measured
historical reaction, (b) its conditioning state, (c) the live market,
(d) a track-record receipt.

## 4. The Situation Engine — two coupled layers
### 4.0 Big Moves — market-defined significance (NORTH_STAR §1c)
Before any event-first analysis, the record is read market-first: every
episode in the registered top tail of measured change (20/60-day price
moves top 5%, curve flips, vol-regime breaks, product-spread blowouts,
flow drops; per asset; 1987+ daily, 1970+ monthly where data exist) is
identified, then attributed to the corpus event(s) knowable in its window
or marked NO IDENTIFIED EVENT. Outputs: data/big_moves.json; two-way base
rates P(big move | class) and P(class | big move); the materiality gate
is derived from the first, the "what has ever changed this market" table
from the second. Published as computed, whatever it shows about conflict.
### 4.1 The Situation Record (per event, historical and live)
PHYSICAL: asset hit, asset role (export terminal / processing / chokepoint
/ pipeline), outputs affected + share, volume at risk, spare capacity and
substitutes at the time, downstream chain (from the ripple graph).
GEOPOLITICAL: actor; target; actor response propensity (measured from the
actor's own record); target response capacity (sourced); alliance
engagement; conflict scope (isolated / campaign / war); tempo (first or
nth); diplomatic state (talks, sanctions regime); prior outcome in this
dyad (what happened last time these actors clashed).
MARKET/POLICY (existing): VIX, inventories, positioning, GPR, curve, SPR
and OPEC posture.
Every field is coded from sources with a citation, or set to "unknown."
Never inferred from outcomes. Human-gated.

### 4.2 Layer G — the Escalation Model (what happens next, geopolitically)
Categorical outcome per situation: CONTAINED / LIMITED RETALIATION /
WIDENING / RESOLUTION-BY-DEAL, observed at +30/+90 days from sources.
Method: structured-analogy retrieval on the geopolitical block →
conditioned reference class → branch base rates with n. Conditioned
subsets count at n≥8; below that the engine falls back to the parent
class and shows a "thin conditioning" flag. Corpus: events only (no
prices required) — extended to 1970 (deep-history tier) so real
precedents (1973 embargo, 1979, the 1985–87 Kharg strikes, tanker war)
are inside the engine.

### 4.3 Layer P — the Propagation Model (what a scenario does to markets)
Given a branch (e.g., asset offline N days / premium-only / widening),
walk the ripple graph: measured pass-through at each hop, PRICE side
(signed reaction, dispersion) beside FLOW side (transits/production —
did barrels stop?). Corpus: 1987+ (daily prices). The load-bearing
finding "conflict doesn't stop trade" is Layer P's headline: realized
flow disruption is the measured minority; the risk premium is the usual
response — reported as a fraction with n, never a slogan.

### 4.4 The Read — a scenario tree with a differencing table
For a live situation: Layer G branch base rates (with n) × Layer P chain
impact per branch (with n at every hop) → the tree. The DIFFERENCING
TABLE: field-by-field then-vs-now against each top analog; each
difference tagged with which branch it shifts and its evidence status —
"measured (subset rate, n)" or "judgment, unmeasured." Likenesses shown
as prominently as differences. Live market overlay: implied vs current,
premium vs realized. "NO ADEQUATE PRECEDENT" is a first-class output.
Track-record stamp: the engine's walk-forward score for this class.

## 5. The self-enforcing backbone — walk-forward validation
Stand at date t; the engine sees only what was knowable at t (no
lookahead in features, thresholds, or retrieval). Produce the read for
every open situation at t (+1w/+1m/+1q). Advance. Score: G-score = Brier
over realized branches; P-score = error on realized magnitude/sign given
the realized branch. Two evaluation windows minimum (train ≤2014 → test
2015–2019; train ≤2019 → test 2020–2026) = two scored cycles, computed
now. Baseline: the unconditioned reference class. The honest question the
backbone answers: does conditioning beat the base rate out of sample?
Results are published whatever they show; weights move only on
out-of-sample evidence; nulls stay nulls. Every card carries its score.

## 6. Integrity regime (already built, retained)
Two-source rule and human gate for every corpus event; caged extraction
with no-fabrication tests; pre-registration of hypotheses with git
timestamps; matched placebo controls; regime-block robustness;
permutation-FDR; one evidentiary bar; a single acceptance command;
adversarial review published (docs/red_team_1.md). Any conditioner is
labeled SUGGESTIVE until it clears the bar in §5.

## 7. Operating model
Continuous: intake every 15 minutes with inline decomposition; daily:
data refresh, integrity check, backups, engine read, Desk regenerated;
weekly: analyst reviews the borderline queue (human gate); quarterly:
walk-forward re-scored, weights re-evaluated, calibration published.
Front door (NORTH_STAR §7): FEED (material stories ranked by the gap
between narrative and record; LOUD/QUIET and QUIET/LOUD flags; NOISE
shelf) → STORY PAGE (significance → is it priced → claim verdicts →
branch table → propagation → trust: engine score + source record → notes
& export; also the paste/URL door) → LEDGER (engine vs base rate; record
vs narrative; sources). Deep views: Trace, Terminal, Backtest. Single-
user, local, $0.

### 7.1 The Claim Ledger
Every checkable claim (asset + direction/magnitude/flow/escalation +
horizon) the engine reads is logged point-in-time with its verdict and
resolves at horizon from data (+20/+60 trading days; +30/+90 calendar
days for escalation), never by hand. Claims that do not resolve to those
fields are UNCHECKABLE and shown as such. Scoreboards: engine vs base
rate (§5); record vs narrative (per resolved story, which was closer);
per-source and per-claim-type resolved-true rate with n. Seed: the corpus
events' own source articles, claim-extracted point-in-time and resolved
against measured CARs already in the DB.

## 8. What "it works" means — acceptance criteria a skeptic would sign
A1 Situation records: 100% of corpus events carry the physical and
   geopolitical blocks, each field sourced or "unknown"; a 20-event
   spot audit shows codings match sources.
A2 Retrieval: any intake returns ranked analogs with similarity scores
   and a likeness/difference table; "no adequate precedent" demonstrably
   fires below threshold (unit-tested).
A3 Scenario tree: branch rates from conditioned subsets with n; fallback
   flagged; only historical frequencies, never invented probabilities.
A4 Propagation: per-branch chain hops with measured edges, flow and
   price shown separately, n on every hop.
A5 Walk-forward: two scored windows published with G- and P-scores
   against the base-rate baseline; every number reproducible.
A6 Live loop: intake continuous; Desk fresh without human action.
A7 Integrity: acceptance green; placebo null; no-fabrication tests pass;
   every displayed number one hop from its receipt.
A8 Deep history: ≥60 sourced geopolitical events 1970–1989 in Layer G.
A9 Claim Ledger: every checkable claim logged point-in-time and resolved
   from data at horizon; the corpus-article pilot published as a
   record-vs-narrative number with N; source scoreboard live (may be
   thin, labeled).
A10 Materiality and Feed: the gate is measured (class CI vs baseline
   CI), NOISE is shelved not hidden, the Feed ranks by narrative-vs-
   record gap, LOUD/QUIET flags computed from an attention series.
A11 Big Moves: thresholds registered before computing; every top-tail
   episode per asset listed with attribution or NO IDENTIFIED EVENT;
   two-way base rates published; the materiality gate demonstrably
   derived from them; Big Moves timeline on the surface.
When A1–A11 hold, the instrument works, and anyone can verify it does.

## 9. Current state and roadmap
Built: spine, live data, price-layer history (289 events), intake and
triage, the Desk and deep views, the integrity regime, the backtest
console. Building now (BUILD_V2.md): situation records (A1), the
Situation Engine (A2–A4), continuous intake (A6), the walk-forward
backbone (A5), deep history (A8). Future: additional domains, intraday
resolution, multi-user deployment.
