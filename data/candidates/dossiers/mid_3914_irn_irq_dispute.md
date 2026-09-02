# Dossier mid_3914_irn_irq_dispute — IRN IRQ dispute

```json
{
 "id": "mid_3914_irn_irq_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3914",
  "detail": "dispute 3914 IRN-IRQ 1989-02-17..1989-03-13 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1989-02-17",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1989-02-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
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
  "query": "Irn Irq Dispute 1989",
  "search_url": "https://history.state.gov/search?q=Irn+Irq+Dispute+1989&within=documents",
  "search_status": 200,
  "window": [
   "1989-01-18",
   "1989-03-19"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:01+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3914 **IRN IRQ dispute**: dispute 3914 IRN-IRQ 1989-02-17..1989-03-13 hihost 4 trigdate 1989-02-17, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irn Irq Dispute 1989` (https://history.state.gov/search?q=Irn+Irq+Dispute+1989&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1989-01-18..1989-03-19. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3914_irn_irq_dispute --approved-by joe`. The code never runs it.
