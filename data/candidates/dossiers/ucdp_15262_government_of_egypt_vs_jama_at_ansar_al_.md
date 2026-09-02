# Dossier ucdp_15262_government_of_egypt_vs_jama_at_ansar_al_ — Government of Egypt vs Jama'at Ansar al-Islam

```json
{
 "id": "ucdp_15262_government_of_egypt_vs_jama_at_ansar_al_",
 "built_by": "session A",
 "built_at": "2026-09-02T21:00:29+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "15262",
  "detail": "dyad 15262 Government of Egypt vs Jama'at Ansar al-Islam (Egypt) onset 2017-10-20 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2017-10-20",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2017-10-20",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "GDELT DOC 2.0",
  "query": "Egypt Jama Ansar",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Egypt+Jama+Ansar&mode=artlist&format=json&maxrecords=25&startdatetime=20171017000000&enddatetime=20171119235959",
  "search_status": 200,
  "window": [
   "2017-10-17",
   "2017-11-19"
  ],
  "opened": [
   {
    "url": "http://www.source-7.com/Msr/1359854.html",
    "title": "\u0628\u0627\u0644\u0623\u0633\u0645\u0627\u0621 .. \u0627\u0644\u0623\u0648\u0642\u0627\u0641 \u062a\u0639\u0644\u0646 \u0627\u0641\u062a\u062a\u0627\u062d 252 \u0645\u0633\u062c\u062f\u064b\u0627 \u062e\u0644\u0627\u0644 \u0633\u0628\u062a\u0645\u0628\u0631 \u0648\u0623\u0643\u062a\u0648\u0628\u0631 \u0648\u0646\u0648\u0641\u0645\u0628\u0631 2017",
    "page_date": "2017-11-17",
    "domain": "source-7.com"
   },
   {
    "url": "http://www.aleqtisady.com/egyptnews/tw-1426908",
    "title": "\u0628\u0627\u0644\u0623\u0633\u0645\u0627\u0621 .. \u0627\u0644\u0623\u0648\u0642\u0627\u0641 \u062a\u0639\u0644\u0646 \u0627\u0641\u062a\u062a\u0627\u062d 252 \u0645\u0633\u062c\u062f\u064b\u0627 \u062e\u0644\u0627\u0644 \u0633\u0628\u062a\u0645\u0628\u0631 \u0648\u0623\u0643\u062a\u0648\u0628\u0631 \u0648\u0646\u0648\u0641\u0645\u0628\u0631 2017",
    "page_date": "2017-11-17",
    "domain": "aleqtisady.com"
   },
   {
    "url": "http://www.zehabesha.com/war-ravaged-africa-and-the-myth-of-africa-rising-dawit-w-giorgis/",
    "title": "War Ravaged Africa and the Myth of Africa Rising \u2013 Dawit W Giorgis",
    "page_date": "2017-11-10",
    "domain": "zehabesha.com"
   },
   {
    "url": "http://www.bbc.com/persian/world-features-41684322",
    "title": "\u06af\u0631\u0648\u0647 \u062f\u0648\u0644\u062a \u0627\u0633\u0644\u0627\u0645\u06cc \u061b \u0638\u0647\u0648\u0631 \u0648 \u0632\u0648\u0627\u0644 \u062f\u0627\u0639\u0634 \u062f\u0631 \u0639\u0631\u0627\u0642 \u0648 \u0633\u0648\u0631\u06cc\u0647",
    "page_date": "2017-11-20",
    "domain": "bbc.com"
   }
  ],
  "retrieved_at": "2026-09-02T21:00:29+00:00",
  "note": "",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 15262 **Government of Egypt vs Jama'at Ansar al-Islam**: dyad 15262 Government of Egypt vs Jama'at Ansar al-Islam (Egypt) onset 2017-10-20 intensity 1 trigdate 2017-10-20, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.egypt:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** GDELT DOC 2.0 search `Egypt Jama Ansar` (https://api.gdeltproject.org/api/v2/doc/doc?query=Egypt+Jama+Ansar&mode=artlist&format=json&maxrecords=25&startdatetime=20171017000000&enddatetime=20171119235959, HTTP 200) returned 4 document(s) opened, none dated inside 2017-10-17..2017-11-19. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: بالأسماء .. الأوقاف تعلن افتتاح 252 مسجدًا خلال سبتمبر وأكتو (2017-11-17); بالأسماء .. الأوقاف تعلن افتتاح 252 مسجدًا خلال سبتمبر وأكتو (2017-11-17); War Ravaged Africa and the Myth of Africa Rising – Dawit W G (2017-11-10); گروه دولت اسلامی ؛ ظهور و زوال داعش در عراق و سوریه (2017-11-20)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_15262_government_of_egypt_vs_jama_at_ansar_al_ --approved-by joe`. The code never runs it.
