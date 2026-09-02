# Dossier icb_135_punjab_war_scare_i — PUNJAB WAR SCARE I

```json
{
 "id": "icb_135_punjab_war_scare_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 135,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=135",
  "trigdate": "1951-07-07",
  "termdate": "1951-08-01",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1951-07-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "target"
  },
  {
   "entity": "country.pak",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Punjab War Scare I 1951",
  "search_url": "https://history.state.gov/search?q=Punjab+War+Scare+I+1951&within=documents",
  "search_status": 200,
  "window": [
   "1951-06-07",
   "1951-08-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:13:29+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 135 **PUNJAB WAR SCARE I**: trigdate 1951-07-07, termdate 1951-08-01, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=135

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.india:target, country.pak:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Punjab War Scare I 1951` (https://history.state.gov/search?q=Punjab+War+Scare+I+1951&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1951-06-07..1951-08-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_135_punjab_war_scare_i --approved-by joe`. The code never runs it.
