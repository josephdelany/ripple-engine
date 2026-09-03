# Dossier rule — pre-1987 admission dossiers (Brief A-6, registered 2026-09-02 before any dossier is built)

A dossier is the evidence file Joe reads before a pre-1987 record may enter `events`. The code builds
dossiers; **only Joe admits** (`python3 src/admit.py --dossier <id> --approved-by joe`); the code never
runs that line and refuses without the flag. Nothing here changes `events`.

## 1. Candidates
Session B's `data/candidates/pre1987_candidates.csv` (REGISTRATION.md) when it lands. Until then, and as the
first pass: every ICB v16 crisis with `trigdate` in 1946-01-01..1986-12-31 that has at least one actor
(`icb2v16.cracid`) in B's registered state set (producers, transit states, major consumers; COW ccodes).
Dossier id: `icb_<crisno>_<slug of crisname>`.

## 2. What a dossier holds (all from the primary record unless marked)
- dates: ICB `trigdate` / `termdate` (day precision; a missing day is coded 1 by the loader and the dossier
  says `date_precision: month`); COW/MID candidates: their own start/end fields.
- actors: crisis actors mapped through `src/state/countries.py` (unmapped COW codes named, never dropped);
  proposed roles: `trigent` (the triggering entity) → actor, the others → target; unknown when `trigent`
  is not among them.
- proposed class (codebook `type`, closed set): `chokepoint_disruption` if the crisis name contains
  canal / strait / blockade / tanker / shipping; `sanctions` if it contains embargo / sanction / boycott;
  otherwise `conflict_escalation`. Joe may change it on the dossier before admission.
- proposed severity band from ICB `viol`: 1→2, 2→3, 3→4, 4→5; `surprise` 3 (provisional); `confidence`
  `medium` (dataset record + one verified document) — all provisional until Joe writes otherwise.
