# Data dictionary

_Generated from the live schema of `data/oil.db` by `src/data_dictionary.py` — not hand-typed, so it cannot drift from the actual database._

## `edges` — 292 rows

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

## `entities` — 32 rows

| column | type | not null | pk |
|---|---|---|---|
| entity_id | TEXT |  | yes |
| type | TEXT | yes |  |
| name | TEXT | yes |  |
| notes | TEXT |  |  |

## `event_entities` — 154 rows

| column | type | not null | pk |
|---|---|---|---|
| event_id | TEXT | yes | yes |
| entity_id | TEXT | yes | yes |
| role | TEXT |  | yes |

## `events` — 52 rows

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

## `forecasts` — 0 rows

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

## `observations` — 219,286 rows

| column | type | not null | pk |
|---|---|---|---|
| series_id | TEXT | yes | yes |
| obs_date | TEXT | yes | yes |
| value | REAL |  |  |
| as_of | TEXT |  | yes |
| retrieved_at | TEXT |  |  |

## `prices` — 20,142 rows

| column | type | not null | pk |
|---|---|---|---|
| date | TIMESTAMP |  |  |
| price | REAL |  |  |
| commodity | TEXT |  |  |

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

## `series` — 213 rows

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

## `situation_log` — 71 rows

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

## Series catalogue (`series_id` → unit, cadence, source)

| series_id | unit | frequency | source |
|---|---|---|---|
| `cftc.mm_net_wti` | contracts | weekly | CFTC |
| `derived.brent_vol20` | percent | daily | derived (this repo) |
| `derived.brent_wti_spread` | USD/bbl | daily | derived (this repo) |
| `derived.brent_wti_spread_z` | sigma | daily | derived (this repo) |
| `derived.cot_pct` | percentile | daily | derived (this repo) |
| `derived.curve_2s10s` | percentage points | daily | derived (this repo) |
| `derived.inv_sigma` | sigma | daily | derived (this repo) |
| `derived.usd_z` | sigma | daily | derived (this repo) |
| `derived.vix_pct` | percentile | daily | derived (this repo) |
| `eia.crude_stocks_xspr` | thousand bbl | weekly | EIA |
| `eia.cushing_stocks` | thousand bbl | weekly | EIA |
| `eia.refinery_util` | percent | weekly | EIA |
| `eia.spr_stocks` | thousand bbl | weekly | EIA |
| `fred.DCOILBRENTEU` | USD/bbl | daily | FRED |
| `fred.DCOILWTICO` | USD/bbl | daily | FRED |
| `fred.DGS10` | percent | daily | FRED |
| `fred.DGS2` | percent | daily | FRED |
| `fred.DGS5` | percent | daily | FRED |
| `fred.DHHNGSP` | USD/MMBtu | daily | FRED |
| `fred.DTWEXBGS` | index | daily | FRED |
| `fred.GASREGW` | USD/gallon | weekly | FRED |
| `fred.VIXCLS` | index | daily | FRED |
| `gpr.GPRD` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `gpr.GPRD_ACT` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `gpr.GPRD_THREAT` | index | daily | Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com) |
| `portwatch.bab_el_mandeb.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.bab_el_mandeb.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.cape_of_good_hope.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.cape_of_good_hope.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.hormuz.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.hormuz.n_tanker` | count | daily | IMF PortWatch |
| `portwatch.suez.capacity_tanker` | dwt | daily | IMF PortWatch |
| `portwatch.suez.n_tanker` | count | daily | IMF PortWatch |
| `wiki.views.aramco` | views | daily | Wikimedia |
| `wiki.views.bab_el_mandeb` | views | daily | Wikimedia |
| `wiki.views.hormuz` | views | daily | Wikimedia |
| `wiki.views.houthis` | views | daily | Wikimedia |
| `wiki.views.iran_war` | views | daily | Wikimedia |
| `wiki.views.suez` | views | daily | Wikimedia |
| `predmkt.*` (174 live markets) | probability | daily | Polymarket |
