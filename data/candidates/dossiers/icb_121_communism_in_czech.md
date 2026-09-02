# Dossier icb_121_communism_in_czech — COMMUNISM IN CZECH.

```json
{
 "id": "icb_121_communism_in_czech",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:08+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 121,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=121",
  "trigdate": "1948-02-13",
  "termdate": "1948-02-25",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1948-02-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  315
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1948v04/d471",
  "title": "The Charg\u00e9 in Czechoslovakia (Bruins) to the Secretary of State (1948, Volume IV, Eastern Europe; The Soviet Union)",
  "date": "1948-01-28",
  "window": [
   "1948-01-14",
   "1948-03-26"
  ],
  "query": "Communism In Czech 1948",
  "search_url": "https://history.state.gov/search?q=Communism+In+Czech+1948&within=documents",
  "retrieved_at": "2026-09-02T19:13:07+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v04/d471",
    "title": "The Charg\u00e9 in Czechoslovakia (Bruins) to the Secretary of State (1948, Volume IV, Eastern Europe; The Soviet Union)",
    "page_date": "1948-01-28",
    "retrieved_at": "2026-09-02T19:13:07+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 121 **COMMUNISM IN CZECH.**: trigdate 1948-02-13, termdate 1948-02-25, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=121

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 315: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:07+00:00: **The Chargé in Czechoslovakia (Bruins) to the Secretary of State (1948, Volume IV, Eastern Europe; The Soviet Union)** — page date 1948-01-28 (window 1948-01-14..1948-03-26)
  https://history.state.gov/historicaldocuments/frus1948v04/d471
- search: https://history.state.gov/search?q=Communism+In+Czech+1948&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_121_communism_in_czech --approved-by joe`. The code never runs it.
