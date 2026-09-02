# Dossier icb_239_cienfuegos_sub_base — CIENFUEGOS SUB. BASE

```json
{
 "id": "icb_239_cienfuegos_sub_base",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:33+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 239,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=239",
  "trigdate": "1970-09-16",
  "termdate": "1970-10-23",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1970-09-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76ve10/d228",
  "title": "228. Memorandum From Viron P. Vaky of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u201310, Documents on American Republic",
  "date": "1970-10-05",
  "window": [
   "1970-08-17",
   "1970-11-22"
  ],
  "query": "Cienfuegos Sub  Base 1970",
  "search_url": "https://history.state.gov/search?q=Cienfuegos+Sub++Base+1970&within=documents",
  "retrieved_at": "2026-09-02T19:16:33+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v12/d211",
    "title": "211. Paper Prepared by the Chairman of the Joint Chiefs of Staff (Moorer) (1969\u20131976, Volume XII, Soviet Union, January 1969\u2013October 1970)",
    "page_date": "1969-04-22",
    "retrieved_at": "2026-09-02T19:16:32+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve10/d239",
    "title": "239. Memorandum From Helmut Sonnenfeldt of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u201310, Documents on American Rep",
    "page_date": "1971-05-28",
    "retrieved_at": "2026-09-02T19:16:32+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve10/d228",
    "title": "228. Memorandum From Viron P. Vaky of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume E\u201310, Documents on American Republic",
    "page_date": "1970-10-05",
    "retrieved_at": "2026-09-02T19:16:33+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 239 **CIENFUEGOS SUB. BASE**: trigdate 1970-09-16, termdate 1970-10-23, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=239

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:33+00:00: **228. Memorandum From Viron P. Vaky of the National Security Council Staff to the President’s Assistant for National Security Affairs (Kissinger) (1969–1976, Volume E–10, Documents on American Republic** — page date 1970-10-05 (window 1970-08-17..1970-11-22)
  https://history.state.gov/historicaldocuments/frus1969-76ve10/d228
- search: https://history.state.gov/search?q=Cienfuegos+Sub++Base+1970&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_239_cienfuegos_sub_base --approved-by joe`. The code never runs it.
