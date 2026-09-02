# Dossier icb_115_marshall_plan — MARSHALL PLAN

```json
{
 "id": "icb_115_marshall_plan",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:00+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 115,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=115",
  "trigdate": "1947-07-03",
  "termdate": "1947-07-11",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1947-07-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [
  315
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1947v06/d533",
  "title": "The Secretary of State to General of the Army Douglas MacArthur, at Tokyo (1947, Volume VI, The Far East)",
  "date": "1947-07-07",
  "window": [
   "1947-06-03",
   "1947-08-10"
  ],
  "query": "Marshall Plan 1947",
  "search_url": "https://history.state.gov/search?q=Marshall+Plan+1947&within=documents",
  "retrieved_at": "2026-09-02T19:12:59+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d94",
    "title": "94. Memorandum From the Acting Assistant Secretary of State for Administration (Peurifoy) to the Under Secretary of State (Acheson) and Secretary of State Marshall (Emergence of the Intelligence Estab",
    "page_date": "1947-01-31",
    "retrieved_at": "2026-09-02T19:12:58+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1946v10/d398",
    "title": "Lieutenant General Alvan C. Gillem, Jr., to Colonel George V. Underwood, at Nanking (1946, Volume X, The Far East: China)",
    "page_date": "1946-09-29",
    "retrieved_at": "2026-09-02T19:12:59+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v06/d533",
    "title": "The Secretary of State to General of the Army Douglas MacArthur, at Tokyo (1947, Volume VI, The Far East)",
    "page_date": "1947-07-07",
    "retrieved_at": "2026-09-02T19:12:59+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 115 **MARSHALL PLAN**: trigdate 1947-07-03, termdate 1947-07-11, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=115

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 315: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:12:59+00:00: **The Secretary of State to General of the Army Douglas MacArthur, at Tokyo (1947, Volume VI, The Far East)** — page date 1947-07-07 (window 1947-06-03..1947-08-10)
  https://history.state.gov/historicaldocuments/frus1947v06/d533
- search: https://history.state.gov/search?q=Marshall+Plan+1947&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_115_marshall_plan --approved-by joe`. The code never runs it.
