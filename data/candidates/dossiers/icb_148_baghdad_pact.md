# Dossier icb_148_baghdad_pact — BAGHDAD PACT

```json
{
 "id": "icb_148_baghdad_pact",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:00+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 148,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=148",
  "trigdate": "1955-02-24",
  "termdate": "1955-10-28",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1955-02-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v12/d73",
  "title": "73. Telegram From the Department of State to the Embassy in Jordan (1955\u20131957, Volume XII, Near East Region; Iran; Iraq)",
  "date": "1955-10-28",
  "window": [
   "1955-01-25",
   "1955-11-27"
  ],
  "query": "Baghdad Pact 1955",
  "search_url": "https://history.state.gov/search?q=Baghdad+Pact+1955&within=documents",
  "retrieved_at": "2026-09-02T19:13:59+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v12/d142",
    "title": "142. Telegram From the Embassy in Iraq to the Department of State (1955\u20131957, Volume XII, Near East Region; Iran; Iraq)",
    "page_date": "1956-11-15",
    "retrieved_at": "2026-09-02T19:13:59+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v12/d73",
    "title": "73. Telegram From the Department of State to the Embassy in Jordan (1955\u20131957, Volume XII, Near East Region; Iran; Iraq)",
    "page_date": "1955-10-28",
    "retrieved_at": "2026-09-02T19:13:59+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 148 **BAGHDAD PACT**: trigdate 1955-02-24, termdate 1955-10-28, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=148

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:59+00:00: **73. Telegram From the Department of State to the Embassy in Jordan (1955–1957, Volume XII, Near East Region; Iran; Iraq)** — page date 1955-10-28 (window 1955-01-25..1955-11-27)
  https://history.state.gov/historicaldocuments/frus1955-57v12/d73
- search: https://history.state.gov/search?q=Baghdad+Pact+1955&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_148_baghdad_pact --approved-by joe`. The code never runs it.
