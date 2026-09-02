# Dossier icb_418_oprn_grapes_of_wrath — OPRN GRAPES OF WRATH

```json
{
 "id": "icb_418_oprn_grapes_of_wrath",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 418,
  "source": "icb",
  "source_id": "418",
  "detail": "OPRN GRAPES OF WRATH 1996-04-09..1996-04-27 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=418",
  "trigdate": "1996-04-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-04-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.lebanon",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Oprn Grapes Of Wrath 1996",
  "search_url": "https://history.state.gov/search?q=Oprn+Grapes+Of+Wrath+1996&within=documents",
  "search_status": 200,
  "window": [
   "1996-03-10",
   "1996-05-09"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:10+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 418 **OPRN GRAPES OF WRATH**: OPRN GRAPES OF WRATH 1996-04-09..1996-04-27 viol 2.0 trigdate 1996-04-09, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=418

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.lebanon:unknown, country.israel:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Oprn Grapes Of Wrath 1996` (https://history.state.gov/search?q=Oprn+Grapes+Of+Wrath+1996&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1996-03-10..1996-05-09. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_418_oprn_grapes_of_wrath --approved-by joe`. The code never runs it.
