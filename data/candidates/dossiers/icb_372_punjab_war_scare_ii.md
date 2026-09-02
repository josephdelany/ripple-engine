# Dossier icb_372_punjab_war_scare_ii — PUNJAB WAR SCARE II

```json
{
 "id": "icb_372_punjab_war_scare_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 372,
  "source": "icb",
  "source_id": "372",
  "detail": "PUNJAB WAR SCARE II 1987-01-28..1987-02-19 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=372",
  "trigdate": "1987-01-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-01-28",
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
  "query": "Punjab War Scare Ii 1987",
  "search_url": "https://history.state.gov/search?q=Punjab+War+Scare+Ii+1987&within=documents",
  "search_status": 200,
  "window": [
   "1986-12-29",
   "1987-02-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:50:59+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 372 **PUNJAB WAR SCARE II**: PUNJAB WAR SCARE II 1987-01-28..1987-02-19 viol 1.0 trigdate 1987-01-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=372

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Punjab War Scare Ii 1987` (https://history.state.gov/search?q=Punjab+War+Scare+Ii+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-12-29..1987-02-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_372_punjab_war_scare_ii --approved-by joe`. The code never runs it.
