# Dossier mid_4137_can_frn_gmy_nor_tur_ukg_usa_yug_dispute — CAN FRN GMY NOR TUR UKG USA YUG dispute

```json
{
 "id": "mid_4137_can_frn_gmy_nor_tur_ukg_usa_yug_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4137",
  "detail": "dispute 4137 CAN-FRN-GMY-NOR-TUR-UKG-USA-YUG 1998-05-03..1999-06-10 hihost 5",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1998-05-03",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-05-03",
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
   "entity": "country.canada",
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
   "entity": "country.hungary",
   "role": "unknown"
  },
  {
   "entity": "country.serbia",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.nor",
   "role": "unknown"
  },
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210,
  211,
  212,
  230,
  235,
  290,
  316,
  325,
  339,
  343,
  350,
  368,
  390,
  395
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Can Frn Gmy Nor Tur Ukg Usa Yug Dispute 1998",
  "search_url": "https://history.state.gov/search?q=Can+Frn+Gmy+Nor+Tur+Ukg+Usa+Yug+Dispute+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-04-03",
   "1998-06-02"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:40+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4137 **CAN FRN GMY NOR TUR UKG USA YUG dispute**: dispute 4137 CAN-FRN-GMY-NOR-TUR-UKG-USA-YUG 1998-05-03..1999-06-10 hihost 5 trigdate 1998-05-03, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 211: UNMAPPED
- 212: UNMAPPED
- 220: country.fra (registered state set)
- 230: UNMAPPED
- 235: UNMAPPED
- 255: country.deu (registered state set)
- 290: UNMAPPED
- 310: country.hungary
- 316: UNMAPPED
- 325: UNMAPPED (registered state set)
- 339: UNMAPPED
- 343: UNMAPPED
- 345: country.serbia
- 350: UNMAPPED
- 365: country.russia (registered state set)
- 368: UNMAPPED
- 385: country.nor (registered state set)
- 390: UNMAPPED (registered state set)
- 395: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.deu:unknown, country.hungary:unknown, country.serbia:unknown, country.russia:unknown, country.nor:unknown, country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Can Frn Gmy Nor Tur Ukg Usa Yug Dispute 1998` (https://history.state.gov/search?q=Can+Frn+Gmy+Nor+Tur+Ukg+Usa+Yug+Dispute+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-04-03..1998-06-02. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4137_can_frn_gmy_nor_tur_ukg_usa_yug_dispute --approved-by joe`. The code never runs it.
