# Dossier icb_337_war_in_lebanon — WAR IN LEBANON

```json
{
 "id": "icb_337_war_in_lebanon",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:18+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 337,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=337",
  "trigdate": "1982-06-05",
  "termdate": "1983-05-17",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1982-06-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "target"
  },
  {
   "entity": "country.lebanon",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d300",
  "title": "300. Memorandum From the President\u2019s Assistant for National Security Affairs (Clark) to President Reagan (1981\u20131988, Volume XXIV, North Africa)",
  "date": "1982-06-24",
  "window": [
   "1982-05-06",
   "1983-06-16"
  ],
  "query": "War In Lebanon 1982",
  "search_url": "https://history.state.gov/search?q=War+In+Lebanon+1982&within=documents",
  "retrieved_at": "2026-09-02T19:19:18+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d300",
    "title": "300. Memorandum From the President\u2019s Assistant for National Security Affairs (Clark) to President Reagan (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1982-06-24",
    "retrieved_at": "2026-09-02T19:19:18+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 337 **WAR IN LEBANON**: trigdate 1982-06-05, termdate 1983-05-17, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=337

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)
- 660: country.lebanon (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.syr:target, country.lebanon:target, country.israel:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:18+00:00: **300. Memorandum From the President’s Assistant for National Security Affairs (Clark) to President Reagan (1981–1988, Volume XXIV, North Africa)** — page date 1982-06-24 (window 1982-05-06..1983-06-16)
  https://history.state.gov/historicaldocuments/frus1981-88v24/d300
- search: https://history.state.gov/search?q=War+In+Lebanon+1982&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_337_war_in_lebanon --approved-by joe`. The code never runs it.
