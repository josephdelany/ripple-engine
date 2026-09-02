# Dossier icb_348_basra_kharg_island — BASRA-KHARG ISLAND

```json
{
 "id": "icb_348_basra_kharg_island",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:33+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 348,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=348",
  "trigdate": "1984-02-21",
  "termdate": "1984-07-11",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1984-02-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "actor"
  },
  {
   "entity": "country.iraq",
   "role": "target"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "target"
  },
  {
   "entity": "country.kuwait",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Basra Kharg Island 1984",
  "search_url": "https://history.state.gov/search?q=Basra+Kharg+Island+1984&within=documents",
  "search_status": 200,
  "window": [
   "1984-01-22",
   "1984-08-10"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:33+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 348 **BASRA-KHARG ISLAND**: trigdate 1984-02-21, termdate 1984-07-11, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=348

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)
- 670: country.saudi_arabia (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.iran:actor, country.iraq:target, country.saudi_arabia:target, country.kuwait:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Basra Kharg Island 1984` (https://history.state.gov/search?q=Basra+Kharg+Island+1984&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1984-01-22..1984-08-10.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_348_basra_kharg_island --approved-by joe`. The code never runs it.
