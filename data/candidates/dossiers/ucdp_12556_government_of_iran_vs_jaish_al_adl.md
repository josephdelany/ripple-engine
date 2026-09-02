# Dossier ucdp_12556_government_of_iran_vs_jaish_al_adl — Government of Iran vs Jaish al-Adl

```json
{
 "id": "ucdp_12556_government_of_iran_vs_jaish_al_adl",
 "built_by": "session A",
 "built_at": "2026-09-02T21:07:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "12556",
  "detail": "dyad 12556 Government of Iran vs Jaish al-Adl (Iran) onset 2019-02-13 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2019-02-13",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2019-02-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "http://idrw.org/pak-army-using-terror-group-to-carry-out-attacks-in-iran/",
  "title": "Pak army using terror group to carry out attacks in Iran \u2013 Indian Defence Research Wing",
  "date": "2019-03-10",
  "domain": "idrw.org",
  "window": [
   "2019-02-10",
   "2019-03-15"
  ],
  "query": "Iran Jaish",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Iran+Jaish&mode=artlist&format=json&maxrecords=25&startdatetime=20190210000000&enddatetime=20190315235959",
  "retrieved_at": "2026-09-02T21:07:46+00:00",
  "opened": [
   {
    "url": "https://www.latimes.com/world/la-fg-iran-bomb-suicide-revolutionary-guard-20190213-story.html",
    "title": "Iran suicide bombing kills 27 Revolutionary Guard members",
    "page_date": "2019-03-16",
    "domain": "latimes.com"
   },
   {
    "url": "http://idrw.org/pak-army-using-terror-group-to-carry-out-attacks-in-iran/",
    "title": "Pak army using terror group to carry out attacks in Iran \u2013 Indian Defence Research Wing",
    "page_date": "2019-03-10",
    "domain": "idrw.org"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 12556 **Government of Iran vs Jaish al-Adl**: dyad 12556 Government of Iran vs Jaish al-Adl (Iran) onset 2019-02-13 intensity 1 trigdate 2019-02-13, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T21:07:46+00:00: **Pak army using terror group to carry out attacks in Iran – Indian Defence Research Wing** — page date 2019-03-10 (window 2019-02-10..2019-03-15)
  http://idrw.org/pak-army-using-terror-group-to-carry-out-attacks-in-iran/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=Iran+Jaish&mode=artlist&format=json&maxrecords=25&startdatetime=20190210000000&enddatetime=20190315235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_12556_government_of_iran_vs_jaish_al_adl --approved-by joe`. The code never runs it.
