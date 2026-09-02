# Dossier icb_324_iraq_nuclear_reactor — IRAQ NUCLEAR REACTOR

```json
{
 "id": "icb_324_iraq_nuclear_reactor",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:57+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 324,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=324",
  "trigdate": "1981-01-01",
  "termdate": "1981-06-19",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1981-01-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "actor"
  },
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Iraq Nuclear Reactor 1981",
  "search_url": "https://history.state.gov/search?q=Iraq+Nuclear+Reactor+1981&within=documents",
  "search_status": 200,
  "window": [
   "1980-12-02",
   "1981-07-19"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d70",
    "title": "70. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
    "page_date": "1987-09-16",
    "retrieved_at": "2026-09-02T19:18:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v05/d122",
    "title": "122. Memorandum of Conversation (1981\u20131988, Volume V, Soviet Union, March 1985\u2013October 1986)",
    "page_date": "1985-10-25",
    "retrieved_at": "2026-09-02T19:18:57+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:55+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 324 **IRAQ NUCLEAR REACTOR**: trigdate 1981-01-01, termdate 1981-06-19, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=324

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.iraq:actor, country.israel:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraq Nuclear Reactor 1981` (https://history.state.gov/search?q=Iraq+Nuclear+Reactor+1981&within=documents, HTTP 200) returned 2 document(s) opened, none dated inside 1980-12-02..1981-07-19.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 70. Memorandum of Conversation (1981–1988, Volume VI, Soviet (1987-09-16); 122. Memorandum of Conversation (1981–1988, Volume V, Soviet (1985-10-25)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_324_iraq_nuclear_reactor --approved-by joe`. The code never runs it.
