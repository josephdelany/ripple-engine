# WORLD-STATE SOURCES — verified register (2026-09-02)
*Companion to WORLD_STATE_FRAMEWORK.md. Each entry records what was actually
checked: the page opened, the file offered, its format, the variables that matter
to us, the years covered, the licence, and what block/field it feeds. "Verified"
means the dataset's own page or codebook was read today; "search-verified" means
confirmed from secondary pages only and the loader must re-check on first run.
Nothing below is assumed.*

Legend for the *feeds* column — P physical · M market · A actors · D dyads ·
S system · N narrative.

## 1. Conflict, crisis, escalation (the outcome side of Layer G)

### ICB — International Crisis Behavior, v16 (Duke) — VERIFIED (page + v12 codebook read)
- Page: https://sites.duke.edu/icbdata/data-collections/ — free CSV downloads:
  ICB1 v16 (system level, one row per crisis), ICB2 v16 (actor level), ICB Dyads
  v16, Non-State Actor data (1987→). Coverage 1918–2021: 512 crises, 1,131 crisis
  actors, 1,000 crisis dyads, 39 protracted conflicts. Citation required
  (Brecher & Wilkenfeld 1997/2000; Brecher et al. 2025 codebook v16).
- Variables read from the codebook (system level): `BREAK` trigger type (1 verbal
  … 7 non-violent military act, 8 indirect violent, 9 violent act); `TRIGENT`
  triggering entity (country code / 995 internal / 996 non-state / 997 multi);
  `TRIGDATE`, `TERMDATE`, `BREXIT` duration; `GRAVCR` gravity of threat (0
  economic … 6 existence); `CRISMG` crisis-management technique (1 negotiation …
  8 violence); `CENVIOSY` centrality of violence; `SEVVIOSY`/`VIOL` intensity
  (1 none, 2 minor clashes, 3 serious clashes, 4 full-scale war); `TIMVIO`;
  `IWCMB` intra-war crisis; `NOACTR`; `GPINV`, `USINV`, `SUINV` great-power/US/
  USSR-Russia involvement and effectiveness; `GLOBORG`, `GLOBACTM`, `GLOBEFCT`
  UN organ, content, effectiveness; `REGORG`; `SUBOUT` outcome content
  (ambiguous/definitive); `FOROUT` form (1 formal agreement … 4 unilateral act, 7
  faded); `EXSAT`; `OUTESR` escalation or reduction of tension (recurrence within
  5 years); `GEOSTR` geostrategic salience; `PROTRAC`/`PCID` protracted conflict;
  `POWDISSY` power discrepancy; `ETHNIC`. The codebook itself cites the
  "Basra–Kharg Island 1984" crisis — our tanker-war cases are already in it.
- Feeds: D (crisis history of the dyad, prior outcome), S (great-power and UN
  involvement), and an **independent, professionally coded outcome label** to
  audit our corpus-derived +90d branches against (WALK_FORWARD_PROTOCOL §1).
- Portion of codebook read: variable index in full; value definitions for
  trigger, gravity, management, violence, outcome and tension variables; the
  state-code table. Not read: every illustration paragraph for the remaining
  ~25 variables.

### COW — Militarized Interstate Disputes v5.0 — VERIFIED (page read)
- https://correlatesofwar.org/data-sets/mids/ — "MID 5 Data and Supporting
  Materials.zip" (3.1 MB): MIDA (dispute level, 1816–2014), MIDB (participant),
  MIDI/MIDIP (incident level 1993–2014); Dyadic MID 4.03 (1816–2014). CSV+DTA.
  Free; cite Palmer et al. 2020. Ends 2014 — UCDP/GED and MID incident
  narratives cover after.
- Feeds: D (count, hostility level, last dispute date, fatalities in the dyad).

