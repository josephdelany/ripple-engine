# Dossier icb_181_bay_of_pigs — BAY OF PIGS

```json
{
 "id": "icb_181_bay_of_pigs",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:42+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 181,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=181",
  "trigdate": "1961-04-15",
  "termdate": "1961-04-24",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1961-04-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  40
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v10/d177",
  "title": "177. Editorial Note (1961\u20131963, Volume X, Cuba, January 1961\u2013September 1962)",
  "date": "1961-04-26",
  "window": [
   "1961-03-16",
   "1961-05-24"
  ],
  "query": "Bay Of Pigs 1961",
  "search_url": "https://history.state.gov/search?q=Bay+Of+Pigs+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:42+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v10/d177",
    "title": "177. Editorial Note (1961\u20131963, Volume X, Cuba, January 1961\u2013September 1962)",
    "page_date": "1961-04-26",
    "retrieved_at": "2026-09-02T19:14:42+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 181 **BAY OF PIGS**: trigdate 1961-04-15, termdate 1961-04-24, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=181

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 40: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:42+00:00: **177. Editorial Note (1961–1963, Volume X, Cuba, January 1961–September 1962)** — page date 1961-04-26 (window 1961-03-16..1961-05-24)
  https://history.state.gov/historicaldocuments/frus1961-63v10/d177
- search: https://history.state.gov/search?q=Bay+Of+Pigs+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_181_bay_of_pigs --approved-by joe`. The code never runs it.
