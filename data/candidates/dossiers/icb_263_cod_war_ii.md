# Dossier icb_263_cod_war_ii — COD WAR II

```json
{
 "id": "icb_263_cod_war_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:18+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 263,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=263",
  "trigdate": "1975-11-23",
  "termdate": "1976-06-01",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1975-11-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  395
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Cod War Ii 1975",
  "search_url": "https://history.state.gov/search?q=Cod+War+Ii+1975&within=documents",
  "search_status": 200,
  "window": [
   "1975-10-24",
   "1976-07-01"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v10/d195",
    "title": "195. Draft Memorandum From Secretary of Defense McNamara to President Johnson (1964\u20131968, Volume X, National Security Policy)",
    "page_date": "1967-12-01",
    "retrieved_at": "2026-09-02T19:17:18+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:17+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 263 **COD WAR II**: trigdate 1975-11-23, termdate 1976-06-01, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=263

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 395: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cod War Ii 1975` (https://history.state.gov/search?q=Cod+War+Ii+1975&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1975-10-24..1976-07-01.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 195. Draft Memorandum From Secretary of Defense McNamara to  (1967-12-01)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_263_cod_war_ii --approved-by joe`. The code never runs it.
