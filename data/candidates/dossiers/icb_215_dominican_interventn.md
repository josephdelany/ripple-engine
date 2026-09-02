# Dossier icb_215_dominican_interventn — DOMINICAN INTERVENTN.

```json
{
 "id": "icb_215_dominican_interventn",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:44+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 215,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=215",
  "trigdate": "1965-04-24",
  "termdate": "1965-08-28",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1965-04-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Dominican Interventn 1965",
  "search_url": "https://history.state.gov/search?q=Dominican+Interventn+1965&within=documents",
  "search_status": 200,
  "window": [
   "1965-03-25",
   "1965-09-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:15:44+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 215 **DOMINICAN INTERVENTN.**: trigdate 1965-04-24, termdate 1965-08-28, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=215

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Dominican Interventn 1965` (https://history.state.gov/search?q=Dominican+Interventn+1965&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1965-03-25..1965-09-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_215_dominican_interventn --approved-by joe`. The code never runs it.
