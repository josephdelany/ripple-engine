# Dossier icb_144_guatemala — GUATEMALA

```json
{
 "id": "icb_144_guatemala",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:52+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 144,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=144",
  "trigdate": "1953-12-12",
  "termdate": "1954-06-28",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1953-12-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  90,
  91
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Guatemala 1953",
  "search_url": "https://history.state.gov/search?q=Guatemala+1953&within=documents",
  "search_status": 200,
  "window": [
   "1953-11-12",
   "1954-07-28"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v04/d100",
    "title": "Memorandum of Conversation, by John L. Ohmans of the Office of Middle American Afairs (1952\u20131954, Volume IV, The American Republics)",
    "page_date": "1953-05-12",
    "retrieved_at": "2026-09-02T19:13:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v04/d420",
    "title": "Editorial Note (1952\u20131954, Volume IV, The American Republics)",
    "page_date": "1953-02-26",
    "retrieved_at": "2026-09-02T19:13:49+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54Guat/d38",
    "title": "38. Report Summary Prepared in the Central Intelligence Agency (1952\u20131954, Guatemala)",
    "page_date": "1953-06-18",
    "retrieved_at": "2026-09-02T19:13:49+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v04/d425",
    "title": "Memorandum for the Record, by Richard Hirsch of the Operations Coordinating Board (1952\u20131954, Volume IV, The American Republics)",
    "page_date": "1953-10-29",
    "retrieved_at": "2026-09-02T19:13:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54Guat/d63",
    "title": "63. Memorandum From [name not declassified] of the Central Intelligence Agency to [name not declassified] of the Central Intelligence Agency (1952\u20131954, Guatemala)",
    "page_date": "1953-11-05",
    "retrieved_at": "2026-09-02T19:13:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950-55Intel/d154",
    "title": "154. Editorial Note (The Intelligence Community, 1950\u20131955)",
    "page_date": "1953-08-12",
    "retrieved_at": "2026-09-02T19:13:51+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:13:47+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 144 **GUATEMALA**: trigdate 1953-12-12, termdate 1954-06-28, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=144

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 90: UNMAPPED
- 91: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Guatemala 1953` (https://history.state.gov/search?q=Guatemala+1953&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1953-11-12..1954-07-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: Memorandum of Conversation, by John L. Ohmans of the Office  (1953-05-12); Editorial Note (1952–1954, Volume IV, The American Republics (1953-02-26); 38. Report Summary Prepared in the Central Intelligence Agen (1953-06-18); Memorandum for the Record, by Richard Hirsch of the Operatio (1953-10-29); 63. Memorandum From [name not declassified] of the Central I (1953-11-05); 154. Editorial Note (The Intelligence Community, 1950–1955) (1953-08-12)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_144_guatemala --approved-by joe`. The code never runs it.
