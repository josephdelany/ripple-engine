# Source repair — carter_doctrine_1980 (1980-01-23)

```json
{
 "event_id": "carter_doctrine_1980",
 "event_date": "1980-01-23",
 "cohort": "bare_eia",
 "outcome": "closed",
 "built_by": "session A",
 "built_at": "2026-09-02T23:17:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://www.eia.gov",
 "parties": [
  "United States",
  "Iran"
 ],
 "proposed_sources": [
  {
   "route": "FRUS",
   "url": "https://history.state.gov/historicaldocuments/frus1977-80v13/d297",
   "title": "297. Memorandum From Secretary of State Vance to President Carter (1977\u20131980, Volume XIII, China)",
   "date": "1980-02-01",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Carter Doctrine: US will use force to defend Gulf oil**

- cohort: `bare_eia` — source_url is exactly https://www.eia.gov
- current source: https://www.eia.gov
- parties on the event: United States, Iran

## Outcome: **closed**

A primary document dated inside the window: **297. Memorandum From Secretary of State Vance to President Carter (1977–1980, Volume XIII, China)** (1980-02-01) via FRUS.
  https://history.state.gov/historicaldocuments/frus1977-80v13/d297

## Routes tried

- **FRUS** — `closed`; query=Carter Doctrine will United States Iran
    - opened: 45. Editorial Note (1977–1980, Volume XVIII, Middle East Region; Arabian Peninsula) (1979-11-04)
    - opened: 175. Memorandum From the President’s Assistant for Domestic Affairs and Policy (Eizenstat) (1980-01-19)
    - opened: 346. Summary of Conclusions of a Special Coordination Committee Meeting (1977–1980, Volume (1980-08-22)
    - opened: 115. Memorandum From the President’s Assistant for National Security Affairs (Brzezinski)  (1979-12-29)
- **UK National Archives** — `none_found`; query=Carter Doctrine will United States Iran; n_hits=0
- **GDELT DOC 2.0** — `out_of_coverage`. GDELT DOC coverage begins 2017-01-01

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
