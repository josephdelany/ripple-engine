# Session G — retrieval routes, tested 2026-09-03 (first pass) and 2026-09-03 (second pass)
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


---

# Second pass, 2026-09-03 — what the first pass got wrong

The first pass concluded that the four 1970–72 commercial records could not reach a second
registrable domain, and named `opec.org` (402), `oxfordenergy.org` (403),
`crsreports.congress.gov` (403), UPI (no 1972 copy) and FRASER's *Economic Report of the
President 1974* (reachable, silent) as the evidence. **That conclusion was wrong, and the
error was the search's, not the archive's.**

The first pass looked for a second **primary** — the producers' own record, the
contemporaneous US economic record — and stopped when those failed. SPINE_REGISTRATION §1(a)
does not require two primaries. It requires *two independent sources, at least one primary*,
and says explicitly that "a scholarly secondary source (a monograph, a peer-reviewed article,
a working paper) may serve as the second source and never as the primary." Every one of these
records already had its primary (FRUS). What each needed was one independent domain of **any**
role — and two such domains were already in Session E's own tested-working set, unused by G:
`ora.ox.ac.uk` and `merip.org`. Recorded here rather than in a commit message, per charter
§2 rule 5.

## Routes that worked (second pass)

| route | what was requested | status |
|---|---|---|
| **ORA (Oxford University Research Archive)** `ora.ox.ac.uk/objects/…/files/…` | Bassam Fattouh, *An Anatomy of the Crude Oil Pricing System*, OIES **WPM 40**, January 2011 (83 pp.) | **works.** The PDF does not convert in the fetch client; it was saved and the text extracted locally (as with Hamilton). Substantive on **Libya September 1970** (the Occidental settlement, income tax on an increased posted price, retroactive payment, the other companies following) and on **Tehran 1971** (the most-favoured-nation chain from Libya's terms; "the negotiations conducted in Tehran resulted in a collective decision to raise the posted price and increase the tax rate"; "the Tehran Agreement"). One sentence on **Iraq 1972**: "Iraq opted for nationalisation in 1972", plus the October 1972 participation agreement for context. **Never names Tripoli** — checked by string search over the whole extracted text, 0 occurrences |
| **MERIP** `merip.org/YYYY/MM/<slug>/` | Michael Renner, "Restructuring the World Energy Industry", *MERIP Reports* No. 120, 26 January 1984; Shawna Bader-Blau, "Iraqi Unions vs. Big Oil", *Middle East Report* No. 243, 26 June 2007 | **works**, article text served with issue number and date. Renner 1984 is the **only** independent attestation of the **Tripoli** agreement retrieved by either pass, and it is one sentence. Bader-Blau 2007 gives one sentence on the 1972 IPC nationalisation |
| **govinfo** `govinfo.gov/app/details/…` (metadata) | S. Prt. 93rd Congress, *The International petroleum cartel, the Iranian consortium, and U.S. national security*, prepared for the Subcommittee on Multinational Corporations, **February 21, 1974** | **metadata page works**; the item exists and is dated. See the failures below for why its text could not be read |

## Routes that did not yield (second pass)

| route | what was requested | status |
|---|---|---|
| `govinfo.gov/content/pkg/CPRT-93SPRT28516/html/…` | HTML rendering of the 1974 Senate committee print | **HTTP 404** — no HTML rendering exists for this item |
| `govinfo.gov/content/pkg/CPRT-93SPRT28516/pdf/…` | the same item as PDF | **exceeds the fetch client's 10 MB limit.** Same wall Session E hit on the 1979 Senate print |
| `govinfo.gov/content/pkg/GPO-CRECB-1970-pt23/pdf/…` | bound *Congressional Record*, September 1970, for Senate floor material on the Libyan cutbacks | **exceeds 10 MB.** The bound Record is scanned page images; every part file is oversized |
| `govinfo.gov/content/pkg/CPRT-92HPRT70318O/pdf/…` | House Task Force on Energy briefings, 92nd Congress | **exceeds 10 MB** |
| `fraser.stlouisfed.org/title/economic-report-president-45/…-1972-…` | *Economic Report of the President, 1972*, as the natural place for the Tehran/Tripoli agreements | the URL guessed for the 1972 volume returns a **browse listing, not the volume**; the 1972 report was not located this pass. The 1974 volume was read in the first pass and is silent |
| `ora.ox.ac.uk` — Boué, "Opec at (More Than) Fifty: The Long Road to Baghdad, and Beyond", *Oxford Energy Forum* | a second ORA route for Tripoli | **retrieved and read in full (6 pp.); silent.** Zero occurrences of Tripoli, Tehran or Libya. It is about OPEC's founding, not 1971. A negative on a reachable route, recorded so it is not re-spent |
| `digitalarchive.wilsoncenter.org`, `nsarchive.gwu.edu` | declassified holdings on the 1971 agreements | searched, **no document link surfaced**. Neither was fetched, and neither is cited |

## What the second pass changed

| record | before | after | second domain |
|---|---|---|---|
| `libya_posted_price_confrontation_1970` | partial — fails (a) | **complete** | `ora.ox.ac.uk` (substantive) |
| `tehran_agreement_1971` | partial — fails (a) | **complete** | `ora.ox.ac.uk` (substantive, no figures) |
| `tripoli_agreement_1971` | partial — fails (a) | **complete, narrowly** | `merip.org` (one sentence, no figures) |
| `iraq_ipc_nationalisation_1972` | partial — fails (a) | **complete** | `ora.ox.ac.uk` + `merip.org` (both year-only) |

The gap that remains is **not** clause (a). It is `severity`: no source retrieved by any pass
gives barrels for any of the four, so all four keep `severity` = `unknown`. That is a
measurement, not a hole to be filled.

## Handoff to Session E (added by the second pass)

3. **`ora.ox.ac.uk` and `merip.org` should be read as general routes, not as one-off finds.**
   E's own dossiers established both, but SPINE_REGISTRATION §4's table does not list either,
   so a later session has to rediscover them. ORA serves the OIES working-paper series in full
   (Fattouh WPM 40 covers the whole 1928–2011 pricing history); MERIP serves *MERIP Reports*
   and *Middle East Report* article text back to at least 1984, with issue number and date.
4. **govinfo's pre-1990 scanned holdings are effectively closed to this toolchain.** Four
   separate items were requested this pass and all four exceeded the 10 MB fetch limit; the
   HTML renderings do not exist for that era. This is a tool limit, not an access limit, and it
   is worth recording as such: the documents are public and free, and we cannot read them.
