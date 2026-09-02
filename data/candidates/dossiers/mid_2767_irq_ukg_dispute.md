# Dossier mid_2767_irq_ukg_dispute — IRQ UKG dispute

```json
{
 "id": "mid_2767_irq_ukg_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2767",
  "detail": "dispute 2767 IRQ-UKG 1988-05-14..1988-05-14 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1988-05-14",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1988-05-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
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
  "query": "Irq Ukg Dispute 1988",
  "search_url": "https://history.state.gov/search?q=Irq+Ukg+Dispute+1988&within=documents",
  "search_status": 200,
  "window": [
   "1988-04-14",
   "1988-06-13"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:53+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2767 **IRQ UKG dispute**: dispute 2767 IRQ-UKG 1988-05-14..1988-05-14 hihost 4 trigdate 1988-05-14, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown, country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Ukg Dispute 1988` (https://history.state.gov/search?q=Irq+Ukg+Dispute+1988&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1988-04-14..1988-06-13. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2767_irq_ukg_dispute --approved-by joe`. The code never runs it.
