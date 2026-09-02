# Dossier icb_209_yemen_war_ii — YEMEN WAR II

```json
{
 "id": "icb_209_yemen_war_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:29+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 209,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=209",
  "trigdate": "1964-05-28",
  "termdate": "1964-11-08",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1964-05-28",
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
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d347",
  "title": "347. Memorandum From Robert W. Komer of the National Security Council Staff to the President\u2019s Special Assistant for National Security Affairs (Bundy) (1964\u20131968, Volume XXI, Near East Region; Arabian",
  "date": "1964-08-24",
  "window": [
   "1964-04-28",
   "1964-12-08"
  ],
  "query": "Yemen War Ii 1964",
  "search_url": "https://history.state.gov/search?q=Yemen+War+Ii+1964&within=documents",
  "retrieved_at": "2026-09-02T19:15:28+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d347",
    "title": "347. Memorandum From Robert W. Komer of the National Security Council Staff to the President\u2019s Special Assistant for National Security Affairs (Bundy) (1964\u20131968, Volume XXI, Near East Region; Arabian",
    "page_date": "1964-08-24",
    "retrieved_at": "2026-09-02T19:15:28+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 209 **YEMEN WAR II**: trigdate 1964-05-28, termdate 1964-11-08, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=209

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 670: country.saudi_arabia (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown, country.saudi_arabia:unknown, country.yemen:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:28+00:00: **347. Memorandum From Robert W. Komer of the National Security Council Staff to the President’s Special Assistant for National Security Affairs (Bundy) (1964–1968, Volume XXI, Near East Region; Arabian** — page date 1964-08-24 (window 1964-04-28..1964-12-08)
  https://history.state.gov/historicaldocuments/frus1964-68v21/d347
- search: https://history.state.gov/search?q=Yemen+War+Ii+1964&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_209_yemen_war_ii --approved-by joe`. The code never runs it.
