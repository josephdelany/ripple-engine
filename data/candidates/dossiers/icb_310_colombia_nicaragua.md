# Dossier icb_310_colombia_nicaragua — COLOMBIA/NICARAGUA

```json
{
 "id": "icb_310_colombia_nicaragua",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:36+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 310,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=310",
  "trigdate": "1979-12-12",
  "termdate": "1981-07-08",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1979-12-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.col",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  93
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Colombia Nicaragua 1979",
  "search_url": "https://history.state.gov/search?q=Colombia+Nicaragua+1979&within=documents",
  "search_status": 200,
  "window": [
   "1979-11-12",
   "1981-08-07"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d362",
    "title": "362. Telegram From the Department of State to the Embassies in Venezuela, Ecuador, Peru, Colombia, and Bolivia (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1979-07-14",
    "retrieved_at": "2026-09-02T19:18:32+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v15/d298",
    "title": "298. Paper Prepared in the White House (1977\u20131980, Volume XV, Central America)",
    "page_date": "1979-07-30",
    "retrieved_at": "2026-09-02T19:18:32+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v15/d308",
    "title": "308. Memorandum of Conversation (1977\u20131980, Volume XV, Central America)",
    "page_date": "1979-09-24",
    "retrieved_at": "2026-09-02T19:18:33+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v15/d144",
    "title": "144. Action Memorandum From the Assistant Secretary of State for Inter-American Affairs (Vaky) to Secretary of State Vance (1977\u20131980, Volume XV, Central America)",
    "page_date": "1978-11-18",
    "retrieved_at": "2026-09-02T19:18:34+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d47",
    "title": "47. Telegram From the Department of State to the Embassies in Ecuador, Venezuela, Colombia, Peru, Bolivia, and Nicaragua (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1979-08-13",
    "retrieved_at": "2026-09-02T19:18:34+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d251",
    "title": "251. Telegram From the Department of State to the Embassy in Colombia (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1979-08-13",
    "retrieved_at": "2026-09-02T19:18:35+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:31+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 310 **COLOMBIA/NICARAGUA**: trigdate 1979-12-12, termdate 1981-07-08, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=310

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 93: UNMAPPED
- 100: country.col (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.col:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Colombia Nicaragua 1979` (https://history.state.gov/search?q=Colombia+Nicaragua+1979&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1979-11-12..1981-08-07.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 362. Telegram From the Department of State to the Embassies  (1979-07-14); 298. Paper Prepared in the White House (1977–1980, Volume XV (1979-07-30); 308. Memorandum of Conversation (1977–1980, Volume XV, Centr (1979-09-24); 144. Action Memorandum From the Assistant Secretary of State (1978-11-18); 47. Telegram From the Department of State to the Embassies i (1979-08-13); 251. Telegram From the Department of State to the Embassy in (1979-08-13)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_310_colombia_nicaragua --approved-by joe`. The code never runs it.
