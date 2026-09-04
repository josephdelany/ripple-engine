> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-4 — Blind re-derivation of 20 IES-90 rows

Repo: `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`, branch `v2-day1`, HEAD `b7c8ec1`.
Read-only throughout. No file under the repo was written. All scratch work is in
`/private/tmp/claude-502/-Users-default-PERSONAL-OS-V2/33693732-1ed6-49a9-aa2e-892d7ee3ffcf/scratchpad/d4work/`
(`derive.py`, `my_derivation.json`, `engine20.json`, `sample20.json`, `ni_lv_samples.json`).

**Environment note, not a repo finding:** the shared scratchpad directory this task was told to use
already contained scratch files from what look like other concurrent audit tasks on the same repo
(`bucket_select.py`, `d3_analysis.py`, `D1_registration_audit.md`, etc.), including a stale
`__pycache__/select.cpython-314.pyc` that shadowed the stdlib `select` module and crashed the first
`pandas` import. Worked around by running from a fresh `d4work/` subdirectory; nothing in that
directory or its contents was read, altered, or relied on.

## 1. Method — what was read, and when

**Before deriving my own labels (blind):**
- `OUTCOME_MAPPING.md` in full, §1–§6 plus Amendments 1, 1.1, 2 — the registered IES-90 rules.
- `src/state/ies90.py` lines 1–228 and 407–423 only: module docstring, constants (`SEED`, `WINDOW`,
  `COVER` date ranges, `HOSTLEV_TO_LEVEL`, `VIOL_TO_LEVEL`, `GED_WAR`/`GED_FORCE` — all identical to
  the numbers already published in the .md, no new information), the `LITTORAL` and `GED_NAMES`
  entity maps, and the pure loaders (`load_midi`, `dedupe_mid`, `load_war`, `load_ged`, `ged_sum`,
  `load_sources`). **Not read:** `score_midi`, `score_war`, `score_mid`, `score_icb`, `score_ged`,
  `score_event`, the body of `run()` beyond the `load_sources()` call, `distribution()`, `audit_pick()`,
  `write_audit()`, `main()` — i.e. every function that actually assigns a level.
- `src/state/outcomes.py` (a different module, the retired §1–§6 `sr_outcome_90` scale, not IES-90)
  lines 1–53 (schema, docstring) and 93–192: `cohen_kappa`, `_corpus`, `load_icb`, `load_mid`,
  `load_ucdp` (raw-file paths and column layout), and, going a little further than strictly
  necessary, `_actors_and_pairs`, `match_icb`, `match_mid` — the retired scale's A/P construction and
  crisis/dispute matching. This is disclosed as scope creep beyond "entity/country mapping": it is
  the retired scale's matching logic, not IES-90's, and OUTCOME_MAPPING.md §2 already states the same
  A/P/L construction in prose, so nothing about IES-90's *level* assignment was learned from it — but
  it is where the A/P/L construction actually used below (§2) came from operationally, so it is named
  here rather than left implicit. **Not read:** `map_icb`, `map_mid`, `map_ucdp`, `match_ucdp`, `run()`,
  `kappa_report()`, `audit_sheet()`, `write_audit()`, `main()`.
- `src/state/icb.py`: grepped function names and the `crises()`/`fetch()` file paths only, not `parse()`.
- `src/state/countries.py` in full (the ccode/ISO3 map — pure data, not logic) and `data/oil.db`'s
  schema (`events`, `event_outcomes`, `event_entities`) via `sqlite3 ... .schema`.
- All raw source files directly: `data/state/raw/icb/{icb1v16,icb2v16,icb_dyads_v16}.csv`,
  `data/state/raw/cow_mid/{dyadic_mid_4.03.csv, MID-5-....zip}`, `data/state/raw/cow_war/{Inter,Intra}-StateWarData*.csv`,
  `data/state/raw/ucdp/UcdpPrioConflict_v26_1.csv`, `data/cache/ucdp_ged_26.1.json` — headers/columns
  only until the independent scorer (below) was written.

**After deriving (step 3 boundary crossed here):** `event_outcomes` rows with `source='ies90'` for the
20 sampled events, then `src/state/ies90.py`'s scoring functions (`score_icb`, `score_mid`, `score_midi`,
`score_war`, `score_ged`, `score_event`, `run`) to understand any disagreement.

## 2. The 20-row sample

