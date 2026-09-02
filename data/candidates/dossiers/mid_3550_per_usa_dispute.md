# Dossier mid_3550_per_usa_dispute — PER USA dispute

```json
{
 "id": "mid_3550_per_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "3550",
  "detail": "dispute 3550 PER-USA 1992-04-24..1992-04-24 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1992-04-24",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-04-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
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
  "query": "Per Usa Dispute 1992",
  "search_url": "https://history.state.gov/search?q=Per+Usa+Dispute+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-03-25",
   "1992-05-24"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:00+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 3550 **PER USA dispute**: dispute 3550 PER-USA 1992-04-24..1992-04-24 hihost 4 trigdate 1992-04-24, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 135: country.peru

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.peru:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Per Usa Dispute 1992` (https://history.state.gov/search?q=Per+Usa+Dispute+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-03-25..1992-05-24. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_3550_per_usa_dispute --approved-by joe`. The code never runs it.
