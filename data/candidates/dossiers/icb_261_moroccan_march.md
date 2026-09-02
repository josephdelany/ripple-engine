# Dossier icb_261_moroccan_march — MOROCCAN MARCH

```json
{
 "id": "icb_261_moroccan_march",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:14+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 261,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=261",
  "trigdate": "1975-10-16",
  "termdate": "1976-04-14",
  "viol": 3,
  "forout": 6
 },
 "event_date": "1975-10-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  230,
  435,
  600
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d109",
  "title": "109. Memorandum From Director of Central Intelligence Colby to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u20139, Part 1, Documents on North Africa, 1973\u20131976)",
  "date": "1975-11-08",
  "window": [
   "1975-09-16",
   "1976-05-14"
  ],
  "query": "Moroccan March 1975",
  "search_url": "https://history.state.gov/search?q=Moroccan+March+1975&within=documents",
  "retrieved_at": "2026-09-02T19:17:14+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d109",
    "title": "109. Memorandum From Director of Central Intelligence Colby to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u20139, Part 1, Documents on North Africa, 1973\u20131976)",
    "page_date": "1975-11-08",
    "retrieved_at": "2026-09-02T19:17:14+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 261 **MOROCCAN MARCH**: trigdate 1975-10-16, termdate 1976-04-14, viol 3, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=261

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 230: UNMAPPED
- 435: UNMAPPED
- 600: UNMAPPED
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:14+00:00: **109. Memorandum From Director of Central Intelligence Colby to the President’s Assistant for National Security Affairs (Kissinger) (1969–1976, Volume E–9, Part 1, Documents on North Africa, 1973–1976)** — page date 1975-11-08 (window 1975-09-16..1976-05-14)
  https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d109
- search: https://history.state.gov/search?q=Moroccan+March+1975&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_261_moroccan_march --approved-by joe`. The code never runs it.
