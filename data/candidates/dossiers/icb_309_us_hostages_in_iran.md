# Dossier icb_309_us_hostages_in_iran — US HOSTAGES IN IRAN

```json
{
 "id": "icb_309_us_hostages_in_iran",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 309,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=309",
  "trigdate": "1979-11-04",
  "termdate": "1981-01-20",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1979-11-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.iran",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v06/d237",
  "title": "237. Telegram From the Department of State to the Embassy in the Soviet Union (1977\u20131980, Volume VI, Soviet Union)",
  "date": "1979-12-08",
  "window": [
   "1979-10-05",
   "1981-02-19"
  ],
  "query": "Us Hostages In Iran 1979",
  "search_url": "https://history.state.gov/search?q=Us+Hostages+In+Iran+1979&within=documents",
  "retrieved_at": "2026-09-02T19:18:30+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v06/d237",
    "title": "237. Telegram From the Department of State to the Embassy in the Soviet Union (1977\u20131980, Volume VI, Soviet Union)",
    "page_date": "1979-12-08",
    "retrieved_at": "2026-09-02T19:18:30+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 309 **US HOSTAGES IN IRAN**: trigdate 1979-11-04, termdate 1981-01-20, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=309

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.iran:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:30+00:00: **237. Telegram From the Department of State to the Embassy in the Soviet Union (1977–1980, Volume VI, Soviet Union)** — page date 1979-12-08 (window 1979-10-05..1981-02-19)
  https://history.state.gov/historicaldocuments/frus1977-80v06/d237
- search: https://history.state.gov/search?q=Us+Hostages+In+Iran+1979&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_309_us_hostages_in_iran --approved-by joe`. The code never runs it.
