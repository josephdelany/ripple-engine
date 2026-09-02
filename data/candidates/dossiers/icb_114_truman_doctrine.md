# Dossier icb_114_truman_doctrine — TRUMAN DOCTRINE

```json
{
 "id": "icb_114_truman_doctrine",
 "built_by": "session A",
 "built_at": "2026-09-02T19:12:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 114,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=114",
  "trigdate": "1947-02-21",
  "termdate": "1947-05-22",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1947-02-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.turkey",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [
  350
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1947v01/d378",
  "title": "Editorial Note (1947, Volume I, General; The United Nations)",
  "date": "1947-04-02",
  "window": [
   "1947-01-22",
   "1947-06-21"
  ],
  "query": "Truman Doctrine 1947",
  "search_url": "https://history.state.gov/search?q=Truman+Doctrine+1947&within=documents",
  "retrieved_at": "2026-09-02T19:11:11+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v01/d134",
    "title": "134. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to President Carter (1977\u20131980, Volume I, Foundations of Foreign Policy)",
    "page_date": "1980-01-02",
    "retrieved_at": "2026-09-02T19:11:09+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d127",
    "title": "127. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to President Carter (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1980-01-02",
    "retrieved_at": "2026-09-02T19:11:10+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v03/d428",
    "title": "The Ambassador in Denmark (Marvel) to the Secretary of State (1947, Volume III, The British Commonwealth; Europe)",
    "page_date": "1947-07-22",
    "retrieved_at": "2026-09-02T19:11:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v01/d378",
    "title": "Editorial Note (1947, Volume I, General; The United Nations)",
    "page_date": "1947-04-02",
    "retrieved_at": "2026-09-02T19:11:11+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 114 **TRUMAN DOCTRINE**: trigdate 1947-02-21, termdate 1947-05-22, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=114

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 350: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.turkey:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:11:11+00:00: **Editorial Note (1947, Volume I, General; The United Nations)** — page date 1947-04-02 (window 1947-01-22..1947-06-21)
  https://history.state.gov/historicaldocuments/frus1947v01/d378
- search: https://history.state.gov/search?q=Truman+Doctrine+1947&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_114_truman_doctrine --approved-by joe`. The code never runs it.
