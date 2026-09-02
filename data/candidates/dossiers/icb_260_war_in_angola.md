# Dossier icb_260_war_in_angola — WAR IN ANGOLA

```json
{
 "id": "icb_260_war_in_angola",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:12+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 260,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=260",
  "trigdate": "1975-07-12",
  "termdate": "1976-03-27",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1975-07-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  },
  {
   "entity": "country.ago",
   "role": "unknown"
  },
  {
   "entity": "country.south_africa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  40,
  551
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v16/d222",
  "title": "222. Note From the Soviet Leadership to the Department of State (1969\u20131976, Volume XVI, Soviet Union, August 1974\u2013December 1976)",
  "date": "1975-11-03",
  "window": [
   "1975-06-12",
   "1976-04-26"
  ],
  "query": "War In Angola 1975",
  "search_url": "https://history.state.gov/search?q=War+In+Angola+1975&within=documents",
  "retrieved_at": "2026-09-02T19:17:12+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v28/d105",
    "title": "105. National Security Study Memorandum 224 (1969\u20131976, Volume XXVIII, Southern Africa)",
    "page_date": "1975-05-26",
    "retrieved_at": "2026-09-02T19:17:10+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v28/d154",
    "title": "154. Message From the Soviet Leadership to President Ford (1969\u20131976, Volume XXVIII, Southern Africa)",
    "page_date": "1973-12-06",
    "retrieved_at": "2026-09-02T19:17:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v28/d107",
    "title": "107. Central Intelligence Agency Intelligence Information Cable (1969\u20131976, Volume XXVIII, Southern Africa)",
    "page_date": "1975-06-09",
    "retrieved_at": "2026-09-02T19:17:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v16/d222",
    "title": "222. Note From the Soviet Leadership to the Department of State (1969\u20131976, Volume XVI, Soviet Union, August 1974\u2013December 1976)",
    "page_date": "1975-11-03",
    "retrieved_at": "2026-09-02T19:17:12+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 260 **WAR IN ANGOLA**: trigdate 1975-07-12, termdate 1976-03-27, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=260

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 40: UNMAPPED
- 365: country.russia (registered state set)
- 490: country.congo_drc
- 540: country.ago (registered state set)
- 551: UNMAPPED
- 560: country.south_africa

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.russia:unknown, country.congo_drc:unknown, country.ago:unknown, country.south_africa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:12+00:00: **222. Note From the Soviet Leadership to the Department of State (1969–1976, Volume XVI, Soviet Union, August 1974–December 1976)** — page date 1975-11-03 (window 1975-06-12..1976-04-26)
  https://history.state.gov/historicaldocuments/frus1969-76v16/d222
- search: https://history.state.gov/search?q=War+In+Angola+1975&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_260_war_in_angola --approved-by joe`. The code never runs it.
