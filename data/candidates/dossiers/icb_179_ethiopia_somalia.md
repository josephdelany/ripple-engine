# Dossier icb_179_ethiopia_somalia — ETHIOPIA/SOMALIA

```json
{
 "id": "icb_179_ethiopia_somalia",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:37+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 179,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=179",
  "trigdate": "1960-12-26",
  "termdate": "1961-01-01",
  "viol": 3,
  "forout": 7
 },
 "event_date": "1960-12-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Ethiopia Somalia 1960",
  "search_url": "https://history.state.gov/search?q=Ethiopia+Somalia+1960&within=documents",
  "search_status": 200,
  "window": [
   "1960-11-26",
   "1961-01-31"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v14/d48",
    "title": "48. Telegram From the Department of State to the Embassy in Italy (1958\u20131960, Volume XIV, Africa)",
    "page_date": "1960-04-15",
    "retrieved_at": "2026-09-02T19:14:33+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v07p2/d272",
    "title": "272. Memorandum of Conversation (1958\u20131960, Volume VII, Part 2, Western Europe)",
    "page_date": "1960-04-14",
    "retrieved_at": "2026-09-02T19:14:34+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v24/d320",
    "title": "320. Memorandum of Conversation (1964\u20131968, Volume XXIV, Africa)",
    "page_date": "1966-10-17",
    "retrieved_at": "2026-09-02T19:14:35+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v21/d281",
    "title": "281. Telegram From the Department of State to the Embassy in Ethiopia (1961\u20131963, Volume XXI, Africa)",
    "page_date": "1962-11-17",
    "retrieved_at": "2026-09-02T19:14:36+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v14/d49",
    "title": "49. National Intelligence Estimate (1958\u20131960, Volume XIV, Africa)",
    "page_date": "1960-06-21",
    "retrieved_at": "2026-09-02T19:14:36+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v21/d304",
    "title": "304. Editorial Note (1961\u20131963, Volume XXI, Africa)",
    "page_date": "1963-10-16",
    "retrieved_at": "2026-09-02T19:14:37+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:14:33+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 179 **ETHIOPIA/SOMALIA**: trigdate 1960-12-26, termdate 1961-01-01, viol 3, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=179

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ethiopia Somalia 1960` (https://history.state.gov/search?q=Ethiopia+Somalia+1960&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1960-11-26..1961-01-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 48. Telegram From the Department of State to the Embassy in  (1960-04-15); 272. Memorandum of Conversation (1958–1960, Volume VII, Part (1960-04-14); 320. Memorandum of Conversation (1964–1968, Volume XXIV, Afr (1966-10-17); 281. Telegram From the Department of State to the Embassy in (1962-11-17); 49. National Intelligence Estimate (1958–1960, Volume XIV, A (1960-06-21); 304. Editorial Note (1961–1963, Volume XXI, Africa) (1963-10-16)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_179_ethiopia_somalia --approved-by joe`. The code never runs it.
