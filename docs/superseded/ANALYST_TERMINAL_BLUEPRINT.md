# The Analyst Terminal — Blueprint

**A job-grade instrument for a geopolitical war-&-conflict-to-markets analyst.**
Eyes on everything; oil & commodities sharpest; live; engine-powered so it eventually
*anticipates* rather than reports. This document is the deeply-researched plan. It is
built from four verified research sweeps (conflict/foreign-policy data, oil/energy/
commodity physical data, market data + the analyst job, and the oil-propagation map).
Every data source named here was verified to exist and to be free/low-cost as stated,
with honesty flags carried through.

Build discipline is non-negotiable and stated once: **foundation-first, one solid brick
at a time** (see `memory: foundation-first-no-premature-scaling`). Sprawl killed the
predecessor. Each brick ships, is trusted, then the next goes on top.

---

## 0. Why this is worth finishing (the honest motivation)

The research into the *job* is unambiguous: the decisive, scarce portfolio artifact is a
**backtested event→price product + pre-registered falsifiable calls + a Brier-scored
track record, in Python, around a niche.** This engine already is that. So every brick
below serves two ends at once: it makes the terminal more useful *and* it hardens the
one artifact that gets Joe hired. Niche = **conflict/energy transmission to markets.**

---

## 1. The four-layer architecture

```
  SENSE  ─────────►  CORROBORATE  ─────────►  REASON  ─────────►  SURFACE
  (ingest, free)     (triangulate)            (the engine)        (OpenBB + voice)

  GDELT firehose     weight-of-evidence       propagation graph   map-centric cockpit
  UCDP verified      independent-source dedup  situations memory   narrated analyst read
  sanctions feeds    cross-modal votes         event study (H1-3)  (caged LLM prose)
  EIA/FRED/PortWatch (news+physical+thermal)   ACH hypotheses      pre-registered calls
  GPR signal         confidence tags           prediction/odds     Brier calibration
  prediction markets                           nowcast/anticipate
```

The engine already implements the spine of this (situations, corroboration brain,
event study, prediction-market adapter, calibration). The blueprint's job is to widen
**SENSE**, deepen **REASON** with the propagation graph, and finish **SURFACE** as a
map-centric terminal.

---

## 2. SENSE — the verified free data stack (what to wire, in order)

All verified July 2026. "Wire order" = foundation-first priority. Flags are real.

### Tier 1 — the load-bearing free core (wire first)
| Source | Gives | Access | Cadence | Flag |
|---|---|---|---|---|
| **EIA API v2** | crude/gas prices, **inventories**, refinery, SPR | free key, JSON | weekly/daily | US-centric; 5,000-row cap |
| **FRED** | Brent/WTI/HH, Treasury curve, FX, **VIX**, credit-spread indices | free key | daily EOD | ICE BofA OAS may be capped to ~3-yr window — verify live |
| **CFTC COT** | weekly futures positioning | free, no key | weekly (3-day lag) | **already integrated** |
| **IMF PortWatch** | **28 chokepoints** (Hormuz/Suez/Bab-el-Mandeb…), 2,065 ports | keyless ArcGIS REST | **weekly (Tue)** | model-estimated; lags fast breaks up to a week; **already integrated** |
| **GDELT 2.0** | real-time world events + tone, geolocated | 15-min CSV / DOC API (keyless) | **15 min** | media-*claim* not fact; noisy — tag `claim` |
| **GPR Index** (Caldara-Iacoviello) | the canonical geopolitical-risk gauge; Threats vs Acts; country-level; daily variant | free download, no auth | monthly + daily | media-bias; the Fed's own benchmark — high credibility |

### Tier 2 — the verified-fact & sanctions backbone
| Source | Gives | Access | Flag |
|---|---|---|---|
| **UCDP GED** | fatality-verified conflict events, georeferenced | free REST + bulk, **CC BY 4.0** | monthly candidate ≤1-mo lag — the corroboration anchor vs GDELT noise |
| **OFAC SDN + CSL + EU FSF + UK FCDO** | sanctions/export-control designations = dated state actions | free (CSL needs free key) | UK OFSI list **closed 28 Jan 2026** → use FCDO; each designation a clean `fact` |
| **NASA FIRMS** | satellite thermal (strike/fire proxy) | free MAP_KEY, CSV, ~3h | heat≠intent; corroboration only; **already integrated** |
| **Prediction markets** (Kalshi, Polymarket) | market-implied event odds ("what's priced") | public read free | Kalshi US-legal + documented limits; Polymarket US-trading in flux; **Polymarket already integrated** |

