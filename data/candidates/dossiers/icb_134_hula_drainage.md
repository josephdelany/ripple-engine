# Dossier icb_134_hula_drainage — HULA DRAINAGE

```json
{
 "id": "icb_134_hula_drainage",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 134,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=134",
  "trigdate": "1951-02-12",
  "termdate": "1951-05-15",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1951-02-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1951v05/d288",
  "title": "The Consul at Jerusalem (Tyler) to the Department of State (1951, Volume V, The Near East and Africa)",
  "date": "1951-03-05",
  "window": [
   "1951-01-13",
   "1951-06-14"
  ],
  "query": "Hula Drainage 1951",
  "search_url": "https://history.state.gov/search?q=Hula+Drainage+1951&within=documents",
  "retrieved_at": "2026-09-02T19:13:28+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1951v05/d288",
    "title": "The Consul at Jerusalem (Tyler) to the Department of State (1951, Volume V, The Near East and Africa)",
    "page_date": "1951-03-05",
    "retrieved_at": "2026-09-02T19:13:28+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 134 **HULA DRAINAGE**: trigdate 1951-02-12, termdate 1951-05-15, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=134

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.syr:target, country.israel:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:28+00:00: **The Consul at Jerusalem (Tyler) to the Department of State (1951, Volume V, The Near East and Africa)** — page date 1951-03-05 (window 1951-01-13..1951-06-14)
  https://history.state.gov/historicaldocuments/frus1951v05/d288
- search: https://history.state.gov/search?q=Hula+Drainage+1951&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_134_hula_drainage --approved-by joe`. The code never runs it.
