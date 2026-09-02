# Dossier icb_164_abort_coup_indonesia — ABORT. COUP INDONESIA

```json
{
 "id": "icb_164_abort_coup_indonesia",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:17+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 164,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=164",
  "trigdate": "1958-02-21",
  "termdate": "1958-05-20",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1958-02-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Abort  Coup Indonesia 1958",
  "search_url": "https://history.state.gov/search?q=Abort++Coup+Indonesia+1958&within=documents",
  "search_status": 200,
  "window": [
   "1958-01-22",
   "1958-06-19"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:17+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 164 **ABORT. COUP INDONESIA**: trigdate 1958-02-21, termdate 1958-05-20, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=164

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Abort  Coup Indonesia 1958` (https://history.state.gov/search?q=Abort++Coup+Indonesia+1958&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1958-01-22..1958-06-19.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_164_abort_coup_indonesia --approved-by joe`. The code never runs it.
