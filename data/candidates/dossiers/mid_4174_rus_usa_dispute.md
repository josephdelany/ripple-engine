# Dossier mid_4174_rus_usa_dispute — RUS USA dispute

```json
{
 "id": "mid_4174_rus_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4174",
  "detail": "dispute 4174 RUS-USA 1997-08-15..1997-08-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1997-08-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1997-08-15",
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
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Rus Usa Dispute 1997",
  "search_url": "https://history.state.gov/search?q=Rus+Usa+Dispute+1997&within=documents",
  "search_status": 200,
  "window": [
   "1997-07-16",
   "1997-09-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:33+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4174 **RUS USA dispute**: dispute 4174 RUS-USA 1997-08-15..1997-08-28 hihost 4 trigdate 1997-08-15, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.russia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Rus Usa Dispute 1997` (https://history.state.gov/search?q=Rus+Usa+Dispute+1997&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1997-07-16..1997-09-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4174_rus_usa_dispute --approved-by joe`. The code never runs it.
