# Dossier mid_3974_frn_irq_ukg_usa_dispute — FRN IRQ UKG USA dispute

```json
{
 "id": "mid_3974_frn_irq_ukg_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3974",
  "detail": "dispute 3974 FRN-IRQ-UKG-USA 1991-03-15..1991-12-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1991-03-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1991-03-15",
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
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Frn Irq Ukg Usa Dispute 1991",
  "search_url": "https://history.state.gov/search?q=Frn+Irq+Ukg+Usa+Dispute+1991&within=documents",
  "search_status": 200,
  "window": [
   "1991-02-13",
   "1991-04-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:35+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3974 **FRN IRQ UKG USA dispute**: dispute 3974 FRN-IRQ-UKG-USA 1991-03-15..1991-12-28 hihost 4 trigdate 1991-03-15, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.fra:unknown, country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Frn Irq Ukg Usa Dispute 1991` (https://history.state.gov/search?q=Frn+Irq+Ukg+Usa+Dispute+1991&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1991-02-13..1991-04-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3974_frn_irq_ukg_usa_dispute --approved-by joe`. The code never runs it.
