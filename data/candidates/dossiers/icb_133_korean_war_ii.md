# Dossier icb_133_korean_war_ii — KOREAN WAR II

```json
{
 "id": "icb_133_korean_war_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:27+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 133,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=133",
  "trigdate": "1950-09-28",
  "termdate": "1951-07-10",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1950-09-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.russia",
   "role": "target"
  },
  {
   "entity": "country.china",
   "role": "target"
  },
  {
   "entity": "country.south_korea",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1950v01/d38",
  "title": "The Charg\u00e9 in the Soviet Union (Barbour) to the Secretary of State (1950, Volume I, National Security Affairs; Foreign Economic Policy)",
  "date": "1950-10-26",
  "window": [
   "1950-08-29",
   "1951-08-09"
  ],
  "query": "Korean War Ii 1950",
  "search_url": "https://history.state.gov/search?q=Korean+War+Ii+1950&within=documents",
  "retrieved_at": "2026-09-02T19:13:27+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950-55Intel/d12",
    "title": "12. Editorial Note (The Intelligence Community, 1950\u20131955)",
    "page_date": "1950-06-25",
    "retrieved_at": "2026-09-02T19:13:24+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v15p1/d83",
    "title": "Memorandum by the Director of the Office of Northeast Asian Affairs (Young) to the Assistant Secretary of State for Far Eastern Affairs (Allison) (1952\u20131954, Volume XV, Part 1, Korea)",
    "page_date": "1952-04-04",
    "retrieved_at": "2026-09-02T19:13:25+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v15p1/d35",
    "title": "The Assistant Secretary of the Army for General Management (Bendetsen) to the Chairman, Senate Foreign Relations Committee (Connally) (1952\u20131954, Volume XV, Part 1, Korea)",
    "page_date": "1952-02-16",
    "retrieved_at": "2026-09-02T19:13:25+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950v07/d666",
    "title": "Memorandum by the Central Intelligence Agency (1950, Volume VII, Korea)",
    "page_date": "1950-06-24",
    "retrieved_at": "2026-09-02T19:13:26+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950v01/d38",
    "title": "The Charg\u00e9 in the Soviet Union (Barbour) to the Secretary of State (1950, Volume I, National Security Affairs; Foreign Economic Policy)",
    "page_date": "1950-10-26",
    "retrieved_at": "2026-09-02T19:13:27+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 133 **KOREAN WAR II**: trigdate 1950-09-28, termdate 1951-07-10, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=133

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 365: country.russia (registered state set)
- 710: country.china (registered state set)
- 731: UNMAPPED
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.russia:target, country.china:target, country.south_korea:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:27+00:00: **The Chargé in the Soviet Union (Barbour) to the Secretary of State (1950, Volume I, National Security Affairs; Foreign Economic Policy)** — page date 1950-10-26 (window 1950-08-29..1951-08-09)
  https://history.state.gov/historicaldocuments/frus1950v01/d38
- search: https://history.state.gov/search?q=Korean+War+Ii+1950&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_133_korean_war_ii --approved-by joe`. The code never runs it.
