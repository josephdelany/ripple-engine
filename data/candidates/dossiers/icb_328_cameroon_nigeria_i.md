# Dossier icb_328_cameroon_nigeria_i — CAMEROON/NIGERIA I

```json
{
 "id": "icb_328_cameroon_nigeria_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:04+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 328,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=328",
  "trigdate": "1981-05-15",
  "termdate": "1981-07-24",
  "viol": 2,
  "forout": 2
 },
 "event_date": "1981-05-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
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
  "route": "FRUS",
  "query": "Cameroon Nigeria I 1981",
  "search_url": "https://history.state.gov/search?q=Cameroon+Nigeria+I+1981&within=documents",
  "search_status": 200,
  "window": [
   "1981-04-15",
   "1981-08-23"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:03+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 328 **CAMEROON/NIGERIA I**: trigdate 1981-05-15, termdate 1981-07-24, viol 2, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=328

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 471: UNMAPPED
- 475: country.nigeria (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.nigeria:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cameroon Nigeria I 1981` (https://history.state.gov/search?q=Cameroon+Nigeria+I+1981&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1981-04-15..1981-08-23.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_328_cameroon_nigeria_i --approved-by joe`. The code never runs it.
