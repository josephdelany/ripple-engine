# Dossier icb_238_black_september — BLACK SEPTEMBER

```json
{
 "id": "icb_238_black_september",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 238,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=238",
  "trigdate": "1970-09-15",
  "termdate": "1970-09-28",
  "viol": 4,
  "forout": 5
 },
 "event_date": "1970-09-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.syr",
   "role": "target"
  },
  {
   "entity": "country.jor",
   "role": "actor"
  },
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v23/d161",
  "title": "161. Editorial Note (1969\u20131976, Volume XXIII, Arab-Israeli Dispute, 1969\u20131972)",
  "date": "1970-09-06",
  "window": [
   "1970-08-16",
   "1970-10-28"
  ],
  "query": "Black September 1970",
  "search_url": "https://history.state.gov/search?q=Black+September+1970&within=documents",
  "retrieved_at": "2026-09-02T19:16:30+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v23/d161",
    "title": "161. Editorial Note (1969\u20131976, Volume XXIII, Arab-Israeli Dispute, 1969\u20131972)",
    "page_date": "1970-09-06",
    "retrieved_at": "2026-09-02T19:16:30+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 238 **BLACK SEPTEMBER**: trigdate 1970-09-15, termdate 1970-09-28, viol 4, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=238

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 652: country.syr (registered state set)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.syr:target, country.jor:actor, country.israel:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:30+00:00: **161. Editorial Note (1969–1976, Volume XXIII, Arab-Israeli Dispute, 1969–1972)** — page date 1970-09-06 (window 1970-08-16..1970-10-28)
  https://history.state.gov/historicaldocuments/frus1969-76v23/d161
- search: https://history.state.gov/search?q=Black+September+1970&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_238_black_september --approved-by joe`. The code never runs it.
