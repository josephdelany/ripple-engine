# Dossier icb_300_raids_on_zipra — RAIDS ON ZIPRA

```json
{
 "id": "icb_300_raids_on_zipra",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:19+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 300,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=300",
  "trigdate": "1979-02-12",
  "termdate": "1979-05-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1979-02-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  551,
  552
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Raids On Zipra 1979",
  "search_url": "https://history.state.gov/search?q=Raids+On+Zipra+1979&within=documents",
  "search_status": 200,
  "window": [
   "1979-01-13",
   "1979-06-27"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v16/d246",
    "title": "246. Summary of Conclusions of a Policy Review Committee Meeting (1977\u20131980, Volume XVI, Southern Africa)",
    "page_date": "1979-11-21",
    "retrieved_at": "2026-09-02T19:18:18+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:17+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 300 **RAIDS ON ZIPRA**: trigdate 1979-02-12, termdate 1979-05-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=300

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)
- 551: UNMAPPED
- 552: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.ago:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Raids On Zipra 1979` (https://history.state.gov/search?q=Raids+On+Zipra+1979&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1979-01-13..1979-06-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 246. Summary of Conclusions of a Policy Review Committee Mee (1979-11-21)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_300_raids_on_zipra --approved-by joe`. The code never runs it.
