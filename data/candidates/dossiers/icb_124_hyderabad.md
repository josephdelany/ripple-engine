# Dossier icb_124_hyderabad — HYDERABAD

```json
{
 "id": "icb_124_hyderabad",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:13+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 124,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=124",
  "trigdate": "1948-08-21",
  "termdate": "1948-09-18",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1948-08-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1948v05p1/d307",
  "title": "The Charg\u00e9 in India (Donovan) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)",
  "date": "1948-09-13",
  "window": [
   "1948-07-22",
   "1948-10-18"
  ],
  "query": "Hyderabad 1948",
  "search_url": "https://history.state.gov/search?q=Hyderabad+1948&within=documents",
  "retrieved_at": "2026-09-02T19:13:12+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v05p1/d307",
    "title": "The Charg\u00e9 in India (Donovan) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)",
    "page_date": "1948-09-13",
    "retrieved_at": "2026-09-02T19:13:12+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 124 **HYDERABAD**: trigdate 1948-08-21, termdate 1948-09-18, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=124

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:12+00:00: **The Chargé in India (Donovan) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)** — page date 1948-09-13 (window 1948-07-22..1948-10-18)
  https://history.state.gov/historicaldocuments/frus1948v05p1/d307
- search: https://history.state.gov/search?q=Hyderabad+1948&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_124_hyderabad --approved-by joe`. The code never runs it.
