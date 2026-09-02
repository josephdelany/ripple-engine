# Dossier icb_497_detention_of_hariri — DETENTION OF HARIRI

```json
{
 "id": "icb_497_detention_of_hariri",
 "built_by": "session A",
 "built_at": "2026-09-02T21:00:29+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 497,
  "source": "icb",
  "source_id": "497",
  "detail": "DETENTION OF HARIRI 2017-11-04..2017-11-21 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=497",
  "trigdate": "2017-11-04",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2017-11-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.lebanon",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "http://haber.sol.org.tr/dunya/lubnan-hukumeti-haririnin-suudiler-tarafindan-alikonuldugunu-dusunuyor-216531",
  "title": "L\u00fcbnan h\u00fck\u00fcmeti , Haririnin Suudiler taraf\u0131ndan al\u0131konuldu\u011funu d\u00fc\u015f\u00fcn\u00fcyor",
  "date": "2017-11-09",
  "domain": "haber.sol.org.tr",
  "window": [
   "2017-11-01",
   "2017-12-04"
  ],
  "query": "DETENTION HARIRI Lebanon",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=DETENTION+HARIRI+Lebanon&mode=artlist&format=json&maxrecords=25&startdatetime=20171101000000&enddatetime=20171204235959",
  "retrieved_at": "2026-09-02T20:23:37+00:00",
  "opened": [
   {
    "url": "http://24.com.eg/lebanon-news/3469036.html",
    "title": "\u0627\u062e\u0631 \u0627\u062e\u0628\u0627\u0631 \u0644\u0628\u0646\u0627\u0646 \u0627\u0644\u064a\u0648\u0645 \u0639\u0627\u062c\u0644 \u0627\u0644\u0623\u062d\u062f 26",
    "page_date": "2017-11-26",
    "domain": "24.com.eg"
   },
   {
    "url": "http://haber.sol.org.tr/dunya/lubnan-hukumeti-haririnin-suudiler-tarafindan-alikonuldugunu-dusunuyor-216531",
    "title": "L\u00fcbnan h\u00fck\u00fcmeti , Haririnin Suudiler taraf\u0131ndan al\u0131konuldu\u011funu d\u00fc\u015f\u00fcn\u00fcyor",
    "page_date": "2017-11-09",
    "domain": "haber.sol.org.tr"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 497 **DETENTION OF HARIRI**: DETENTION OF HARIRI 2017-11-04..2017-11-21 viol 1.0 trigdate 2017-11-04, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=497

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.lebanon:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:23:37+00:00: **Lübnan hükümeti , Haririnin Suudiler tarafından alıkonulduğunu düşünüyor** — page date 2017-11-09 (window 2017-11-01..2017-12-04)
  http://haber.sol.org.tr/dunya/lubnan-hukumeti-haririnin-suudiler-tarafindan-alikonuldugunu-dusunuyor-216531
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=DETENTION+HARIRI+Lebanon&mode=artlist&format=json&maxrecords=25&startdatetime=20171101000000&enddatetime=20171204235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_497_detention_of_hariri --approved-by joe`. The code never runs it.
