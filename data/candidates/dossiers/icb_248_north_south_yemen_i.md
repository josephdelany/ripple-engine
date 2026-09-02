# Dossier icb_248_north_south_yemen_i — NORTH/SOUTH YEMEN I

```json
{
 "id": "icb_248_north_south_yemen_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:42+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 248,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=248",
  "trigdate": "1972-09-26",
  "termdate": "1972-11-28",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1972-09-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  680
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d197",
  "title": "197. Telegram From the Embassy in Saudi Arabia to the Department of State (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
  "date": "1972-11-07",
  "window": [
   "1972-08-27",
   "1972-12-28"
  ],
  "query": "North South Yemen I 1972",
  "search_url": "https://history.state.gov/search?q=North+South+Yemen+I+1972&within=documents",
  "retrieved_at": "2026-09-02T19:16:41+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d193",
    "title": "193. Telegram From Secretary of State Rogers to the Department of State (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
    "page_date": "1972-07-03",
    "retrieved_at": "2026-09-02T19:16:40+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d200",
    "title": "200. Memorandum From Harold Saunders of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u20139, Part 2, Documents on the Midd",
    "page_date": "1973-06-27",
    "retrieved_at": "2026-09-02T19:16:41+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d197",
    "title": "197. Telegram From the Embassy in Saudi Arabia to the Department of State (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
    "page_date": "1972-11-07",
    "retrieved_at": "2026-09-02T19:16:41+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 248 **NORTH/SOUTH YEMEN I**: trigdate 1972-09-26, termdate 1972-11-28, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=248

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 678: country.yemen (registered state set)
- 680: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.yemen:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:41+00:00: **197. Telegram From the Embassy in Saudi Arabia to the Department of State (1969–1976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969–1972; Jordan, September 1970)** — page date 1972-11-07 (window 1972-08-27..1972-12-28)
  https://history.state.gov/historicaldocuments/frus1969-76v24/d197
- search: https://history.state.gov/search?q=North+South+Yemen+I+1972&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_248_north_south_yemen_i --approved-by joe`. The code never runs it.
