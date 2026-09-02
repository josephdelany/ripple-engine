# Dossier icb_143_qibya — QIBYA

```json
{
 "id": "icb_143_qibya",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:47+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 143,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=143",
  "trigdate": "1953-10-14",
  "termdate": "1953-10-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1953-10-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.jor",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1952-54v09p1/d728",
  "title": "No. 728The Secretary of State to the United States Mission at the United Nations (1952\u20131954, Volume IX, Part 1, The Near and Middle East)",
  "date": "1953-11-14",
  "window": [
   "1953-09-14",
   "1953-11-27"
  ],
  "query": "Qibya 1953",
  "search_url": "https://history.state.gov/search?q=Qibya+1953&within=documents",
  "retrieved_at": "2026-09-02T19:13:46+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v09p1/d728",
    "title": "No. 728The Secretary of State to the United States Mission at the United Nations (1952\u20131954, Volume IX, Part 1, The Near and Middle East)",
    "page_date": "1953-11-14",
    "retrieved_at": "2026-09-02T19:13:46+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 143 **QIBYA**: trigdate 1953-10-14, termdate 1953-10-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=143

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 663: country.jor (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.jor:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:46+00:00: **No. 728The Secretary of State to the United States Mission at the United Nations (1952–1954, Volume IX, Part 1, The Near and Middle East)** — page date 1953-11-14 (window 1953-09-14..1953-11-27)
  https://history.state.gov/historicaldocuments/frus1952-54v09p1/d728
- search: https://history.state.gov/search?q=Qibya+1953&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_143_qibya --approved-by joe`. The code never runs it.
