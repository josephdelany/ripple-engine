# Dossier icb_192_taiwan_strait_iii — TAIWAN STRAIT III

```json
{
 "id": "icb_192_taiwan_strait_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 192,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=192",
  "trigdate": "1962-04-22",
  "termdate": "1962-06-27",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1962-04-22",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v22/d122",
  "title": "122. Record of Meeting (1961\u20131963, Volume XXII, Northeast Asia)",
  "date": "1962-06-20",
  "window": [
   "1962-03-23",
   "1962-07-27"
  ],
  "query": "Taiwan Strait Iii 1962",
  "search_url": "https://history.state.gov/search?q=Taiwan+Strait+Iii+1962&within=documents",
  "retrieved_at": "2026-09-02T19:15:00+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v22/d172",
    "title": "172. Memorandum From the Ambassador to the Republic of China (Kirk) to President Kennedy (1961\u20131963, Volume XXII, Northeast Asia)",
    "page_date": "1963-03-29",
    "retrieved_at": "2026-09-02T19:15:00+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v22/d122",
    "title": "122. Record of Meeting (1961\u20131963, Volume XXII, Northeast Asia)",
    "page_date": "1962-06-20",
    "retrieved_at": "2026-09-02T19:15:00+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 192 **TAIWAN STRAIT III**: trigdate 1962-04-22, termdate 1962-06-27, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=192

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.china:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:00+00:00: **122. Record of Meeting (1961–1963, Volume XXII, Northeast Asia)** — page date 1962-06-20 (window 1962-03-23..1962-07-27)
  https://history.state.gov/historicaldocuments/frus1961-63v22/d122
- search: https://history.state.gov/search?q=Taiwan+Strait+Iii+1962&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_192_taiwan_strait_iii --approved-by joe`. The code never runs it.
