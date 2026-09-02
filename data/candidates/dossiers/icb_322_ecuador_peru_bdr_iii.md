# Dossier icb_322_ecuador_peru_bdr_iii — ECUADOR/PERU BDR. III

```json
{
 "id": "icb_322_ecuador_peru_bdr_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:00+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 322,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=322",
  "trigdate": "1981-01-22",
  "termdate": "1981-04-02",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1981-01-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ecuador",
   "role": "target"
  },
  {
   "entity": "country.peru",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Ecuador Peru Bdr  Iii 1981",
  "search_url": "https://history.state.gov/search?q=Ecuador+Peru+Bdr++Iii+1981&within=documents",
  "search_status": 200,
  "window": [
   "1980-12-23",
   "1981-05-02"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:00+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 322 **ECUADOR/PERU BDR. III**: trigdate 1981-01-22, termdate 1981-04-02, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=322

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 130: country.ecuador (registered state set)
- 135: country.peru

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.ecuador:target, country.peru:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ecuador Peru Bdr  Iii 1981` (https://history.state.gov/search?q=Ecuador+Peru+Bdr++Iii+1981&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1980-12-23..1981-05-02.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_322_ecuador_peru_bdr_iii --approved-by joe`. The code never runs it.
