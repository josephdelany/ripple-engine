# Wireframes — the chosen direction

*2026-09-03, session A. Companion to `docs/design/STUDY.md`. Direction **B spine + C figures**: each
screen reads as a short registered report; the figures are instrument-grade.*

**Every number below is real**, read from the repo on this date at the path named beside it. Nothing
is illustrative. Where a region is ugly — no precedent, insufficient n, a null hop, a claim that can
never resolve — the ugly state is drawn, not skipped, because those are the majority cases.

Monospace column width is 100ch, matching the 1100px content width at the Evidence-tier size.

Legend: `▓` full-contrast Finding · `▒` Evidence · `░` Provenance · `├──┼──┤` interval bar with tick
· `▨` hatch (insufficient) · `│` the zero rule.

---

## 0. The record bar (DESIGN.md §5) — persistent, every screen

Named fields, not a sentence. Provenance labels above Evidence values; the two verdicts carry §2
colour.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ░CORPUS  ░GEO   ░STATE@t      ░CELLS      ░CLAIMS   ░G vs CLIM        ░P vs PERS       ░AUDIT   │
│ ▒313     ▒187   ▒60 of 786    ▒15 of 371  ▒51/112   ▒−0.097 ·worse    ▒+0.128 ·better  ▒1 of 30 │
│ ░events  ░coded ░knowable     ░transmit   ░resolved ░[−.180,−.018]    ░[.070,.185]     ░κ n/a   │
│                                                                                                 │
│ ░run walk_20260903T003422Z · as of 2026-08-25 · every field one click from its file             │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

`STATE@t 60 of 786` is new and is the point of the redesign: the vintage wall is now on every screen.
Receipts: `data/state/situation_knowable.json`, `data/ripple/irf.json`, `data/walk_forward/summary.json`,
`data/ledger/*.jsonl`.

---

## 1. THE RESULT — the landing screen (replaces Feed)

Reads as an abstract. This is the ten-second object.

```
════════════════════════════════════════════════════════════════════════════════════════════════════
 ▓ Restricted to what was knowable at the time, the record goes quiet.
 ▒ Three findings from 313 geopolitical events and 772 series, 1973–2026. All pre-registered.
════════════════════════════════════════════════════════════════════════════════════════════════════

 ▓ 1 · For 262 of 313 events the engine has no state to condition on at all.
   ▒ Every situation field carries the date it became knowable. 726 of 786 field-values were
   ▒ knowable only after the event they describe. 60 survive. 51 events keep at least one field.
                                                                    ░data/state/situation_knowable.json
        events with ≥1 field at t   ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  51 of 313  (16.3%)
        field-values kept at t      ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  60 of 786  ( 7.6%)
   ░ This is not a data-collection gap we intend to close. It is what point-in-time honesty costs,
   ░ and most published event studies do not pay it. Rule (e), if adopted, moves 60 → 83. ░docs/g/

 ▓ 2 · The engine forecasts escalation worse than the base rate, and prices better than persistence.
   ▒ Daily tier, 253 scored reads, sealed before resolution. Four baselines, all shown.
                                                                     ░data/walk_forward/summary.json
                                        worse ←──────── │ ────────→ better
     escalation vs climatology   −0.097          ├───┼──┤│                    n=150  DM p 0.022
     escalation vs persistence   −0.600   ├──────────┼──┤│                    n=150  DM p 0.0002
     escalation vs random analogs −0.021              ├──┼┼─┤                 n=150  DM p 0.58
     escalation vs frozen engine +0.007               │├┼┤                    n=150  DM p 0.029
     price vs persistence        +0.128               │      ├──┼──┤          n=253  DM p 3e-5
     price vs climatology        −0.071            ├──┼─┤    │                n=253  DM p 0.016
     price vs random analogs     −0.005              ├──┼┼──┤                 n=253  DM p 0.85
     price vs frozen engine      +0.007               │├┼┤                    n=253  DM p 8e-5
     ░ scale −0.70 to +0.30 · zero rule drawn on every row · skill, so above zero is better
   ▒ The interval crosses zero against random analogs on both tasks: no effect distinguishable
   ▒ from drawing comparable past events at random, at this sample size.
   ░ Permutation p 0.124. Monthly tier: 0 reads scored, permits_validation false — no monthly result.

 ▓ 3 · 15 of 371 registered pass-through cells transmit. Sanctions transmit nowhere.
   ▒ 53 cells per class × 7 classes, fixed before estimation; 500 state-matched placebo draws.
   ▒ 301 null · 55 insufficient · 15 transmitting · 11 survive Benjamini–Hochberg at q=0.10.
                                                                              ░data/ripple/irf.json
        policy_response      ███████                      7
        infrastructure_attack███                          3
        opec_decision        ██                           2
        demand_shock         █                            1
        chokepoint_disruption█                            1
        conflict_escalation  █                            1
        sanctions            ░ none                       0   ← 53 cells, nothing transmits
   ░ A 5% screen over 371 cells would produce ~19 by chance alone; 15 fire and 11 survive FDR
   ░ control. Read as: the aggregate is not a signal, and eleven specific cells may be.

────────────────────────────────────────────────────────────────────────────────────────────────────
 ░ What this project does NOT claim: that it forecasts oil prices; that escalation is predictable
 ░ from the record; that the G target is validated (its 30-event audit stands at 1 of 30, κ n/a).
 ░ VALIDATED is reserved by WALK_FORWARD_PROTOCOL §7 and is not claimed anywhere.
════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## 2. HOW YOU'D CATCH US — the method screen

```
════════════════════════════════════════════════════════════════════════════════════════════════════
 ▓ Six ways this could be wrong, and what each one is checked against.
