# Dossier icb_342_chad_libya_vi — CHAD/LIBYA VI

```json
{
 "id": "icb_342_chad_libya_vi",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:26+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 342,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=342",
  "trigdate": "1983-06-24",
  "termdate": "1984-12-11",
  "viol": 2,
  "forout": 2
 },
 "event_date": "1983-06-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.libya",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d139",
  "title": "139. Action Memorandum From the Chairman of the Policy Planning Council (Bosworth) to Secretary of State Shultz (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
  "date": "1983-11-22",
  "window": [
   "1983-05-25",
   "1985-01-10"
  ],
  "query": "Chad Libya Vi 1983",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Vi+1983&within=documents",
  "retrieved_at": "2026-09-02T19:19:25+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d139",
    "title": "139. Action Memorandum From the Chairman of the Policy Planning Council (Bosworth) to Secretary of State Shultz (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
    "page_date": "1983-11-22",
    "retrieved_at": "2026-09-02T19:19:25+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 342 **CHAD/LIBYA VI**: trigdate 1983-06-24, termdate 1984-12-11, viol 2, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=342

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.fra:target, country.libya:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:25+00:00: **139. Action Memorandum From the Chairman of the Policy Planning Council (Bosworth) to Secretary of State Shultz (1981–1988, Volume IV, Soviet Union, January 1983–March 1985)** — page date 1983-11-22 (window 1983-05-25..1985-01-10)
  https://history.state.gov/historicaldocuments/frus1981-88v04/d139
- search: https://history.state.gov/search?q=Chad+Libya+Vi+1983&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_342_chad_libya_vi --approved-by joe`. The code never runs it.
