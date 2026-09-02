# Dossier icb_295_beagle_channel_ii — BEAGLE CHANNEL II

```json
{
 "id": "icb_295_beagle_channel_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:05+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 295,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=295",
  "trigdate": "1978-10-16",
  "termdate": "1979-01-08",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1978-10-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.chile",
   "role": "target"
  },
  {
   "entity": "country.argentina",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Beagle Channel Ii 1978",
  "search_url": "https://history.state.gov/search?q=Beagle+Channel+Ii+1978&within=documents",
  "search_status": 200,
  "window": [
   "1978-09-16",
   "1979-02-07"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d84",
    "title": "84. Memorandum From Robert Pastor of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Brzezinski) and the President\u2019s Deputy Assistant for National Secur",
    "page_date": "1978-08-09",
    "retrieved_at": "2026-09-02T19:17:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d111",
    "title": "111. Memorandum From Acting Secretary of State Christopher to President Carter (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1980-06-14",
    "retrieved_at": "2026-09-02T19:18:02+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d96",
    "title": "96. Memorandum From the Assistant Secretary of State for Inter-American Affairs (Vaky) to the Executive Secretary of the Department of State (Tarnoff) (1977\u20131980, Volume XXIV, South America; Latin Ame",
    "page_date": "1979-02-13",
    "retrieved_at": "2026-09-02T19:18:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v13/d1",
    "title": "1. Airgram From the Embassy in Argentina to the Department of State (1981\u20131988, Volume XIII, Conflict in the South Atlantic, 1981\u20131984)",
    "page_date": "1979-05-16",
    "retrieved_at": "2026-09-02T19:18:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d109",
    "title": "109. Paper Prepared in the Department of State (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1980-05-12",
    "retrieved_at": "2026-09-02T19:18:04+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d50",
    "title": "50. Memorandum From Robert Pastor of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Brzezinski) (1977\u20131980, Volume XXIV, South America; Latin America R",
    "page_date": "1980-10-29",
    "retrieved_at": "2026-09-02T19:18:05+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:01+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 295 **BEAGLE CHANNEL II**: trigdate 1978-10-16, termdate 1979-01-08, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=295

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 155: country.chile
- 160: country.argentina (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.chile:target, country.argentina:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Beagle Channel Ii 1978` (https://history.state.gov/search?q=Beagle+Channel+Ii+1978&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1978-09-16..1979-02-07.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 84. Memorandum From Robert Pastor of the National Security C (1978-08-09); 111. Memorandum From Acting Secretary of State Christopher t (1980-06-14); 96. Memorandum From the Assistant Secretary of State for Int (1979-02-13); 1. Airgram From the Embassy in Argentina to the Department o (1979-05-16); 109. Paper Prepared in the Department of State (1977–1980, V (1980-05-12); 50. Memorandum From Robert Pastor of the National Security C (1980-10-29)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_295_beagle_channel_ii --approved-by joe`. The code never runs it.
