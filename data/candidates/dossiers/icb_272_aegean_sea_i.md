# Dossier icb_272_aegean_sea_i — AEGEAN SEA I

```json
{
 "id": "icb_272_aegean_sea_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:30+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 272,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=272",
  "trigdate": "1976-08-06",
  "termdate": "1976-09-25",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1976-08-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  350
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v21/d2",
  "title": "2. Paper Prepared by Cyrus Vance for Governor Carter (1977\u20131980, Volume XXI, Cyprus; Turkey; Greece)",
  "date": "1976-10-06",
  "window": [
   "1976-07-07",
   "1976-10-25"
  ],
  "query": "Aegean Sea I 1976",
  "search_url": "https://history.state.gov/search?q=Aegean+Sea+I+1976&within=documents",
  "retrieved_at": "2026-09-02T19:17:30+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v21/d199",
    "title": "199. Discussion Paper Prepared for a Policy Review Committee Meeting (1977\u20131980, Volume XXI, Cyprus; Turkey; Greece)",
    "page_date": "1974-08-28",
    "retrieved_at": "2026-09-02T19:17:28+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v21/d8",
    "title": "8. Report by the President\u2019s Personal Emissary to Greece, Turkey, and Cyprus (Clifford) to President Carter (1977\u20131980, Volume XXI, Cyprus; Turkey; Greece)",
    "page_date": "1977-03-01",
    "retrieved_at": "2026-09-02T19:17:29+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v21/d2",
    "title": "2. Paper Prepared by Cyrus Vance for Governor Carter (1977\u20131980, Volume XXI, Cyprus; Turkey; Greece)",
    "page_date": "1976-10-06",
    "retrieved_at": "2026-09-02T19:17:30+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 272 **AEGEAN SEA I**: trigdate 1976-08-06, termdate 1976-09-25, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=272

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 350: UNMAPPED
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.turkey:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:30+00:00: **2. Paper Prepared by Cyrus Vance for Governor Carter (1977–1980, Volume XXI, Cyprus; Turkey; Greece)** — page date 1976-10-06 (window 1976-07-07..1976-10-25)
  https://history.state.gov/historicaldocuments/frus1977-80v21/d2
- search: https://history.state.gov/search?q=Aegean+Sea+I+1976&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_272_aegean_sea_i --approved-by joe`. The code never runs it.
