> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# Platform audit — one cohesive engine, vs the spec

*Self-audit after the convergence build (2026-09-01). Measured against Joe's brain-dump:
everything in conversation · use everything · ripple decomposition · then-vs-now
differencing · live intake · flow-not-price · question-an-article · backtest-vs-reality ·
Apple-cohesive. Verified by running (screenshots + route smoke test + acceptance).*

## Built & verified (all routes 200; acceptance framework-sound; 5 tabs, one design system)

| Spec ask | Where it lives | Evidence |
|---|---|---|
| Terminal not in a vacuum | Terminal **Ripple Lens** (`/term_ripples`) | per-product measured reaction by event class + live situations |
| Everything in conversation | shared segmented nav + cross-links (Terminal↔Trace↔Back-test↔Question↔Workbench) | every route 200; entities in Question/Trace deep-link across |
| Use everything / weak terminal DB | catalog **38 series / 12 groups** | crude…cracks…gas/LNG…chokepoint transits…cross-asset…regime signals |
| Ripple decomposition of a shock | **Shock-Tracer** (`/trace`, `shock_tracer.py`) | Iran→JKM +11.5%/TTF +9.3%; Hormuz→tankers −8.5%, each n+range+flag |
| Then-vs-now differencing ("rhymes") | **Trace** state box (`state_context`) | VIX 18th now vs ~51st then → dampening regime under validated H1 |
| Conflict ≠ stops trade (measure it) | **Flow vs Price** (`_flow_vs_price`) | signed median CAR ≈0 vs 9% magnitude = risk premium; live transits |
| Question an op-ed / analyst call | **Question** (`/question_view` → `/wb_deconstruct`) | "framing outruns the median"; "market DISCOUNTING a supply premium" |
| Backtest against reality (self-enforced) | **Back-test** (`/backtest`) | H1 holds OOS +2.9pp; walk-forward MAE 9.06→8.25; analogue NULL (honest); 247 gaps Brier 0.247 |
| Feel like Apple, cohesive | `desk.css` (SF, macOS dark, translucent masthead, segmented nav) | all 5 tabs link it; screenshots confirm |

## Honest gaps (named, not hidden — the stricter next pass)

1. **Data staleness → acceptance DEGRADED.** Feeds are a few days old (no daily refresh ran
   this session). Not breakage; a live `python3 src/daily.py` clears it to GREEN. *(Env: some
   fetchers may be network-limited here.)*
2. **Differencing depth.** Then-vs-now uses the *validated* conditioner (VIX/H1). Actor
   munitions / alliances / which-exports-matter (the Kharg→helium→LNG specifics) are not
   structured in `oil.db` — surfaced as the LNG/gas ripple we *can* measure, flagged as a gap,
   never fabricated. Deepening needs new coded fields (a corpus/enrichment task).
3. **Analogue forecaster is a null OOS.** Reported as a null (more corpus is the fix, not
   tuning) — this is correct behavior, but it means the point-forecast layer is not yet an edge.
4. **Live `situation` trace anchor** resolves only when `situation_log.actor_entity` is set;
   live situations are already surfaced on the Terminal Ripple Lens regardless.
5. **Workbench** shares the palette/links but keeps its own layout (not the segmented shell) —
   cohesive in look, distinct in structure by design (it's the writing Desk).

## Ranked stricter next steps
(a) run the daily refresh loop so the whole platform is live/GREEN; (b) enrich the corpus with
world-state + actor fields to deepen the differencing beyond VIX; (c) grow the corpus toward the
analogue edge; (d) fold the daily brief in as a first-class tab.

## Verify (run & read)
`python3 src/backend.py` → open `/terminal` `/trace_view?entity=country.iran`
`/backtest_view` `/question_view` `/workbench`. Every number one hop from a stored
computation; nulls shown; nothing fabricated. `python3 src/acceptance.py` → framework-sound.
