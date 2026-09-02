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
