# Dossier icb_287_beagle_channel_i — BEAGLE CHANNEL I

```json
{
 "id": "icb_287_beagle_channel_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:49+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 287,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=287",
  "trigdate": "1977-12-05",
  "termdate": "1978-02-20",
  "viol": 1,
  "forout": 1
 },
 "event_date": "1977-12-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.chile",
   "role": "target"
  },
  {
   "entity": "country.argentina",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d27",
  "title": "27. Editorial Note (1977\u20131980, Volume XXIV, South America; Latin America Region)",
  "date": "1978-02-14",
  "window": [
   "1977-11-05",
   "1978-03-22"
  ],
  "query": "Beagle Channel I 1977",
  "search_url": "https://history.state.gov/search?q=Beagle+Channel+I+1977&within=documents",
  "retrieved_at": "2026-09-02T19:17:49+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d42",
    "title": "42. Telegram From the Department of State to the Embassy in Argentina (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1978-12-21",
    "retrieved_at": "2026-09-02T19:17:47+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d84",
    "title": "84. Memorandum From Robert Pastor of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Brzezinski) and the President\u2019s Deputy Assistant for National Secur",
    "page_date": "1978-08-09",
    "retrieved_at": "2026-09-02T19:17:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d27",
    "title": "27. Editorial Note (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1978-02-14",
    "retrieved_at": "2026-09-02T19:17:49+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 287 **BEAGLE CHANNEL I**: trigdate 1977-12-05, termdate 1978-02-20, viol 1, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=287

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 155: country.chile
- 160: country.argentina (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.chile:target, country.argentina:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:49+00:00: **27. Editorial Note (1977–1980, Volume XXIV, South America; Latin America Region)** — page date 1978-02-14 (window 1977-11-05..1978-03-22)
  https://history.state.gov/historicaldocuments/frus1977-80v24/d27
- search: https://history.state.gov/search?q=Beagle+Channel+I+1977&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_287_beagle_channel_i --approved-by joe`. The code never runs it.
