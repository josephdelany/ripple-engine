# Dossier ucdp_807_government_of_russia — Government of Russia

```json
{
 "id": "ucdp_807_government_of_russia",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "807",
  "detail": "dyad 807 Government of Russia (Soviet Union) vs Republic of Armenia (Russia (Soviet Union)) onset 1990-08-31 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1990-08-31",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1990-08-31",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1989-92v31/d150",
  "title": "150. Memorandum of Conversation (1989\u20131992, Volume XXXI, START I, 1989\u20131991)",
  "date": "1990-08-01",
  "window": [
   "1990-08-01",
   "1990-09-30"
  ],
  "query": "Government Of Russia 1990",
  "search_url": "https://history.state.gov/search?q=Government+Of+Russia+1990&within=documents",
  "retrieved_at": "2026-09-02T19:53:30+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1918Russiav03/d173",
    "title": "The Secretary of Commerce (Redfield) to the Secretary of State (1918, Volume III, Russia)",
    "page_date": "1918-06-08",
    "retrieved_at": "2026-09-02T19:53:20+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v06/d159",
    "title": "159. Memorandum of Conversation (1981\u20131988, Volume VI, Soviet Union, October 1986\u2013January 1989)",
    "page_date": "1988-05-30",
    "retrieved_at": "2026-09-02T19:53:20+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1989-92v31/d71",
    "title": "71. Memorandum of Conversation (1989\u20131992, Volume XXXI, START I, 1989\u20131991)",
    "page_date": "1990-02-07",
    "retrieved_at": "2026-09-02T19:53:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1989-92v31/d150",
    "title": "150. Memorandum of Conversation (1989\u20131992, Volume XXXI, START I, 1989\u20131991)",
    "page_date": "1990-08-01",
    "retrieved_at": "2026-09-02T19:53:30+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 807 **Government of Russia**: dyad 807 Government of Russia (Soviet Union) vs Republic of Armenia (Russia (Soviet Union)) onset 1990-08-31 intensity 1 trigdate 1990-08-31, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:53:30+00:00: **150. Memorandum of Conversation (1989–1992, Volume XXXI, START I, 1989–1991)** — page date 1990-08-01 (window 1990-08-01..1990-09-30)
  https://history.state.gov/historicaldocuments/frus1989-92v31/d150
- search: https://history.state.gov/search?q=Government+Of+Russia+1990&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_807_government_of_russia --approved-by joe`. The code never runs it.
