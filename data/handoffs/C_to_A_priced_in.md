# Handoff C → A (2026-09-02): priced-in inputs loaded (C-5) — series ids and shape

Verified and loaded by Session C per R2 rules (RIPPLE_SOURCES.md §11 written first; loader
`src/ripple_fetch.py`, kinds `cftc_disagg` / `cftc_legacy`; seeds under `data/seed/ripple/`
with sha256 in `MANIFEST.json`; tests `tests/test_ripple_fetch.py::test_c5_*` on real slices).
All in `observations` (series_id, obs_date, value, as_of = obs_date, retrieved_at); weekly,
**Tuesday-dated**; unit = contracts. Knowability: a Tuesday value is public from the
following Friday 15:30 ET (CFTC release schedule) → for point-in-time use, shift by +3
calendar days (state at date t uses the last Tuesday ≤ t − 3).

## Series (22 new + 2 existing)
| series_id | what | first | last | rows |
|---|---|---|---|---|
| cftc.wti_mm_long / _mm_short / _mm_spread | managed money long / short / spreading, NYMEX WTI 067651 (disaggregated futures-only) | 2006-06-13 | 2026-08-25 | 1,055 |
| cftc.wti_pm_long / _pm_short | producer/merchant/processor/user long / short | 2006-06-13 | 2026-08-25 | 1,055 |
| cftc.wti_swap_long / _swap_short | swap dealer long / short | 2006-06-13 | 2026-08-25 | 1,055 |
| cftc.wti_oi | open interest (all) | 2006-06-13 | 2026-08-25 | 1,055 |
| cftc.brent_nymex_{mm_long, mm_short, mm_spread, pm_long, pm_short, swap_long, swap_short, oi} | **PROXY**: NYMEX "Brent Last Day" 06765T — ICE Futures Europe Brent is NOT in the CFTC files (GAP) | 2011-10-18 | 2026-08-25 | 765 |
| cftc.wti_legacy_noncomm_long / _short / _spread | legacy futures-only, non-commercial long / short / spreading, WTI 067651 | 1986-01-15 | 2026-08-25 | 1,930 |
| cftc.wti_legacy_comm_long / _short | legacy commercial long / short | 1986-01-15 | 2026-08-25 | 1,930 |
| cftc.wti_legacy_oi | legacy open interest (all) | 1986-01-15 | 2026-08-25 | 1,930 |
| cftc.mm_net_wti (existing, fetch_cot.py) | managed-money net long = mm_long − mm_short | 2006-06-13 | 2026-08-25 | 1,055 |
| fred.OVXCLS (existing) | Cboe crude oil ETF volatility index, daily close | 2007-05-10 | 2026-09-01 | 4,861 |
| state_panel `curve_m1_m4_spread` (existing, Session A) | NYMEX RCLC1–RCLC4 term spread, daily; ends 2024-04-05 (EIA stopped) | 1985-01-02 | 2024-04-05 | 9,857 |

## Derived fields Session A may build from these (suggested names; mechanism strings required by CLAUDE.md)
- `positioning.mm_net_wti_pct5y` — managed-money net long (mm_long − mm_short) as a 5-year
  percentile; already exists as `derived.cot_pct` from cftc.mm_net_wti (2007-06 →).
- `positioning.mm_net_oi_share` — (mm_long − mm_short) / oi; scale-free crowding measure.
- `positioning.noncomm_net_wti_legacy` — (noncomm_long − noncomm_short), 1986 →: the only
  positioning series that reaches 1990/1991 and 2001–2005; **not comparable in level** to
  the disaggregated managed-money series (different category definitions; both exist over
  2006–2026 so a splice test is possible but must be labelled).
- `positioning.pm_net_wti` — producer/merchant net (hedging pressure).
- OVX percentile: `derived.ovx_pct` already exists (2008-05 →).

## Rules that travel with the data
Join on contract CODE (067651 / 06765T), never on the name (WTI was renamed to
"WTI-PHYSICAL" between 2017 and 2026). The Brent proxy must be printed as "NYMEX Brent Last
Day (COT proxy)", never as "ICE Brent positioning". Seeds are public domain (CFTC web policy
quote in RIPPLE_SOURCES.md §11); refresh with `python3 src/ripple_fetch.py --refresh --only cftc.`.
