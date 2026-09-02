# Data dictionary

_Generated from the live schema of `data/oil.db` by `src/data_dictionary.py` — not hand-typed, so it cannot drift from the actual database._

## `belief_state` — 3 rows

| column | type | not null | pk |
|---|---|---|---|
| variable_id | TEXT |  | yes |
| value | REAL |  |  |
| as_of | TEXT |  |  |
| status | TEXT |  |  |
| method | TEXT |  |  |
| updated_at | TEXT |  |  |

## `edges` — 8,073 rows

| column | type | not null | pk |
|---|---|---|---|
| edge_id | INTEGER |  | yes |
| from_entity | TEXT |  |  |
| to_entity | TEXT |  |  |
| polarity | TEXT |  |  |
| lag | TEXT |  |  |
| strength | TEXT |  |  |
| confidence | TEXT |  |  |
| mechanism | TEXT |  |  |
| event_id | TEXT |  |  |
| target_series | TEXT |  |  |
| car5 | REAL |  |  |
| car20 | REAL |  |  |
| units | TEXT |  |  |
| n_days | INTEGER |  |  |

## `entities` — 122 rows

| column | type | not null | pk |
|---|---|---|---|
| entity_id | TEXT |  | yes |
| type | TEXT | yes |  |
| name | TEXT | yes |  |
| notes | TEXT |  |  |

## `event_entities` — 711 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT | yes | yes |
| entity_id | TEXT | yes | yes |
| role | TEXT |  | yes |

## `event_outcomes` — 3,626 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT | yes | yes |
| source | TEXT | yes | yes |
| field | TEXT | yes | yes |
| value | REAL |  |  |
| value_text | TEXT |  |  |
| detail | TEXT |  |  |
| computed_at | TEXT | yes |  |

## `events` — 313 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT |  | yes |
| event_date | TEXT | yes |  |
| date_precision | TEXT |  |  |
| type | TEXT | yes |  |
| title | TEXT | yes |  |
| description | TEXT |  |  |
| severity | INTEGER |  |  |
| confidence | TEXT |  |  |
| source_url | TEXT | yes |  |
| added_at | TEXT |  |  |
| surprise | INTEGER |  |  |
| sr_actor | TEXT |  |  |
| sr_target | TEXT |  |  |
| sr_asset_role | TEXT |  |  |
| sr_conflict_scope | TEXT |  |  |
| sr_tempo | TEXT |  |  |
| sr_alliance | TEXT |  |  |
| sr_diplomatic | TEXT |  |  |
| sr_target_capacity | TEXT |  |  |
| sr_outcome_30 | TEXT |  |  |
| sr_outcome_90 | TEXT |  |  |
| sr_actor_propensity | REAL |  |  |
| sr_prior_dyad | TEXT |  |  |
| sr_confidence | REAL |  |  |
| sr_json | TEXT |  |  |

## `forecasts` — 8 rows

| column | type | not null | pk |
|---|---|---|---|
| forecast_id | INTEGER |  | yes |
| made_at | TEXT | yes |  |
| question | TEXT | yes |  |
| horizon | TEXT |  |  |
| my_prob | REAL |  |  |
| market_prob | REAL |  |  |
| market_source | TEXT |  |  |
| resolved_at | TEXT |  |  |
| outcome | INTEGER |  |  |
| notes | TEXT |  |  |

## `gaps` — 248 rows

| column | type | not null | pk |
|---|---|---|---|
| gap_id | TEXT |  | yes |
| as_of | TEXT |  |  |
| anchor_date | TEXT |  |  |
| subject | TEXT |  |  |
| engine_call | TEXT |  |  |
| engine_p | REAL |  |  |
| priced_ovx | REAL |  |  |
| priced_ovx_pct | REAL |  |  |
| gap_direction | TEXT |  |  |
| horizon_days | INTEGER |  |  |
| outcome | INTEGER |  |  |
| brier | REAL |  |  |
| resolved_at | TEXT |  |  |
| source_url | TEXT |  |  |
| notes | TEXT |  |  |

## `library` — 297 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT |  | yes |
| event_date | TEXT |  |  |
| signature | TEXT |  |  |
| mag_pp | REAL |  |  |

## `observations` — 467,436 rows

| column | type | not null | pk |
|---|---|---|---|
| series_id | TEXT | yes | yes |
| obs_date | TEXT | yes | yes |
| value | REAL |  |  |
| as_of | TEXT |  | yes |
| retrieved_at | TEXT |  |  |

## `prices` — 20,194 rows

| column | type | not null | pk |
|---|---|---|---|
| date | TIMESTAMP |  |  |
| price | REAL |  |  |
| commodity | TEXT |  |  |

## `propagation_edges` — 232 rows

| column | type | not null | pk |
|---|---|---|---|
| edge_id | TEXT |  | yes |
| kind | TEXT |  |  |
| from_node | TEXT |  |  |
| to_node | TEXT |  |  |
| lag | TEXT |  |  |
| strength | REAL |  |  |
| ci_lo | REAL |  |  |
| ci_hi | REAL |  |  |
| perm_p | REAL |  |  |
| status | TEXT |  |  |
| mechanism | TEXT |  |  |

