# Dossier icb_298_sino_vietnam_war — SINO/VIETNAM WAR

```json
{
 "id": "icb_298_sino_vietnam_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:17+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 298,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=298",
  "trigdate": "1978-12-25",
  "termdate": "1979-03-15",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1978-12-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "target"
  },
  {
   "entity": "country.vietnam",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Sino Vietnam War 1978",
  "search_url": "https://history.state.gov/search?q=Sino+Vietnam+War+1978&within=documents",
  "search_status": 200,
  "window": [
   "1978-11-25",
   "1979-04-14"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v22/d31",
    "title": "31. Interagency Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XXII, Southeast Asia and the Pacific)",
    "page_date": "1978-11-14",
    "retrieved_at": "2026-09-02T19:18:12+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v22/d132",
    "title": "132. Interagency Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XXII, Southeast Asia and the Pacific)",
    "page_date": "1978-11-14",
    "retrieved_at": "2026-09-02T19:18:13+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v22/d21",
    "title": "21. Paper Prepared in the Central Intelligence Agency (1977\u20131980, Volume XXII, Southeast Asia and the Pacific)",
    "page_date": "1978-03-08",
    "retrieved_at": "2026-09-02T19:18:14+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v13/d125",
    "title": "125. Intelligence Assessment Prepared in the National Foreign Assessment Center, Central Intelligence Agency (1977\u20131980, Volume XIII, China)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:18:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v13/d152",
    "title": "152. Interagency Intelligence Memorandum (1977\u20131980, Volume XIII, China)",
    "page_date": "1978-11-14",
    "retrieved_at": "2026-09-02T19:18:16+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v13/d226",
    "title": "226. Research Paper Prepared in the National Foreign Assessment Center, Central Intelligence Agency (1977\u20131980, Volume XIII, China)",
    "page_date": "1977-01-20",
    "retrieved_at": "2026-09-02T19:18:16+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:12+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 298 **SINO/VIETNAM WAR**: trigdate 1978-12-25, termdate 1979-03-15, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=298

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.china:target, country.vietnam:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sino Vietnam War 1978` (https://history.state.gov/search?q=Sino+Vietnam+War+1978&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1978-11-25..1979-04-14.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 31. Interagency Intelligence Memorandum Prepared in the Cent (1978-11-14); 132. Interagency Intelligence Memorandum Prepared in the Cen (1978-11-14); 21. Paper Prepared in the Central Intelligence Agency (1977– (1978-03-08); 125. Intelligence Assessment Prepared in the National Foreig (no date); 152. Interagency Intelligence Memorandum (1977–1980, Volume  (1978-11-14); 226. Research Paper Prepared in the National Foreign Assessm (1977-01-20)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_298_sino_vietnam_war --approved-by joe`. The code never runs it.
