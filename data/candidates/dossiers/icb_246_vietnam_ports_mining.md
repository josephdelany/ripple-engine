# Dossier icb_246_vietnam_ports_mining — VIETNAM PORTS MINING

```json
{
 "id": "icb_246_vietnam_ports_mining",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:39+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 246,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=246",
  "trigdate": "1972-03-28",
  "termdate": "1972-07-19",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1972-03-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.vietnam",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v08/d136",
  "title": "136. Editorial Note (1969\u20131976, Volume VIII, Vietnam, January\u2013October 1972)",
  "date": "1972-05-08",
  "window": [
   "1972-02-27",
   "1972-08-18"
  ],
  "query": "Vietnam Ports Mining 1972",
  "search_url": "https://history.state.gov/search?q=Vietnam+Ports+Mining+1972&within=documents",
  "retrieved_at": "2026-09-02T19:16:38+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v08/d136",
    "title": "136. Editorial Note (1969\u20131976, Volume VIII, Vietnam, January\u2013October 1972)",
    "page_date": "1972-05-08",
    "retrieved_at": "2026-09-02T19:16:38+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 246 **VIETNAM PORTS MINING**: trigdate 1972-03-28, termdate 1972-07-19, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=246

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 816: country.vietnam
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.vietnam:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:38+00:00: **136. Editorial Note (1969–1976, Volume VIII, Vietnam, January–October 1972)** — page date 1972-05-08 (window 1972-02-27..1972-08-18)
  https://history.state.gov/historicaldocuments/frus1969-76v08/d136
- search: https://history.state.gov/search?q=Vietnam+Ports+Mining+1972&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_246_vietnam_ports_mining --approved-by joe`. The code never runs it.
