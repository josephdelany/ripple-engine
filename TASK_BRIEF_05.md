# TASK_BRIEF_05 — The Synthesis Layer ("Engine Read")

Read CLAUDE.md first. All its guardrails apply. This brief builds the layer that
turns the engine's frozen findings into a daily, stateful read of the market.

## Outcome

A new module `src/engine_read.py` that, on every run, answers:
**"If a geopolitical shock landed TODAY, what does history say would happen?"**

It must produce:

1. `data/engine_read.json` — machine-readable:
   - `as_of` date
   - per registered hypothesis (H1 vix_pct, H2 inv_sigma, H3 cot_pct):
     latest value, the historical event-sample median it's compared against,
     and amplifier status ON/OFF (H3 reported but labeled FAILED — it did not
     survive pre-registration and must never be used as an amplifier)
   - per event type: clustered historical base-rate CAR+1/+5/+10/+20 and n
   - a plain-English `read` string, e.g. "Inventories 2.0σ below seasonal norm
     (H2 amplifier ON); VIX 38th pct (H1 OFF). A supply shock today lands on a
     physically primed but psychologically calm market."
2. `data/engine_read.md` — the same content as a short human-readable daily
   note (this is the seed of the daily publication).
3. A new `engine_read` widget in `backend.py` (table type, worst-case simple).
4. `engine_read.py` wired into `refresh.py` as the FINAL step, so every daily
   refresh ends with a fresh read.

## Standard

- Amplifier thresholds and base rates must be COMPUTED from oil.db and the same
  clustering logic as `robustness.py` (import/reuse; do not re-implement or
  fork the math).
- H1/H2/H3 directions and verdicts come from the pre-registered results. This
  module CONSUMES the registered findings; it must not re-test, re-split, or
  invent new hypotheses.
- Point-in-time discipline: the read uses only data available as of the run.
- Every number in the .md must trace to a query — no editorializing beyond the
  template `read` string.
- Teach-style comments, same voice as the rest of src/.
- Receipt: commit a sample run as `data/engine_read_sample.txt` (console
  output), and show `python3 src/refresh.py` completing with the new step OK.

## Bounds

- No new data sources. No scraping. No API keys touched.
- No events added or modified (human gate stands).
- No trading logic of any kind.
- Do not modify event_study.py, robustness.py, conditioned_study.py logic —
  import only.
- Do not kill or rebind ports 5050/6900.
- If anything can't be computed honestly, say so in the output rather than
  approximating.
