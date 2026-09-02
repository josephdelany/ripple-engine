# Dossier icb_203_jordan_waters — JORDAN WATERS

```json
{
 "id": "icb_203_jordan_waters",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:21+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 203,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=203",
  "trigdate": "1963-12-11",
  "termdate": "1964-05-05",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1963-12-11",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "target"
  },
  {
   "entity": "country.syr",
   "role": "target"
  },
  {
   "entity": "country.lebanon",
   "role": "target"
  },
  {
   "entity": "country.jor",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d384",
  "title": "384. Telegram From the Department of State to the Embassy in Israel (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
  "date": "1963-12-09",
  "window": [
   "1963-11-11",
   "1964-06-04"
  ],
  "query": "Jordan Waters 1963",
  "search_url": "https://history.state.gov/search?q=Jordan+Waters+1963&within=documents",
  "retrieved_at": "2026-09-02T19:15:21+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d33",
    "title": "33. Memorandum From the Department of State Executive Secretary (Brubeck) to the President\u2019s Special Assistant for National Security Affairs (Bundy) (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
    "page_date": "1962-08-30",
    "retrieved_at": "2026-09-02T19:15:20+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d384",
    "title": "384. Telegram From the Department of State to the Embassy in Israel (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
    "page_date": "1963-12-09",
    "retrieved_at": "2026-09-02T19:15:21+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 203 **JORDAN WATERS**: trigdate 1963-12-11, termdate 1964-05-05, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=203

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 652: country.syr (registered state set)
- 660: country.lebanon (registered state set)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.egypt:target, country.syr:target, country.lebanon:target, country.jor:target, country.israel:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:21+00:00: **384. Telegram From the Department of State to the Embassy in Israel (1961–1963, Volume XVIII, Near East, 1962–1963)** — page date 1963-12-09 (window 1963-11-11..1964-06-04)
  https://history.state.gov/historicaldocuments/frus1961-63v18/d384
- search: https://history.state.gov/search?q=Jordan+Waters+1963&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_203_jordan_waters --approved-by joe`. The code never runs it.
