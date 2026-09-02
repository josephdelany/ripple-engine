# Dossier icb_493_venezuelan_election — VENEZUELAN ELECTION

```json
{
 "id": "icb_493_venezuelan_election",
 "built_by": "session A",
 "built_at": "2026-09-02T21:07:18+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 493,
  "source": "icb",
  "source_id": "493",
  "detail": "VENEZUELAN ELECTION 2019-01-23..2019-05-10 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=493",
  "trigdate": "2019-01-23",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2019-01-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.venezuela",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://www.voanews.com/a/doctors-demand-humanitarian-aid-be-allowed-into-venezuela/4781181.html",
  "title": "Venezuela Guaido Blasts Government Aid Blockade",
  "date": "2019-02-11",
  "domain": "voanews.com",
  "window": [
   "2019-01-20",
   "2019-02-22"
  ],
  "query": "VENEZUELAN ELECTION Venezuela",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=VENEZUELAN+ELECTION+Venezuela&mode=artlist&format=json&maxrecords=25&startdatetime=20190120000000&enddatetime=20190222235959",
  "retrieved_at": "2026-09-02T20:36:47+00:00",
  "opened": [
   {
    "url": "https://www.voanews.com/a/doctors-demand-humanitarian-aid-be-allowed-into-venezuela/4781181.html",
    "title": "Venezuela Guaido Blasts Government Aid Blockade",
    "page_date": "2019-02-11",
    "domain": "voanews.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 493 **VENEZUELAN ELECTION**: VENEZUELAN ELECTION 2019-01-23..2019-05-10 viol 1.0 trigdate 2019-01-23, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=493

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 101: country.venezuela (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.venezuela:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:36:47+00:00: **Venezuela Guaido Blasts Government Aid Blockade** — page date 2019-02-11 (window 2019-01-20..2019-02-22)
  https://www.voanews.com/a/doctors-demand-humanitarian-aid-be-allowed-into-venezuela/4781181.html
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=VENEZUELAN+ELECTION+Venezuela&mode=artlist&format=json&maxrecords=25&startdatetime=20190120000000&enddatetime=20190222235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_493_venezuelan_election --approved-by joe`. The code never runs it.
