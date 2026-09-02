# Dossier icb_363_gulf_of_syrte_ii — GULF OF SYRTE II

```json
{
 "id": "icb_363_gulf_of_syrte_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 363,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=363",
  "trigdate": "1986-03-24",
  "termdate": "1986-04-21",
  "viol": 2,
  "forout": 6
 },
 "event_date": "1986-03-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "actor"
  },
  {
   "entity": "country.libya",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Gulf Of Syrte Ii 1986",
  "search_url": "https://history.state.gov/search?q=Gulf+Of+Syrte+Ii+1986&within=documents",
  "search_status": 200,
  "window": [
   "1986-02-22",
   "1986-05-21"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:46+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 363 **GULF OF SYRTE II**: trigdate 1986-03-24, termdate 1986-04-21, viol 2, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=363

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:actor, country.libya:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Gulf Of Syrte Ii 1986` (https://history.state.gov/search?q=Gulf+Of+Syrte+Ii+1986&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-02-22..1986-05-21.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_363_gulf_of_syrte_ii --approved-by joe`. The code never runs it.
