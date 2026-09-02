# Dossier icb_234_shatt_al_arab_ii — SHATT-AL-ARAB II

```json
{
 "id": "icb_234_shatt_al_arab_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 234,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=234",
  "trigdate": "1969-04-15",
  "termdate": "1969-10-28",
  "viol": 1,
  "forout": 2
 },
 "event_date": "1969-04-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "target"
  },
  {
   "entity": "country.iraq",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Shatt Al Arab Ii 1969",
  "search_url": "https://history.state.gov/search?q=Shatt+Al+Arab+Ii+1969&within=documents",
  "search_status": 200,
  "window": [
   "1969-03-16",
   "1969-11-27"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d317",
    "title": "317. Research Study Prepared in the Central Intelligence Agency (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:14:28+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v06/d302",
    "title": "302. Summary Memorandum of Conversation (1977\u20131980, Volume VI, Soviet Union)",
    "page_date": "1980-09-25",
    "retrieved_at": "2026-09-02T19:16:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve04/d181",
    "title": "181. Intelligence Memorandum ER IM 72\u201379 (1969\u20131976, Volume E\u20134, Documents on Iran and Iraq, 1969\u20131972)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:16:22+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:16:20+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 234 **SHATT-AL-ARAB II**: trigdate 1969-04-15, termdate 1969-10-28, viol 1, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=234

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.iran:target, country.iraq:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Shatt Al Arab Ii 1969` (https://history.state.gov/search?q=Shatt+Al+Arab+Ii+1969&within=documents, HTTP 200) returned 3 document(s) opened, none dated inside 1969-03-16..1969-11-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 317. Research Study Prepared in the Central Intelligence Age (no date); 302. Summary Memorandum of Conversation (1977–1980, Volume V (1980-09-25); 181. Intelligence Memorandum ER IM 72–79 (1969–1976, Volume  (no date)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_234_shatt_al_arab_ii --approved-by joe`. The code never runs it.
