# Dossier ucdp_11199_government_of_afghanistan_vs_government_ — Government of Afghanistan vs Government of United Kingdom, Government of United States of America

```json
{
 "id": "ucdp_11199_government_of_afghanistan_vs_government_",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "11199",
  "detail": "dyad 11199 Government of Afghanistan vs Government of United Kingdom, Government of United States of America (Afghanistan, United Kingdom, United States of America) onset 2001-10-07 intensity 2",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2001-10-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2001-10-07",
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
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.afg",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2001: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 11199 **Government of Afghanistan vs Government of United Kingdom, Government of United States of America**: dyad 11199 Government of Afghanistan vs Government of United Kingdom, Government of United States of America (Afghanistan, United Kingdom, United States of America) onset 2001-10-07 intensity 2 trigdate 2001-10-07, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 700: country.afg

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.afg:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2001: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_11199_government_of_afghanistan_vs_government_ --approved-by joe`. The code never runs it.
