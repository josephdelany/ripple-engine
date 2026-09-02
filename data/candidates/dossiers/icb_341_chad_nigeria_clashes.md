# Dossier icb_341_chad_nigeria_clashes — CHAD/NIGERIA CLASHES

```json
{
 "id": "icb_341_chad_nigeria_clashes",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:24+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 341,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=341",
  "trigdate": "1983-04-18",
  "termdate": "1983-07-11",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1983-04-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.nigeria",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Chad Nigeria Clashes 1983",
  "search_url": "https://history.state.gov/search?q=Chad+Nigeria+Clashes+1983&within=documents",
  "search_status": 200,
  "window": [
   "1983-03-19",
   "1983-08-10"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:24+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 341 **CHAD/NIGERIA CLASHES**: trigdate 1983-04-18, termdate 1983-07-11, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=341

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 475: country.nigeria (registered state set)
- 483: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.nigeria:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Nigeria Clashes 1983` (https://history.state.gov/search?q=Chad+Nigeria+Clashes+1983&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1983-03-19..1983-08-10.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_341_chad_nigeria_clashes --approved-by joe`. The code never runs it.
