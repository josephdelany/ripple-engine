# Dossier icb_230_vietnam_spring_off — VIETNAM SPRING OFF.

```json
{
 "id": "icb_230_vietnam_spring_off",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:14+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 230,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=230",
  "trigdate": "1969-02-22",
  "termdate": "1969-06-08",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1969-02-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v12/d50",
  "title": "50. Memorandum From Helmut Sonnenfeldt of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XII, Soviet Union, January 1969\u2013",
  "date": "1969-05-22",
  "window": [
   "1969-01-23",
   "1969-07-08"
  ],
  "query": "Vietnam Spring Off 1969",
  "search_url": "https://history.state.gov/search?q=Vietnam+Spring+Off+1969&within=documents",
  "retrieved_at": "2026-09-02T19:16:14+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v06/d147",
    "title": "147. Backchannel Message From the Ambassador to Vietnam (Bunker) to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume VI, Vietnam, January 1969\u2013July 1970)",
    "page_date": "1969-11-15",
    "retrieved_at": "2026-09-02T19:16:10+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v07/d174",
    "title": "174. Editorial Note (1969\u20131976, Volume VII, Vietnam, July 1970\u2013January 1972)",
    "page_date": "1971-04-07",
    "retrieved_at": "2026-09-02T19:16:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v07/d274",
    "title": "274. Editorial Note (1964\u20131968, Volume VII, Vietnam, September 1968\u2013January 1969)",
    "page_date": "1969-01-06",
    "retrieved_at": "2026-09-02T19:16:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v06/d167",
    "title": "167. Memorandum From the President\u2019s Assistant for National Security Affairs (Kissinger) to President Nixon (1969\u20131976, Volume VI, Vietnam, January 1969\u2013July 1970)",
    "page_date": "1970-01-07",
    "retrieved_at": "2026-09-02T19:16:12+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v41/d320",
    "title": "320. Memorandum of Conversations (1969\u20131976, Volume XLI, Western Europe; NATO, 1969\u20131972)",
    "page_date": "1969-11-03",
    "retrieved_at": "2026-09-02T19:16:13+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v12/d50",
    "title": "50. Memorandum From Helmut Sonnenfeldt of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XII, Soviet Union, January 1969\u2013",
    "page_date": "1969-05-22",
    "retrieved_at": "2026-09-02T19:16:14+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 230 **VIETNAM SPRING OFF.**: trigdate 1969-02-22, termdate 1969-06-08, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=230

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:14+00:00: **50. Memorandum From Helmut Sonnenfeldt of the National Security Council Staff to the President’s Assistant for National Security Affairs (Kissinger) (1969–1976, Volume XII, Soviet Union, January 1969–** — page date 1969-05-22 (window 1969-01-23..1969-07-08)
  https://history.state.gov/historicaldocuments/frus1969-76v12/d50
- search: https://history.state.gov/search?q=Vietnam+Spring+Off+1969&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_230_vietnam_spring_off --approved-by joe`. The code never runs it.
