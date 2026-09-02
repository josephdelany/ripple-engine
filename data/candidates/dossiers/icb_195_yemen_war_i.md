# Dossier icb_195_yemen_war_i — YEMEN WAR I

```json
{
 "id": "icb_195_yemen_war_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:07+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 195,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=195",
  "trigdate": "1962-09-26",
  "termdate": "1963-04-15",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1962-09-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d74",
  "title": "74. Draft Memorandum From the Office of National Estimates, Central Intelligence Agency, to Director of Central Intelligence McCone (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
  "date": "1962-10-08",
  "window": [
   "1962-08-27",
   "1963-05-15"
  ],
  "query": "Yemen War I 1962",
  "search_url": "https://history.state.gov/search?q=Yemen+War+I+1962&within=documents",
  "retrieved_at": "2026-09-02T19:15:06+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d177",
    "title": "177. Memorandum From the President\u2019s Assistant for National Security Affairs (Kissinger) to President Nixon (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, Septem",
    "page_date": "1969-12-19",
    "retrieved_at": "2026-09-02T19:15:06+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d74",
    "title": "74. Draft Memorandum From the Office of National Estimates, Central Intelligence Agency, to Director of Central Intelligence McCone (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
    "page_date": "1962-10-08",
    "retrieved_at": "2026-09-02T19:15:06+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 195 **YEMEN WAR I**: trigdate 1962-09-26, termdate 1963-04-15, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=195

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 663: country.jor (registered state set)
- 670: country.saudi_arabia (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown, country.jor:unknown, country.saudi_arabia:unknown, country.yemen:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:06+00:00: **74. Draft Memorandum From the Office of National Estimates, Central Intelligence Agency, to Director of Central Intelligence McCone (1961–1963, Volume XVIII, Near East, 1962–1963)** — page date 1962-10-08 (window 1962-08-27..1963-05-15)
  https://history.state.gov/historicaldocuments/frus1961-63v18/d74
- search: https://history.state.gov/search?q=Yemen+War+I+1962&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_195_yemen_war_i --approved-by joe`. The code never runs it.