════════════════════════════════════════════════════════════════════════════════════════════════════

 ▒ 1 Look-ahead   Every field carries knowable_at; the join drops anything knowable after t.
                  ░726 of 786 dropped · data/state/situation_knowable.json · charter §2 rule 5
                  ░Precedent: the Philadelphia Fed SPF benchmarks on the vintage panelists had.
 ▒ 2 Re-cutting   Windows, splits and metrics registered before the run. Cells fixed at 53/class.
                  ░RIPPLE_REGISTRATION.md cbf4fdc + A,B · seed 19900802 · WALK_FORWARD_PROTOCOL.md
 ▒ 3 Cherry-pick  Every registered cell is displayed, nulls included. The band is never filtered
                  ░by verdict. 301 nulls are on the page. DESIGN.md Amendment 1 A1.1
 ▒ 4 Luck         500 state-matched placebo pseudo-events per cell; permutation p 0.124 overall.
                  ░data/ripple/irf.json meta.n_placebo · summary.json permutation
 ▒ 5 Bad target   IES-90 is coded from ICB/MID/UCDP/COW, not from our own corpus. sr_outcome_90
                  ░was RETIRED at κ≈0 on 2026-09-02 and nothing conditions on it. OUTCOME_MAPPING.md
 ▒ 6 Grading self The 30-event human audit is ▨ 1 of 30 done, κ not computable, passed: false.
                  ░data/audits/ies90_audit_30.csv — this is the weakest link and it is stated first.

 ▓ The data itself is not a random sample, and we cannot fix it.
   ▒ 40 of 772 series stopped reporting before Sept 2025. They did not break — they went dark.
        jodi.ir.*  crude production, exports, stocks, refinery intake, products demand  ends 2018-07
                   ░the month US secondary sanctions were reimposed
        jodi.ae.*  five series                                                          ends 2018-12
        jodi.qa.*  five series                                                          ends 2018-12
        jodi.ru.crude_stocks                                                            ends 2009-12
        jodi.kz.crude_stocks                                                            ends 2014-03
   ▒ Any post-2018 physical-flow result is conditioned on the states that chose to keep reporting.
   ░ Stated as a selection problem with no correction available. ░data/oil.db observations
════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## 3. A CASE — the Story screen (Direction B spine, C figures)

Real payload: `GET /api/story?id=abqaiq_attack_2019`. Prose spine, figures inline, provenance inline.
Note this event exercises three ugly states at once.

