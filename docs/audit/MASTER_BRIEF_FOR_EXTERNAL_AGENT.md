# Master brief — for an external agent with no prior context

*Paste this whole document. It is self-contained.*

---

## 1. WHY YOU ARE HERE, AND THE TWO GOALS

You are auditing a research repository. It was built over six weeks — **890 commits across 29 active
days** — by an undergraduate history major at Colby College, using multiple parallel Claude Code
sessions under a registration discipline he designed. I am one of those Claude sessions, acting as
architect. I am handing you this because **my own audit covered ~3.2% of the source and found four
defects in that 3.2%**, which means the remaining 97% is unknown.

**Two goals govern everything below. Judge every recommendation against them.**

> **GOAL 1 — SIGNIFICANT.** There must be a real finding in here that a professional would care
> about. Not "the code runs." Not "the method is rigorous." A result. If there isn't one, say so.
>
> **GOAL 2 — RESUME QUALITY.** This is going on a resume and into consulting interviews (Oliver
> Wyman and similar). It must survive a competent reader opening the repository and checking. Every
> claim must match what the code computes, or be withdrawn. **A single overclaim that a reader can
> falsify in ninety seconds costs more than five findings gain.**

These constrain the answer. A result that is real but unexplainable fails Goal 2. A result that is
presentable but overstated fails both.

---

## 2. WHAT THE PROJECT IS

**The intellectual origin.** The author watched geopolitical and economic analysts on television
reason from precedent — *"this Hormuz closure resembles the 1973 embargo because the oil stopped."*
His objection: those comparisons are selected on a handful of **surface** features when valid
inference requires **structural** correspondence across the full state. As practised the claim is
**unfalsifiable**, because the state is never made explicit. He set out to make it explicit and test
it.

That objection has a literature — Khong's *Analogies at War* (1992) on Munich and Korea in the
Vietnam decisions, May (1973), Jervis (1976) — all establishing that the reasoning happens and is
done badly, none testing whether a disciplined version carries information.

**What he built.** 313 dated geopolitical and oil-policy shocks, 1956–2026. A world-state panel from
27 academic and government sources (Correlates of War, ICB, UCDP, ATOP, Polity, V-Dem, SIPRI,
Archigos, UNGA ideal points, GPR, EIA, CFTC, World Bank, IMF, FRED, Energy Institute) — **352,295
panel rows, 772 price and macro series, 678,280 observations.** A state-conditioned analog engine
retrieves similar prior events and forecasts escalation outcomes and petroleum-complex price paths.
It walks forward through history, **sealing each forecast by SHA-256 hash before the outcome is
looked up**, scoring with strictly proper rules against four baselines, under a rule that only
information demonstrably knowable on the date may enter a read.

**The architecture is a catastrophe model** — hazard (event catalogue + reference-class retrieval),
vulnerability (damage → outage duration), exposure (which asset, what capacity), financial
(propagation across 53 nodes: crude → products → cracks → gas/LNG → fertilizer → freight → credit).
Hazard and financial are built. Exposure was attempted and reached a complete record for **5 of 80**
physical events.

**The headline results as currently published:** escalation Brier skill vs climatology **−0.084**,
95% CI [−0.175, +0.004], *p* = 0.076, n = 100. Price CRPS vs climatology **−0.074**, *p* = 0.011,
n = 246. Price vs persistence **+0.134**, *p* < 0.001 — the one comparison the engine wins.
Specification curve negative in **all 162** settings. **Four published retractions** of the project's
own positive findings.

---

## 3. WHAT IS VERIFIED SOUND — do not re-derive unless you doubt it

| file | verified |
|---|---|
| `engine/scoring.py` | CRPS is the proper `E|X−y| − ½E|X−X′|` in O(n log n); Brier multi-category; RPS per Epstein (1969); `skill = 1 − engine/ref` |
| `engine/inference.py` | Diebold–Mariano with correct Harvey–Leybourne–Newbold correction; Newey–West Bartlett kernel; Politis–Romano stationary bootstrap |
| `ripple_lp.py` | Jordà (2005) local projections with Montiel Olea & Plagborg-Møller (2021) lag augmentation, controls at t−1, HC1 primary, NW(h) diagnostic, cluster-collapsed, BH-FDR |
| `walk.py` | filtration is honest — baselines draw from the **same** constrained pool as the engine; the leakage test breaks it deliberately and scores move |
| `tests/` | **915 test functions, 2,689 assertions, zero tests without an assertion** |

**These are genuine strengths and are better than much published applied work.** If Goal 1 fails,
this discipline is still worth something and should be presented.

---

## 4. THE FOUR DEFECTS I FOUND — all the same kind

**Not bugs.** In every case the code is correct and computes a **different quantity** than the paper
says it computes. That single question — *does the code compute the quantity the sentence describes?*
— surfaced all four.

**A1 · `engine/read.py:148–177`.** The price target is the raw % change in Brent from the event date
to +20 trading days. **No market model, no abnormal-return adjustment, no detrending.** Grep for
`abnormal|market_model|expected_return|CAR` across the walk: nothing. So the engine forecasts **the
oil market**, not the event's effect, and climatology ≈ the unconditional distribution of 20-day oil
returns. **The price null follows from the target definition.**

