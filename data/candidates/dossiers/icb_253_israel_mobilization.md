# Dossier icb_253_israel_mobilization — ISRAEL MOBILIZATION

```json
{
 "id": "icb_253_israel_mobilization",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:58+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 253,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=253",
  "trigdate": "1973-04-10",
  "termdate": "1973-06-28",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1973-04-10",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Israel Mobilization 1973",
  "search_url": "https://history.state.gov/search?q=Israel+Mobilization+1973&within=documents",
  "search_status": 200,
  "window": [
   "1973-03-11",
   "1973-07-28"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v25/d99",
    "title": "99. Memorandum From William B. Quandt of the National Security Council Staff to the President\u2019s Deputy Assistant for National Security Affairs (Scowcroft) (1969\u20131976, Volume XXV, Arab-Israeli Crisis a",
    "page_date": "1973-10-06",
    "retrieved_at": "2026-09-02T19:16:54+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v25/d94",
    "title": "94. Telegram From the Embassy in Israel to the Department of State (1969\u20131976, Volume XXV, Arab-Israeli Crisis and War, 1973)",
    "page_date": "1973-10-01",
    "retrieved_at": "2026-09-02T19:16:55+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v25/d147",
    "title": "147. Telegram From the Embassy in Jordan to the Department of State (1969\u20131976, Volume XXV, Arab-Israeli Crisis and War, 1973)",
    "page_date": "1973-10-10",
    "retrieved_at": "2026-09-02T19:16:55+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v26/d254",
    "title": "254. Minutes of National Security Council Meeting (1969\u20131976, Volume XXVI, Arab-Israeli Dispute, 1974\u20131976)",
    "page_date": "1976-01-13",
    "retrieved_at": "2026-09-02T19:16:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d25",
    "title": "25. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-04-04",
    "retrieved_at": "2026-09-02T19:16:57+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d238",
    "title": "238. Telegram From the Interests Section in Baghdad to the Department of State (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1973-11-04",
    "retrieved_at": "2026-09-02T19:16:57+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:53+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 253 **ISRAEL MOBILIZATION**: trigdate 1973-04-10, termdate 1973-06-28, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=253

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.israel:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Israel Mobilization 1973` (https://history.state.gov/search?q=Israel+Mobilization+1973&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1973-03-11..1973-07-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 99. Memorandum From William B. Quandt of the National Securi (1973-10-06); 94. Telegram From the Embassy in Israel to the Department of (1973-10-01); 147. Telegram From the Embassy in Jordan to the Department o (1973-10-10); 254. Minutes of National Security Council Meeting (1969–1976 (1976-01-13); 25. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-04-04); 238. Telegram From the Interests Section in Baghdad to the D (1973-11-04)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_253_israel_mobilization --approved-by joe`. The code never runs it.
