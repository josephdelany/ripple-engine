# Dossier icb_474_houthi_rebellion — HOUTHI REBELLION

```json
{
 "id": "icb_474_houthi_rebellion",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 474,
  "source": "icb",
  "source_id": "474",
  "detail": "HOUTHI REBELLION 2015-01-22..2020-12-26 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=474",
  "trigdate": "2015-01-22",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2015-01-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.uae",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2015: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 474 **HOUTHI REBELLION**: HOUTHI REBELLION 2015-01-22..2020-12-26 viol 4.0 trigdate 2015-01-22, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=474

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 670: country.saudi_arabia (registered state set)
- 696: country.uae (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.saudi_arabia:unknown, country.uae:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2015: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_474_houthi_rebellion --approved-by joe`. The code never runs it.
