# Dossier icb_183_kuwait_independence — KUWAIT INDEPENDENCE

```json
{
 "id": "icb_183_kuwait_independence",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:44+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 183,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=183",
  "trigdate": "1961-06-19",
  "termdate": "1961-07-13",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1961-06-19",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "actor"
  },
  {
   "entity": "country.iraq",
   "role": "target"
  },
  {
   "entity": "country.kuwait",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v17/d75",
  "title": "75. Circular Telegram From the Department of State to Certain Consular and Diplomatic Posts (1961\u20131963, Volume XVII, Near East, 1961\u20131962)",
  "date": "1961-06-30",
  "window": [
   "1961-05-20",
   "1961-08-12"
  ],
  "query": "Kuwait Independence 1961",
  "search_url": "https://history.state.gov/search?q=Kuwait+Independence+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:44+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v17/d75",
    "title": "75. Circular Telegram From the Department of State to Certain Consular and Diplomatic Posts (1961\u20131963, Volume XVII, Near East, 1961\u20131962)",
    "page_date": "1961-06-30",
    "retrieved_at": "2026-09-02T19:14:44+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 183 **KUWAIT INDEPENDENCE**: trigdate 1961-06-19, termdate 1961-07-13, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=183

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 645: country.iraq (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.gbr:actor, country.iraq:target, country.kuwait:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:44+00:00: **75. Circular Telegram From the Department of State to Certain Consular and Diplomatic Posts (1961–1963, Volume XVII, Near East, 1961–1962)** — page date 1961-06-30 (window 1961-05-20..1961-08-12)
  https://history.state.gov/historicaldocuments/frus1961-63v17/d75
- search: https://history.state.gov/search?q=Kuwait+Independence+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_183_kuwait_independence --approved-by joe`. The code never runs it.
