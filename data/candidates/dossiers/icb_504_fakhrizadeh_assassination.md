# Dossier icb_504_fakhrizadeh_assassination — FAKHRIZADEH ASSASSINATION

```json
{
 "id": "icb_504_fakhrizadeh_assassination",
 "built_by": "session A",
 "built_at": "2026-09-02T21:10:38+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 504,
  "source": "icb",
  "source_id": "504",
  "detail": "FAKHRIZADEH ASSASSINATION 2020-11-27..2020-12-03 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=504",
  "trigdate": "2020-11-27",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2020-11-27",
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
  "url": "https://www.republicworld.com/world-news/middle-east/iran-bestows-posthumous-military-honour-on-slain-nuclear-scientist-mohsen-fakhrizadeh.html",
  "title": "Iran\u00a0bestows posthumous military honour on slain nuclear scientist Mohsen Fakhrizadeh",
  "date": "2020-12-14",
  "domain": "republicworld.com",
  "window": [
   "2020-11-24",
   "2020-12-27"
  ],
  "query": "FAKHRIZADEH ASSASSINATION Iran",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=FAKHRIZADEH+ASSASSINATION+Iran&mode=artlist&format=json&maxrecords=25&startdatetime=20201124000000&enddatetime=20201227235959",
  "retrieved_at": "2026-09-02T20:42:45+00:00",
  "opened": [
   {
    "url": "https://www.republicworld.com/world-news/middle-east/iran-bestows-posthumous-military-honour-on-slain-nuclear-scientist-mohsen-fakhrizadeh.html",
    "title": "Iran\u00a0bestows posthumous military honour on slain nuclear scientist Mohsen Fakhrizadeh",
    "page_date": "2020-12-14",
    "domain": "republicworld.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 504 **FAKHRIZADEH ASSASSINATION**: FAKHRIZADEH ASSASSINATION 2020-11-27..2020-12-03 viol 2.0 trigdate 2020-11-27, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=504

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:42:45+00:00: **Iran bestows posthumous military honour on slain nuclear scientist Mohsen Fakhrizadeh** — page date 2020-12-14 (window 2020-11-24..2020-12-27)
  https://www.republicworld.com/world-news/middle-east/iran-bestows-posthumous-military-honour-on-slain-nuclear-scientist-mohsen-fakhrizadeh.html
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=FAKHRIZADEH+ASSASSINATION+Iran&mode=artlist&format=json&maxrecords=25&startdatetime=20201124000000&enddatetime=20201227235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_504_fakhrizadeh_assassination --approved-by joe`. The code never runs it.
