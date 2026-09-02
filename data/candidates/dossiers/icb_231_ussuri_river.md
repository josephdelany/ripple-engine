# Dossier icb_231_ussuri_river — USSURI RIVER

```json
{
 "id": "icb_231_ussuri_river",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:16+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 231,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=231",
  "trigdate": "1969-03-02",
  "termdate": "1969-10-20",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1969-03-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "target"
  },
  {
   "entity": "country.china",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v34/d62",
  "title": "62. Editorial Note (1969\u20131976, Volume XXXIV, National Security Policy, 1969\u20131972)",
  "date": "1969-08-14",
  "window": [
   "1969-01-31",
   "1969-11-19"
  ],
  "query": "Ussuri River 1969",
  "search_url": "https://history.state.gov/search?q=Ussuri+River+1969&within=documents",
  "retrieved_at": "2026-09-02T19:16:16+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v34/d62",
    "title": "62. Editorial Note (1969\u20131976, Volume XXXIV, National Security Policy, 1969\u20131972)",
    "page_date": "1969-08-14",
    "retrieved_at": "2026-09-02T19:16:16+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 231 **USSURI RIVER**: trigdate 1969-03-02, termdate 1969-10-20, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=231

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 710: country.china (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.russia:target, country.china:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:16+00:00: **62. Editorial Note (1969–1976, Volume XXXIV, National Security Policy, 1969–1972)** — page date 1969-08-14 (window 1969-01-31..1969-11-19)
  https://history.state.gov/historicaldocuments/frus1969-76v34/d62
- search: https://history.state.gov/search?q=Ussuri+River+1969&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_231_ussuri_river --approved-by joe`. The code never runs it.
