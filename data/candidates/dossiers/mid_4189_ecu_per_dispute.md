# Dossier mid_4189_ecu_per_dispute — ECU PER dispute

```json
{
 "id": "mid_4189_ecu_per_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4189",
  "detail": "dispute 4189 ECU-PER 1998-07-01..1998-08-01 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1998-07-01",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-07-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ecuador",
   "role": "unknown"
  },
  {
   "entity": "country.peru",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Ecu Per Dispute 1998",
  "search_url": "https://history.state.gov/search?q=Ecu+Per+Dispute+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-06-01",
   "1998-07-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:44+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4189 **ECU PER dispute**: dispute 4189 ECU-PER 1998-07-01..1998-08-01 hihost 4 trigdate 1998-07-01, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 130: country.ecuador (registered state set)
- 135: country.peru

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.ecuador:unknown, country.peru:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ecu Per Dispute 1998` (https://history.state.gov/search?q=Ecu+Per+Dispute+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-06-01..1998-07-31. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4189_ecu_per_dispute --approved-by joe`. The code never runs it.
