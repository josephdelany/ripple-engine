# Dossier icb_169_mex_guat_fishing — MEX./GUAT. FISHING

```json
{
 "id": "icb_169_mex_guat_fishing",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:23+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 169,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=169",
  "trigdate": "1958-12-28",
  "termdate": "1959-02-01",
  "viol": 2,
  "forout": 2
 },
 "event_date": "1958-12-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.mex",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  90
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Mex Guat  Fishing 1958",
  "search_url": "https://history.state.gov/search?q=Mex+Guat++Fishing+1958&within=documents",
  "search_status": 200,
  "window": [
   "1958-11-28",
   "1959-03-03"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:23+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 169 **MEX./GUAT. FISHING**: trigdate 1958-12-28, termdate 1959-02-01, viol 2, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=169

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 70: country.mex (registered state set)
- 90: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.mex:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Mex Guat  Fishing 1958` (https://history.state.gov/search?q=Mex+Guat++Fishing+1958&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1958-11-28..1959-03-03.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_169_mex_guat_fishing --approved-by joe`. The code never runs it.
