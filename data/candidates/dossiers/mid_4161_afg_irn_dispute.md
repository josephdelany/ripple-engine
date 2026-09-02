# Dossier mid_4161_afg_irn_dispute — AFG IRN dispute

```json
{
 "id": "mid_4161_afg_irn_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4161",
  "detail": "dispute 4161 AFG-IRN 1999-05-16..1999-05-16 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1999-05-16",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-05-16",
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
   "entity": "country.afg",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Afg Irn Dispute 1999",
  "search_url": "https://history.state.gov/search?q=Afg+Irn+Dispute+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-04-16",
   "1999-06-15"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:58+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4161 **AFG IRN dispute**: dispute 4161 AFG-IRN 1999-05-16..1999-05-16 hihost 4 trigdate 1999-05-16, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 700: country.afg

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.afg:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Afg Irn Dispute 1999` (https://history.state.gov/search?q=Afg+Irn+Dispute+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-04-16..1999-06-15. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4161_afg_irn_dispute --approved-by joe`. The code never runs it.
