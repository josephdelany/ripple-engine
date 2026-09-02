# Dossier icb_214_rann_of_kutch — RANN OF KUTCH

```json
{
 "id": "icb_214_rann_of_kutch",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:43+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 214,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=214",
  "trigdate": "1965-04-08",
  "termdate": "1965-06-28",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1965-04-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
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
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v25/d111",
  "title": "111. Telegram From the Embassy in Pakistan to the Department of State (1964\u20131968, Volume XXV, South Asia)",
  "date": "1965-04-27",
  "window": [
   "1965-03-09",
   "1965-07-28"
  ],
  "query": "Rann Of Kutch 1965",
  "search_url": "https://history.state.gov/search?q=Rann+Of+Kutch+1965&within=documents",
  "retrieved_at": "2026-09-02T19:15:42+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v25/d111",
    "title": "111. Telegram From the Embassy in Pakistan to the Department of State (1964\u20131968, Volume XXV, South Asia)",
    "page_date": "1965-04-27",
    "retrieved_at": "2026-09-02T19:15:42+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 214 **RANN OF KUTCH**: trigdate 1965-04-08, termdate 1965-06-28, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=214

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.india:target, country.pak:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:42+00:00: **111. Telegram From the Embassy in Pakistan to the Department of State (1964–1968, Volume XXV, South Asia)** — page date 1965-04-27 (window 1965-03-09..1965-07-28)
  https://history.state.gov/historicaldocuments/frus1964-68v25/d111
- search: https://history.state.gov/search?q=Rann+Of+Kutch+1965&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_214_rann_of_kutch --approved-by joe`. The code never runs it.
