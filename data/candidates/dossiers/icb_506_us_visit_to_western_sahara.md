# Dossier icb_506_us_visit_to_western_sahara — US VISIT TO WESTERN SAHARA

```json
{
 "id": "icb_506_us_visit_to_western_sahara",
 "built_by": "session A",
 "built_at": "2026-09-02T21:13:32+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 506,
  "source": "icb",
  "source_id": "506",
  "detail": "US VISIT TO WESTERN SAHARA 2021-01-09..2021-01-18 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=506",
  "trigdate": "2021-01-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2021-01-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "undetermined",
  "route": "GDELT DOC 2.0",
  "query": "VISIT WESTERN SAHARA Algeria",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2021-01-06",
   "2021-02-08"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:13:32+00:00",
  "note": "ReadTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 506 **US VISIT TO WESTERN SAHARA**: US VISIT TO WESTERN SAHARA 2021-01-09..2021-01-18 viol 1.0 trigdate 2021-01-09, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=506

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `VISIT WESTERN SAHARA Algeria` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ReadTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_506_us_visit_to_western_sahara --approved-by joe`. The code never runs it.
