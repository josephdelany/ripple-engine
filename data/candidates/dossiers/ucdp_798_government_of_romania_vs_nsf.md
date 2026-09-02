# Dossier ucdp_798_government_of_romania_vs_nsf — Government of Romania vs NSF

```json
{
 "id": "ucdp_798_government_of_romania_vs_nsf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "798",
  "detail": "dyad 798 Government of Romania vs NSF (Romania) onset 1989-12-22 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1989-12-22",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1989-12-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  360
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "opened": [],
  "window": null,
  "note": "no query can be formed from 'Government of Romania vs NSF' that names a registered state or carries two content terms (\u00a75.2)"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 798 **Government of Romania vs NSF**: dyad 798 Government of Romania vs NSF (Romania) onset 1989-12-22 intensity 1 trigdate 1989-12-22, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 360: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no query can be formed from 'Government of Romania vs NSF' that names a registered state or carries two content terms (§5.2)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_798_government_of_romania_vs_nsf --approved-by joe`. The code never runs it.
