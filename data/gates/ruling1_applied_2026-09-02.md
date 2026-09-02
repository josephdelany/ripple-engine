# Ruling 1 applied — the five amplification edges retracted (session B, 2026-09-02)

Joe ruled option (a) on `data/gates/ripple_2026-09-02.md` Ruling 1. Session C ran the re-test under a
registration sealed before the code and declined to edit a table that is not its file; this is session B
carrying it out on Joe's authority. The dated amendment (`EDGE_PORTFOLIO.md`, 2026-09-02) was committed
**before** the table was touched, in the same order every registration in this repo follows.

## Rows flipped — five

`propagation_edges`, kind `stress->node`, `status` `validated` → **`retracted_h1_retest`**, `mechanism`
extended with the pointer `retracted 2026-09-02 by Joe's Ruling 1; re-test data/ripple/retraction_six.json;
docs/red_team_1.md`. `strength`, `ci_lo`, `ci_hi` keep the values as originally computed — the retraction is
a status, not an erasure.

| edge_id | strength (kept) | CI (kept) | re-test β at h=20 | placebo pct | new status |
|---|---|---|---|---|---|
| `amp.Brent oil` | +6.041 | [+1.557, +10.087] | +0.614 % [−4.116, +5.345], n 40 | 55.0 | `retracted_h1_retest` |
| `amp.Heating oil` | +5.030 | [+1.527, +9.230] | +2.008 % [−2.617, +6.633], n 35 | 87.8 | `retracted_h1_retest` |
| `amp.5Y breakeven` | +16.247 | [+4.470, +31.022] | −0.061 pp [−0.237, +0.116], n 20 | 2.2 | `retracted_h1_retest` |
| `amp.S&P 500` | +1.894 | [+0.342, +3.448] | −0.760 % [−2.769, +1.249], n 36 | 3.8 | `retracted_h1_retest` |
| `amp.Platinum` | +7.425 | [+1.958, +14.647] | −1.286 % [−5.042, +2.469], n 25 | 4.2 | `retracted_h1_retest` |

**`propagation_edges` now holds zero rows with `status = 'validated'`** (221 null, 6 trap, 5 retracted).
Before-state saved and quoted above; the re-test evidence is `data/ripple/retraction_six.json`.

One correction to the ruling's wording, for the record: the table held **five** `validated` rows, not six.
Palladium's row (`amp.Palladium`) was already `null` — its original CI, [−0.251, +10.108], covers zero — so
it was never in the validated set and does not enter or leave one here.

## The ruling is in the code, not just the data

`src/propagation_graph.py` **writes** this table (`DELETE` + re-`INSERT` on every run), so a flip applied only
to the rows would be silently undone by the next refresh. `apply_ruling1()` now forces the retracted status
and the pointer onto those five `edge_id`s, and the palladium note onto its row, whatever a run computes.
Verified by rebuilding: `python3 src/propagation_graph.py` re-ran end to end and the five came out retracted,
`backbone_validated` came out empty, and the palladium note survived. Lifting the retraction requires a dated
amendment in `EDGE_PORTFOLIO.md`, not a re-run. `tests/test_ruling1_retraction.py` asserts exactly this
(three tests, including the rebuild path on synthetic rows).

## Palladium — recorded as computed, and not a finding

Re-test: **−5.807 % [−10.663, −0.951], n = 22, placebo percentile 0.0, verdict TRANSMITTING.** Recorded on
the `amp.Palladium` row, in `data/ripple/retraction_six.json`, and in `data/evidence/node.palladium.json`
(tier `NOT_A_FINDING`), each carrying all four reasons together, as Joe required:
1. its row was already `null` and does not gain status here;
2. palladium is not on the oil chain;
3. one survivor of six at this base rate is what noise looks like — about a 26 % chance of at least one
   survivor at a 5 % threshold under a complete null;
4. the re-test's sign (−5.81 %) is the opposite of this sample's (+5.14 %); the two do not agree in direction.
It is not surfaced as a finding on any page, in any export, or in the paper.

## Claims re-read — every surface that leaned on the five

| surface | what it said | now |
|---|---|---|
| `propagation_edges` (5 rows) | `validated` | `retracted_h1_retest` + pointer |
| `data/propagation_graph.json` | `backbone_validated`: all five | `backbone_validated: []`, plus `backbone_retracted_2026_09_02` naming them |
| `src/backend.py` desk panel (line ~957) and brief (line ~1071) | rendered "BACKBONE (validated) … ripples harder under stress (FDR-corrected)" per edge | both iterate `backbone_validated`, now empty — the panel renders no backbone rows and the brief's "Validated propagation backbone" paragraph is skipped by its own `if bb:` |
| `src/mcp_server.py` (line ~292) | served `backbone_validated` | same list, now empty |
| `src/shock_tracer.py` transmission lane | reads `status='validated'` from `propagation_edges` | zero rows match, by construction |
| `data/evidence/node.{brent_oil,heating_oil,5y_breakeven,s&p_500,platinum}.json` | claim cards: "A shock ripples harder into X when VIX stress is elevated", tier SUGGESTIVE | **RETRACTION cards** at the same paths (tier `RETRACTED`), stating the claim is withdrawn and pointing at the ruling, the amendment, the re-test and the red-team file. Written by `src/evidence.py`, so a regeneration keeps them. |
| `data/evidence/node.palladium.json` | claim card, tier SUGGESTIVE | tier `NOT_A_FINDING` with the four reasons |
| `EVIDENCE.md` | listed the five as claims | a "Retracted 2026-09-02 (Joe's Ruling 1)" table; the claim rows are gone |
| `EVALUATION.md` | §0 had **already** downgraded the entire prior validated set to SUGGESTIVE ("under this bar the current validated set is empty"), and §2's jackknife table is explicitly marked "superseded for tiering by §0" | no claim there needed weakening. The stored rows had been lagging the published bar; this amendment makes the data say what the document already said. |
| `docs/PAPER_DRAFT.md` (line 469) | already states the edges "were retracted under a" re-test | consistent; no change |
| `src/edge_battery.py`, `src/domain_conditioning.py`, `PRE_REGISTRATION.md` | "ripples harder" appears in *mechanism strings for other hypotheses* (gold/USD, gold/real-rates, conflict-intensity/gold) | untouched: different edges, different registrations, not part of this ruling |

## Tests

`tests/test_ruling1_retraction.py` (3) — the registered set is exactly the five; a rebuild cannot
re-validate them; no surface calls them validated. `tests/test_evidence.py` (4, one new) — a withdrawn pack
must carry its ruling and must not read as a live claim, and palladium's must carry every reason.

## What I did not do
- Did not touch `RIPPLE_REGISTRATION.md` or `data/ripple/*` — session C's files; its re-test stands as
  computed and is only pointed at from here.
- Did not re-run the re-test or recompute any number in it.
- Did not delete a single row, card or historical claim: every retracted artifact keeps its numbers.
- Did not act on Rulings 2 (JODI licence) or 3 — not in this brief and not session B's to decide.
