# Dossier icb_257_cyprus_iii — CYPRUS III

```json
{
 "id": "icb_257_cyprus_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:07+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 257,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=257",
  "trigdate": "1974-07-15",
  "termdate": "1975-02-24",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1974-07-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  350,
  352
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v30/d122",
  "title": "122. Briefing Memorandum From the Cyprus Task Force to Secretary of State Kissinger (1969\u20131976, Volume XXX, Greece; Cyprus; Turkey, 1973\u20131976)",
  "date": "1974-07-28",
  "window": [
   "1974-06-15",
   "1975-03-26"
  ],
  "query": "Cyprus Iii 1974",
  "search_url": "https://history.state.gov/search?q=Cyprus+Iii+1974&within=documents",
  "retrieved_at": "2026-09-02T19:17:06+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v30/d122",
    "title": "122. Briefing Memorandum From the Cyprus Task Force to Secretary of State Kissinger (1969\u20131976, Volume XXX, Greece; Cyprus; Turkey, 1973\u20131976)",
    "page_date": "1974-07-28",
    "retrieved_at": "2026-09-02T19:17:06+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 257 **CYPRUS III**: trigdate 1974-07-15, termdate 1975-02-24, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=257

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 350: UNMAPPED
- 352: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:06+00:00: **122. Briefing Memorandum From the Cyprus Task Force to Secretary of State Kissinger (1969–1976, Volume XXX, Greece; Cyprus; Turkey, 1973–1976)** — page date 1974-07-28 (window 1974-06-15..1975-03-26)
  https://history.state.gov/historicaldocuments/frus1969-76v30/d122
- search: https://history.state.gov/search?q=Cyprus+Iii+1974&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_257_cyprus_iii --approved-by joe`. The code never runs it.
