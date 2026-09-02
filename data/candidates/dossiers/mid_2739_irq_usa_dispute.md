# Dossier mid_2739_irq_usa_dispute — IRQ USA dispute

```json
{
 "id": "mid_2739_irq_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2739",
  "detail": "dispute 2739 IRQ-USA 1987-05-17..1987-05-18 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-05-17",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-05-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.iraq",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irq Usa Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Irq+Usa+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-04-17",
   "1987-06-16"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:27+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2739 **IRQ USA dispute**: dispute 2739 IRQ-USA 1987-05-17..1987-05-18 hihost 4 trigdate 1987-05-17, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Usa Dispute 1987` (https://history.state.gov/search?q=Irq+Usa+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-04-17..1987-06-16. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2739_irq_usa_dispute --approved-by joe`. The code never runs it.
