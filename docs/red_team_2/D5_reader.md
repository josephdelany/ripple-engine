> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-5: 30 real headlines vs a human read

Repo: `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`, branch `v2-day1`,
HEAD `b7c8ec1` (verified `git log -1`; note the repo had a **different, concurrently-running
session actively writing to `data/`** throughout this review — `data/alert_queue.csv`,
`data/watch_seen.db`, `data/candidates/dossiers/*` etc. changed under me between 15:07 and
15:13 local time. That churn was not caused by this review: it went entirely through a read-only
sqlite URI connection (`file:...?mode=ro`) and `RIPPLE_READER=off`, and nothing under `data/` was
opened for writing by my scripts. `git status --porcelain data/` before and after shows the same
set of pre-existing dirty files plus that other session's new ones — none attributable to me.)

## 0. Which "reader" is which

There are **two separate LLM-caging systems** in this repo, both matching the brief's description
loosely but serving different roles. This split itself is worth stating plainly before the table:

1. **`src/reader.py`** — "the caged reader" (`CLAIM_LEDGER_REGISTRATION.md` §2 + Amendment 3).
   Turns a headline or article into `event_class` (7-way closed vocab from
   `load_events.VALID_TYPES`), `entities` (closed vocab, each with a role), and `claims`
   (verbatim-quote-only, fabrication-guarded). **This is the live path**: `src/story_read.py`
   (Story page) and `src/feed_build.py` (`feed.json`, the Feed shown by `./go` at
   `/app`) both call it directly, ungated, on every fresh headline
   (`src/feed_build.py:117` `reads = R.read_headlines(...)`). Its output never includes a date
   field of any kind, and never includes a confidence score — confirmed by reading
   `STORY_SCHEMA`/`BATCH_SCHEMA` (`src/reader.py:228-256`) and `cage()`/`cage_claim()`
   (`src/reader.py:340-456`): the schema has `event_class`, `entities`, `unmapped`, `claims` and
   nothing else. This is a structural fact, not a run-time artifact — see Finding F1.

2. **`src/extract_events.py`** (+ `src/extract_prepare.py`, `ops/extract_agent.md`, not read in
   depth here) — a **separate** worker/cage pair used for **corpus admission** ("living-engine
   step 2"). Its schema *does* carry `event_date`, `date_precision`, `confidence`,
   `severity_suggestion`, `surprise_suggestion` and a URL fabrication guard. Clean proposals land
   in `data/candidate_events.csv`, not `events.csv` — `apply_review.py` + `load_events.py` are
   still, per the docstring, "the one sanctioned, gated path" into canon.

Both `triage.py` (regex-only, no LLM, used for the paste-a-headline `/triage` card and as the
**fallback implementation inside `reader.py`**) and `src/engine/read.py` (nothing to do with news
reading — it's the analog-retrieval statistical read over the corpus) are not "the reader" in the
sense this task means; `watch_cycle.py` is just the hourly scheduler that runs `watcher.py` (surfaces
alerts, scores nothing) then `notify.py`.

**This D-5 exercise tests `src/reader.py` on the live (Feed) path**, since that's the one that
reads a bare headline into class/entity and (per the brief) date/confidence — even though, as
Finding F1 shows, date and confidence turn out not to exist in its output at all.

## 1. Method

- **Source of headlines**: `data/alert_queue.csv` (124 real captured alerts, GDELT + 4 RSS
  feeds, timestamped 2026-07-25 to 2026-07-28 — the only intake source with enough volume and a
  clean mix of geopolitical / market / noise items; `data/feed.json` only holds the single most
  recent day (2026-08-31) and didn't overlap with this sample; `data/event_candidates_*.csv` are
  pre-typed corpus candidates, not raw headlines, so were not used as the primary pool).
- I read all 124 rows and hand-classified each into one of three pools **by my own judgment of
  the headline text**, not by the CSV's own `heuristic_type` column (that column is itself a
  regex classifier and would contaminate the "human read"): 12 clearly-geopolitical-oil
  candidates, 12 ambiguous/market-only candidates, 14 noise/irrelevant candidates (row indices
  recorded in `/private/tmp/.../scratchpad/select.py` → renamed `bucket_select.py` after a
  stdlib name collision with Python's `select` module).
- **Seeded draw**: `random.seed(20260902)`, `random.sample(pool, 10)` per bucket, run once
  (`bucket_select.py`), giving the 30 rows below. Row indices are 0-based positions in
  `data/alert_queue.csv` as read at the start of this review.
- **Human read written first**: for each of the 30, I recorded class (from the same 7-value
  `VALID_TYPES` vocabulary the reader uses, or `None`/no-class), a primary entity, an inferred
  event date, and a real-shock judgment — all *before* running the reader (`human_reads.py`,
  committed verbatim to the scratchpad). One honesty caveat, stated once here rather than per row:
  for three Red Sea/Houthi headlines (rows 12, 25, 9) my read leaned on background knowledge of
  the mid-2026 Houthi Red Sea campaign visible elsewhere in the same alert batch — a human reading
  *only* that one isolated headline, with no other context, might land on the same class the reader
  did. I flag this rather than silently count it as a reader error.
- **Reader run**: `RIPPLE_READER=off` forced for every call. Reason, stated per the task's own
  instruction: the `claude` CLI *is* present on this machine (`which claude` →
  `/Users/default/.npm-global/bin/claude`), but invoking it would (a) place a real, metered call
  through Joe's subscription for a read-only review task, and (b) on any live LLM hit,
  `reader.py`'s own code path unconditionally writes the proposal to
  `data/reader/cache/*.json` (`_cache_put`, called after every successful live call regardless of
  the `use_cache` flag) — which the task explicitly forbids. `RIPPLE_READER=off` makes
  `reader._cli()` return `None`, so every one of the 30 calls fell through to
  `_fallback_story`/the regex path inside `read_headlines` (`src/reader.py:283-284`,
  `:562-573`), and no proposal was ever cached — confirmed by `git status --porcelain data/`
  showing no new files under `data/reader/`. **The fallback is what is being tested here**, exactly
  as the task anticipated. `data/feed.json` (built on a different day, under a live LLM run —
  `"reader": {"llm": 123}` in its `counts` block) is separate, pre-existing evidence of the live
  mode's behavior on other headlines, not evidence I produced.
- Reader was called through `reader.read_headlines()` (the batch entrypoint `feed_build.py`
  itself uses) with a read-only sqlite URI connection to `data/oil.db`
  (`file:...?mode=ro`) so the vocabulary lookup could not write anything either.

## 2. The 30-row table

Class vocabulary: `chokepoint_disruption / conflict_escalation / demand_shock /
infrastructure_attack / opec_decision / policy_response / sanctions / None`. "Date" is reported
`N/A` for the reader column across all 30 rows — see Finding F1: **the field does not exist in
`reader.py`'s output at all**, so there is nothing to disagree about, and the reported 0% below is
structural, not 30 accumulated errors. Same for "confidence."

| # | headline (verbatim) | source (row in alert_queue.csv) | my class | reader class | my entity | reader entities | my date | reader date | class agree | entity agree | note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GEO-1 | Iran-backed Houthis claim missile attack on Saudi Arabia | rss:bbc_world (9) | conflict_escalation | infrastructure_attack | Yemen(Houthi)→Saudi Arabia | country.iran, country.saudi_arabia (role=mention) | 2026-07-25 | N/A | ✗ | ✓(SAU) | genuinely hard case (see caveat); reader also missed Yemen as actor |
| GEO-2 | World chess chief faces endgame after EU announces Russia war sanctions | rss:bbc_world (11) | sanctions | sanctions | Russia | country.russia | 2026-07-25 | N/A | ✓ | ✓ | noise-flavored headline (chess story) correctly typed on the subordinate clause |
| GEO-3 | Houthi attacks raise fears of wider Middle East conflict and more global economic damage | rss:bbc_world (12) | chokepoint_disruption | infrastructure_attack | Yemen (Red Sea) | (none) | 2026-07-25 | N/A | ✗ | ✗ (no entity extracted at all) | "attacks" keyword fires infrastructure_attack before any chokepoint cue; no country/chokepoint token matched in this sentence |
| GEO-4 | Middle East: UN warns against wider escalation after Houthi attacks in the Red Sea | rss:un_news (25) | chokepoint_disruption | infrastructure_attack | Yemen / Bab el Mandeb | (none) | 2026-07-25 | N/A | ✗ | ✗ | "Red Sea" is not in the chokepoint regex (only "hormuz"/"suez"/"bab el mandeb"/"strait"/"canal"/"pipeline"/"blockad*"/"transit*"); "attacks" wins by priority order |
| GEO-5 | Stranded seafarers remain trapped as Hormuz shipping stalls | rss:un_news (28) | chokepoint_disruption | chokepoint_disruption | Hormuz | chokepoint.hormuz | 2026-07-25 | N/A | ✓ | ✓ | clean hit |
| GEO-6 | Petroleum markets responded to disruptions in the Middle East in the second quarter | rss:eia_energy (37) | None (recap article) | None | — | (none) | 2026-07-25 | N/A | ✓ | ✓ | reader correctly nulls a retrospective analysis piece |
| GEO-7 | [GDELT] US OFFICIAL / IRAN: fight/clash signal | gdelt (55) | conflict_escalation (thin) | conflict_escalation | Iran / USA | country.iran | 2026-07-25 | N/A | ✓ | ✓(IRN); missed USA | bare GDELT event-code label, not real prose; "USA" is deliberately excluded from the watcher's own actor net (per `watcher.py`'s comment) but that's a watcher-side design choice, unrelated to why the reader didn't extract it here (the label just doesn't say "USA" as a word) |
| GEO-8 | Why a new war in Yemen could be different for the Houthis | rss:aljazeera (72) | None (opinion/analysis) | conflict_escalation | Yemen | country.yemen | 2026-07-27 | N/A | ✗ | ✓ | "war" fires conflict_escalation on a hypothetical-framed opinion piece ("could be different") |
| GEO-9 | Saudi Arabia defends against drone strikes from 'Iran-backed' groups | rss:aljazeera (83) | infrastructure_attack | infrastructure_attack | Iran(-backed)→Saudi Arabia | country.iran, country.saudi_arabia | 2026-07-27 | N/A | ✓ | ✓ | clean hit |
| GEO-10 | Houthis want to copy Iran's Hormuz control in the Red Sea: Yemeni FM | rss:aljazeera (104) | chokepoint_disruption | chokepoint_disruption | Yemen/Iran, Hormuz (comparison) | chokepoint.hormuz, country.iran | 2026-07-28 | N/A | ✓ | ✓; missed Yemen | reads as a stated aspiration/threat, not an actual disruption — reader has no way to distinguish that from an actual one (see F-Big-Moves discussion, N/A here since it never reaches corpus) |
| AMB-1 | Commercial crude oil inventories increased by 2.0 million barrels | rss:eia_energy (35) | None | None | USA (implied) | commodity.crude_oil | 2026-07-25 | N/A | ✓ | ~ (commodity, not country — no country named in text, so arguably correct) | routine data release correctly nulled |
| AMB-2 | What are tank bottoms? | rss:eia_energy (36) | None | None | — | (none) | n/a | N/A | ✓ | ✓ | explainer correctly nulled |
| AMB-3 | Global liquefied natural gas trade volumes reached record high in 2025 | rss:eia_energy (38) | None | None | — | commodity.natgas | n/a | N/A | ✓ | ~ | correctly nulled; commodity token picked up, no false class |
| AMB-4 | The United States produced more crude oil than any other country in 2025 | rss:eia_energy (39) | None | None | USA | commodity.crude_oil | n/a | N/A | ✓ | ✗ | **entity-extraction gap**: "United States" spelled out is never matched — `country.usa`'s stored name is `"Usa"` and the regex fallback only matches the literal token `usa`/`Usa`, not `united states` |
| AMB-5 | U.S. commercial crude oil inventories have decreased in June | rss:eia_energy (44) | None | None | USA (implied) | commodity.crude_oil | 2026-07-25 (June data) | N/A | ✓ | ~ | correctly nulled |
| AMB-6 | UAE's exit from OPEC+ reduced the group's share of crude oil production and capacity | rss:eia_energy (45) | opec_decision (marginal) | opec_decision | UAE / OPEC | commodity.crude_oil, country.uae, institution.opec | unknown (retrospective) | N/A | ✓ | ✓ | correct class, but is this the *decision itself* or an EIA recap of an old decision? headline alone can't say — the reader has no way to tell either, and would treat both the same |
| AMB-7 | Permian natural gas production increased faster than crude oil | rss:eia_energy (46) | None | None | USA (implied) | commodity.crude_oil, commodity.natgas | n/a | N/A | ✓ | ~ | correctly nulled |
| AMB-8 | U.S. jet fuel production rises after prices doubled in March | rss:eia_energy (48) | None | None | USA (implied) | (none) | 2026-07-25 (refs March) | N/A | ✓ | ✓ | correctly nulled; refers to a March move without saying what caused it — a genuine "which event?" gap that's on the source, not the reader |
| AMB-9 | California natural gas prices reach historic lows in early 2026 | rss:eia_energy (51) | None | None | USA/California (implied) | commodity.natgas | early 2026 | N/A | ✓ | ~ | correctly nulled |
| AMB-10 | Oil price dives as US and Iran pause attacks | rss:bbc_world (63) | None (de-escalation; no class fits) | infrastructure_attack | Iran / USA | country.iran | 2026-07-27 | N/A | ✗ | ✓(IRN) | **class-confusion failure mode**: the word "attacks" inside "**pause** attacks" (a ceasefire, i.e. de-escalation) fires `infrastructure_attack` — the regex has no negation/direction awareness at all |
| NOISE-1 | Families still search for bodies a month after Venezuela earthquakes | rss:bbc_world (14) | None | None | Venezuela | country.venezuela | ~late June 2026 (quake, not article date) | N/A | ✓ | ✓ | correctly nulled; illustrates publish-date-vs-event-date gap even though class is right |
| NOISE-2 | Born too soon: Premature babies fight for survival in Gaza | rss:aljazeera (17) | None | None | — | (none) | n/a | N/A | ✓ | ✓ | correctly nulled |
| NOISE-3 | Venezuelans hold vigil one month after devastating earthquakes | rss:aljazeera (19) | None | None | Venezuela | (none) | ~late June 2026 | N/A | ✓ | ✗ | Venezuela not extracted (name not repeated in this headline's exact wording) |
| NOISE-4 | 'Women do not stop giving birth in an emergency' – one month after Venezuela quakes | rss:un_news (23) | None | None | Venezuela | country.venezuela | ~late June 2026 | N/A | ✓ | ✓ | correctly nulled |
| NOISE-5 | Zelensky visit sends clear message of support for Ukraine, Burnham says | rss:bbc_world (65) | None | None | Ukraine | country.ukraine | 2026-07-27 | N/A | ✓ | ✓ | correctly nulled |
| NOISE-6 | New UK PM Burnham assures Zelenskyy of continuing Ukraine support | rss:aljazeera (66) | None | None | Ukraine | country.ukraine | 2026-07-27 | N/A | ✓ | ✓ | correctly nulled |
| NOISE-7 | What drove Venezuela's decision to leave the ICC? | rss:aljazeera (68) | None | None | Venezuela | country.venezuela | 2026-07-27 | N/A | ✓ | ✓ | correctly nulled |
| NOISE-8 | Gaza student tops national exams despite war and displacement | rss:aljazeera (75) | None | **conflict_escalation** | — | (none) | n/a | N/A | ✗ | ✓ (both empty) | **irrelevant headline classified as a shock**: "war" inside "despite war and displacement" fires `conflict_escalation` on a pure human-interest story; zero entities extracted, so `feed_build.py`'s own `qualifying_entities` check would demote this from MATERIAL to IN_LINE — but the *class* is still wrong and would display as "conflict_escalation" on the Feed |
| NOISE-9 | Why have US-Lebanon direct flights been banned for 40 years? | rss:aljazeera (97) | None | None | Lebanon | country.lebanon | n/a (40-yr-old policy) | N/A | ✓ | ✓ | correctly nulled |
| NOISE-10 | Why London's Hackney Council wants to repeal its 'twin' status with Haifa | rss:aljazeera (118) | None | None | Israel (loosely) | (none) | 2026-07-28 | N/A | ✓ | ✗ | correctly nulled; Haifa not in the entity vocab, so no entity — matches my read only loosely |

## 3. Agreement numbers (executed)

Computed in `/private/tmp/.../scratchpad/compare.py` over the 30 rows above:

- **Class agreement: 24/30 = 80%** (GEO 6/10, AMB 9/10, NOISE 9/10)
- **Entity agreement (loose — any of my named entity ids appears in the reader's list, or both
  empty): 19/30 = 63%** (GEO 8/10, AMB 3/10, NOISE 8/10)
- **Date agreement: 0/30 = 0%, but this is a structural fact, not 30 independent misses** —
  `reader.py` never emits a date field, on either the LLM or the regex-fallback path (confirmed by
  reading `STORY_SCHEMA`, `BATCH_SCHEMA`, `cage()`, and every dict literal returned by
  `read_story`/`read_headlines`, `src/reader.py:228-256, 493-585`). See Finding F1.
- **Confidence: not applicable — the field doesn't exist in `reader.py`'s schema at all** (unlike
  the separate `extract_events.py` cage, which does have `confidence_suggestion`). Every row above
  is `regex_fallback` (confirmed per-row from `reader['mode']`), which is the intended condition
  for this run.
- Per-bucket read: the AMB bucket's low entity score (3/10) is mostly an artifact of my scoring
  rule treating "USA (implied)" as a miss when the reader instead (correctly) extracted a
  commodity id from text that never names a country — arguably the reader is *right* on several of
  those, not wrong; see the "~" notes in the table. The GEO bucket's low class score (6/10) is the
  real signal: **4 of 10 clearly-geopolitical, oil-relevant headlines got a class disagreement**,
  three of them a specific, repeatable pattern (see §4).

## 4. Disagreements, verbatim, with failure-mode characterization

All from the table above; reproduced here with both reads side by side.

1. **"Houthi attacks raise fears of wider Middle East conflict and more global economic damage"**
   (rss:bbc_world, row 12) — my read: `chokepoint_disruption`. Reader: `infrastructure_attack`,
   zero entities. *Failure mode: class confusion, chokepoint vs infrastructure_attack* — the
   chokepoint regex only fires on the literal tokens `strait/canal/chokepoint/blockad*/transit*/
   hormuz/suez/bab el mandeb/pipeline/reroute*`; "Red Sea," "Middle East conflict" and "economic
   damage" don't match, so the generic `attacks` token in `infrastructure_attack`'s pattern wins by
   priority order. Also zero entities extracted, so no country/chokepoint token survives at all.

2. **"Middle East: UN warns against wider escalation after Houthi attacks in the Red Sea"**
   (rss:un_news, row 25) — my read: `chokepoint_disruption`. Reader: `infrastructure_attack`, zero
   entities. Same failure mode as #1 — "Red Sea" isn't in the chokepoint vocabulary; "attacks"
   fires the wrong bucket first.

3. **"Oil price dives as US and Iran pause attacks"** (rss:bbc_world, row 63) — my read: no class
   fits cleanly (this is a *de-escalation* headline — a ceasefire pause — and the 7-value codebook
   has no "de-escalation" class). Reader: `infrastructure_attack`, entity `country.iran`.
   *Failure mode: class confusion driven by keyword polarity-blindness* — the regex has no
   negation handling, so "**pause** attacks" (attacks stopping) is scored identically to "launch
   attacks" (attacks happening). This is the sharpest finding in the sample: a *de-escalatory*
   headline is read as an *escalatory infrastructure-attack* signal.

4. **"Why a new war in Yemen could be different for the Houthis"** (rss:aljazeera, row 72) —
   my read: `None` (an opinion/analysis piece, hypothetically framed — "could be"). Reader:
   `conflict_escalation`, entity `country.yemen`. *Failure mode: opinion/analysis piece admitted
   as a shock* — "war" fires the class regex regardless of the hypothetical framing around it; the
   system prompt for the LLM path explicitly instructs "use null ... commentary," but the regex
   fallback (what's actually running here, and per the docstring what runs whenever the CLI is
   off/unavailable) has no equivalent discipline.

5. **"Gaza student tops national exams despite war and displacement"** (rss:aljazeera, row 75) —
   my read: `None` (pure human-interest, no oil/market relevance). Reader: `conflict_escalation`,
   zero entities. *Failure mode: irrelevant headline admitted as a shock* — same "war" keyword
   trigger as #4, on a story with no geopolitical-actor content whatsoever. Because zero entities
   are extracted, `feed_build.py`'s own gate (`if sig == "MATERIAL" and not
   qualifying_entities: sig = "IN_LINE"`) would catch this specific case before it could display as
   MATERIAL on the Feed — but the wrong *class label* (`conflict_escalation`) still reaches the
   page and is shown next to the headline regardless of significance tier.

6. **"Iran-backed Houthis claim missile attack on Saudi Arabia"** (rss:bbc_world, row 9) — my
   read: `conflict_escalation`, actor Yemen/Houthi. Reader: `infrastructure_attack`, entities
   `country.iran`, `country.saudi_arabia` (missed Yemen entirely — "Houthis" isn't in the entity
   vocab as a standalone token, only `country.yemen` is, and the regex requires the country name or
   its id-tail, not a proxy-group name). *Failure mode: wrong/missing actor* — the country actually
   doing the striking (Yemen, via the Houthis) never enters the entity list; only the two countries
   whose *names* are literally present (Iran as backer, Saudi Arabia as target) do. This is a
   real "wrong actor from a mentioned third party" case, just inverted from the classic pattern:
   here the *true* actor is dropped, not a *bystander* wrongly promoted to actor.

No "date = publish date vs event date" disagreement could be tabulated in the strict sense
because the reader has no date field to disagree with — see Finding F1. The closest analogue in
the sample is the three Venezuela-earthquake follow-ups (NOISE-1/3/4), where the true event
(the earthquake) was roughly a month before the article's own timestamp; had the reader (or
`promote_alert.py`, downstream) used the alert's capture date as "the" event date, it would be off
by ~30 days. `promote_alert.py` does exactly this by design, labelled honestly (`# Event date
defaults to the alert's date -- Joe must confirm the real event date`, `src/promote_alert.py:56`).

## 5. Where the reader's output feeds anything published

- **`reader.py` → `feed_build.py` → `data/feed.json` → the Feed page (`./go` → `/app`), ungated.**
  `src/feed_build.py:117` calls `R.read_headlines(...)` on every fresh headline in
  `alert_queue.csv` with **no human step in between** — the caged read's `event_class`,
  `significance` (via `materiality.gate`), and ranking go straight into `feed.json` and onto the
  page. This never writes to `events.csv` / the corpus, so it does not, on its own, violate
  `SESSION_CHARTER.md` §2 rule 3 ("Nothing enters `events` without Joe") or the matching README
  sentence ("Nothing enters the corpus without a human"). But it *does* mean every misclassification
  found in §4 (e.g. row 75, row 63) is visible to Joe on the live Feed, unreviewed, before any human
  step — the Feed's own footer text calls this "gated," which is accurate only in the sense of the
  *materiality* gate (a ratio threshold), not a *human* gate. See Finding F2.

- **Corpus admission (`events.csv`) never goes through `reader.py`.** `promote_alert.py` (Joe's
  one deliberate step from alert → candidate) uses the alert's own `heuristic_type` (the *regex*
  classifier baked into `watcher.py`, not `reader.py`) as an unconfirmed suggestion, and explicitly
  labels the candidate `UNVERIFIED — Joe must confirm the event, its real date, and code
  severity/surprise before this can be approved` (`src/promote_alert.py:63-64`); `joe_decision`
  starts blank. The separate `extract_events.py` cage (a different worker) also never writes
  `events.csv` directly — clean proposals land in `data/candidate_events.csv` only, and the
  docstring states "Canon is only ever written later by `apply_review.py` + `load_events.py`."

- **`src/admit_events.py` sets `joe_decision = "approve"` in code, with no human in the loop, for
  a specific auto-admit tier** (`src/admit_events.py:91`, inside `run()`: `if tier ==
  "AUTO_ADMIT": ... r["joe_decision"] = "approve"`). The gate for that tier (`P_AUTO=0.90,
  N_AUTO=3`, exact source-URL match against a deterministic corroboration log) is itself
  deterministic and doesn't touch `reader.py` or an LLM's own confidence number — but it is a
  **programmatic write of the literal field that means "Joe decided,"** without Joe deciding. This
  is a genuine, if narrow, exception to both `SESSION_CHARTER.md` §2 rule 3 and the README's
  "Nothing enters the corpus without a human" sentence. It only applies to `candidate_source ==
  'llm_extract'` rows (the `extract_events.py` path), not to anything from `reader.py` or the
  Feed/watcher — worth stating precisely so it isn't overstated as "the reader bypasses the gate,"
  which it does not; a *different, related* LLM pipeline's admission tier does.

- **Big Moves attribution is clean.** `src/big_moves.py` never imports `reader` (confirmed:
  `grep -n "reader\|import R\b" src/big_moves.py src/big_moves_page.py` returns nothing) and
  builds attribution purely from `SELECT event_id, event_date, type, title FROM events`
  (`src/big_moves.py:141`) — i.e., only the human-gated corpus, using its Joe-confirmed
  `event_date`, never a reader-inferred class or date, and never anything from the Feed. The
  README's claim "each attributed to what was knowable while it moved" is not contaminated by
  the reader or by hindsight, as far as this file goes. This is the one place the task singled out
  as a risk, and it checks out clean.

## 6. FINDINGS, ranked by whether they change a published README sentence

**F1 — HIGH. Changes: "Feed (market state, gated stream)" (README "What it is").**
`src/reader.py` — on both the live LLM path and the regex fallback — never extracts or assigns an
event date, and never produces a confidence score. This is not a bug surfaced by this sample; it's
visible directly in the schema (`STORY_SCHEMA`/`BATCH_SCHEMA`, `src/reader.py:228-256`) and in
every returned dict (`cage()` at `:422-456`, `read_story`/`read_headlines` at `:493-585`). Every
downstream date associated with a headline (in `alert_queue.csv`, `feed.json`, or a
`promote_alert.py`-created candidate) is the **capture/publish timestamp**, never an inferred
event date — and that's honestly labelled where it matters (`promote_alert.py`'s explicit "Joe
must confirm the real event date"). But nothing in the reader itself, or in `feed_build.py`, flags
publish-date-vs-event-date drift to the reader; the three Venezuela-earthquake headlines in this
sample (§4, NOISE-1/3/4) show the gap can be ~30 days. The word "gated" in "Feed (market state,
gated stream)" is technically accurate (the materiality ratio gate) but reads, to someone who
hasn't opened `feed_build.py`, like a human-reviewed stream; it is not — see F2.

**F2 — HIGH. Changes: "Nothing enters the corpus without a human" (README "The integrity record")
and `SESSION_CHARTER.md` §2 rule 3 ("Nothing enters `events` without Joe").**
This is true of `reader.py`'s own path (the Feed never writes to `events.csv`) but **false for a
specific tier of the separate `extract_events.py`/`admit_events.py` pipeline**:
`src/admit_events.py:91` sets `joe_decision = "approve"` by code when a candidate's recommendation
is `keep`, its source URL exactly matches a corroboration-log entry, confidence ≥ 0.90 and
n_independent ≥ 3 — with no human step. `apply_review.py` + `load_events.py` will then admit that
row to `events.csv` reading `joe_decision == 'approve'`, unable to distinguish it from a row Joe
actually approved. The severity/surprise values are honestly labelled "provisional," and a human
*can* veto before the next `apply_review.py` run — but as written, the literal claim "nothing
enters the corpus without a human" is falsifiable by this code path today. Not a `reader.py`
finding as such, but it is exactly the "does a reader-classified headline ever enter `events`
without a human" check the task asked for, and the answer for this adjacent pipeline is: yes, under
a specific, narrow, disclosed-in-code condition.

**F3 — MEDIUM. Does not (yet) change a README sentence, but is upstream of what the Feed and Story
pages show.** In this sample, the regex fallback shows a repeatable class-confusion pattern: the
bare token "attack(s)" in `infrastructure_attack`'s regex outranks the Red-Sea-specific language
that should route to `chokepoint_disruption` (§4 #1, #2), and has no polarity/negation awareness,
so a **de-escalation headline ("pause attacks") reads as an escalatory infrastructure-attack
signal** (§4 #3) and **"war" alone, even inside human-interest or hypothetical-framed copy, fires
`conflict_escalation`** (§4 #4, #5) with no entities to anchor it. 2 of 10 noise-bucket headlines
and 2 of 10 ambiguous-bucket headlines got a non-null class from a bare keyword hit on prose that
described the *absence* or *irrelevance* of a shock. The materiality gate's `qualifying_entities`
check (`feed_build.py`, demoting MATERIAL→IN_LINE when no entity is present) catches the
zero-entity cases from displaying as MATERIAL, but the wrong *class label* still reaches the page
regardless of significance tier, and would not be caught at all if any entity happened to co-occur
in the same headline by chance.

**F4 — LOW/informational. No README sentence affected directly.** Entity extraction in the regex
fallback matches only literal name/id-tail tokens from the `entities` table — it misses "United
States" (only matches literal `USA`/`Usa`) and drops proxy-actor names like "Houthis" that aren't
themselves entity-table rows (only the country `country.yemen` is). This under-counts qualifying
entities more than it over-counts them, which — given the materiality gate's fail-*safe* direction
(no entity → can't be MATERIAL) — biases the regex fallback toward under- rather than
over-promoting stories, a mitigating detail worth stating alongside F3 rather than compounding it.

## What I did not do

- Did not invoke the live `claude` CLI reader path (see §1's rationale — cost/consent and the
  unconditional cache-write behavior on a live hit, both out of scope for a read-only review).
  `data/feed.json`'s pre-existing `"reader": {"llm": 123}` counts are the only live-mode evidence
  cited, and I did not generate them.
- Did not read `ops/reader_agent.md` or `ops/extract_agent.md` (the system-prompt files that would
  govern the live LLM path in more depth) — the in-code `system_prompt()` function in `reader.py`
  was read directly instead, which is what actually executes.
- Did not exhaustively audit every caller of `reader.py` (e.g. `terminal_api.py`, `mcp_server.py`)
  for other places a reader-classified item might reach a surface; `story_read.py` and
  `feed_build.py` were confirmed as the two live-path callers via `grep -rn "import reader\|from
  reader"`, and those are the ones with any plausible path toward "published."
- Did not modify, promote, or write anything to `data/` at any point; all outputs are in this
  scratchpad directory.
