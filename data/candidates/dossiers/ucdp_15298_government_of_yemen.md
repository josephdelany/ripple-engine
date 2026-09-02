# Dossier ucdp_15298_government_of_yemen — Government of Yemen

```json
{
 "id": "ucdp_15298_government_of_yemen",
 "built_by": "session A",
 "built_at": "2026-09-02T21:02:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "15298",
  "detail": "dyad 15298 Government of Yemen (North Yemen) vs GPC (Yemen (North Yemen)) onset 2017-11-30 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2017-11-30",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2017-11-30",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "undetermined",
  "route": "GDELT DOC 2.0",
  "query": "Yemen",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2017-11-27",
   "2017-12-30"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:02:28+00:00",
  "note": "ReadTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 15298 **Government of Yemen**: dyad 15298 Government of Yemen (North Yemen) vs GPC (Yemen (North Yemen)) onset 2017-11-30 intensity 1 trigdate 2017-11-30, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.yemen:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `Yemen` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ReadTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_15298_government_of_yemen --approved-by joe`. The code never runs it.
