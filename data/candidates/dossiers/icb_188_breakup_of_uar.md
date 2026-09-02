# Dossier icb_188_breakup_of_uar — BREAKUP OF UAR

```json
{
 "id": "icb_188_breakup_of_uar",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:58+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 188,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=188",
  "trigdate": "1961-09-28",
  "termdate": "1961-10-05",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1961-09-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v17/d123",
  "title": "123. National Intelligence Estimate (1961\u20131963, Volume XVII, Near East, 1961\u20131962)",
  "date": "1961-10-05",
  "window": [
   "1961-08-29",
   "1961-11-04"
  ],
  "query": "Breakup Of Uar 1961",
  "search_url": "https://history.state.gov/search?q=Breakup+Of+Uar+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:58+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v18/d38",
    "title": "38. Memorandum From the Director of Intelligence and Research (Hilsman) to Secretary of State Rusk (1961\u20131963, Volume XVIII, Near East, 1962\u20131963)",
    "page_date": "1962-09-13",
    "retrieved_at": "2026-09-02T19:14:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v17/d68",
    "title": "68. National Intelligence Estimate (1961\u20131963, Volume XVII, Near East, 1961\u20131962)",
    "page_date": "1961-06-27",
    "retrieved_at": "2026-09-02T19:14:57+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v17/d123",
    "title": "123. National Intelligence Estimate (1961\u20131963, Volume XVII, Near East, 1961\u20131962)",
    "page_date": "1961-10-05",
    "retrieved_at": "2026-09-02T19:14:58+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 188 **BREAKUP OF UAR**: trigdate 1961-09-28, termdate 1961-10-05, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=188

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:58+00:00: **123. National Intelligence Estimate (1961–1963, Volume XVII, Near East, 1961–1962)** — page date 1961-10-05 (window 1961-08-29..1961-11-04)
  https://history.state.gov/historicaldocuments/frus1961-63v17/d123
- search: https://history.state.gov/search?q=Breakup+Of+Uar+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_188_breakup_of_uar --approved-by joe`. The code never runs it.
