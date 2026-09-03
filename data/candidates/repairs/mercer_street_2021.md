# Source repair — mercer_street_2021 (2021-07-29)

```json
{
 "event_id": "mercer_street_2021",
 "event_date": "2021-07-29",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-03T00:01:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/July_2021_Gulf_of_Oman_incident",
 "parties": [],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://www.msn.com/en-in/news/world/china-hamas-and-more-us-not-alone-a-list-of-countries-thatve-aced-drone-warfare/ar-AANPOVt",
   "title": "China , Hamas & More : US Not Alone , A List of Countries Thatve Aced Drone Warfare",
   "date": "2021-08-28",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Drone attack strikes tanker Mercer Street off Oman**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/July_2021_Gulf_of_Oman_incident
- parties on the event: none mapped

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `drone, attack, strikes` with this event: **China , Hamas & More : US Not Alone , A List of Countries Thatve Aced Drone Warfare** (2021-08-28, GDELT DOC 2.0).
  https://www.msn.com/en-in/news/world/china-hamas-and-more-us-not-alone-a-list-of-countries-thatve-aced-drone-warfare/ar-AANPOVt

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2021-07-29
- **Federal Register** — `none_found`; query=Drone attack strikes; n_hits=1
    - opened: Marine Mammals; Incidental Take During Specified Activities; North Slope, Alaska (2021-08-05)
- **GDELT DOC 2.0** — `press_candidate`; query=Drone attack strikes
    - opened: China , Hamas & More : US Not Alone , A List of Countries Thatve Aced Drone Warfare (2021-08-28)
- **UK National Archives** — `out_of_coverage`. the UK 20-year rule: files from 2021 are not open before about 2041, so the archive has nothing to return (§6.6)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
