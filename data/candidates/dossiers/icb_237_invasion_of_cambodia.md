# Dossier icb_237_invasion_of_cambodia — INVASION OF CAMBODIA

```json
{
 "id": "icb_237_invasion_of_cambodia",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:29+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 237,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=237",
  "trigdate": "1970-03-13",
  "termdate": "1970-07-22",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1970-03-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.vietnam",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  811,
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v06/d242",
  "title": "242. Memorandum From Director of Central Intelligence Helms to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume VI, Vietnam, January 1969\u2013July 1970)",
  "date": "1970-04-21",
  "window": [
   "1970-02-11",
   "1970-08-21"
  ],
  "query": "Invasion Of Cambodia 1970",
  "search_url": "https://history.state.gov/search?q=Invasion+Of+Cambodia+1970&within=documents",
  "retrieved_at": "2026-09-02T19:16:28+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v06/d242",
    "title": "242. Memorandum From Director of Central Intelligence Helms to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume VI, Vietnam, January 1969\u2013July 1970)",
    "page_date": "1970-04-21",
    "retrieved_at": "2026-09-02T19:16:28+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 237 **INVASION OF CAMBODIA**: trigdate 1970-03-13, termdate 1970-07-22, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=237

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 811: UNMAPPED
- 816: country.vietnam
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.vietnam:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:28+00:00: **242. Memorandum From Director of Central Intelligence Helms to the President’s Assistant for National Security Affairs (Kissinger) (1969–1976, Volume VI, Vietnam, January 1969–July 1970)** — page date 1970-04-21 (window 1970-02-11..1970-08-21)
  https://history.state.gov/historicaldocuments/frus1969-76v06/d242
- search: https://history.state.gov/search?q=Invasion+Of+Cambodia+1970&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_237_invasion_of_cambodia --approved-by joe`. The code never runs it.
