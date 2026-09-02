# Dossier icb_145_dien_bien_phu — DIEN BIEN PHU

```json
{
 "id": "icb_145_dien_bien_phu",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:53+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 145,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=145",
  "trigdate": "1954-03-13",
  "termdate": "1954-07-21",
  "viol": 4,
  "forout": 5
 },
 "event_date": "1954-03-13",
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
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1952-54v16/d417",
  "title": "The Secretary of State to the Department of State (1952\u20131954, Volume XVI, The Geneva Conference)",
  "date": "1954-05-03",
  "window": [
   "1954-02-11",
   "1954-08-20"
  ],
  "query": "Dien Bien Phu 1954",
  "search_url": "https://history.state.gov/search?q=Dien+Bien+Phu+1954&within=documents",
  "retrieved_at": "2026-09-02T19:13:53+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v16/d417",
    "title": "The Secretary of State to the Department of State (1952\u20131954, Volume XVI, The Geneva Conference)",
    "page_date": "1954-05-03",
    "retrieved_at": "2026-09-02T19:13:53+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 145 **DIEN BIEN PHU**: trigdate 1954-03-13, termdate 1954-07-21, viol 4, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=145

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.fra:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:53+00:00: **The Secretary of State to the Department of State (1952–1954, Volume XVI, The Geneva Conference)** — page date 1954-05-03 (window 1954-02-11..1954-08-20)
  https://history.state.gov/historicaldocuments/frus1952-54v16/d417
- search: https://history.state.gov/search?q=Dien+Bien+Phu+1954&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_145_dien_bien_phu --approved-by joe`. The code never runs it.
