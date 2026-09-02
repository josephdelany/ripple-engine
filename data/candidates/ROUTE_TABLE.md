# Primary-document routes — what is actually reachable, and what each covers by era
*Session A owns this table and the fetch/verify path. Probed live on 2026-09-02; every row is the result of a
request made that day, not a claim from documentation. Re-probe before trusting a row that is more than a few
weeks old. Companion rules: `DOSSIER_RULE.md` §5.1 (a refusal is not an absence), §5.2 (a query that names nobody
is not a search), §6 (what closed / partial / blocked-by-declassification are each allowed to mean).*

## 1. Reachable, keyless, wired into `src/source_repair.py`

| route | endpoint | era it covers | what a hit yields | rate limit observed |
|---|---|---|---|---|
| **FRUS** (US State Dept, Office of the Historian) | `history.state.gov/search?q=…&within=documents`, HTML; each document page carries its own dateline | 1945 → early 1990s (volume coverage; nothing later) | a **document with its own date** → can close | none stated; 0.4 s spacing used |
| **Federal Register** | `federalregister.gov/api/v1/documents.json`, JSON, no key | **1994 →** (verified on 2018 and 2019 queries) | a **dated** rule, notice or presidential document → can close | none stated; 0.4 s spacing used |
| **UK National Archives Discovery** | `discovery.nationalarchives.gov.uk/API/search/records`, JSON, no key, date-bounded | all eras **subject to release**: the 20/30-year rule means files after roughly the mid-1990s are largely unreleased | a **file-level record** with covering dates, not a document date → **partial only** | none stated; 0.4 s spacing used |
| **GDELT DOC 2.0** | `api.gdeltproject.org/api/v2/doc/doc`, JSON, no key | **2017 →** | a **dated article** → can close | **one request per 10 s** (5 s was still refused in practice; HTTP 429) |

## 2. Reachable but not wired, with the reason

| route | endpoint | why not wired |
|---|---|---|
| **govinfo** (GPO) | `api.govinfo.gov/search`, **POST** with a JSON body; `api.data.gov` key required | `DEMO_KEY` answers (verified: 1,661 hits for a Federal Register query) but it is a **shared public demo key with a low hourly cap**, so a run of any size would be throttled and would read as an absence. A free personal key removes the cap and is Joe's to obtain (`api.data.gov/signup`); the route is otherwise ready. Its Federal Register content is already covered keylessly by the row above. |

## 3. Not reachable by script on 2026-09-02

| route | what happens | consequence |
|---|---|---|
| **CIA CREST / FOIA reading room** | every search form (`/readingroom/search/site/…`, `?search_api_fulltext=`, `/advanced-search-view`) returns the **landing page**, 38 KB, zero document links; results need JavaScript | the main declassified-intelligence route for 1940s–1990s is closed to us |
| **UN Security Council / UN Digital Library** | `un.org/securitycouncil` → HTTP 403; `digitallibrary.un.org/search` → 202 with an empty body (JS challenge) | UN resolutions cannot be cited automatically; Joe may cite one by hand |
| **OPEC archive** | `opec.org` press/RSS paths → HTTP 403 (Cloudflare "Just a moment") | OPEC conference records cannot be cited automatically |
| **US NARA catalog** | `catalog.archives.gov/api/v1` and `/api/v2/records/search` return the **JavaScript app shell**, not JSON | the US national catalogue is closed to us |

## 4. What this means by era — the honest coverage map

| era | can close | partial only | practical outcome |
|---|---|---|---|
| 1945–1993 | FRUS | UK TNA (released) | good for diplomacy; **blocked** where the record is CIA/UN/OPEC |
| 1994–1999 | Federal Register (US policy) | UK TNA (mostly released) | good for US measures; thin for events abroad |
| 2000–2016 | Federal Register (US policy only) | UK TNA (**largely unreleased**, 20/30-year rule) | **the hard window**: no free full-text news search reaches back here, so a non-US event is often blocked by access, not absent from history |
| 2017 → | GDELT DOC 2.0, Federal Register | — | good |

The 2000–2016 gap is the reason the automatic second-source pass returned "absent" for 438 of 473 post-1987
candidates. That number measures **our reach**, not the historical record, and no report may present it otherwise.