### Tier 3 — the dependency-tracing kit (powers "everything oil touches")
| Source | Gives | Access | Flag |
|---|---|---|---|
| **USGS Mineral Commodity Summaries** | net-import-reliance % + source countries, ~90 minerals (helium, PGMs, REE, gallium…) | free PDF + bulk | US-centric, annual — the reliance backbone |
| **UN Comtrade / BACI (CEPII)** | bilateral HS-6 trade → concentration/HHI, who depends on whom | free (registration) | BACI pre-reconciles mirror flows — preferred for concentration math |
| **OECD ICIO / TiVA** | inter-country input-output → upstream/downstream propagation | free CSV | sector-level (45 industries), 2–3 yr lag |
| **GIE AGSI+/ALSI, ENTSOG** | European gas storage & flows (where gas shocks show first) | AGSI free key; ENTSOG keyless | 60-call/min & 60-sec query limits |

### Deprioritize / handle with care (honest)
- **ACLED** — best curated events, but on a personal email the engine likely gets
  **aggregated-only** access (no event-level API since the Sept-2025 tiering). UCDP +
  GDELT cover the same ground free at event level. Wire only with institutional/paid.
- **OpenSanctions** — great free aggregator but **CC BY-NC**; if this ever commercializes
  the NC clause bites — build sanctions on the primary government feeds as system-of-record.
- **AIS live tanker feeds** (AISStream free/no-history; TankerMap unofficial no-SLA) —
  enrichment, not core. **PortWatch is the trusted chokepoint base.**
- **Vessel-level tanker tracking with history** (Kpler/Vortexa/Spire) is the one genuinely
  paid capability with no free substitute — deferred by choice, not needed for the foundation.

---

## 3. REASON — the propagation graph ("everything oil touches")

This is the signature capability and the thing Joe described (helium facility → helium is
a small semiconductor input → chip production slows). The research produced a fully-sourced
map. It has two geometries:

**A. Bulk cost chains** (price pass-through; fast at top, slow/partial at consumer):
- crude → refined products (**crack-spread amplification** — products spike *more* than
  crude when refining is tight) → diesel→freight→goods, jet→airfares, gasoline→CPI.
- **natural gas → ammonia (>70% of variable cost) → nitrogen fertilizer → food** (Europe
  is the marginal, first-to-close producer; 2022: ~50% of EU ammonia capacity offline).
- naphtha/ethane → petrochemicals (ethylene/propylene) → plastics, packaging, PVC/construction.

**B. Chokepoint chains** ("small input, big consequence" — price fires in weeks, replacement
takes years; the tradeable asymmetry). The ranked watchlist (trigger → choke → downstream):

| # | Choke (tiny input) | Trigger geography | Downstream gated | Live-ness |
|---|---|---|---|---|
| 1 | Heavy rare earths (Dy/Tb) separation | China ~99% | EV motors, wind, **missiles/F-35** | active license campaign thru 2025 |
| 2 | Gallium (GaN) | China ~99% | military AESA radar, EW, 5G | ban suspended Nov-2025, licensing remains |
| 3 | Semi-grade neon | Ukraine ~50% chip-grade / Russia feedstock | **all DUV chip lithography** | war-zone; buffered by inventory depth |
| 4 | Palladium | Russia ~40% | gasoline autocatalysts | sanctions/airspace-sensitive |
| 5 | Antimony | China ~48% | **munitions**, flame retardant, solar glass | +157% into 2025; suspended Nov-2025 |
| 6 | Platinum | S.Africa ~70% | diesel catalysts, **H₂ fuel cells** | SA grid risk |
| 7 | Germanium | China ~60% | **night-vision/IR optics**, fiber | same package as gallium |
| 8 | Tungsten | China ~80%+ | AP penetrators, **all carbide tooling** | Feb-2025 license controls |
| 9 | Helium (Grade-A) | Qatar ~⅓ / Russia Amur / US reserve sold | chip fabs + **MRI** | 2026 Qatar outage developing |
| 10 | Cobalt | DRC ~76% / China refine | EV/electronics batteries | DRC ban 2025; **LFP substitution caps it** |
| 11 | Gas→ammonia | Europe marginal / Russia | **global food prices** | watch TTF–Henry Hub spread |
| 12–18 | Niobium (Brazil ~90%), Graphite (China >90% anode), Tantalum (DRC), Hafnium, Indium/Tellurium (China ~70%), diesel refining, ethane/naphtha | — | superalloys, anodes, avionics, jet blades, displays/solar, freight-inflation, plastics | mixed |

