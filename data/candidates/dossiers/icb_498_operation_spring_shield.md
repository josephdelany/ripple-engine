# Dossier icb_498_operation_spring_shield — OPERATION SPRING SHIELD

```json
{
 "id": "icb_498_operation_spring_shield",
 "built_by": "session A",
 "built_at": "2026-09-02T21:10:06+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 498,
  "source": "icb",
  "source_id": "498",
  "detail": "OPERATION SPRING SHIELD 2020-02-27..2020-03-05 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=498",
  "trigdate": "2020-02-27",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2020-02-27",
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
   "entity": "country.turkey",
   "role": "unknown"
  },
  {
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "undetermined",
  "route": "GDELT DOC 2.0",
  "query": "OPERATION SPRING SHIELD Russia Turkey",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2020-02-24",
   "2020-03-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:10:06+00:00",
  "note": "ReadTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 498 **OPERATION SPRING SHIELD**: OPERATION SPRING SHIELD 2020-02-27..2020-03-05 viol 4.0 trigdate 2020-02-27, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=498

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 640: country.turkey (registered state set)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown, country.turkey:unknown, country.syr:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `OPERATION SPRING SHIELD Russia Turkey` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ReadTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_498_operation_spring_shield --approved-by joe`. The code never runs it.