- entities under the entity register: the mapped `country.*` ids with roles; `commodity.brent` and
  `commodity.wti` are NOT added by the code (asset roles are Joe's call).

## 3. The two-source rule (VERIFIED sources only; every citation opened by the code, URL and date recorded)
Source 1 is the primary dataset record (ICB case page `https://www.icb.umd.edu/dataviewer/?crisno=N`).
Source 2 must be one of the following, actually retrieved on the build date:
| route | status on 2026-09-02 | how it is used |
|---|---|---|
| FRUS, history.state.gov (primary documents 1945–1980s) | reachable: `/search?q=…&within=documents` returns document links; each document page carries its date | query = crisis name + trigger year; a document counts when its page date lies in [trigdate − 30 d, termdate + 30 d]; URL, title and page date recorded |
| UN Security Council resolutions, un.org/securitycouncil | HTTP 403 to scripts (also the UN Digital Library: JS challenge, empty body) | not usable by the code; the dossier says so; Joe may cite one by hand on the dossier |
| EIA petroleum chronology | the chronology URL redirects to eia.gov/reports (page gone); the spot-price page carries an event chart, not a dated record | not usable; recorded as unavailable |
| OPEC conference press releases, opec.org | HTTP 403 to scripts | not usable |
| NYT Archive API | no key in `tools/config.json` on this machine | not usable; the code never writes a key |
If no second source is found the dossier says **"second source: none found — not admissible"** and
`admissible: false`; `admit.py` refuses it whatever the flag says.

## 4. What the code never does
Never fabricates a citation, a date, an actor or a class outside the rules above; never writes to
`events`, `data/events.csv` or the situation records without `--approved-by joe`; never runs `admit.py`
itself. Every dossier carries `built_by: session A` and the build timestamp.

## 5. Post-1987 completeness (Brief A-12, registered 2026-09-02 before the sheet is computed)
Candidates, 1987-01-01..2026-12-31, from the sources session A already holds (read only), each a dated record with
at least one actor / party in B's registered state set (§1), and **not within 3 days of any corpus event date**:
| source | record | date used | actors |
|---|---|---|---|
| ICB v16 | one row per crisis | `trigdate` | crisis actors (`icb2v16.cracid`) |
| Dyadic MID 4.03 | one row per dispute with `hihost` ≥ 4 (use of force / war) | earliest dyad start | every state in the dispute's dyads |
| UCDP Dyadic v26.1 | one row per dyad at its onset (`start_date2`, the first year the dyad reached 25 deaths) | `start_date2` | `gwno_a`, `gwno_b` (state parties) |
| GPR daily (Caldara–Iacoviello, `gpr.GPRD` in `observations`) | one row per day above the 99th percentile of the 1987+ series (337.84 on 2026-09-02, n 14,489), consecutive days collapsed to the first | the day | none named (a global index) — listed for Joe, dossier built only when the FRUS/GDELT search names a registered state |
Output `data/candidates/post1987_candidates.csv` (`event_date, source, source_id, source_detail, actors, nearest_corpus_event, days_to_corpus`),
counts by decade and source in `post1987_candidates_summary.json`.
**Second source for this era**, in this order, every citation opened and dated by the code: (a) FRUS as §3 (volumes run
into the early 1990s; the search decides); (b) **GDELT DOC 2.0** article search (`api.gdeltproject.org/api/v2/doc/doc`,
`startdatetime`/`enddatetime` = the window, one request per 5 s; coverage begins 2017-01-01 per the API) — an
article whose `seendate` lies in [d − 3 d, d + 30 d] and whose title names the crisis or a party; URL, title, domain
and seendate recorded. Where neither route answers (in practice 1993–2016) the dossier says "second source: none
found — not admissible". Dossier ids: `icb_<crisno>_<slug>`, `mid_<disno>_<slug>`, `ucdp_<dyad_id>_<slug>`,
`gpr_<YYYYMMDD>`.

### §5.1 (2026-09-02, registered before the code, after the first post-1987 pass) — "refused" is not "absent"
The first post-1987 pass recorded `second source: none found — not admissible` on dossiers whose GDELT DOC request
had been **refused** (HTTP 429) or timed out, because the builder spaced requests 0.4 s apart while §5(b) registers
one per 5 s. That reads a fault of ours as a fact about the world, which §4 forbids. Corrected:
1. A second-source record carries a **status**, not a boolean: `found` (a dated document inside the window),
   `none_found` (the source answered, HTTP 200, and nothing in the reply fits the window), or **`undetermined`**
   (the source refused, errored or timed out — HTTP 4xx/5xx or a transport error). `admissible` is true only for
   `found`; `undetermined` is **not** an assertion that no second source exists, and the dossier says so in those
   words, with the HTTP status and the retry instruction.
2. A refused or failed fetch is never cached, so a re-run asks again.
3. Requests to a host with a stated limit are spaced by that limit (`HOST_SPACING_S`); GDELT DOC is set to 10 s
   after 5 s was still refused in practice on 2026-09-02, with one retry after 60 s on a 429.
4. `dossiers_index*.json` counts `found` / `none_found` / `undetermined` separately; the same three counts are what
   any report of this work must quote.

### §5.2 (2026-09-02, registered before the code, after the second post-1987 pass) — a query that names nobody is not a search
The second pass marked 8 GPR-spike dossiers admissible on a GDELT match to the single word `spike`: the candidate
names no party (a GPR spike is a global index reading), so the query degenerated to one generic term and matched any
article containing it. A keyword hit is not a second source for a specific event. Corrected: a second-source search
runs only when a query can be formed that **names at least one registered state** (a mapped `country.*` party of the
record) or carries **two or more content terms** from the record's own name. Where no such query exists — every GPR
row, and any record whose parties are all unmapped — no search is made, the status is `none_found`, and the reason is
recorded verbatim: *"a GPR spike names no party; no query can name a state, so no second source can be sought (§5.2)"*.
Such a row stays on the sheet for Joe, who may name the event himself; it is never admissible from a keyword.

## 6. Source repair for events already in the corpus (registered 2026-09-02, before the code)
Priority E: 72 events already feeding the engine rest on a weak source. They are repaired to the §2–§3 dossier
standard **before** any of the 473 post-1987 candidates is worked. Nothing is admitted or edited: a repair dossier is
evidence put in front of Joe, who decides. The three cohorts, by the query that defines each (run 2026-09-02):
| cohort | query | n | decades |
|---|---|---|---|
| encyclopaedia-only | `source_url` matches wikipedia/britannica | 31 | 1990s 4, 2000s 11, 2010s 5, 2020s 11 |
| bare EIA root | `source_url` is exactly `https://www.eia.gov` | 9 | 1970s 3, 1980s 6 |
| draft scaffolding | `description` contains "DRAFT coding" | 32 | 1980s 1, 1990s 6, 2000s 4, 2010s 11, 2020s 10 |
The three are disjoint; 72 events in all. *(The brief said 49 for the third cohort; the marker in the text yields 32.
The query is stated here so the difference is checkable, and a different definition of "scaffolding" supersedes this
one on Joe's word.)*

### 6.1 Routes, primary documents first — what each can and cannot answer
| route | reachable by script on 2026-09-02 | covers | what it yields |
|---|---|---|---|
| **FRUS** (history.state.gov) | yes, HTML search + dated document pages | 1945 to the early 1990s | a **document with its own date** |
| **UK National Archives Discovery** (`/API/search/records`, JSON, keyless, date-bounded) | yes | all eras, subject to release | a **file-level record** with covering dates, not a document date |
| **GDELT DOC 2.0** | yes, one request per 10 s (§5.1) | 2017 onward | a dated article |
| **CIA CREST** (cia.gov/readingroom) | **no** — every search form redirects to the landing page; results need JavaScript | 1940s–1990s | — |
| **UN Security Council / UN Digital Library** | **no** — HTTP 403 to scripts; the digital library serves a JS challenge | all | — |
| **OPEC archive** | **no** — HTTP 403 (Cloudflare) | 1960 onward | — |
| **US NARA catalog** | **no** — the API path returns the JavaScript app shell | all | — |

### 6.2 The three outcomes, and what each is allowed to mean
- **closed** — a primary document whose **own date** falls in [d − 3 d, d + 30 d] and whose title names the event or one
  of its registered parties. Only FRUS and GDELT yield this. The dossier records URL, title and document date.
- **partial** — an archival **file** whose covering dates contain the event date and whose title names the subject or a
  party (UK TNA). This is a pointer to primary material, not a record of the event; it is never counted as closed, and
  the dossier says which file and which covering dates.
- **blocked-by-declassification** — no route that could answer is reachable: the event's era is served only by CREST,
  the UN or OPEC archives (all closed to scripts), or the era's national files are not yet released. This is a statement
  about **access**, never about whether a source exists, and the dossier says so in those words.
A route that refuses or errors is `undetermined` and never written as an absence (§5.1). A query that can name nobody
is not run (§5.2).

### §6.3 (2026-09-02, registered before the code, after session A's post-2000 pass) — a news article is not a primary document
§6.2 listed GDELT DOC 2.0 as yielding a document that can **close** a repair. That is wrong as written: GDELT indexes
**press articles**, which are contemporaneous secondary reporting, not primary documents. Priority E asks for primary
documents first. The first post-2000 pass therefore reported 5 "closed" where it should have reported 5 contemporaneous
press reports, and one of those five was an aggregator **listing page** ("… : Latest News, Photos, Videos on …"), which
is not a report of anything. Corrected:
1. `closed` splits in two, and the dossier and index always say which:
   - **closed-primary** — a government or archival document with its own date: FRUS, the Federal Register. This is what
     Priority E asks for.
   - **closed-contemporaneous** — a dated press report naming the event (GDELT). Better than an encyclopaedia, since it
     is dated and contemporaneous; **not** a primary document, and never counted as one in any report.
2. A press hit whose title is an **aggregator or listing page** is rejected, not accepted: titles matching
   `latest news`, `photos , videos`, `news , photos`, `live updates`, `topics?/`, or ending in `: latest news` name no
   event and are treated as `none_found` with the rejected title recorded.
3. Any report of this work quotes the two counts separately. Collapsing them into one "closed" number is the same
   overstatement §5.2 corrected for keyword matches.

### §6.4 (2026-09-02, registered before the code) — naming a party is not naming the event
Two of the six press matches in session A's post-2000 pass named a party but reported something else: an opinion piece
("Are Saudi Arabia and the UAE No Longer U.S. Partners?", 2022-04-16) offered for a Houthi attack on Jeddah, and a
story on nuclear talks (2025-07-21) offered for a June 2025 strike. Both passed because the query terms include the
event's **parties**, and a party name appears in almost any article about that country. This is §5.2 recurring at a
finer grain. Corrected: a press hit must contain **at least one content term of the event's own title** — a term that
survives the stopword list and is not merely a party name — in addition to falling inside the window. An event whose
title yields no such term cannot be closed from the press at all, and says so. Rejected titles are recorded with the
reason, so the near-misses stay visible to Joe rather than disappearing.

### §6.5 (2026-09-02, registered before the code) — press matching is a suggestion, not a closure
§6.3 and §6.4 each tightened the press match and each was defeated by the next run: a party name matched any article
about that country, then a content term matched any article containing a generic word ("attack", "strike"). Four
attempts is enough evidence: **keyword overlap between an event title and an article title cannot identify a specific
event**, and no further tightening of it will be attempted. Corrected:
1. A GDELT hit is no longer an outcome that closes anything. Its outcome is **`press_candidate`**: a dated article,
   inside the window, that mentions the event's words — offered to Joe as *a place to look*, with the matched terms
   printed so he can dismiss it in one glance. It is never counted as a repair.
2. Only **closed-primary** (FRUS, Federal Register: a government document with its own date) repairs an event.
3. Every report of this work states `closed-primary` separately from `press_candidate`, and never adds them.
The consequence, stated plainly: for events outside US federal policy and outside FRUS's era, this toolchain can
currently offer Joe a place to look and nothing more. That is a limit of the reachable routes (`ROUTE_TABLE.md` §4),
not of the historical record.

### §6.6 (2026-09-02, registered before the code) — the UK release rule is coverage, not a failed call
Ten of session A's 27 post-2000 repairs recorded the UK National Archives as `undetermined` (HTTP 202, no body). All
ten are dated 2022-2025. Under the UK 20-year rule those files are not open yet, so the archive has nothing to return
and the 202 is the API declining a query it cannot serve, not a transient failure — a retry reproduced all ten exactly.
Recording it as `undetermined` overstates our uncertainty: we know why there is no answer. Corrected: an event dated
within **20 years of today** is `out_of_coverage` for this route, with the release rule named, and the route is not
called. Outside that window a 202 or any non-200 remains `undetermined` under §5.1.
