# Dossier icb_343_invasion_of_grenada — INVASION OF GRENADA

```json
{
 "id": "icb_343_invasion_of_grenada",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 343,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=343",
  "trigdate": "1983-10-19",
  "termdate": "1983-10-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1983-10-19",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  55
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d173",
  "title": "173. Memorandum From Donald Fortier of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (McFarlane) (1981\u20131988, Volume I, Foundations of Foreign Policy)",
  "date": "1983-10-25",
  "window": [
   "1983-09-19",
   "1983-11-27"
  ],
  "query": "Invasion Of Grenada 1983",
  "search_url": "https://history.state.gov/search?q=Invasion+Of+Grenada+1983&within=documents",
  "retrieved_at": "2026-09-02T19:19:27+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d173",
    "title": "173. Memorandum From Donald Fortier of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (McFarlane) (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1983-10-25",
    "retrieved_at": "2026-09-02T19:19:27+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 343 **INVASION OF GRENADA**: trigdate 1983-10-19, termdate 1983-10-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=343

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 55: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:27+00:00: **173. Memorandum From Donald Fortier of the National Security Council Staff to the President’s Assistant for National Security Affairs (McFarlane) (1981–1988, Volume I, Foundations of Foreign Policy)** — page date 1983-10-25 (window 1983-09-19..1983-11-27)
  https://history.state.gov/historicaldocuments/frus1981-88v01/d173
- search: https://history.state.gov/search?q=Invasion+Of+Grenada+1983&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_343_invasion_of_grenada --approved-by joe`. The code never runs it.
