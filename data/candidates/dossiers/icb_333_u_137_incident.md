# Dossier icb_333_u_137_incident — U-137 INCIDENT

```json
{
 "id": "icb_333_u_137_incident",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:12+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 333,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=333",
  "trigdate": "1981-10-28",
  "termdate": "1981-11-06",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1981-10-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  380
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "U  Incident 1981",
  "search_url": "https://history.state.gov/search?q=U++Incident+1981&within=documents",
  "search_status": 200,
  "window": [
   "1981-09-28",
   "1981-12-06"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d346",
    "title": "346. Telegram From the Embassy in Afghanistan to the Department of State (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1981-01-20",
    "retrieved_at": "2026-09-02T19:19:08+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d175",
    "title": "175. Telegram From the Department of State to the Embassy in Algeria (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1988-04-13",
    "retrieved_at": "2026-09-02T19:19:08+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d329",
    "title": "329. Memorandum From the Director of the Joint Staff of the Joint Chiefs of Staff (Carter) to the Assistant Secretary of Defense for International Security Affairs (Armitage) (1981\u20131988, Volume XXIV, ",
    "page_date": "1985-09-03",
    "retrieved_at": "2026-09-02T19:19:09+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d296",
    "title": "296. Memorandum From Raymond Tanter of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Clark) (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1982-04-28",
    "retrieved_at": "2026-09-02T19:19:10+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v05/d94",
    "title": "94. Minutes of a National Security Council Meeting (1981\u20131988, Volume V, Soviet Union, March 1985\u2013October 1986)",
    "page_date": "1985-09-20",
    "retrieved_at": "2026-09-02T19:19:11+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d115",
    "title": "115. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
    "page_date": "1987-12-10",
    "retrieved_at": "2026-09-02T19:19:11+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:19:07+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 333 **U-137 INCIDENT**: trigdate 1981-10-28, termdate 1981-11-06, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=333

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)
- 380: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `U  Incident 1981` (https://history.state.gov/search?q=U++Incident+1981&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1981-09-28..1981-12-06.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 346. Telegram From the Embassy in Afghanistan to the Departm (1981-01-20); 175. Telegram From the Department of State to the Embassy in (1988-04-13); 329. Memorandum From the Director of the Joint Staff of the  (1985-09-03); 296. Memorandum From Raymond Tanter of the National Security (1982-04-28); 94. Minutes of a National Security Council Meeting (1981–198 (1985-09-20); 115. Memorandum of Conversation (1981–1988, Volume VI, Sovie (1987-12-10)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_333_u_137_incident --approved-by joe`. The code never runs it.
