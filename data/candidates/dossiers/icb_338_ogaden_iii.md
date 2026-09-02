# Dossier icb_338_ogaden_iii — OGADEN III

```json
{
 "id": "icb_338_ogaden_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:19+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 338,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=338",
  "trigdate": "1982-06-28",
  "termdate": "1982-08-01",
  "viol": 3,
  "forout": 6
 },
 "event_date": "1982-06-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520,
  530
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Ogaden Iii 1982",
  "search_url": "https://history.state.gov/search?q=Ogaden+Iii+1982&within=documents",
  "search_status": 200,
  "window": [
   "1982-05-29",
   "1982-08-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:19+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 338 **OGADEN III**: trigdate 1982-06-28, termdate 1982-08-01, viol 3, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=338

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ogaden Iii 1982` (https://history.state.gov/search?q=Ogaden+Iii+1982&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1982-05-29..1982-08-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_338_ogaden_iii --approved-by joe`. The code never runs it.
