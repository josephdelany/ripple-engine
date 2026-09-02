# Dossier icb_259_mayaguez — MAYAGUEZ

```json
{
 "id": "icb_259_mayaguez",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:08+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 259,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=259",
  "trigdate": "1975-05-12",
  "termdate": "1975-05-15",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1975-05-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  811
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v10/d300",
  "title": "300. Message From the Commander in Chief, Pacific (Gayler) to the Joint Chiefs of Staff (1969\u20131976, Volume X, Vietnam, January 1973\u2013July 1975)",
  "date": "1975-05-15",
  "window": [
   "1975-04-12",
   "1975-06-14"
  ],
  "query": "Mayaguez 1975",
  "search_url": "https://history.state.gov/search?q=Mayaguez+1975&within=documents",
  "retrieved_at": "2026-09-02T19:17:08+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v10/d300",
    "title": "300. Message From the Commander in Chief, Pacific (Gayler) to the Joint Chiefs of Staff (1969\u20131976, Volume X, Vietnam, January 1973\u2013July 1975)",
    "page_date": "1975-05-15",
    "retrieved_at": "2026-09-02T19:17:08+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 259 **MAYAGUEZ**: trigdate 1975-05-12, termdate 1975-05-15, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=259

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 811: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:08+00:00: **300. Message From the Commander in Chief, Pacific (Gayler) to the Joint Chiefs of Staff (1969–1976, Volume X, Vietnam, January 1973–July 1975)** — page date 1975-05-15 (window 1975-04-12..1975-06-14)
  https://history.state.gov/historicaldocuments/frus1969-76v10/d300
- search: https://history.state.gov/search?q=Mayaguez+1975&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_259_mayaguez --approved-by joe`. The code never runs it.
