> **REFERENCE — SPECIFICATION, NOT A RESULT.** A specification or codebook for the legacy engine's data and rules. It claims no finding; the authoritative result is in [`PAPER.md`](../PAPER.md).

# WORLD-STATE CODEBOOK — one line per field, registered before any loader runs
*2026-09-02 (PATH Step 1). Every panel and dossier field the state engine may
condition on. Columns: block · field (the `state_panel.field` id) · unit ·
resolution (d daily, w weekly, m monthly, q quarterly, a annual, e per event) ·
source + URL (URLs only from WORLD_STATE_SOURCES.md / WORLD_STATE_FRAMEWORK.md)
· coverage · licence · rule id. Entity keys: `world`, `opec`, `region.<name>`,
`country.<iso3 lower>` (mapped to the corpus `country.*` ids where they exist),
`dyad.<a>__<b>` (sorted). A field is loaded by code from the named dataset
with the dataset's own release date as `vintage`; the engine at t sees it only
if vintage ≤ t (WORLD_STATE_FRAMEWORK §4.3, enforced by `src/state/panel.py`).
Fields marked "loaded" already sit in `observations` and are exposed through
the panel view without re-fetching. Licence codes: PD public domain · CC-BY ·
CC-BY-SA · cite (free, citation required) · **local** (redistribution
prohibited or by request: file lives in `data/state/local/`, gitignored, README
stub committed) · gap (no free source; field is "unknown" and counted).*

## Rules
- **WS-R1 vintage.** `vintage` = the dataset's release date (version page or
  HTTP Last-Modified of the file actually parsed), never null, never the
  observation date, never the fetch date alone; `retrieved_at` is separate.
- **WS-R2 annual carry.** An annual value applies from 1 Jan of its year and is
  labelled `annual`; no interpolation.
- **WS-R3 unknown.** Missing = absent row; the join reports `unknown` and counts
  it. No imputation.
- **WS-R4 identity.** Country codes map through one table
  (`src/state/countries.py`: COW ccode ↔ ISO3 ↔ corpus `country.*`); unmapped
  codes are listed in the status report, never silently dropped.
- **WS-R5 splice.** Two sources for one concept are two fields (e.g. curve from
  EIA to 2024-04 and from a delayed continuous feed after), never spliced.

## Fields

