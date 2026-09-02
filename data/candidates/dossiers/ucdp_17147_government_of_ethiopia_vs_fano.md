# Dossier ucdp_17147_government_of_ethiopia_vs_fano — Government of Ethiopia vs Fano

```json
{
 "id": "ucdp_17147_government_of_ethiopia_vs_fano",
 "built_by": "session A",
 "built_at": "2026-09-02T21:16:34+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "17147",
  "detail": "dyad 17147 Government of Ethiopia vs Fano (Ethiopia) onset 2023-06-27 intensity 2",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2023-06-27",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2023-06-27",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530
 ],
 "second_source": {
  "found": false,
  "status": "undetermined",
  "route": "GDELT DOC 2.0",
  "query": "Ethiopia Fano",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2023-06-24",
   "2023-07-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:16:34+00:00",
  "note": "ConnectTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 17147 **Government of Ethiopia vs Fano**: dyad 17147 Government of Ethiopia vs Fano (Ethiopia) onset 2023-06-27 intensity 2 trigdate 2023-06-27, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `Ethiopia Fano` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ConnectTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_17147_government_of_ethiopia_vs_fano --approved-by joe`. The code never runs it.