### COW — National Material Capabilities v7.0 — VERIFIED (page read)
- https://correlatesofwar.org/data-sets/national-material-capabilities/ —
  NMCv7.zip (4.7 MB), CSV/DTA/TXT; 1816–2022; six components (military
  expenditure, personnel, energy consumption, iron/steel, urban pop, total pop)
  + CINC. Free; cite Singer, Bremer & Stuckey 1972. The page warns raw
  components vary in quality across time; use CINC and shares, not levels.
- Feeds: A (capability, capability ratio of the dyad).

### COW — War data (v4.0 inter-state; intra-state v5.1) — search-verified
- https://correlatesofwar.org/data-sets/cow-war/ ; use for wars 1816–2007;
  UCDP covers 1946→ with annual updates, so COW wars are the pre-1946 tail only.

### ATOP — Alliance Treaty Obligations and Provisions v5.1 — VERIFIED (page read)
- http://www.atopdata.org/data.html — atop_5.1__.csv_.zip (2.5 MB), last updated
  Aug 2022; six units of analysis including state-year, dyad-year, directed
  dyad-year; 1815–2018. Free; cite Leeds et al. 2002. Ends 2018 — for 2019→ the
  dossier records alliance state from sources (and ATOP's own future updates).
- Feeds: D (defense pact / neutrality / consultation obligations between the
  pair; shared allies), A (alliance count).

### UCDP — Uppsala Conflict Data Program v26.1 — VERIFIED (page read)
- https://ucdp.uu.se/downloads/ — all CSV, **CC BY 4.0**: UCDP/PRIO Armed
  Conflict (1946–2025, conflict-year), Dyadic (1946–2025), Battle-Related Deaths
  (1989–2025), GED events (1989–2025, geocoded, daily), Candidate events
  (monthly release, ≤1-month lag), Onset, Termination (dates + means of
  termination), External Support (1975–2017: who backed whom), Peace Agreements
  (1975–2021). REST API at ucdp.uu.se/apidocs.
- Feeds: S (active wars, intensity, battle deaths), D (dyad conflict status),
  A (external supporters of actors), and the live side of escalation outcomes
  post-2014 where MID stops.

### CSP/INSCR — Polity5, Coups, MEPV — VERIFIED (page read)
- https://www.systemicpeace.org/inscrdata.html — Polity5 annual 1946–2018
  (p5v2018.xls; pre-1946 values are Polity IV), Coups d'État 1946–2021 (list +
  annual), Major Episodes of Political Violence 1946–2018 (war magnitude scores
  incl. neighbours and regional context), PITF problem set 1955–2018, High
  Casualty Terrorist Bombings 1989–2021. **Licence: copyrighted; reproduction
  or redistribution prohibited without written permission** → load locally,
  never commit the files, cite.
- Feeds: A (regime score, durability, recent coup), S (regional war magnitude).

### V-Dem v16 (March 2026) — VERIFIED (page read)
- https://www.v-dem.net/data/the-v-dem-dataset/ — Country-Year Core/Full (CSV),
  Country-Date; 1789→ present; **CC BY-SA 4.0**. Replaces Polity after 2018
  (indices are not comparable across versions — pin v16).
- Feeds: A (regime indices 2019→; leader-constraint proxies).

### Archigos v4.1 — search-verified
- Leaders 1875–2015 (Goemans, Gleditsch, Chiozza); rochester.edu/…/hgoemans/data.htm.
  Feeds A (leader tenure, entry/exit type, recent change). Post-2015: dossier.

### GSDB — Global Sanctions Data Base R5 — VERIFIED (page read)
- https://www.globalsanctionsdatabase.com/ — 1950–2025, 1,794 cases; case and
  dyadic versions; R5 adds month of imposition/termination; GSDB-FS financial
  subtypes. **By request form only (24h), non-commercial, do not redistribute.**
  → Joe requests with the project title; loader reads the local file; never
  committed.
- Feeds: D (sanctions in force between the pair, type, objective), A (sanctions
  burden on the actor).

### SIPRI — Military Expenditure and Arms Transfers — search-verified (cached page showed 1949–2015; current file runs to 2025)
- https://www.sipri.org/databases/milex — Excel; 1949→; open sources; user terms
  require citation. Arms Transfers database (TIV) 1950→ separately.
