# Dossier mid_2749_chn_drv_dispute — CHN DRV dispute

```json
{
 "id": "mid_2749_chn_drv_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2749",
  "detail": "dispute 2749 CHN-DRV 1988-02-20..1988-03-16 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1988-02-20",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1988-02-20",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.vietnam",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Chn Drv Dispute 1988",
  "search_url": "https://history.state.gov/search?q=Chn+Drv+Dispute+1988&within=documents",
  "search_status": 200,
  "window": [
   "1988-01-21",
   "1988-03-21"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:49+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2749 **CHN DRV dispute**: dispute 2749 CHN-DRV 1988-02-20..1988-03-16 hihost 4 trigdate 1988-02-20, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.vietnam:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chn Drv Dispute 1988` (https://history.state.gov/search?q=Chn+Drv+Dispute+1988&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1988-01-21..1988-03-21. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2749_chn_drv_dispute --approved-by joe`. The code never runs it.
