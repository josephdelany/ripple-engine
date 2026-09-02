# Dossier icb_275_syria_mobilization — SYRIA MOBILIZATION

```json
{
 "id": "icb_275_syria_mobilization",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:34+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 275,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=275",
  "trigdate": "1976-11-21",
  "termdate": "1976-12-13",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1976-11-21",
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
  "query": "Syria Mobilization 1976",
  "search_url": "https://history.state.gov/search?q=Syria+Mobilization+1976&within=documents",
  "search_status": 200,
  "window": [
   "1976-10-22",
   "1977-01-12"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v26/d183",
    "title": "183. Memorandum of Conversation (1969\u20131976, Volume XXVI, Arab-Israeli Dispute, 1974\u20131976)",
    "page_date": "1975-06-11",
    "retrieved_at": "2026-09-02T19:17:33+00:00"
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
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d222",
    "title": "222. Minutes of a Washington Special Actions Group Meeting (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
    "page_date": "1970-09-10",
    "retrieved_at": "2026-09-02T19:17:33+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v26/d4",
    "title": "4. Memorandum of Conversation (1969\u20131976, Volume XXVI, Arab-Israeli Dispute, 1974\u20131976)",
    "page_date": "1974-01-13",
    "retrieved_at": "2026-09-02T19:17:34+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:32+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 275 **SYRIA MOBILIZATION**: trigdate 1976-11-21, termdate 1976-12-13, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=275

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.israel:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Syria Mobilization 1976` (https://history.state.gov/search?q=Syria+Mobilization+1976&within=documents, HTTP 200) returned 5 document(s) opened, none dated inside 1976-10-22..1977-01-12.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 183. Memorandum of Conversation (1969–1976, Volume XXVI, Ara (1975-06-11); 254. Minutes of National Security Council Meeting (1969–1976 (1976-01-13); 25. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-04-04); 222. Minutes of a Washington Special Actions Group Meeting ( (1970-09-10); 4. Memorandum of Conversation (1969–1976, Volume XXVI, Arab- (1974-01-13)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_275_syria_mobilization --approved-by joe`. The code never runs it.
