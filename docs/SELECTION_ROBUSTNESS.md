# Selection robustness — the class concentration read from both directions

*2026-09-03, session A. Every figure is read from `data/big_moves/summary.json` at the **registered**
variant (`BIG_MOVES_REGISTRATION.md` §3, Amendments 1–2 for onset/end, Amendment 4 for the re-run:
both windows pooled and clustered once within 60 **trading** days, no merge step). The file also
publishes a superseded `as_computed` cut; it is used here only as a robustness check and is labelled
where it appears. Intervals are Wilson 95%.*

---

## 0. The objection this answers

The project's headline physical result is that **geopolitical events concentrate in the diesel crack
and not in crude**. Stated the usual way — *given one of our events, how often was there a big move?* —
it is conditioned on our own event list, and the obvious reviewer's objection is that we chose the
events. If we picked events that happen to sit near crack moves, the finding is an artefact of the
picking.

`summary.json` carries a second conditional that is immune to that objection, because it **starts
from the market**: take the market's own largest moves, defined only by each series' own history, and
ask what was going on. Our corpus can only affect *whether an episode gets attributed*, never which
episodes exist. Both directions are reported below, side by side.

---

## 1. What the denominators are — and why the two tables must be read differently

This is the part most likely to be misread, so it is stated before the numbers.

**Direction A — `p_big_given_class`. Unit: a corpus event. Denominators are DISJOINT.**
An event carries exactly one `type`, so the seven class denominators partition the evaluable corpus
(299–300 of 313 events; the remainder lack price data on that series). Pooling classes is legitimate
here, and the pooled rows below are real.

**Direction B — `p_class_given_big`. Unit: a market episode. Denominators are NOT disjoint.**
Every class shares the same denominator — the asset's episode count — and an episode may contain
events of several classes, so an episode is counted once per class present. **The percentages in
Table B do not partition anything and must not be summed.** Concretely:

| asset | episodes | no identified event | attributed | class-episode pairs | pairs per attributed episode | geopolitical share of pairs |
|---|---|---|---|---|---|---|
| Brent | 44 | 14 (31.8%) | 30 | 60 | 2.00 | 30/60 = 50.0% |
| WTI | 48 | 14 (29.2%) | 34 | 61 | 1.79 | 32/61 = 52.5% |
| Diesel crack | 37 | 8 (21.6%) | 29 | 79 | 2.72 | 47/79 = 59.5% |

Brent's 60 pairs across 30 attributed episodes is 2.00 classes per episode; the crack's is 2.72.
Summing a column of Table B would therefore give 136%, 127% and 214% respectively — which is not a
paradox, it is what a non-exclusive tabulation looks like.

Throughout, **geopolitical** means the four classes `conflict escalation`, `infrastructure attack`,
`chokepoint disruption`, `sanctions` (bold in the tables). The other three — `OPEC decision`,
`policy response`, `demand shock` — are the control group: they are also events we chose, so if the
concentration were an artefact of our choosing, they should move with the geopolitical four.

---

## 2. Direction A — corpus-selected: P(big move | our event)

Conditioned on our event list. Ratios are against **that asset's own** everyday base rate
(Brent 18.7%, WTI 19.3%, crack 18.2%), never a shared one.

| class | Brent | WTI | Diesel crack | crack − Brent |
|---|---|---|---|---|
| **conflict escalation** | 12/50 = 24.0% [14.3, 37.4] | 15/50 = 30.0% [19.1, 43.8] | 23/50 = 46.0% [33.0, 59.6] | +22.0 pp |
| **infrastructure attack** | 6/44 = 13.6% [6.4, 26.7] | 7/45 = 15.6% [7.7, 28.8] | 15/45 = 33.3% [21.4, 47.9] | +19.7 pp |
| **chokepoint disruption** | 4/26 = 15.4% [6.2, 33.5] | 4/26 = 15.4% [6.2, 33.5] | 10/26 = 38.5% [22.4, 57.5] | +23.1 pp |
| **sanctions** | 8/55 = 14.5% [7.6, 26.2] | 6/55 = 10.9% [5.1, 21.8] | 19/55 = 34.5% [23.4, 47.7] | +20.0 pp |
| OPEC decision | 16/51 = 31.4% [20.3, 45.0] | 14/51 = 27.5% [17.1, 40.9] | 13/51 = 25.5% [15.5, 38.9] | -5.9 pp |
| policy response | 18/56 = 32.1% [21.4, 45.2] | 20/56 = 35.7% [24.5, 48.8] | 20/56 = 35.7% [24.5, 48.8] | +3.6 pp |
| demand shock | 6/17 = 35.3% [17.3, 58.7] | 5/17 = 29.4% [13.3, 53.1] | 5/17 = 29.4% [13.3, 53.1] | -5.9 pp |
| **geopolitical, pooled** | 30/175 = 17.1% [12.3, 23.4] | 32/176 = 18.2% [13.2, 24.5] | 67/176 = 38.1% [31.2, 45.4] | +21.0 pp |
| ratio to that asset's everyday rate | ×0.92 | ×0.94 | ×2.09 | |
| non-geopolitical, pooled | 40/124 = 32.3% [24.7, 40.9] | 39/124 = 31.5% [23.9, 40.1] | 38/124 = 30.6% [23.2, 39.2] | |
| ratio to that asset's everyday rate | ×1.73 | ×1.63 | ×1.68 | |

