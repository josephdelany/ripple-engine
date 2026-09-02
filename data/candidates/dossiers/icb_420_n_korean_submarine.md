# Dossier icb_420_n_korean_submarine — N. KOREAN SUBMARINE

```json
{
 "id": "icb_420_n_korean_submarine",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 420,
  "source": "icb",
  "source_id": "420",
  "detail": "N. KOREAN SUBMARINE 1996-09-18..1996-12-28 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=420",
  "trigdate": "1996-09-18",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-09-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.south_korea",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "N  Korean Submarine 1996",
  "search_url": "https://history.state.gov/search?q=N++Korean+Submarine+1996&within=documents",
  "search_status": 200,
  "window": [
   "1996-08-19",
   "1996-10-18"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:20+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 420 **N. KOREAN SUBMARINE**: N. KOREAN SUBMARINE 1996-09-18..1996-12-28 viol 2.0 trigdate 1996-09-18, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=420

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 731: UNMAPPED
- 732: country.south_korea (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.south_korea:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `N  Korean Submarine 1996` (https://history.state.gov/search?q=N++Korean+Submarine+1996&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1996-08-19..1996-10-18. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_420_n_korean_submarine --approved-by joe`. The code never runs it.
