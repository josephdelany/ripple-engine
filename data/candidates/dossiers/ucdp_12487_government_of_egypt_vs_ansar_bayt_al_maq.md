# Dossier ucdp_12487_government_of_egypt_vs_ansar_bayt_al_maq — Government of Egypt vs Ansar Bayt al-Maqdis

```json
{
 "id": "ucdp_12487_government_of_egypt_vs_ansar_bayt_al_maq",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "12487",
  "detail": "dyad 12487 Government of Egypt vs Ansar Bayt al-Maqdis (Egypt) onset 2014-05-02 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2014-05-02",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2014-05-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2014: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 12487 **Government of Egypt vs Ansar Bayt al-Maqdis**: dyad 12487 Government of Egypt vs Ansar Bayt al-Maqdis (Egypt) onset 2014-05-02 intensity 1 trigdate 2014-05-02, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2014: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_12487_government_of_egypt_vs_ansar_bayt_al_maq --approved-by joe`. The code never runs it.
