# Dossier icb_344_able_archer_83 — ABLE ARCHER 83

```json
{
 "id": "icb_344_able_archer_83",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 344,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=344",
  "trigdate": "1983-11-02",
  "termdate": "1983-11-11",
  "viol": 1,
  "forout": 7
 },
 "event_date": "1983-11-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d134",
  "title": "134. Article in the National Intelligence Daily (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
  "date": "1983-11-10",
  "window": [
   "1983-10-03",
   "1983-12-11"
  ],
  "query": "Able Archer 1983",
  "search_url": "https://history.state.gov/search?q=Able+Archer+1983&within=documents",
  "retrieved_at": "2026-09-02T19:19:30+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d135",
    "title": "135. Editorial Note (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
    "page_date": "1982-11-12",
    "retrieved_at": "2026-09-02T19:19:29+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d134",
    "title": "134. Article in the National Intelligence Daily (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
    "page_date": "1983-11-10",
    "retrieved_at": "2026-09-02T19:19:30+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 344 **ABLE ARCHER 83**: trigdate 1983-11-02, termdate 1983-11-11, viol 1, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=344

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:30+00:00: **134. Article in the National Intelligence Daily (1981–1988, Volume IV, Soviet Union, January 1983–March 1985)** — page date 1983-11-10 (window 1983-10-03..1983-12-11)
  https://history.state.gov/historicaldocuments/frus1981-88v04/d134
- search: https://history.state.gov/search?q=Able+Archer+1983&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_344_able_archer_83 --approved-by joe`. The code never runs it.
