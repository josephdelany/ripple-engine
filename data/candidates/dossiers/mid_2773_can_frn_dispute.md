# Dossier mid_2773_can_frn_dispute — CAN FRN dispute

```json
{
 "id": "mid_2773_can_frn_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2773",
  "detail": "dispute 2773 CAN-FRN 1988-04-14..1988-05-06 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1988-04-14",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1988-04-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.canada",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Can Frn Dispute 1988",
  "search_url": "https://history.state.gov/search?q=Can+Frn+Dispute+1988&within=documents",
  "search_status": 200,
  "window": [
   "1988-03-15",
   "1988-05-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:51+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2773 **CAN FRN dispute**: dispute 2773 CAN-FRN 1988-04-14..1988-05-06 hihost 4 trigdate 1988-04-14, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 20: country.canada (registered state set)
- 220: country.fra (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.canada:unknown, country.fra:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Can Frn Dispute 1988` (https://history.state.gov/search?q=Can+Frn+Dispute+1988&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1988-03-15..1988-05-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2773_can_frn_dispute --approved-by joe`. The code never runs it.
