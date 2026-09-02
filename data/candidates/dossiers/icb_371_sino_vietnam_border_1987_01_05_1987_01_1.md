# Dossier icb_371_sino_vietnam_border_1987_01_05_1987_01_1 — SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0

```json
{
 "id": "icb_371_sino_vietnam_border_1987_01_05_1987_01_1",
 "built_by": "session A",
 "built_at": "2026-09-02T19:50:26+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 371,
  "source": "icb",
  "source_id": "371",
  "detail": "SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=371",
  "trigdate": "1987-01-05",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-01-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.vietnam",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Sino Vietnam Border   Viol 1987",
  "search_url": "https://history.state.gov/search?q=Sino+Vietnam+Border+++Viol+1987&within=documents",
  "search_status": 200,
  "window": [
   "1986-12-06",
   "1987-02-04"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:50:26+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 371 **SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0**: SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0 trigdate 1987-01-05, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=371

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.vietnam:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sino Vietnam Border   Viol 1987` (https://history.state.gov/search?q=Sino+Vietnam+Border+++Viol+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-12-06..1987-02-04. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_371_sino_vietnam_border_1987_01_05_1987_01_1 --approved-by joe`. The code never runs it.
