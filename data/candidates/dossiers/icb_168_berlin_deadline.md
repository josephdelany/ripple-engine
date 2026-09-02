# Dossier icb_168_berlin_deadline — BERLIN DEADLINE

```json
{
 "id": "icb_168_berlin_deadline",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 168,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=168",
  "trigdate": "1958-11-27",
  "termdate": "1959-09-15",
  "viol": 1,
  "forout": 1
 },
 "event_date": "1958-11-27",
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
   "entity": "country.gbr",
   "role": "target"
  },
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.russia",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  260,
  265
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1958-60v08/d100",
  "title": "100. Telegram From the Department of State to the Embassy in Germany (1958\u20131960, Volume VIII, Berlin Crisis, 1958\u20131959)",
  "date": "1958-12-11",
  "window": [
   "1958-10-28",
   "1959-10-15"
  ],
  "query": "Berlin Deadline 1958",
  "search_url": "https://history.state.gov/search?q=Berlin+Deadline+1958&within=documents",
  "retrieved_at": "2026-09-02T19:14:21+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v08/d100",
    "title": "100. Telegram From the Department of State to the Embassy in Germany (1958\u20131960, Volume VIII, Berlin Crisis, 1958\u20131959)",
    "page_date": "1958-12-11",
    "retrieved_at": "2026-09-02T19:14:21+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 168 **BERLIN DEADLINE**: trigdate 1958-11-27, termdate 1959-09-15, viol 1, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=168

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 260: UNMAPPED (registered state set)
- 265: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.gbr:target, country.fra:target, country.russia:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:21+00:00: **100. Telegram From the Department of State to the Embassy in Germany (1958–1960, Volume VIII, Berlin Crisis, 1958–1959)** — page date 1958-12-11 (window 1958-10-28..1959-10-15)
  https://history.state.gov/historicaldocuments/frus1958-60v08/d100
- search: https://history.state.gov/search?q=Berlin+Deadline+1958&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_168_berlin_deadline --approved-by joe`. The code never runs it.
