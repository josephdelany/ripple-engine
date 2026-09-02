# Dossier icb_410_cameroon_nigeria_iii — CAMEROON/NIGERIA III

```json
{
 "id": "icb_410_cameroon_nigeria_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 410,
  "source": "icb",
  "source_id": "410",
  "detail": "CAMEROON/NIGERIA III 1993-12-28..1994-11-28 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=410",
  "trigdate": "1993-12-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-12-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.nigeria",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  471
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Cameroon Nigeria Iii 1993",
  "search_url": "https://history.state.gov/search?q=Cameroon+Nigeria+Iii+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-11-28",
   "1994-01-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:31+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 410 **CAMEROON/NIGERIA III**: CAMEROON/NIGERIA III 1993-12-28..1994-11-28 viol 3.0 trigdate 1993-12-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=410

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 471: UNMAPPED
- 475: country.nigeria (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.nigeria:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cameroon Nigeria Iii 1993` (https://history.state.gov/search?q=Cameroon+Nigeria+Iii+1993&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-11-28..1994-01-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_410_cameroon_nigeria_iii --approved-by joe`. The code never runs it.
