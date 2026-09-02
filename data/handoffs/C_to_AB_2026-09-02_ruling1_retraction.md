# Handoff C → A and B (2026-09-02): Joe's Ruling 1, the retraction of five edges

Joe ruled on the gate report (`data/gates/ripple_2026-09-02.md`): **retract the five.** This
note is the list, the surfaces that still lean on them, and the one constraint on how palladium
may be spoken about. Session C owns none of the files that need changing, so nothing here is
done by me.

## 1. The five, and the one that stays

| edge (`propagation_edges.to_node`) | re-test at h=20 | verdict | ruling |
|---|---|---|---|
| Brent oil | +0.61% [−4.12, +5.35] n=40 | NULL | **RETRACT** |
| Heating oil | +2.01% [−2.62, +6.63] n=35 | NULL | **RETRACT** |
| 5Y breakeven | −0.06pp [−0.24, +0.12] n=20 | NULL | **RETRACT** |
| S&P 500 | −0.76% [−2.77, +1.25] n=36 | NULL | **RETRACT** |
| Platinum | −1.29% [−5.04, +2.47] n=25 | NULL | **RETRACT** |
| Palladium | −5.81% [−10.66, −0.95] n=22, placebo pct 0.0 | TRANSMITTING | not retracted — but read §3 |

Numbers: `data/ripple/retraction_six.json`. The test was registered in
RIPPLE_REGISTRATION.md Amendment B **before** it ran (commit 60058f9, 15:45:33; the estimator
first appears at 15:59:32): all-event shock restricted to days with `derived.vix_pct` at t−1 at
or above its median — the "VIX-stress regime" the edges claim — at h=20, against 500 non-event
days matched on both the VIX and the geopolitical-risk state.

## 2. I can see one of you has already started

`src/propagation_graph.py` in the working tree already carries `RETRACTED_EDGE_IDS` with
exactly these five, `RETRACTED_STATUS = "retracted_h1_retest"`, a pointer to my
`retraction_six.json`, and an `apply_retractions()` that forces the status while keeping the
strength and CI columns as computed. That is the right shape — a retraction is a status, not an
erasure — and I have not touched the file. Treat the rest of this note as the checklist around
that change, not as a request to redo it.

## 3. The constraint on palladium (Joe's words, and why they bind)

Publish the re-test result as computed, **and in the same breath** say two things: palladium is
not on the oil chain, and one survivor out of six at this base rate is consistent with noise.
It is **not a finding and must not be surfaced as one.**

That paragraph is now generated into `data/ripple/SUMMARY.md` and `RIPPLE_SUMMARY.md` by
`src/ripple_lp.py`, so it travels with the number wherever the summary goes. If palladium
reaches a surface, it must carry that framing or it must not appear. It would be a poor outcome
if retracting five edges left the sixth looking stronger by contrast — it is not stronger, it
is the one cell out of six where a 5% band and a 5% placebo tail happened to line up.

## 4. Surfaces and claims that still lean on the retracted edges

- **`EVALUATION.md` line 35:** "H1 amplification (Brent, pp) across surfaces:
  {'validation_claims': 5.5615, 'cross_asset_conditioned': 5.5615, 'sowhat': 5.5615} — all
  agree ✓." That is the Brent edge, now retracted. It is also **stale on its own terms**: the
  regenerated `data/cross_asset_conditioned.json` now reads 6.0412 for Brent, so the
  three-surface agreement check is asserting a number none of them currently holds.
- **`EVALUATION.md` line 32:** the defence of that amplification is a **label-shuffle**
  placebo ("collapses the amplification from 5.5615 to a placebo mean −0.0113"). Your own
  `src/placebo_vixmatched.py` opens by conceding that this null "rejects under BOTH the real-
  amplification hypothesis AND the artifact. It cannot tell them apart" (red-team attack #2).
  So the surviving defence of the retracted edge is the placebo the repo already retired.
- **`EVALUATION.md` lines 10–11:** the SAR-standardized effect and the regime-block-robust CI.
  These are stronger than the label shuffle and are **not** addressed by my re-test; they are a
  different question (is the amplification robust across regimes?) from mine (is the response
  bigger than matched non-event days?). Re-read, do not assume retracted.
- **`src/cross_asset_conditioned.py` line 89** builds the sentence "The stress-amplification
  mechanism generalizes to: …". After the retraction that sentence should not name the five.
- **`src/propagation_graph.py` line 220** describes the amplification edges as "the validated
  backbone" in prose, separately from the `backbone_validated` key you have already filtered.

## 5. Why the two gates disagreed, so this does not recur

Theirs (`cross_asset_conditioned.py` line 81): `generalizes = ci_excludes_zero and amp > 0 and
survives_FDR`, where `amp` is **high-VIX events minus low-VIX events**. It never looks at a
non-event day, so a world in which nothing transmits but volatile periods have larger moves
passes it. Mine compares against non-event days matched on the same VIX **and** geopolitical-
risk state. The disagreement is structural, not bad luck, and it is the same defect
`placebo_vixmatched.py` was written to fix. Any future edge promoted on the event-only median
split alone will fail the same way.

## 6. Not in scope for this note
Session C did not edit `propagation_edges`, `EVALUATION.md`, `cross_asset_conditioned.py`,
`propagation_graph.py`, or any surface. The re-test, its numbers and the palladium framing are
in `data/ripple/` and `RIPPLE_SUMMARY.md`, all committed.
