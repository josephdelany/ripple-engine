# Dossier mid_3551_frn_gmy_ukg_usa_yug_dispute — FRN GMY UKG USA YUG dispute

```json
{
 "id": "mid_3551_frn_gmy_ukg_usa_yug_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3551",
  "detail": "dispute 3551 FRN-GMY-UKG-USA-YUG 1992-07-16..1996-10-02 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1992-07-16",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-07-16",
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
   "entity": "country.serbia",
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
  230,
  235,
  325,
  350,
  360,
  390
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Frn Gmy Ukg Usa Yug Dispute 1992",
  "search_url": "https://history.state.gov/search?q=Frn+Gmy+Ukg+Usa+Yug+Dispute+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-06-16",
   "1992-08-15"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:03+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3551 **FRN GMY UKG USA YUG dispute**: dispute 3551 FRN-GMY-UKG-USA-YUG 1992-07-16..1996-10-02 hihost 4 trigdate 1992-07-16, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 211: UNMAPPED
- 220: country.fra (registered state set)
- 230: UNMAPPED
- 235: UNMAPPED
- 255: country.deu (registered state set)
- 325: UNMAPPED (registered state set)
- 345: country.serbia
- 350: UNMAPPED
- 360: UNMAPPED (registered state set)
- 390: UNMAPPED (registered state set)
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.deu:unknown, country.serbia:unknown, country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Frn Gmy Ukg Usa Yug Dispute 1992` (https://history.state.gov/search?q=Frn+Gmy+Ukg+Usa+Yug+Dispute+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-06-16..1992-08-15. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3551_frn_gmy_ukg_usa_yug_dispute --approved-by joe`. The code never runs it.
