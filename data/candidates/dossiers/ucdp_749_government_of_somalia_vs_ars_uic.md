# Dossier ucdp_749_government_of_somalia_vs_ars_uic — Government of Somalia vs ARS/UIC

```json
{
 "id": "ucdp_749_government_of_somalia_vs_ars_uic",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "749",
  "detail": "dyad 749 Government of Somalia vs ARS/UIC (Somalia) onset 2006-10-24 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2006-10-24",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2006-10-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "opened": [],
  "window": null,
  "note": "no query can be formed from 'Government of Somalia vs ARS/UIC' that names a registered state or carries two content terms (\u00a75.2)"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 749 **Government of Somalia vs ARS/UIC**: dyad 749 Government of Somalia vs ARS/UIC (Somalia) onset 2006-10-24 intensity 1 trigdate 2006-10-24, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no query can be formed from 'Government of Somalia vs ARS/UIC' that names a registered state or carries two content terms (§5.2)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_749_government_of_somalia_vs_ars_uic --approved-by joe`. The code never runs it.
