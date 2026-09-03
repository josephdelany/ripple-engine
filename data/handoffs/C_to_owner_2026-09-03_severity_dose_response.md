# C → whoever owns `data/edge_battery.json` and `src/admit_events.py` (cc Joe)

2026-09-03, Session C. Two items, both from OPEN_ITEMS 1.5/1.6 as registered at `4bfcbf3`. I have
**not** edited either file: `edge_battery.json` is another session's output and `admit_events.py` is
A's corpus tooling. Charter §1.

---

## 1. `severity_dose_response` is RETRACTED — please change the status, not the numbers

`data/edge_battery.json` carries it as `"validated": true`. Under the discipline registered in
`MAGNITUDE_REGISTRATION.md` §5 (sealed `8cb9d3d`, verdict words fixed before the run) it does not
survive. Full write-up: `docs/MAGNITUDE_SEVERITY_RETEST.md`. Numbers:
`data/magnitude/severity_retest.json`.

| | published | re-tested |
|---|---|---|
| amp (high − low mean \|CAR+20\|, Brent) | +5.079 [+1.003, +9.364] | **+2.071 [−4.067, +8.209]** |
| permutation p | 0.0303 | **0.269** |
| n | 116 (76 / 40) | 91 (52 / 39), de-overlapped within severity group |
| state-matched placebo | *never built* | **95.8th pct**, inside [−2.306, +2.192] |

**Suggested treatment — the one v2 §3 used on the propagation edges:** change `validated` to a
**status**, not an erasure. Keep `amp`, `ci`, `perm_p` at their computed values and add a
`retraction` block naming the re-test, so the record shows what was believed and why it changed.
That pattern is already in `src/propagation_graph.py` (`RETRACTED_EDGE_IDS`, `apply_retractions`).

**Two reasons it failed, both inflating significance:**

1. **No non-event comparison.** The gate compares events to other events, so severe events happening
   in volatile periods pass it with nothing transmitting. Already conceded in the repo as red-team
   attack #2 and the basis for the five propagation-edge retractions.
2. **Clustering unit.** `_oil_type_frame` clusters **within event type** — right for the neighbouring
   chokepoint-vs-sanctions test, wrong when the grouping variable is severity. High arm: 106 raw →
   **92** within type (used) → **56** within severity group (required). 36 overlapping same-severity
   episodes counted as independent.

   *This one is worth a look beyond this claim*: `chokepoint_gt_sanction` is grouped by type, so
   within-type clustering is correct there. Any other two-group test in that file grouped by
   something other than type inherits the same problem. I have not audited the rest.

**Also in that file, untested by me:** `copper_growth` and `hy_credit_stress` are marked `validated`
and are state-conditioned amplification edges scored by the same gate. I make no claim about either;
they share the defect and the same re-test is available.

---

## 2. `admit_events.py` — a latent INV-5 violation, not a live one. My earlier report overstated it.

I reported (and Joe registered at `4bfcbf3`) that "102 of 313 `events.severity` values are
auto-assigned by class". **That was an upper bound and the resolved number is zero.** Evidence:

- `data/extract/admission_log.csv` does not exist — the auto-admit path has produced no receipt.
- No current event carries an `AUTO-ADMIT` rec_reason in `data/candidate_review.csv`.
- All 32 current events present in that sheet are `joe_decision=approve`.
- The 102 overlap is what chance predicts: `SEV_BAND` is {3, 2}, the modal severities of a 1–5 scale.

**So OPEN_ITEMS 1.6 should be re-scoped from "live defect in the data" to "latent defect in the
code".** It is still worth fixing, because the next run of `admit_events.py` *will* create it:
`src/admit_events.py:89` writes a class-derived number into the same `severity` column that carries
Joe's judgements, and nothing downstream can then tell them apart.

**Suggested fix, additive and cheap:** have the auto-admit path write the provisional value to a
**separate column** (`severity_provisional`, plus a `severity_source` of `analyst` / `class_band`)
and leave `severity` NULL until a human sets it. `load_events.py` already rejects a non-1–5
severity, so a NULL would surface rather than pass silently. That keeps measured and inferred in
different columns, which is what INV-5 asks.

**The live issue that does survive**, and which matters more for anything that reads the field:
`severity` carries **no per-value source anywhere**. It is analyst judgement throughout — uniform, so
not an INV-5 breach, but inferred, and it must be labelled inferred wherever it is displayed or used.
`MAGNITUDE_REGISTRATION.md` Amendment C-1 §3 now registers that it may never serve as a quantity
magnitude (M-Q).

---

Nothing in `src/edge_battery.py`, `data/edge_battery.json`, `src/admit_events.py`, `data/events.csv`
or the `events` table was modified by this session.
