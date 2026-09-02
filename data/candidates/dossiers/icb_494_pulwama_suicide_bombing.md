# Dossier icb_494_pulwama_suicide_bombing — PULWAMA SUICIDE BOMBING

```json
{
 "id": "icb_494_pulwama_suicide_bombing",
 "built_by": "session A",
 "built_at": "2026-09-02T21:07:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 494,
  "source": "icb",
  "source_id": "494",
  "detail": "PULWAMA SUICIDE BOMBING 2019-02-14..2019-03-01 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=494",
  "trigdate": "2019-02-14",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2019-02-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://www.oneindia.com/india/nyt-refers-pulwama-terror-attack-as-explosion-twitterati-ask-was-9-11-just-a-plane-crash-2863580.html",
  "title": "NYT refers Pulwama terror attack as  explosion , Twitterati ask was  9 / 11 just a plane crash ? ",
  "date": "2019-03-12",
  "domain": "oneindia.com",
  "window": [
   "2019-02-11",
   "2019-03-16"
  ],
  "query": "PULWAMA SUICIDE BOMBING India Pakistan",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=PULWAMA+SUICIDE+BOMBING+India+Pakistan&mode=artlist&format=json&maxrecords=25&startdatetime=20190211000000&enddatetime=20190316235959",
  "retrieved_at": "2026-09-02T20:38:47+00:00",
  "opened": [
   {
    "url": "https://www.oneindia.com/india/nyt-refers-pulwama-terror-attack-as-explosion-twitterati-ask-was-9-11-just-a-plane-crash-2863580.html",
    "title": "NYT refers Pulwama terror attack as  explosion , Twitterati ask was  9 / 11 just a plane crash ? ",
    "page_date": "2019-03-12",
    "domain": "oneindia.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 494 **PULWAMA SUICIDE BOMBING**: PULWAMA SUICIDE BOMBING 2019-02-14..2019-03-01 viol 2.0 trigdate 2019-02-14, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=494

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:38:47+00:00: **NYT refers Pulwama terror attack as  explosion , Twitterati ask was  9 / 11 just a plane crash ? ** — page date 2019-03-12 (window 2019-02-11..2019-03-16)
  https://www.oneindia.com/india/nyt-refers-pulwama-terror-attack-as-explosion-twitterati-ask-was-9-11-just-a-plane-crash-2863580.html
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=PULWAMA+SUICIDE+BOMBING+India+Pakistan&mode=artlist&format=json&maxrecords=25&startdatetime=20190211000000&enddatetime=20190316235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_494_pulwama_suicide_bombing --approved-by joe`. The code never runs it.
