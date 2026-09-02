# Dossier icb_194_china_india_bdr_ii — CHINA/INDIA BDR. II

```json
{
 "id": "icb_194_china_india_bdr_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:04+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 194,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=194",
  "trigdate": "1962-09-08",
  "termdate": "1963-01-23",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1962-09-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "actor"
  },
  {
   "entity": "country.india",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "China India Bdr  Ii 1962",
  "search_url": "https://history.state.gov/search?q=China+India+Bdr++Ii+1962&within=documents",
  "search_status": 200,
  "window": [
   "1962-08-09",
   "1963-02-22"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:15:04+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 194 **CHINA/INDIA BDR. II**: trigdate 1962-09-08, termdate 1963-01-23, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=194

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.china:actor, country.india:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `China India Bdr  Ii 1962` (https://history.state.gov/search?q=China+India+Bdr++Ii+1962&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1962-08-09..1963-02-22.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_194_china_india_bdr_ii --approved-by joe`. The code never runs it.
