# Dossier icb_120_pal_prt_israel_ind — PAL. PRT./ISRAEL IND.

```json
{
 "id": "icb_120_pal_prt_israel_ind",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:06+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 120,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=120",
  "trigdate": "1947-11-28",
  "termdate": "1949-07-20",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1947-11-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "unknown"
  },
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.syr",
   "role": "unknown"
  },
  {
   "entity": "country.lebanon",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Pal  Prt Israel Ind 1947",
  "search_url": "https://history.state.gov/search?q=Pal++Prt+Israel+Ind+1947&within=documents",
  "search_status": 200,
  "window": [
   "1947-10-29",
   "1949-08-19"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:13:06+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 120 **PAL. PRT./ISRAEL IND.**: trigdate 1947-11-28, termdate 1949-07-20, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=120

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)
- 651: country.egypt (registered state set)
- 652: country.syr (registered state set)
- 660: country.lebanon (registered state set)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.iraq:unknown, country.egypt:unknown, country.syr:unknown, country.lebanon:unknown, country.jor:unknown, country.israel:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Pal  Prt Israel Ind 1947` (https://history.state.gov/search?q=Pal++Prt+Israel+Ind+1947&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1947-10-29..1949-08-19.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_120_pal_prt_israel_ind --approved-by joe`. The code never runs it.
