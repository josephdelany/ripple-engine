# Dossier icb_219_yemen_war_iv — YEMEN WAR IV

```json
{
 "id": "icb_219_yemen_war_iv",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:51+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 219,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=219",
  "trigdate": "1966-10-14",
  "termdate": "1967-09-26",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1966-10-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Yemen War Iv 1966",
  "search_url": "https://history.state.gov/search?q=Yemen+War+Iv+1966&within=documents",
  "search_status": 200,
  "window": [
   "1966-09-14",
   "1967-10-26"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v24/d182",
    "title": "182. Special National Intelligence Estimate (1969\u20131976, Volume XXIV, Middle East Region and Arabian Peninsula, 1969\u20131972; Jordan, September 1970)",
    "page_date": "1971-02-11",
    "retrieved_at": "2026-09-02T19:15:36+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d5",
    "title": "5. National Intelligence Estimate Prepared in the Central Intelligence Agency (1969\u20131976, Volume E\u20139, Part 2, Documents on the Middle East Region, 1973\u20131976)",
    "page_date": "1973-06-07",
    "retrieved_at": "2026-09-02T19:15:47+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v12/d138",
    "title": "138. National Intelligence Estimate (1969\u20131976, Volume XII, Soviet Union, January 1969\u2013October 1970)",
    "page_date": "1970-03-05",
    "retrieved_at": "2026-09-02T19:15:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d143",
    "title": "143. Briefing Paper Prepared in the Department of State (1977\u20131980, Volume XVIII, Middle East Region; Arabian Peninsula)",
    "page_date": "1977-01-03",
    "retrieved_at": "2026-09-02T19:15:49+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve02/d144",
    "title": "144. Intelligence Report Prepared by Directorate of Intelligence, Central Intelligence Agency (1969\u20131976, Volume E\u20132, Documents on Arms Control and Nonproliferation, 1969\u20131972)",
    "page_date": "1969-08-18",
    "retrieved_at": "2026-09-02T19:15:50+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve06/d91",
    "title": "91. Study Prepared by the Ad Hoc Inter-Departmental Regional Group for Africa (1969\u20131976, Volume E\u20136, Documents on Africa, 1973\u20131976)",
    "page_date": "1973-07-06",
    "retrieved_at": "2026-09-02T19:15:50+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:15:47+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 219 **YEMEN WAR IV**: trigdate 1966-10-14, termdate 1967-09-26, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=219

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 670: country.saudi_arabia (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown, country.saudi_arabia:unknown, country.yemen:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Yemen War Iv 1966` (https://history.state.gov/search?q=Yemen+War+Iv+1966&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1966-09-14..1967-10-26.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 182. Special National Intelligence Estimate (1969–1976, Volu (1971-02-11); 5. National Intelligence Estimate Prepared in the Central In (1973-06-07); 138. National Intelligence Estimate (1969–1976, Volume XII,  (1970-03-05); 143. Briefing Paper Prepared in the Department of State (197 (1977-01-03); 144. Intelligence Report Prepared by Directorate of Intellig (1969-08-18); 91. Study Prepared by the Ad Hoc Inter-Departmental Regional (1973-07-06)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_219_yemen_war_iv --approved-by joe`. The code never runs it.
