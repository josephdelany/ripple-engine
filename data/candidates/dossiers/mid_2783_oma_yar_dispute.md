# Dossier mid_2783_oma_yar_dispute — OMA YAR dispute

```json
{
 "id": "mid_2783_oma_yar_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "2783",
  "detail": "dispute 2783 OMA-YAR 1987-10-11..1987-10-11 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1987-10-11",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-10-11",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.yemen",
   "role": "unknown"
  },
  {
   "entity": "country.omn",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Oma Yar Dispute 1987",
  "search_url": "https://history.state.gov/search?q=Oma+Yar+Dispute+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-09-11",
   "1987-11-10"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:46+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 2783 **OMA YAR dispute**: dispute 2783 OMA-YAR 1987-10-11..1987-10-11 hihost 4 trigdate 1987-10-11, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 678: country.yemen (registered state set)
- 698: country.omn (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.yemen:unknown, country.omn:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Oma Yar Dispute 1987` (https://history.state.gov/search?q=Oma+Yar+Dispute+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-09-11..1987-11-10. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_2783_oma_yar_dispute --approved-by joe`. The code never runs it.
