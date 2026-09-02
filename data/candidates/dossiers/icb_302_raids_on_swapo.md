# Dossier icb_302_raids_on_swapo — RAIDS ON SWAPO

```json
{
 "id": "icb_302_raids_on_swapo",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:24+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 302,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=302",
  "trigdate": "1979-03-06",
  "termdate": "1979-03-28",
  "viol": 2,
  "forout": 6
 },
 "event_date": "1979-03-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v16/d111",
  "title": "111. Telegram From Secretary of State Vance to the Department of State (1977\u20131980, Volume XVI, Southern Africa)",
  "date": "1979-03-19",
  "window": [
   "1979-02-04",
   "1979-04-27"
  ],
  "query": "Raids On Swapo 1979",
  "search_url": "https://history.state.gov/search?q=Raids+On+Swapo+1979&within=documents",
  "retrieved_at": "2026-09-02T19:18:24+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v16/d111",
    "title": "111. Telegram From Secretary of State Vance to the Department of State (1977\u20131980, Volume XVI, Southern Africa)",
    "page_date": "1979-03-19",
    "retrieved_at": "2026-09-02T19:18:24+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 302 **RAIDS ON SWAPO**: trigdate 1979-03-06, termdate 1979-03-28, viol 2, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=302

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.ago:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:24+00:00: **111. Telegram From Secretary of State Vance to the Department of State (1977–1980, Volume XVI, Southern Africa)** — page date 1979-03-19 (window 1979-02-04..1979-04-27)
  https://history.state.gov/historicaldocuments/frus1977-80v16/d111
- search: https://history.state.gov/search?q=Raids+On+Swapo+1979&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_302_raids_on_swapo --approved-by joe`. The code never runs it.
