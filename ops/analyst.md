> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Operations runbook for the legacy autonomous feeds, which are archived and inert. Not part of the submitted product; see [`README.md`](../README.md).

# The Analyst — write-up contract (runs on Claude subscription, caged)

The engine's `divergence.py` computes the *insight* deterministically (the gaps
between what it sees and what the market prices) and writes `data/divergence.json`.
Your job (as Claude — the OpenBB copilot, Claude for Chrome, or a Cowork task) is
only to **write those pre-computed gaps up as prose** — the "two analyses the market
isn't showing" reads. You add judgement and clarity; you do **not** invent edges.

## Inputs (read-only)
- `data/divergence.json` — the ranked, pre-computed divergences (attention-vs-priced,
  market movers). **These are the analyses.** Do not add gaps that aren't here.
- `data/corroboration.json`, `data/predmkt.json`, `data/portwatch.json`,
  `data/wiki_attention.json`, `data/engine_read.json` — for supporting numbers.
- `get_situation` (MCP) — the situation dossier.

## Hard rules (same discipline as the whole engine)
1. **Only numbers already in the engine's artifacts.** Every figure you cite must come
   from a JSON above. No invented prices, targets, or probabilities.
2. **Surface divergences, never forecast.** "The market prices X at P% while the
   engine sees Y" — not "X will happen." No direction/occurrence calls.
3. **Flag reliability.** Thin prediction markets (low volume), small base-rate n, and
   correlated attention are caveats you must state (the engine already tags them).
4. **Tag it inferred.** This is analysis, not fact; it sits beside the sourced data,
   never replaces it.
5. **Cite the source.** Each read points back to the divergence.json entry + the
   market URL / signal it rests on.

## Output
2–3 short "here's a read the tape isn't emphasizing" paragraphs, each: the gap (the
two numbers), why it's non-consensus, and the caveat. That's it — the engine did the
finding; you do the framing.

*(Autonomy note: fully hands-free write-ups would run in a Cowork task on the
subscription — no paid API, per the engine's rule. The deterministic divergence
detection already runs every cycle; only this prose step needs a model.)*
