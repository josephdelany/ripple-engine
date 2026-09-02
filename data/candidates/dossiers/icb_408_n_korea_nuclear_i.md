# Dossier icb_408_n_korea_nuclear_i — N. KOREA NUCLEAR I

```json
{
 "id": "icb_408_n_korea_nuclear_i",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 408,
  "source": "icb",
  "source_id": "408",
  "detail": "N. KOREA NUCLEAR I 1993-03-28..1994-10-21 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=408",
  "trigdate": "1993-03-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-03-28",
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
   "entity": "country.south_korea",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "N  Korea Nuclear I 1993",
  "search_url": "https://history.state.gov/search?q=N++Korea+Nuclear+I+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-02-26",
   "1993-04-27"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v44p1/d193",
    "title": "193. Memorandum From Acting Director of Central Intelligence Gates to the President\u2019s Assistant for National Security Affairs (Carlucci) (1981\u20131988, Volume XLIV, Part 1, National Security Policy, 1985",
    "page_date": "1987-01-15",
    "retrieved_at": "2026-09-02T19:54:18+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:54:17+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 408 **N. KOREA NUCLEAR I**: N. KOREA NUCLEAR I 1993-03-28..1994-10-21 viol 1.0 trigdate 1993-03-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=408

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 731: UNMAPPED
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.south_korea:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `N  Korea Nuclear I 1993` (https://history.state.gov/search?q=N++Korea+Nuclear+I+1993&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1993-02-26..1993-04-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 193. Memorandum From Acting Director of Central Intelligence (1987-01-15)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_408_n_korea_nuclear_i --approved-by joe`. The code never runs it.
