# Dossier icb_445_s_ossetia_abkhazia — S. OSSETIA/ABKHAZIA

```json
{
 "id": "icb_445_s_ossetia_abkhazia",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 445,
  "source": "icb",
  "source_id": "445",
  "detail": "S. OSSETIA/ABKHAZIA 2004-06-10..2004-11-05 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=445",
  "trigdate": "2004-06-10",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2004-06-10",
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
   "entity": "country.georgia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2004: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 445 **S. OSSETIA/ABKHAZIA**: S. OSSETIA/ABKHAZIA 2004-06-10..2004-11-05 viol 2.0 trigdate 2004-06-10, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=445

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 372: country.georgia

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown, country.georgia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2004: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_445_s_ossetia_abkhazia --approved-by joe`. The code never runs it.
