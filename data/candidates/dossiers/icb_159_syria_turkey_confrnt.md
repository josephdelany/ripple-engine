# Dossier icb_159_syria_turkey_confrnt — SYRIA/TURKEY CONFRNT.

```json
{
 "id": "icb_159_syria_turkey_confrnt",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:11+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 159,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=159",
  "trigdate": "1957-08-18",
  "termdate": "1957-10-28",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1957-08-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.turkey",
   "role": "target"
  },
  {
   "entity": "country.syr",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Syria Turkey Confrnt 1957",
  "search_url": "https://history.state.gov/search?q=Syria+Turkey+Confrnt+1957&within=documents",
  "search_status": 200,
  "window": [
   "1957-07-19",
   "1957-11-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:11+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 159 **SYRIA/TURKEY CONFRNT.**: trigdate 1957-08-18, termdate 1957-10-28, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=159

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 640: country.turkey (registered state set)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.turkey:target, country.syr:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Syria Turkey Confrnt 1957` (https://history.state.gov/search?q=Syria+Turkey+Confrnt+1957&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1957-07-19..1957-11-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_159_syria_turkey_confrnt --approved-by joe`. The code never runs it.
