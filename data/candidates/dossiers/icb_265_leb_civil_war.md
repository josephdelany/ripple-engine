# Dossier icb_265_leb_civil_war — LEB. CIVIL WAR

```json
{
 "id": "icb_265_leb_civil_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 265,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=265",
  "trigdate": "1976-01-18",
  "termdate": "1976-11-15",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1976-01-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Leb  Civil War 1976",
  "search_url": "https://history.state.gov/search?q=Leb++Civil+War+1976&within=documents",
  "search_status": 200,
  "window": [
   "1975-12-19",
   "1976-12-15"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v09Ed2/d42",
    "title": "42. Telegram From the Embassy in Syria to the Department of State (1977\u20131980, Volume IX, Arab-Israeli Dispute, August 1978\u2013December 1980, Second, Revised Edition)",
    "page_date": "1978-09-11",
    "retrieved_at": "2026-09-02T19:17:22+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:21+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 265 **LEB. CIVIL WAR**: trigdate 1976-01-18, termdate 1976-11-15, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=265

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.syr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Leb  Civil War 1976` (https://history.state.gov/search?q=Leb++Civil+War+1976&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1975-12-19..1976-12-15.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 42. Telegram From the Embassy in Syria to the Department of  (1978-09-11)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_265_leb_civil_war --approved-by joe`. The code never runs it.
