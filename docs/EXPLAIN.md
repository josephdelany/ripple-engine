# Saying it out loud

*The versions to have ready. Written to be spoken, not read.*

---

## 20 seconds — what it is

> I tested whether the historical analogies analysts use in geopolitical risk assessment
> actually contain predictive information once you remove hindsight. I built a system that
> retrieves historically similar events and forecasts from what happened next, then ran it
> forward through the record under a strict rule: on any given date it could only see
> information demonstrably available on that date. The signal largely disappeared under
> that rule, and a much simpler baseline beat it.

## 60 seconds — the full arc

> Analysts reason by precedent — *this looks like 1990, not like 2019*. I wanted to know
> whether that reasoning survives being tested, so I built it.
>
> I assembled 313 dated geopolitical and oil-policy shocks from 1973 to 2026, and a
> world-state panel from 27 academic and government datasets — Correlates of War, ICB,
> UCDP, Polity, SIPRI, EIA and so on. For any event, the system finds prior events whose
> world-state was similar, and forecasts escalation and Brent prices from what happened
> after those. Then it walks the whole record forward, sealing each forecast with a hash
> before looking up what actually happened, and scores it against four baselines.
>
> The first results looked promising. Then I enforced the constraint properly: at date *t*
> the model may only use information that was demonstrably available by date *t*. A
> political-risk score published in 2024 describes 2018 accurately but tells you nothing an
> analyst had in 2018. Once that rule bound, 262 of my 313 events turned out to have no
> state information provably available on the day — and the apparent skill vanished.
>
> The most interesting result was the baseline. A rule that just says "this pair of
> countries will keep doing roughly what they've been doing for 90 days" beat my whole
> analogue engine on escalation, and beat it decisively. But on the oil-price side the
> analogues *did* add something over that baseline. So historical analogy may be more
> useful for the market consequences of a shock than for predicting the shock's own
> political trajectory.

## If they ask: "so did it work?"

> Not the way I expected. Under the strict point-in-time test it significantly
> underperformed the base rate for escalation. The more interesting finding is *why* — the
> earlier apparent signal came from state variables that carried information from after the
> forecast date. It did keep an advantage over persistence on the oil-price target.

## If they ask: "why did you build it?"

> I was interested in how much weight historical precedent actually carries in geopolitical
> risk analysis, as opposed to how much it feels like it carries. Someone says a
> confrontation resembles an earlier crisis and everyone nods. I wanted to know whether
> that could be formalised and tested rather than asserted after the fact — and then
> whether the resemblance was even visible at the time.

## If they ask: "what did you learn?"

> Two things. Information timing matters as much as model design — a model can look like
> it's extracting historical structure when it's really consuming variables built with
> later knowledge. And simple baselines are extremely hard to beat: the recent behaviour of
> the same pair of countries outperformed a much more elaborate system.

## If they ask: "did you check whether you'd just asked it the wrong question?"

*This is the answer that separates the project from a negative result someone gave up on.*

> Yes, and I had. Persistence beat the engine by 0.29, but the comparison wasn't fair: I was
> asking the engine to predict the escalation level from scratch while persistence starts
> from the answer. So I re-anchored the identical sealed forecasts — same analogs, same
> weights, nothing re-retrieved — to predict the *change* instead of the level. That moved
> it from 0.769 to 0.480, a dead heat. The entire gap was a missing anchor, not bad
> analogies.
>
> But that fixed the question without changing the answer. Asked properly — does analogy add
> anything once you know where the dyad already stands? — it adds nothing detectable. And
> then I ran one more control, which is the result I'd actually lead with: I swapped the
> retrieved analogues for the plain base rate of that event class, holding everything else
> identical. The base rate did just as well — marginally better, in fact. So the small gain
> that existed was coming from *pooling two distributions*, not from the historical
> similarity. The retrieval step, which is the entire idea of the engine, turned out to be
> interchangeable with the average.

## If they ask: "would more data have fixed it?"

*This is the question every null invites, and it is the one most projects cannot answer.*

