# Dossier ucdp_769_government_of_india_vs_unlf — Government of India vs UNLF

```json
{
 "id": "ucdp_769_government_of_india_vs_unlf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "769",
  "detail": "dyad 769 Government of India vs UNLF (India) onset 1993-12-31 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1993-12-31",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-12-31",
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
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of India Vs Unlf 1993",
  "search_url": "https://history.state.gov/search?q=Government+Of+India+Vs+Unlf+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-12-01",
   "1994-01-30"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:32+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 769 **Government of India vs UNLF**: dyad 769 Government of India vs UNLF (India) onset 1993-12-31 intensity 1 trigdate 1993-12-31, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of India Vs Unlf 1993` (https://history.state.gov/search?q=Government+Of+India+Vs+Unlf+1993&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-12-01..1994-01-30. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_769_government_of_india_vs_unlf --approved-by joe`. The code never runs it.
