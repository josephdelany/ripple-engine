# Dossier icb_269_iraqi_threat — IRAQI THREAT

```json
{
 "id": "icb_269_iraqi_threat",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:26+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 269,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=269",
  "trigdate": "1976-06-09",
  "termdate": "1976-06-17",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1976-06-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Iraqi Threat 1976",
  "search_url": "https://history.state.gov/search?q=Iraqi+Threat+1976&within=documents",
  "search_status": 200,
  "window": [
   "1976-05-10",
   "1976-07-17"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d321",
    "title": "321. Telegram From the Interests Section in Baghdad to the Department of State (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1976-11-30",
    "retrieved_at": "2026-09-02T19:17:23+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d317",
    "title": "317. Research Study Prepared in the Central Intelligence Agency (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:14:28+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d208",
    "title": "208. Telegram From the Interests Section in Baghdad to the Department of State (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-03-31",
    "retrieved_at": "2026-09-02T19:17:24+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d5",
    "title": "5. Telegram From the Department of State to the Embassies in France, Italy, and Tunisia (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1977-04-02",
    "retrieved_at": "2026-09-02T19:17:25+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d222",
    "title": "222. Backchannel Message From the Ambassador to Iran (Helms) to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-07-09",
    "retrieved_at": "2026-09-02T19:16:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d23",
    "title": "23. Minutes of Senior Review Group Meeting (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-07-20",
    "retrieved_at": "2026-09-02T19:17:25+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:23+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 269 **IRAQI THREAT**: trigdate 1976-06-09, termdate 1976-06-17, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=269

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.syr:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraqi Threat 1976` (https://history.state.gov/search?q=Iraqi+Threat+1976&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1976-05-10..1976-07-17.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 321. Telegram From the Interests Section in Baghdad to the D (1976-11-30); 317. Research Study Prepared in the Central Intelligence Age (no date); 208. Telegram From the Interests Section in Baghdad to the D (1973-03-31); 5. Telegram From the Department of State to the Embassies in (1977-04-02); 222. Backchannel Message From the Ambassador to Iran (Helms) (1973-07-09); 23. Minutes of Senior Review Group Meeting (1969–1976, Volum (1973-07-20)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_269_iraqi_threat --approved-by joe`. The code never runs it.
