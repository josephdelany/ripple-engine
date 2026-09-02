# Dossier icb_162_formation_of_uar — FORMATION OF UAR

```json
{
 "id": "icb_162_formation_of_uar",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:16+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 162,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=162",
  "trigdate": "1958-02-01",
  "termdate": "1958-02-14",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1958-02-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Formation Of Uar 1958",
  "search_url": "https://history.state.gov/search?q=Formation+Of+Uar+1958&within=documents",
  "search_status": 200,
  "window": [
   "1958-01-02",
   "1958-03-16"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v13/d221",
    "title": "221. Memorandum of a Conversation Between the United Arab Republic Ambassador (Kamel) and the Assistant Secretary of State for Near Eastern and South Asian Affairs (Rountree), Department of State, Was",
    "page_date": "1958-10-08",
    "retrieved_at": "2026-09-02T19:14:12+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v12/d17",
    "title": "17. National Intelligence Estimate (1958\u20131960, Volume XII, Near East Region; Iraq; Iran; Arabian Peninsula)",
    "page_date": "1958-06-05",
    "retrieved_at": "2026-09-02T19:14:13+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v13/d218",
    "title": "218. Memorandum of a Conversation, Department of State, Washington, September 4, 1958 (1958\u20131960, Volume XIII, Arab-Israeli Dispute; United Arab Republic; North Africa)",
    "page_date": "1958-09-04",
    "retrieved_at": "2026-09-02T19:14:14+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v12/d52",
    "title": "52. Memorandum From the Assistant Secretary of State for Near Eastern and South Asian Affairs (Rountree) to Secretary of State Dulles (1958\u20131960, Volume XII, Near East Region; Iraq; Iran; Arabian Peni",
    "page_date": "1958-12-27",
    "retrieved_at": "2026-09-02T19:14:14+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v11/d165",
    "title": "165. Telegram From the Department of State to the Embassy in Jordan (1958\u20131960, Volume XI, Lebanon and Jordan)",
    "page_date": "1958-05-20",
    "retrieved_at": "2026-09-02T19:14:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1958-60v12/d210",
    "title": "210. Special National Intelligence Estimate (1958\u20131960, Volume XII, Near East Region; Iraq; Iran; Arabian Peninsula)",
    "page_date": "1959-12-15",
    "retrieved_at": "2026-09-02T19:14:16+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:14:12+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 162 **FORMATION OF UAR**: trigdate 1958-02-01, termdate 1958-02-14, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=162

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)
- 663: country.jor (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.iraq:unknown, country.jor:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Formation Of Uar 1958` (https://history.state.gov/search?q=Formation+Of+Uar+1958&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1958-01-02..1958-03-16.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 221. Memorandum of a Conversation Between the United Arab Re (1958-10-08); 17. National Intelligence Estimate (1958–1960, Volume XII, N (1958-06-05); 218. Memorandum of a Conversation, Department of State, Wash (1958-09-04); 52. Memorandum From the Assistant Secretary of State for Nea (1958-12-27); 165. Telegram From the Department of State to the Embassy in (1958-05-20); 210. Special National Intelligence Estimate (1958–1960, Volu (1959-12-15)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_162_formation_of_uar --approved-by joe`. The code never runs it.
