# Dossier icb_149_gaza_raid_czech_arms — GAZA RAID-CZECH. ARMS

```json
{
 "id": "icb_149_gaza_raid_czech_arms",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 149,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=149",
  "trigdate": "1955-02-28",
  "termdate": "1956-06-23",
  "viol": 3,
  "forout": 6
 },
 "event_date": "1955-02-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1955-57v14/d333",
  "title": "333. Memorandum of a Conversation, Department of State, Washington, October 11, 1955 (1955\u20131957, Volume XIV, Arab-Israeli Dispute, 1955)",
  "date": "1955-10-11",
  "window": [
   "1955-01-29",
   "1956-07-23"
  ],
  "query": "Gaza Raid Czech  Arms 1955",
  "search_url": "https://history.state.gov/search?q=Gaza+Raid+Czech++Arms+1955&within=documents",
  "retrieved_at": "2026-09-02T19:14:01+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v14/d333",
    "title": "333. Memorandum of a Conversation, Department of State, Washington, October 11, 1955 (1955\u20131957, Volume XIV, Arab-Israeli Dispute, 1955)",
    "page_date": "1955-10-11",
    "retrieved_at": "2026-09-02T19:14:01+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 149 **GAZA RAID-CZECH. ARMS**: trigdate 1955-02-28, termdate 1956-06-23, viol 3, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=149

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.egypt:target, country.israel:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:01+00:00: **333. Memorandum of a Conversation, Department of State, Washington, October 11, 1955 (1955–1957, Volume XIV, Arab-Israeli Dispute, 1955)** — page date 1955-10-11 (window 1955-01-29..1956-07-23)
  https://history.state.gov/historicaldocuments/frus1955-57v14/d333
- search: https://history.state.gov/search?q=Gaza+Raid+Czech++Arms+1955&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_149_gaza_raid_czech_arms --approved-by joe`. The code never runs it.
