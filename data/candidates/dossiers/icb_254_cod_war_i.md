# Dossier icb_254_cod_war_i — COD WAR I

```json
{
 "id": "icb_254_cod_war_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 254,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=254",
  "trigdate": "1973-05-14",
  "termdate": "1973-11-13",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1973-05-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  395
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve03/d11",
  "title": "11. Analytical Study OPR\u20133 Prepared by the Central Intelligence Agency (1969\u20131976, Volume E\u20133, Documents on Global Issues, 1973\u20131976)",
  "date": "1973-09-04",
  "window": [
   "1973-04-14",
   "1973-12-13"
  ],
  "query": "Cod War I 1973",
  "search_url": "https://history.state.gov/search?q=Cod+War+I+1973&within=documents",
  "retrieved_at": "2026-09-02T19:17:00+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve15p2/d186",
    "title": "186. Telegram 1209 From the Embassy in Iceland to the Department of State (1969\u20131976, Volume E\u201315, Part 2, Documents on Western Europe, 1973\u20131976)",
    "page_date": "1974-09-03",
    "retrieved_at": "2026-09-02T19:16:59+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve15p2Ed2/d186",
    "title": "186. Telegram 1209 From the Embassy in Iceland to the Department of State (1969\u20131976, Volume E\u201315, Part 2, Documents on Western Europe, 1973\u20131976, Second, Revised Edition)",
    "page_date": "1974-09-03",
    "retrieved_at": "2026-09-02T19:17:00+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve03/d11",
    "title": "11. Analytical Study OPR\u20133 Prepared by the Central Intelligence Agency (1969\u20131976, Volume E\u20133, Documents on Global Issues, 1973\u20131976)",
    "page_date": "1973-09-04",
    "retrieved_at": "2026-09-02T19:17:00+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 254 **COD WAR I**: trigdate 1973-05-14, termdate 1973-11-13, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=254

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 395: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:00+00:00: **11. Analytical Study OPR–3 Prepared by the Central Intelligence Agency (1969–1976, Volume E–3, Documents on Global Issues, 1973–1976)** — page date 1973-09-04 (window 1973-04-14..1973-12-13)
  https://history.state.gov/historicaldocuments/frus1969-76ve03/d11
- search: https://history.state.gov/search?q=Cod+War+I+1973&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_254_cod_war_i --approved-by joe`. The code never runs it.
