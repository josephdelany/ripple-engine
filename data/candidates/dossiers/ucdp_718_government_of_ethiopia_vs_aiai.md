# Dossier ucdp_718_government_of_ethiopia_vs_aiai — Government of Ethiopia vs AIAI

```json
{
 "id": "ucdp_718_government_of_ethiopia_vs_aiai",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "718",
  "detail": "dyad 718 Government of Ethiopia vs AIAI (Ethiopia) onset 1993-10-13 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1993-10-13",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-10-13",
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
  "query": "Government Of Ethiopia Vs Aiai 1993",
  "search_url": "https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Aiai+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-09-13",
   "1993-11-12"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:28+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 718 **Government of Ethiopia vs AIAI**: dyad 718 Government of Ethiopia vs AIAI (Ethiopia) onset 1993-10-13 intensity 1 trigdate 1993-10-13, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Ethiopia Vs Aiai 1993` (https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Aiai+1993&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-09-13..1993-11-12. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_718_government_of_ethiopia_vs_aiai --approved-by joe`. The code never runs it.
