# Dossier icb_249_christmas_bombing — CHRISTMAS BOMBING

```json
{
 "id": "icb_249_christmas_bombing",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:43+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 249,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=249",
  "trigdate": "1972-10-23",
  "termdate": "1973-01-27",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1972-10-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "actor"
  },
  {
   "entity": "country.vietnam",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v09/d222",
  "title": "222. Message From the Chairman of the Joint Chiefs of Staff (Moorer) to the Commander in Chief, Pacific (Gayler) and the Commander in Chief, Strategic Air Command (Meyer) (1969\u20131976, Volume IX, Vietna",
  "date": "1972-12-23",
  "window": [
   "1972-09-23",
   "1973-02-26"
  ],
  "query": "Christmas Bombing 1972",
  "search_url": "https://history.state.gov/search?q=Christmas+Bombing+1972&within=documents",
  "retrieved_at": "2026-09-02T19:16:43+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v09/d222",
    "title": "222. Message From the Chairman of the Joint Chiefs of Staff (Moorer) to the Commander in Chief, Pacific (Gayler) and the Commander in Chief, Strategic Air Command (Meyer) (1969\u20131976, Volume IX, Vietna",
    "page_date": "1972-12-23",
    "retrieved_at": "2026-09-02T19:16:43+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 249 **CHRISTMAS BOMBING**: trigdate 1972-10-23, termdate 1973-01-27, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=249

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 816: country.vietnam
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:actor, country.vietnam:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:43+00:00: **222. Message From the Chairman of the Joint Chiefs of Staff (Moorer) to the Commander in Chief, Pacific (Gayler) and the Commander in Chief, Strategic Air Command (Meyer) (1969–1976, Volume IX, Vietna** — page date 1972-12-23 (window 1972-09-23..1973-02-26)
  https://history.state.gov/historicaldocuments/frus1969-76v09/d222
- search: https://history.state.gov/search?q=Christmas+Bombing+1972&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_249_christmas_bombing --approved-by joe`. The code never runs it.
