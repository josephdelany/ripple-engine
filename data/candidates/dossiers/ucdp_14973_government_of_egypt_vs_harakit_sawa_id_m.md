# Dossier ucdp_14973_government_of_egypt_vs_harakit_sawa_id_m — Government of Egypt vs Harakit Sawa'id Misr

```json
{
 "id": "ucdp_14973_government_of_egypt_vs_harakit_sawa_id_m",
 "built_by": "session A",
 "built_at": "2026-09-02T21:00:00+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "14973",
  "detail": "dyad 14973 Government of Egypt vs Harakit Sawa'id Misr (Egypt) onset 2017-07-14 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2017-07-14",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2017-07-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "GDELT DOC 2.0",
  "query": "Egypt Harakit Sawa",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Egypt+Harakit+Sawa&mode=artlist&format=json&maxrecords=25&startdatetime=20170711000000&enddatetime=20170813235959",
  "search_status": 200,
  "window": [
   "2017-07-11",
   "2017-08-13"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:00:00+00:00",
  "note": "",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 14973 **Government of Egypt vs Harakit Sawa'id Misr**: dyad 14973 Government of Egypt vs Harakit Sawa'id Misr (Egypt) onset 2017-07-14 intensity 1 trigdate 2017-07-14, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** GDELT DOC 2.0 search `Egypt Harakit Sawa` (https://api.gdeltproject.org/api/v2/doc/doc?query=Egypt+Harakit+Sawa&mode=artlist&format=json&maxrecords=25&startdatetime=20170711000000&enddatetime=20170813235959, HTTP 200) returned 0 document(s) opened, none dated inside 2017-07-11..2017-08-13. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_14973_government_of_egypt_vs_harakit_sawa_id_m --approved-by joe`. The code never runs it.
