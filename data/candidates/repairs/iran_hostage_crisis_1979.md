# Source repair — iran_hostage_crisis_1979 (1979-11-04)

```json
{
 "event_id": "iran_hostage_crisis_1979",
 "event_date": "1979-11-04",
 "cohort": "bare_eia",
 "outcome": "closed",
 "built_by": "session A",
 "built_at": "2026-09-02T23:17:24+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://www.eia.gov",
 "parties": [
  "Iran",
  "United States"
 ],
 "proposed_sources": [
  {
   "route": "FRUS",
   "url": "https://history.state.gov/historicaldocuments/frus1977-80v11p1/d42",
   "title": "42. Paper Prepared in the Department of State (1977\u20131980, Volume XI, Part 1, Iran: Hostage Crisis, November 1979\u2013September 1980)",
   "date": "1979-11-20",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**US embassy hostage crisis begins in Tehran**

- cohort: `bare_eia` — source_url is exactly https://www.eia.gov
- current source: https://www.eia.gov
- parties on the event: Iran, United States

## Outcome: **closed**

A primary document dated inside the window: **42. Paper Prepared in the Department of State (1977–1980, Volume XI, Part 1, Iran: Hostage Crisis, November 1979–September 1980)** (1979-11-20) via FRUS.
  https://history.state.gov/historicaldocuments/frus1977-80v11p1/d42

## Routes tried

- **FRUS** — `closed`; query=embassy hostage begins Iran United States
    - opened: 42. Paper Prepared in the Department of State (1977–1980, Volume XI, Part 1, Iran: Hostage (1979-11-20)
- **UK National Archives** — `none_found`; query=embassy hostage begins Iran United States; n_hits=0
- **GDELT DOC 2.0** — `out_of_coverage`. GDELT DOC coverage begins 2017-01-01

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
