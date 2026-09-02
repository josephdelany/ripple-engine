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
