# extract_agent — the event-extraction worker contract

**Who runs this:** the Cowork scheduled task = **Claude on Joe's subscription, NO API key** (same model
as `ops/situation_agent.md` / `ops/SYNTHESIZE.md`). The worker does the ONE thing an LLM is allowed to
do here: **extraction** — read sourced news and PROPOSE codebook-coded candidate events. It does **no
scoring math**; a deterministic Python cage (`src/extract_events.py`) validates everything it emits.

## Input
The newest `data/extract/inbox_<batch>.json` that `extract_prepare.py` wrote — a manifest of
already-sourced live alerts (`alert_id`, `timestamp_utc`, `source`, `headline`, `url`,
`matched_entities`, `heuristic_type`) plus `allowed_types` (the closed event vocabulary).

## Task
For each alert that describes a **discrete, dated, oil/commodity-relevant SHOCK** (per
`EVENTS_CODEBOOK.md` — a cause, not a price move), emit one proposal. Skip alerts that are commentary,
price recaps, round-ups, or not plausibly supply/demand relevant. You may do light web research to
**confirm** an event and its first-knowable date, and may add extra independent `corroborating_urls`.

## Output — write `data/extract/proposals_<batch>.json`
```json
{ "batch_id": "<same as the inbox>",
  "proposals": [
    { "alert_id": "<from the inbox — ties the proposal to a sourced alert>",
      "type": "<one of allowed_types>",
      "event_date": "YYYY-MM-DD",          // FIRST-KNOWABLE / announcement day. NEVER a later or
                                            // 'as we now know' date. Must be <= the alert timestamp.
      "date_precision": "day|week|month",
      "title": "<short factual title>",
      "description": "<one or two sentences, prose only>",
      "entities": "country.x:actor;chokepoint.y:location;commodity.z:affected_market",
      "source_url": "<MUST be a url present in this batch (an alert url or a corroborating_url)>",
      "severity_suggestion": 1-5,           // a SUGGESTION (codebook: expected disruption, not price
      "surprise_suggestion": 1-5,           //   reaction). The cage quarantines these from all math.
      "confidence": "high|medium|low",
      "rationale": "<why this type/severity — prose>",
      "corroborating_urls": ["<optional extra independent sources>"] }
  ] }
```

## Hard rules (the cage enforces every one; a violation drops the proposal to the review queue)
1. **Real source, always.** `source_url` must be a URL that physically appears in this batch (an alert
   `url` or a `corroborating_url` you provide). No source → not an event. You cannot invent a URL.
2. **Closed vocabulary.** `type` ∈ `allowed_types`; `date_precision` ∈ {day,week,month}; `confidence`
   ∈ {high,medium,low}; severity/surprise integers 1–5.
3. **First-knowable date, frozen.** `event_date` = the day the market could first have known; it must
   be ≤ the alert timestamp and ≤ today. Coding a today's-date or revised date for a past event is a
   **lookahead** violation and is rejected.
4. **No numbers in prose you didn't source.** Keep `title`/`description` factual; don't introduce
   figures not in a sourced headline (mirrors the situation-agent fabrication guard).
5. **You propose; you never admit.** Your severity/surprise are *suggestions*. Admission runs through
   the deterministic codebook gate + corroboration tiers; uncertain events wait in Joe's review queue.

## After writing
Commit/push `proposals_<batch>.json` so the engine's next run picks it up. If nothing in the batch is a
real shock, write `{"batch_id": "...", "proposals": []}` — an empty batch is a valid, honest result.
