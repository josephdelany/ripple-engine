# Dossier icb_507_us_taiwan_diplomatic_visits_ii — US-TAIWAN DIPLOMATIC VISITS II

```json
{
 "id": "icb_507_us_taiwan_diplomatic_visits_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T21:13:32+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 507,
  "source": "icb",
  "source_id": "507",
  "detail": "US-TAIWAN DIPLOMATIC VISITS II 2021-01-09..2021-11-15 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=507",
  "trigdate": "2021-01-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2021-01-09",
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
   "entity": "country.taiwan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://www.tribunnews.com/internasional/2021/01/08/cina-as-bermain-dengan-api-jika-kirimkan-dubes-ke-taiwan",
  "title": "Cina : AS  Bermain Dengan Api  Jika Kirimkan Dubes ke Taiwan",
  "date": "2021-01-08",
  "domain": "tribunnews.com",
  "window": [
   "2021-01-06",
   "2021-02-08"
  ],
  "query": "TAIWAN DIPLOMATIC VISITS China Taiwan",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=TAIWAN+DIPLOMATIC+VISITS+China+Taiwan&mode=artlist&format=json&maxrecords=25&startdatetime=20210106000000&enddatetime=20210208235959",
  "retrieved_at": "2026-09-02T20:44:34+00:00",
  "opened": [
   {
    "url": "https://elaph.com/Web/News/2021/01/1315892.html",
    "title": "\u0628\u0643\u064a\u0646 \u062a\u062d\u0630\u0631 \u0648\u0627\u0634\u0646\u0637\u0646 \u0645\u0646  \u062b\u0645\u0646 \u0628\u0627\u0647\u0638  \u0625\u0630\u0627 \u0632\u0627\u0631\u062a \u0633\u0641\u064a\u0631\u062a\u0647\u0627 \u062a\u0627\u064a\u0648\u0627\u0646",
    "page_date": "2021-01-08",
    "domain": "elaph.com"
   },
   {
    "url": "https://www.tribunnews.com/internasional/2021/01/08/cina-as-bermain-dengan-api-jika-kirimkan-dubes-ke-taiwan",
    "title": "Cina : AS  Bermain Dengan Api  Jika Kirimkan Dubes ke Taiwan",
    "page_date": "2021-01-08",
    "domain": "tribunnews.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 507 **US-TAIWAN DIPLOMATIC VISITS II**: US-TAIWAN DIPLOMATIC VISITS II 2021-01-09..2021-11-15 viol 1.0 trigdate 2021-01-09, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=507

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.taiwan:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:44:34+00:00: **Cina : AS  Bermain Dengan Api  Jika Kirimkan Dubes ke Taiwan** — page date 2021-01-08 (window 2021-01-06..2021-02-08)
  https://www.tribunnews.com/internasional/2021/01/08/cina-as-bermain-dengan-api-jika-kirimkan-dubes-ke-taiwan
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=TAIWAN+DIPLOMATIC+VISITS+China+Taiwan&mode=artlist&format=json&maxrecords=25&startdatetime=20210106000000&enddatetime=20210208235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_507_us_taiwan_diplomatic_visits_ii --approved-by joe`. The code never runs it.
