# Dossier mid_2826_irn_rus_dispute — IRN RUS dispute

```json
{
 "id": "mid_2826_irn_rus_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2826",
  "detail": "dispute 2826 IRN-RUS 1987-04-21..1987-11-02 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-04-21",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-04-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
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
  "query": "Irn Rus Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Irn+Rus+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-03-22",
   "1987-05-21"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:24+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2826 **IRN RUS dispute**: dispute 2826 IRN-RUS 1987-04-21..1987-11-02 hihost 4 trigdate 1987-04-21, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown, country.iran:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Irn Rus Dispute 1987` (https://history.state.gov/search?q=Irn+Rus+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-03-22..1987-05-21. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2826_irn_rus_dispute --approved-by joe`. The code never runs it.
