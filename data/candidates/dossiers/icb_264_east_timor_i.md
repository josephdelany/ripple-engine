# Dossier icb_264_east_timor_i — EAST TIMOR I

```json
{
 "id": "icb_264_east_timor_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:21+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 264,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=264",
  "trigdate": "1975-11-28",
  "termdate": "1976-07-17",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1975-11-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve12/d144",
  "title": "144. Memorandum From Thomas J. Barnes of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Scowcroft), Washington, December 12, 1975. (1969\u20131976, Volume E",
  "date": "1975-12-12",
  "window": [
   "1975-10-29",
   "1976-08-16"
  ],
  "query": "East Timor I 1975",
  "search_url": "https://history.state.gov/search?q=East+Timor+I+1975&within=documents",
  "retrieved_at": "2026-09-02T19:17:20+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve12/d120",
    "title": "120. Memorandum From W.R. Smyser of the National Security Council Staff to Secretary of State Kissinger, Washington, March 4, 1975. (1969\u20131976, Volume E\u201312, Documents on East and Southeast Asia, 1973\u2013",
    "page_date": "1975-03-04",
    "retrieved_at": "2026-09-02T19:17:19+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve12/d144",
    "title": "144. Memorandum From Thomas J. Barnes of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Scowcroft), Washington, December 12, 1975. (1969\u20131976, Volume E",
    "page_date": "1975-12-12",
    "retrieved_at": "2026-09-02T19:17:20+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 264 **EAST TIMOR I**: trigdate 1975-11-28, termdate 1976-07-17, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=264

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:20+00:00: **144. Memorandum From Thomas J. Barnes of the National Security Council Staff to the President’s Assistant for National Security Affairs (Scowcroft), Washington, December 12, 1975. (1969–1976, Volume E** — page date 1975-12-12 (window 1975-10-29..1976-08-16)
  https://history.state.gov/historicaldocuments/frus1969-76ve12/d144
- search: https://history.state.gov/search?q=East+Timor+I+1975&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_264_east_timor_i --approved-by joe`. The code never runs it.
