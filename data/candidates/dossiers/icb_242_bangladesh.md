# Dossier icb_242_bangladesh — BANGLADESH

```json
{
 "id": "icb_242_bangladesh",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:35+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 242,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=242",
  "trigdate": "1971-03-25",
  "termdate": "1971-12-17",
  "viol": 4,
  "forout": 5
 },
 "event_date": "1971-03-25",
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
 "unmapped_ccodes": [
  771
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v11/d77",
  "title": "77. Telegram From the Department of State to the Embassy in Pakistan (1969\u20131976, Volume XI, South Asia Crisis, 1971)",
  "date": "1971-06-22",
  "window": [
   "1971-02-23",
   "1972-01-16"
  ],
  "query": "Bangladesh 1971",
  "search_url": "https://history.state.gov/search?q=Bangladesh+1971&within=documents",
  "retrieved_at": "2026-09-02T19:16:35+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v11/d77",
    "title": "77. Telegram From the Department of State to the Embassy in Pakistan (1969\u20131976, Volume XI, South Asia Crisis, 1971)",
    "page_date": "1971-06-22",
    "retrieved_at": "2026-09-02T19:16:35+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 242 **BANGLADESH**: trigdate 1971-03-25, termdate 1971-12-17, viol 4, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=242

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak
- 771: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.india:target, country.pak:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:35+00:00: **77. Telegram From the Department of State to the Embassy in Pakistan (1969–1976, Volume XI, South Asia Crisis, 1971)** — page date 1971-06-22 (window 1971-02-23..1972-01-16)
  https://history.state.gov/historicaldocuments/frus1969-76v11/d77
- search: https://history.state.gov/search?q=Bangladesh+1971&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_242_bangladesh --approved-by joe`. The code never runs it.
