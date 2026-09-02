# Dossier mid_2740_irn_usa_dispute — IRN USA dispute

```json
{
 "id": "mid_2740_irn_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2740",
  "detail": "dispute 2740 IRN-USA 1987-01-27..1988-07-03 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-01-27",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-01-27",
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
   "entity": "country.iran",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Irn Usa Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Irn+Usa+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1986-12-28",
   "1987-02-26"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:50:57+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2740 **IRN USA dispute**: dispute 2740 IRN-USA 1987-01-27..1988-07-03 hihost 4 trigdate 1987-01-27, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.iran:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irn Usa Dispute 1987` (https://history.state.gov/search?q=Irn+Usa+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-12-28..1987-02-26. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2740_irn_usa_dispute --approved-by joe`. The code never runs it.
