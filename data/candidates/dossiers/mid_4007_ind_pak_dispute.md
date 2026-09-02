# Dossier mid_4007_ind_pak_dispute — IND PAK dispute

```json
{
 "id": "mid_4007_ind_pak_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4007",
  "detail": "dispute 4007 IND-PAK 1993-09-17..1999-07-17 hihost 5",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1993-09-17",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-09-17",
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
  "query": "Ind Pak Dispute 1993",
  "search_url": "https://history.state.gov/search?q=Ind+Pak+Dispute+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-08-18",
   "1993-10-17"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:24+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4007 **IND PAK dispute**: dispute 4007 IND-PAK 1993-09-17..1999-07-17 hihost 5 trigdate 1993-09-17, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ind Pak Dispute 1993` (https://history.state.gov/search?q=Ind+Pak+Dispute+1993&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-08-18..1993-10-17. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4007_ind_pak_dispute --approved-by joe`. The code never runs it.