```
════════════════════════════════════════════════════════════════════════════════════════════════════
 ░ knowable 2019-09-14 · infrastructure attack · eia.gov · commodity.brent, country.saudi_arabia
 ▓ The market moved less than an ordinary day would predict.
 ▒ Attack on Saudi Abqaiq and Khurais facilities — the largest single disruption of crude
 ▒ processing on record — sits inside a big Brent move 11.4% of the time (5 of 44), against
 ▒ 18.3% for any random day. Ratio 0.62. It is material for diesel, not for crude.
                                                                    ░data/big_moves/brent.json
────────────────────────────────────────────────────────────────────────────────────────────────────
 WHAT WAS KNOWABLE ON 2019-09-14
 ▒ No situation field for this event was knowable at t, so the engine read it on class and
 ▒ entities alone. This is the ordinary case: it is true for 262 of 313 events in the corpus.
 ░ data/state/situation_knowable.json · WORLD_STATE_FRAMEWORK.md Amendment A

 IS IT PRICED?
 ▒ Brent at knowable: $68.42. 15 conditioned analogs, all knowable before 2019-09-14.
 ▒ Realized path sits 17.8% below the analog median at +20 trading days.
        $/bbl                                            ░ individual analog paths, not a box plot
        +30% ┤ ░░░░░░░░░░░░░░░░░░░░░░░░░ nda_bonny_2016 2016-02-10  +30.3%  ← best analog
             │ ░░░░░░░░░░░░░░
          0% ┼─────────────────────────────────────────────────── zero, always drawn
             │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ realized
        −15% ┤ ░░░░░░░░░░░░░░░░░░░░░░░░░ saudi_ew_pipeline_2019 2019-05-14 −15.0% ← worst analog
             └──┬────┬────┬────┬────┬────┬  ░ECMWF plume, not box-and-whisker: the analog
                0    4    8   12   16   20  ░distribution is bimodal and a box would hide it
 ░ front spread · curve slope · OVX percentile · COT percentile: all four null for this event,
 ░ shown as literal `unknown` rather than as a zero or an omission. ░api/story priced.*

 IS THE NARRATIVE RIGHT?
 ▒ 1 claim extracted, 1 checkable, 0 uncheckable.
   ▒ "Aerial attack temporarily removes a large share of Saudi processing capacity"
                                                          ░data-verbatim, source eia.gov
     ▒ flow claim · asserted · brent at +20 trading days · verdict MIXED · r 0.467 · n 15
        of 15 comparable events: ▼ down 4 · ─ flat 3 · ▲ up 8   ├────┼────┤  k=7
   ░ MIXED is a verdict, not a missing one: the reference class splits 8/4 and the record
   ░ does not call it. ░data/ledger/claims.jsonl · CLAIM_LEDGER_REGISTRATION.md

 WHAT IS THE TAIL?
 ▒ 23 conditioned analogs, all knowable before 2019-09-14. no_adequate_precedent: false.
        contained            17 of 23   ├─────┼─────┤        Wilson 95% [0.535, 0.875]
        ░ closest analog  1977-05-11  Fire at Saudi Abqaiq processing facility  sim 0.80
        ░ likeness: type · target · conflict_scope · tempo
        ░ difference: prior_dyad CONTAINED → LIMITED_RETALIATION (judgment, unmeasured)
 ▓ TWO DEFECTS ARE VISIBLE HERE, and both are real on the built screen today.
   ░ (a) The screen renders "17 of 23  74%" with NO interval. §1 says a proportion "appears
   ░     with its interval or not at all". The Wilson bound above is what it should carry.
   ░ (b) `conflict_scope` is offered as evidence that a 1977 event matches a 2019 one. That
   ░     field is computed over ±120 days around the event (src/situation_record.py), so it
   ░     is contaminated by the future — a look-ahead value on a point-in-time screen.
   ░     Reported by session G (data/handoffs/G_to_A_2026-09-03_knowable_at_rule_e.md §3);
   ░     verified present in the rendered DOM on 2026-09-03. Needs a ruling, not a patch.

 WHERE DOES IT TRAVEL?
 ▓ 3 of 53 registered cells transmit for infrastructure attacks — and crude is not one of them.
   ░ VSUP grid: colour saturates with |effect|, desaturates toward grey with uncertainty.
   ░ Hatched = insufficient (n < 15). Every cell drawn, none filtered by verdict.

        hop                            cells   ░ 4 crude cells, none transmitting
    0   crude                          ▒▒▒▒                                     0 tx
    1   refined products & cracks      ▓▓▒▒▒▒▒                                  2 tx
          jet_gulf        +4.404 %      │  ├────────┼────────┤        n=20 h=20  TRANSMITTING
          gasoline_crack  +2.509 idx    │  ├────┼─────┤               n=20 h=20  TRANSMITTING
    2   physical flow & stocks         ▒▒▒▒▒▨▨▨▨▨▨▨                              0 tx, 7 ▨
          transit_hormuz               ▨ insufficient (n=14): below the registered minimum of 15
    3   gas & LNG                      ▒▒▒▒▨                                     0 tx, 1 ▨
    4   fertiliser & coal              ▒▒▒▒▒▒                                    0 tx
    x   macro cross-asset              ▒▒▒▒▒▒▒                                   0 tx
    e   equity proxies                 ▓▒▒▒▒▒▒▨▨▨▨▨                              1 tx, 5 ▨
          eq_tnk           +3.169 %     │ ├───┼────┤                 n=15 h=5   TRANSMITTING
   ▒ The shock is visible in jet fuel, gasoline cracks and tanker equities. It is not visible in
   ▒ crude at the registered horizon. 37 of 53 cells are null; that is the finding, not a gap.
   ░ Each null: "The interval crosses zero: no effect distinguishable from none at this sample
   ░ size." — rendered on every cell, per §2. data/ripple/irf.json · RIPPLE_REGISTRATION.md + A,B

 HOW MUCH TO TRUST THIS
 ▒ G Brier skill vs climatology  −0.097  ├───┼──┤│          n=150  DM p 0.022
 ▒ P CRPS skill vs persistence   +0.128       │  ├──┼──┤    n=253  DM p 3e-5
 ▒ G SPA p (best of menu)         0.645  ░best model M03_market_only, n=137
 ░ run walk_20260903T003422Z · protocol §7 status SUGGESTIVE / null · label audit NOT passed (1/30)
════════════════════════════════════════════════════════════════════════════════════════════════════
```

