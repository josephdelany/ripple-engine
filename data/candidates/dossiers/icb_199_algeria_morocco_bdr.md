# Dossier icb_199_algeria_morocco_bdr — ALGERIA/MOROCCO BDR.

```json
{
 "id": "icb_199_algeria_morocco_bdr",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:12+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 199,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=199",
  "trigdate": "1963-10-01",
  "termdate": "1963-11-04",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1963-10-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  600
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Algeria Morocco Bdr 1963",
  "search_url": "https://history.state.gov/search?q=Algeria+Morocco+Bdr+1963&within=documents",
  "search_status": 200,
  "window": [
   "1963-09-01",
   "1963-12-04"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:15:12+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 199 **ALGERIA/MOROCCO BDR.**: trigdate 1963-10-01, termdate 1963-11-04, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=199

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 600: UNMAPPED
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Algeria Morocco Bdr 1963` (https://history.state.gov/search?q=Algeria+Morocco+Bdr+1963&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1963-09-01..1963-12-04.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_199_algeria_morocco_bdr --approved-by joe`. The code never runs it.
