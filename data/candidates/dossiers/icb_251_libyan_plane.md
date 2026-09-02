# Dossier icb_251_libyan_plane — LIBYAN PLANE

```json
{
 "id": "icb_251_libyan_plane",
 "built_by": "session A",
 "built_at": "2026-09-02T19:16:49+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 251,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=251",
  "trigdate": "1973-02-21",
  "termdate": "1973-02-21",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1973-02-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v25/d22",
  "title": "22. Conversation Between President Nixon and his Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XXV, Arab-Israeli Crisis and War, 1973)",
  "date": "1973-02-21",
  "window": [
   "1973-01-22",
   "1973-03-23"
  ],
  "query": "Libyan Plane 1973",
  "search_url": "https://history.state.gov/search?q=Libyan+Plane+1973&within=documents",
  "retrieved_at": "2026-09-02T19:16:48+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d8",
    "title": "8. Telegram 51869 From the Department of State to the Mission to the United Nations (1969\u20131976, Volume E\u20139, Part 1, Documents on North Africa, 1973\u20131976)",
    "page_date": "1973-03-29",
    "retrieved_at": "2026-09-02T19:16:45+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d134",
    "title": "134. Memorandum From the Executive Secretary of the Department of State (Tarnoff) to the President\u2019s Assistant for National Security Affairs (Brzezinski) (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1980-07-30",
    "retrieved_at": "2026-09-02T19:16:45+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d21",
    "title": "21. Study Prepared by the Ad Hoc Interdepartmental Group for Africa (1969\u20131976, Volume E\u20139, Part 1, Documents on North Africa, 1973\u20131976)",
    "page_date": "1973-07-06",
    "retrieved_at": "2026-09-02T19:16:46+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d90",
    "title": "90. Telegram From the Department of State to the Embassy in Libya (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1977-07-08",
    "retrieved_at": "2026-09-02T19:16:47+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d82",
    "title": "82. Memorandum From Secretary of State Vance to President Carter (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1977-02-14",
    "retrieved_at": "2026-09-02T19:16:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v25/d22",
    "title": "22. Conversation Between President Nixon and his Assistant for National Security Affairs (Kissinger) (1969\u20131976, Volume XXV, Arab-Israeli Crisis and War, 1973)",
    "page_date": "1973-02-21",
    "retrieved_at": "2026-09-02T19:16:48+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 251 **LIBYAN PLANE**: trigdate 1973-02-21, termdate 1973-02-21, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=251

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.israel:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:16:48+00:00: **22. Conversation Between President Nixon and his Assistant for National Security Affairs (Kissinger) (1969–1976, Volume XXV, Arab-Israeli Crisis and War, 1973)** — page date 1973-02-21 (window 1973-01-22..1973-03-23)
  https://history.state.gov/historicaldocuments/frus1969-76v25/d22
- search: https://history.state.gov/search?q=Libyan+Plane+1973&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_251_libyan_plane --approved-by joe`. The code never runs it.
