# Dossier ucdp_18195_government_of_israel_vs_government_of_ye — Government of Israel vs Government of Yemen

```json
{
 "id": "ucdp_18195_government_of_israel_vs_government_of_ye",
 "built_by": "session A",
 "built_at": "2026-09-02T21:21:13+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "18195",
  "detail": "dyad 18195 Government of Israel vs Government of Yemen (North Yemen) (Israel, Yemen (North Yemen)) onset 2025-05-22 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2025-05-22",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2025-05-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.israel",
   "role": "unknown"
  },
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
  "query": "Israel Yemen",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2025-05-19",
   "2025-06-21"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:21:13+00:00",
  "note": "ConnectTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 18195 **Government of Israel vs Government of Yemen**: dyad 18195 Government of Israel vs Government of Yemen (North Yemen) (Israel, Yemen (North Yemen)) onset 2025-05-22 intensity 1 trigdate 2025-05-22, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 666: country.israel (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.israel:unknown, country.yemen:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `Israel Yemen` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ConnectTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_18195_government_of_israel_vs_government_of_ye --approved-by joe`. The code never runs it.
