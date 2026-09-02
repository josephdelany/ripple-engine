# Dossier ucdp_811_government_of_djibouti_vs_frud_c — Government of Djibouti vs FRUD-C

```json
{
 "id": "ucdp_811_government_of_djibouti_vs_frud_c",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "811",
  "detail": "dyad 811 Government of Djibouti vs FRUD-C (Djibouti) onset 1999-07-24 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1999-07-24",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-07-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  522
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Djibouti Vs Frud C 1999",
  "search_url": "https://history.state.gov/search?q=Government+Of+Djibouti+Vs+Frud+C+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-06-24",
   "1999-08-23"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:03+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 811 **Government of Djibouti vs FRUD-C**: dyad 811 Government of Djibouti vs FRUD-C (Djibouti) onset 1999-07-24 intensity 1 trigdate 1999-07-24, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 522: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Djibouti Vs Frud C 1999` (https://history.state.gov/search?q=Government+Of+Djibouti+Vs+Frud+C+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-06-24..1999-08-23. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_811_government_of_djibouti_vs_frud_c --approved-by joe`. The code never runs it.
