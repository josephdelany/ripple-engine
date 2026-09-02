# Dossier icb_386_libyan_jets — LIBYAN JETS

```json
{
 "id": "icb_386_libyan_jets",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 386,
  "source": "icb",
  "source_id": "386",
  "detail": "LIBYAN JETS 1988-12-21..1989-01-12 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=386",
  "trigdate": "1988-12-21",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1988-12-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Libyan Jets 1988",
  "search_url": "https://history.state.gov/search?q=Libyan+Jets+1988&within=documents",
  "search_status": 200,
  "window": [
   "1988-11-21",
   "1989-01-20"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d319",
    "title": "319. Telegram From the Department of State to the Embassy in Tunisia (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1984-11-17",
    "retrieved_at": "2026-09-02T19:52:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d156",
    "title": "156. Telegram From the Embassy in Algeria to the Department of State (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1986-01-08",
    "retrieved_at": "2026-09-02T19:52:56+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:52:55+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 386 **LIBYAN JETS**: LIBYAN JETS 1988-12-21..1989-01-12 viol 2.0 trigdate 1988-12-21, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=386

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Libyan Jets 1988` (https://history.state.gov/search?q=Libyan+Jets+1988&within=documents, HTTP 200) returned 2 document(s) opened, none dated inside 1988-11-21..1989-01-20. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 319. Telegram From the Department of State to the Embassy in (1984-11-17); 156. Telegram From the Embassy in Algeria to the Department  (1986-01-08)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_386_libyan_jets --approved-by joe`. The code never runs it.
