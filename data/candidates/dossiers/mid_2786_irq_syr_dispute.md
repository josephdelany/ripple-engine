# Dossier mid_2786_irq_syr_dispute — IRQ SYR dispute

```json
{
 "id": "mid_2786_irq_syr_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2786",
  "detail": "dispute 2786 IRQ-SYR 1987-07-28..1987-07-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-07-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-07-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "unknown"
  },
  {
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irq Syr Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Irq+Syr+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-06-28",
   "1987-08-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:36+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2786 **IRQ SYR dispute**: dispute 2786 IRQ-SYR 1987-07-28..1987-07-28 hihost 4 trigdate 1987-07-28, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iraq:unknown, country.syr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Syr Dispute 1987` (https://history.state.gov/search?q=Irq+Syr+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-06-28..1987-08-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2786_irq_syr_dispute --approved-by joe`. The code never runs it.