- Feeds: A (spending level and trend, share of GDP, arms imports as capacity proxy).

## 2. Geopolitical risk, attention, narrative

### Caldara–Iacoviello GPR — VERIFIED (page read)
- https://www.matteoiacoviello.com/gpr.htm — monthly Excel/Stata (updated 1st of
  month; last 2026-09-01): Recent GPR 1985→ (10 papers) with GPRT threats / GPRA
  acts subindices and **44 country-specific indexes**; **Historical GPRH 1900→**
  (3 papers) with threats/acts and 8 subcategories (war threats, peace threats,
  military buildups, nuclear threats, terror threats, beginning of war,
  escalation of war, terror acts). Daily Recent GPR 1985→ (weekly update).
  Monthly vintages archived (data_gpr_export_YYYYMM.xls) → **true vintages for
  the filtration rule**. **CC BY**.
- Feeds: S (system tension), N (attention, threats vs acts), and per-country
  GPR for actors. The vintage archive makes GPR one of the few narrative
  series we can serve point-in-time honestly.

### GDELT 2.0 (1979→ events; 2015→ GKG) — already in the engine; N.
### NYT Article Search API — NOT verifiable from here (developer.nytimes.com blocked to this sandbox); known: free key, archive 1851→, rate-limited. Loader must test on Joe's machine. Feeds N (what was said the week of the event; per-event dossier queries).

## 3. Physical oil system

### EIA — Global Surplus Crude Oil Production Capacity 1970–2021 — VERIFIED (page read)
- https://www.eia.gov/international/content/analysis/special_topics/Global_Surplus_Crude_Oil_Production_Capacity/
  — annual series built from the 1989 Memo to the Record (1970–88), IEOs
  (1985–2002) and STEO (2003→); figure2.xlsx downloadable; consistent
  "effective capacity" definition; excludes outages/sanctioned volumes. Summary:
  peak 11.3 mb/d in 1985; 1990–2015 peak 5.3; 2020 7.0. Monthly STEO country
  spare capacity 2003→ (STEO tables). Public domain.
- Feeds: P (spare capacity, total/Saudi; the single most important state field).

