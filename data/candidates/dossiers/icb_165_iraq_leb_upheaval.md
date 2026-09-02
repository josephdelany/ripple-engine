# Dossier icb_165_iraq_leb_upheaval — IRAQ/LEB. UPHEAVAL

```json
{
 "id": "icb_165_iraq_leb_upheaval",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:19+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 165,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=165",
  "trigdate": "1958-05-08",
  "termdate": "1958-10-28",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1958-05-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
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
   "entity": "country.lebanon",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Iraq Leb  Upheaval 1958",
  "search_url": "https://history.state.gov/search?q=Iraq+Leb++Upheaval+1958&within=documents",
  "search_status": 200,
  "window": [
   "1958-04-08",
   "1958-11-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:18+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 165 **IRAQ/LEB. UPHEAVAL**: trigdate 1958-05-08, termdate 1958-10-28, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=165

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 660: country.lebanon (registered state set)
- 663: country.jor (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.lebanon:unknown, country.jor:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraq Leb  Upheaval 1958` (https://history.state.gov/search?q=Iraq+Leb++Upheaval+1958&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1958-04-08..1958-11-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_165_iraq_leb_upheaval --approved-by joe`. The code never runs it.
