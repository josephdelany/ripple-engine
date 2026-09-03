# Source repair — me_nasrallah_2024 (2024-09-27)

```json
{
 "event_id": "me_nasrallah_2024",
 "event_date": "2024-09-27",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-03T00:01:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/2024_Hezbollah_headquarters_strike",
 "parties": [
  "Iran"
 ],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://www.livemint.com/news/world/irans-ayatollah-ali-khamenei-moves-to-safety-amid-fears-of-israeli-strikes-hassan-nasrallah-lebanon-hezbollah-11727522674173.html",
   "title": "Iran hides supreme leader Ayatollah Ali Khamenei as Israeli airstrike kills Hezbollah chief Hassan Nasrallah",
   "date": "2024-09-28",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Israeli airstrike kills Hezbollah leader Hassan Nasrallah**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/2024_Hezbollah_headquarters_strike
- parties on the event: Iran

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `israeli, airstrike, kills` with this event: **Iran hides supreme leader Ayatollah Ali Khamenei as Israeli airstrike kills Hezbollah chief Hassan Nasrallah** (2024-09-28, GDELT DOC 2.0).
  https://www.livemint.com/news/world/irans-ayatollah-ali-khamenei-moves-to-safety-amid-fears-of-israeli-strikes-hassan-nasrallah-lebanon-hezbollah-11727522674173.html

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2024-09-27
- **Federal Register** — `none_found`; query=Israeli airstrike kills Iran; n_hits=0
- **GDELT DOC 2.0** — `press_candidate`; query=Israeli airstrike kills Iran
    - opened: Iran hides supreme leader Ayatollah Ali Khamenei as Israeli airstrike kills Hezbollah chie (2024-09-28)
- **UK National Archives** — `out_of_coverage`. the UK 20-year rule: files from 2024 are not open before about 2044, so the archive has nothing to return (§6.6)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
