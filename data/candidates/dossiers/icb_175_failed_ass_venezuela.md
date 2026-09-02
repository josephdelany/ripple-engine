# Dossier icb_175_failed_ass_venezuela — FAILED ASS. VENEZUELA

```json
{
 "id": "icb_175_failed_ass_venezuela",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:32+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 175,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=175",
  "trigdate": "1960-06-24",
  "termdate": "1960-09-28",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1960-06-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.venezuela",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  42
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Failed Ass  Venezuela 1960",
  "search_url": "https://history.state.gov/search?q=Failed+Ass++Venezuela+1960&within=documents",
  "search_status": 200,
  "window": [
   "1960-05-25",
   "1960-10-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:32+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 175 **FAILED ASS. VENEZUELA**: trigdate 1960-06-24, termdate 1960-09-28, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=175

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 42: UNMAPPED
- 101: country.venezuela (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.venezuela:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Failed Ass  Venezuela 1960` (https://history.state.gov/search?q=Failed+Ass++Venezuela+1960&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1960-05-25..1960-10-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_175_failed_ass_venezuela --approved-by joe`. The code never runs it.
