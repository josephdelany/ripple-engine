# Dossier icb_336_falklands_malvinas — FALKLANDS/MALVINAS

```json
{
 "id": "icb_336_falklands_malvinas",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:16+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 336,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=336",
  "trigdate": "1982-03-28",
  "termdate": "1982-06-14",
  "viol": 4,
  "forout": 5
 },
 "event_date": "1982-03-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.argentina",
   "role": "actor"
  },
  {
   "entity": "country.gbr",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v13/d53",
  "title": "53. Memorandum From James M. Rentschler, Dennis C. Blair, and Roger Fontaine of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Clark) (1981\u20131988, Volum",
  "date": "1982-04-02",
  "window": [
   "1982-02-26",
   "1982-07-14"
  ],
  "query": "Falklands Malvinas 1982",
  "search_url": "https://history.state.gov/search?q=Falklands+Malvinas+1982&within=documents",
  "retrieved_at": "2026-09-02T19:19:16+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v13/d53",
    "title": "53. Memorandum From James M. Rentschler, Dennis C. Blair, and Roger Fontaine of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Clark) (1981\u20131988, Volum",
    "page_date": "1982-04-02",
    "retrieved_at": "2026-09-02T19:19:16+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 336 **FALKLANDS/MALVINAS**: trigdate 1982-03-28, termdate 1982-06-14, viol 4, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=336

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 160: country.argentina (registered state set)
- 200: country.gbr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.argentina:actor, country.gbr:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:16+00:00: **53. Memorandum From James M. Rentschler, Dennis C. Blair, and Roger Fontaine of the National Security Council Staff to the President’s Assistant for National Security Affairs (Clark) (1981–1988, Volum** — page date 1982-04-02 (window 1982-02-26..1982-07-14)
  https://history.state.gov/historicaldocuments/frus1981-88v13/d53
- search: https://history.state.gov/search?q=Falklands+Malvinas+1982&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_336_falklands_malvinas --approved-by joe`. The code never runs it.
