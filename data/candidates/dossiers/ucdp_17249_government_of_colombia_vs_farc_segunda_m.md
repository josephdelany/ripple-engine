# Dossier ucdp_17249_government_of_colombia_vs_farc_segunda_m — Government of Colombia vs FARC - Segunda Marquetalia 

```json
{
 "id": "ucdp_17249_government_of_colombia_vs_farc_segunda_m",
 "built_by": "session A",
 "built_at": "2026-09-02T21:20:03+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "17249",
  "detail": "dyad 17249 Government of Colombia vs FARC - Segunda Marquetalia  (Colombia) onset 2024-09-05 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2024-09-05",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2024-09-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.col",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "undetermined",
  "route": "GDELT DOC 2.0",
  "query": "Colombia FARC Segunda",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2024-09-02",
   "2024-10-05"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:20:03+00:00",
  "note": "ConnectTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 17249 **Government of Colombia vs FARC - Segunda Marquetalia **: dyad 17249 Government of Colombia vs FARC - Segunda Marquetalia  (Colombia) onset 2024-09-05 intensity 1 trigdate 2024-09-05, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 100: country.col (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.col:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `Colombia FARC Segunda` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ConnectTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_17249_government_of_colombia_vs_farc_segunda_m --approved-by joe`. The code never runs it.
