# Dossier icb_308_raid_on_angola — RAID ON ANGOLA

```json
{
 "id": "icb_308_raid_on_angola",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:29+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 308,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=308",
  "trigdate": "1979-10-28",
  "termdate": "1979-11-02",
  "viol": 2,
  "forout": 6
 },
 "event_date": "1979-10-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
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
  "query": "Raid On Angola 1979",
  "search_url": "https://history.state.gov/search?q=Raid+On+Angola+1979&within=documents",
  "search_status": 200,
  "window": [
   "1979-09-28",
   "1979-12-02"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:28+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 308 **RAID ON ANGOLA**: trigdate 1979-10-28, termdate 1979-11-02, viol 2, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=308

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.ago:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Raid On Angola 1979` (https://history.state.gov/search?q=Raid+On+Angola+1979&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1979-09-28..1979-12-02.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_308_raid_on_angola --approved-by joe`. The code never runs it.
