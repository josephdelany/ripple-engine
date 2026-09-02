# Dossier icb_499_galwan_valley_border_clash — GALWAN VALLEY BORDER CLASH

```json
{
 "id": "icb_499_galwan_valley_border_clash",
 "built_by": "session A",
 "built_at": "2026-09-02T21:10:06+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 499,
  "source": "icb",
  "source_id": "499",
  "detail": "GALWAN VALLEY BORDER CLASH 2020-05-05..2021-02-10 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=499",
  "trigdate": "2020-05-05",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2020-05-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.india",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://defence.pk/pdf/threads/chinese-troops-tighten-control-in-galwan-valley-after-india-trespasses-chinese-territory-source.666950/",
  "title": "Chinese troops tighten control in Galwan Valley after India trespasses Chinese territory : source",
  "date": "2020-05-18",
  "domain": "defence.pk",
  "window": [
   "2020-05-02",
   "2020-06-04"
  ],
  "query": "GALWAN VALLEY BORDER China India",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=GALWAN+VALLEY+BORDER+China+India&mode=artlist&format=json&maxrecords=25&startdatetime=20200502000000&enddatetime=20200604235959",
  "retrieved_at": "2026-09-02T20:09:06+00:00",
  "opened": [
   {
    "url": "https://defence.pk/pdf/threads/chinese-troops-tighten-control-in-galwan-valley-after-india-trespasses-chinese-territory-source.666950/",
    "title": "Chinese troops tighten control in Galwan Valley after India trespasses Chinese territory : source",
    "page_date": "2020-05-18",
    "domain": "defence.pk"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 499 **GALWAN VALLEY BORDER CLASH**: GALWAN VALLEY BORDER CLASH 2020-05-05..2021-02-10 viol 2.0 trigdate 2020-05-05, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=499

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.india:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:09:06+00:00: **Chinese troops tighten control in Galwan Valley after India trespasses Chinese territory : source** — page date 2020-05-18 (window 2020-05-02..2020-06-04)
  https://defence.pk/pdf/threads/chinese-troops-tighten-control-in-galwan-valley-after-india-trespasses-chinese-territory-source.666950/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=GALWAN+VALLEY+BORDER+China+India&mode=artlist&format=json&maxrecords=25&startdatetime=20200502000000&enddatetime=20200604235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_499_galwan_valley_border_clash --approved-by joe`. The code never runs it.
