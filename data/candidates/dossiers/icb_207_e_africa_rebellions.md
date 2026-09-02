# Dossier icb_207_e_africa_rebellions — E. AFRICA REBELLIONS

```json
{
 "id": "icb_207_e_africa_rebellions",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:25+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 207,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=207",
  "trigdate": "1964-01-19",
  "termdate": "1964-01-28",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1964-01-19",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "E  Africa Rebellions 1964",
  "search_url": "https://history.state.gov/search?q=E++Africa+Rebellions+1964&within=documents",
  "search_status": 200,
  "window": [
   "1963-12-20",
   "1964-02-27"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve06/d21",
    "title": "21. Response to National Security Study Memorandum 201 (1969\u20131976, Volume E\u20136, Documents on Africa, 1973\u20131976)",
    "page_date": "1974-10-08",
    "retrieved_at": "2026-09-02T19:15:24+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve07/d85",
    "title": "85. National Intelligence Estimate 31/32\u201370 (1969\u20131976, Volume E\u20137, Documents on South Asia, 1969\u20131972)",
    "page_date": "1970-10-20",
    "retrieved_at": "2026-09-02T19:15:25+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:15:23+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 207 **E. AFRICA REBELLIONS**: trigdate 1964-01-19, termdate 1964-01-28, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=207

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `E  Africa Rebellions 1964` (https://history.state.gov/search?q=E++Africa+Rebellions+1964&within=documents, HTTP 200) returned 2 document(s) opened, none dated inside 1963-12-20..1964-02-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 21. Response to National Security Study Memorandum 201 (1969 (1974-10-08); 85. National Intelligence Estimate 31/32–70 (1969–1976, Volu (1970-10-20)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_207_e_africa_rebellions --approved-by joe`. The code never runs it.
