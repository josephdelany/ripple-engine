# Dossier icb_212_yemen_war_iii — YEMEN WAR III

```json
{
 "id": "icb_212_yemen_war_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:39+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 212,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=212",
  "trigdate": "1964-12-03",
  "termdate": "1965-08-25",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1964-12-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Yemen War Iii 1964",
  "search_url": "https://history.state.gov/search?q=Yemen+War+Iii+1964&within=documents",
  "search_status": 200,
  "window": [
   "1964-11-03",
   "1965-09-24"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d382",
    "title": "382. Memorandum of Conversation (1964\u20131968, Volume XXI, Near East Region; Arabian Peninsula)",
    "page_date": "1965-10-19",
    "retrieved_at": "2026-09-02T19:15:35+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d182",
    "title": "182. Special National Intelligence Estimate (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
    "page_date": "1971-02-11",
    "retrieved_at": "2026-09-02T19:15:36+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d321",
    "title": "321. Memorandum From the Department of State Executive Secretary (Read) to the President\u2019s Special Assistant for National Security Affairs (Bundy) (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
    "page_date": "1963-09-06",
    "retrieved_at": "2026-09-02T19:15:36+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v18/d308",
    "title": "308. Memorandum of Conversation (1964\u20131968, Volume XVIII, Arab-Israeli Dispute, 1964\u20131967)",
    "page_date": "1966-07-13",
    "retrieved_at": "2026-09-02T19:15:37+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v18/d25",
    "title": "25. Telegram From the Embassy in the United Arab Republic to the Department of State (1964\u20131968, Volume XVIII, Arab-Israeli Dispute, 1964\u20131967)",
    "page_date": "1964-03-04",
    "retrieved_at": "2026-09-02T19:15:38+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d20",
    "title": "20. Memorandum From Harold H. Saunders of the National Security Council Staff to the President\u2019s Special Assistant (Rostow) (1964\u20131968, Volume XXI, Near East Region; Arabian Peninsula)",
    "page_date": "1967-05-16",
    "retrieved_at": "2026-09-02T19:15:39+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:15:34+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 212 **YEMEN WAR III**: trigdate 1964-12-03, termdate 1965-08-25, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=212

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 670: country.saudi_arabia (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown, country.saudi_arabia:unknown, country.yemen:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Yemen War Iii 1964` (https://history.state.gov/search?q=Yemen+War+Iii+1964&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1964-11-03..1965-09-24.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 382. Memorandum of Conversation (1964–1968, Volume XXI, Near (1965-10-19); 182. Special National Intelligence Estimate (1969–1976, Volu (1971-02-11); 321. Memorandum From the Department of State Executive Secre (1963-09-06); 308. Memorandum of Conversation (1964–1968, Volume XVIII, Ar (1966-07-13); 25. Telegram From the Embassy in the United Arab Republic to (1964-03-04); 20. Memorandum From Harold H. Saunders of the National Secur (1967-05-16)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_212_yemen_war_iii --approved-by joe`. The code never runs it.
