# Dossier icb_200_cuba_venezuela — CUBA/VENEZUELA

```json
{
 "id": "icb_200_cuba_venezuela",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:16+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 200,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=200",
  "trigdate": "1963-11-01",
  "termdate": "1963-12-01",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1963-11-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.venezuela",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v12/d170",
  "title": "170. Circular Telegram From the Department of State to Posts in the American Republics (1961\u20131963, Volume XII, American Republics)",
  "date": "1963-12-04",
  "window": [
   "1963-10-02",
   "1963-12-31"
  ],
  "query": "Cuba Venezuela 1963",
  "search_url": "https://history.state.gov/search?q=Cuba+Venezuela+1963&within=documents",
  "retrieved_at": "2026-09-02T19:15:16+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v10-12mSupp/d229",
    "title": "229. Circular airgram CA\u201310071 to Moscow, March 18 (1961\u20131963, Volumes X/XI/XII, Microfiche Supplement, American Republics; Cuba 1961\u20131962; Cuban Missile Crisis and Aftermath)",
    "page_date": "1963-03-18",
    "retrieved_at": "2026-09-02T19:15:14+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v31/d53",
    "title": "53. Memorandum From the President\u2019s Special Assistant (Rostow) to President Johnson (1964\u20131968, Volume XXXI, South and Central America; Mexico)",
    "page_date": "1967-05-12",
    "retrieved_at": "2026-09-02T19:15:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v32/d279",
    "title": "279. Editorial Note (1964\u20131968, Volume XXXII, Dominican Republic; Cuba; Haiti; Guyana)",
    "page_date": "1964-07-26",
    "retrieved_at": "2026-09-02T19:15:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v12/d170",
    "title": "170. Circular Telegram From the Department of State to Posts in the American Republics (1961\u20131963, Volume XII, American Republics)",
    "page_date": "1963-12-04",
    "retrieved_at": "2026-09-02T19:15:16+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 200 **CUBA/VENEZUELA**: trigdate 1963-11-01, termdate 1963-12-01, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=200

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 101: country.venezuela (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.venezuela:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:16+00:00: **170. Circular Telegram From the Department of State to Posts in the American Republics (1961–1963, Volume XII, American Republics)** — page date 1963-12-04 (window 1963-10-02..1963-12-31)
  https://history.state.gov/historicaldocuments/frus1961-63v12/d170
- search: https://history.state.gov/search?q=Cuba+Venezuela+1963&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_200_cuba_venezuela --approved-by joe`. The code never runs it.
