# Dossier icb_431_kargil — KARGIL

```json
{
 "id": "icb_431_kargil",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 431,
  "source": "icb",
  "source_id": "431",
  "detail": "KARGIL 1999-05-09..1999-07-04 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=431",
  "trigdate": "1999-05-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-05-09",
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
  "query": "Kargil 1999",
  "search_url": "https://history.state.gov/search?q=Kargil+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-04-09",
   "1999-06-08"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:57+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 431 **KARGIL**: KARGIL 1999-05-09..1999-07-04 viol 3.0 trigdate 1999-05-09, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=431

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Kargil 1999` (https://history.state.gov/search?q=Kargil+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-04-09..1999-06-08. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_431_kargil --approved-by joe`. The code never runs it.
