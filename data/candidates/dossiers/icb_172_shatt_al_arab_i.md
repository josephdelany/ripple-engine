# Dossier icb_172_shatt_al_arab_i — SHATT-AL-ARAB I

```json
{
 "id": "icb_172_shatt_al_arab_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 172,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=172",
  "trigdate": "1959-11-28",
  "termdate": "1960-01-04",
  "viol": 2,
  "forout": 3
 },
 "event_date": "1959-11-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "actor"
  },
  {
   "entity": "country.iraq",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Shatt Al Arab I 1959",
  "search_url": "https://history.state.gov/search?q=Shatt+Al+Arab+I+1959&within=documents",
  "search_status": 200,
  "window": [
   "1959-10-29",
   "1960-02-03"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v12/d223",
    "title": "223. Paper Prepared by the Operations Coordinating Board (1958\u20131960, Volume XII, Near East Region; Iraq; Iran; Arabian Peninsula)",
    "page_date": "1960-12-14",
    "retrieved_at": "2026-09-02T19:14:27+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v12/d215",
    "title": "215. Telegram From the Embassy in Iraq to the Department of State (1958\u20131960, Volume XII, Near East Region; Iraq; Iran; Arabian Peninsula)",
    "page_date": "1960-02-26",
    "retrieved_at": "2026-09-02T19:14:28+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d317",
    "title": "317. Research Study Prepared in the Central Intelligence Agency (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:14:28+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v22/d110",
    "title": "110. Telegram From the Embassy in Iran to the Department of State (1964\u20131968, Volume XXII, Iran)",
    "page_date": "1965-11-28",
    "retrieved_at": "2026-09-02T19:14:29+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:14:26+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 172 **SHATT-AL-ARAB I**: trigdate 1959-11-28, termdate 1960-01-04, viol 2, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=172

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.iran:actor, country.iraq:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Shatt Al Arab I 1959` (https://history.state.gov/search?q=Shatt+Al+Arab+I+1959&within=documents, HTTP 200) returned 4 document(s) opened, none dated inside 1959-10-29..1960-02-03.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 223. Paper Prepared by the Operations Coordinating Board (19 (1960-12-14); 215. Telegram From the Embassy in Iraq to the Department of  (1960-02-26); 317. Research Study Prepared in the Central Intelligence Age (no date); 110. Telegram From the Embassy in Iran to the Department of  (1965-11-28)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_172_shatt_al_arab_i --approved-by joe`. The code never runs it.
