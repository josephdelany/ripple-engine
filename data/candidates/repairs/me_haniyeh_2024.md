# Source repair — me_haniyeh_2024 (2024-07-31)

```json
{
 "event_id": "me_haniyeh_2024",
 "event_date": "2024-07-31",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-03T00:01:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/Assassination_of_Ismail_Haniyeh",
 "parties": [
  "Iran"
 ],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://menafn.com/1108599553/Will-Live-Forever-With-Allah-Slain-Hamas-Leader-Ismail-Haniyehs-Poster-In-Kerala-Sparks-Outrage-See-Pics",
   "title": "  Will Live Forever With Allah : Slain Hamas Leader Ismail Haniyeh Poster In Kerala Sparks Outrage ; See Pics",
   "date": "2024-08-26",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Hamas leader Ismail Haniyeh assassinated in Tehran**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/Assassination_of_Ismail_Haniyeh
- parties on the event: Iran

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `hamas, leader, ismail` with this event: **  Will Live Forever With Allah : Slain Hamas Leader Ismail Haniyeh Poster In Kerala Sparks Outrage ; See Pics** (2024-08-26, GDELT DOC 2.0).
  https://menafn.com/1108599553/Will-Live-Forever-With-Allah-Slain-Hamas-Leader-Ismail-Haniyehs-Poster-In-Kerala-Sparks-Outrage-See-Pics

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2024-07-31
- **Federal Register** — `none_found`; query=Hamas leader Ismail Iran; n_hits=0
- **GDELT DOC 2.0** — `press_candidate`; query=Hamas leader Ismail Iran
    - opened:   Will Live Forever With Allah : Slain Hamas Leader Ismail Haniyeh Poster In Kerala Sparks (2024-08-26)
- **UK National Archives** — `out_of_coverage`. the UK 20-year rule: files from 2024 are not open before about 2044, so the archive has nothing to return (§6.6)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
