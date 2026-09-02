# Dossier icb_425_india_pakistan_nuclear_tests — INDIA/PAKISTAN NUCLEAR TESTS

```json
{
 "id": "icb_425_india_pakistan_nuclear_tests",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 425,
  "source": "icb",
  "source_id": "425",
  "detail": "INDIA/PAKISTAN NUCLEAR TESTS 1998-05-11..1998-06-11 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=425",
  "trigdate": "1998-05-11",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-05-11",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "India Pakistan Nuclear Tests 1998",
  "search_url": "https://history.state.gov/search?q=India+Pakistan+Nuclear+Tests+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-04-11",
   "1998-06-10"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:42+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 425 **INDIA/PAKISTAN NUCLEAR TESTS**: INDIA/PAKISTAN NUCLEAR TESTS 1998-05-11..1998-06-11 viol 1.0 trigdate 1998-05-11, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=425

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `India Pakistan Nuclear Tests 1998` (https://history.state.gov/search?q=India+Pakistan+Nuclear+Tests+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-04-11..1998-06-10. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_425_india_pakistan_nuclear_tests --approved-by joe`. The code never runs it.