**The meta-signal (carried from research):** in every China case the **price front-ran the
outright ban by 12–16 months via the *licensing* phase — the licensing announcement is the
tradeable moment.** And the binding variable for neon/helium is **inventory depth × sourcing
diversity, not headline supply share** — "new regime / no clean analogue" is a valid engine
output. This is exactly the anticipation edge the engine should encode.

Engine encoding: a sourced `propagation.yaml` (each chain: trigger geography, choke, share,
downstream market, mechanism, lag, free observing series, historical episode) + a module that,
given the **active situations**, surfaces which chains are live — extending the criticality
arm from a flat map into a directional transmission graph. **This is Brick 1.**

---

## 4. SURFACE — the map-centric terminal

Organizing model = **the map**, not a flat table (Joe's frame: satellite-style, weighted by
importance). Nodes = chokepoints + oil ports, **sized by barrels/day** (Hormuz ~20 Mb/d = the
brightest point). Edges = tanker lanes. Live layers = PortWatch transit anomaly + FIRMS fires
+ active-situation overlay + the propagation chains that geography triggers. Free to draw:
**Plotly map inside OpenBB** (OpenStreetMap tiles, no token) first; **Kepler.gl** (now on
MapLibre, no Mapbox token) as the richer arcs/time-playback upgrade later.

Above the map, the **narrated analyst voice** — the "Cramer-for-geopolitics" read — written
by the **caged LLM from deterministic engine fields only** (never inventing numbers), plus the
**pre-registered call + Brier calibration** panel that makes it a portfolio piece.

Every field wears its `as_of` timestamp; each layer refreshes at the fastest cadence its
source honestly supports (structural yearly, exposure/price every loop run). Nothing fakes
freshness. The autonomous GitHub Actions loop already re-runs the engine free, no machine on.

---

## 5. Foundation-first build roadmap (bricks, in order)

1. **Propagation graph** — `data/propagation.yaml` (sourced chains above) + `src/propagation.py`
   (active-situation → live chains) + surface widget + tests. *The "everything oil touches"
   engine.* Builds on the trusted criticality/situations base. ← **START HERE**
2. **GPR signal** — wire the Caldara-Iacoviello index as the canonical conflict-risk gauge
   (free, no auth) into observations; show it against Brent/VIX. Small, canonical, high-signal.
3. **The oil map** — `data/oil_map.yaml` (chokepoint/port geography, barrels/day) + Plotly
   map widget overlaying PortWatch + FIRMS + situations we already collect.
4. **Verified-fact backbone** — UCDP GED adapter (CC BY 4.0) as the corroboration anchor;
   then sanctions feeds (OFAC/CSL/EU/UK) as dated `fact` observations.
5. **GDELT firehose** — the 15-min real-time event front-door, tagged `claim`, corroborated
   against UCDP.
6. **Deepen anticipation** — propagation-aware nowcast, licensing→ban lead-time detector,
   inventory-buffer "new regime" flagger; widen the pre-registered calls + Brier record.
7. **Kepler upgrade + narrated voice polish** — route arcs, time-playback; the analyst read
   and calibration panel as the finished portfolio surface.

## 6. Standing constraints (from canon, restated)
- Engine core stays **free/local/reproducible**; paid platform only by Joe's explicit choice.
- LLM = **extraction + prose only**, never scoring/update/gap-fill/probability math.
- **Never blend** `observed`/`claim`/`nowcast`/`inferred`; every observation carries
  `source_url` + `retrieved_at`; typed buckets, not invented decimals.
- Pre-registration is binding; point-in-time discipline; null results reported, not buried.
- One canonical DB (`data/oil.db`); new data = new rows via small adapters; no parallel DBs.
