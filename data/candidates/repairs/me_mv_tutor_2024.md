# Source repair — me_mv_tutor_2024 (2024-06-12)

```json
{
 "event_id": "me_mv_tutor_2024",
 "event_date": "2024-06-12",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-03T00:01:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/MV_Tutor",
 "parties": [],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://www.wmdt.com/i/british-military-says-bulk-carrier-tutor-sinks-after-attack-by-yemens-houthi-rebels-believed-to-have-killed-1-on-board/",
   "title": "British military says bulk carrier Tutor sinks after attack by Yemen Houthi rebels believed to have killed 1 on board",
   "date": "2024-06-19",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Houthi attack sinks bulk carrier MV Tutor in the Red Sea**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/MV_Tutor
- parties on the event: none mapped

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `houthi, attack, sinks` with this event: **British military says bulk carrier Tutor sinks after attack by Yemen Houthi rebels believed to have killed 1 on board** (2024-06-19, GDELT DOC 2.0).
  https://www.wmdt.com/i/british-military-says-bulk-carrier-tutor-sinks-after-attack-by-yemens-houthi-rebels-believed-to-have-killed-1-on-board/

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2024-06-12
- **Federal Register** — `none_found`; query=Houthi attack sinks; n_hits=0
- **GDELT DOC 2.0** — `press_candidate`; query=Houthi attack sinks
    - opened: British military says bulk carrier Tutor sinks after attack by Yemen Houthi rebels believe (2024-06-19)
- **UK National Archives** — `out_of_coverage`. the UK 20-year rule: files from 2024 are not open before about 2044, so the archive has nothing to return (§6.6)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
