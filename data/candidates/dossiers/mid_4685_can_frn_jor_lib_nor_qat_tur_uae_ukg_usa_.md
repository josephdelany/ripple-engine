# Dossier mid_4685_can_frn_jor_lib_nor_qat_tur_uae_ukg_usa_ — CAN FRN JOR LIB NOR QAT TUR UAE UKG USA dispute

```json
{
 "id": "mid_4685_can_frn_jor_lib_nor_qat_tur_uae_ukg_usa_",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4685",
  "detail": "dispute 4685 CAN-FRN-JOR-LIB-NOR-QAT-TUR-UAE-UKG-USA 2011-03-18..2011-08-23 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "2011-03-18",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2011-03-18",
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
   "entity": "country.hungary",
   "role": "unknown"
  },
  {
   "entity": "country.nor",
   "role": "unknown"
  },
  {
   "entity": "country.libya",
   "role": "unknown"
  },
  {
   "entity": "country.turkey",
   "role": "unknown"
  },
  {
   "entity": "country.jor",
   "role": "unknown"
  },
  {
   "entity": "country.qatar",
   "role": "unknown"
  },
  {
   "entity": "country.uae",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210,
  211,
  212,
  230,
  235,
  290,
  316,
  317,
  325,
  339,
  341,
  344,
  349,
  350,
  355,
  360,
  366,
  367,
  368,
  380,
  390,
  395
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "none",
  "note": "no verified route for 2011: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md \u00a75)",
  "opened": [],
  "window": null
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4685 **CAN FRN JOR LIB NOR QAT TUR UAE UKG USA dispute**: dispute 4685 CAN-FRN-JOR-LIB-NOR-QAT-TUR-UAE-UKG-USA 2011-03-18..2011-08-23 hihost 4 trigdate 2011-03-18, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 211: UNMAPPED
- 212: UNMAPPED
- 220: country.fra (registered state set)
- 230: UNMAPPED
- 235: UNMAPPED
- 255: country.deu (registered state set)
- 290: UNMAPPED
- 310: country.hungary
- 316: UNMAPPED
- 317: UNMAPPED
- 325: UNMAPPED (registered state set)
- 339: UNMAPPED
- 341: UNMAPPED
- 344: UNMAPPED
- 349: UNMAPPED
- 350: UNMAPPED
- 355: UNMAPPED
- 360: UNMAPPED (registered state set)
- 366: UNMAPPED
- 367: UNMAPPED
- 368: UNMAPPED
- 380: UNMAPPED
- 385: country.nor (registered state set)
- 390: UNMAPPED (registered state set)
- 395: UNMAPPED
- 620: country.libya (registered state set)
- 640: country.turkey (registered state set)
- 663: country.jor (registered state set)
- 694: country.qatar (registered state set)
- 696: country.uae (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.deu:unknown, country.hungary:unknown, country.nor:unknown, country.libya:unknown, country.turkey:unknown, country.jor:unknown, country.qatar:unknown, country.uae:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** none search `` (None, HTTP None) returned 0 document(s) opened, none dated inside ?..?. no verified route for 2011: FRUS volumes end in the early 1990s, GDELT DOC begins 2017-01-01 (DOSSIER_RULE.md §5)
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4685_can_frn_jor_lib_nor_qat_tur_uae_ukg_usa_ --approved-by joe`. The code never runs it.