| block | field | unit | resolution | source + URL | coverage | licence | rule id |
|---|---|---|---|---|---|---|---|
| PHYSICAL | surplus_capacity_world | mb/d | a | EIA Global Surplus Crude Oil Production Capacity 1970–2021 (figure2.xlsx) — https://www.eia.gov/international/content/analysis/special_topics/Global_Surplus_Crude_Oil_Production_Capacity/ | 1970–2021 | PD | WS-P01 |
| PHYSICAL | spare_capacity_opec | mb/d | m | EIA STEO country spare capacity tables (register §3: "Monthly STEO country spare capacity 2003→") — no direct URL in the register; loader records the file URL it parsed | 2003→ | PD | WS-P02 |
| PHYSICAL | crude_production | kb/d | m | EIA International Energy Statistics API v2 (free key, register §3) — key absent → stub | 1973→ | PD | WS-P03 |
| PHYSICAL | crude_production_annual | kb/d | a | EI Statistical Review of World Energy, archive xlsx — https://www.energyinst.org/statistical-review/resources-and-data-downloads | 1965→ | cite | WS-P04 |
| PHYSICAL | consumption_annual | kb/d | a | EI Statistical Review — https://www.energyinst.org/statistical-review/resources-and-data-downloads | 1965→ | cite | WS-P05 |
| PHYSICAL | refinery_capacity_annual | kb/d | a | EI Statistical Review — https://www.energyinst.org/statistical-review/resources-and-data-downloads | 1965→ | cite | WS-P06 |
| PHYSICAL | proven_reserves | bn bbl | a | EI Statistical Review — https://www.energyinst.org/statistical-review/resources-and-data-downloads | 1980→ | cite | WS-P07 |
| PHYSICAL | net_import_dependence | ratio | a | EI Statistical Review (consumption − production) / consumption — https://www.energyinst.org/statistical-review/resources-and-data-downloads | 1965→ | cite | WS-P08 |
| PHYSICAL | us_crude_stocks_xspr | kb | w | EIA weekly (loaded: `eia.crude_stocks_xspr`) | 1982→ | PD | WS-P09 |
| PHYSICAL | us_spr_stock | kb | w | EIA weekly (loaded: `eia.spr_stocks`) | 1982→ | PD | WS-P10 |
| PHYSICAL | us_refinery_utilization | percent | w | EIA weekly (loaded: `eia.refinery_util`) | 1990→ | PD | WS-P11 |
| PHYSICAL | chokepoint_transits | vessels/day | d | IMF PortWatch (loaded: `data/portwatch.json`) | 2019→ | cite | WS-P12 |
| PHYSICAL | tanker_freight | index | d | Baltic Dirty/Clean Tanker Index — licensed, no free source (register §5) | 1998→ (not held) | gap | WS-P13 |
| MARKET | wti_monthly | USD/bbl | m | FRED WTISPLC (loaded: `fred.WTISPLC`) | 1946→ | PD | WS-M01 |
| MARKET | brent_daily | USD/bbl | d | FRED DCOILBRENTEU (loaded) | 1987→ | PD | WS-M02 |
| MARKET | wti_daily | USD/bbl | d | FRED DCOILWTICO (loaded) | 1986→ | PD | WS-M03 |
| MARKET | diesel_crack | USD/bbl | d | derived from loaded EIA/FRED series (loaded: `derived.diesel_crack`) | 1986→ | PD | WS-M04 |
| MARKET | curve_m1_m4_spread | USD/bbl | d | EIA NYMEX futures contracts 1–4 (RCLC1..RCLC4) — https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm | 1985-04→2024-04-05 | PD | WS-M05 |
| MARKET | curve_m1_m4_spread_cme | USD/bbl | d | delayed continuous CL contracts (yfinance), separate source tag, never spliced (WS-R5) | 2024-04→ | cite | WS-M06 |
| MARKET | vxo | index | d | CBOE via FRED (loaded: `fred.VXOCLS`) | 1986→ | PD | WS-M07 |
| MARKET | vix | index | d | CBOE via FRED (loaded: `fred.VIXCLS`) | 1990→ | PD | WS-M08 |
| MARKET | ovx | index | d | CBOE via FRED (loaded: `fred.OVXCLS`) | 2007→ | PD | WS-M09 |
| MARKET | cot_managed_money_net | contracts | w | CFTC (loaded: `cftc.mm_net_wti`) | 2006→ | PD | WS-M10 |
| MARKET | macro_vintages | various | m | FRED/ALFRED vintages (loaded: `fred.*`, `alfred.*`) | 1946→ | PD | WS-M11 |
| MARKET | kilian_igrea | index | m | Kilian global real economic activity index (Dallas Fed IGREA release) — https://sites.google.com/site/lkilian2019/research/data-sets | 1968→ | cite | WS-M12 |
| MARKET | opec_supply_shock_kilian | mb/d | q | Kilian exogenous OPEC supply-shock series — https://sites.google.com/site/lkilian2019/research/data-sets | 1971–2004 | cite | WS-M13 |
| ACTORS | cinc | share | a | COW National Material Capabilities v7 — https://correlatesofwar.org/data-sets/national-material-capabilities/ | 1816–2022 | cite | WS-A01 |
| ACTORS | milex_cow | thousand USD (current) | a | COW NMC v7 `milex` — https://correlatesofwar.org/data-sets/national-material-capabilities/ | 1816–2022 | cite | WS-A02 |
| ACTORS | milper_cow | thousands | a | COW NMC v7 `milper` — https://correlatesofwar.org/data-sets/national-material-capabilities/ | 1816–2022 | cite | WS-A03 |
| ACTORS | milex_sipri | USD m (constant) | a | SIPRI Military Expenditure Database — https://www.sipri.org/databases/milex | 1949→ | local | WS-A04 |
| ACTORS | milex_gdp_share_sipri | percent | a | SIPRI Military Expenditure Database — https://www.sipri.org/databases/milex | 1949→ | local | WS-A05 |
| ACTORS | arms_imports_tiv | TIV m | a | SIPRI Arms Transfers Database (register §1, "Arms Transfers database (TIV) 1950→") | 1950→ | local | WS-A06 |
| ACTORS | polity2 | score −10..10 | a | Polity5 (p5v2018.xls) — https://www.systemicpeace.org/inscrdata.html | 1946–2018 | local | WS-A07 |
| ACTORS | polity_durable | years | a | Polity5 `durable` — https://www.systemicpeace.org/inscrdata.html | 1946–2018 | local | WS-A08 |
| ACTORS | vdem_polyarchy | index 0..1 | a | V-Dem v16 Country-Year Core `v2x_polyarchy` — https://www.v-dem.net/data/the-v-dem-dataset/ | 1789→ (used 2019→) | CC-BY-SA | WS-A09 |
| ACTORS | leader_tenure_days | days | e | Archigos v4.1 (register §1; rochester.edu) | 1875–2015 | cite | WS-A10 |
| ACTORS | leader_change_last_365d | 0/1 | e | Archigos v4.1 (register §1) | 1875–2015 | cite | WS-A11 |
| ACTORS | oil_rents_gdp | percent | a | World Bank WDI `NY.GDP.PETR.RT.ZS` (free API, register §4) | 1970→ | cite | WS-A12 |
| ACTORS | fiscal_breakeven | USD/bbl | a | IMF (loaded: `data/breakevens*`) | 2000s→ | cite | WS-A13 |
| ACTORS | coup_last_5y | count | a | CSP Coups d'État 1946–2021 — https://www.systemicpeace.org/inscrdata.html | 1946–2021 | local | WS-A14 |
| DYADS | atop_defense_pact | 0/1 | a | ATOP 5.1 dyad-year — http://www.atopdata.org/data.html | 1815–2018 | cite | WS-D01 |
| DYADS | atop_any_obligation | 0/1 | a | ATOP 5.1 dyad-year (defense, offense, neutrality, nonaggression, consultation) — http://www.atopdata.org/data.html | 1815–2018 | cite | WS-D02 |
| DYADS | mid_count_10y | count | a | COW MID 5.0 dyadic (4.03) — https://correlatesofwar.org/data-sets/mids/ | 1816–2014 | cite | WS-D03 |
| DYADS | mid_max_hostlev_10y | 1..5 | a | COW MID 5.0 dyadic `hostlev` — https://correlatesofwar.org/data-sets/mids/ | 1816–2014 | cite | WS-D04 |
| DYADS | mid_last_date | date | a | COW MID 5.0 dyadic — https://correlatesofwar.org/data-sets/mids/ | 1816–2014 | cite | WS-D05 |
| DYADS | icb_crisis_count | count | e | ICB v16 system + dyads — https://sites.duke.edu/icbdata/data-collections/ | 1918–2021 | cite | WS-D06 |
| DYADS | icb_last_outcome_form | 1..7 (FOROUT) | e | ICB v16 — https://sites.duke.edu/icbdata/data-collections/ | 1918–2021 | cite | WS-D07 |
| DYADS | icb_last_violence | 1..4 (VIOL) | e | ICB v16 — https://sites.duke.edu/icbdata/data-collections/ | 1918–2021 | cite | WS-D08 |
| DYADS | icb_last_tension | OUTESR | e | ICB v16 — https://sites.duke.edu/icbdata/data-collections/ | 1918–2021 | cite | WS-D09 |
| DYADS | sanctions_in_force | 0/1 + type | a | GSDB R5 dyadic — https://www.globalsanctionsdatabase.com/ (by request; Joe) | 1950–2025 | local | WS-D10 |
| DYADS | trade_share_bilateral | percent of exports | a | IMF Direction of Trade Statistics (register §1 "IMF DOTS (1948→)") | 1948→ | cite | WS-D11 |
| DYADS | unga_ideal_point_distance | distance | a | Voeten UNGA ideal points (register §1) | 1946→ | cite | WS-D12 |
| DYADS | diplomatic_representation | level | a | COW Diplomatic Exchange (register: to 2005) / dossier after | to 2005 | cite | WS-D13 |
| SYSTEM | ucdp_active_conflicts | count | a | UCDP/PRIO Armed Conflict v26.1 — https://ucdp.uu.se/downloads/ | 1946→ | CC-BY | WS-S01 |
| SYSTEM | ucdp_intensity_max | 1..2 | a | UCDP/PRIO Armed Conflict `intensity_level` — https://ucdp.uu.se/downloads/ | 1946→ | CC-BY | WS-S02 |
| SYSTEM | ucdp_battle_deaths | deaths (best) | a | UCDP Battle-Related Deaths v26.1 — https://ucdp.uu.se/downloads/ | 1989→ | CC-BY | WS-S03 |
| SYSTEM | gp_posture_gulf | text | e | dossier (sourced statements; framework §3 SYSTEM) | — | cite | WS-S04 |
| SYSTEM | gpr_monthly | index | m | Caldara–Iacoviello GPR Recent, monthly export — https://www.matteoiacoviello.com/gpr.htm | 1985→ | CC-BY | WS-S05 |
| SYSTEM | gpr_threats_monthly | index | m | GPR Recent `GPRT` — https://www.matteoiacoviello.com/gpr.htm | 1985→ | CC-BY | WS-S06 |
| SYSTEM | gpr_acts_monthly | index | m | GPR Recent `GPRA` — https://www.matteoiacoviello.com/gpr.htm | 1985→ | CC-BY | WS-S07 |
| SYSTEM | gprh_monthly | index | m | GPR Historical `GPRH` — https://www.matteoiacoviello.com/gpr.htm | 1900→ | CC-BY | WS-S08 |
| SYSTEM | gpr_country_monthly | index | m | GPR country indexes (44 countries) — https://www.matteoiacoviello.com/gpr.htm | 1985→ | CC-BY | WS-S09 |
| SYSTEM | gpr_vintage_monthly | index | m | GPR monthly vintage archive (data_gpr_export_YYYYMM.xls) — https://www.matteoiacoviello.com/gpr.htm | archive as published | CC-BY | WS-S10 |
| SYSTEM | opec_decision_dated | text/date | e | OPEC conference record + Känzig announcement dataset (register §3, GitHub dkaenzig/replicationOilSupplyNews) | 1960→ / 1983→ | cite | WS-S11 |
| SYSTEM | unsc_action | text | e | dossier (UN records) | — | cite | WS-S12 |
| SYSTEM | mepv_regional_war | magnitude | a | CSP Major Episodes of Political Violence — https://www.systemicpeace.org/inscrdata.html | 1946–2018 | local | WS-S13 |
| NARRATIVE | gprh_newspaper_share | percent | m | GPR Historical article share — https://www.matteoiacoviello.com/gpr.htm | 1900→ | CC-BY | WS-N01 |
| NARRATIVE | nyt_article_count | count | m/e | NYT Article Search API (free key, never committed; register §2) — key absent → stub | 1851→ | local | WS-N02 |
| NARRATIVE | gdelt_volume_tone | count/tone | d | GDELT 2.0 (loaded: `data/gdelt_tone.json`) | 1979→ | cite | WS-N03 |
| NARRATIVE | contemporaneous_claims | text | e | source article of the event + NYT archive, claim-extracted point-in-time (`reader.py`, ledger) | per event | cite | WS-N04 |

