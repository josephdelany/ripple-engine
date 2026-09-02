# Dossier icb_354_nicaragua_mig_21s — NICARAGUA MIG-21S

```json
{
 "id": "icb_354_nicaragua_mig_21s",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:40+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 354,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=354",
  "trigdate": "1984-11-06",
  "termdate": "1984-11-12",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1984-11-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [
  93
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d303",
  "title": "303. Telegram from the Embassy in the Soviet Union to the Department of State (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
  "date": "1984-11-07",
  "window": [
   "1984-10-07",
   "1984-12-12"
  ],
  "query": "Nicaragua Mig S 1984",
  "search_url": "https://history.state.gov/search?q=Nicaragua+Mig+S+1984&within=documents",
  "retrieved_at": "2026-09-02T19:19:39+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v04/d303",
    "title": "303. Telegram from the Embassy in the Soviet Union to the Department of State (1981\u20131988, Volume IV, Soviet Union, January 1983\u2013March 1985)",
    "page_date": "1984-11-07",
    "retrieved_at": "2026-09-02T19:19:39+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 354 **NICARAGUA MIG-21S**: trigdate 1984-11-06, termdate 1984-11-12, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=354

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 93: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:19:39+00:00: **303. Telegram from the Embassy in the Soviet Union to the Department of State (1981–1988, Volume IV, Soviet Union, January 1983–March 1985)** — page date 1984-11-07 (window 1984-10-07..1984-12-12)
  https://history.state.gov/historicaldocuments/frus1981-88v04/d303
- search: https://history.state.gov/search?q=Nicaragua+Mig+S+1984&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_354_nicaragua_mig_21s --approved-by joe`. The code never runs it.
