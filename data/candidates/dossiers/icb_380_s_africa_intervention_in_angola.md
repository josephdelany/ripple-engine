# Dossier icb_380_s_africa_intervention_in_angola — S. AFRICA INTERVENTION IN ANGOLA

```json
{
 "id": "icb_380_s_africa_intervention_in_angola",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 380,
  "source": "icb",
  "source_id": "380",
  "detail": "S. AFRICA INTERVENTION IN ANGOLA 1987-10-03..1988-08-22 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=380",
  "trigdate": "1987-10-03",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-10-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "unknown"
  },
  {
   "entity": "country.south_africa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d82",
  "title": "82. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
  "date": "1987-10-22",
  "window": [
   "1987-09-03",
   "1987-11-02"
  ],
  "query": "S  Africa Intervention In Angola 1987",
  "search_url": "https://history.state.gov/search?q=S++Africa+Intervention+In+Angola+1987&within=documents",
  "retrieved_at": "2026-09-02T19:52:44+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d275",
    "title": "275. Address by Secretary of State Shultz (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1986-09-05",
    "retrieved_at": "2026-09-02T19:52:43+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d82",
    "title": "82. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
    "page_date": "1987-10-22",
    "retrieved_at": "2026-09-02T19:52:44+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 380 **S. AFRICA INTERVENTION IN ANGOLA**: S. AFRICA INTERVENTION IN ANGOLA 1987-10-03..1988-08-22 viol 3.0 trigdate 1987-10-03, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=380

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)
- 560: country.south_africa

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.ago:unknown, country.south_africa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:52:44+00:00: **82. Memorandum of Conversation (1981–1988, Volume VI, Soviet Union, October 1986–January 1989)** — page date 1987-10-22 (window 1987-09-03..1987-11-02)
  https://history.state.gov/historicaldocuments/frus1981-88v06/d82
- search: https://history.state.gov/search?q=S++Africa+Intervention+In+Angola+1987&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_380_s_africa_intervention_in_angola --approved-by joe`. The code never runs it.
