# Dossier icb_330_gulf_of_syrte_i — GULF OF SYRTE I

```json
{
 "id": "icb_330_gulf_of_syrte_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:05+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 330,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=330",
  "trigdate": "1981-08-12",
  "termdate": "1981-09-01",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1981-08-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Gulf Of Syrte I 1981",
  "search_url": "https://history.state.gov/search?q=Gulf+Of+Syrte+I+1981&within=documents",
  "search_status": 200,
  "window": [
   "1981-07-13",
   "1981-10-01"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:05+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 330 **GULF OF SYRTE I**: trigdate 1981-08-12, termdate 1981-09-01, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=330

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.libya:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Gulf Of Syrte I 1981` (https://history.state.gov/search?q=Gulf+Of+Syrte+I+1981&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1981-07-13..1981-10-01.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_330_gulf_of_syrte_i --approved-by joe`. The code never runs it.
