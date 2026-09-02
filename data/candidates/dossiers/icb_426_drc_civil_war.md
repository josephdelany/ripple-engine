# Dossier icb_426_drc_civil_war — DRC CIVIL WAR

```json
{
 "id": "icb_426_drc_civil_war",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 426,
  "source": "icb",
  "source_id": "426",
  "detail": "DRC CIVIL WAR 1998-07-28..2002-07-28 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=426",
  "trigdate": "1998-07-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-07-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  },
  {
   "entity": "country.ago",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  483,
  500,
  517,
  552,
  565
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Drc Civil War 1998",
  "search_url": "https://history.state.gov/search?q=Drc+Civil+War+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-06-28",
   "1998-08-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:46+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 426 **DRC CIVIL WAR**: DRC CIVIL WAR 1998-07-28..2002-07-28 viol 4.0 trigdate 1998-07-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=426

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 483: UNMAPPED
- 490: country.congo_drc
- 500: UNMAPPED
- 517: UNMAPPED
- 540: country.ago (registered state set)
- 552: UNMAPPED
- 565: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.congo_drc:unknown, country.ago:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Drc Civil War 1998` (https://history.state.gov/search?q=Drc+Civil+War+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-06-28..1998-08-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_426_drc_civil_war --approved-by joe`. The code never runs it.
