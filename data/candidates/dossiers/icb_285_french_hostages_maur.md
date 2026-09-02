# Dossier icb_285_french_hostages_maur — FRENCH HOSTAGES MAUR.

```json
{
 "id": "icb_285_french_hostages_maur",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 285,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=285",
  "trigdate": "1977-10-25",
  "termdate": "1977-12-23",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1977-10-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "French Hostages Maur 1977",
  "search_url": "https://history.state.gov/search?q=French+Hostages+Maur+1977&within=documents",
  "search_status": 200,
  "window": [
   "1977-09-25",
   "1978-01-22"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:17:46+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 285 **FRENCH HOSTAGES MAUR.**: trigdate 1977-10-25, termdate 1977-12-23, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=285

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.fra:unknown, country.dza:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `French Hostages Maur 1977` (https://history.state.gov/search?q=French+Hostages+Maur+1977&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1977-09-25..1978-01-22.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_285_french_hostages_maur --approved-by joe`. The code never runs it.
