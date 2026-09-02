# Dossier icb_206_panama_flag — PANAMA FLAG

```json
{
 "id": "icb_206_panama_flag",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:23+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 206,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=206",
  "trigdate": "1964-01-09",
  "termdate": "1964-01-12",
  "viol": 2,
  "forout": 5
 },
 "event_date": "1964-01-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "actor"
  },
  {
   "entity": "country.panama",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v31/d374",
  "title": "374. Telegram From President Johnson to the Assistant Secretary of State for Inter-American Affairs (Mann) in Panama (1964\u20131968, Volume XXXI, South and Central America; Mexico)",
  "date": "1964-01-11",
  "window": [
   "1963-12-10",
   "1964-02-11"
  ],
  "query": "Panama Flag 1964",
  "search_url": "https://history.state.gov/search?q=Panama+Flag+1964&within=documents",
  "retrieved_at": "2026-09-02T19:15:23+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v31/d374",
    "title": "374. Telegram From President Johnson to the Assistant Secretary of State for Inter-American Affairs (Mann) in Panama (1964\u20131968, Volume XXXI, South and Central America; Mexico)",
    "page_date": "1964-01-11",
    "retrieved_at": "2026-09-02T19:15:23+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 206 **PANAMA FLAG**: trigdate 1964-01-09, termdate 1964-01-12, viol 2, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=206

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 95: country.panama (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:actor, country.panama:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:23+00:00: **374. Telegram From President Johnson to the Assistant Secretary of State for Inter-American Affairs (Mann) in Panama (1964–1968, Volume XXXI, South and Central America; Mexico)** — page date 1964-01-11 (window 1963-12-10..1964-02-11)
  https://history.state.gov/historicaldocuments/frus1964-68v31/d374
- search: https://history.state.gov/search?q=Panama+Flag+1964&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_206_panama_flag --approved-by joe`. The code never runs it.