`event_outcomes` rows with `source='ies90', field='level'` (184 total, i.e. every geopolitical-type
event that has an IES-90 label at all) were listed ordered by `event_id`; `random.Random(20260902).sample(ids, 20)`
drew the 20 below. For each, `A` (mapped `country.*` entities: `sr_actor`/`sr_target` plus every coded
`event_entities` country entity), `P` (actor–target pairs; all pairs of `A` if roles are ambiguous) and
`L` (location/target-role entities, else `A`, plus the A2.2 littoral map for chokepoint entities) were
built by hand from `events` and `event_entities`, per OUTCOME_MAPPING.md §2/A1.2's prose definition —
**before** looking at any IES-90 level. I then wrote an independent scorer
(`d4work/derive.py`, ~230 lines) against the raw ICB/MID/MIDI/COW-War/GED files, applying Amendment
1 + 1.1 + 2 as written (dated wholly/onset/ongoing subcases for ICB and MID, war-spell overlap for COW
War, deaths-threshold for GED, dyadic-vs-location precedence, littoral map, tie order). Only after
recording all 20 independent levels did I read the engine's stored rows and its scoring code.

Two ambiguities I resolved by choice, flagged as findings in their own right (§6):
- **P/A construction for events with an ambiguous role** (e.g. `country.azerbaijan` coded role=`source`
  on `btc_pipeline_blast_2008`): I treated `source` as neither actor, target, nor location for pair
  purposes (only `actor`/`target`/`location` roles feed `P`), since the .md text names only those three.
- **What "level 0" should be called when a GED death count is 0**: A2.3 lists only `GED.location.ge250`
  and `GED.location.ge25` as GED rule ids; there is no listed id for "GED covered, found nothing." I
  invented `GED.location.lt25`; the engine instead folds every level-0 outcome (whichever source
  produced it) into the single generic `NONE.covered`, confirmed against its actual output. This did
  not change any of the 20 levels — only my rule-id label, corrected below.

| event | date | my level | engine level | agree | my basis | engine basis | rule fired (both) | note |
|---|---|---|---|---|---|---|---|---|
| kirkuk_ceyhan_isis_2014 | 2014-03-02 | 3 | 3 | Y | location | location | GED.location.ge250 | A empty (chokepoint-only coding); L={iraq,turkey} via littoral map |
| saudi_suspends_bab_el_mandeb_2018 | 2018-07-25 | 0 | 0 | Y | dyadic | dyadic | NONE.covered | ICB "HOUTHI REBELLION" ongoing at d → no level; dyadic precedence discards GED level 3 |
| me_midnight_hammer_2025 | 2025-06-22 | 2 | 2 | Y | location | location | GED.location.ge25 | only GED covers a 2025 date |
| chn_5minerals_2025 | 2025-02-04 | 0 | 0 | Y | location | location | NONE.covered | GED deaths=0 |
| sanc_2013_11_24 | 2013-11-24 | 2 | 2 | Y | location | location | MIDI.single.overlap | matched MIDI/MID incidents are Iran–Pakistan/Iran–Afghanistan border disputes, unrelated to the JPOA deal; see §6 |
| egypt_revolution_2011 | 2011-01-25 | 0 | 0 | Y | location | location | NONE.covered | no matching record in any source |
| russia_pricecap_enforce_2023 | 2023-11-16 | 2 | 2 | Y | location | location | GED.location.ge25 | |
| me_maersk_diversions_2023 | 2023-12-15 | 3 | 3 | Y | location | location | GED.location.ge250 | |
| btc_pipeline_blast_2008 | 2008-08-05 | 0 | 0 | Y | dyadic | dyadic | NONE.covered | dyadic precedence (P={azerbaijan,turkey}) discards a GED level-2 signal (240 deaths, Turkey — real but unrelated PKK-conflict violence); see §6 |
| shah_leaves_iran_1979 | 1979-01-16 | 3 | 3 | Y | location | location | WAR.intra.location | mixed war-spell status: "Overthrow of the Shah" ongoing at d, "Anti-Khomeini Coalition" onset in W |
| venezuela_blackout_2019 | 2019-03-07 | 0 | 0 | Y | location | location | NONE.covered | ICB "VENEZUELAN ELECTION" ongoing at d → no level |
| praying_mantis_1988 | 1988-04-18 | 2 | 2 | Y | dyadic | dyadic | MID.pair.wholly | dyadic MID (US–Iran, disno 2834) overrides a location-basis COW-intra war (level 3) and an ongoing, unrelated ICB Iraq–Iran crisis |
| us_chevron_venez_2025 | 2025-02-26 | 0 | 0 | Y | location | location | NONE.covered | |
| rus_druzhba_strike_2025a | 2025-08-18 | 2 | 2 | Y | location | location | GED.location.ge25 | corpus codes only `country.russia`; Ukraine (the actor) and Hungary/Slovakia (named in the title) are not coded entities on this event at all |
| ras_tanura_attack_2021 | 2021-03-07 | 0 | 0 | Y | dyadic | dyadic | NONE.covered | GED deaths=0 (only tov=1 state-based counted; a plausibly-intercepted Houthi strike) |
| qatar_gulf_blockade_2017 | 2017-06-05 | 0 | 0 | Y | location | location | NONE.covered | corpus codes only Qatar as target; the blockading states are not coded, so no dyadic pair is even possible |
| libya_jathran_blockade_2013 | 2013-08-01 | 0 | 0 | Y | location | location | NONE.covered | A empty; L={libya} via littoral map |
| russia_sectoral_sanctions_2014 | 2014-07-16 | 2 | 2 | Y | location | location | MIDI.single.overlap (+GED tied at 2) | engine reports a genuine MIDI/GED tie (`level_source=midi,ged`); my scorer's tie-break only surfaced one — a limitation of my code, not a level disagreement |
| iran_revolution_1979 | 1979-02-11 | 3 | 3 | Y | location | location | WAR.intra.location | |
| rosneft_trading_venez_2020 | 2020-02-18 | 0 | 0 | Y | location | location | NONE.covered | |

