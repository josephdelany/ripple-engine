# Dossier icb_166_taiwan_strait_ii — TAIWAN STRAIT II

```json
{
 "id": "icb_166_taiwan_strait_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:20+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 166,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=166",
  "trigdate": "1958-07-17",
  "termdate": "1958-10-23",
  "viol": 3,
  "forout": 3
 },
 "event_date": "1958-07-17",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.china",
   "role": "actor"
  },
  {
   "entity": "country.taiwan",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1958-60v19/d25",
  "title": "25. Telegram From the Embassy in the Republic of China to the Department of State (1958\u20131960, Volume XIX, China)",
  "date": "1958-08-07",
  "window": [
   "1958-06-17",
   "1958-11-22"
  ],
  "query": "Taiwan Strait Ii 1958",
  "search_url": "https://history.state.gov/search?q=Taiwan+Strait+Ii+1958&within=documents",
  "retrieved_at": "2026-09-02T19:14:20+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v19/d25",
    "title": "25. Telegram From the Embassy in the Republic of China to the Department of State (1958\u20131960, Volume XIX, China)",
    "page_date": "1958-08-07",
    "retrieved_at": "2026-09-02T19:14:20+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 166 **TAIWAN STRAIT II**: trigdate 1958-07-17, termdate 1958-10-23, viol 3, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=166

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 710: country.china (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.china:actor, country.taiwan:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:20+00:00: **25. Telegram From the Embassy in the Republic of China to the Department of State (1958–1960, Volume XIX, China)** — page date 1958-08-07 (window 1958-06-17..1958-11-22)
  https://history.state.gov/historicaldocuments/frus1958-60v19/d25
- search: https://history.state.gov/search?q=Taiwan+Strait+Ii+1958&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_166_taiwan_strait_ii --approved-by joe`. The code never runs it.
