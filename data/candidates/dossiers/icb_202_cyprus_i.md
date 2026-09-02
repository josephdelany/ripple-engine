# Dossier icb_202_cyprus_i — CYPRUS I

```json
{
 "id": "icb_202_cyprus_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:19+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 202,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=202",
  "trigdate": "1963-11-28",
  "termdate": "1964-08-10",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1963-11-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  350,
  352
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v16/d298",
  "title": "298. Telegram from the Embassy in Turkey to the Department of State (1961\u20131963, Volume XVI, Eastern Europe; Cyprus; Greece; Turkey)",
  "date": "1963-12-07",
  "window": [
   "1963-10-29",
   "1964-09-09"
  ],
  "query": "Cyprus I 1963",
  "search_url": "https://history.state.gov/search?q=Cyprus+I+1963&within=documents",
  "retrieved_at": "2026-09-02T19:15:18+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v16/d272",
    "title": "272. Telegram From the Embassy in Cyprus to the Department of State (1961\u20131963, Volume XVI, Eastern Europe; Cyprus; Greece; Turkey)",
    "page_date": "1963-02-13",
    "retrieved_at": "2026-09-02T19:15:18+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v16/d298",
    "title": "298. Telegram from the Embassy in Turkey to the Department of State (1961\u20131963, Volume XVI, Eastern Europe; Cyprus; Greece; Turkey)",
    "page_date": "1963-12-07",
    "retrieved_at": "2026-09-02T19:15:18+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 202 **CYPRUS I**: trigdate 1963-11-28, termdate 1964-08-10, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=202

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 350: UNMAPPED
- 352: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:18+00:00: **298. Telegram from the Embassy in Turkey to the Department of State (1961–1963, Volume XVI, Eastern Europe; Cyprus; Greece; Turkey)** — page date 1963-12-07 (window 1963-10-29..1964-09-09)
  https://history.state.gov/historicaldocuments/frus1961-63v16/d298
- search: https://history.state.gov/search?q=Cyprus+I+1963&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_202_cyprus_i --approved-by joe`. The code never runs it.