## `quiet_events` — 6 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT |  | yes |
| event_date | TEXT | yes |  |
| date_precision | TEXT |  |  |
| type | TEXT | yes |  |
| title | TEXT | yes |  |
| description | TEXT |  |  |
| severity | INTEGER |  |  |
| surprise | INTEGER |  |  |
| confidence | TEXT |  |  |
| source_url | TEXT | yes |  |
| added_at | TEXT |  |  |

## `reads` — 1 rows

| column | type | not null | pk |
|---|---|---|---|
| read_id | INTEGER |  | yes |
| made_at | TEXT | yes |  |
| situation_id | TEXT |  |  |
| kind | TEXT | yes |  |
| anchor_date | TEXT | yes |  |
| anchor_series | TEXT | yes |  |
| anchor_value | REAL |  |  |
| horizon_days | INTEGER | yes |  |
| expected_car | REAL | yes |  |
| basis | TEXT |  |  |
| amp_context | TEXT |  |  |
| resolved_at | TEXT |  |  |
| realized_car | REAL |  |  |
| error | REAL |  |  |
| notes | TEXT |  |  |

## `series` — 598 rows

| column | type | not null | pk |
|---|---|---|---|
| series_id | TEXT |  | yes |
| name | TEXT | yes |  |
| entity_id | TEXT |  |  |
| unit | TEXT |  |  |
| frequency | TEXT |  |  |
| source | TEXT |  |  |
| source_url | TEXT |  |  |
| notes | TEXT |  |  |

## `signals` — 7 rows

| column | type | not null | pk |
|---|---|---|---|
| signal_id | TEXT |  | yes |
| name | TEXT |  |  |
| mechanism | TEXT |  |  |
| method | TEXT |  |  |
| inputs | TEXT |  |  |
| oos_metric | TEXT |  |  |
| oos_value | REAL |  |  |
| status | TEXT |  |  |
| evidence | TEXT |  |  |
| updated_at | TEXT |  |  |

## `situation_log` — 3,627 rows

| column | type | not null | pk |
|---|---|---|---|
| log_id | INTEGER |  | yes |
| situation_id | TEXT | yes |  |
| ts | TEXT | yes |  |
| kind | TEXT |  |  |
| actor_entity | TEXT |  |  |
| headline | TEXT | yes |  |
| detail | TEXT |  |  |
| source_url | TEXT | yes |  |
| retrieved_at | TEXT | yes |  |
| status | TEXT | yes |  |
| confidence | TEXT |  |  |
| alert_url | TEXT |  |  |
| promoted_event_id | TEXT |  |  |

## `situation_state` — 8,564 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT | yes | yes |
| entity_id | TEXT | yes | yes |
| field | TEXT | yes | yes |
| obs_date | TEXT |  |  |
| value | REAL |  |  |
| value_text | TEXT |  |  |
| vintage | TEXT | yes |  |
| release | TEXT | yes |  |
| retrospective | INTEGER | yes |  |
| source | TEXT | yes |  |
| joined_at | TEXT | yes |  |

## `state_panel` — 280,208 rows

| column | type | not null | pk |
|---|---|---|---|
| entity_id | TEXT | yes | yes |
| field | TEXT | yes | yes |
| obs_date | TEXT | yes | yes |
| value | REAL |  |  |
| value_text | TEXT |  |  |
| unit | TEXT |  |  |
| source | TEXT | yes |  |
| vintage | TEXT | yes | yes |
| release | TEXT | yes |  |
| retrospective | INTEGER | yes |  |
| retrieved_at | TEXT | yes |  |

## Series catalogue (`series_id` → unit, cadence, source)

