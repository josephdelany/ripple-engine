# Dossier icb_508_israel_iran_clashes_in_syria_iii — ISRAEL-IRAN CLASHES IN SYRIA III

```json
{
 "id": "icb_508_israel_iran_clashes_in_syria_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T21:14:42+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 508,
  "source": "icb",
  "source_id": "508",
  "detail": "ISRAEL-IRAN CLASHES IN SYRIA III 2021-01-13..2021-01-22 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=508",
  "trigdate": "2021-01-13",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2021-01-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
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
  "query": "ISRAEL IRAN CLASHES Iran Syria",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc",
  "search_status": null,
  "window": [
   "2021-01-10",
   "2021-02-12"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T21:14:42+00:00",
  "note": "ConnectTimeout",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 508 **ISRAEL-IRAN CLASHES IN SYRIA III**: ISRAEL-IRAN CLASHES IN SYRIA III 2021-01-13..2021-01-22 viol 4.0 trigdate 2021-01-13, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=508

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.syr:unknown

## Second source (rule §3)
- **second source: UNDETERMINED — the source refused or failed, not an absence.** GDELT DOC 2.0 returned HTTP None for `ISRAEL IRAN CLASHES Iran Syria` (https://api.gdeltproject.org/api/v2/doc/doc). This dossier is NOT admissible and is NOT evidence that no second source exists; re-run `python3 src/dossier.py --csv data/candidates/post1987_candidates.csv` when the limit clears (DOSSIER_RULE.md §5.1). ConnectTimeout

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_508_israel_iran_clashes_in_syria_iii --approved-by joe`. The code never runs it.
