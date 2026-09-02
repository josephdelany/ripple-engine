# Dossier icb_216_kashmir_ii — KASHMIR II

```json
{
 "id": "icb_216_kashmir_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 216,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=216",
  "trigdate": "1965-08-05",
  "termdate": "1966-01-10",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1965-08-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "target"
  },
  {
   "entity": "country.pak",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v25/d195",
  "title": "195. Memorandum for the Record (1964\u20131968, Volume XXV, South Asia)",
  "date": "1965-09-09",
  "window": [
   "1965-07-06",
   "1966-02-09"
  ],
  "query": "Kashmir Ii 1965",
  "search_url": "https://history.state.gov/search?q=Kashmir+Ii+1965&within=documents",
  "retrieved_at": "2026-09-02T19:15:46+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v25/d195",
    "title": "195. Memorandum for the Record (1964\u20131968, Volume XXV, South Asia)",
    "page_date": "1965-09-09",
    "retrieved_at": "2026-09-02T19:15:46+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 216 **KASHMIR II**: trigdate 1965-08-05, termdate 1966-01-10, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=216

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.india:target, country.pak:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:46+00:00: **195. Memorandum for the Record (1964–1968, Volume XXV, South Asia)** — page date 1965-09-09 (window 1965-07-06..1966-02-09)
  https://history.state.gov/historicaldocuments/frus1964-68v25/d195
- search: https://history.state.gov/search?q=Kashmir+Ii+1965&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_216_kashmir_ii --approved-by joe`. The code never runs it.
