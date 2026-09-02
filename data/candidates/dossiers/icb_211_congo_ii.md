# Dossier icb_211_congo_ii — CONGO II

```json
{
 "id": "icb_211_congo_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:34+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 211,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=211",
  "trigdate": "1964-08-04",
  "termdate": "1964-12-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1964-08-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  211
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v23/d253",
  "title": "253. Paper Prepared in the Central Intelligence Agency (1964\u20131968, Volume XXIII, Congo, 1960\u20131968)",
  "date": "1964-09-10",
  "window": [
   "1964-07-05",
   "1965-01-27"
  ],
  "query": "Congo Ii 1964",
  "search_url": "https://history.state.gov/search?q=Congo+Ii+1964&within=documents",
  "retrieved_at": "2026-09-02T19:15:33+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v23/d253",
    "title": "253. Paper Prepared in the Central Intelligence Agency (1964\u20131968, Volume XXIII, Congo, 1960\u20131968)",
    "page_date": "1964-09-10",
    "retrieved_at": "2026-09-02T19:15:33+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 211 **CONGO II**: trigdate 1964-08-04, termdate 1964-12-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=211

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 211: UNMAPPED
- 365: country.russia (registered state set)
- 490: country.congo_drc

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.russia:unknown, country.congo_drc:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:33+00:00: **253. Paper Prepared in the Central Intelligence Agency (1964–1968, Volume XXIII, Congo, 1960–1968)** — page date 1964-09-10 (window 1964-07-05..1965-01-27)
  https://history.state.gov/historicaldocuments/frus1964-68v23/d253
- search: https://history.state.gov/search?q=Congo+Ii+1964&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_211_congo_ii --approved-by joe`. The code never runs it.
