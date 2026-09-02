# Dossier ucdp_11545_government_of_somalia_vs_republic_of_som — Government of Somalia vs Republic of Somaliland

```json
{
 "id": "ucdp_11545_government_of_somalia_vs_republic_of_som",
 "built_by": "session A",
 "built_at": "2026-09-02T21:06:49+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "11545",
  "detail": "dyad 11545 Government of Somalia vs Republic of Somaliland (Somalia) onset 2018-05-15 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2018-05-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2018-05-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520
 ],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "http://www.somalilandpress.com/the-aggression-of-federal-somalia-against-somaliland-republic/",
  "title": "The Aggression of Federal Somalia against Somaliland Republic",
  "date": "2018-05-17",
  "domain": "somalilandpress.com",
  "window": [
   "2018-05-12",
   "2018-06-14"
  ],
  "query": "Somalia Republic Somaliland",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Somalia+Republic+Somaliland&mode=artlist&format=json&maxrecords=25&startdatetime=20180512000000&enddatetime=20180614235959",
  "retrieved_at": "2026-09-02T21:06:48+00:00",
  "opened": [
   {
    "url": "http://www.somalilandpress.com/the-aggression-of-federal-somalia-against-somaliland-republic/",
    "title": "The Aggression of Federal Somalia against Somaliland Republic",
    "page_date": "2018-05-17",
    "domain": "somalilandpress.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 11545 **Government of Somalia vs Republic of Somaliland**: dyad 11545 Government of Somalia vs Republic of Somaliland (Somalia) onset 2018-05-15 intensity 1 trigdate 2018-05-15, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T21:06:48+00:00: **The Aggression of Federal Somalia against Somaliland Republic** — page date 2018-05-17 (window 2018-05-12..2018-06-14)
  http://www.somalilandpress.com/the-aggression-of-federal-somalia-against-somaliland-republic/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=Somalia+Republic+Somaliland&mode=artlist&format=json&maxrecords=25&startdatetime=20180512000000&enddatetime=20180614235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_11545_government_of_somalia_vs_republic_of_som --approved-by joe`. The code never runs it.
