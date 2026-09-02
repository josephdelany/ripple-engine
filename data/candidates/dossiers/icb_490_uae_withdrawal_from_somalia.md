# Dossier icb_490_uae_withdrawal_from_somalia — UAE WITHDRAWAL FROM SOMALIA

```json
{
 "id": "icb_490_uae_withdrawal_from_somalia",
 "built_by": "session A",
 "built_at": "2026-09-02T21:03:38+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 490,
  "source": "icb",
  "source_id": "490",
  "detail": "UAE WITHDRAWAL FROM SOMALIA 2018-04-15..2018-04-22 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=490",
  "trigdate": "2018-04-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2018-04-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520
 ],
 "second_source": {
  "found": true,
  "status": "found",
  "route": "GDELT DOC 2.0",
  "url": "https://www.albawaba.com/news/ethiopia-demands-multinational-african-peacekeeping-force-stay-somalia-1122784",
  "title": "Ethiopia Demands Multinational African Peacekeeping Force to Stay in Somalia",
  "date": "2018-04-26",
  "domain": "albawaba.com",
  "window": [
   "2018-04-12",
   "2018-05-15"
  ],
  "query": "WITHDRAWAL FROM SOMALIA",
  "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=WITHDRAWAL+FROM+SOMALIA&mode=artlist&format=json&maxrecords=25&startdatetime=20180412000000&enddatetime=20180515235959",
  "retrieved_at": "2026-09-02T20:32:15+00:00",
  "opened": [
   {
    "url": "https://www.albawaba.com/news/ethiopia-demands-multinational-african-peacekeeping-force-stay-somalia-1122784",
    "title": "Ethiopia Demands Multinational African Peacekeeping Force to Stay in Somalia",
    "page_date": "2018-04-26",
    "domain": "albawaba.com"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 490 **UAE WITHDRAWAL FROM SOMALIA**: UAE WITHDRAWAL FROM SOMALIA 2018-04-15..2018-04-22 viol 3.0 trigdate 2018-04-15, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=490

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- GDELT DOC 2.0 document opened 2026-09-02T20:32:15+00:00: **Ethiopia Demands Multinational African Peacekeeping Force to Stay in Somalia** — page date 2018-04-26 (window 2018-04-12..2018-05-15)
  https://www.albawaba.com/news/ethiopia-demands-multinational-african-peacekeeping-force-stay-somalia-1122784
- search: https://api.gdeltproject.org/api/v2/doc/doc?query=WITHDRAWAL+FROM+SOMALIA&mode=artlist&format=json&maxrecords=25&startdatetime=20180412000000&enddatetime=20180515235959

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_490_uae_withdrawal_from_somalia --approved-by joe`. The code never runs it.
