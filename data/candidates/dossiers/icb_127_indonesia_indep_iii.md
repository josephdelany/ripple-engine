# Dossier icb_127_indonesia_indep_iii — INDONESIA INDEP. III

```json
{
 "id": "icb_127_indonesia_indep_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:19+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 127,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=127",
  "trigdate": "1948-12-19",
  "termdate": "1949-12-27",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1948-12-19",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Indonesia Indep  Iii 1948",
  "search_url": "https://history.state.gov/search?q=Indonesia+Indep++Iii+1948&within=documents",
  "search_status": 200,
  "window": [
   "1948-11-19",
   "1950-01-26"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:13:18+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 127 **INDONESIA INDEP. III**: trigdate 1948-12-19, termdate 1949-12-27, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=127

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 210: UNMAPPED
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Indonesia Indep  Iii 1948` (https://history.state.gov/search?q=Indonesia+Indep++Iii+1948&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1948-11-19..1950-01-26.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_127_indonesia_indep_iii --approved-by joe`. The code never runs it.
