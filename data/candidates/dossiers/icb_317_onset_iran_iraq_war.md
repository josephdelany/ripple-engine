# Dossier icb_317_onset_iran_iraq_war — ONSET IRAN/IRAQ WAR

```json
{
 "id": "icb_317_onset_iran_iraq_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:48+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 317,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=317",
  "trigdate": "1980-09-17",
  "termdate": "1980-11-28",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1980-09-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "target"
  },
  {
   "entity": "country.iraq",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Onset Iran Iraq War 1980",
  "search_url": "https://history.state.gov/search?q=Onset+Iran+Iraq+War+1980&within=documents",
  "search_status": 200,
  "window": [
   "1980-08-18",
   "1980-12-28"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:48+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 317 **ONSET IRAN/IRAQ WAR**: trigdate 1980-09-17, termdate 1980-11-28, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=317

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.iran:target, country.iraq:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Onset Iran Iraq War 1980` (https://history.state.gov/search?q=Onset+Iran+Iraq+War+1980&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1980-08-18..1980-12-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_317_onset_iran_iraq_war --approved-by joe`. The code never runs it.
