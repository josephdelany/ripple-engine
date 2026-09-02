# Dossier icb_417_aegean_sea_iv — AEGEAN SEA IV

```json
{
 "id": "icb_417_aegean_sea_iv",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 417,
  "source": "icb",
  "source_id": "417",
  "detail": "AEGEAN SEA IV 1996-01-26..1996-01-28 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=417",
  "trigdate": "1996-01-26",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-01-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  350
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Aegean Sea Iv 1996",
  "search_url": "https://history.state.gov/search?q=Aegean+Sea+Iv+1996&within=documents",
  "search_status": 200,
  "window": [
   "1995-12-27",
   "1996-02-25"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1919Parisv07/d23",
    "title": "Notes of a Meeting of the Heads of Delegations of the Five Great Powers Held in M. Pichon\u2019s Room at the Quai d\u2019Orsay, Paris, on Tuesday, July 29, 1919, at 3:30 p.m. (1919, Volume VII, The Paris Peace ",
    "page_date": "1919-07-29",
    "retrieved_at": "2026-09-02T19:55:07+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:55:06+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 417 **AEGEAN SEA IV**: AEGEAN SEA IV 1996-01-26..1996-01-28 viol 1.0 trigdate 1996-01-26, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=417

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 350: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Aegean Sea Iv 1996` (https://history.state.gov/search?q=Aegean+Sea+Iv+1996&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1995-12-27..1996-02-25. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: Notes of a Meeting of the Heads of Delegations of the Five G (1919-07-29)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_417_aegean_sea_iv --approved-by joe`. The code never runs it.
