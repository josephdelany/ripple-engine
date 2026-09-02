# Dossier icb_289_litani_operation — LITANI OPERATION

```json
{
 "id": "icb_289_litani_operation",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 289,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=289",
  "trigdate": "1978-03-14",
  "termdate": "1978-06-13",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1978-03-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
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
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d230",
  "title": "230. Telegram From the Department of State to the Embassy in Israel (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
  "date": "1978-03-16",
  "window": [
   "1978-02-12",
   "1978-07-13"
  ],
  "query": "Litani Operation 1978",
  "search_url": "https://history.state.gov/search?q=Litani+Operation+1978&within=documents",
  "retrieved_at": "2026-09-02T19:17:56+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d230",
    "title": "230. Telegram From the Department of State to the Embassy in Israel (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1978-03-16",
    "retrieved_at": "2026-09-02T19:17:56+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 289 **LITANI OPERATION**: trigdate 1978-03-14, termdate 1978-06-13, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=289

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.lebanon:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:56+00:00: **230. Telegram From the Department of State to the Embassy in Israel (1977–1980, Volume VIII, Arab-Israeli Dispute, January 1977–August 1978)** — page date 1978-03-16 (window 1978-02-12..1978-07-13)
  https://history.state.gov/historicaldocuments/frus1977-80v08/d230
- search: https://history.state.gov/search?q=Litani+Operation+1978&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_289_litani_operation --approved-by joe`. The code never runs it.
