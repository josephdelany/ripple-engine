# Dossier icb_140_korean_war_iii — KOREAN WAR III

```json
{
 "id": "icb_140_korean_war_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:40+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 140,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=140",
  "trigdate": "1953-04-16",
  "termdate": "1953-07-27",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1953-04-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
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
   "entity": "country.south_korea",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Korean War Iii 1953",
  "search_url": "https://history.state.gov/search?q=Korean+War+Iii+1953&within=documents",
  "search_status": 200,
  "window": [
   "1953-03-17",
   "1953-08-26"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v15p2/d824",
    "title": "The Secretary of Defense (Wilson) to the Secretary of State (1952\u20131954, Volume XV, Part 2, Korea)",
    "page_date": "1953-12-23",
    "retrieved_at": "2026-09-02T19:13:37+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v29p1/d98",
    "title": "98. Intelligence Memorandum (1964\u20131968, Volume XXIX, Part 1, Korea)",
    "page_date": "1966-11-08",
    "retrieved_at": "2026-09-02T19:13:38+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v23p2/d235",
    "title": "235. Memorandum of a Conversation Between the Korean Ambassador (Yang) and the Assistant Secretary of State for Far Eastern Affairs (Robertson), Department of State, Washington, July 26, 1957 (1955\u201319",
    "page_date": "1957-07-26",
    "retrieved_at": "2026-09-02T19:13:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1951v01/d57",
    "title": "Memorandum by the Director of the Policy Planning Staff (Nitze) to the Secretary of State (1951, Volume I, National Security Affairs; Foreign Economic Policy)",
    "page_date": "1951-10-17",
    "retrieved_at": "2026-09-02T19:13:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1951v01/d52",
    "title": "Memorandum for the National Security Council by the Acting Executive Secretary (Gleason) (1951, Volume I, National Security Affairs; Foreign Economic Policy)",
    "page_date": "1951-10-12",
    "retrieved_at": "2026-09-02T19:13:40+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:13:37+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 140 **KOREAN WAR III**: trigdate 1953-04-16, termdate 1953-07-27, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=140

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 710: country.china (registered state set)
- 731: UNMAPPED
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.china:unknown, country.south_korea:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Korean War Iii 1953` (https://history.state.gov/search?q=Korean+War+Iii+1953&within=documents, HTTP 200) returned 5 document(s) opened, none dated inside 1953-03-17..1953-08-26.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Secretary of Defense (Wilson) to the Secretary of State  (1953-12-23); 98. Intelligence Memorandum (1964–1968, Volume XXIX, Part 1, (1966-11-08); 235. Memorandum of a Conversation Between the Korean Ambassa (1957-07-26); Memorandum by the Director of the Policy Planning Staff (Nit (1951-10-17); Memorandum for the National Security Council by the Acting E (1951-10-12)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_140_korean_war_iii --approved-by joe`. The code never runs it.
