# Dossier ucdp_870_government_of_russia — Government of Russia

```json
{
 "id": "ucdp_870_government_of_russia",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "870",
  "detail": "dyad 870 Government of Russia (Soviet Union) vs Wahhabi movement of the Buinaksk district (Russia (Soviet Union)) onset 1999-09-02 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1999-09-02",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-09-02",
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
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Russia 1999",
  "search_url": "https://history.state.gov/search?q=Government+Of+Russia+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-08-03",
   "1999-10-02"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1894/d541",
    "title": "Mr. Gresham to Mr. White. (1894, With the Annual Message of the President, Transmitted to Congress, December 3, 1894)",
    "page_date": "1894-10-02",
    "retrieved_at": "2026-09-02T19:56:04+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1887/d580",
    "title": "No. 580.Mr. Bayard to Mr. Lothrop. (1887, For the Year 1887, Transmitted to Congress, With a Message of the President, June 26, 1888)",
    "page_date": "1887-01-18",
    "retrieved_at": "2026-09-02T19:56:05+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1916/d500",
    "title": "The Secretary of State to Senator Hitchcock (1916, With the Address of the President to Congress December 5, 1916)",
    "page_date": "1916-09-08",
    "retrieved_at": "2026-09-02T19:56:06+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1895p2/d308",
    "title": "Mr. Breckinridge to Mr. Olney. (1895, Part II, With the Annual Message of the President, Transmitted to Congress December 2, 1895)",
    "page_date": "1895-11-29",
    "retrieved_at": "2026-09-02T19:56:06+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1885/d677",
    "title": "Mr. Bayard to Mr. Cox. (1885, Transmitted to Congress, With the Annual Message of the President, December 8, 1885)",
    "page_date": "1869-01-19",
    "retrieved_at": "2026-09-02T19:56:07+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1924v01/d547",
    "title": "The Minister in China (Schurman) to the Secretary of State (1924, Volume I)",
    "page_date": "1924-02-29",
    "retrieved_at": "2026-09-02T19:56:08+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:56:04+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 870 **Government of Russia**: dyad 870 Government of Russia (Soviet Union) vs Wahhabi movement of the Buinaksk district (Russia (Soviet Union)) onset 1999-09-02 intensity 1 trigdate 1999-09-02, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Russia 1999` (https://history.state.gov/search?q=Government+Of+Russia+1999&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1999-08-03..1999-10-02. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: Mr. Gresham to Mr. White. (1894, With the Annual Message of  (1894-10-02); No. 580.Mr. Bayard to Mr. Lothrop. (1887, For the Year 1887, (1887-01-18); The Secretary of State to Senator Hitchcock (1916, With the  (1916-09-08); Mr. Breckinridge to Mr. Olney. (1895, Part II, With the Annu (1895-11-29); Mr. Bayard to Mr. Cox. (1885, Transmitted to Congress, With  (1869-01-19); The Minister in China (Schurman) to the Secretary of State ( (1924-02-29)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_870_government_of_russia --approved-by joe`. The code never runs it.
