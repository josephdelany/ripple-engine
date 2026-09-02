# Dossier mid_3568_irq_kuw_dispute — IRQ KUW dispute

```json
{
 "id": "mid_3568_irq_kuw_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3568",
  "detail": "dispute 3568 IRQ-KUW 1992-10-07..1994-01-02 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1992-10-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-10-07",
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
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.iraq",
   "role": "unknown"
  },
  {
   "entity": "country.kuwait",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irq Kuw Dispute 1992",
  "search_url": "https://history.state.gov/search?q=Irq+Kuw+Dispute+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-09-07",
   "1992-11-06"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:09+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3568 **IRQ KUW dispute**: dispute 3568 IRQ-KUW 1992-10-07..1994-01-02 hihost 4 trigdate 1992-10-07, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 645: country.iraq (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.fra:unknown, country.iraq:unknown, country.kuwait:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Kuw Dispute 1992` (https://history.state.gov/search?q=Irq+Kuw+Dispute+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-09-07..1992-11-06. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3568_irq_kuw_dispute --approved-by joe`. The code never runs it.
