# Dossier ucdp_15333_government_of_libya_vs_pfll — Government of Libya vs PFLL

```json
{
 "id": "ucdp_15333_government_of_libya_vs_pfll",
 "built_by": "session A",
 "built_at": "2026-09-02T21:01:35+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "15333",
  "detail": "dyad 15333 Government of Libya vs PFLL (Libya) onset 2017-11-08 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2017-11-08",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2017-11-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "GDELT DOC 2.0",
  "query": "Libya PFLL",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Libya+PFLL&mode=artlist&format=json&maxrecords=25&startdatetime=20171105000000&enddatetime=20171208235959",
  "search_status": 200,
  "window": [
   "2017-11-05",
   "2017-12-08"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:01:34+00:00",
  "note": "",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 15333 **Government of Libya vs PFLL**: dyad 15333 Government of Libya vs PFLL (Libya) onset 2017-11-08 intensity 1 trigdate 2017-11-08, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** GDELT DOC 2.0 search `Libya PFLL` (https://api.gdeltproject.org/api/v2/doc/doc?query=Libya+PFLL&mode=artlist&format=json&maxrecords=25&startdatetime=20171105000000&enddatetime=20171208235959, HTTP 200) returned 0 document(s) opened, none dated inside 2017-11-05..2017-12-08. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_15333_government_of_libya_vs_pfll --approved-by joe`. The code never runs it.