**Read:** the four geopolitical classes move together by **+19.7 to +23.1 pp** from Brent to the
crack. The three control classes move by **−5.9 to +3.6 pp** — that is, not at all. Pooled, the
geopolitical rate goes from ×0.92 of Brent's everyday rate to ×2.09 of the crack's, while the
non-geopolitical rate is ×1.73 against ×1.68 — indistinguishable.

Against crude, geopolitical events are **below** the everyday base rate: a big Brent move is slightly
*less* likely on a geopolitical event day than on a random day.

---

## 3. Direction B — market-defined: P(class present | the market's biggest moves)

Starts from each series' own largest moves. Our corpus cannot affect which episodes exist.

| class | Brent | WTI | Diesel crack | crack − Brent |
|---|---|---|---|---|
| **conflict escalation** | 11/44 = 25.0% [14.6, 39.4] | 15/48 = 31.2% [19.9, 45.3] | 17/37 = 45.9% [31.0, 61.6] | +20.9 pp |
| **infrastructure attack** | 5/44 = 11.4% [5.0, 24.0] | 6/48 = 12.5% [5.9, 24.7] | 9/37 = 24.3% [13.4, 40.1] | +13.0 pp |
| **chokepoint disruption** | 4/44 = 9.1% [3.6, 21.2] | 4/48 = 8.3% [3.3, 19.6] | 9/37 = 24.3% [13.4, 40.1] | +15.2 pp |
| **sanctions** | 10/44 = 22.7% [12.8, 37.0] | 7/48 = 14.6% [7.2, 27.2] | 12/37 = 32.4% [19.6, 48.5] | +9.7 pp |
| OPEC decision | 17/44 = 38.6% [25.7, 53.4] | 16/48 = 33.3% [21.7, 47.5] | 13/37 = 35.1% [21.8, 51.2] | -3.5 pp |
| policy response | 7/44 = 15.9% [7.9, 29.4] | 8/48 = 16.7% [8.7, 29.6] | 13/37 = 35.1% [21.8, 51.2] | +19.2 pp |
| demand shock | 6/44 = 13.6% [6.4, 26.7] | 5/48 = 10.4% [4.5, 22.2] | 6/37 = 16.2% [7.7, 31.1] | +2.6 pp |

