# Dossier icb_146_taiwan_strait_i — TAIWAN STRAIT I

```json
{
 "id": "icb_146_taiwan_strait_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:57+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 146,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=146",
  "trigdate": "1954-08-28",
  "termdate": "1955-04-23",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1954-08-28",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.taiwan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v02/d151",
  "title": "151. Letter From the Ambassador in the Republic of China (Rankin) to the Assistant Secretary of State for Far Eastern Affairs (Robertson) (1955\u20131957, Volume II, China)",
  "date": "1955-03-13",
  "window": [
   "1954-07-29",
   "1955-05-23"
  ],
  "query": "Taiwan Strait I 1954",
  "search_url": "https://history.state.gov/search?q=Taiwan+Strait+I+1954&within=documents",
  "retrieved_at": "2026-09-02T19:13:57+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v30/d318",
    "title": "318. Telegram From the Department of State to the Embassy in the Republic of China (1964\u20131968, Volume XXX, China)",
    "page_date": "1968-07-12",
    "retrieved_at": "2026-09-02T19:13:54+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v03/d107",
    "title": "107. Telegram From the Ambassador in the Republic of China (Rankin) to the Department of State (1955\u20131957, Volume III, China)",
    "page_date": "1955-11-29",
    "retrieved_at": "2026-09-02T19:13:55+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v22/d4",
    "title": "4. Memorandum From the Assistant Secretary of State for Far Eastern Affairs (Parsons) to Secretary of State Rusk (1961\u20131963, Volume XXII, Northeast Asia)",
    "page_date": "1961-02-19",
    "retrieved_at": "2026-09-02T19:13:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v30/d273",
    "title": "273. Memorandum From the Republic of China Country Director (Bennett) to the Deputy Assistant Secretary of State for East Asian and Pacific Affairs (Berger) (1964\u20131968, Volume XXX, China)",
    "page_date": "1967-07-11",
    "retrieved_at": "2026-09-02T19:13:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v02/d151",
    "title": "151. Letter From the Ambassador in the Republic of China (Rankin) to the Assistant Secretary of State for Far Eastern Affairs (Robertson) (1955\u20131957, Volume II, China)",
    "page_date": "1955-03-13",
    "retrieved_at": "2026-09-02T19:13:57+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 146 **TAIWAN STRAIT I**: trigdate 1954-08-28, termdate 1955-04-23, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=146

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 710: country.china (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.china:unknown, country.taiwan:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:57+00:00: **151. Letter From the Ambassador in the Republic of China (Rankin) to the Assistant Secretary of State for Far Eastern Affairs (Robertson) (1955–1957, Volume II, China)** — page date 1955-03-13 (window 1954-07-29..1955-05-23)
  https://history.state.gov/historicaldocuments/frus1955-57v02/d151
- search: https://history.state.gov/search?q=Taiwan+Strait+I+1954&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_146_taiwan_strait_i --approved-by joe`. The code never runs it.
