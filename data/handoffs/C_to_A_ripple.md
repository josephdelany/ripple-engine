# Handoff C → A (2026-09-02): the ripple outputs and what the Story page may say

Session C built the ripple study (brief R; RIPPLE_SOURCES.md, RIPPLE_REGISTRATION.md
+ Amendments A/B, src/ripple_fetch.py, src/ripple_lp.py, src/ripple_big_move_order.py).
This note is the wiring contract for Session A (C-7). Nothing here is a finding; the
findings are in `data/ripple/SUMMARY.md` (mirrored at `RIPPLE_SUMMARY.md`).

## 1. `data/ripple/irf.json` — shape

```json
{
 "meta": {"when": "...", "registration": "RIPPLE_REGISTRATION.md cbf4fdc + A, B", "seed": 19900802,
          "n_placebo": 500, "daily_T": 9963, "shock_counts_daily_deoverlapped": {"chokepoint_disruption": 21, "...": 0},
          "runtime_s": 90.5},
 "rows": [
  {"node": "heating_oil_nyh", "series_id": "fred.DHOILNYH", "hop": 1, "freq": "daily", "transform": "log",
   "shock": "tightening",              // one of the 7 classes | all | tightening | bigmove_up | bigmove_down
   "spec": "total",                    // total | crude_conditioned   (primary = total)
   "sample": "full", "headline_h": 20, "n_events": 47,
   "irf": [{"h": 0, "beta": 0.41, "se_ehw": 0.3, "se_nw": 0.3, "lo95": -0.2, "hi95": 1.0, "lo90": ..., "hi90": ...,
            "z_ehw": 1.3, "p_ehw": 0.19, "nw_covers_zero": true, "ehw_covers_zero": true, "n_events": 47, "T": 8900},
           ...],                        // h in {0,1,2,5,10,20,40,60} daily; {0,1,2,4,8,13,26} weekly; {0,1,2,3,6,9,12} monthly
   "placebo": {"beta_real": ..., "pseudo_p2_5": ..., "pseudo_p97_5": ..., "percentile": 100.0, "beyond_state": true,
               "n_pseudo": 500, "buckets_fallback_to_vix_only": 0, "n_events_matched": 45, "n_events_unbucketed": 2}
               | null,                   // null when n < 15 or spec != total or a Big Moves shock
   "verdict": "TRANSMITTING" | "NULL" | "INSUFFICIENT" | null,   // Amendment B rule; null for non-verdict rows
   "fragile": false,                    // EHW and Newey-West disagree on zero coverage (counted as NULL)
   "bh_q10_reject": false               // Benjamini-Hochberg q=.10 within the node's 9-shock family at headline_h
  }
 ]
}
```
Units: `transform` log → β in % of the node; `pp` → percentage points; `lvl` → the series
unit (cracks USD/bbl; spread USD/bbl). `n_events` = de-overlapped events with the dummy on
inside the estimation sample at that horizon. Companion files with the same row shape:
`retraction_six.json` (`sample` = "vix_ge_median", plus a `status` map), `regimes.json`
(`sample` = "pre_2009-02-06" | "post_2009-02-13").

## 2. `data/ripple/passthrough.json` — shape (§2.6, the crude→product sign split)

```json
{"meta": {...}, "note": "slope-based symmetry test (Kilian & Vigfusson 2011 caveat ...)",
 "daily_spot": [{"node": "gasoline_gulf", "h": 20, "beta_plus": 1.258, "beta_minus": 0.173, "se_plus": ..., "se_minus": ...,
                 "W": 1.085, "z_W": 3.26, "p_W": 0.0011, "asymmetric_at_5pct": true, "T": 8900}, ...],
 "weekly_retail": [{"node": "retail_gasoline_GASREGW", "h_weeks": 4, "beta_plus": 0.379, "beta_minus": 0.473, "W": -0.094,
                    "z_W": -1.05, "p_W": 0.296, "increases_pass_faster": false, "asymmetric_at_5pct": false, "T": 1800}, ...]}
```
β⁺ = % move in the product per 1% Brent *increase* on day t, cumulative to h; β⁻ the same
for decreases (entered together, never censored). W = β⁺ − β⁻; a positive significant W
means increases pass through faster/further.

## 3. The two sentences the Story page may print (verbatim templates; fill from irf.json)

For a class with at least one TRANSMITTING hop (rows where `shock == <class>`, `spec == "total"`,
`verdict == "TRANSMITTING"`), one sentence per transmitting node, most-upstream hop first:

> "Across {n_events} {class_label} events since 1990, {node_label} moved {beta:+.1f}{unit} over the
> {headline_h} trading days after the event (95% band {lo95:+.1f} to {hi95:+.1f}), which is outside
> what {n_pseudo} matched quiet-market days of the same VIX and geopolitical-risk state produce
> (placebo percentile {percentile}). Registered before computing; {bh_note}."

where `bh_note` = "survives the q=0.10 false-discovery control" if `bh_q10_reject` else
"does not survive the q=0.10 false-discovery control across this node's nine shocks — read it
as one of {k} nominal hits among {cells} cells". `unit` = "%" for log nodes, "pp" for pp,
"$/bbl" for cracks. Never say "causes"; never drop the placebo clause; never print a
TRANSMITTING row whose `fragile` is true (there are none in this run, but the rule stands).

For a class with no TRANSMITTING hop, print exactly one of:

- if every hop is NULL or the class has ≥ 15 events at Brent:
  > "Across {n_events} {class_label} events since 1990, no chain node moved beyond its matched
  > quiet-market baseline at the registered horizons; the Brent response at 5 days was
  > {beta:+.1f}% (95% band {lo95:+.1f} to {hi95:+.1f}). This is a registered null, not an absence
  > of data."
- if the class is INSUFFICIENT at Brent (n < 15):
  > "Insufficient: {class_label} has {n_events} de-overlapped events since 1990, below the
  > registered minimum of 15; no ripple is estimated for this class."

The base-rate clause must accompany any transmitting sentence somewhere on the page:
"{k} of {cells} node×shock cells transmit in this run; between 1 and 24 would be expected if
nothing transmitted at all" (numbers from `SUMMARY.md` Tally; recompute from `rows` if the
file is regenerated).

## 4. The retraction of the six (Amendment B) — for Session A/B to act on
`data/ripple/retraction_six.json` → `status`: five RETRACTED (Brent oil, Heating oil, 5Y
breakeven, S&P 500, Platinum), one RETAINED (Palladium). The `propagation_edges` table was
not edited by Session C. The engine's Story text that cites those edges should stop calling
them validated until A/B rule on the retraction; the per-edge numbers are in `SUMMARY.md`.

## 5. Not to be wired
`bigmove_up` / `bigmove_down` rows (they condition on crude's own move; descriptive),
`crude_conditioned` rows (diagnostic), and every `transit_*` node (2019→, INSUFFICIENT by
construction) — none of these may feed a sentence.
