# Dossier ucdp_14636_government_of_nigeria_vs_ipob — Government of Nigeria vs IPOB

```json
{
 "id": "ucdp_14636_government_of_nigeria_vs_ipob",
 "built_by": "session A",
 "built_at": "2026-09-02T21:15:24+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "14636",
  "detail": "dyad 14636 Government of Nigeria vs IPOB (Nigeria) onset 2021-04-24 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2021-04-24",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2021-04-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.nigeria",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://thenationonlineng.net/its-disrespectful-to-nigeria/",
  "title": "  It disrespectful to Nigeria  | The Nation News Nigeria",
  "date": "2021-04-21",
  "domain": "thenationonlineng.net",
  "window": [
   "2021-04-21",
   "2021-05-24"
  ],
  "query": "Nigeria IPOB",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=Nigeria+IPOB&mode=artlist&format=json&maxrecords=25&startdatetime=20210421000000&enddatetime=20210524235959",
  "retrieved_at": "2026-09-02T21:15:24+00:00",
  "opened": [
   {
    "url": "https://thenationonlineng.net/its-disrespectful-to-nigeria/",
    "title": "  It disrespectful to Nigeria  | The Nation News Nigeria",
    "page_date": "2021-04-21",
    "domain": "thenationonlineng.net"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 14636 **Government of Nigeria vs IPOB**: dyad 14636 Government of Nigeria vs IPOB (Nigeria) onset 2021-04-24 intensity 1 trigdate 2021-04-24, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 475: country.nigeria (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.nigeria:unknown

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T21:15:24+00:00: **  It disrespectful to Nigeria  | The Nation News Nigeria** — page date 2021-04-21 (window 2021-04-21..2021-05-24)
  https://thenationonlineng.net/its-disrespectful-to-nigeria/
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=Nigeria+IPOB&mode=artlist&format=json&maxrecords=25&startdatetime=20210421000000&enddatetime=20210524235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_14636_government_of_nigeria_vs_ipob --approved-by joe`. The code never runs it.
