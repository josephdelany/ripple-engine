# Dossier icb_141_e_german_uprising — E. GERMAN UPRISING

```json
{
 "id": "icb_141_e_german_uprising",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:43+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 141,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=141",
  "trigdate": "1953-06-17",
  "termdate": "1953-07-11",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1953-06-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1952-54v07p2/d715",
  "title": "No. 715Memorandum of Discussion at the 150th Meeting of the National Security Council, Thursday, June 18, 1953 (1952\u20131954, Volume VII, Part 2, Germany and Austria)",
  "date": "1953-06-18",
  "window": [
   "1953-05-18",
   "1953-08-10"
  ],
  "query": "E  German Uprising 1953",
  "search_url": "https://history.state.gov/search?q=E++German+Uprising+1953&within=documents",
  "retrieved_at": "2026-09-02T19:13:43+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v26/d235",
    "title": "235. Report Prepared by the Operations Coordinating Board (1955\u20131957, Volume XXVI, Central and Southeastern Europe)",
    "page_date": "1957-07-17",
    "retrieved_at": "2026-09-02T19:13:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v26/d231",
    "title": "231. Report by the Operations Coordinating Board (1955\u20131957, Volume XXVI, Central and Southeastern Europe)",
    "page_date": "1956-12-05",
    "retrieved_at": "2026-09-02T19:13:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v07p2/d715",
    "title": "No. 715Memorandum of Discussion at the 150th Meeting of the National Security Council, Thursday, June 18, 1953 (1952\u20131954, Volume VII, Part 2, Germany and Austria)",
    "page_date": "1953-06-18",
    "retrieved_at": "2026-09-02T19:13:43+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 141 **E. GERMAN UPRISING**: trigdate 1953-06-17, termdate 1953-07-11, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=141

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:43+00:00: **No. 715Memorandum of Discussion at the 150th Meeting of the National Security Council, Thursday, June 18, 1953 (1952–1954, Volume VII, Part 2, Germany and Austria)** — page date 1953-06-18 (window 1953-05-18..1953-08-10)
  https://history.state.gov/historicaldocuments/frus1952-54v07p2/d715
- search: https://history.state.gov/search?q=E++German+Uprising+1953&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_141_e_german_uprising --approved-by joe`. The code never runs it.
