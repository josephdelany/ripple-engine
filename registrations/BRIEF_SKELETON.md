> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# When Do Geopolitical Shocks Actually Move Oil?
## Evidence from 40 Years of Events — Registered Analysis Plan & Brief Skeleton

**Author:** Joseph Delany
**Status:** REGISTERED SKELETON — hypotheses declared BEFORE conditioning results are computed.
**Registered:** 2026-07-21 (git-committed; the commit timestamp is the pre-registration record)
**Rule:** Sections marked [PENDING] are written ONLY after the analysis runs. Nothing in them may be drafted, hinted, or assumed before then.

---

## 1. The Question (~half page)

Policymakers and market commentary routinely assume that military escalation drives oil prices — an assumption that quietly underwrites threat inflation, energy-security arguments, and intervention rhetoric. Is it true? And if the average effect is weaker than assumed, what actually determines when a geopolitical shock produces a large, persistent market ripple?

This brief tests both questions against four decades of daily price data and a hand-curated, fully-sourced database of 20 energy-geopolitical events.

*[Final hook paragraph written AFTER results — it must describe what was found, not what was hoped.]*

## 2. Data (~half page)

- **Prices:** Daily Brent and WTI spot prices, FRED (DCOILBRENTEU, DCOILWTICO), 1986/87–present (~10,000 trading days each).
- **State variables:** Broad dollar index, 2Y & 10Y Treasury yields, VIX, Henry Hub natural gas (FRED); weekly US crude inventories ex-SPR (EIA); managed-money positioning (CFTC Commitment of Traders). All ingested into a canonical schema with provenance (source URL + retrieval date per observation).
- **Events:** 20 discrete energy-geopolitical shocks, 1990–2023, six pre-registered types (conflict escalation, OPEC decision, sanctions, infrastructure attack, demand shock, chokepoint disruption). Each event: dated to first public knowability, severity (1–5) and surprise (1–5) coded per a written codebook *before* analysis, every event cited to a primary or wire source. Codebook and full dataset public in the repository.
- **Known limitations, stated up front:** n = 20 events (17 independent episodes after clustering); event coding involves judgment; the sample over-represents recent decades.

## 3. Method (~half page)

- **Event study** (MacKinlay 1997): constant-mean-return model over an estimation window of t−130 to t−11; abnormal returns cumulated over an event window of t−5 to t+20; CAR reported at +1, +5, +10, +20 days. Windows declared before analysis and not varied thereafter.
- **Conditioning:** each event is assigned the value of each state variable as of t−1 (last reading strictly before the event — no lookahead). Ripple magnitude |CAR+20| compared across high/low states split at the sample median.
- **Clustering correction:** events whose windows overlap within 35 calendar days are collapsed to one episode (first event kept). All conditioning results reported both raw and clustered.
- **Honesty rules:** all pre-registered hypotheses are reported regardless of outcome; no metric added after seeing results may be presented as confirmatory; significance at this n is treated as indicative, never conclusive.

## 4. PRE-REGISTERED HYPOTHESES (declared 2026-07-21, before computation)

**H1 — Market stress conditioning (VIX).** Shocks arriving when the VIX sits above its sample-median 5-yr percentile produce larger |CAR+20| than shocks arriving in calm conditions. *Mechanism: thin risk appetite amplifies transmission.* (Note: an earlier exploratory pass suggested this; it is re-tested here as confirmatory alongside H2/H3, clustered.)

**H2 — Physical tightness conditioning (inventories).** Shocks arriving when US crude inventories ex-SPR are below their seasonal norm (negative σ deviation from the 5-yr seasonal band at t−1) produce larger |CAR+20|. *Mechanism: thin physical buffers cannot absorb supply risk, so price must.*

**H3 — Positioning conditioning (COT).** Shocks arriving when managed-money net-long positioning is at an extreme percentile of its 5-yr range produce larger |CAR+20|. *Mechanism: crowded positioning unwinds violently on shocks.*

**H4 (descriptive, already computed — reported as-is):** Mean CAR by event type, including the finding that conflict escalation shows approximately zero average effect (n=6) with large dispersion — and the prior failed hypothesis that "surprise" coding conditions magnitude (it did not, −1.7pp).

**Decision rule, fixed now:** a hypothesis "holds" if the clustered amplification exceeds +5pp in the predicted direction; "fails" otherwise. Partial/mixed outcomes reported as such. No re-splitting, re-windowing, or metric substitution after results are seen.

**H5 — GPR conditioning (EXPLORATORY, registered 2026-07-23, before computation).** Question: do shocks arriving when the Caldara–Iacoviello daily GPR index sits above its sample-median percentile at t−1 produce systematically different |CAR+20| than shocks arriving in geopolitically calm conditions? **No direction is predicted.** The analyst's stated position at registration: "not sure" — two plausible mechanisms point opposite ways (elevated tension → fragility/amplification, vs. elevated tension → anticipation/pre-pricing → dampening). Accordingly H5 is registered as a two-sided exploratory question: results will be reported as hypothesis-generating, with a two-sided permutation p, and may NOT be described as confirming a prediction, because none was made. The +5pp directional decision rule does not apply to H5. Same splits, clustering, standardization, and honesty rules as H1–H3.

## 5. Results — [PENDING — DO NOT WRITE UNTIL THE ANALYSIS RUNS]

*[Table: mean CAR by event type (already computed, stable). Table: H1–H3 conditioning results, raw and clustered. The ripple figure and conditioned-ripple figure. Whatever the numbers say, verbatim honesty.]*

## 6. What It Means for Statecraft — [PENDING — follows from Results only]

*[To be argued from findings. If the conflict null + conditioning story holds: markets do not price escalation per se; they price escalation into fragile states — implications for threat-inflation narratives, sanctions timing, energy-security planning. If conditioning fails: the honest conclusion is that ripple size is not predictable from these state variables at this sample size — itself a policy-relevant negative result. Restraint-relevant either way.]*

## 7. Limitations & Future Work (~quarter page)

Small n; wide intervals; event-coding judgment; single market (oil) in a single country's data; confounding within clustered macro episodes (2020). Future: multi-domain extension (FX, rates, minerals), automated event ingestion with human verification, live forecast log scored against market-implied odds (Kalshi).

---
*Engine, data, codebook, and full revision history: github repository (ripple-engine). Every number in this brief is reproducible by running the committed scripts against the committed data.*
