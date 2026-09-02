# Dossier icb_229_beirut_airport — BEIRUT AIRPORT

```json
{
 "id": "icb_229_beirut_airport",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:08+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 229,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=229",
  "trigdate": "1968-12-28",
  "termdate": "1969-01-01",
  "viol": 2,
  "forout": 6
 },
 "event_date": "1968-12-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.lebanon",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v20/d367",
  "title": "367. Editorial Note (1964\u20131968, Volume XX, Arab-Israeli Dispute, 1967\u20131968)",
  "date": "1968-12-26",
  "window": [
   "1968-11-28",
   "1969-01-31"
  ],
  "query": "Beirut Airport 1968",
  "search_url": "https://history.state.gov/search?q=Beirut+Airport+1968&within=documents",
  "retrieved_at": "2026-09-02T19:16:08+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v20/d367",
    "title": "367. Editorial Note (1964\u20131968, Volume XX, Arab-Israeli Dispute, 1967\u20131968)",
    "page_date": "1968-12-26",
    "retrieved_at": "2026-09-02T19:16:08+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 229 **BEIRUT AIRPORT**: trigdate 1968-12-28, termdate 1969-01-01, viol 2, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=229

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.lebanon:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:08+00:00: **367. Editorial Note (1964–1968, Volume XX, Arab-Israeli Dispute, 1967–1968)** — page date 1968-12-26 (window 1968-11-28..1969-01-31)
  https://history.state.gov/historicaldocuments/frus1964-68v20/d367
- search: https://history.state.gov/search?q=Beirut+Airport+1968&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_229_beirut_airport --approved-by joe`. The code never runs it.
