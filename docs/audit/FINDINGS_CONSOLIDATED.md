> **HISTORICAL AUDIT SNAPSHOT — SUPERSEDED AS CURRENT STATUS.** This file records the audit state before the maintained structural-versus-surface experiment and later repository-wide closure. Its present-tense coverage and “central finding” statements are not current. Use [`PUBLIC_PRODUCT_CLOSURE.md`](PUBLIC_PRODUCT_CLOSURE.md), [`../PAPER.md`](../PAPER.md), and [`../../SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md). `docs/EVENTS_CODEBOOK.md` now exists.

# Consolidated audit findings — all passes, one document

*2026-09-03. Supersedes `docs/EXTERNAL_REVIEW_2026-09-03.md` and `docs/SYSTEM_AUDIT_2026-09-03.md`,
which were partial passes. Every finding below was verified against committed code or recomputed
from the database.*

---

## ⚠ COVERAGE — read this before anything else

| | |
|---|---:|
| Total source | **54,680 lines** |
| Examined (full, plus 25% credit for partial reads) | **~1,749 lines** |
| **Coverage** | **3.2%** |
| Unexamined files over 300 lines | **43** |

**Three Tier-1 defects were found in 3.2% of the code. The base rate implies more exist.** This
audit is not complete and must not be represented as complete.

**Most serious coverage gap:** `src/situation_vintage.py` (603 lines) produced the **262 of 313**
figure — the paper's central finding, and the one result this audit has repeatedly called sound. **It
has never been opened.** That claim is currently unverified at the code level.

---

## TIER 1 — Defects that determine the result

### A1 · The price target is a raw return with no market model
`engine/read.py:148–177`. `path()` = `(seg/seg[0]−1)*100`; `outcome()` takes `pct[h]` at +20 trading
days. No expected-return model, no detrending. Grep for `abnormal|market_model|expected_return|CAR`
across the walk: **nothing**.
→ The engine is asked to forecast the **oil market**, not the event effect. Climatology ≈ the
unconditional distribution of 20-day oil returns. **The price null follows from the target
definition.**

### A2 · The pool is class-filtered, so the headline means something far narrower
`engine/read.py:208` admits only same-class candidates; `walk.py:262` computes climatology from that
same pool. Both sides get class conditioning free.

| k | median G pool | engine's share | reads with pool ≤ k | events with no situation field |
|---:|---:|---:|---:|---:|
| **8** | **18** | 44% | **26%** | **262/313 (84%)** |

→ What was tested is **within-class reranking on market state vs within-class pooling** — not
"formalised historical analogy."

### A3 · The escalation target is 83% a country-violence indicator
`state/ies90.py:385–420`, rule `GED.location.ge250`.

| basis | lvl 0 | 1 | 2 | 3 | total |
|---|---:|---:|---:|---:|---:|
| dyadic | 11 | 3 | 5 | 4 | **23** |
| location | 62 | 6 | 25 | 16 | **109** |

Of **59 non-zero labels: 47 location-based, 12 dyadic.**
**Corollary:** `engine/persistence.py:45` calls the *same* `score_event` on [t−90, t−1] — so
persistence is that same variable lagged. Country violence is heavily autocorrelated.
→ **Persistence is an AR(1) on a country fixed effect, not a rival forecaster.** This mechanically
explains OPEN_ITEMS 1.1 and shows G's grid-panel location artefact is in the main corpus and
dominates it.

---

## TIER 2 — Published claims that fail; implementation choices that weaken inference

| # | finding | status |
|---|---|---|
| **B1** | **Anticipation is mostly definitional.** `big_moves.py:92` sets onset to the ex-post price extreme; median episode 76 d, 100% exceed 20 d; uniform null gives **55% "anticipated" mechanically** vs **69%** observed. | **withdraw** |
| **B2** | **Red Sea is confounded.** Brent **−14.8% in Q4 2023 before the attacks**; **+9.5% across the attack window**. The published −4.9% is a windowing choice at n = 2. | **demote to illustration** |
| **B3** | **Pass-through is a replication** — Bacon (1991); Borenstein, Cameron & Gilbert (1997, *QJE*). Survives FDR at h=20 (propane *q*<0.0001) but is not new. | **reposition** |
| **B4** | **Model family lacks diversity.** M02/M04/M10 weight a block empty for 84% of events; M01/M06/M07 differ only in *k*; M08/M09 only in threshold. Hedge sits at exactly **1/13** on every item. SPA and the Reality Check have little power. | **disclose** |
| **B5** | **`as_of` = `obs_date` for revision-prone EIA series.** Weekly stocks publish days late and are revised. `inv_sigma` — 1 of only 3 "physical" fields — inherits a mild look-ahead. | **disclose** |
| **B6** | **Percentile bootstrap on a ratio statistic** (`skill = 1 − engine/ref`). BCa would be more accurate. | **low severity** |

---

## TIER 3 — Structural limits

| # | limit |
|---|---|
| **C1** | State vector is macro-financial, not fundamental. "Physical" block = 3 price-derived fields. No days-of-cover, supply growth, demand growth, floating storage — from 772 available series. A design choice. |
| **C2** | Reference class spans incommensurable regimes: 8 events pre-1983 (no crude futures), 78 pre-2010 (pre-shale), **150 of 313 in the 2020s**. |
| **C3** | Escalation is a political-science target carrying most of the apparatus, not the economic question. |
| **C4** | `policy_response` = 57 heterogeneous events, second-largest class. |
| **C5** | Only 4 of 7 classes are G-scorable (`similarity.py:46`). |
| **C6** | 106 skip/xfail markers across the suite. |
| **C7** | **`EVENTS_CODEBOOK.md` is not in this repository** — the corpus inclusion rule cannot be audited from this tree. |

---

## VERIFIED SOUND — claim these

1. **Scoring correct.** CRPS = proper `E|X−y| − ½E|X−X′|` in O(n log n); Brier multi-category; RPS per Epstein (1969); `skill = 1 − engine/ref`.
2. **Diebold–Mariano correct**, with proper Harvey–Leybourne–Newbold correction.
3. **Newey–West correct** — Bartlett kernel, weights `1 − j/(lag+1)`.
4. **Stationary bootstrap correct** — Politis–Romano, geometric blocks, circular wrap.
5. **Local projections modern and correct** — Jordà (2005) with Montiel Olea & Plagborg-Møller (2021) lag augmentation, controls at t−1, HC1 primary, NW(h) diagnostic, cluster-collapsed, BH-FDR.
6. **Filtration honest** — baselines draw from the same constrained pool as the engine; the leakage test breaks it deliberately and scores move.
7. **Sourced-or-unknown enforced in code** — `_outcome()` returns `no_independent_outcome` rather than defaulting.
8. **Test suite real** — 915 functions, 2,689 assertions, **zero without an assertion**.

---

## WHAT REMAINS UNEXAMINED — ranked by risk

**Every file below produced a published number and has not been read.**

| lines | file | published claim it produces |
|---:|---|---|
| **603** | `situation_vintage.py` | **262 of 313 — the paper's central finding** |
| 607 | `engine/delta_experiment.py` | §11 NO ADDITION; the re-anchoring 0.682→0.506 |
| 644 | `engine/grid/power_arithmetic.py` | n_eff 1,979; "50× rows buys 7.9× power" |
| 507 | `engine/grid/price_walk.py` | "fitting does not beat frozen", +0.0013 |
| 1,152 | `ripple_physical.py` | Red Sea/Hormuz; JODI coverage dates |
| 535 | `g_era_confound.py` | "era confound not separable at n=150" |
| 433 | `spine_audit.py` | provenance: 11.9% / 25.0% / 63.1% |
| 434 | `edge_battery.py` | the retracted H1; `severity_dose_response` |
| 1,224 | `grid_labels.py` | the dyad-date panel, 15,740 cells |
| 646 | `validate.py` | acceptance gates |

**Lower risk (infrastructure, not claims):** `backend.py` (2,374), `api_v2.py`, `mcp_server.py`,
`terminal_api.py`, `figures_paper.py`, `citation_guard.py`, `digest.py`, `story_read.py`.

---

## The honest verdict

**The engineering is sound where it was checked. Both outcome variables are mis-specified relative
to the claims made about them. Three published findings fail. And 96.8% of the code has not been
audited, including the file that produces the paper's central result.**

The correct next action is not to fix — it is to **finish the audit**, starting with
`situation_vintage.py`, because the project's headline finding currently rests on code no one has
verified.
