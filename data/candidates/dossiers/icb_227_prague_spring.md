# Dossier icb_227_prague_spring — PRAGUE SPRING

```json
{
 "id": "icb_227_prague_spring",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:06+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 227,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=227",
  "trigdate": "1968-04-09",
  "termdate": "1968-10-18",
  "viol": 2,
  "forout": 5
 },
 "event_date": "1968-04-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.hungary",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  265,
  290,
  315,
  355
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Prague Spring 1968",
  "search_url": "https://history.state.gov/search?q=Prague+Spring+1968&within=documents",
  "search_status": 200,
  "window": [
   "1968-03-10",
   "1968-11-17"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v20/d105",
    "title": "105. Telegram From the Embassy in Czechoslovakia to the Department of State and Multiple Diplomatic Posts (1977\u20131980, Volume XX, Eastern Europe)",
    "page_date": "1978-08-11",
    "retrieved_at": "2026-09-02T19:16:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v10/d418",
    "title": "418. Intelligence Research Report Prepared in the Bureau of Intelligence and Research (1981\u20131988, Volume X, Eastern Europe)",
    "page_date": "1987-09-11",
    "retrieved_at": "2026-09-02T19:16:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v20/d116",
    "title": "116. Telegram From the Embassy in Czechoslovakia to the Department of State (1977\u20131980, Volume XX, Eastern Europe)",
    "page_date": "1980-11-26",
    "retrieved_at": "2026-09-02T19:16:04+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v29/d4",
    "title": "4. Airgram From the Office of the Permanent Representative to the North Atlantic Treaty Organization to the Department of State (1969\u20131976, Volume XXIX, Eastern Europe; Eastern Mediterranean, 1969\u2013197",
    "page_date": "1969-05-12",
    "retrieved_at": "2026-09-02T19:16:05+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v17/d99",
    "title": "99. Airgram From the Embassy in Czechoslovakia to the Department of State (1964\u20131968, Volume XVII, Eastern Europe)",
    "page_date": "1968-11-29",
    "retrieved_at": "2026-09-02T19:16:05+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v10/d5",
    "title": "5. Paper Prepared in the Bureau of Intelligence and Research (1981\u20131988, Volume X, Eastern Europe)",
    "page_date": "1981-08-28",
    "retrieved_at": "2026-09-02T19:16:06+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:02+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 227 **PRAGUE SPRING**: trigdate 1968-04-09, termdate 1968-10-18, viol 2, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=227

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 265: UNMAPPED
- 290: UNMAPPED
- 310: country.hungary
- 315: UNMAPPED
- 355: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.hungary:unknown, country.russia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Prague Spring 1968` (https://history.state.gov/search?q=Prague+Spring+1968&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1968-03-10..1968-11-17.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 105. Telegram From the Embassy in Czechoslovakia to the Depa (1978-08-11); 418. Intelligence Research Report Prepared in the Bureau of  (1987-09-11); 116. Telegram From the Embassy in Czechoslovakia to the Depa (1980-11-26); 4. Airgram From the Office of the Permanent Representative t (1969-05-12); 99. Airgram From the Embassy in Czechoslovakia to the Depart (1968-11-29); 5. Paper Prepared in the Bureau of Intelligence and Research (1981-08-28)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_227_prague_spring --approved-by joe`. The code never runs it.
