# Verification log — Session E

*Dossiers are drafted by researchers working to `SPINE_REGISTRATION.md`. A dossier is a
claim that a source says something. This file records the independent checks made on those
claims by re-retrieving the document and comparing the quote character by character. It
exists because "the researcher said so" is exactly the standard this project rejects.*

Two kinds of check are logged:

- **mechanical** — `python3 src/spine_check.py`, which decides whether a dossier meets the
  registration (sections, a primary source, two distinct domains, retrieved_at and a quote
  on every source, resolvable [Sn] markers, a 120–250 word narrative, no wikipedia). A
  dossier that claims "complete" while failing any check is reported FAIL.
- **quote spot-check** — the reviewer re-fetches the cited URL and compares the quoted text
  against what comes back.

## 2026-09-02

### Mechanical

`src/spine_check.py` run on every dossier after each batch lands; results are recorded in
the batch commit message. No dossier has been accepted with verdict FAIL.

### Quote spot-checks

| dossier | source | claim checked | independent re-fetch | result |
|---|---|---|---|---|
| `oapec_embargo_1973` | S1 `history.state.gov/historicaldocuments/frus1969-76v36/d219` | that the document is "Minutes of Washington Special Actions Group Meeting", Washington, October 17, 1973, 3:05–4:04 p.m., and that Kissinger said "We don't expect an oil cut-off now in the light of the discussions with the Arab Foreign Ministers this morning", and Clements "In the Mediterranean there has already been a cut-back by about 12% in the amount of crude available." | re-fetched by the reviewer | **matches exactly** — document number, title, place-and-date line and both quotations |
| `oapec_embargo_1973` | S3 `history.state.gov/historicaldocuments/frus1969-76v36/d223` | that the document is "Memorandum Prepared in the Office of Economic Research, Central Intelligence Agency", Washington, October 19, 1973, and contains "Production will be reduced by not less than 5% a month until an Israeli withdrawal from occupied territories is completed" and that Libya, Abu Dhabi, Kuwait and Saudi Arabia "have either announced or threatened a total embargo against the United States." | re-fetched by the reviewer | **matches exactly** — title, date line and both quotations |
| registration §4 route table | `history.state.gov/.../frus1969-76v36/d221` | that FRUS document pages return full text with an exact place-and-date line | fetched by the reviewer before the registration was written | **confirmed** — "Minutes of Washington Special Actions Group Meeting", Washington, October 19, 1973, 10:04–10:57 a.m. |
| registration §4 route table | `presidency.ucsb.edu` | that the American Presidency Project serves presidential documents with a date line | fetched by the reviewer | **confirmed** — Nixon, "Address to the Nation About Policies To Deal With the Energy Shortages", November 7, 1973 |
| registration §4 route table | `archives.gov/federal-register/codification/executive-order/12170.html` | that executive orders are retrievable with title and date | fetched by the reviewer | **confirmed** — EO 12170, "Blocking Iranian Government property", November 14, 1979 |
| registration §4 route table | `nber.org/.../w16790.pdf` | that the Hamilton chronology is retrievable and quotable | fetched, saved and text-extracted by the reviewer (52 pp.) | **confirmed** — quotes used in the decade essays are copied from that extraction |
| decade essay sources | `bis.org/publ/work725.pdf` | that BIS Working Paper 725 is retrievable and quotable | fetched and text-extracted by the reviewer (31 pp.) | **confirmed** — Fueki et al., May 2018; abstract quoted in `docs/spine/1970s.md` |
| decade essay sources | `arxiv.org/abs/2409.00769` | title, authors, dates and abstract of the Kilian (2009) replication | fetched by the reviewer | **confirmed** — Ryan and Michieka, submitted 1 September 2024, revised 24 July 2025 |
| `iran_iraq_ceasefire_1988` | S1 `peacekeeping.un.org/.../past/uniimogbackgr.html` | that the UN records the ceasefire as announced on 8 August 1988 and effective at 0300 GMT on 20 August 1988, and resolution 619 of 9 August | re-fetched by the reviewer | **matches exactly** — all three quoted sentences. *Reviewer error worth recording: the first check fetched `uniimogfacts.html`, a different page on the same host, which does not carry those dates, and briefly looked like a discrepancy. The dossier's URL was right and mine was wrong.* |
| `praying_mantis_1988` | the `source_url` currently in the database, `asil.org/insights/volume/8/issue/25/...` | that the live corpus citation no longer serves the cited article | fetched by the reviewer | **confirmed unusable** — HTTP 403 to the reviewer. The researcher reported it redirecting to an unrelated 2004 article; the reviewer did not reproduce that specific behaviour and does not assert it. Both observations agree that the citation cannot be verified today, and the dossier records a working replacement URL |
| entity register | `data/oil.db` `entities` | the researchers' report that `country.syria`, `country.libya`, `country.algeria` and `institution.oapec` are missing | queried directly by the reviewer | **partly wrong, corrected**: `country.libya` **does** exist. `country.syria`, `country.algeria`, `institution.oapec` and `institution.un` are genuinely absent |

### Routes recorded as unusable (checked, not assumed)

`digitallibrary.un.org` HTTP 403 · `securitycouncilreport.org` HTTP 403 · `opec.org`
HTTP 402 · `cia.gov/readingroom/search/...` returns the site homepage with no results ·
the EIA petroleum chronology page is gone and the surviving weekly report page carries no
timeline. Two PDF mirrors of Kilian (2009) (`papers.economics.ubc.ca`,
`douglaslaxton.org`) failed TLS certificate validation and were not used.
