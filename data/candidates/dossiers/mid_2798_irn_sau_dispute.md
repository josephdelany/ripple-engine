# Dossier mid_2798_irn_sau_dispute — IRN SAU dispute

```json
{
 "id": "mid_2798_irn_sau_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2798",
  "detail": "dispute 2798 IRN-SAU 1987-08-02..1988-04-24 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-08-02",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-08-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irn Sau Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Irn+Sau+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-07-03",
   "1987-09-01"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:37+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2798 **IRN SAU dispute**: dispute 2798 IRN-SAU 1987-08-02..1988-04-24 hihost 4 trigdate 1987-08-02, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 670: country.saudi_arabia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.saudi_arabia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irn Sau Dispute 1987` (https://history.state.gov/search?q=Irn+Sau+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-07-03..1987-09-01. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2798_irn_sau_dispute --approved-by joe`. The code never runs it.
