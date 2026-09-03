# Tier 3 — Structural limits on interpretation

*Not defects. Boundaries on what the evidence can support. Disclose them; do not attempt to fix
them.*

| # | limit | evidence |
|---|---|---|
| **C1** | **The state vector is macro-financial, not fundamental.** The "physical" block is three price-derived fields (inventory sigma, diesel crack, Brent–WTI spread). Absent: OECD days of cover, non-OPEC supply growth, demand growth, floating storage, rig counts, spare capacity. With 772 series available this was a design choice, not a data constraint. | `grid/price/summary.json` `registered.blocks` |
| **C2** | **The reference class spans incommensurable regimes.** 8 events precede 1983 (no NYMEX crude futures); 78 precede 2010 (pre-shale); **150 of 313 fall in the 2020s**. Retrieving a 1979 analog for a 2024 event assumes price formation is stable across the introduction of futures markets, the SPR, financialisation and shale. Nothing in the design tests this — and it is at least as plausible an explanation of the null as §1.1's three conditions. | `oil.db events` |
| **C3** | **The escalation target is a political-science construct, not the economic question**, yet carries most of the apparatus. | paper §§5, 8, 11 |
| **C4** | **`policy_response` is a 57-event heterogeneous class** — the second largest. Large heterogeneous classes absorb noise and dilute real effects. | `oil.db events` |
| **C5** | **Only 4 of 7 classes are G-scorable** (`similarity.py:46` `GEO_TYPES`), so every escalation result describes a subset of the corpus. | code |
| **C6** | **106 skip/xfail markers** across the suite. | `tests/` |
| **C7** | **The corpus inclusion rule is not in this repository.** `EVENTS_CODEBOOK.md` lives in the adjacent repo. An auditor of *this* tree cannot check what qualified an event for admission. | absent |
