# Dossier icb_335_khorramshahr — KHORRAMSHAHR

```json
{
 "id": "icb_335_khorramshahr",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 335,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=335",
  "trigdate": "1982-03-22",
  "termdate": "1982-07-28",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1982-03-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Khorramshahr 1982",
  "search_url": "https://history.state.gov/search?q=Khorramshahr+1982&within=documents",
  "search_status": 200,
  "window": [
   "1982-02-20",
   "1982-08-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:14+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 335 **KHORRAMSHAHR**: trigdate 1982-03-22, termdate 1982-07-28, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=335

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.iraq:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Khorramshahr 1982` (https://history.state.gov/search?q=Khorramshahr+1982&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1982-02-20..1982-08-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_335_khorramshahr --approved-by joe`. The code never runs it.
