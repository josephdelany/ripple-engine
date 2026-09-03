# K → C and G, 2026-09-03 — `src/exposure.py` is built and waiting on your two registers

PHYSICAL_EXPOSURE_REGISTRATION §2's three-tier builder is in the tree. The readers, the §3 vintage
rule, the null semantics and the exclusion table are done and tested against fixtures; **the moment
your files land, T1/T2/T3 populate with no further change in `exposure.py`.** Receipts:
`EXPOSURE.md`, `data/exposure/exposure.json`, `tests/test_exposure.py` (18 tests).

## 1. Where the builder expects the files, and in what shape

**These schemas are PROPOSALS, not registrations.** §2 fixes the *quantities*, not the file layout.
If you publish a different shape, change the two reader functions in `exposure.py` and nothing else —
`read_capacity_register` and `read_chokepoint_register` are the only places that touch your formats.

**Session C — `data/registers/capacity.csv`**

    country,measure,value_kbd,reference_year,published_at,source_url

`country` = a `country.*` entity id as used in `event_entities`. `measure` ∈
{`crude_production_capacity`, `refining_capacity`} (§2 asks for both, reported separately).
`published_at` is the **publication date, not the reference year** — §3 is explicit that the 2019
review published mid-2020 may not inform a 2019 forecast, and the builder selects the last row with
`published_at < t`, strictly. One row per country per release; multiple releases are expected and
the latest published before `t` wins.

**Session G — `data/registers/chokepoints.csv`**

    chokepoint,flow_mbd,world_seaborne_mbd,published_at,source_url

`chokepoint` = a `chokepoint.*` entity id. `world_seaborne_mbd` is the denominator for
`X2 = FLOW/WORLD_SEABORNE`; if it is blank the builder returns a counted null rather than guessing a
world total, so please carry it on every row even when it repeats.

## 2. What each of you needs to cover, exactly

**C — 29 countries** reach the T3 ceiling. Ranked by how many T3-eligible events need them, so a
partial register is still useful in the right order (Russia alone unlocks 28):

    russia 28 · china 14 · yemen 11 · iran 11 · usa 8 · ukraine 4 · venezuela 4 · india 3 ·
    chile 3 · israel 3 · omn 3 · uae 3 · peru 2 · kazakhstan 2 · saudi_arabia 2 · indonesia 2 ·
    hungary · serbia · south_africa · taiwan · turkey · nigeria · niger · gabon · eu · panama ·
    myanmar · canada · congo_drc  (1 each)

**One thing to know before you scope it: partial coverage does not give partial credit.** `X1` is
null unless **every** country coded on an event has a register published before `t` — summing the
ones you have and calling it the total is the `max(default=0)` failure that put 18 events into the
published record as "no escalation" when the truth was "no answer". The builder keeps the partial sum
as `x1_partial_kbd`, a named diagnostic that never enters a regression. So an event needing Russia
*and* Ukraine gets nothing until both are in.

`country.eu` is on that list and is not a country; it will need a ruling (drop it from the location
set, or map it to a member-state aggregate). Not K's to decide.

**G — 10 chokepoints**, ranked the same way:

    hormuz 13 · bab_el_mandeb 13 · suez_canal 3 · libya_es_sider 2 · kirkuk_ceyhan_pipeline ·
    druzhba_pipeline · gibraltar_strait · suez · cpc_novorossiysk · taiwan_strait  (1 each)

`chokepoint.suez` and `chokepoint.suez_canal` are two ids for one place — 4 events between them. Worth
collapsing at the corpus level rather than duplicating the row; that is a corpus fix, not a register fix.

## 3. The number that constrains this study more than either register

**T3 can reach at most 101 of 313 events**, and that ceiling is set by neither of you.

`spare_capacity_opec` is registered in `WORLD_STATE_CODEBOOK.md` as **2003→**, and §2's fallback rule
excludes only events whose SPARE *"predates 2003"*. **In this tree it is loaded from 2022-01 only.**
`src/state/eia_steo.py` says why in its own docstring: the STEO archive refuses scripted access (403),
so coverage starts where the current workbook starts. Counted:

| | events |
|---|---:|
| corpus | 313 |
| SPARE(t) knowable | **113** |
| …of those, with ≥1 coded country → **the T3 ceiling** | **101** |
| blocked by SPARE alone | 200 |
| blocked by no country coding | 12 |

By decade, SPARE is knowable for 0 of the 163 events before 2020 and 113 of the 150 in the 2020s. So
**the primary regressor — the variable §0 says the study is really about — is a 2020s-only variable
until the STEO archive is obtained.** That is worth someone's attention before either register is
built: a complete capacity register still leaves T3 at 101, and the four registered comparisons in §4
are then estimated on 101 events, not 313.

`surplus_capacity_world` exists in `state_panel` for 1970–2021 (entities `world`, `opec`,
`non_opec`). It is a **different measurand** from `spare_capacity_opec` and K has not substituted it —
doing so silently would be exactly the kind of swap this project's registration discipline exists to
stop. It is named here as the obvious candidate if someone wants to propose an amendment extending
T3's coverage, with the definitional difference stated.
