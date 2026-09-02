# Dossier mid_4283_afg_can_frn_pak_rus_tur_ukg_usa_dispute — AFG CAN FRN PAK RUS TUR UKG USA dispute

```json
{
 "id": "mid_4283_afg_can_frn_pak_rus_tur_ukg_usa_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4283",
  "detail": "dispute 4283 AFG-CAN-FRN-PAK-RUS-TUR-UKG-USA 2001-09-15..2001-12-22 hihost 5",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "2001-09-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2001-09-15",
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
   "entity": "country.canada",
   "role": "unknown"
  },
  {
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.deu",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.turkey",
   "role": "unknown"
  },
  {
   "entity": "country.afg",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210,
  230,
  235,
  350,
  702,
  704,
  900
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2001: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4283 **AFG CAN FRN PAK RUS TUR UKG USA dispute**: dispute 4283 AFG-CAN-FRN-PAK-RUS-TUR-UKG-USA 2001-09-15..2001-12-22 hihost 5 trigdate 2001-09-15, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 220: country.fra (registered state set)
- 230: UNMAPPED
- 235: UNMAPPED
- 255: country.deu (registered state set)
- 350: UNMAPPED
- 365: country.russia (registered state set)
- 640: country.turkey (registered state set)
- 700: country.afg
- 702: UNMAPPED
- 704: UNMAPPED
- 770: country.pak
- 900: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.deu:unknown, country.russia:unknown, country.turkey:unknown, country.afg:unknown, country.pak:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2001: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4283_afg_can_frn_pak_rus_tur_ukg_usa_dispute --approved-by joe`. The code never runs it.
