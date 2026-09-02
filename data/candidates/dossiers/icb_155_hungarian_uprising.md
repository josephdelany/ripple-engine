# Dossier icb_155_hungarian_uprising — HUNGARIAN UPRISING

```json
{
 "id": "icb_155_hungarian_uprising",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:08+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 155,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=155",
  "trigdate": "1956-10-23",
  "termdate": "1957-01-01",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1956-10-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.hungary",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v09/d201",
  "title": "201. Memorandum of Discussion at the 303d Meeting of the National Security Council, Washington, November 8, 1956 (1955\u20131957, Volume IX, Foreign Economic Policy; Foreign Information Program)",
  "date": "1956-11-08",
  "window": [
   "1956-09-23",
   "1957-01-31"
  ],
  "query": "Hungarian Uprising 1956",
  "search_url": "https://history.state.gov/search?q=Hungarian+Uprising+1956&within=documents",
  "retrieved_at": "2026-09-02T19:14:08+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v25/d280",
    "title": "280. Telegram From the Department of State to the Mission at the United Nations (1955\u20131957, Volume XXV, Eastern Europe)",
    "page_date": "1957-12-27",
    "retrieved_at": "2026-09-02T19:14:06+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v25/d255",
    "title": "255. Editorial Note (1955\u20131957, Volume XXV, Eastern Europe)",
    "page_date": "1957-05-27",
    "retrieved_at": "2026-09-02T19:14:07+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v09/d201",
    "title": "201. Memorandum of Discussion at the 303d Meeting of the National Security Council, Washington, November 8, 1956 (1955\u20131957, Volume IX, Foreign Economic Policy; Foreign Information Program)",
    "page_date": "1956-11-08",
    "retrieved_at": "2026-09-02T19:14:08+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 155 **HUNGARIAN UPRISING**: trigdate 1956-10-23, termdate 1957-01-01, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=155

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 310: country.hungary
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.hungary:unknown, country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:08+00:00: **201. Memorandum of Discussion at the 303d Meeting of the National Security Council, Washington, November 8, 1956 (1955–1957, Volume IX, Foreign Economic Policy; Foreign Information Program)** — page date 1956-11-08 (window 1956-09-23..1957-01-31)
  https://history.state.gov/historicaldocuments/frus1955-57v09/d201
- search: https://history.state.gov/search?q=Hungarian+Uprising+1956&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_155_hungarian_uprising --approved-by joe`. The code never runs it.
