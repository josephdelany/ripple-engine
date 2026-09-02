# Dossier icb_378_india_int_sri_lanka — INDIA INT./SRI LANKA

```json
{
 "id": "icb_378_india_int_sri_lanka",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 378,
  "source": "icb",
  "source_id": "378",
  "detail": "INDIA INT./SRI LANKA 1987-06-03..1987-07-28 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=378",
  "trigdate": "1987-06-03",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-06-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  780
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "India Int Sri Lanka 1987",
  "search_url": "https://history.state.gov/search?q=India+Int+Sri+Lanka+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-05-04",
   "1987-07-03"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:31+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 378 **INDIA INT./SRI LANKA**: INDIA INT./SRI LANKA 1987-06-03..1987-07-28 viol 1.0 trigdate 1987-06-03, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=378

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 780: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `India Int Sri Lanka 1987` (https://history.state.gov/search?q=India+Int+Sri+Lanka+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-05-04..1987-07-03. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_378_india_int_sri_lanka --approved-by joe`. The code never runs it.
