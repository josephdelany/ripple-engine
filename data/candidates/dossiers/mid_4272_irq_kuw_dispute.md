# Dossier mid_4272_irq_kuw_dispute — IRQ KUW dispute

```json
{
 "id": "mid_4272_irq_kuw_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4272",
  "detail": "dispute 4272 IRQ-KUW 1996-10-01..1997-09-25 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1996-10-01",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-10-01",
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
   "entity": "country.kuwait",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irq Kuw Dispute 1996",
  "search_url": "https://history.state.gov/search?q=Irq+Kuw+Dispute+1996&within=documents",
  "search_status": 200,
  "window": [
   "1996-09-01",
   "1996-10-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:23+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4272 **IRQ KUW dispute**: dispute 4272 IRQ-KUW 1996-10-01..1997-09-25 hihost 4 trigdate 1996-10-01, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iraq:unknown, country.kuwait:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Kuw Dispute 1996` (https://history.state.gov/search?q=Irq+Kuw+Dispute+1996&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1996-09-01..1996-10-31. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4272_irq_kuw_dispute --approved-by joe`. The code never runs it.
