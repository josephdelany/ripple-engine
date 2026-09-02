# Dossier ucdp_719_government_of_ethiopia_vs_onlf — Government of Ethiopia vs ONLF

```json
{
 "id": "ucdp_719_government_of_ethiopia_vs_onlf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "719",
  "detail": "dyad 719 Government of Ethiopia vs ONLF (Ethiopia) onset 1994-02-26 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1994-02-26",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-02-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Ethiopia Vs Onlf 1994",
  "search_url": "https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Onlf+1994&within=documents",
  "search_status": 200,
  "window": [
   "1994-01-27",
   "1994-03-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:36+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 719 **Government of Ethiopia vs ONLF**: dyad 719 Government of Ethiopia vs ONLF (Ethiopia) onset 1994-02-26 intensity 1 trigdate 1994-02-26, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Ethiopia Vs Onlf 1994` (https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Onlf+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1994-01-27..1994-03-28. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_719_government_of_ethiopia_vs_onlf --approved-by joe`. The code never runs it.
