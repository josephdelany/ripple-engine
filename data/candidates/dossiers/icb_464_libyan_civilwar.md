# Dossier icb_464_libyan_civilwar — LIBYAN CIVILWAR

```json
{
 "id": "icb_464_libyan_civilwar",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 464,
  "source": "icb",
  "source_id": "464",
  "detail": "LIBYAN CIVILWAR 2011-02-22..2011-10-20 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=464",
  "trigdate": "2011-02-22",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2011-02-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.canada",
   "role": "unknown"
  },
  {
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.libya",
   "role": "unknown"
  },
  {
   "entity": "country.qatar",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  325
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2011: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 464 **LIBYAN CIVILWAR**: LIBYAN CIVILWAR 2011-02-22..2011-10-20 viol 4.0 trigdate 2011-02-22, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=464

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 325: UNMAPPED (registered state set)
- 620: country.libya (registered state set)
- 694: country.qatar (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.libya:unknown, country.qatar:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2011: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_464_libyan_civilwar --approved-by joe`. The code never runs it.
