# Dossier icb_132_korean_war_i — KOREAN WAR I

```json
{
 "id": "icb_132_korean_war_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:23+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 132,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=132",
  "trigdate": "1950-06-25",
  "termdate": "1950-09-28",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1950-06-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
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
   "entity": "country.taiwan",
   "role": "unknown"
  },
  {
   "entity": "country.south_korea",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1950v06/d731",
  "title": "Memorandum by the Consultant to the Secretary (Dulles) to the Secretary of State (1950, Volume VI, East Asia and the Pacific)",
  "date": "1950-07-19",
  "window": [
   "1950-05-26",
   "1950-10-28"
  ],
  "query": "Korean War I 1950",
  "search_url": "https://history.state.gov/search?q=Korean+War+I+1950&within=documents",
  "retrieved_at": "2026-09-02T19:13:22+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950v06/d731",
    "title": "Memorandum by the Consultant to the Secretary (Dulles) to the Secretary of State (1950, Volume VI, East Asia and the Pacific)",
    "page_date": "1950-07-19",
    "retrieved_at": "2026-09-02T19:13:22+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 132 **KOREAN WAR I**: trigdate 1950-06-25, termdate 1950-09-28, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=132

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 710: country.china (registered state set)
- 713: country.taiwan
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.china:unknown, country.taiwan:unknown, country.south_korea:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:22+00:00: **Memorandum by the Consultant to the Secretary (Dulles) to the Secretary of State (1950, Volume VI, East Asia and the Pacific)** — page date 1950-07-19 (window 1950-05-26..1950-10-28)
  https://history.state.gov/historicaldocuments/frus1950v06/d731
- search: https://history.state.gov/search?q=Korean+War+I+1950&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_132_korean_war_i --approved-by joe`. The code never runs it.
