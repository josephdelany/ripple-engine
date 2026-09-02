# Dossier icb_352_sino_vietnam_clashes — SINO/VIETNAM CLASHES

```json
{
 "id": "icb_352_sino_vietnam_clashes",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:38+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 352,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=352",
  "trigdate": "1984-04-02",
  "termdate": "1984-06-28",
  "viol": 3,
  "forout": 7
 },
 "event_date": "1984-04-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "actor"
  },
  {
   "entity": "country.vietnam",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Sino Vietnam Clashes 1984",
  "search_url": "https://history.state.gov/search?q=Sino+Vietnam+Clashes+1984&within=documents",
  "search_status": 200,
  "window": [
   "1984-03-03",
   "1984-07-28"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v34/d59",
    "title": "59. Editorial Note (1969\u20131976, Volume XXXIV, National Security Policy, 1969\u20131972)",
    "page_date": "1969-05-15",
    "retrieved_at": "2026-09-02T19:19:37+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:19:37+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 352 **SINO/VIETNAM CLASHES**: trigdate 1984-04-02, termdate 1984-06-28, viol 3, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=352

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.china:actor, country.vietnam:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sino Vietnam Clashes 1984` (https://history.state.gov/search?q=Sino+Vietnam+Clashes+1984&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1984-03-03..1984-07-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 59. Editorial Note (1969–1976, Volume XXXIV, National Securi (1969-05-15)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_352_sino_vietnam_clashes --approved-by joe`. The code never runs it.
