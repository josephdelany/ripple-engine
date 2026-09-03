# Session G — retrieval routes, tested 2026-09-03
*Every route below was requested in this session's own fetch log. The status is what came
back, not what is supposed to come back (SPINE_REGISTRATION §4's convention). This file is
Session G's; it does not amend SPINE_REGISTRATION.md, which is Session E's. Where a route
here changes E's §4 table, that is a handoff to E, recorded at the bottom.*

## Routes that worked

| route | what was requested | status |
|---|---|---|
| **FRUS** `history.state.gov/historicaldocuments/…` | `frus1955-57v16` volume page and Docs 1, 2; `frus1964-68v19` volume page and Docs 149, 152, 155, 160, 180; `frus1969-76v36` volume page, `ch2`, `ch3`, `ch4`, and Docs 55, 79, 85, 86, 87, 88, 124 | **works throughout**, including for 1956, 1967 and the 1969–1974 energy volume. Section pages (`/chN`) list documents with dates; `/comp2` returns 404 and is not the section URL |
| **American Presidency Project** `presidency.ucsb.edu/documents/…` | LBJ, "Address at the State Department's Foreign Policy Conference for Educators", June 19, 1967; Nixon, "Special Message to the Congress on Energy Resources", June 4, 1971 | **works.** The LBJ address is primary for the 1967 dossier. The Nixon 1971 energy message contains nothing on Middle East or North African supply — checked, and reported as a negative |
| **UN Peacekeeping** `peacekeeping.un.org/sites/default/files/past/…` | `unef1backgr2.html` (UNEF I background) | **works**; primary for the facts of the UN operation and the canal clearance (as E's Amendment 1 A.1 already recorded). `unefi.htm` is a summary page and carries none of the 1967 detail |
| **NBER** `nber.org/system/files/working_papers/…pdf` | Hamilton, *Historical Oil Shocks*, WP 16790 | **works**, but the PDF does not convert to text in the fetch client; it was saved and the text extracted locally. Covers Suez 1956–57 in detail; contains **no** mention of the Six-Day War, Libya 1970, the Tehran agreement or the IPC nationalisation |
| **FRASER** `fraser.stlouisfed.org` (new — not in E's §4 table) | *Economic Report of the President, 1974*, full text | **reachable and searchable.** Negative result on the substance: no mention of the Tehran or Tripoli agreements, posted prices, Libya, producer nationalisation, or Iraq. Recorded because a negative on a reachable route is evidence, and the next session should not re-spend the fetch |

## Routes that did not yield

| route | what was requested | status |
|---|---|---|
| `upi.com/Archives` | 1972 Iraq / Iraq Petroleum Company nationalisation | search returns no 1972 wire copy; only later Iraq energy stories. Consistent with E's Amendment 1 A.3 ("intermittent") |
| `opec.org`, `oxfordenergy.org`, `crsreports.congress.gov` | not re-requested this session | E's Amendment 2 already records 402 / 403 / 403; nothing here contradicts it |

## What the tests mean for the 1970–72 records

Three of the six Session G dossiers (Libya 1970, Tehran 1971, Tripoli 1971) rest on
`history.state.gov` alone, and a fourth (IPC 1972) on a single document there. That is not a
shortfall of effort: FRUS is the only free route tested that carries the commercial history of
the concession fights, and the two obvious alternatives — the producers' own record (`opec.org`,
402) and the contemporaneous US economic record (FRASER's *Economic Report*, reachable but
silent) — were both checked. SPINE_REGISTRATION Amendment 2 registered this outcome in advance
for the `opec_decision` class; these four records are its instances.

## Handoff to Session E

Two entries would belong in SPINE_REGISTRATION §4 if E agrees:
1. **FRASER (`fraser.stlouisfed.org`) is reachable** and serves full text of the *Economic
   Report of the President* series. Useful for official US economic statements; it did not
   carry the 1970–72 oil-concession material.
2. **FRUS section pages are `/chN`, not `/compN`**, and FRUS 1969–1976 Volume XXXVI
   (*Energy Crisis, 1969–1974*) is published and is the single richest primary route for the
   1969–74 oil-commercial record. E's Amendment 1 A.2 records the Reagan-era volumes as
   unpublished; that is unrelated to this one and both statements hold.

## Handoff to Session A — entity register gaps found while writing these dossiers

Named in retrieved primary sources and absent from `entities`: `country.france`,
`country.syria`, `country.jordan`, `country.algeria`, Qatar, the United Arab Emirates, and
**any entity type for an oil company** (Occidental, the Oasis partners, Shell, BP, IPC).
Reported, never invented.
