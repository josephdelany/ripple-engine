# Dossier mid_4297_jpn_rus_dispute — JPN RUS dispute

```json
{
 "id": "mid_4297_jpn_rus_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4297",
  "detail": "dispute 4297 JPN-RUS 1996-10-12..1996-10-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1996-10-12",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-10-12",
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
   "entity": "country.japan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Jpn Rus Dispute 1996",
  "search_url": "https://history.state.gov/search?q=Jpn+Rus+Dispute+1996&within=documents",
  "search_status": 200,
  "window": [
   "1996-09-12",
   "1996-11-11"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:24+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4297 **JPN RUS dispute**: dispute 4297 JPN-RUS 1996-10-12..1996-10-28 hihost 4 trigdate 1996-10-12, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 740: country.japan (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown, country.japan:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Jpn Rus Dispute 1996` (https://history.state.gov/search?q=Jpn+Rus+Dispute+1996&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1996-09-12..1996-11-11. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4297_jpn_rus_dispute --approved-by joe`. The code never runs it.