## Coverage and status
Coverage is the dataset's, as stated in the register. What is actually loaded,
per block per decade, is printed by `python3 src/state/status.py` and never
recited here.

## Amendment 1 — 2026-09-02, after the first smoke load and before the first loader commit (disclosed)
WS-R1 as written made every historical value invisible: a panel released in 2022–2026
carries observations from 1946→, and `vintage = release date` means the engine at
2001-09-11 sees nothing — the opposite of what WORLD_STATE_FRAMEWORK §7 expects
("CINC 2000, Polity 2000, SIPRI 2000 ... with vintages ≤ that day"). Seen in the
first run and rejected as a definition error. Replaced by two dates on every row:
- **`vintage`** = the date the value was *nominally available* under the loader's
  schedule convention, not an independently verified contemporaneous publication receipt: a daily market print on its date; a
  monthly index on the first day of the following month; an annual value on
  1 January of the following year; an event-resolution value (crisis outcome,
  leader change, dispute) on the day after the event ends. Never null.
- **`release`** = the dataset release actually parsed (its HTTP Last-Modified or
  documented version date). Never null. Recorded so a revision can be traced.
- **`retrospective`** = 1 when the series is a later *construction* rather than a
  contemporaneous record (EIA's 2022 surplus-capacity reconstruction, GPR/GPRH
  indexes built from archives, IGREA). The value is still dated knowable at period
  end, but the walk (WALK_FORWARD_PROTOCOL) must report results with and without
  retrospective fields; a retrospective field alone can never make a read
  VALIDATED.
The engine at t reads `vintage ≤ t` (unchanged). WS-R2..R5 unchanged.

**Later audit qualification (2026-09-04).** For the public experiment, `vintage <= t` excludes
none of the 11,029 panel rows, while `release <= t` excludes 10,150. The former is therefore too
permissive to prove historical knowability and the latter can be too conservative when `release`
is the date of a modern retrospective file. A future experiment needs source-specific publication
receipts; neither generic column should be described as ground truth about what an analyst knew.
