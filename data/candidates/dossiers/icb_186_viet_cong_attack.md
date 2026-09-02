# Dossier icb_186_viet_cong_attack — VIET CONG ATTACK

```json
{
 "id": "icb_186_viet_cong_attack",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:51+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 186,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=186",
  "trigdate": "1961-09-18",
  "termdate": "1961-11-15",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1961-09-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v01/d130",
  "title": "130. Telegram From the Chief of the Military Assistance Advisory Group in Viet-Nam (McGarr) to the Commander in Chief, Pacific (Felt) (1961\u20131963, Volume I, Vietnam, 1961)",
  "date": "1961-09-10",
  "window": [
   "1961-08-19",
   "1961-12-15"
  ],
  "query": "Viet Cong Attack 1961",
  "search_url": "https://history.state.gov/search?q=Viet+Cong+Attack+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:51+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v01/d130",
    "title": "130. Telegram From the Chief of the Military Assistance Advisory Group in Viet-Nam (McGarr) to the Commander in Chief, Pacific (Felt) (1961\u20131963, Volume I, Vietnam, 1961)",
    "page_date": "1961-09-10",
    "retrieved_at": "2026-09-02T19:14:51+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 186 **VIET CONG ATTACK**: trigdate 1961-09-18, termdate 1961-11-15, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=186

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:51+00:00: **130. Telegram From the Chief of the Military Assistance Advisory Group in Viet-Nam (McGarr) to the Commander in Chief, Pacific (Felt) (1961–1963, Volume I, Vietnam, 1961)** — page date 1961-09-10 (window 1961-08-19..1961-12-15)
  https://history.state.gov/historicaldocuments/frus1961-63v01/d130
- search: https://history.state.gov/search?q=Viet+Cong+Attack+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_186_viet_cong_attack --approved-by joe`. The code never runs it.
