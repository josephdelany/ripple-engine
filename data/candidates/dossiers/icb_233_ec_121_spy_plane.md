# Dossier icb_233_ec_121_spy_plane — EC-121 SPY PLANE

```json
{
 "id": "icb_233_ec_121_spy_plane",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:20+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 233,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=233",
  "trigdate": "1969-04-15",
  "termdate": "1969-04-26",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1969-04-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Ec  Spy Plane 1969",
  "search_url": "https://history.state.gov/search?q=Ec++Spy+Plane+1969&within=documents",
  "search_status": 200,
  "window": [
   "1969-03-16",
   "1969-05-26"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v29p1/d331",
    "title": "331. Editorial Note (1964\u20131968, Volume XXIX, Part 1, Korea)",
    "page_date": "1968-12-23",
    "retrieved_at": "2026-09-02T19:16:19+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:18+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 233 **EC-121 SPY PLANE**: trigdate 1969-04-15, termdate 1969-04-26, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=233

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ec  Spy Plane 1969` (https://history.state.gov/search?q=Ec++Spy+Plane+1969&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1969-03-16..1969-05-26.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 331. Editorial Note (1964–1968, Volume XXIX, Part 1, Korea) (1968-12-23)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_233_ec_121_spy_plane --approved-by joe`. The code never runs it.
