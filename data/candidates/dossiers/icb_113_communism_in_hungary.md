# Dossier icb_113_communism_in_hungary — COMMUNISM IN HUNGARY

```json
{
 "id": "icb_113_communism_in_hungary",
 "built_by": "session A",
 "built_at": "2026-09-02T19:12:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 113,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=113",
  "trigdate": "1947-02-10",
  "termdate": "1947-06-01",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1947-02-10",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.hungary",
   "role": "actor"
  },
  {
   "entity": "country.russia",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Communism In Hungary 1947",
  "search_url": "https://history.state.gov/search?q=Communism+In+Hungary+1947&within=documents",
  "search_status": 200,
  "window": [
   "1947-01-11",
   "1947-07-01"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v04/d254",
    "title": "The Charg\u00e9 in the United Kingdom (Clark) to the Secretary of State (1947, Volume IV, Eastern Europe; The Soviet Union)",
    "page_date": "1947-08-15",
    "retrieved_at": "2026-09-02T19:11:01+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v04/d242",
    "title": "The Minister in Hungary (Chapin) to the Secretary of State (1947, Volume IV, Eastern Europe; The Soviet Union)",
    "page_date": "1947-07-18",
    "retrieved_at": "2026-09-02T19:11:02+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v05/d290",
    "title": "Department of State Policy Statement (1949, Volume V, Eastern Europe; The Soviet Union)",
    "page_date": "1949-11-01",
    "retrieved_at": "2026-09-02T19:11:03+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v05/d4",
    "title": "Record of the 36th Meeting, Policy Planning Staff, Department of State, March 1, 1949, 3:30 p. m. to 4:30 p. m. (1949, Volume V, Eastern Europe; The Soviet Union)",
    "page_date": "1949-03-01",
    "retrieved_at": "2026-09-02T19:11:05+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v05/d16",
    "title": "The Ambassador in the Soviet Union (Kirk) to the Secretary of State (1949, Volume V, Eastern Europe; The Soviet Union)",
    "page_date": "1949-12-03",
    "retrieved_at": "2026-09-02T19:11:06+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1947v04/d267",
    "title": "The Minister in Hungary (Chapin) to the Secretary of State (1947, Volume IV, Eastern Europe; The Soviet Union)",
    "page_date": "1947-10-02",
    "retrieved_at": "2026-09-02T19:11:07+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:11:00+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 113 **COMMUNISM IN HUNGARY**: trigdate 1947-02-10, termdate 1947-06-01, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=113

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 310: country.hungary
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.hungary:actor, country.russia:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Communism In Hungary 1947` (https://history.state.gov/search?q=Communism+In+Hungary+1947&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1947-01-11..1947-07-01.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Chargé in the United Kingdom (Clark) to the Secretary of (1947-08-15); The Minister in Hungary (Chapin) to the Secretary of State ( (1947-07-18); Department of State Policy Statement (1949, Volume V, Easter (1949-11-01); Record of the 36th Meeting, Policy Planning Staff, Departmen (1949-03-01); The Ambassador in the Soviet Union (Kirk) to the Secretary o (1949-12-03); The Minister in Hungary (Chapin) to the Secretary of State ( (1947-10-02)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_113_communism_in_hungary --approved-by joe`. The code never runs it.
