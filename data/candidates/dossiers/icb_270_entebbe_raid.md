# Dossier icb_270_entebbe_raid — ENTEBBE RAID

```json
{
 "id": "icb_270_entebbe_raid",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:27+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 270,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=270",
  "trigdate": "1976-06-27",
  "termdate": "1976-07-04",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1976-06-27",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  500
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve06/d184",
  "title": "184. Memorandum From Roger Harrison of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Scowcroft) (1969\u20131976, Volume E\u20136, Documents on Africa, 1973\u20131976",
  "date": "1976-07-03",
  "window": [
   "1976-05-28",
   "1976-08-03"
  ],
  "query": "Entebbe Raid 1976",
  "search_url": "https://history.state.gov/search?q=Entebbe+Raid+1976&within=documents",
  "retrieved_at": "2026-09-02T19:17:27+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve06/d184",
    "title": "184. Memorandum From Roger Harrison of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Scowcroft) (1969\u20131976, Volume E\u20136, Documents on Africa, 1973\u20131976",
    "page_date": "1976-07-03",
    "retrieved_at": "2026-09-02T19:17:27+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 270 **ENTEBBE RAID**: trigdate 1976-06-27, termdate 1976-07-04, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=270

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 500: UNMAPPED
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.israel:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:27+00:00: **184. Memorandum From Roger Harrison of the National Security Council Staff to the President’s Assistant for National Security Affairs (Scowcroft) (1969–1976, Volume E–6, Documents on Africa, 1973–1976** — page date 1976-07-03 (window 1976-05-28..1976-08-03)
  https://history.state.gov/historicaldocuments/frus1969-76ve06/d184
- search: https://history.state.gov/search?q=Entebbe+Raid+1976&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_270_entebbe_raid --approved-by joe`. The code never runs it.