## 3. Agreement

**Raw agreement: 20/20 = 100%.** Cohen's unweighted κ over {0,1,2,3}, executed in `python3`
(`cohen_kappa` per the formula I'd already read in `outcomes.py`): **κ = 1.0** (p_o = 1.0, p_e = 0.38).
Confusion matrix (rows = mine, cols = engine):

| | eng 0 | eng 1 | eng 2 | eng 3 |
|---|---|---|---|---|
| **mine 0** | 10 | 0 | 0 | 0 |
| **mine 1** | 0 | 0 | 0 | 0 |
| **mine 2** | 0 | 0 | 6 | 0 |
| **mine 3** | 0 | 0 | 0 | 4 |

No level-1 event landed in this draw (population-wide there are only 6 of 184 — expected ≈0.65 in a
20-draw without replacement, so a zero is unsurprising, not a gap in the check).

`deal` was checked too, after first discovering a real bug in my own scorer: I had required an actual
matched crisis/dispute record before defaulting `deal=0`, but the registered rule is "0 if ICB or MID
*covers* W" — where "covers" (per A1.2's own preamble, which I had read but under-weighted) means the
date window and ≥1 mapped country, independent of whether a record was found. Corrected, my `deal`
matched the engine's stored value on all 20 (10 events with `deal=0`, 10 with `deal=null` because
neither ICB nor MID's coverage window reaches the event's date — this correction is disclosed as
informed by the comparison, not blind).

**Verdict on implementation fidelity:** on this sample, `ies90.py`'s code implements the rules
registered in OUTCOME_MAPPING.md Amendment 1+1.1+2 correctly, including the subtle ones (ongoing-crisis
suppression, dyadic-precedence overriding a stronger location signal, tie handling). That is a real,
executed check, not a re-statement of the .md text.

## 4. Absence of evidence vs. recorded zero

DB-wide there are only **3** `no_independent_outcome=1` rows (not 76 level-0 rows to choose 3 of — all
3 were used) and I drew 3 of the 76 level-0 rows with the same seed.

| event | date | `no_independent_outcome` | `covering` | `rule_fired` | reading |
|---|---|---|---|---|---|
| iran_israel_us_strike_2026 | 2026-02-28 | 1 | (none) | UNCOVERED | genuinely no source's date window reaches this event — ICB ends 2021, MID/MIDI end 2014, GED ends 2025-12-31, a 2026 event's window can't fit inside any of them |
| rus_novorossiysk_terminal_2025 | 2025-11-14 | 1 | (none) | UNCOVERED | window (d,d+90] runs into 2026-02, past GED's 2025-12-31 ceiling |
| hormuz_closure_2026 | 2026-03-04 | 1 | (none) | UNCOVERED | same |
| kazakhstan_unrest_2022 | 2022-01-05 | 0 (level=0) | ged | NONE.covered | GED covered and recorded 0 state-based deaths in Kazakhstan in the window — a real "checked, nothing found" |
| nigeria_warri_shutin_2003 | 2003-03-23 | 0 (level=0) | midi,war,icb,mid,ged | NONE.covered | GED covered; `deaths_ged_90=0` but `deaths_ged_other_90=152` (one-sided/non-state violence, excluded from the level by design, per A1.2) |