### The same screen, thin case — what a story with almost nothing looks like

```
 ░ knowable 2026-07-28 · no class matched · pasted text · regex-fallback reader
 ▓ The desk cannot read this as a market event.
 ▒ No event class matched, so no reference class exists: no analogs, no branches, no pass-through.
 ▨ Is it priced?        — no fan: an unclassified story has no comparable set.
 ▨ Is the narrative right? — 0 checkable claims extracted from this text.
 ▨ What is the tail?    — no reference class: branches are conditioned on the event class.
 ▨ Where does it travel? — no event class: this band is conditioned on the story's class.
 ░ Each region states why it is empty. None of them is blank. DESIGN.md §6.
 ▒ This is the honest majority outcome for pasted text: today's feed is 2 material of 14 items.
```

---

## 4. THE RECORD — Big moves, corpus, and the live loop

```
════════════════════════════════════════════════════════════════════════════════════════════════════
 ▓ 15 of the 43 biggest Brent moves since 1987 have no identified event at all.
 ▒ Significance is the top 5% of 20- and 60-day moves in each asset's own history — defined here,
 ▒ not by anyone's severity score. Everyday base rate 18.3%.        ░data/big_moves/brent.json
        no identified event   15 of 43  ├──────┼──────┤   Wilson 95% [0.224, 0.498]   (34.9%)
        ░ The single largest category. It is drawn first because it is the largest.

 ▒ P(class | a big move happened), with intervals against the everyday base rate:
        class                    k of 43   rate    interval
        opec_decision            14 of 43  32.6%   ├────┼────┤
        conflict_escalation      10 of 43  23.3%   ├───┼────┤
        sanctions                 9 of 43  20.9%   ├───┼────┤
        policy_response           8 of 43  18.6%   ├───┼───┤
        demand_shock              5 of 43  11.6%   ├──┼───┤
        infrastructure_attack     4 of 43   9.3%   ├──┼──┤
        chokepoint_disruption     4 of 43   9.3%   ├──┼──┤
        ░ intervals are Wilson 95%; the zero rule here is the 18.3% everyday base rate
 ▨ THE `anticipated` COLUMN CANNOT BE DRAWN. DESIGN.md §3.5 requires that `anticipated`
 ▨ "becomes a visible column rather than an inline tag". There is no such field in
 ▨ data/big_moves/brent.json — all 43 episodes carry `anticipated: null`, and the key is
 ▨ absent from the file's schema. §3.5 specifies a column with no backing data. Either
 ▨ big_moves.py computes it or §3.5 is amended; it must not be drawn until one of those.

 ▒ The corpus: 313 events, 1973-10-06 → 2026-06-17, seven classes.
        sanctions 57 · policy_response 57 · conflict_escalation 55 · opec_decision 52 ·
        infrastructure_attack 48 · chokepoint_disruption 27 · demand_shock 17
   ░ demand_shock at n=17 is the thinnest class in the corpus; every result conditioned on it
   ░ carries that n, and 1 of its 53 pass-through cells transmits.

 ▒ The live loop still runs — proof of operation, not a product surface.
        2026-07-28   material 2 · in line 0 · noise 12
        ░ The feed is a diagnostic. It is not a recommendation and makes no claim to be actionable.
════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## 5. THE LEDGER — folded into THE RESULT, drawn as a register not a scoreboard

Following the Retraction Watch dual-entry model: a claim and its dated status change are both
records. This reads correctly at n=1, where a scoreboard reads as failure.

```
 ▓ At 36 resolved claims the record and the narrative are not distinguishable.
 ▒ 112 claims logged · 64 checkable · 51 resolved · 36 carry a record call.
                                  rate − coin flip
   Record right             19 of 36   ├──────┼──────┤│           n=36
   Narrative right          17 of 36  │├──────┼──────┤            n=36
   Record right, they disagree 18 of 34 ├──────┼──────┤│          n=34
   ░ the zero rule on this board is the coin flip · both right 1 · both wrong 1 · disagree 34 of 36

 ▒ 1 claim awaiting a horizon · 12 logged as hypothetical and never resolved.
 ░ 0 of 20 trading days observed since 2026-09-02; the due date is the date of the 20th trading
 ░ observation, which is not knowable in advance. fred.DCOILBRENTEU ends 2026-08-25.
 ░ ── the price series trails the claim log by about a week; nothing logged in that window resolves.

 ▒ Sources — resolved-true rate. 10 of 12 rows are below n=8 and are hatched, not scored:
        eia.gov · flow          0 of 9   ├────┼────┤│      n=9
        aljazeera.com · flow    8 of 8            │├───┼──┤ n=8
        osw.waw.pl · flow       ▨ insufficient (n=7)
        cnn.com · flow          ▨ insufficient (n=5)
        cnbc.com · level        ▨ insufficient (n=5)
        ░ …7 more hatched. A 100% rate on 8 claims is not a source-quality finding.

 ▶ 14 uncheckable claims — logged, not scored                                        ░collapsed