**A2 · `engine/read.py:208`** filters candidates to the **same event class**; `walk.py:262` computes
climatology from that same pool. Both sides get class conditioning free. **k = 8 against a median
pool of 18** — the engine uses 44% of what's available, and **in 26% of reads the pool is at or below
k, so no selection occurs at all.** What was tested is within-class reranking, not "historical
analogy."

**A3 · `state/ies90.py:385–420`, rule `GED.location.ge250`.** A level can be assigned from a
**location** death count — violence anywhere in the affected country. Measured: basis is **location
for 109 of 132 labels, dyadic for 23**; of **59 non-zero labels, 47 are location-based and 12 are
dyadic.** So the escalation target is largely *"was there violence in this country"*, not *"did these
two parties escalate."* And **`engine/persistence.py:45` computes the baseline by calling the same
`score_event` on the prior 90-day window** — so persistence is that same variable lagged. **It is an
AR(1) on a country fixed effect, not a rival forecaster.**

**A4 · `situation_vintage.py:279`** — this produces the paper's **central finding**. "262 of 313
events have no state field knowable at *t*", which the paper reads as the earlier apparent skill
having been hindsight. But `knowable_at` comes from the source: a dated URL gives a real date,
**everything else falls back to `added_at`, the 2026 coding date.** Distribution across 786 values:
`coding_date(corpus-derived)` **413**, `coding_date(undated url)` **297**, `url_date` **76**. So
**710 of 786 (90%) got their date from when it was coded**, and since `kept()` requires
`date <= event_date` they drop mechanically. **The finding is about provenance recording, not
information availability.** Note `state_panel` already has `vintage`, `release` and `retrospective`
columns populated at **100% across 352,295 rows** — the infrastructure exists and the situation
fields don't use it.

---

## 5. WHAT SURVIVES — protect these, and tell me if any shouldn't have

- **The provenance result.** Even restated as metadata rather than availability, *"90% of situation
  values cannot be shown to have been knowable at the time"* is a real finding about how
  political-science panel data is built, and it generalises past this project.
- **Flags vs magnitude**, on the **44 days** that are both a corpus OPEC event and a Känzig (2021)
  announcement. Same days, four regressors, only the encoding changes: the 0/1 flag's band **covers
  zero (−1.572)**, a continuous measure of the *same events* **excludes it (+2.230)**, and the flag
  **collapses to −0.483** when both are present. Clean design; indicts every product built on dated
  event dummies.
- **5 COMPLETE of 80** on the physical exposure attempt, with six documented failure modes.
- ***r* = −0.023 over 614 months** between the "geopolitical oil risk" classes and the identified
  supply shock; Fisher-*z* CI **[−0.102, +0.056]** — a **bound**, ruling out any relationship above
  ~1% shared variance.
- **Pass-through asymmetry at h = 20**, surviving BH-FDR across a 17-test family (propane
  *q* < 0.0001, **+1.050 up vs −0.015 down**). **This replicates Bacon (1991) and
  Borenstein–Cameron–Gilbert (1997)** and must be presented as replication, not discovery.

---

## 6. WHAT IS UNEXAMINED — and my prioritisation has failed twice, so do not trust it

**147 files in `src/` write a published artifact. Together they are 43,914 lines. I have examined
~1,750 of them — 4%.** An earlier version of this brief named eight files as priorities; that list
covered **12%** of the claim-producing code and omitted `ripple_fetch.py`, the data-acquisition
layer, which is the highest-risk file in the repository because a mislabelled or misaligned series
corrupts everything downstream silently and no test would catch it.

**I have now mis-prioritised twice. Do not work from my ranking. Work from this inventory.**

### Two-pass protocol

**PASS 1 — shallow, all files.** For each file below: what artifact does it write, and does any
sentence in `README.md`, `docs/BRIEF.md`, `docs/PAPER_DRAFT.md` or `docs/OIL_FINDINGS.md` depend on
it? Output one line per file. Flag anything where a published sentence depends on a computation you
cannot immediately verify as matching its description.

**PASS 2 — deep, flagged files only.** Apply the single question: *does the code compute the
quantity the sentence describes?*

**Pass 1 across everything beats Pass 2 on a subset.** The risk here is unknown-unknowns, and every
defect found so far was in a file nobody had opened.

### The inventory — files ≥ 200 lines that write a published artifact

