# Dossier ucdp_852_government_of_russia — Government of Russia

```json
{
 "id": "ucdp_852_government_of_russia",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "852",
  "detail": "dyad 852 Government of Russia (Soviet Union) vs Chechen Republic of Ichkeria (Russia (Soviet Union)) onset 1994-11-26 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1994-11-26",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-11-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Russia 1994",
  "search_url": "https://history.state.gov/search?q=Government+Of+Russia+1994&within=documents",
  "search_status": 200,
  "window": [
   "1994-10-27",
   "1994-12-26"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v17/d20",
    "title": "20. Editorial Note (1969\u20131976, Volume XVII, China, 1969\u20131972)",
    "page_date": "1969-03-01",
    "retrieved_at": "2026-09-02T19:54:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1938v01/d66",
    "title": "The Charg\u00e9 in France (Wilson) to the Secretary of State (1938, Volume I, General)",
    "page_date": "1938-11-25",
    "retrieved_at": "2026-09-02T19:54:51+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v09/d88",
    "title": "Memorandum of Conversation, by the Secretary of State (1949, Volume IX, The Far East: China)",
    "page_date": "1949-09-13",
    "retrieved_at": "2026-09-02T19:54:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v07p2/d384",
    "title": "Report by Mr. Charles W. Yost, Special Assistant to the Ambassador at Large (Jessup) (1949, Volume VII, Part 2, The Far East and Australasia)",
    "page_date": "1949-09-16",
    "retrieved_at": "2026-09-02T19:54:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1989-92v31/d150",
    "title": "150. Memorandum of Conversation (1989\u20131992, Volume XXXI, START I, 1989\u20131991)",
    "page_date": "1990-08-01",
    "retrieved_at": "2026-09-02T19:53:30+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:54:50+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 852 **Government of Russia**: dyad 852 Government of Russia (Soviet Union) vs Chechen Republic of Ichkeria (Russia (Soviet Union)) onset 1994-11-26 intensity 1 trigdate 1994-11-26, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Russia 1994` (https://history.state.gov/search?q=Government+Of+Russia+1994&within=documents, HTTP 200) returned 5 document(s) opened, none dated inside 1994-10-27..1994-12-26. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 20. Editorial Note (1969–1976, Volume XVII, China, 1969–1972 (1969-03-01); The Chargé in France (Wilson) to the Secretary of State (193 (1938-11-25); Memorandum of Conversation, by the Secretary of State (1949, (1949-09-13); Report by Mr. Charles W. Yost, Special Assistant to the Amba (1949-09-16); 150. Memorandum of Conversation (1989–1992, Volume XXXI, STA (1990-08-01)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_852_government_of_russia --approved-by joe`. The code never runs it.
