# Dossier icb_256_oman_south_yemen — OMAN/SOUTH YEMEN

```json
{
 "id": "icb_256_oman_south_yemen",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:05+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 256,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=256",
  "trigdate": "1973-11-18",
  "termdate": "1976-03-11",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1973-11-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.omn",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d213",
  "title": "213. Memorandum of Conversation (1969\u20131976, Volume E\u20139, Part 2, Documents on the Middle East Region, 1973\u20131976)",
  "date": "1975-01-09",
  "window": [
   "1973-10-19",
   "1976-04-10"
  ],
  "query": "Oman South Yemen 1973",
  "search_url": "https://history.state.gov/search?q=Oman+South+Yemen+1973&within=documents",
  "retrieved_at": "2026-09-02T19:17:05+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d197",
    "title": "197. Information Memorandum From the Assistant Secretary of State for Near Eastern and South Asian Affairs (Sisco) to the Deputy Secretary of State (Rush) (1969\u20131976, Volume E\u20139, Part 2, Documents on ",
    "page_date": "1973-03-29",
    "retrieved_at": "2026-09-02T19:17:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d200",
    "title": "200. Memorandum From Harold Saunders of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u20139, Part 2, Documents on the Midd",
    "page_date": "1973-06-27",
    "retrieved_at": "2026-09-02T19:16:41+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d205",
    "title": "205. Special National Intelligence Estimate Prepared in the Central Intelligence Agency (1969\u20131976, Volume E\u20139, Part 2, Documents on the Middle East Region, 1973\u20131976)",
    "page_date": "1973-10-01",
    "retrieved_at": "2026-09-02T19:17:04+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d213",
    "title": "213. Memorandum of Conversation (1969\u20131976, Volume E\u20139, Part 2, Documents on the Middle East Region, 1973\u20131976)",
    "page_date": "1975-01-09",
    "retrieved_at": "2026-09-02T19:17:05+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 256 **OMAN/SOUTH YEMEN**: trigdate 1973-11-18, termdate 1976-03-11, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=256

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 698: country.omn (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.omn:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:05+00:00: **213. Memorandum of Conversation (1969–1976, Volume E–9, Part 2, Documents on the Middle East Region, 1973–1976)** — page date 1975-01-09 (window 1973-10-19..1976-04-10)
  https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d213
- search: https://history.state.gov/search?q=Oman+South+Yemen+1973&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_256_oman_south_yemen --approved-by joe`. The code never runs it.
