# Source repair — me_midnight_hammer_2025 (2025-06-22)

```json
{
 "event_id": "me_midnight_hammer_2025",
 "event_date": "2025-06-22",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-02T23:46:04+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/2025_United_States_strikes_on_Iranian_nuclear_sites",
 "parties": [],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://www.financialexpress.com/world-news/iran-to-resume-nuclear-negotiations-with-france-uk-germany-diplomats-set-to-meet-in-istanbul/3922073/",
   "title": "Iran to resume nuclear negotiations with France , united kingdom , Germany ; diplomats set to meet in Istanbul",
   "date": "2025-07-21",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**US strikes Iranian nuclear sites Fordow Natanz and Isfahan**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/2025_United_States_strikes_on_Iranian_nuclear_sites
- parties on the event: none mapped

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `strikes, iranian, nuclear` with this event: **Iran to resume nuclear negotiations with France , united kingdom , Germany ; diplomats set to meet in Istanbul** (2025-07-21, GDELT DOC 2.0).
  https://www.financialexpress.com/world-news/iran-to-resume-nuclear-negotiations-with-france-uk-germany-diplomats-set-to-meet-in-istanbul/3922073/

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2025-06-22
- **Federal Register** — `none_found`; query=strikes Iranian nuclear; n_hits=0
- **GDELT DOC 2.0** — `press_candidate`; query=strikes Iranian nuclear
    - opened: عاجل .. ترامب : مستعدون لشن ضربات متكررة على المنشآت النووية الإيرانية إذا لزم الأمر (2025-07-22)
    - opened: ترامب : مستعدون لشن ضربات متكررة على المنشآت النووية الإيرانية إذا لزم الأمر (2025-07-22)
    - opened: ترامب يلوّح بشن ضربات متكررة على إيران  إذا لزم الأمر   (2025-07-22)
    - opened: ردا على تصريحات عراقجي ، ترامب يهدد إيران بشن ضربات متكررة على منشآتها النووية (2025-07-22)
- **UK National Archives** — `undetermined`; query=strikes Iranian nuclear; search_status=202. the source refused or failed (§5.1)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