### EIA — NYMEX futures contracts 1–4 — VERIFIED (page read)
- https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm — daily RCLC1 (1983→),
  RCLC2 (1985→), RCLC3 (1983→), RCLC4 (1985→); heating oil contracts 1980→.
  **Series end 2024-04-05** ("futures prices after April 5, 2024, are not
  available"). Public domain. → Curve structure (M1–M4) 1983–2024 from EIA;
  2024→ from a delayed CME/yfinance continuous-contract feed, labelled as a
  different source, never spliced silently.
- Feeds: M (backwardation/contango at knowability; term spread).

### EIA — International Energy Statistics (API v2) — search-verified
- Monthly production by country (1973→ for many), consumption, imports/exports;
  free API key required (registration). Feeds P.

### EIA — US weekly/monthly stocks, SPR — already partly loaded; P.
### Energy Institute — Statistical Review of World Energy — VERIFIED (page read)
- https://www.energyinst.org/statistical-review/resources-and-data-downloads —
  2026 edition xlsx (14 MB) and Consolidated Narrow-format CSV (19.5 MB) behind
  an email gate; **archive direct links** for 2025 (EI-Stats-Review-ALL-data.xlsx)
  and 2024/2023; annual 1965→: production, consumption, reserves, refinery
  capacity/throughput, trade movements by country. Free public good; cite
  Energy Institute (year).
- Feeds: P (production/consumption/refining/reserves by country, import
  dependence), A (oil dependence of each actor).

### OPEC Annual Statistical Bulletin — search-verified
- PDFs 2014–2025 at opec.org/assets/assetdb/asb-YYYY.pdf; interactive version;
  no clean xlsx found → use EI for panel, OPEC ASB for quota/agreement history
  via the dossier. OPEC conference decisions: Känzig's announcement dataset
  (GitHub dkaenzig/replicationOilSupplyNews, 1983→) for dated decisions.

### Kilian — global real economic activity index — VERIFIED (page read)
- https://sites.google.com/site/lkilian2019/research/data-sets — monthly index
  1968.1→ (corrected), now published monthly by the Dallas Fed (IGREA; also on
  FRED); exogenous OPEC supply-shock series quarterly 1971–2004; oil price
  expectations 3/6/9/12m monthly 1992–2017. Free with citation.
- Feeds: M/S (global demand state at knowability — the demand-shock
  conditioner the corpus lacks).

### IMF PortWatch (2019→ chokepoint transits) — loaded; P. Pre-2019 chokepoint
flows: **no free daily source exists**; EIA chokepoint factsheets give annual
volumes (2011→). Gap stated.
### Tanker freight: Baltic Dirty/Clean indices are licensed (not free);
Clarksons paid. **Gap** pre-2019 for the flow side; stated in every read.

## 4. Market and macro (already largely in the DB)
FRED/ALFRED vintages (rates, curve, dollar, CPI, IP, recessions; VXO 1986→,
VIX 1990→, OVX 2007→), CFTC COT, daily Brent/WTI/products, WTISPLC monthly
1946→. World Bank WDI (oil rents % GDP, 1970→; free API) → A.

## 5. What is genuinely missing (and the honest substitute)
| need | status | substitute / rule |
|---|---|---|
| munitions / ability to respond | no open dataset | SIPRI arms imports (TIV) + NMC military personnel/expenditure as capacity proxies; IISS Military Balance is paid → dossier from dated sources |
| posture / stated intent | no dataset | dossier: verbatim dated statements (NYT archive, GDELT), two sources |
| chokepoint transits pre-2019 | none free | annual EIA factsheet volumes; "unknown" at daily resolution |
| tanker freight pre-1998 / any free daily | none free | "unknown"; flow side = price proxy, labelled |
| monthly spare capacity pre-2003 | annual only | annual value carried within year, labelled "annual" |
| curve structure after 2024-04 | EIA series ended | yfinance CL continuous contracts, labelled different source |
| narrative at the time, pre-1979 | GDELT starts 1979 | GPRH monthly counts 1900→; NYT archive queries per event |
| leaders after 2015 | Archigos ends | dossier |
| alliances after 2018 | ATOP ends | dossier |
| sanctions | request-only | request GSDB R5 (Joe), local only |

## 6. Licences at a glance
Free + redistributable with citation: COW (NMC, MID), ATOP, ICB, UCDP (CC BY),
V-Dem (CC BY-SA), GPR (CC BY), EIA (public domain), Kilian (cite), EI (cite).
Local-only, never committed: Polity/CSP (redistribution prohibited), GSDB
(request, non-commercial), SIPRI (terms), NYT (API terms), EI 2026 file if
obtained through the email gate.

## 7. State at 2001-09-11 — what the framework can put on the screen
From the panel, with vintages ≤ that day: WTI/Brent daily and the NYMEX curve
(RCLC1–4), VIX/VXO, COT, FRED rates/dollar, Kilian index (Aug 2001), EIA spare
capacity (annual 2000/2001), EI production/consumption 2000, SPR level, GPR
monthly to Aug 2001 (Recent + Historical, US/Saudi/Iran/Iraq country indexes),
CINC 2000 for US/Saudi/Iraq/Iran/Afghanistan, Polity 2000, SIPRI 2000, ATOP
alliances in force 2001, MIDs to date, ICB crises to date (incl. Gulf War,
Iraq no-fly, Kharg), UCDP active conflicts 2000, sanctions in force (GSDB) on
Iraq/Iran/Libya, Archigos leaders. From the dossier: US posture statements
that week, Saudi/OPEC statements, tanker-insurance notes — sourced or
"unknown". Then the read, sealed; then the outcome; then the score.
