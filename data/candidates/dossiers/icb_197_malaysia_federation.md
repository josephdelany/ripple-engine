# Dossier icb_197_malaysia_federation — MALAYSIA FEDERATION

```json
{
 "id": "icb_197_malaysia_federation",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:11+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 197,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=197",
  "trigdate": "1963-02-11",
  "termdate": "1965-08-09",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1963-02-11",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  820
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v23/d331",
  "title": "331. Memorandum of Conversation (1961\u20131963, Volume XXIII, Southeast Asia)",
  "date": "1963-04-24",
  "window": [
   "1963-01-12",
   "1965-09-08"
  ],
  "query": "Malaysia Federation 1963",
  "search_url": "https://history.state.gov/search?q=Malaysia+Federation+1963&within=documents",
  "retrieved_at": "2026-09-02T19:15:11+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v23/d331",
    "title": "331. Memorandum of Conversation (1961\u20131963, Volume XXIII, Southeast Asia)",
    "page_date": "1963-04-24",
    "retrieved_at": "2026-09-02T19:15:11+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 197 **MALAYSIA FEDERATION**: trigdate 1963-02-11, termdate 1965-08-09, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=197

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 820: UNMAPPED (registered state set)
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.indonesia:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:11+00:00: **331. Memorandum of Conversation (1961–1963, Volume XXIII, Southeast Asia)** — page date 1963-04-24 (window 1963-01-12..1965-09-08)
  https://history.state.gov/historicaldocuments/frus1961-63v23/d331
- search: https://history.state.gov/search?q=Malaysia+Federation+1963&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_197_malaysia_federation --approved-by joe`. The code never runs it.
