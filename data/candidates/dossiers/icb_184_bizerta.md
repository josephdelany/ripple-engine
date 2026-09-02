# Dossier icb_184_bizerta — BIZERTA

```json
{
 "id": "icb_184_bizerta",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:45+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 184,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=184",
  "trigdate": "1961-07-17",
  "termdate": "1961-09-28",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1961-07-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  616
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Bizerta 1961",
  "search_url": "https://history.state.gov/search?q=Bizerta+1961&within=documents",
  "search_status": 200,
  "window": [
   "1961-06-17",
   "1961-10-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:45+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 184 **BIZERTA**: trigdate 1961-07-17, termdate 1961-09-28, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=184

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 616: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.fra:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Bizerta 1961` (https://history.state.gov/search?q=Bizerta+1961&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1961-06-17..1961-10-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_184_bizerta --approved-by joe`. The code never runs it.