| lines | file |
|---:|---|
|  2374 | `src/backend.py` |
|  1561 | `src/walk.py` |
|  1224 | `src/grid_labels.py` |
|  1152 | `src/ripple_physical.py` |
|  1040 | `src/citation_guard.py` |
|   863 | `src/ripple_lp.py` |
|   851 | `src/state/ies90.py` |
|   818 | `src/brief.py` |
|   778 | `src/ripple_fetch.py` |
|   715 | `src/figures_paper.py` |
|   646 | `src/validate.py` |
|   644 | `src/engine/grid/power_arithmetic.py` |
|   623 | `src/reader.py` |
|   607 | `src/engine/delta_experiment.py` |
|   603 | `src/situation_vintage.py` |
|   573 | `src/story_read.py` |
|   573 | `src/digest.py` |
|   535 | `src/g_era_confound.py` |
|   527 | `src/read_exposure.py` |
|   519 | `src/exposure_harness.py` |
|   507 | `src/engine/grid/price_walk.py` |
|   477 | `src/engine/read.py` |
|   464 | `src/g_monthly_gap.py` |
|   449 | `src/deconstruct.py` |
|   434 | `src/edge_battery.py` |
|   433 | `src/spine_audit.py` |
|   432 | `src/evaluate.py` |
|   425 | `src/ledger.py` |
|   413 | `src/engine/similarity.py` |
|   396 | `src/exposure.py` |
|   388 | `src/magnitude_severity_retest.py` |
|   386 | `src/corroborate.py` |
|   385 | `src/acceptance_v2.py` |
|   375 | `src/cross_asset.py` |
|   372 | `src/magnitude_stage0.py` |
|   367 | `src/state/capacity.py` |
|   358 | `src/g_chokepoint_register.py` |
|   357 | `src/state/outcomes.py` |
|   353 | `src/dossier.py` |
|   339 | `src/situation.py` |
|   311 | `src/audit_reader.py` |
|   302 | `src/source_repair.py` |
|   300 | `src/ledger_backfill.py` |
|   297 | `src/evidence.py` |
|   296 | `src/state/situation_state.py` |
|   295 | `src/spine_patch.py` |
|   290 | `src/exposure_schema.py` |
|   290 | `src/engine_read.py` |
|   289 | `src/heartbeat.py` |
|   282 | `src/inference.py` |
|   281 | `src/audit_ies90.py` |
|   274 | `src/propagation_graph.py` |
|   271 | `src/antecedent.py` |
|   262 | `src/frozen_lens.py` |
|   260 | `src/scenario.py` |
|   258 | `src/big_moves.py` |
|   249 | `src/triage.py` |
|   249 | `src/evidentiary_bar.py` |
|   243 | `src/spine_apply.py` |
|   238 | `src/challenge.py` |
|   236 | `src/state/panel.py` |
|   236 | `src/spine_check.py` |
|   233 | `src/spec_curve.py` |
|   233 | `src/gpr_signal.py` |
|   232 | `src/situation_record.py` |
|   229 | `src/cross_chain.py` |
|   228 | `src/gaps.py` |
|   227 | `src/uncheckable_audit.py` |
|   227 | `src/triage_candidates.py` |
|   222 | `src/fetch_predmkt.py` |
|   222 | `src/analogue.py` |
|   220 | `src/h5_gpr.py` |
|   218 | `src/signal_registry.py` |
|   216 | `src/probability.py` |
|   209 | `src/state/bridge.py` |
|   208 | `src/state/stubs.py` |
|   204 | `src/apply_review.py` |
|   202 | `src/chain_view.py` |

*(plus 69 further files under 200 lines that also write artifacts)*

**Known high-risk, previously unnamed:**
- `src/ripple_fetch.py` — **data acquisition.** Series identity, alignment, units, transformation. An
  error here is invisible downstream and invalidates everything built on the affected series.
- `src/validate.py`, `src/acceptance_v2.py` — the acceptance gates. If a gate is wrong, "PASS" means
  nothing.
- `src/evaluate.py` — known to regenerate two retracted claims as current status.
- `src/edge_battery.py` — produced the retracted H1 and `severity_dose_response`.
- `src/state/ies90.py` — 851 lines; I read the function list and the thresholds, not the logic.
- `src/walk.py` — 1,561 lines; I read the scoring and baseline construction, not the rest.

## 7. YOUR JOB — two questions

**QUESTION 1 (Goal 2).** For each file above, read the code that produces published numbers and
answer: **does the code compute the quantity the sentence describes?** Not whether the arithmetic is
right — whether it is the **right quantity**. Cite `file:line`. If a file is clean, say so plainly; a
clean file is a real result.

**QUESTION 2 (Goal 1).** After auditing, tell me:
- **Which single result here is the most significant defensible finding**, and why.
- **What one additional analysis, using only data already in this repository**, would most raise the
  project's standing. Name the files.
- **If your answer is "none of these are significant and the honest move is to present this as a
  methods paper about measurement failure" — say that.** Better heard now than in an interview.

---

## 8. CONSTRAINTS

- **Do not edit anything.** Report only. `file:line` for every finding.
- **If you disagree with A1–A4, say so and show the code.** I would rather be wrong than have the
  author carry a bad correction. I overclaimed five separate times today; treat my audit as a
  hypothesis to attack, not a result to confirm.
- **Do not trust the prose.** Every document in this repository, including my audit, was written by
  an agent. **The code and the database are the only ground truth.**
- **Already written — do not duplicate:** `docs/audit/06_exact_restatements.md` (drop-in replacement
  text for nine claims), `docs/audit/05_remediation_plan.md`, `docs/audit/FINDINGS_CONSOLIDATED.md`.
- **Prefer breadth over depth.** A partial audit of all eight files beats a complete audit of one.
  The risk is unknown-unknowns.
- **Timeline: today.**
