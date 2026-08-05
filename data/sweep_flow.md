# Sweep flow (PRISMA-style) -- corpus completeness census  (2026-08-05)

*Systematic cross-reference of the event corpus against three authoritative oil-shock
chronologies. This is a CENSUS check (does the corpus miss any documented MAJOR shock?),
not an exhaustive re-derivation of all corpus events. Sources: Hamilton NBER w16790;
Wikipedia List of oil crises; EIA Today-in-Energy id=67865 + CRS R45281. Nothing dropped
silently -- every chronicled candidate has a recorded disposition in data/sweep_ledger.csv.*

```
  chronicled major shocks (3 legs, 1990-2026) ............ 15
  after de-duplication across legs ...................... 15   (curated distinct)
  screened against the corpus .......................... 15
         |
         |-- already in corpus ......................... 10
         |-- ADMITTED this sweep (5 gates, 2-source) ... 3
         |-- JOE-QUEUE (borderline, Joe's call) ........ 1
         '-- REJECTED (codebook reason) ............... 1
```

## Disposition of every chronicled candidate
| leg | date | shock | status | detail |
|---|---|---|---|---|
| Hamilton+Wiki | 1990-08-02 | Iraq invades Kuwait (First Gulf War) | **already-in-corpus** | iraq_invades_kuwait_1990 |
| Hamilton | 1991-01-17 | Operation Desert Storm air campaign | **already-in-corpus** | desert_storm_air_campaign_1991 |
| Hamilton+Wiki | 1997-07-02 | East Asian financial crisis (Thai baht float) | **already-in-corpus** | thai_baht_float_1997 |
| Hamilton | 1999-03-23 | OPEC production cut ends the price collapse | **already-in-corpus** | opec_cut_1999 |
| Hamilton | 2002-12-02 | Venezuela PDVSA general strike (2.1 mb/d lost) | **JOE-QUEUE** | venezuela_general_strike_2002 (borderline -> Joe) |
| Hamilton+Wiki | 2003-03-20 | US invasion of Iraq (Second Gulf War) | **already-in-corpus** | iraq_war_begins_2003 |
| Hamilton+Wiki | 2008-09-15 | Global financial crisis / demand collapse | **already-in-corpus** | lehman_collapse_2008 |
| Wiki | 2014-11-27 | OPEC declines to cut -> 2014-16 shale glut | **already-in-corpus** | opec_declines_cut_2014 |
| Wiki | 2020-03-06 | OPEC+ price war (Saudi-Russia) | **already-in-corpus** | opec_talks_collapse_2020 |
| Wiki | 2020-03-11 | COVID-19 pandemic demand crash | **already-in-corpus** | covid_pandemic_declared_2020 |
| Wiki | 2022-02-24 | Russia invades Ukraine | **already-in-corpus** | russia_invades_ukraine_2022 |
| EIA+Wiki | 2026-02-28 | US+Israel strike Iran (2026 escalation) | **admitted** | iran_israel_us_strike_2026 (this sweep) |
| EIA+CRS | 2026-03-04 | Iran declares the Strait of Hormuz closed | **admitted** | hormuz_closure_2026 (this sweep) |
| EIA+CNN | 2026-06-17 | US-Iran MOU reopens the Strait of Hormuz | **admitted** | us_iran_hormuz_mou_2026 (this sweep) |
| EIA | 2026-04-29 | Brent peaks at $118/bbl | **REJECTED** | rejected: price OUTCOME, not an event (codebook rule 4) |

## Finding
The corpus covers **every documented major oil shock 1990-2025** in all three chronologies.
The one real gap -- the **2026 Strait of Hormuz crisis** -- is now closed (3 sourced events,
F1.1). One borderline candidate (the **Venezuela 2002-03 PDVSA strike-onset**, whose OPEC
response `opec_hike_jan_2003` is already coded) is queued for Joe. Brent's $118 peak is
recorded REJECTED -- it is a price outcome, not an event.

Reproduce: `python3 src/sweep.py`. Every admitted event's sources are in
`data/state/two_source_log.csv`; the queue is `data/borderline_queue.csv`.
