# Dossier icb_470_syria_chemical_weapons — SYRIA CHEMICAL WEAPONS

```json
{
 "id": "icb_470_syria_chemical_weapons",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 470,
  "source": "icb",
  "source_id": "470",
  "detail": "SYRIA CHEMICAL WEAPONS 2013-08-21..2013-09-21 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=470",
  "trigdate": "2013-08-21",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2013-08-21",
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
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2013: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 470 **SYRIA CHEMICAL WEAPONS**: SYRIA CHEMICAL WEAPONS 2013-08-21..2013-09-21 viol 4.0 trigdate 2013-08-21, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=470

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.syr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2013: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_470_syria_chemical_weapons --approved-by joe`. The code never runs it.
