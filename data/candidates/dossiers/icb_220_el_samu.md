# Dossier icb_220_el_samu — EL SAMU

```json
{
 "id": "icb_220_el_samu",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:52+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 220,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=220",
  "trigdate": "1966-11-12",
  "termdate": "1966-11-15",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1966-11-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "El Samu 1966",
  "search_url": "https://history.state.gov/search?q=El+Samu+1966&within=documents",
  "search_status": 200,
  "window": [
   "1966-10-13",
   "1966-12-15"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:15:52+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 220 **EL SAMU**: trigdate 1966-11-12, termdate 1966-11-15, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=220

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.jor:unknown, country.israel:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `El Samu 1966` (https://history.state.gov/search?q=El+Samu+1966&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1966-10-13..1966-12-15.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_220_el_samu --approved-by joe`. The code never runs it.
