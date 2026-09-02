# Dossier icb_392_kashmir_iii_nuclear — KASHMIR III-NUCLEAR

```json
{
 "id": "icb_392_kashmir_iii_nuclear",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 392,
  "source": "icb",
  "source_id": "392",
  "detail": "KASHMIR III-NUCLEAR 1990-01-14..1990-06-28 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=392",
  "trigdate": "1990-01-14",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1990-01-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Kashmir Iii Nuclear 1990",
  "search_url": "https://history.state.gov/search?q=Kashmir+Iii+Nuclear+1990&within=documents",
  "search_status": 200,
  "window": [
   "1989-12-15",
   "1990-02-13"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:18+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 392 **KASHMIR III-NUCLEAR**: KASHMIR III-NUCLEAR 1990-01-14..1990-06-28 viol 3.0 trigdate 1990-01-14, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=392

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Kashmir Iii Nuclear 1990` (https://history.state.gov/search?q=Kashmir+Iii+Nuclear+1990&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1989-12-15..1990-02-13. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_392_kashmir_iii_nuclear --approved-by joe`. The code never runs it.
