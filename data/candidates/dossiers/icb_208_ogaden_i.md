# Dossier icb_208_ogaden_i — OGADEN I

```json
{
 "id": "icb_208_ogaden_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:27+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 208,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=208",
  "trigdate": "1964-02-07",
  "termdate": "1964-03-28",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1964-02-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520,
  530
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v24/d290",
  "title": "290. Circular Airgram From the Department of State to Certain African Posts (1964\u20131968, Volume XXIV, Africa)",
  "date": "1964-03-21",
  "window": [
   "1964-01-08",
   "1964-04-27"
  ],
  "query": "Ogaden I 1964",
  "search_url": "https://history.state.gov/search?q=Ogaden+I+1964&within=documents",
  "retrieved_at": "2026-09-02T19:15:27+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v24/d290",
    "title": "290. Circular Airgram From the Department of State to Certain African Posts (1964\u20131968, Volume XXIV, Africa)",
    "page_date": "1964-03-21",
    "retrieved_at": "2026-09-02T19:15:27+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 208 **OGADEN I**: trigdate 1964-02-07, termdate 1964-03-28, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=208

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:27+00:00: **290. Circular Airgram From the Department of State to Certain African Posts (1964–1968, Volume XXIV, Africa)** — page date 1964-03-21 (window 1964-01-08..1964-04-27)
  https://history.state.gov/historicaldocuments/frus1964-68v24/d290
- search: https://history.state.gov/search?q=Ogaden+I+1964&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_208_ogaden_i --approved-by joe`. The code never runs it.