**The mapping does what it claims here**: `no_independent_outcome` (nothing covers) and level 0
(something covered, recorded nothing that counts) are stored and labeled distinctly, and the
distinction held up on inspection. The Nigeria case is a genuine, disclosed cost of the "state-based
deaths only" restriction (152 non-state deaths sit right beside a level=0 "none" label) — not a defect
in the code, but a substantive limitation worth restating to a reader who sees "level 0" and assumes
"no violence."

## 5. The ongoing-war question (executed, on all 184 labelled events)

Amendment 1.1 explicitly re-dated ICB and MID so a crisis/dispute merely *ongoing at d* asserts no
level (fixing "the whole-episode defect"). **It did not extend the same fix to COW War or to GED** — and
those two sources are the *only* two that ever produce a level-3 ("war") label in this corpus:

```
level=3 rows (n=54) by level_source:  ged 38 | war 15 | midi,war 1
```

Zero of the 54 level-3 rows come from ICB's dated-onset rule or MID's dated-onset rule (both of which
*can* reach 3, per the mapping table, but evidently never do in this corpus at the war tier). So the
"dated, not whole-episode" fix the mapping's own Amendment 1.1 was written to deliver does not reach
the top of the scale at all.

**COW War (16 rows carry a matched war spell; 15 pure-war + 1 tied with MIDI):**
- 12 rows: every matched war spell **started at or before d** — i.e. the war was already ongoing when
  the oil-shock event happened; the level-3 label is a fact about the calendar, not about this event.
  (`bridgeton_mine_strike_1987`, `earnest_will_1987`, `iran_iraq_war_1980`, `iran_oilworkers_strike_1978`,
  `iraq_invades_kuwait_1990`, and 7 more.)
