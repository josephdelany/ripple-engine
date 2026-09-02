# Dossier icb_226_karameh — KARAMEH

```json
{
 "id": "icb_226_karameh",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 226,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=226",
  "trigdate": "1968-03-18",
  "termdate": "1968-03-22",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1968-03-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v20/d128",
  "title": "128. Memorandum for the Record (1964\u20131968, Volume XX, Arab-Israeli Dispute, 1967\u20131968)",
  "date": "1968-03-29",
  "window": [
   "1968-02-17",
   "1968-04-21"
  ],
  "query": "Karameh 1968",
  "search_url": "https://history.state.gov/search?q=Karameh+1968&within=documents",
  "retrieved_at": "2026-09-02T19:16:00+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v20/d128",
    "title": "128. Memorandum for the Record (1964\u20131968, Volume XX, Arab-Israeli Dispute, 1967\u20131968)",
    "page_date": "1968-03-29",
    "retrieved_at": "2026-09-02T19:16:00+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 226 **KARAMEH**: trigdate 1968-03-18, termdate 1968-03-22, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=226

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.jor:unknown, country.israel:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:00+00:00: **128. Memorandum for the Record (1964–1968, Volume XX, Arab-Israeli Dispute, 1967–1968)** — page date 1968-03-29 (window 1968-02-17..1968-04-21)
  https://history.state.gov/historicaldocuments/frus1964-68v20/d128
- search: https://history.state.gov/search?q=Karameh+1968&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_226_karameh --approved-by joe`. The code never runs it.
