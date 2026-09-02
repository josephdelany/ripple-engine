# Dossier icb_224_pueblo — PUEBLO

```json
{
 "id": "icb_224_pueblo",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:57+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 224,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=224",
  "trigdate": "1968-01-21",
  "termdate": "1968-12-23",
  "viol": 2,
  "forout": 5
 },
 "event_date": "1968-01-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.south_korea",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v29p1/d249",
  "title": "249. Telegram From the Joint Intelligence Committee to the Central Intelligence Agency (1964\u20131968, Volume XXIX, Part 1, Korea)",
  "date": "1968-01-31",
  "window": [
   "1967-12-22",
   "1969-01-22"
  ],
  "query": "Pueblo 1968",
  "search_url": "https://history.state.gov/search?q=Pueblo+1968&within=documents",
  "retrieved_at": "2026-09-02T19:15:57+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v29p1/d249",
    "title": "249. Telegram From the Joint Intelligence Committee to the Central Intelligence Agency (1964\u20131968, Volume XXIX, Part 1, Korea)",
    "page_date": "1968-01-31",
    "retrieved_at": "2026-09-02T19:15:57+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 224 **PUEBLO**: trigdate 1968-01-21, termdate 1968-12-23, viol 2, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=224

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 731: UNMAPPED
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.south_korea:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:57+00:00: **249. Telegram From the Joint Intelligence Committee to the Central Intelligence Agency (1964–1968, Volume XXIX, Part 1, Korea)** — page date 1968-01-31 (window 1967-12-22..1969-01-22)
  https://history.state.gov/historicaldocuments/frus1964-68v29p1/d249
- search: https://history.state.gov/search?q=Pueblo+1968&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_224_pueblo --approved-by joe`. The code never runs it.