- 2 rows: the matched spell **started within (d, d+90]** — a genuine dated onset
  (`september_11_attacks_2001`, and one leg of `iran_revolution_1979`'s two war matches).
- 2 mixed (`desert_storm_air_campaign_1991`, `shah_leaves_iran_1979`): at least one matched spell
  ongoing, at least one onset.

**GED (38 rows, deaths-in-window ≥ 250):** using the mapping's own stored-but-unused field
`deaths_ged_pre90` (deaths in the *prior* 90 days), **31 of 38** already had ≥250 deaths in the 90 days
*before* d too — the country was already at the war-intensity threshold before the event, e.g.
Russia–Ukraine (39,985 in-window vs 20,473 pre-window), Israel–Gaza (24,670 vs 3,835), the 2024/2025
Russia refinery-strike series (thousands both sides). Only 7 GED-driven rows show a level that looks
like a fresh spike (`deaths_ged_pre90` under 250): `libya_civil_war_2011`, `red_sea_attacks_2023`,
`libya_haftar_blockade_2020`, `iraq_ofp_exports_begin_1996`, `israel_iran_war_2025` (below threshold
pre-window despite being war-adjacent), `rus_novorossiysk_depots_2024`, `rus_tuapse_strike_2024b`.

**Combined: ~43 of 54 (≈80%) of level-3 "war" labels are attributable to a war or conflict that
predates the specific oil-shock event, continuing through its 90-day window, rather than to escalation
caused by or immediately following that event.** Only ~11 of 54 (≈20%) look like a dated, event-linked
war onset. Answering the task's direct question: yes — for the war tier, "ongoing → level 3" is exactly
what the registered rule does (COW War: "a war spell overlapping W gives level 3," no ongoing
carve-out; GED: a raw threshold with no ongoing carve-out at all), and the executed data confirm the
consequence the task worried about: **the level-3 label is substantially a function of when the event
happened to fall relative to a pre-existing war, not of what the event was.** That inflates the base
rate of "war" outcomes for oil-shock events that simply occur during active wars (Yemen, Russia–Ukraine,
Gaza, Sudan, Nigeria Delta), which is most of the post-2011 sample.

## 6. The κ ≈ 0 claim

`grep -rn kappa src/ data/` finds it computed in `src/state/outcomes.py::cohen_kappa`, called from
`run()` (not read — only the pure function was), writing `data/state/outcomes_kappa.json`. This is the
**retired** `sr_outcome_90`-vs-independent-sources comparison (Amendment 1's A1.1), not a check on
IES-90 (IES-90 has no self-coded comparison to test against — it *is* the independent record).

Stored: κ = −0.0013 (ICB, n43), −0.2342 (MID, n15), 0.104 (UCDP, n184), 0.0606 (precedence, n184).
Re-executed independently from the raw `event_outcomes` rows (`source in (icb,mid,ucdp,precedence)`,
`field='branch'`) joined to `events.sr_outcome_90`, using the same Cohen's-κ formula:

```
icb          kappa=-0.0013  n=43
mid          kappa=-0.2342  n=15
ucdp         kappa=0.104    n=184
precedence   kappa=0.0606   n=184
```

**Exact match.** The README's "κ ≈ 0" is accurate and reproducible for what it actually measures (the
retired scale vs. independent sources, which is why that scale was retired). What it does not do is
say anything about IES-90's own reliability — there is no second coding of IES-90 to compare against;
the closest thing to that check is this D-4 exercise (§3), which found the *code* faithful to the
*rules*, and §5, which found the *rules* — at the war tier — substantially date-of-event-independent.

## 7. Findings, ranked by risk to a published sentence

**1. (Highest — README, lines 30–33) "Escalation at +90 days ... is computed from dated records in
ICB, COW MID, COW War and UCDP ... after our self-coded labels tested at chance against them (κ ≈ 0)."**
The κ≈0 clause is verified accurate (§6) but describes a *retired* comparison, not IES-90. The "dated
records" clause is true of the sources but not, in practice, true of the war tier of the *output*:
100% of level-3 labels come from the two sources with no ongoing/onset distinction, and ~80% of them
are pre-existing wars continuing through the window (§5). A reader taking "dated" to mean "the war
level is dated to this event's escalation" would be wrong four times in five. Recommend the README
sentence either drop "dated" as applied to the war tier specifically, or add the caveat this audit
found executed: most war-level labels reflect a pre-existing conflict, not this event's escalation.

**2. (OUTCOME_MAPPING.md Amendment 1.1's own stated purpose)** "'ongoing → no level' ... A crisis or
dispute that merely starts in W has the same problem" was registered specifically to stop dating a
whole episode's peak to an event that didn't cause it. That fix was applied to ICB and MID. It was not
applied to COW War (explicitly: "a war spell overlapping W gives level 3" with no carve-out) or to GED
(no ongoing/onset concept exists for a raw death-count threshold at all) — and those two sources
produce every single level-3 label in the corpus. The defect Amendment 1.1 set out to close reopens,
unaddressed, at exactly the top of the scale. This is not a coding bug — the rule is implemented
exactly as registered — it is a registered rule whose consequence contradicts its own stated rationale.

**3. (Data quality, not a published claim — but feeds #1 and #2)** Location-basis contamination
persists whenever the corpus doesn't code a dyadic counterparty. `sanc_2013_11_24` (the JPOA
de-escalation deal) is coded level 2 "use of force" from Iran–Pakistan/Iran–Afghanistan border
incidents with nothing to do with the nuclear deal, solely because our event coding names only Iran
(no counterparty), so P is empty and the event falls back to location-basis. `qatar_gulf_blockade_2017`
and `rus_druzhba_strike_2025a` show the same gap (blockading states / Ukraine not coded as entities at
all, even though they're named in the title). Amendment 2's dyadic-precedence fix only fires when P is
non-empty; it can't rescue an event whose corpus coding never named the other side.

**4. (Minor, self-corrected, does not survive to any output)** My own scorer initially conflated
"ICB/MID covers W" (date + ≥1 mapped country, per A1.2's own preamble) with "a matching crisis/dispute
was found," which broke `deal` until corrected against the engine's stored `covering` field. Noted for
completeness; it affected only my intermediate derivation, not any conclusion above, and level
agreement was unaffected throughout.

**No fixes were made or proposed beyond what OUTCOME_MAPPING.md and the audit task asked me to check.**
