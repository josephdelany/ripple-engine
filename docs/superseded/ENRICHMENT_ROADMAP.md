> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# Enrichment Roadmap — making the engine smart

The goal: not just *more feeds*, but a pipeline that turns many free, noisy signals
into **confirmed, scored events** — triangulation. This is the concrete, free/local
implementation path for the belief-state engine the canon (`ENGINE_SPEC.md`) already
designs (ACH, Admiralty credibility, sqlite-vec kNN, Brier calibration).

## The three layers

```
INGEST (free modalities)   →   ENRICH (make machine-usable)   →   FUSE (confirm + score)
```

### Layer 1 — INGEST (free, by modality)
An event is credible when *independent modalities* agree. So we ingest across kinds:

| Modality | Sources (all free) | Key? | Cadence |
|---|---|---|---|
| Crowd-priced odds | **Polymarket** (Gamma/CLOB/WSS), **Kalshi**, Metaculus | no* | real-time |
| Overhead / thermal | **NASA FIRMS** (fires), Copernicus/Sentinel imagery | FIRMS key | ~3 h |
| Physical flow | **IMF PortWatch** (chokepoint transits), aisstream (AIS) | no / key | daily / live |
| Social firehose | **Bluesky Jetstream**, Mastodon, Reddit RSS, Telegram | no | live |
| News / text | GDELT DOC 2.0, RSS, Google News RSS | no | 15 min |
| Attention | Wikipedia EventStreams (edit velocity), Google Trends | no | live |
| Oil fundamentals | EIA (Cushing, refinery util, SPR, intl production), Baker Hughes rigs, crack spread, NHC→BSEE Gulf shut-ins | EIA key | daily/weekly |

\* prediction-market *data* is free/no-auth; only trading needs auth.

**Discipline:** every signal is tagged **stats-safe** (EIA/FRED only — feeds registered
statistics) vs **display/context** (everything else — never feeds the math). Never blend.

### Layer 2 — ENRICH (free/local NLP; CPU; no paid LLM)
Turn raw text/signals into structured, geolocated, deduplicated units:
- **NER**: spaCy `en_core_web_sm` + **GLiNER** (`gliner-community/*-v2.5`, Apache-2.0) for the bespoke oil ontology (facility, chokepoint, terminal, tanker).
- **Geoparse → lat/lon** (THE join key): **Irchel Geoparser** (`dguzh/geoparser`, MIT, offline GeoNames SQLite) resolves "Abqaiq"→coords so FIRMS/AIS can corroborate the same spot.
- **Embeddings + analog matching**: `sentence-transformers` (`BAAI/bge-small-en-v1.5`) into **`sqlite-vec`** (in the existing `oil.db`); `model2vec`/potion for high-volume dedup prefilter.
- **Sentiment / escalation buckets**: VADER + `ProsusAI/finbert`; zero-shot NLI for escalation → typed buckets, not decimals.
- **Translation** (GDELT/Telegram multilingual): Argos Translate / OPUS-MT (offline, permissive); `lingua-py` for language ID.
- **Source credibility prior**: Lin et al. domain-quality (0–1 over 11.5k domains) + NELA-GT (CC0).

### Layer 3 — FUSE (the brain; deterministic Python, no LLM in the math)
1. **Match signals to ONE event** — block by sliding time-window × geohash × semantic-LSH; score composite time+space+semantic+entity similarity; cluster with DBSCAN. (`datasketch`, `sentence-transformers`, `rapidfuzz`, `pygeohash`, sklearn.)
2. **Kill correlated double-counting** — the #1 trap: *20 headlines from one wire = 1 piece of evidence*. Dedup wire-copies (MinHash), then contribute **one weight per source cluster** (effective-sample-size / tempering). Without this, the engine is confidently, systematically wrong.
3. **Score confidence in decibans** — independent evidence *adds* in log-odds:
   `logit_post = logit_prior + Σ (Admiralty-discounted log-likelihood-ratio)`. Interpretable, stable, Brier-scoreable.
4. **Structure as competing hypotheses (ACH)** — {real / artifact / deception / unresolvable}; seek disconfirmers; carry the full posterior; MOM/POP/MOSES/EVE gate on high-impact single-source clusters.
5. **Calibrate + tag** — recalibrate the fused score on resolved events (`netcal` temperature→beta); map to an ICD-203 band ("likely" = 55–80%); `UNVERIFIED` is a valid terminal state.
6. **Grade continuously** — Brier + Murphy decomposition (reliability→0 is the KPI); reuse the existing `reads`/`resolve_reads` calibration ledger.

## Why prediction markets are special (the Bridgewater anchor)
Bridgewater's **"AIA Forecaster" (arXiv:2511.07678)**: an *ensemble of their forecaster
with market consensus beats consensus alone* — markets carry additive information, and
still often beat the model. That is exactly this engine's thesis: **fuse the engine's
read with the market-priced probability; don't defer to either.** Use markets right:
de-bias longshots, discount thin/single-whale/divergent markets, ensemble (log-odds pool).

## Discipline (unchanged, load-bearing)
- ONE database (`oil.db`); new signals = new rows via small `fetch_*.py` adapters.
- No paid dependency anywhere; LLM (if any) = extraction/prose only, never scoring.
- Tag everything (stats-safe/display, observed/inferred, source, confidence); buckets not
  invented decimals; the human gate is untouched; "no analogue / new regime" is valid output.
- Corroboration raises *confidence*, never the registered statistics.

## Build order
- **E1 — prediction-market adapter** (Polymarket + Kalshi): the priced anchor. *(building now)*
- **E2 — NASA FIRMS + facility gazetteer**: physical fire confirmation.
- **E3 — corroboration scaffold**: dedup → weight-of-evidence → confidence tag (the fusion brain).
- **E4+** — Bluesky firehose, GDELT DOC, geoparse/NER enrichment, PortWatch, oil fundamentals,
  then the OpenBB widget surface + MCP so the front-end is designed live.

Each is a small, free, self-contained slice that drops into the existing schema + Actions
pipeline. Sources/methods verified in `research` (July 2026); see commit history.
