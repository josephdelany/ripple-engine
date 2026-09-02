# Dossier ucdp_902_government_of_djibouti_vs_government_of_ — Government of Djibouti vs Government of Eritrea

```json
{
 "id": "ucdp_902_government_of_djibouti_vs_government_of_",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "902",
  "detail": "dyad 902 Government of Djibouti vs Government of Eritrea (Djibouti, Eritrea) onset 2008-06-11 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2008-06-11",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2008-06-11",
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
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 902 **Government of Djibouti vs Government of Eritrea**: dyad 902 Government of Djibouti vs Government of Eritrea (Djibouti, Eritrea) onset 2008-06-11 intensity 1 trigdate 2008-06-11, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

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
`python3 src/admit.py --dossier ucdp_902_government_of_djibouti_vs_government_of_ --approved-by joe`. The code never runs it.
