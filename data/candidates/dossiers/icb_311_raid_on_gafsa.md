# Dossier icb_311_raid_on_gafsa — RAID ON GAFSA

```json
{
 "id": "icb_311_raid_on_gafsa",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:37+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 311,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=311",
  "trigdate": "1980-01-27",
  "termdate": "1980-04-28",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1980-01-27",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  616
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d204",
  "title": "204. Telegram From the Embassy in Tunisia to the Department of State (1977\u20131980, Volume XVII, Part 3, North Africa)",
  "date": "1980-01-28",
  "window": [
   "1979-12-28",
   "1980-05-28"
  ],
  "query": "Raid On Gafsa 1980",
  "search_url": "https://history.state.gov/search?q=Raid+On+Gafsa+1980&within=documents",
  "retrieved_at": "2026-09-02T19:18:37+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d204",
    "title": "204. Telegram From the Embassy in Tunisia to the Department of State (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1980-01-28",
    "retrieved_at": "2026-09-02T19:18:37+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 311 **RAID ON GAFSA**: trigdate 1980-01-27, termdate 1980-04-28, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=311

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 616: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:37+00:00: **204. Telegram From the Embassy in Tunisia to the Department of State (1977–1980, Volume XVII, Part 3, North Africa)** — page date 1980-01-28 (window 1979-12-28..1980-05-28)
  https://history.state.gov/historicaldocuments/frus1977-80v17p3/d204
- search: https://history.state.gov/search?q=Raid+On+Gafsa+1980&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_311_raid_on_gafsa --approved-by joe`. The code never runs it.
