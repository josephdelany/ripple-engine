# Dossier icb_153_qalqilya — QALQILYA

```json
{
 "id": "icb_153_qalqilya",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:03+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 153,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=153",
  "trigdate": "1956-09-13",
  "termdate": "1956-10-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1956-09-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Qalqilya 1956",
  "search_url": "https://history.state.gov/search?q=Qalqilya+1956&within=documents",
  "search_status": 200,
  "window": [
   "1956-08-14",
   "1956-11-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:03+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 153 **QALQILYA**: trigdate 1956-09-13, termdate 1956-10-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=153

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.jor:target, country.israel:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Qalqilya 1956` (https://history.state.gov/search?q=Qalqilya+1956&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1956-08-14..1956-11-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_153_qalqilya --approved-by joe`. The code never runs it.
