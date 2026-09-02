# Dossier icb_319_jordan_syria_confrnt — JORDAN/SYRIA CONFRNT.

```json
{
 "id": "icb_319_jordan_syria_confrnt",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:50+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 319,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=319",
  "trigdate": "1980-11-25",
  "termdate": "1980-12-14",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1980-11-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Jordan Syria Confrnt 1980",
  "search_url": "https://history.state.gov/search?q=Jordan+Syria+Confrnt+1980&within=documents",
  "search_status": 200,
  "window": [
   "1980-10-26",
   "1981-01-13"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:49+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 319 **JORDAN/SYRIA CONFRNT.**: trigdate 1980-11-25, termdate 1980-12-14, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=319

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.jor:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Jordan Syria Confrnt 1980` (https://history.state.gov/search?q=Jordan+Syria+Confrnt+1980&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1980-10-26..1981-01-13.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_319_jordan_syria_confrnt --approved-by joe`. The code never runs it.
