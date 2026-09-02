# Dossier icb_154_poland_liberalization — POLAND LIBERALIZATION

```json
{
 "id": "icb_154_poland_liberalization",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:05+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 154,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=154",
  "trigdate": "1956-10-15",
  "termdate": "1956-10-22",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1956-10-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  290
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v25/d89",
  "title": "89. Telegram From the Embassy in Poland to the Department of State (1955\u20131957, Volume XXV, Eastern Europe)",
  "date": "1956-09-21",
  "window": [
   "1956-09-15",
   "1956-11-21"
  ],
  "query": "Poland Liberalization 1956",
  "search_url": "https://history.state.gov/search?q=Poland+Liberalization+1956&within=documents",
  "retrieved_at": "2026-09-02T19:14:05+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v25/d89",
    "title": "89. Telegram From the Embassy in Poland to the Department of State (1955\u20131957, Volume XXV, Eastern Europe)",
    "page_date": "1956-09-21",
    "retrieved_at": "2026-09-02T19:14:05+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 154 **POLAND LIBERALIZATION**: trigdate 1956-10-15, termdate 1956-10-22, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=154

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 290: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:05+00:00: **89. Telegram From the Embassy in Poland to the Department of State (1955–1957, Volume XXV, Eastern Europe)** — page date 1956-09-21 (window 1956-09-15..1956-11-21)
  https://history.state.gov/historicaldocuments/frus1955-57v25/d89
- search: https://history.state.gov/search?q=Poland+Liberalization+1956&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_154_poland_liberalization --approved-by joe`. The code never runs it.
