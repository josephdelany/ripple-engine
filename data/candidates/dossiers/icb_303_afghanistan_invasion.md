# Dossier icb_303_afghanistan_invasion — AFGHANISTAN INVASION

```json
{
 "id": "icb_303_afghanistan_invasion",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:26+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 303,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=303",
  "trigdate": "1979-03-28",
  "termdate": "1980-02-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1979-03-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.afg",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d174",
  "title": "174. Intelligence Information Cable Prepared in the Central Intelligence Agency (1977\u20131980, Volume XII, Afghanistan)",
  "date": "1980-01-18",
  "window": [
   "1979-02-26",
   "1980-03-29"
  ],
  "query": "Afghanistan Invasion 1979",
  "search_url": "https://history.state.gov/search?q=Afghanistan+Invasion+1979&within=documents",
  "retrieved_at": "2026-09-02T19:18:25+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d174",
    "title": "174. Intelligence Information Cable Prepared in the Central Intelligence Agency (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1980-01-18",
    "retrieved_at": "2026-09-02T19:18:25+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 303 **AFGHANISTAN INVASION**: trigdate 1979-03-28, termdate 1980-02-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=303

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 365: country.russia (registered state set)
- 700: country.afg
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.russia:unknown, country.afg:unknown, country.pak:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:25+00:00: **174. Intelligence Information Cable Prepared in the Central Intelligence Agency (1977–1980, Volume XII, Afghanistan)** — page date 1980-01-18 (window 1979-02-26..1980-03-29)
  https://history.state.gov/historicaldocuments/frus1977-80v12/d174
- search: https://history.state.gov/search?q=Afghanistan+Invasion+1979&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_303_afghanistan_invasion --approved-by joe`. The code never runs it.
