# Dossier icb_142_trieste_ii — TRIESTE II

```json
{
 "id": "icb_142_trieste_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:45+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 142,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=142",
  "trigdate": "1953-10-08",
  "termdate": "1953-12-05",
  "viol": 1,
  "forout": 1
 },
 "event_date": "1953-10-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.serbia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  325
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1952-54v08/d136",
  "title": "No. 136Memorandum by the Assistant Secretary of State for European Affairs (Merchant) to the Secretary of State (1952\u20131954, Volume VIII, Eastern Europe; Soviet Union; Eastern Mediterranean)",
  "date": "1953-10-14",
  "window": [
   "1953-09-08",
   "1954-01-04"
  ],
  "query": "Trieste Ii 1953",
  "search_url": "https://history.state.gov/search?q=Trieste+Ii+1953&within=documents",
  "retrieved_at": "2026-09-02T19:13:45+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v08/d136",
    "title": "No. 136Memorandum by the Assistant Secretary of State for European Affairs (Merchant) to the Secretary of State (1952\u20131954, Volume VIII, Eastern Europe; Soviet Union; Eastern Mediterranean)",
    "page_date": "1953-10-14",
    "retrieved_at": "2026-09-02T19:13:45+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 142 **TRIESTE II**: trigdate 1953-10-08, termdate 1953-12-05, viol 1, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=142

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 325: UNMAPPED (registered state set)
- 345: country.serbia

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.serbia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:45+00:00: **No. 136Memorandum by the Assistant Secretary of State for European Affairs (Merchant) to the Secretary of State (1952–1954, Volume VIII, Eastern Europe; Soviet Union; Eastern Mediterranean)** — page date 1953-10-14 (window 1953-09-08..1954-01-04)
  https://history.state.gov/historicaldocuments/frus1952-54v08/d136
- search: https://history.state.gov/search?q=Trieste+Ii+1953&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_142_trieste_ii --approved-by joe`. The code never runs it.
