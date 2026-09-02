# Dossier mid_4035_chn_taw_dispute — CHN TAW dispute

```json
{
 "id": "mid_4035_chn_taw_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4035",
  "detail": "dispute 4035 CHN-TAW 1994-06-01..1994-11-14 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1994-06-01",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-06-01",
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
   "entity": "country.taiwan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Chn Taw Dispute 1994",
  "search_url": "https://history.state.gov/search?q=Chn+Taw+Dispute+1994&within=documents",
  "search_status": 200,
  "window": [
   "1994-05-02",
   "1994-07-01"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:42+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4035 **CHN TAW dispute**: dispute 4035 CHN-TAW 1994-06-01..1994-11-14 hihost 4 trigdate 1994-06-01, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.taiwan:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chn Taw Dispute 1994` (https://history.state.gov/search?q=Chn+Taw+Dispute+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1994-05-02..1994-07-01. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4035_chn_taw_dispute --approved-by joe`. The code never runs it.
