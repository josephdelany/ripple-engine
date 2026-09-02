# Dossier icb_495_soleimani_assassination — SOLEIMANI ASSASSINATION

```json
{
 "id": "icb_495_soleimani_assassination",
 "built_by": "session A",
 "built_at": "2026-09-02T21:07:46+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 495,
  "source": "icb",
  "source_id": "495",
  "detail": "SOLEIMANI ASSASSINATION 2019-06-18..2020-01-08 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=495",
  "trigdate": "2019-06-18",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2019-06-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
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
  "url": "https://www.upi.com/Top_News/Voices/2019/07/10/EU-must-follow-US-lead-by-imposing-sanctions-on-Iran/4191562764009/",
  "title": "EU must follow U . S . lead by imposing sanctions on Iran",
  "date": "2019-07-10",
  "domain": "upi.com",
  "window": [
   "2019-06-15",
   "2019-07-18"
  ],
  "query": "SOLEIMANI ASSASSINATION United States Iran",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=SOLEIMANI+ASSASSINATION+United+States+Iran&mode=artlist&format=json&maxrecords=25&startdatetime=20190615000000&enddatetime=20190718235959",
  "retrieved_at": "2026-09-02T20:39:23+00:00",
  "opened": [
   {
    "url": "https://elaph.com/Web/NewsPapers/2019/06/1255065.html",
    "title": "\u0643\u064a\u0641 \u062a\u062a\u062c\u0647 \u0625\u064a\u0631\u0627\u0646 \u0646\u062d\u0648 \u0627\u0644\u062a\u0635\u0639\u064a\u062f \u0627\u0644\u0623\u0645\u0646\u064a \u0636\u062f \u062f\u0648\u0644 \u0627\u0644\u062e\u0644\u064a\u062c \u061f ",
    "page_date": "2019-06-24",
    "domain": "elaph.com"
   },
   {
    "url": "https://www.upi.com/Top_News/Voices/2019/07/10/EU-must-follow-US-lead-by-imposing-sanctions-on-Iran/4191562764009/",
    "title": "EU must follow U . S . lead by imposing sanctions on Iran",
    "page_date": "2019-07-10",
    "domain": "upi.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 495 **SOLEIMANI ASSASSINATION**: SOLEIMANI ASSASSINATION 2019-06-18..2020-01-08 viol 2.0 trigdate 2019-06-18, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=495

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 630: country.iran (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.iran:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:39:23+00:00: **EU must follow U . S . lead by imposing sanctions on Iran** — page date 2019-07-10 (window 2019-06-15..2019-07-18)
  https://www.upi.com/Top_News/Voices/2019/07/10/EU-must-follow-US-lead-by-imposing-sanctions-on-Iran/4191562764009/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=SOLEIMANI+ASSASSINATION+United+States+Iran&mode=artlist&format=json&maxrecords=25&startdatetime=20190615000000&enddatetime=20190718235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_495_soleimani_assassination --approved-by joe`. The code never runs it.