```

### The same screen, no adequate precedent — `yom_kippur_war_1973`, read at 1973-10-06

The first event in the corpus. Nothing precedes it, so the retrieval returns nothing — not because
the search failed but because point-in-time honesty means there is nothing behind this date.

```
 ░ knowable 1973-10-06 · conflict escalation · the first event in the corpus
 ▓ Nothing in the record precedes this event, so the engine has no reference class.
 ▒ 0 analogs. Best similarity 0.000 against a retrieval threshold of 0.400.
 ▒ The pool is every geopolitical event knowable before 1973-10-06, and it is empty.
 ▨ Is it priced?         — no fan: a comparable set needs at least one comparable event.
 ▨ What is the tail?     — no adequate precedent. This is the state, not a failure of it.
 ▨ Where does it travel? — class-level pass-through only; this event contributes to it,
 ▨                         and is not conditioned on it.
 ░ escalation.py RETRIEVE_MIN 0.400 · COND_SIM 0.500 · COND_MIN_N 8
 ▒ The second and only other case is iran_oilworkers_strike_1978, which fails differently:
 ▒ prior events exist, and the closest scores 0.377 — just under the registered threshold.
 ░ Measured over all 187 geopolitical events read at their own date, 2026-09-03.
```

---

## 6. What each ugly state looks like, collected

The four states that must never look like a bug, and the exact words:

| state | where it is real today | rendering |
|---|---|---|
| **no adequate precedent** | fires for **2 of 187** geopolitical events read at their own date: `yom_kippur_war_1973` (max similarity 0.000, nothing precedes it) and `iran_oilworkers_strike_1978` (0.377 against a 0.400 threshold). A further **23** fall back to the parent class as `thin`. False for Abqaiq, which has 23 analogs | Finding-tier sentence naming *why* none can be computed; never an empty panel |
| **insufficient (n=…)** | 55 of 371 propagation cells; 10 of 12 ledger source rows; `transit_hormuz` n=14 | hatch, never colour; caption `insufficient (n=14): below the registered minimum of 15 events` |
| **a null hop** | 301 of 371 cells; all 4 crude cells for infrastructure_attack | grey bar, zero rule drawn, caption *"The interval crosses zero: no effect distinguishable from none at this sample size."* |
| **uncheckable / never resolves** | 14 uncheckable in the recent window; 12 hypothetical claims | collapsed behind a count with the reason, per Metaculus annulment |
| **no state at t** *(new)* | 262 of 313 events | prose sentence, not a panel: *"No situation field for this event was knowable at t, so the engine read it on class and entities alone."* |

---

## 7. Constraints check

| constraint | how this direction meets it |
|---|---|
| single file | all screens remain in `src/app.html`; no build step |
| no new dependency, no CDN | VSUP grid is ~30 lines of SVG using the existing `HATCH_DEFS` and palette; no library |
| jsdom-testable | every state above is a DOM assertion; `tests/test_ledger_screen.py` is the pattern, and jsdom is now installed so the tests actually run |
| every number one click from source | each block carries its `░` receipt path; the record bar carries the four top-level ones |
| absence language preserved | §2's three states, the zero rule and the plain-words captions are used throughout — and for the first time actually *rendered* on Story, which measurement showed they are not today |