The crack attributes more of its episodes to *something* (78.4% against Brent's 68.2%), which would
inflate every crack cell. Normalising to attributed episodes removes that, and Brent and the crack
have almost the same attributed count (30 against 29):

| class | Brent | WTI | Diesel crack | crack − Brent |
|---|---|---|---|---|
| **conflict escalation** | 11/30 = 36.7% [21.9, 54.5] | 15/34 = 44.1% [28.9, 60.5] | 17/29 = 58.6% [40.7, 74.5] | +22.0 pp |
| **infrastructure attack** | 5/30 = 16.7% [7.3, 33.6] | 6/34 = 17.6% [8.3, 33.5] | 9/29 = 31.0% [17.3, 49.2] | +14.4 pp |
| **chokepoint disruption** | 4/30 = 13.3% [5.3, 29.7] | 4/34 = 11.8% [4.7, 26.6] | 9/29 = 31.0% [17.3, 49.2] | +17.7 pp |
| **sanctions** | 10/30 = 33.3% [19.2, 51.2] | 7/34 = 20.6% [10.3, 36.8] | 12/29 = 41.4% [25.5, 59.3] | +8.0 pp |
| OPEC decision | 17/30 = 56.7% [39.2, 72.6] | 16/34 = 47.1% [31.5, 63.3] | 13/29 = 44.8% [28.4, 62.5] | -11.8 pp |
| policy response | 7/30 = 23.3% [11.8, 40.9] | 8/34 = 23.5% [12.4, 40.0] | 13/29 = 44.8% [28.4, 62.5] | +21.5 pp |
| demand shock | 6/30 = 20.0% [9.5, 37.3] | 5/34 = 14.7% [6.4, 30.1] | 6/29 = 20.7% [9.8, 38.4] | +0.7 pp |

---

## 4. Verdict

**The concentration holds in the market-defined direction. It is not an artefact of which events we
chose.**

The evidence for that, in order of how much weight it carries:

1. **All four geopolitical classes are elevated in the crack in both directions.** Direction A
   +19.7 to +23.1 pp; direction B (normalised) +8.0 to +22.0 pp. Eight of eight cells, same sign.
2. **The internal control goes the other way.** `OPEC decision` — the archetypal crude-supply event —
   is the one class where crude should dominate if the mechanism is real, and it does: crack minus
   Brent is **−5.9 pp** in direction A and **−11.8 pp** in direction B (normalised). An artefact of
   attribution would have lifted OPEC too, because OPEC decisions are events we chose in exactly the
   same way. `demand shock` is flat in both (−5.9 pp, +0.7 pp).
3. **It survives the clustering rule.** Under the superseded `as_computed` rule the pooled direction-A
   geopolitical rate is 16.0% for Brent against 37.5% for the crack, against 17.1% and 38.1% under the
   registered rule. The result is not an artefact of Amendment 4's re-run either.

### The one thing that does not fit, stated rather than buried

**`policy response` behaves differently in the two directions.** It is flat in direction A
(+3.6 pp) but strongly elevated in direction B (+19.2 pp raw, +21.5 pp normalised) — as large as any
geopolitical class. So the clean geopolitical / non-geopolitical separation that direction A shows is
**not** reproduced exactly in the market-defined direction; there, three of the four geopolitical
classes and one control class are all elevated.

This weakens the sharp version of the claim ("only geopolitical classes concentrate in the crack") but
not the version that matters ("the crack concentration is not an artefact of our event selection"),
because the artefact story predicts *all* our classes lift together, and OPEC and demand shock do not.
A reviewer is entitled to ask why policy response splits, and this document does not answer it.

---

## 5. What is NOT claimed, and what these numbers cannot support

- **No p-value is given for any crack-versus-crude difference, and none can be from this file.**
  Direction A scores **the same corpus events** against two price series, so the comparison is
  *paired*. A paired test (McNemar) needs the per-event agreement — how many events moved the crack
  but not Brent, and vice versa — and `summary.json` publishes only marginal counts. An unpaired
  two-proportion test would be the wrong test and would overstate significance. The per-event
  indicators exist upstream in `src/big_moves.py`; computing the paired contrast is a separate job
  and is **not** done here.
- **The intervals overlap.** Brent's conflict-escalation rate is 24.0% [14.3, 37.4] and the crack's is
  46.0% [33.0, 59.6] — they nearly touch, and several other pairs overlap outright. No single row here
  is a result on its own. The strength of the finding is the **consistency of sign across four
  disjoint classes with a control that reverses**, not any one interval.
- **Multiplicity is unaddressed.** Seven classes × three assets × two directions is 42 cells, reported
  without correction because none of them is being used as a test.
- **The classes are not independent of one another** in direction B: one episode contributes to several
  class rows, so the four geopolitical rows in that table are correlated by construction, and the
  "eight of eight cells, same sign" count above is not eight independent draws.
- **Attribution is still ours.** Direction B is immune to which events we chose, but not to whether we
  *found* the event that accompanied a given episode. 31.8% of Brent episodes and 21.6% of crack
  episodes have no identified event at all. If our corpus is systematically better at covering the
  kind of event that moves cracks, that would produce this pattern without any physical mechanism.
  Nothing in this file rules that out; it is the strongest remaining form of the objection.

---

## 6. Receipts

`data/big_moves/summary.json` — registered variant for §2–§4, `as_computed` block for §4.3 ·
`BIG_MOVES_REGISTRATION.md` §3 + Amendments 1, 2, 4 · everyday base rates are each asset's own
`everyday_base_rate_pct` · Wilson 95% intervals computed in this pass, not stored.
