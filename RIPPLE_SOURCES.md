# RIPPLE SOURCES — verified register (2026-09-02)
*Companion to RIPPLE_REGISTRATION.md (brief R, items R2/R3a). Rule inherited from
WORLD_STATE_SOURCES.md: no source is used until its page was opened, its variables,
frequency, coverage and licence confirmed, and that recorded here. A source that could
not be verified is a **GAP** line, never a number. Nothing paid; no new keys; the EIA
key (if present) is never quoted and is not used by the ripple loaders at all.*

**How verification was done.** Pages were opened with the session's web fetch tool;
files were downloaded with Python `requests` and opened locally with pandas/openpyxl/
xlrd/pypdf (the workspace hook blocks `curl`/`wget` from the shell; nothing was fetched
by circumventing it). "Verified" = the file or endpoint was retrieved and inspected
today. "In DB" = the series was already in `data/oil.db` from an earlier verified
loader; for those the FRED CSV endpoint was re-opened today and the first/last dates
below are today's. Loader: `src/ripple_fetch.py` (seeds under `data/seed/ripple/`,
manifest with sha256 + retrieval time; `--refresh` pulls live; `--verify` prints
first/last/rows without writing). Loader run 2026-09-02 19:34 UTC: **54 series ok,
0 failed.** Downloaded evidence for this register is in the session scratchpad; the
seeds are the committed copies.

Legend — *how loaded*: `existing` (already in oil.db via the named loader),
`seed` (ripple_fetch, committed under data/seed/ripple/ — licence permits
redistribution), `refresh-only` (ripple_fetch pulls live into the local DB; never
committed — licence unread or personal-use), `not loaded` (gap).

## 1. Crude and products — daily, FRED (keyless CSV; source EIA, public domain)

FRED terms (fred.stlouisfed.org/legal, opened): "Public Domain: Citation requested —
These series may be under copyright or in the public domain and may be used without
permission… please cite the data source and acknowledge that you obtained the data
from FRED." All series in this table are EIA-sourced (EIA: "U.S. government
publications are in the public domain", eia.gov/about/copyrights_reuse.php, opened).

| series_id | FRED id | what | unit | first | last (2026-09-02) | rows | how loaded |
|---|---|---|---|---|---|---|---|
| fred.DCOILBRENTEU | DCOILBRENTEU | Brent spot, Europe | USD/bbl | 1987-05-20 | 2026-09-01 | 9,967 | existing (fetch_prices) |
| fred.DCOILWTICO | DCOILWTICO | WTI spot, Cushing | USD/bbl | 1986-01-02 | 2026-09-01 | 10,236 | existing |
| fred.DHOILNYH | DHOILNYH | No.2 heating oil, NY Harbor | USD/gal | 1986-06-02 | 2026-09-01 | 10,110 | existing |
| fred.DGASUSGULF | DGASUSGULF | conventional gasoline, US Gulf | USD/gal | 1986-06-02 | 2026-09-01 | 10,109 | existing (fetch_value_chain) |
| **fred.DGASNYH** | DGASNYH | conventional gasoline, NY Harbor regular | USD/gal | 1986-06-02 | 2026-09-01 | 10,112 | **seed** (new) |
| **fred.DJFUELUSGULF** | DJFUELUSGULF | kerosene-type jet fuel, US Gulf | USD/gal | 1990-04-02 | 2026-09-01 | 9,145 | **seed** (new) |
| fred.DPROPANEMBTX | DPROPANEMBTX | propane, Mont Belvieu | USD/gal | 1992-07-09 | 2026-09-01 | 8,559 | existing |
| fred.DHHNGSP | DHHNGSP | Henry Hub natural gas spot | USD/mmbtu | 1997-01-07 | 2026-09-01 | 7,446 | existing |

Cracks are derived in `derive_signals.py` (`derived.diesel_crack`, `derived.gasoline_crack`,
1986-06-02 →, mechanism-gated). No new crack is derived here. **Correction (appended
2026-09-02, same day):** an earlier version of this line said a jet crack and an NYH gasoline
crack "are registered in RIPPLE_REGISTRATION.md as derived nodes". They are not — Table N
carries only the two existing cracks above, and no jet or NYH crack was registered or computed.
The pointer did not resolve; it is withdrawn rather than honoured after the fact, since adding
a node to a sealed registration after seeing results is exactly what the seal forbids. If those
cracks are wanted they need a dated amendment before any run that uses them.
Publication: FRED daily petroleum spots post with a lag of ~1–3 business days (the DB
had 08-25 as latest on 09-02 before today's refresh; today's endpoint shows 09-01).

