# Dossier icb_411_haiti_mil_regime — HAITI MIL. REGIME

```json
{
 "id": "icb_411_haiti_mil_regime",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 411,
  "source": "icb",
  "source_id": "411",
  "detail": "HAITI MIL. REGIME 1994-07-28..1994-10-15 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=411",
  "trigdate": "1994-07-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-07-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  41
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Haiti Mil  Regime 1994",
  "search_url": "https://history.state.gov/search?q=Haiti+Mil++Regime+1994&within=documents",
  "search_status": 200,
  "window": [
   "1994-06-28",
   "1994-08-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:45+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 411 **HAITI MIL. REGIME**: HAITI MIL. REGIME 1994-07-28..1994-10-15 viol 2.0 trigdate 1994-07-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=411

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 41: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Haiti Mil  Regime 1994` (https://history.state.gov/search?q=Haiti+Mil++Regime+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1994-06-28..1994-08-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_411_haiti_mil_regime --approved-by joe`. The code never runs it.
