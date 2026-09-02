# Dossier icb_111_turkish_straits — TURKISH STRAITS

```json
{
 "id": "icb_111_turkish_straits",
 "built_by": "session A",
 "built_at": "2026-09-02T19:12:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 111,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=111",
  "trigdate": "1946-08-07",
  "termdate": "1946-10-26",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1946-08-07",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.turkey",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1946v07/d700",
  "title": "The Ambassador in Turkey (Wilson) to the Secretary of State (1946, Volume VII, The Near East and Africa)",
  "date": "1946-11-25",
  "window": [
   "1946-07-08",
   "1946-11-25"
  ],
  "query": "Turkish Straits 1946",
  "search_url": "https://history.state.gov/search?q=Turkish+Straits+1946&within=documents",
  "retrieved_at": "2026-09-02T19:10:59+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1946v07/d700",
    "title": "The Ambassador in Turkey (Wilson) to the Secretary of State (1946, Volume VII, The Near East and Africa)",
    "page_date": "1946-11-25",
    "retrieved_at": "2026-09-02T19:10:59+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 111 **TURKISH STRAITS**: trigdate 1946-08-07, termdate 1946-10-26, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=111

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.turkey:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:10:59+00:00: **The Ambassador in Turkey (Wilson) to the Secretary of State (1946, Volume VII, The Near East and Africa)** — page date 1946-11-25 (window 1946-07-08..1946-11-25)
  https://history.state.gov/historicaldocuments/frus1946v07/d700
- search: https://history.state.gov/search?q=Turkish+Straits+1946&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_111_turkish_straits --approved-by joe`. The code never runs it.
