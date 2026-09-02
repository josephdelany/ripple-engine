# Dossier icb_236_cairo_agreement_plo — CAIRO AGREEMENT-PLO

```json
{
 "id": "icb_236_cairo_agreement_plo",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:27+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 236,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=236",
  "trigdate": "1969-10-22",
  "termdate": "1969-11-03",
  "viol": 3,
  "forout": 5
 },
 "event_date": "1969-10-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.lebanon",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Cairo Agreement Plo 1969",
  "search_url": "https://history.state.gov/search?q=Cairo+Agreement+Plo+1969&within=documents",
  "search_status": 200,
  "window": [
   "1969-09-22",
   "1969-12-03"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d80",
    "title": "80. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-08-09",
    "retrieved_at": "2026-09-02T19:16:23+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v26/d290",
    "title": "290. Memorandum of Conversation (1969\u20131976, Volume XXVI, Arab-Israeli Dispute, 1974\u20131976)",
    "page_date": "1976-06-22",
    "retrieved_at": "2026-09-02T19:16:24+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d103",
    "title": "103. Memorandum From William Quandt of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Brzezinski) (1977\u20131980, Volume VIII, Arab-Israeli Dispute, Januar",
    "page_date": "1977-09-19",
    "retrieved_at": "2026-09-02T19:16:25+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d9",
    "title": "9. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-02-17",
    "retrieved_at": "2026-09-02T19:16:25+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d18",
    "title": "18. Memorandum From the Assistant Secretary of State for Near Eastern and South Asian Affairs (Sisco) to Secretary of State Rogers (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 19",
    "page_date": "1970-01-06",
    "retrieved_at": "2026-09-02T19:16:26+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d63",
    "title": "63. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-08-01",
    "retrieved_at": "2026-09-02T19:16:27+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:23+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 236 **CAIRO AGREEMENT-PLO**: trigdate 1969-10-22, termdate 1969-11-03, viol 3, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=236

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.lebanon:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cairo Agreement Plo 1969` (https://history.state.gov/search?q=Cairo+Agreement+Plo+1969&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1969-09-22..1969-12-03.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 80. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-08-09); 290. Memorandum of Conversation (1969–1976, Volume XXVI, Ara (1976-06-22); 103. Memorandum From William Quandt of the National Security (1977-09-19); 9. Memorandum of Conversation (1977–1980, Volume VIII, Arab- (1977-02-17); 18. Memorandum From the Assistant Secretary of State for Nea (1970-01-06); 63. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-08-01)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_236_cairo_agreement_plo --approved-by joe`. The code never runs it.
