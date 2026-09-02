# Source repair — me_damascus_consulate_2024 (2024-04-01)

```json
{
 "event_id": "me_damascus_consulate_2024",
 "event_date": "2024-04-01",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-02T23:46:04+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/Israeli_airstrike_on_the_Iranian_consulate_in_Damascus",
 "parties": [
  "Iran"
 ],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://infotel.ca/newsitem/ml-syria-israel/cp1178037748",
   "title": "Israeli airstrike destroys Iran consular building in Damascus , killing several , says Syrian media | iNFOnews",
   "date": "2024-04-01",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Israel airstrike destroys Iran consulate in Damascus**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/Israeli_airstrike_on_the_Iranian_consulate_in_Damascus
- parties on the event: Iran

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `israel, airstrike, destroys` with this event: **Israeli airstrike destroys Iran consular building in Damascus , killing several , says Syrian media | iNFOnews** (2024-04-01, GDELT DOC 2.0).
  https://infotel.ca/newsitem/ml-syria-israel/cp1178037748

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2024-04-01
- **Federal Register** — `none_found`; query=Israel airstrike destroys Iran; n_hits=0
- **GDELT DOC 2.0** — `press_candidate`; query=Israel airstrike destroys Iran
    - opened: Israeli airstrike destroys Iran consular building in Damascus , killing several , says Syr (2024-04-01)
- **UK National Archives** — `undetermined`; query=Israel airstrike destroys Iran; search_status=202. the source refused or failed (§5.1)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
