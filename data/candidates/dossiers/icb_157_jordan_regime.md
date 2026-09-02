# Dossier icb_157_jordan_regime — JORDAN REGIME

```json
{
 "id": "icb_157_jordan_regime",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:10+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 157,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=157",
  "trigdate": "1957-04-04",
  "termdate": "1957-05-03",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1957-04-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v17/d278",
  "title": "278. Editorial Note (1955\u20131957, Volume XVII, Arab-Israeli Dispute, 1957)",
  "date": "1957-03-08",
  "window": [
   "1957-03-05",
   "1957-06-02"
  ],
  "query": "Jordan Regime 1957",
  "search_url": "https://history.state.gov/search?q=Jordan+Regime+1957&within=documents",
  "retrieved_at": "2026-09-02T19:14:09+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v17/d278",
    "title": "278. Editorial Note (1955\u20131957, Volume XVII, Arab-Israeli Dispute, 1957)",
    "page_date": "1957-03-08",
    "retrieved_at": "2026-09-02T19:14:09+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 157 **JORDAN REGIME**: trigdate 1957-04-04, termdate 1957-05-03, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=157

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.jor:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:09+00:00: **278. Editorial Note (1955–1957, Volume XVII, Arab-Israeli Dispute, 1957)** — page date 1957-03-08 (window 1957-03-05..1957-06-02)
  https://history.state.gov/historicaldocuments/frus1955-57v17/d278
- search: https://history.state.gov/search?q=Jordan+Regime+1957&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_157_jordan_regime --approved-by joe`. The code never runs it.
