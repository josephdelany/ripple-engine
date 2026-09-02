# Dossier mid_4273_irq_sau_ukg_usa_dispute — IRQ SAU UKG USA dispute

```json
{
 "id": "mid_4273_irq_sau_ukg_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4273",
  "detail": "dispute 4273 IRQ-SAU-UKG-USA 1997-10-07..2003-05-02 hihost 5",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1997-10-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1997-10-07",
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
   "entity": "country.deu",
   "role": "unknown"
  },
  {
   "entity": "country.turkey",
   "role": "unknown"
  },
  {
   "entity": "country.iraq",
   "role": "unknown"
  },
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.kuwait",
   "role": "unknown"
  },
  {
   "entity": "country.bhr",
   "role": "unknown"
  },
  {
   "entity": "country.qatar",
   "role": "unknown"
  },
  {
   "entity": "country.uae",
   "role": "unknown"
  },
  {
   "entity": "country.omn",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210,
  290,
  325,
  350,
  900
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irq Sau Ukg Usa Dispute 1997",
  "search_url": "https://history.state.gov/search?q=Irq+Sau+Ukg+Usa+Dispute+1997&within=documents",
  "search_status": 200,
  "window": [
   "1997-09-07",
   "1997-11-06"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:36+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4273 **IRQ SAU UKG USA dispute**: dispute 4273 IRQ-SAU-UKG-USA 1997-10-07..2003-05-02 hihost 5 trigdate 1997-10-07, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 220: country.fra (registered state set)
- 255: country.deu (registered state set)
- 290: UNMAPPED
- 325: UNMAPPED (registered state set)
- 350: UNMAPPED
- 640: country.turkey (registered state set)
- 645: country.iraq (registered state set)
- 651: country.egypt (registered state set)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)
- 670: country.saudi_arabia (registered state set)
- 690: country.kuwait (registered state set)
- 692: country.bhr (registered state set)
- 694: country.qatar (registered state set)
- 696: country.uae (registered state set)
- 698: country.omn (registered state set)
- 900: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.fra:unknown, country.deu:unknown, country.turkey:unknown, country.iraq:unknown, country.egypt:unknown, country.jor:unknown, country.israel:unknown, country.saudi_arabia:unknown, country.kuwait:unknown, country.bhr:unknown, country.qatar:unknown, country.uae:unknown, country.omn:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irq Sau Ukg Usa Dispute 1997` (https://history.state.gov/search?q=Irq+Sau+Ukg+Usa+Dispute+1997&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1997-09-07..1997-11-06. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4273_irq_sau_ukg_usa_dispute --approved-by joe`. The code never runs it.
