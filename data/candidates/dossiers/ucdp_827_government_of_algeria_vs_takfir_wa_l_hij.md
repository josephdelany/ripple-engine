# Dossier ucdp_827_government_of_algeria_vs_takfir_wa_l_hij — Government of Algeria vs Takfir wa'l Hijra

```json
{
 "id": "ucdp_827_government_of_algeria_vs_takfir_wa_l_hij",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "827",
  "detail": "dyad 827 Government of Algeria vs Takfir wa'l Hijra (Algeria) onset 1991-12-09 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1991-12-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1991-12-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Algeria Vs Takfir Wa L Hijra 1991",
  "search_url": "https://history.state.gov/search?q=Government+Of+Algeria+Vs+Takfir+Wa+L+Hijra+1991&within=documents",
  "search_status": 200,
  "window": [
   "1991-11-09",
   "1992-01-08"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:53+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 827 **Government of Algeria vs Takfir wa'l Hijra**: dyad 827 Government of Algeria vs Takfir wa'l Hijra (Algeria) onset 1991-12-09 intensity 1 trigdate 1991-12-09, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Algeria Vs Takfir Wa L Hijra 1991` (https://history.state.gov/search?q=Government+Of+Algeria+Vs+Takfir+Wa+L+Hijra+1991&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1991-11-09..1992-01-08. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_827_government_of_algeria_vs_takfir_wa_l_hij --approved-by joe`. The code never runs it.
