# Dossier icb_305_goulimime_tarfaya_rd — GOULIMIME-TARFAYA RD

```json
{
 "id": "icb_305_goulimime_tarfaya_rd",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 305,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=305",
  "trigdate": "1979-06-01",
  "termdate": "1979-06-25",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1979-06-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
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
  "query": "Goulimime Tarfaya Rd 1979",
  "search_url": "https://history.state.gov/search?q=Goulimime+Tarfaya+Rd+1979&within=documents",
  "search_status": 200,
  "window": [
   "1979-05-02",
   "1979-07-25"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:27+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 305 **GOULIMIME-TARFAYA RD**: trigdate 1979-06-01, termdate 1979-06-25, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=305

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 600: UNMAPPED
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Goulimime Tarfaya Rd 1979` (https://history.state.gov/search?q=Goulimime+Tarfaya+Rd+1979&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1979-05-02..1979-07-25.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_305_goulimime_tarfaya_rd --approved-by joe`. The code never runs it.
