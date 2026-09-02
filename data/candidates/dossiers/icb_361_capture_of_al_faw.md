# Dossier icb_361_capture_of_al_faw — CAPTURE OF AL-FAW

```json
{
 "id": "icb_361_capture_of_al_faw",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:44+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 361,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=361",
  "trigdate": "1986-02-09",
  "termdate": "1986-04-28",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1986-02-09",
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
  "query": "Capture Of Al Faw 1986",
  "search_url": "https://history.state.gov/search?q=Capture+Of+Al+Faw+1986&within=documents",
  "search_status": 200,
  "window": [
   "1986-01-10",
   "1986-05-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:43+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 361 **CAPTURE OF AL-FAW**: trigdate 1986-02-09, termdate 1986-04-28, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=361

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)
- 670: country.saudi_arabia (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.iran:actor, country.iraq:target, country.saudi_arabia:target, country.kuwait:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Capture Of Al Faw 1986` (https://history.state.gov/search?q=Capture+Of+Al+Faw+1986&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-01-10..1986-05-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_361_capture_of_al_faw --approved-by joe`. The code never runs it.
