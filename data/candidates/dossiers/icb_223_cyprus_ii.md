# Dossier icb_223_cyprus_ii — CYPRUS II

```json
{
 "id": "icb_223_cyprus_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 223,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=223",
  "trigdate": "1967-11-15",
  "termdate": "1967-12-04",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1967-11-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  350,
  352
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Cyprus Ii 1967",
  "search_url": "https://history.state.gov/search?q=Cyprus+Ii+1967&within=documents",
  "search_status": 200,
  "window": [
   "1967-10-16",
   "1968-01-03"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v30/d75",
    "title": "75. Study Prepared by the Interdepartmental Group for Near East and South Asia (1969\u20131976, Volume XXX, Greece; Cyprus; Turkey, 1973\u20131976)",
    "page_date": "1974-05-06",
    "retrieved_at": "2026-09-02T19:15:55+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:15:54+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 223 **CYPRUS II**: trigdate 1967-11-15, termdate 1967-12-04, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=223

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 350: UNMAPPED
- 352: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cyprus Ii 1967` (https://history.state.gov/search?q=Cyprus+Ii+1967&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1967-10-16..1968-01-03.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 75. Study Prepared by the Interdepartmental Group for Near E (1974-05-06)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_223_cyprus_ii --approved-by joe`. The code never runs it.
