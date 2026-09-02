# Dossier icb_371_sino_vietnam_border — SINO/VIETNAM BORDER

```json
{
 "id": "icb_371_sino_vietnam_border",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 371,
  "source": "icb",
  "source_id": "371",
  "detail": "SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=371",
  "trigdate": "1987-01-05",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-01-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.vietnam",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Sino Vietnam Border 1987",
  "search_url": "https://history.state.gov/search?q=Sino+Vietnam+Border+1987&within=documents",
  "search_status": 200,
  "window": [
   "1986-12-06",
   "1987-02-04"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v19p2/d121",
    "title": "121. Memorandum of Conversation (1969\u20131976, Volume XIX, Part 2, Japan, 1969\u20131972)",
    "page_date": "1972-06-12",
    "retrieved_at": "2026-09-02T19:50:56+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:50:55+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 371 **SINO/VIETNAM BORDER**: SINO/VIETNAM BORDER 1987-01-05..1987-01-10 viol 3.0 trigdate 1987-01-05, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=371

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.vietnam:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sino Vietnam Border 1987` (https://history.state.gov/search?q=Sino+Vietnam+Border+1987&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1986-12-06..1987-02-04. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 121. Memorandum of Conversation (1969–1976, Volume XIX, Part (1972-06-12)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_371_sino_vietnam_border --approved-by joe`. The code never runs it.
