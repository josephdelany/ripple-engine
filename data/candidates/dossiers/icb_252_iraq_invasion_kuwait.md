# Dossier icb_252_iraq_invasion_kuwait — IRAQ INVASION/KUWAIT

```json
{
 "id": "icb_252_iraq_invasion_kuwait",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:53+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 252,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=252",
  "trigdate": "1973-03-20",
  "termdate": "1973-06-08",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1973-03-20",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.kuwait",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Iraq Invasion Kuwait 1973",
  "search_url": "https://history.state.gov/search?q=Iraq+Invasion+Kuwait+1973&within=documents",
  "search_status": 200,
  "window": [
   "1973-02-18",
   "1973-07-08"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d222",
    "title": "222. Backchannel Message From the Ambassador to Iran (Helms) to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-07-09",
    "retrieved_at": "2026-09-02T19:16:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d27",
    "title": "27. Memorandum of Conversation (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-07-24",
    "retrieved_at": "2026-09-02T19:16:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d1",
    "title": "1. Airgram From the Embassy in Iran to the Department of State (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-01-09",
    "retrieved_at": "2026-09-02T19:16:51+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve06/d142",
    "title": "142. Interagency Memorandum DCI/NIO 1076\u201375 (1969\u20131976, Volume E\u20136, Documents on Africa, 1973\u20131976)",
    "page_date": "1975-05-07",
    "retrieved_at": "2026-09-02T19:16:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d44",
    "title": "44. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
    "page_date": "1987-04-14",
    "retrieved_at": "2026-09-02T19:16:52+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:49+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 252 **IRAQ INVASION/KUWAIT**: trigdate 1973-03-20, termdate 1973-06-08, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=252

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.kuwait:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraq Invasion Kuwait 1973` (https://history.state.gov/search?q=Iraq+Invasion+Kuwait+1973&within=documents, HTTP 200) returned 5 document(s) opened, none dated inside 1973-02-18..1973-07-08.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 222. Backchannel Message From the Ambassador to Iran (Helms) (1973-07-09); 27. Memorandum of Conversation (1969–1976, Volume XXVII, Ira (1973-07-24); 1. Airgram From the Embassy in Iran to the Department of Sta (1973-01-09); 142. Interagency Memorandum DCI/NIO 1076–75 (1969–1976, Volu (1975-05-07); 44. Memorandum of Conversation (1981–1988, Volume VI, Soviet (1987-04-14)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_252_iraq_invasion_kuwait --approved-by joe`. The code never runs it.