## 2. EIA weekly physical (the PHYSICAL ripple targets) — keyless hist_xls workbooks

Pages opened: `eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=<KEY>&f=W` for all five
keys; workbooks `eia.gov/dnav/pet/hist_xls/<KEY>w.xls` downloaded and parsed (sheet
`Data 1`; row 1 carries the sourcekey and the parser refuses a mismatch). Release:
Weekly Petroleum Status Report, published Wednesdays for the week ending the prior
Friday (release date shown on the page: 9/2/2026 for the week of 8/28). Licence:
public domain (quoted above), acknowledgment requested.

| series_id | sourcekey | title (verbatim from workbook) | unit | first | last | rows | how loaded |
|---|---|---|---|---|---|---|---|
| eia.refinery_util | WPULEUS3 | Weekly U.S. Percent Utilization of Refinery Operable Capacity | percent | 1990-11-02 | 2026-08-28 (xls) / 08-21 in DB | 1,870 | existing (fetch_eia, API); xls verified today, same sourcekey |
| eia.crude_stocks_xspr | WCESTUS1 | Weekly U.S. Ending Stocks excluding SPR of Crude Oil | thousand bbl | 1982-08-20 | 2026-08-28 / 08-21 in DB | 2,292 | existing (fetch_eia); xls verified |
| **eia.distillate_stocks** | WDISTUS1 | Weekly U.S. Ending Stocks of Distillate Fuel Oil | thousand bbl | 1982-08-20 | 2026-08-28 | 2,292 | **seed** (new) |
| **eia.gasoline_stocks** | WGTSTUS1 | Weekly U.S. Ending Stocks of Total Gasoline | thousand bbl | 1990-01-05 | 2026-08-28 | 1,913 | **seed** (new) |
| **eia.crude_imports** | WCRIMUS2 | Weekly U.S. Imports of Crude Oil | thousand bbl/day | 1990-01-05 | 2026-08-28 | 1,913 | **seed** (new) |

## 3. Gas and LNG

- **Henry Hub daily** — fred.DHHNGSP, table 1.
- **yf.ttf (TTF=F)** — VERIFIED as an instrument, unit UNSTATED by Yahoo. yfinance
  `.info`: shortName "Dutch TTF Natural Gas Calendar", exchange NYM, currency EUR,
  quoteType FUTURE; history 2017-10-23 → 2026-09-02, 2,229 rows. It is a
  calendar/continuous contract (which month rolls when is not documented by Yahoo).
  The DB labels the unit EUR/MWh (fetch_value_chain); Yahoo's page does not state the
  unit, so the unit is *inferred from the contract convention*, not measured — flagged.
  Yahoo terms: no market-data redistribution clause was located on the general terms
  page (GAP); yfinance README: "the Yahoo! finance API is intended for personal use
  only." → existing series kept; used as a **regime-check node only**, never seeded.
- **yf.jkm (JKM=F) — NOT a verified daily series.** yfinance returns quoteType
  `ALTSYMBOL`, no longName/shortName, no currency, and prints "possibly delisted; no
  price data found" on the quote lookup, although `history(period='max')` still
  returns 2,813 rows 2014-07-29 → 2026-09-01. What contract, unit or currency those
  closes represent cannot be confirmed from Yahoo. **Ruling: JKM is excluded from the
  ripple study; the Asian LNG node is the World Bank monthly LNG Japan series (§4).**
  `yf.jkm` stays in the DB as-is with this note; it is not used.
- **Monthly fallback with clean provenance: World Bank Pink Sheet** (§4): Natural gas
  US, Natural gas Europe, Liquefied natural gas Japan (1977-01 →).
- **fred.PCU325311325311** — nitrogenous fertilizer PPI, monthly, 1975-12-01 →
  2026-07-01, 597 rows; existing (fetch_value_chain); BLS via FRED, public domain.

