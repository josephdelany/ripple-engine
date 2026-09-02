# Dossier mid_4223_ind_pak_dispute — IND PAK dispute

```json
{
 "id": "mid_4223_ind_pak_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4223",
  "detail": "dispute 4223 IND-PAK 1999-07-18..2000-10-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1999-07-18",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-07-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Ind Pak Dispute 1999",
  "search_url": "https://history.state.gov/search?q=Ind+Pak+Dispute+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-06-18",
   "1999-08-17"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:00+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4223 **IND PAK dispute**: dispute 4223 IND-PAK 1999-07-18..2000-10-28 hihost 4 trigdate 1999-07-18, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ind Pak Dispute 1999` (https://history.state.gov/search?q=Ind+Pak+Dispute+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-06-18..1999-08-17. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4223_ind_pak_dispute --approved-by joe`. The code never runs it.
