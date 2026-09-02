# Dossier icb_442_iran_nuclear_i — IRAN NUCLEAR I

```json
{
 "id": "icb_442_iran_nuclear_i",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 442,
  "source": "icb",
  "source_id": "442",
  "detail": "IRAN NUCLEAR I 2003-06-13..2004-11-15 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=442",
  "trigdate": "2003-06-13",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2003-06-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.iran",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  260
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2003: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 442 **IRAN NUCLEAR I**: IRAN NUCLEAR I 2003-06-13..2004-11-15 viol 1.0 trigdate 2003-06-13, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=442

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 260: UNMAPPED (registered state set)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown, country.fra:unknown, country.iran:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2003: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_442_iran_nuclear_i --approved-by joe`. The code never runs it.
