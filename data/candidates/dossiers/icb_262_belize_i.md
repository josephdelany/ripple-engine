# Dossier icb_262_belize_i — BELIZE I

```json
{
 "id": "icb_262_belize_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:17+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 262,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=262",
  "trigdate": "1975-11-01",
  "termdate": "1975-11-28",
  "viol": 1,
  "forout": 2
 },
 "event_date": "1975-11-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve11p1/d208",
  "title": "208. Telegram 15823 From the Embassy in the United Kingdom to the Department of State (1969\u20131976, Volume E\u201311, Part 1, Documents on Mexico; Central America; and the Caribbean, 1973\u20131976)",
  "date": "1975-10-15",
  "window": [
   "1975-10-02",
   "1975-12-28"
  ],
  "query": "Belize I 1975",
  "search_url": "https://history.state.gov/search?q=Belize+I+1975&within=documents",
  "retrieved_at": "2026-09-02T19:17:16+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve11p1/d201",
    "title": "201. Telegram 595 From the Consulate General in Belize to the Department of State (1969\u20131976, Volume E\u201311, Part 1, Documents on Mexico; Central America; and the Caribbean, 1973\u20131976)",
    "page_date": "1975-09-12",
    "retrieved_at": "2026-09-02T19:17:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve11p1/d208",
    "title": "208. Telegram 15823 From the Embassy in the United Kingdom to the Department of State (1969\u20131976, Volume E\u201311, Part 1, Documents on Mexico; Central America; and the Caribbean, 1973\u20131976)",
    "page_date": "1975-10-15",
    "retrieved_at": "2026-09-02T19:17:16+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 262 **BELIZE I**: trigdate 1975-11-01, termdate 1975-11-28, viol 1, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=262

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:16+00:00: **208. Telegram 15823 From the Embassy in the United Kingdom to the Department of State (1969–1976, Volume E–11, Part 1, Documents on Mexico; Central America; and the Caribbean, 1973–1976)** — page date 1975-10-15 (window 1975-10-02..1975-12-28)
  https://history.state.gov/historicaldocuments/frus1969-76ve11p1/d208
- search: https://history.state.gov/search?q=Belize+I+1975&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_262_belize_i --approved-by joe`. The code never runs it.
