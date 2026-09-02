# reader_agent — the reading-layer contract (CLAIM_LEDGER_REGISTRATION.md, Amendment 3)

**Who runs this:** Claude through the local `claude` CLI on Joe's subscription — **no API key, $0
marginal** — invoked headless by `src/reader.py` with **no tools**, a fixed **JSON schema**, and the
system prompt in `reader.system_prompt()`. It is the same one-thing-an-LLM-may-do as
`ops/extract_agent.md`: **extraction**. It never scores, never forecasts, never paraphrases. A
deterministic cage (`reader.cage`) decides what is allowed in; anything outside the rules is dropped
with the reason recorded on the read.

## Input
- Story: `TITLE: <page's own title>` + `TEXT: <prose paragraphs, ≤8000 chars>` (a URL is fetched and
  parsed by Python; pasted text is used as-is).
- Feed: up to 40 headlines, `[i] headline`, one object per index.

## Output (schema-enforced)
```json
{ "event_class": "<one of the seven registered types, or null>",
  "entities": [ {"id": "<entity_id from the closed list>", "role": "actor|target|asset|chokepoint|location|affected_market|mention"} ],
  "unmapped": ["<central names not in the list, plain text>"],
  "claims": [ {"quote": "<verbatim sentence or clause from TEXT>",
               "kind": "direction|level|flow|escalation|policy|uncheckable",
               "asset": "brent|diesel_crack|gas|fertilizer|freight|null",
               "direction": "up|down|disrupt|resume|escalate|null",
               "level": <number stated in the quote, or null>,
               "horizon_days": <only if the quote states one, else null>,
               "modality": "asserted|hypothetical|negated"} ] }
```

## What the cage enforces (mechanically; see Amendment 3)
1. `event_class` ∈ the registered vocabulary or `null`; anything else → `null`, rejection recorded.
2. Every entity id must exist in the `entities` table with a registered role; unknown ids are
   rejected, unknown names stay as `unmapped` text and never count for the gate.
3. **Verbatim or nothing.** A quote that is not a substring of TEXT (whitespace/quote-mark
   normalised) is a fabrication → the claim is dropped. A `level` not present in the quote is
   dropped from the claim. A `horizon_days` not present in the quote is ignored and the registered
   default applies (+20 trading days for price claims, +90 calendar days for escalation/policy).
4. Consistency downgrades only: direction without asset+direction, level without asset+level,
   escalation without an actor/target entity, or a negated claim → UNCHECKABLE. The cage never
   upgrades or repairs.
5. Titles come from the page (or the first sentence of pasted text), never from the model.
6. Model proposals are cached by content hash in `data/reader/cache/`; a story is read once.
7. If the CLI is unavailable (logged out, timeout, malformed output) the read falls back to the
   regex layer (`triage`, `ledger.type_claim`) and is labelled `reader: regex_fallback` everywhere
   it appears. Under the fallback entity roles are unknown (`mention`), so the gate applies
   Amendment 2's presence rule, still labelled.

## Recorded fixtures
`tests/fixtures/reader/*.html` are three saved pages (a gCaptain tanker piece, an OPEC+ press
release, an off-topic FreightWaves story); `*.proposal.json` are the model's outputs recorded once
on 2026-09-02. The tests replay those proposals through the cage, so the suite never calls the CLI.