## 4. World Bank Pink Sheet (CMO-Historical-Data-Monthly.xlsx) — VERIFIED, seeded

- Page opened: worldbank.org/en/research/commodity-markets ("Next update: September 2,
  2026"). File opened (577,979 bytes, valid xlsx): sheets `AFOSHEET, Monthly Prices,
  Monthly Indices, Description, Index Weights`; `Monthly Prices` header "monthly prices
  in nominal US dollars, 1960 to present", "Updated on August 04, 2026"; 72 commodity
  columns; rows 1960M01 → 2026M07.
- Licence: **CC BY 4.0** — data.worldbank.org/summary-terms-of-use (opened): "you are
  free to copy, distribute, adapt, display or include the data in other products for
  commercial or noncommercial purposes at no cost under a Creative Commons Attribution
  4.0 International License". The dedicated datacatalog licence page is JS-rendered
  and did not return text (noted; the summary-terms page is authoritative enough).
- URL caveat (raised earlier in fetch_value_chain): the document URL embeds a
  version token. `--refresh` fails loudly if it moves; the committed seed keeps the
  study reproducible offline. Publication lag: ~4 days after month end.

| series_id | Pink Sheet column (verbatim) | unit | first | last | rows | how loaded |
|---|---|---|---|---|---|---|
| wb.crude_avg | Crude oil, average | $/bbl | 1960-01 | 2026-07 | 799 | seed |
| wb.brent | Crude oil, Brent | $/bbl | 1960-01 | 2026-07 | 799 | seed |
| wb.ngas_us | Natural gas, US | $/mmbtu | 1960-01 | 2026-07 | 799 | seed |
| wb.ngas_eu | Natural gas, Europe | $/mmbtu | 1960-01 | 2026-07 | 799 | seed |
| wb.lng_japan | Liquefied natural gas, Japan | $/mmbtu | 1977-01 | 2026-07 | 595 | seed |
| wb.urea | Urea | $/mt | 1960-01 | 2026-07 | 799 | seed |
| wb.dap | DAP | $/mt | 1967-01 | 2026-07 | 715 | seed |
| wb.tsp | TSP | $/mt | 1960-01 | 2026-07 | 799 | seed |
| wb.potash | Potassium chloride ** | $/mt | 1960-01 | 2026-07 | 799 | seed |
| wb.coal_aus | Coal, Australian | $/mt | 1970-01 | 2026-07 | 679 | seed |

(The `**` footnote mark is stripped from the key; the workbook's own note applies.)

## 5. Physical flows and chokepoints

### IMF PortWatch daily chokepoint transits — VERIFIED (service queried), refresh-only
- Endpoint: ArcGIS FeatureServer `Daily_Chokepoints_Data/FeatureServer/0` (the same
  service fetch_portwatch.py already uses). Fields: date, year, month, day, portid,
  portname, n_container, n_dry_bulk, n_general_cargo, n_roro, n_tanker, n_cargo,
  n_total, capacity_* (metric tons) by ship type. 28 chokepoints; exact names
  confirmed: `Strait of Hormuz`, `Bab el-Mandeb Strait`, `Suez Canal`, `Malacca Strait`,
  `Panama Canal`, `Bosporus Strait`, `Cape of Good Hope`. Hormuz earliest 2019-01-01,
  latest 2026-08-30.
- Licence — **READ, and the series are now seeded** (Joe's Ruling 3, 2026-09-02). The ArcGIS
  item (id 3da2b9ca97684916b75c4013f95d18ab, owner IMF-portwatch_imf_dataviz) points
  `licenseInfo` at **imf.org/external/terms.htm**, "Copyright and Usage", effective
  **2020-01-02**, final section (special terms for statistical Data). Verbatim:

  > "Users may download, extract, copy, create derivative works, publish, distribute, and sell
  > Data obtained from IMF Sites, including for commercial purposes"

  subject to attribution **"Source: International Monetary Fund"**, no alteration of the data's
  integrity, and disclosure that the data is freely available if it is resold.
  **Provenance of this quote, stated plainly:** it was read from the source and verified by Joe
  via Cowork on 2026-09-02. This session could not retrieve that page itself — `requests`
  returned HTTP 403 (Cloudflare challenge) and the fetch tool returned an empty body on two
  further attempts. The quote is first-hand to the ruling and second-hand to this session; the
  loader did not verify it.
- **The one limit.** Section VIII covers Data the IMF owns; PortWatch's upstream inputs are
  third-party AIS. So only the **published daily aggregates** are committed — the transit counts
  and capacity figures the API serves — and no vessel-level upstream data is fetched or stored.
- Attribution carried in each series' notes and required on any surface:
  **"Sources: UN Global Platform; IMF PortWatch (portwatch.imf.org)."**
  → **seeded 2026-09-02**: 21 series (7 chokepoints × n_tanker, n_total, capacity_tanker),
  2,799 rows each, so a fresh clone reproduces them offline.
- Loaded today (full history, 7 chokepoints × n_tanker, n_total, capacity_tanker):
  `portwatch.<slug>.<field>`, 2019-01-01 → 2026-08-30, 2,799 rows each (the four
  pre-existing slugs were backfilled from 132 rows; malacca/panama/bosporus are new).
- **Pre-2019 chokepoint flows: no free daily source exists** (as WORLD_STATE_SOURCES
  already records). GAP.

### Suez Canal Authority monthly transits — VERIFIED as available, NOT LOADED this pass
- suezcanal.gov.eg Navigation Statistics: the interactive report widget hung on a
  loading spinner (checked twice); the annual Navigation Reports PDFs 2008–2025 are
  downloadable (2025.pdf, 954,750 bytes, text-extractable, not scanned): Table 1
  yearly vessels & net tonnage 1975–2025; Table 2 monthly vessels/net tonnage for the
  current and prior year only; Table 3 by ship type (tankers, LNG, …); Table 4 cargo by
  direction. A monthly series needs every year's PDF stitched (each carries 2 years).
  No terms-of-use page found (footer copyright only). → registered as a **GAP: parseable
  but not loaded**; a stitched loader is a later brief.

### JODI-Oil — VERIFIED format, licence NOT FOUND, NOT LOADED
- jodidata.org/oil/database/data-downloads.aspx (opened): "Complete data series for all
  products, flows and countries, from January 2002 to one month-old can be downloaded,
  for free". The bulk `world_ext.zip` (16,014,495 bytes) is **Beyond 20/20 `.ivt`, not
  CSV**. Per-year CSVs exist (SDMX long format: REF_AREA, TIME_PERIOD, ENERGY_PRODUCT,
  FLOW_BREAKDOWN, UNIT_MEASURE, OBS_VALUE, ASSESSMENT_CODE; primary products CRUDEOIL,
  NGL, OTHERCRUDE, TOTCRUDE; flows INDPROD, REFINOBS, CLOSTLV, TOTIMPSB, TOTEXPSB, …;
  118 reporters in 2002, 96 in the partial 2026 file). Update "on or around the 20th
  of each month"; last refresh 2026-08-20 (June 2026 data).
- Licence: **no licence or terms page exists on the site** — only "freely available" and a
  `© Copyright JODI 2026` footer. **Joe's Ruling 2 (2026-09-02): option (a) — load it, but read
  "freely available" as ACCESS, not RIGHTS.** The per-year CSVs are loaded **refresh-only**:
  pulled live into the local DB, **never seeded, never committed, never redistributed**, cited
  as *JODI-Oil* with the retrieval date carried in each observation's `retrieved_at`.
- **A trap in the file that would have poisoned the data, found before loading.** JODI reports
  every (country, product, flow, month) in **five unit rows** — CONVBBL, KBBL, KBD, KL, KTONS —
  filling the ones a reporter does not submit with `-` or `x`. **CONVBBL is not a volume.** It
  is the country's barrels-per-tonne conversion factor × 1000. Verified on Saudi crude
  production 2026-01: KBBL/KTONS = 313100/42755.7012 = **7.323**, exactly CONVBBL/1000 = 7.323,
  and KBD × 31 = 10100 × 31 = 313100 = KBBL. CONVBBL is populated for **all 96 reporters** while
  real volumes exist for only 56, so a loader taking "whichever unit is populated" would record
  **Russia's crude production as 7356** and Iraq's as 7430. The loader therefore **pins the unit
  per measure** (KBD for flows, KBBL for stock levels), refuses CONVBBL by raising, and drops
  `-`/`x` rather than zero-filling. A reporter publishing no volume yields an empty series and
  is reported as empty.
- Loaded (`src/ripple_fetch.py`, kind `jodi`): 22 countries × 5 measures — crude production
  (CRUDEOIL/INDPROD/KBD), refinery intake (CRUDEOIL/REFINOBS/KBD), closing crude stocks
  (CRUDEOIL/CLOSTLV/KBBL), crude exports (CRUDEOIL/TOTEXPSB/KBD), total product demand
  (TOTPRODS/TOTDEMO/KBD), from the annual CSVs 2002 → present.
- **None of these is a node in the sealed RIPPLE_REGISTRATION.md Table N**, and none was used in
  the computed study. They are loaded for later work; using one needs a dated amendment first.
- **Load receipt, 2026-09-02** (`--refresh --only jodi.`, ~19 min, 925 MB fetched and discarded):
  **106 of 110 series loaded, 27,400 observations, 2002-01 → 2026-06**, 0 seeds written.
  Spot checks against the pinned units: Saudi crude production 2026-01 = **10,100** thousand
  bbl/day, US = **13,246.4**, US closing crude stocks = **676,671** thousand bbl.
  Four series are empty and are reported as empty, not filled: `ru.products_demand`,
  `cn.crude_stocks`, `kz.refinery_intake`, `kz.products_demand`.
- **The coverage fact that matters most, and the proof the unit guard works.** Six reporters
  stopped publishing crude-production VOLUMES while continuing to publish the conversion factor,
  so their series end where the volumes end instead of running on with a number near 7,400:

  | reporter | crude production ends | reporter | crude production ends |
  |---|---|---|---|
  | Iran | 2018-07 | Brazil | 2022-12 |
  | UAE | 2018-12 | Russia | 2023-03 |
  | Qatar | 2018-12 | Iraq | 2024-03 |

  Four of the six are major OPEC producers. Any JODI-based production panel is therefore
  **structurally missing the OPEC core after 2018**, and a loader without the CONVBBL guard
  would instead have shown them reporting continuously to 2026 at implausibly flat values.

### OPEC MOMR — VERIFIED access, restrictive terms, NOT LOADED
- opec.org/monthly-oil-market-report.html (opened in a browser; plain HTTP is a
  Cloudflare challenge): latest MOMR August 2026; PDF download page requires no login
  or registration; the PDF itself was not downloaded (session-token URL). The small
  public appendix workbook (momr-appendix-august-2026.xlsx) holds Tables 11-1…11-5
  (world balance, OECD stocks, non-DoC liquids, rig count) — **the "OPEC crude
  production by secondary sources" table is not in it; which MOMR table holds it was
  not verified.**
- Terms and Conditions (opened): "Users may not reproduce, distribute, display, sell,
  barter, publish, broadcast or otherwise circulate any of the Material to any third
  party"; internal research use "on an occasional and infrequent basis" with
  attribution. → **not loaded; GAP.** Dated OPEC decisions come from the events table
  and from Känzig's announcement dates (CC BY) instead.

## 6. Freight — GAP; equity proxies registered as such

- **Baltic tanker indices (BDTI/BCTI) are licensed, not free. GAP.** Nothing in this
  repo is a freight rate.
- Equity proxies via yfinance (opened via `yf.Ticker(...).info` + `history('max')`),
  all NYQ/USD equities unless noted; labelled **EQUITY PROXY** in the series name;
  Yahoo terms: personal use → **refresh-only, never committed**:

| series_id | ticker | company | first | rows |
|---|---|---|---|---|
| yf.eq_fro | FRO | Frontline plc | 2001-08-06 | 6,305 |
| yf.eq_dht | DHT | DHT Holdings | 2005-10-13 | 5,253 |
| yf.eq_tnk | TNK | Teekay Tankers | 2007-12-13 | 4,708 |
| yf.eq_insw | INSW | International Seaways | 2016-11-16 | 2,460 |
| yf.tankers (existing) | STNG | Scorpio Tankers (product tankers) | 2010-03-31 | 4,131 |
| yf.freight (existing) | BDRY | Breakwave Dry Bulk Shipping ETF (PCX) — dry bulk, not tankers | 2018-03-22 | 2,123 |
| yf.eq_vlo | VLO | Valero | 1982-01-04 | 11,256 |
| yf.eq_mpc | MPC | Marathon Petroleum | 2011-06-24 | 3,819 |
| yf.eq_psx | PSX | Phillips 66 | 2012-04-12 | 3,618 |
| yf.eq_cf | CF | CF Industries | 2005-08-11 | 5,297 |
| yf.eq_ntr | NTR | Nutrien | 2018-01-02 | 2,178 |
| yf.eq_mos | MOS | Mosaic | 1988-01-26 | 9,723 |
| yf.eq_lng | LNG | Cheniere Energy | 1994-04-04 | 8,158 |

(All last 2026-09-02.) An equity proxy responds to the whole equity market as well as
its sector; RIPPLE_REGISTRATION.md requires the S&P 500 (yf.sp500, existing) as a
control for every equity-proxy regression.

## 7. Macro / cross-asset — FRED daily (existing; endpoints re-opened today)

| series_id | what | first | last | rows | note |
|---|---|---|---|---|---|
| fred.T5YIE | 5-year breakeven inflation | 2003-01-02 | 2026-09-01 | 5,921 | Fed, public |
| fred.VIXCLS | CBOE VIX | 1990-01-02 | 2026-09-01 | 9,264 | Cboe via FRED |
| fred.DTWEXBGS | broad USD index (goods & services) | 2006-01-02 | 2026-08-28 | 5,179 | starts 2006. The older DTWEXB (1995-01-04 → 2019-12-31) and TWEXBMTH (1973-01 → 2019-12) are discontinued and on a different methodology: **never spliced.** Pre-2006 dollar control = GAP. |
| fred.BAMLH0A0HYM2 | ICE BofA HY OAS | 2023-09-04 (endpoint) / 2023-07-31 (DB) | 2026-09-01 | 786 | FRED note (opened): "Starting in April 2026, this series will only include 3 years of observations." ICE licence text on the page. **Unusable as a 1990→ control.** The free proxy is yf.hyg (HYG ETF, 2007-04-11 →, existing) labelled ETF proxy; `derived.credit_stress` already exists (2008-10 →). |
| gpr.GPRD / GPRD_ACT / GPRD_THREAT | Caldara–Iacoviello daily GPR | 1985-01-01 | 2026-09-01 | 15,219 | existing (fetch_gpr). Page matteoiacoviello.com/gpr.htm opened today: file data_gpr_daily_recent.xls (columns DAY, N10D, GPRD, GPRD_ACT, GPRD_THREAT, date, GPRD_MA30, GPRD_MA7, event, …), 15,219 rows 1985-01-01 → 2026-09-01 — matches the DB exactly. Licence (quoted from the page): "completely open access under the Creative Commons BY license". |

## 8. Shock series

- **Primary: the events table** — 313 classed, dated events (7 classes:
  chokepoint_disruption 27, conflict_escalation 55, demand_shock 17,
  infrastructure_attack 48, opec_decision 52, policy_response 57, sanctions 57;
  date_precision day 306 / week 2 / month 5; surprise 1–5 coded for 296). Source:
  `data/events.csv` + EVENTS_CODEBOOK.md (two-source rule). In DB.
- **Market-defined alternative: Big Moves onsets** — `data/big_moves/{brent,wti,
  diesel_crack,wti_monthly}.json`, BIG_MOVES_REGISTRATION.md (Amendments 1–3): Brent
  43 episodes 1987-05 →, WTI 46, each with onset/end/sign/attributed events. In repo.
- **External check 1: Känzig (2021) oil supply news** — VERIFIED, seeded (CC BY 4.0,
  repo README: "The data are licensed under the Creative Commons Attribution 4.0
  International License"). File oilSupplyNewsShocks_2025M12.xlsx (110,802 bytes),
  sheets `Daily (pre-Covid)`, `Monthly (pre-Covid)`, `Daily`, `Monthly`. Loaded:
  kanzig.surprise_daily_pc (PC of 1M–12M WTI futures surprises on OPEC announcement
  days; 169 rows 1983-07-19 → 2025-12-01), kanzig.surprise_monthly (612 rows 1975-01 →
  2025-12; zero before 1983-04 by construction), kanzig.news_shock_monthly (VAR-
  extracted shock, 612 rows). Cite Känzig (2021) AER 111(4), DOI 10.1257/aer.20190964.
  Update cadence per README: about every six months, 4–5 month lag.
- **External check 2: Baumeister & Hamilton (2019) structural shocks** — VERIFIED,
  refresh-only. sites.google.com/site/cjsbaumeister/datasets (opened): "Monthly
  Structural Oil Supply Shocks" and "Monthly Structural Oil Demand Shocks", 1975M2 →
  2026M3, "Next update: October 2, 2026"; Google Drive xlsx files downloaded (28,169 and
  48,233 bytes). Columns: supply file `date, oil supply shocks`; demand file `date,
  economic activity shocks, oil consumption demand shocks, oil inventory demand shocks`;
  in-sheet note "Estimates are posterior medians." + the AER citation. **No licence
  text anywhere** → loaded live as bh.* (614 rows each, 1975-02-01 → 2026-03-01), not
  committed.

## 9. Gap register (one line each; none of these is a number anywhere)

| need | status | what would close it |
|---|---|---|
| JKM daily LNG | Yahoo instrument unverifiable (ALTSYMBOL, no name/currency) | a named JKM source; until then Pink Sheet LNG Japan monthly |
| Baltic tanker freight (BDTI/BCTI) | licensed, not free | none at $0; equity proxies labelled as such |
| Pre-2019 chokepoint transits | no free daily source | none; annual EIA factsheets only |
| Suez monthly transits | annual PDFs 2008–2025 parseable; widget broken | stitched PDF loader (later brief) |
| JODI-Oil | ~~gap~~ **RULED 2026-09-02 (a)**: loaded refresh-only, never redistributed | closed; a licence page would allow seeding |
| OPEC MOMR secondary-sources production | access verified; terms forbid redistribution; table not located | not loaded; Känzig dates + events table stand in |
| Broad USD before 2006 | DTWEXB/TWEXBMTH discontinued 2019, different method | none; dollar control starts 2006 |
| HY OAS before 2023 | FRED window cut to 3 years (ICE licence) | yf.hyg 2007→ as labelled proxy |
| IMF PortWatch terms text | ~~gap~~ **READ 2026-09-02** (Joe/Cowork; this session still gets 403): redistribution permitted with attribution → seeded | closed; daily aggregates only, AIS inputs third-party |
| TTF unit | Yahoo states currency EUR, not the unit | treat as EUR/MWh by contract convention, labelled inferred |

## 10. What was opened today (receipt list)

Pages: FRED series pages DGASNYH, DJFUELUSGULF, DCOILBRENTEU, BAMLH0A0HYM2 and
fred.stlouisfed.org/legal; FRED CSV endpoints for all 13 FRED ids above; EIA
LeafHandler pages for WPULEUS3, WCESTUS1, WDISTUS1, WGTSTUS1, WCRIMUS2 and
eia.gov/about/copyrights_reuse.php; worldbank.org/en/research/commodity-markets and
data.worldbank.org/summary-terms-of-use; the PortWatch FeatureServer (fields, distinct
names, Hormuz min/max) and the ArcGIS item metadata; jodidata.org downloads/overview
pages; opec.org MOMR page, download page, appendix workbook and terms; Suez Canal
Authority statistics page and 2025 annual report; Yahoo quote data via yfinance for 15
symbols and yfinance's README; github.com/dkaenzig/oilsupplynews (README + xlsx);
sites.google.com/site/cjsbaumeister/datasets (+ two xlsx); matteoiacoviello.com/gpr.htm
(+ daily xls). Files downloaded: the five EIA workbooks, the Pink Sheet, the Känzig
workbook, both Baumeister workbooks, the GPR daily workbook, JODI world_ext.zip and
four annual CSVs, the MOMR appendix, the Suez 2025 PDF, six FRED CSVs.

## 11. Priced-in inputs (Session C, C-5) — verified 2026-09-02 19:48–19:56 UTC

### CFTC Commitments of Traders — VERIFIED (index page opened; five zips downloaded and parsed), seeded
- Index: cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm.
  Files actually downloaded and parsed: `fut_disagg_txt_2026.zip` (9,217 rows, 2026-01-06 →
  2026-08-25), `fut_disagg_txt_2010.zip`, `fut_disagg_txt_hist_2006_2016.zip` (70,199 rows,
  2006-06-13 → 2016-12-27; **the name without `_hist_` 404s**), `deacot1986_2016.zip`
  (146,677 rows, 1986-01-15 → 2016-12-27), `deacot2026.zip`. 191 columns (disaggregated),
  128 (legacy); category columns as used by the loader are named in `src/ripple_fetch.py`
  (`Swap__Positions_Short_All` carries CFTC's own double underscore).
- Contract keys: **WTI = code 067651** — its name changed from "CRUDE OIL, LIGHT SWEET - NEW
  YORK MERCANTILE EXCHANGE" (2006–2016 files) to "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE"
  (2026 file); the loader joins on the code, never the name. **ICE Futures Europe Brent does
  not appear in the CFTC files under any name** (every Brent-named contract is NYMEX or ICE
  Futures Energy Div). The nearest continuous series is **code 06765T, "BRENT (CRUDE OIL) LAST
  DAY - NEW YORK MERCANTILE EXCHANGE", 2011-10-18 →**, a cash-settled NYMEX look-alike; loaded
  and labelled **PROXY**, and the ICE Brent COT is a **GAP**.
- Definitions (DisaggregatedExplanatoryNotes, opened): Producer/Merchant/Processor/User,
  Swap Dealer, Managed Money ("a registered commodity trading advisor (CTA); a registered
  commodity pool operator (CPO); or an unregistered fund identified by CFTC"), Other
  Reportables. Release (ReleaseSchedule page): "released at 3:30 p.m. Eastern time… usually
  released on Friday. The release usually includes data from the previous Tuesday."
  → knowability lag: Tuesday positions are knowable from Friday 15:30 ET (+3 days).
- Licence (cftc.gov/webpolicy, opened): "Government information at the CFTC website is in
  the public domain… it is requested that in any subsequent use the CFTC be given
  appropriate acknowledgement." → seeded.
- Loader run 2026-09-02 19:56 UTC: 22 series ok, 0 failed, 11 files (bundle + 2017–2026):

| series_id (weekly, Tuesday-dated, contracts) | first | last | rows |
|---|---|---|---|
| cftc.wti_{mm_long, mm_short, mm_spread, pm_long, pm_short, swap_long, swap_short, oi} | 2006-06-13 | 2026-08-25 | 1,055 each |
| cftc.brent_nymex_{same eight} — PROXY (06765T), not ICE Europe Brent | 2011-10-18 | 2026-08-25 | 765 each |
| cftc.wti_legacy_{noncomm_long, noncomm_short, noncomm_spread, comm_long, comm_short, oi} | 1986-01-15 | 2026-08-25 | 1,930 each |
| cftc.mm_net_wti (existing, fetch_cot.py; = mm_long − mm_short) | 2006-06-13 | 2026-08-25 | 1,055 |

### FRED OVXCLS — VERIFIED (CSV endpoint + series page opened); existing series
- Cboe Crude Oil ETF Volatility Index, daily close; endpoint 5,039 rows 2007-05-10 →
  2026-09-01; in DB as `fred.OVXCLS` (4,861 rows, same range; the difference is FRED's "."
  rows). Page note: "Copyright, 2016, Chicago Board Options Exchange, Inc. Reprinted with
  permission." → used as loaded; not re-seeded (already served by the existing loader).

### NYMEX curve RCLC1–4 — already in the state panel (Session A)
- `state_panel` field `curve_m1_m4_spread`, source "EIA NYMEX futures contracts 1-4 (RCLC1..
  RCLC4 daily, ends 2024-04-05)", 1985-01-02 → 2024-04-05, 9,857 rows (WORLD_STATE_SOURCES
  §3 already records the page and the 2024-04-05 end). Not reloaded here. 2024-04 → is a
  GAP for the curve unless a labelled CME/yfinance continuous feed is added (never spliced).
