# Dossier icb_488_israel_iran_clashes_in_syria — ISRAEL-IRAN CLASHES IN SYRIA

```json
{
 "id": "icb_488_israel_iran_clashes_in_syria",
 "built_by": "session A",
 "built_at": "2026-09-02T21:02:28+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 488,
  "source": "icb",
  "source_id": "488",
  "detail": "ISRAEL-IRAN CLASHES IN SYRIA 2018-02-10..2018-05-10 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=488",
  "trigdate": "2018-02-10",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2018-02-10",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://www.nmtv.tv/benjamin-netanyahu-accuses-iran-of-wanting-to-turn-lebanon-into-one-giant-missile-site/",
  "title": "Benjamin Netanyahu accuses Iran of wanting to turn Lebanon into one giant missile site  ",
  "date": "2018-03-05",
  "domain": "nmtv.tv",
  "window": [
   "2018-02-07",
   "2018-03-12"
  ],
  "query": "ISRAEL IRAN CLASHES Iran Israel",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=ISRAEL+IRAN+CLASHES+Iran+Israel&mode=artlist&format=json&maxrecords=25&startdatetime=20180207000000&enddatetime=20180312235959",
  "retrieved_at": "2026-09-02T20:24:48+00:00",
  "opened": [
   {
    "url": "https://www.urduvoa.com/a/israel-air-strikes/4248178.html",
    "title": "\u0627\u0633\u0631\u0627\u0626\u06cc\u0644\u06cc \u062c\u0646\u06af\u06cc \u0637\u06cc\u0627\u0631\u0648\u06ba \u06a9\u06d2 \u0634\u0627\u0645 \u0645\u06cc\u06ba \u0645\u062a\u0639\u062f\u062f \u0641\u0648\u062c\u06cc \u0679\u06be\u06a9\u0627\u0646\u0648\u06ba \u067e\u0631 \u062d\u0645\u0644\u06d2",
    "page_date": "2018-02-10",
    "domain": "urduvoa.com"
   },
   {
    "url": "http://www.irna.ir/ur/News/3578272",
    "title": "\u0635\u06c1\u06cc\u0648\u0646\u06cc \u062d\u06a9\u0645\u0631\u0627\u0646 \u062a\u0646\u0627\u0648 \u0627\u0648\u0631 \u062c\u06be\u0691\u067e\u0648\u06ba \u0645\u06cc\u06ba \u0627\u067e\u0646\u06cc \u0628\u0642\u0627 \u062f\u06cc\u06a9\u06be\u062a\u06d2 \u06c1\u06cc\u06ba : \u0627\u06cc\u0631\u0627\u0646\u06cc \u062a\u0631\u062c\u0645\u0627\u0646",
    "page_date": "2018-02-15",
    "domain": "irna.ir"
   },
   {
    "url": "https://www.nmtv.tv/benjamin-netanyahu-accuses-iran-of-wanting-to-turn-lebanon-into-one-giant-missile-site/",
    "title": "Benjamin Netanyahu accuses Iran of wanting to turn Lebanon into one giant missile site  ",
    "page_date": "2018-03-05",
    "domain": "nmtv.tv"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 488 **ISRAEL-IRAN CLASHES IN SYRIA**: ISRAEL-IRAN CLASHES IN SYRIA 2018-02-10..2018-05-10 viol 2.0 trigdate 2018-02-10, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=488

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.israel:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:24:48+00:00: **Benjamin Netanyahu accuses Iran of wanting to turn Lebanon into one giant missile site  ** — page date 2018-03-05 (window 2018-02-07..2018-03-12)
  https://www.nmtv.tv/benjamin-netanyahu-accuses-iran-of-wanting-to-turn-lebanon-into-one-giant-missile-site/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=ISRAEL+IRAN+CLASHES+Iran+Israel&mode=artlist&format=json&maxrecords=25&startdatetime=20180207000000&enddatetime=20180312235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_488_israel_iran_clashes_in_syria --approved-by joe`. The code never runs it.
