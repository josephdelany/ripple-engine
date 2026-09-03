# Source repair — me_days_of_repentance_2024 (2024-10-26)

```json
{
 "event_id": "me_days_of_repentance_2024",
 "event_date": "2024-10-26",
 "cohort": "encyclopaedia",
 "outcome": "press_candidate",
 "built_by": "session A",
 "built_at": "2026-09-03T00:01:15+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md \u00a76 (2026-09-02)",
 "current_source": "https://en.wikipedia.org/wiki/October_2024_Israeli_strikes_on_Iran",
 "parties": [
  "Iran"
 ],
 "proposed_sources": [
  {
   "route": "GDELT DOC 2.0",
   "url": "https://nationalinterest.org/blog/buzz/israeli-strikes-reportedly-destroy-iran%E2%80%99s-covert-nuclear-facility-213762",
   "title": "Israeli Strikes Reportedly Destroy Iran Covert Nuclear Facility",
   "date": "2024-11-18",
   "reference": null,
   "covering_dates": null
  }
 ],
 "approved_by": null,
 "approved_at": null
}
```

**Israel strikes Iranian military sites in Operation Days of Repentance**

- cohort: `encyclopaedia` — source_url matches wikipedia/britannica
- current source: https://en.wikipedia.org/wiki/October_2024_Israeli_strikes_on_Iran
- parties on the event: Iran

## Outcome: **press_candidate**

**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms `israel, strikes, iranian` with this event: **Israeli Strikes Reportedly Destroy Iran Covert Nuclear Facility** (2024-11-18, GDELT DOC 2.0).
  https://nationalinterest.org/blog/buzz/israeli-strikes-reportedly-destroy-iran%E2%80%99s-covert-nuclear-facility-213762

Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.

## Routes tried

- **FRUS** — `out_of_coverage`. FRUS volumes run to the early 1990s; the event is 2024-10-26
- **Federal Register** — `none_found`; query=Israel strikes Iranian Iran; n_hits=1
    - opened: Order Renewing Order Temporarily Denying Export Privileges (2024-11-01)
- **GDELT DOC 2.0** — `press_candidate`; query=Israel strikes Iranian Iran
    - opened: بعد ضرب دفاعاتها الجوية .. هل تواصل إيران التصعيد ضد إسرائيل ؟  (2024-11-05)
    - opened: كبير مستشاري خامنئي : إيران تستعد للرد على ضربات إسرائيل (2024-11-24)
    - opened: كبير مستشاري خامنئي : إيران تستعد للرد على ضربات إسرائيل (2024-11-24)
    - opened: Israeli Strikes Reportedly Destroy Iran Covert Nuclear Facility (2024-11-18)
- **UK National Archives** — `out_of_coverage`. the UK 20-year rule: files from 2024 are not open before about 2044, so the archive has nothing to return (§6.6)

Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands.
