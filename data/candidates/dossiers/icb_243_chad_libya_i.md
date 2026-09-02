# Dossier icb_243_chad_libya_i — CHAD/LIBYA I

```json
{
 "id": "icb_243_chad_libya_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:37+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 243,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=243",
  "trigdate": "1971-05-24",
  "termdate": "1972-04-17",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1971-05-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve05p2/d81",
  "title": "81. Letter From Secretary of State Rogers to Secretary of Defense Laird (1969\u20131976, Volume E\u20135, Part 2, Documents on North Africa, 1969\u20131972)",
  "date": "1971-12-15",
  "window": [
   "1971-04-24",
   "1972-05-17"
  ],
  "query": "Chad Libya I 1971",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+I+1971&within=documents",
  "retrieved_at": "2026-09-02T19:16:36+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve05p2/d81",
    "title": "81. Letter From Secretary of State Rogers to Secretary of Defense Laird (1969\u20131976, Volume E\u20135, Part 2, Documents on North Africa, 1969\u20131972)",
    "page_date": "1971-12-15",
    "retrieved_at": "2026-09-02T19:16:36+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 243 **CHAD/LIBYA I**: trigdate 1971-05-24, termdate 1972-04-17, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=243

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:36+00:00: **81. Letter From Secretary of State Rogers to Secretary of Defense Laird (1969–1976, Volume E–5, Part 2, Documents on North Africa, 1969–1972)** — page date 1971-12-15 (window 1971-04-24..1972-05-17)
  https://history.state.gov/historicaldocuments/frus1969-76ve05p2/d81
- search: https://history.state.gov/search?q=Chad+Libya+I+1971&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_243_chad_libya_i --approved-by joe`. The code never runs it.
