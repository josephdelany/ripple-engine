# Dossier icb_423_cyprus_turkey_missile — CYPRUS/TURKEY MISSILE

```json
{
 "id": "icb_423_cyprus_turkey_missile",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 423,
  "source": "icb",
  "source_id": "423",
  "detail": "CYPRUS/TURKEY MISSILE 1998-01-24..1998-12-28 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=423",
  "trigdate": "1998-01-24",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-01-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  352
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Cyprus Turkey Missile 1998",
  "search_url": "https://history.state.gov/search?q=Cyprus+Turkey+Missile+1998&within=documents",
  "search_status": 200,
  "window": [
   "1997-12-25",
   "1998-02-23"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:39+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 423 **CYPRUS/TURKEY MISSILE**: CYPRUS/TURKEY MISSILE 1998-01-24..1998-12-28 viol 1.0 trigdate 1998-01-24, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=423

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 352: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cyprus Turkey Missile 1998` (https://history.state.gov/search?q=Cyprus+Turkey+Missile+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1997-12-25..1998-02-23. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_423_cyprus_turkey_missile --approved-by joe`. The code never runs it.