> I tested it rather than speculating. I rebuilt the evaluation so the unit of observation was
> a date rather than an event — 476 month-end dates, six price series, five horizons, about
> eleven thousand scored forecasts. The important part is that I computed the *effective*
> sample size rather than quoting the raw count, because overlapping horizons and correlated
> price series mean fifty times the rows is nowhere near fifty times the evidence. It came to
> about two thousand effective observations against two hundred and fifty before.
>
> At that size, actually fitting the model becomes legitimate instead of overfitting. So I
> fitted it — the block weights and the similarity scale, by nested cross-validation where
> every quantity used to choose a parameter had to be knowable at the time. **It didn't beat
> the constants I'd registered by hand.** The difference was two thousandths of a point with a
> p-value of 0.64, and the fitted weights never settled — fifteen different selections across
> four hundred folds. That was a genuine either-way test and it came back saying my registered
> guesses were already about as good as this design gets.
>
> One thing did change, though, and it's the reason I don't describe the project as a flat
> null. At the small sample the engine couldn't be distinguished from drawing historical
> analogies *at random*. At the larger one it can — a small effect, but a real one. So the
> honest verdict isn't "analogy doesn't work." It's that the retrieval step is underpowered and
> its forecasts are too confident, and I can show both with a calibration diagnostic. Getting
> to a more precise negative result is what the extra data bought.

## If they ask: "what would you do next?"

> The binding constraint is sample size — 150 scored reads against about 1,200 needed. I'd
> registered expanding the corpus backwards as the route, and then measured that it doesn't
> work: six pre-1974 records built to full sourcing standard buy zero additional *scored*
> reads, and the pre-1973 oil price isn't a traded series — 16 distinct values in 324 months
> — so there's nothing to forecast. So the route is forwards in density instead of backwards
> in time: make the unit of observation a date rather than an event. Score on a regular grid
> across several horizons and several price series, with escalation labels at the
> dyad-date level. That's a different question, so it gets registered as a new study rather
> than as a patch. It also fixes a selection problem I found but didn't solve — scoring only
> on my chosen events means never testing the engine on the days the market actually moved,
> and 35% of the biggest moves have no event in my corpus at all.

## If they ask: "why only 313 events?"

> Because each one needs a date, an independent outcome I didn't code myself, and a state
> vector restricted to what was knowable then. The corpus was deliberately conservative.
> The historical tail turned out too thin, which is a documented limitation, and I have 624
> pre-1987 candidates screened for the next expansion.

## The terms, in plain English

| term | what to say |
|---|---|
| **Brier score** | Measures how good probabilistic forecasts are. Lower is better. |
| **CRPS** | The same idea for a full predictive distribution rather than a category — it scores the whole forecast distribution, not just the central estimate. |
| **Walk-forward** | At each historical date the model sees only what came before, forecasts, then moves forward. No peeking. |
| **Vintage constraint** | A dataset published in 2024 can't inform a 2018 forecast just because it contains 2018 data. |
| **Persistence baseline** | Assume the recent state of the same relationship continues. The simplest possible competitor. |
| **Climatology** | The base rate — how often each outcome happens overall, ignoring the situation. |
| **Diebold–Mariano** | Tests whether the difference in forecast accuracy between two methods is real or noise. |
| **Reality Check / SPA** | Ask whether the best-looking model among many could just be the result of trying enough models. |
| **Permutation test** | Shuffle the labels and re-run; if the real result looks like the shuffled ones, there's nothing there. |
| **Specification curve** | Re-run the whole test across every defensible combination of settings, so the answer doesn't depend on choices I made. |
| **Calibration** | When it says 30%, does it happen 30% of the time? |
| **PIT** | A check that a predictive *distribution* is the right shape, not just the right centre. |

## One sentence, if that's all there's room for

> I tested whether the historical analogies used in geopolitical risk assessment contain
> out-of-sample predictive information once hindsight is removed — and found that most of
> the apparent signal was hindsight.

---

*Never say: "I proved historical analogy doesn't work." Say: "this implementation, under a
strict point-in-time constraint, did not outperform simple baselines for escalation."*
