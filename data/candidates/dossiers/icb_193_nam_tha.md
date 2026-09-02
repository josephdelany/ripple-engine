# Dossier icb_193_nam_tha — NAM THA

```json
{
 "id": "icb_193_nam_tha",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:03+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 193,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=193",
  "trigdate": "1962-05-06",
  "termdate": "1962-06-12",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1962-05-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.thailand",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d350",
  "title": "350. Special National Intelligence Estimate (1961\u20131963, Volume XXIV, Laos Crisis)",
  "date": "1962-05-09",
  "window": [
   "1962-04-06",
   "1962-07-12"
  ],
  "query": "Nam Tha 1962",
  "search_url": "https://history.state.gov/search?q=Nam+Tha+1962&within=documents",
  "retrieved_at": "2026-09-02T19:15:03+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d290",
    "title": "290. Telegram From the Department of State to the Embassy in Laos (1961\u20131963, Volume XXIV, Laos Crisis)",
    "page_date": "1962-02-06",
    "retrieved_at": "2026-09-02T19:15:02+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d350",
    "title": "350. Special National Intelligence Estimate (1961\u20131963, Volume XXIV, Laos Crisis)",
    "page_date": "1962-05-09",
    "retrieved_at": "2026-09-02T19:15:03+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 193 **NAM THA**: trigdate 1962-05-06, termdate 1962-06-12, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=193

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 800: country.thailand

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.thailand:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:03+00:00: **350. Special National Intelligence Estimate (1961–1963, Volume XXIV, Laos Crisis)** — page date 1962-05-09 (window 1962-04-06..1962-07-12)
  https://history.state.gov/historicaldocuments/frus1961-63v24/d350
- search: https://history.state.gov/search?q=Nam+Tha+1962&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_193_nam_tha --approved-by joe`. The code never runs it.
