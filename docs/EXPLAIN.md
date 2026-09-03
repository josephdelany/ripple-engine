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

## If they ask: "what would you do next?"

> Make persistence the baseline rather than an afterthought. The next experiment asks
> whether historical analogy adds information about the *change* from a dyad's current
> state, rather than replacing it. I'd also expand the pre-1987 corpus — I have 624
> screened candidates — and rebuild the state variables from genuinely contemporaneous
> sources.

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
