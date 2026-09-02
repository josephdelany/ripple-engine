# Dossier icb_456_djibouti_eritrea — DJIBOUTI-ERITREA

```json
{
 "id": "icb_456_djibouti_eritrea",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 456,
  "source": "icb",
  "source_id": "456",
  "detail": "DJIBOUTI-ERITREA 2008-04-07..2008-06-28 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=456",
  "trigdate": "2008-04-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2008-04-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  522,
  531
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2008: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 456 **DJIBOUTI-ERITREA**: DJIBOUTI-ERITREA 2008-04-07..2008-06-28 viol 2.0 trigdate 2008-04-07, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=456

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 522: UNMAPPED (registered state set)
- 531: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2008: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_456_djibouti_eritrea --approved-by joe`. The code never runs it.
