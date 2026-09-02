# Dossier icb_232_war_of_attrition — WAR OF ATTRITION

```json
{
 "id": "icb_232_war_of_attrition",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:18+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 232,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=232",
  "trigdate": "1969-03-08",
  "termdate": "1970-08-07",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1969-03-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "actor"
  },
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v23/d51",
  "title": "51. Memorandum From the President\u2019s Assistant for National Security Affairs (Kissinger) to President Nixon (1969\u20131976, Volume XXIII, Arab-Israeli Dispute, 1969\u20131972)",
  "date": "1969-09-25",
  "window": [
   "1969-02-06",
   "1970-09-06"
  ],
  "query": "War Of Attrition 1969",
  "search_url": "https://history.state.gov/search?q=War+Of+Attrition+1969&within=documents",
  "retrieved_at": "2026-09-02T19:16:18+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v23/d51",
    "title": "51. Memorandum From the President\u2019s Assistant for National Security Affairs (Kissinger) to President Nixon (1969\u20131976, Volume XXIII, Arab-Israeli Dispute, 1969\u20131972)",
    "page_date": "1969-09-25",
    "retrieved_at": "2026-09-02T19:16:18+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 232 **WAR OF ATTRITION**: trigdate 1969-03-08, termdate 1970-08-07, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=232

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 651: country.egypt (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.russia:target, country.egypt:actor, country.israel:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:18+00:00: **51. Memorandum From the President’s Assistant for National Security Affairs (Kissinger) to President Nixon (1969–1976, Volume XXIII, Arab-Israeli Dispute, 1969–1972)** — page date 1969-09-25 (window 1969-02-06..1970-09-06)
  https://history.state.gov/historicaldocuments/frus1969-76v23/d51
- search: https://history.state.gov/search?q=War+Of+Attrition+1969&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_232_war_of_attrition --approved-by joe`. The code never runs it.
