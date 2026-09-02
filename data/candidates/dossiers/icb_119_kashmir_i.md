# Dossier icb_119_kashmir_i — KASHMIR I

```json
{
 "id": "icb_119_kashmir_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:05+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 119,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=119",
  "trigdate": "1947-10-24",
  "termdate": "1949-01-01",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1947-10-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "target"
  },
  {
   "entity": "country.pak",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1947v03/d125",
  "title": "The Charg\u00e9 in India (Donovan) to the Secretary of State (1947, Volume III, The British Commonwealth; Europe)",
  "date": "1947-12-29",
  "window": [
   "1947-09-24",
   "1949-01-31"
  ],
  "query": "Kashmir I 1947",
  "search_url": "https://history.state.gov/search?q=Kashmir+I+1947&within=documents",
  "retrieved_at": "2026-09-02T19:13:04+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v08/d8",
    "title": "8. Telegram From the Department of State to the Embassy in Pakistan (1955\u20131957, Volume VIII, South Asia)",
    "page_date": "1955-07-27",
    "retrieved_at": "2026-09-02T19:13:04+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v03/d125",
    "title": "The Charg\u00e9 in India (Donovan) to the Secretary of State (1947, Volume III, The British Commonwealth; Europe)",
    "page_date": "1947-12-29",
    "retrieved_at": "2026-09-02T19:13:04+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 119 **KASHMIR I**: trigdate 1947-10-24, termdate 1949-01-01, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=119

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.india:target, country.pak:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:04+00:00: **The Chargé in India (Donovan) to the Secretary of State (1947, Volume III, The British Commonwealth; Europe)** — page date 1947-12-29 (window 1947-09-24..1949-01-31)
  https://history.state.gov/historicaldocuments/frus1947v03/d125
- search: https://history.state.gov/search?q=Kashmir+I+1947&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_119_kashmir_i --approved-by joe`. The code never runs it.
