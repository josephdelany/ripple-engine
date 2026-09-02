# Dossier mid_3569_qat_sau_dispute — QAT SAU dispute

```json
{
 "id": "mid_3569_qat_sau_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3569",
  "detail": "dispute 3569 QAT-SAU 1992-09-28..1992-10-23 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1992-09-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-09-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.qatar",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Qat Sau Dispute 1992",
  "search_url": "https://history.state.gov/search?q=Qat+Sau+Dispute+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-08-29",
   "1992-10-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:08+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3569 **QAT SAU dispute**: dispute 3569 QAT-SAU 1992-09-28..1992-10-23 hihost 4 trigdate 1992-09-28, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 670: country.saudi_arabia (registered state set)
- 694: country.qatar (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.saudi_arabia:unknown, country.qatar:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Qat Sau Dispute 1992` (https://history.state.gov/search?q=Qat+Sau+Dispute+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-08-29..1992-10-28. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3569_qat_sau_dispute --approved-by joe`. The code never runs it.
