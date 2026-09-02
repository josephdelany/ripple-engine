# Dossier ucdp_10006_government_of_ethiopia_vs_iglf — Government of Ethiopia vs IGLF

```json
{
 "id": "ucdp_10006_government_of_ethiopia_vs_iglf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "10006",
  "detail": "dyad 10006 Government of Ethiopia vs IGLF (Ethiopia) onset 1991-10-10 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1991-10-10",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1991-10-10",
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
  "query": "Government Of Ethiopia Vs Iglf 1991",
  "search_url": "https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Iglf+1991&within=documents",
  "search_status": 200,
  "window": [
   "1991-09-10",
   "1991-11-09"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:51+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 10006 **Government of Ethiopia vs IGLF**: dyad 10006 Government of Ethiopia vs IGLF (Ethiopia) onset 1991-10-10 intensity 1 trigdate 1991-10-10, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Ethiopia Vs Iglf 1991` (https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Iglf+1991&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1991-09-10..1991-11-09. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_10006_government_of_ethiopia_vs_iglf --approved-by joe`. The code never runs it.
