# Dossier icb_358_egypt_air_hijacking — EGYPT AIR HIJACKING

```json
{
 "id": "icb_358_egypt_air_hijacking",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:43+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 358,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=358",
  "trigdate": "1985-11-23",
  "termdate": "1985-12-03",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1985-11-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  },
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d155",
  "title": "155. Letter From Vice President Bush to Algerian President Bendjedid (1981\u20131988, Volume XXIV, North Africa)",
  "date": "1985-12-17",
  "window": [
   "1985-10-24",
   "1986-01-02"
  ],
  "query": "Egypt Air Hijacking 1985",
  "search_url": "https://history.state.gov/search?q=Egypt+Air+Hijacking+1985&within=documents",
  "retrieved_at": "2026-09-02T19:19:42+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d155",
    "title": "155. Letter From Vice President Bush to Algerian President Bendjedid (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1985-12-17",
    "retrieved_at": "2026-09-02T19:19:42+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 358 **EGYPT AIR HIJACKING**: trigdate 1985-11-23, termdate 1985-12-03, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=358

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown, country.egypt:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:42+00:00: **155. Letter From Vice President Bush to Algerian President Bendjedid (1981–1988, Volume XXIV, North Africa)** — page date 1985-12-17 (window 1985-10-24..1986-01-02)
  https://history.state.gov/historicaldocuments/frus1981-88v24/d155
- search: https://history.state.gov/search?q=Egypt+Air+Hijacking+1985&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_358_egypt_air_hijacking --approved-by joe`. The code never runs it.
