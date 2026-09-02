# Dossier icb_297_angola_invasion_scare — ANGOLA INVASION SCARE

```json
{
 "id": "icb_297_angola_invasion_scare",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:11+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 297,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=297",
  "trigdate": "1978-11-07",
  "termdate": "1978-11-14",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1978-11-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Angola Invasion Scare 1978",
  "search_url": "https://history.state.gov/search?q=Angola+Invasion+Scare+1978&within=documents",
  "search_status": 200,
  "window": [
   "1978-10-08",
   "1978-12-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:11+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 297 **ANGOLA INVASION SCARE**: trigdate 1978-11-07, termdate 1978-11-14, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=297

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.ago:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Angola Invasion Scare 1978` (https://history.state.gov/search?q=Angola+Invasion+Scare+1978&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1978-10-08..1978-12-14.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_297_angola_invasion_scare --approved-by joe`. The code never runs it.