| series_id | unit | frequency | source |
|---|---|---|---|
| `cftc.mm_net_wti` | contracts | weekly | CFTC |
| `derived.be_level` | percentile | daily | derived (this repo) |
| `derived.brent_vol20` | percent | daily | derived (this repo) |
| `derived.brent_wti_spread` | USD/bbl | daily | derived (this repo) |
| `derived.brent_wti_spread_z` | sigma | daily | derived (this repo) |
| `derived.conflict_intensity_pct` | percentile | daily | derived (this repo) |
| `derived.cot_pct` | percentile | daily | derived (this repo) |
| `derived.credit_stress` | percentile | daily | derived (this repo) |
| `derived.curve_2s10s` | percentage points | daily | derived (this repo) |
| `derived.diesel_crack` | USD/bbl | daily | derived (this repo) |
| `derived.gasoline_crack` | USD/bbl | daily | derived (this repo) |
| `derived.inv_sigma` | sigma | daily | derived (this repo) |
| `derived.ovx_pct` | percentile | daily | derived (this repo) |
| `derived.real_rate` | percentile | daily | derived (this repo) |
| `derived.usd_z` | sigma | daily | derived (this repo) |
| `derived.vix_pct` | percentile | daily | derived (this repo) |
| `eia.crude_stocks_xspr` | thousand bbl | weekly | EIA |
| `eia.cushing_stocks` | thousand bbl | weekly | EIA |
| `eia.refinery_util` | percent | weekly | EIA |
| `eia.spr_stocks` | thousand bbl | weekly | EIA |
| `fred.BAMLH0A0HYM2` | percent | daily | FRED |
| `fred.DCOILBRENTEU` | USD/bbl | daily | FRED |
| `fred.DCOILWTICO` | USD/bbl | daily | FRED |
| `fred.DEXCHUS` | CNY/USD | daily | FRED |
| `fred.DEXJPUS` | JPY/USD | daily | FRED |
| `fred.DEXUSEU` | USD/EUR | daily | FRED |
| `fred.DFII10` | percent | daily | FRED |
| `fred.DGASUSGULF` | USD/gal | daily | FRED |
| `fred.DGS10` | percent | daily | FRED |
| `fred.DGS2` | percent | daily | FRED |
| `fred.DGS5` | percent | daily | FRED |
| `fred.DHHNGSP` | USD/MMBtu | daily | FRED |
| `fred.DHOILNYH` | USD/gal | daily | FRED |
| `fred.DPROPANEMBTX` | USD/gal | daily | FRED |
| `fred.DTWEXBGS` | index | daily | FRED |
| `fred.GASREGW` | USD/gallon | weekly | FRED |
| `fred.OVXCLS` | index | daily | FRED |
| `fred.PCU325211325211` | index | monthly | FRED |
| `fred.PCU325311325311` | index | monthly | FRED |
| `fred.SP500` | index | daily | FRED |
| `fred.T10YIE` | percent | daily | FRED |
| `fred.T5YIE` | percent | daily | FRED |
| `fred.VIXCLS` | index | daily | FRED |
| `fred.WTISPLC` | $/bbl | monthly | FRED |
| `gdelt.tone.hormuz` | tone | daily | GDELT DOC |
| `gdelt.tone.opec` | tone | daily | GDELT DOC |
| `gpr.GPRD` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `gpr.GPRD_ACT` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `gpr.GPRD_THREAT` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `imf.breakeven.algeria` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.iran` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.iraq` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.kazakhstan` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.kuwait` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.oman` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.qatar` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.saudi_arabia` | USD/bbl | yearly | IMF REO (via FRED) |
| `imf.breakeven.uae` | USD/bbl | yearly | IMF REO (via FRED) |
| `live.brent` | USD/bbl | daily | Yahoo (yfinance) |
| `live.dxy` | index | daily | Yahoo (yfinance) |
| `live.gold` | USD/oz | daily | Yahoo (yfinance) |
| `live.natgas` | USD/MMBtu | daily | Yahoo (yfinance) |
| `live.sp500` | index | daily | Yahoo (yfinance) |
| `live.us10y` | percent | daily | Yahoo (yfinance) |
| `live.vix` | index | daily | Yahoo (yfinance) |
| `live.wti` | USD/bbl | daily | Yahoo (yfinance) |
| `live.xle` | USD | daily | Yahoo (yfinance) |
| `portwatch.bab_el_mandeb.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.bab_el_mandeb.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.cape_of_good_hope.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.cape_of_good_hope.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.hormuz.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.hormuz.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.suez.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.suez.n_tanker` | count | daily | IMF PortWatch |
| `ucdp.fat_africa` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `ucdp.fat_americas` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `ucdp.fat_asia` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `ucdp.fat_europe` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `ucdp.fat_global` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `ucdp.fat_middle_east` | fatalities (best est.) | monthly | UCDP GED (Uppsala) |
| `wiki.views.aramco` | views | daily | Wikimedia |
| `wiki.views.bab_el_mandeb` | views | daily | Wikimedia |
| `wiki.views.hormuz` | views | daily | Wikimedia |
| `wiki.views.houthis` | views | daily | Wikimedia |
| `wiki.views.iran_war` | views | daily | Wikimedia |
| `wiki.views.suez` | views | daily | Wikimedia |
| `yf.copper` | USD/lb | daily | Yahoo (yfinance) |
| `yf.copper_miners` | USD | daily | Yahoo (yfinance) |
| `yf.corn` | USc/bu | daily | Yahoo (yfinance) |
| `yf.freight` | USD | daily | Yahoo (yfinance) |
| `yf.gold` | USD/oz | daily | Yahoo (yfinance) |
| `yf.hyg` | USD | daily | Yahoo (yfinance) |
| `yf.jkm` | USD/MMBtu | daily | Yahoo (yfinance) |
| `yf.miners` | USD | daily | Yahoo (yfinance) |
| `yf.palladium` | USD/oz | daily | Yahoo (yfinance) |
| `yf.platinum` | USD/oz | daily | Yahoo (yfinance) |
| `yf.silver` | USD/oz | daily | Yahoo (yfinance) |
| `yf.soybean` | USc/bu | daily | Yahoo (yfinance) |
| `yf.sp500` | index | daily | Yahoo (yfinance) |
| `yf.tankers` | USD | daily | Yahoo (yfinance) |
| `yf.ttf` | EUR/MWh | daily | Yahoo (yfinance) |
| `yf.wheat` | USc/bu | daily | Yahoo (yfinance) |
| `predmkt.*` (495 live markets) | probability | daily | Polymarket |
