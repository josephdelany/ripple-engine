# Dossier ucdp_865_government_of_eritrea_vs_government_of_e — Government of Eritrea vs Government of Ethiopia

```json
{
 "id": "ucdp_865_government_of_eritrea_vs_government_of_e",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "865",
  "detail": "dyad 865 Government of Eritrea vs Government of Ethiopia (Eritrea, Ethiopia) onset 1998-05-31 intensity 2",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1998-05-31",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-05-31",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530,
  531
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Eritrea Vs Government Of Ethiopia 1998",
  "search_url": "https://history.state.gov/search?q=Government+Of+Eritrea+Vs+Government+Of+Ethiopia+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-05-01",
   "1998-06-30"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:43+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 865 **Government of Eritrea vs Government of Ethiopia**: dyad 865 Government of Eritrea vs Government of Ethiopia (Eritrea, Ethiopia) onset 1998-05-31 intensity 2 trigdate 1998-05-31, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)
- 531: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Eritrea Vs Government Of Ethiopia 1998` (https://history.state.gov/search?q=Government+Of+Eritrea+Vs+Government+Of+Ethiopia+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-05-01..1998-06-30. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_865_government_of_eritrea_vs_government_of_e --approved-by joe`. The code never runs it.
