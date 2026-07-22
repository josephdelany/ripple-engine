# Task Brief 03 — Systematic Event-Corpus Expansion (the harvester)

*Read CLAUDE.md first; its rules override this brief. Commit after each step. The goal: expand the event dataset from 20 toward the FULL universe of qualifying energy-geopolitical events in the price-data window (1987–present), while keeping every row human-verified and citable.*

## The cardinal rule
**Nothing enters the `events` table without Joe's approval.** The harvester produces CANDIDATES into `data/candidate_events.csv`. Joe reviews, edits codings, approves. Only `load_events.py` on the approved file touches the database. No exceptions — automated ingestion of unverified events is the failure mode this project is built against.

## Step 1 — Seed the candidate file with the known backlog
Create `data/candidate_events.csv` (same columns as events.csv, plus a `status` column: candidate/approved/rejected, and a `candidate_source` column: manual/gdelt). Seed it with these manually-identified conflict events (find one real primary/wire source URL for each — the sourcing pattern from events.csv; do NOT fabricate URLs, verify each resolves):
Desert Storm air campaign (1991-01-17) · Operation Desert Fox (1998-12-16) · September 11 attacks (2001-09-11) · Israel–Hezbollah war (2006-07-12) · Russia–Georgia war (2008-08-08) · Saudi-led intervention in Yemen (2015-03-26) · Gulf of Oman tanker attacks (2019-06-13) · Iran direct missile strike on Israel (2024-04-13) · Iran October strike on Israel (2024-10-01) · Israel–Iran war onset (2025-06-13).
Draft severity/surprise codings per EVENTS_CODEBOOK.md, marked as drafts. Commit.

## Step 2 — GDELT harvester (`src/harvest_gdelt.py`)
Query the GDELT 2.0 Events database (BigQuery is not available — use the raw daily/masterfile CSVs or the GDELT DOC/GEO APIs, whichever is reliably reachable without credentials) for candidate events 1987–present matching the codebook's six types. Filter strategy:
- CAMEO event codes for: military attack/clash (18x, 19x, 20x), embargo/sanctions (163), and actor pairs involving major producers (Iraq, Iran, Saudi Arabia, Russia, Libya, Venezuela, Kuwait, UAE) or energy institutions (OPEC).
- Aggregate mentions by date+actors; keep only high-coverage events (NumMentions above a threshold — tune so the output is hundreds, not tens of thousands).
- Dedupe against existing events.csv and candidate rows (±3 days, same actors).
Output: append to `data/candidate_events.csv` with status=candidate, candidate_source=gdelt, a drafted type/title, and the GDELT source URL for the most-mentioned article. If GDELT's bulk files are too heavy for this machine, sample by year and say so honestly in the output. Commit.

## Step 3 — Review interface (cheap and human)
`python3 src/review_candidates.py`: prints candidates one at a time with all fields; Joe types approve / reject / edit (edit = prompts for corrected fields). Approved rows (status=approved) are appended to `data/events.csv` in the exact existing format. Rejected rows keep status=rejected (never deleted — the rejection record is part of reproducibility). Commit.

## Step 4 — Report
Print: how many candidates from each source, how many awaiting review. Do NOT run any analysis on unapproved data. The registered/expanded rerun happens only after Joe finishes review.

## Out of scope
No writes to events.csv except via approved candidates. No analysis reruns. No new tables (the candidate file is a CSV, not a DB table). No LLM-invented events, dates, or URLs — every candidate traces to a real, checkable source link.

## Done when
candidate_events.csv exists with the 10 seeded conflict events (sourced) plus GDELT-harvested candidates, review_candidates.py works, and Joe has a clear count of what's waiting for his judgment.
