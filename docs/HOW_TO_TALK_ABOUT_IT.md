# The project: what it is, how to run it, what it found, and how to say it

*2026-09-03. Every figure verified against a named file. Written to be spoken from.*

---

## 1. The description — the canonical paragraph

> **The Ripple Engine** asks whether the reasoning analysts actually use about oil — *this crisis
> looks like 1990, not 2019* — carries real predictive information once it is formalised and tested
> under honest constraints. It is built as a catastrophe model over the petroleum complex: a
> **hazard** module of 313 dated geopolitical and policy shocks from 1956 to 2026 with
> reference-class retrieval, a **financial** module tracing propagation across 53 nodes from crude
> through refined products, cracks, gas, fertilizer and freight, and an **exposure** module carrying
> physical magnitude. Its governing discipline is point-in-time: every forecast is sealed by
> cryptographic hash before its outcome is looked up, and no variable may enter a read unless it was
> demonstrably knowable on that date. The purpose was to build a working instrument; the result is a
> measured account of why one cannot yet be built from public data. Analogical forecasting requires
> three conditions — an observable state, a reference pool dense enough for "similar" to mean
> something, and a target not dominated by its own autocorrelation — and all three fail here, most
> starkly in that **262 of 313 events carry no state variable provably available on the day**;
> enforcing that constraint erased the apparent skill entirely, because the signal had been
> hindsight. Two further results locate the failure precisely: dated event-occurrence flags carry no
> information about the *size* of a market response once the market's own revision in expectations
> is controlled for, and an attempt to replace them with physical capacity-at-risk reached a complete
> record for only **5 of 80** disruptions — defeated by belligerents contesting exactly the two
> fields that matter, incompatible national reporting units, restoration announced as forecast rather
> than confirmed, and closed archives. What it delivers, and defends: a working three-module
> instrument with an operator-supplied exposure layer, four published retractions of its own positive
> findings, and a specification of what a validated version would require.

---

## 2. How to use it

**Reproduce the whole result from source.**
```
make reproduce          # rebuilds summary.json under the full registered draws
pytest -q               # the gate; refuses to report green if it did not actually run
```

**Open the desk.**
```
./go                    # refresh, rebuild, serve at http://127.0.0.1:5050/app
```

**Grade the label audit** — the one human-in-the-loop gate, blind by construction.
```
python3 src/audit_ies90.py
```

**Run a live read — this is the instrument.** Supply an exposure; get a distribution.
```
python3 src/read_exposure.py --exposure <file.json>
```
It searches all 80 historical cases, retrieves comparables **by exposure similarity**, and returns
the duration and price/margin distributions with the *n* behind each and the reference class named.
Two worked examples are committed: `data/exposure/reads/abqaiq_2019_heldout.md` (a held-out
historical case) and `ras_tanura_scenario.md` (a live scenario).

**What it will refuse to do.** It returns historical frequencies with their *n*, never an occurrence
probability. Below five comparable cases it returns `no adequate precedent` as a first-class answer
rather than a thin number. Any figure without a source and a date stays `unknown`.

---

## 3. The findings — technical

**Primary result.** Escalation Brier skill against the base rate **−0.084, 95% CI [−0.175, +0.004],
DM *p* = 0.076, n = 100** on the Amendment 4 target — worse than climatology, though the interval
crosses zero at this sample size. On price the engine *is* significantly worse than the base rate
(**−0.074, CI [−0.140, −0.021], *p* = 0.011, n = 246**). Its one surviving win is against
persistence on price: **+0.134, CI [+0.076, +0.193], *p* < 0.001** — the only result stable in sign
across every run.

**The mechanism.** Amendment H enforced a vintage rule on the per-event state fields, revealing
**262 of 313 events with no situation field knowable at *t***; retrieval falls back to the market
block alone and the earlier apparent parity disappears. Measured minimum detectable skill is
**0.137** at n = 100, so the null is informative about large effects and uninformative about small
ones — stated beside every headline rather than buried.

**The instrument result.** On the 44 days that are both a corpus OPEC event and a Känzig (2021)
announcement, four regressors differing only in what they say about the same days: the 0/1 flag
gives **−1.572 [−5.423, +2.279]**, covering zero; a continuous measure gives **+2.230 [+0.809,
+3.651]**, excluding zero; with both present the flag **collapses to −0.483**.

**The physical attempt.** Six researchers, disjoint blocks, one absolute sourcing rule:
**5 COMPLETE of 80 (6%)** against a registered gate of 30. Six independently encountered walls,
including that ~40% of in-scope events have no point asset and that restoration is announced as
forecast — which defeated even Abqaiq, the best-documented case in the corpus.

**Cross-asset.** Geopolitical and military classes coincide with top-5% **diesel-crack** moves
**1.9–2.5×** more often than with top-5% **crude** moves; OPEC decisions and demand shocks invert.
Red Sea 2024: Bab el-Mandeb flow **−56.6%**, Cape reroutes **+101.8%**, Brent **−4.9%**. Hormuz
2026: flow **−92.3%**, reroute **+20.7%**, Brent **+48.5%**.

**Integrity.** Pre-registration verifiable by commit order; sealed reads hashed before outcome
lookup; four baselines; DM/HLN, stationary bootstrap, SPA, permutation, BH-FDR, matched placebo,
regime blocks, a 162-cell specification curve negative in all 162; a filtration audit of **15,241**
point-in-time checks with zero violations; reproducibility to a content digest; **four published
retractions** of the project's own positive findings.

---

## 4. The findings — in plain words

**The question.** People who analyse oil markets reason by precedent. *This looks like 1990.* It's
everywhere in the field and almost nobody checks whether it works. I wanted to check.

**The catch, and it turned out to be the whole story.** To test the reasoning you have to be strict
about *when* you knew things. A political-risk score published in 2024 describes 2018 accurately and
tells you nothing an analyst had in 2018. When I enforced that rule properly, **most of my events
turned out to have no usable information available on the day at all** — and the skill I thought I
had measured vanished with it. It had been hindsight.

**The second thing, which is the useful one.** Everyone codes these events as a flag: *a sanctions
event happened, yes or no.* But two OPEC announcements both get a "1" whether one repriced the whole
curve or was completely expected. The flag throws away the only thing that varies. I showed this on
44 days where I could compare the flag against a continuous measure of the very same events: the
flag carried nothing, and it collapsed the moment the continuous measure was included.

**So I tried to build the missing measure — barrels at risk — and I couldn't.** Not because it was
expensive or slow. Because it isn't public. Attacker and operator contest exactly the two numbers
that matter. Russian refineries publish capacity in tonnes a year, Western sources convert to
barrels a day at a factor nobody states. Restoration is always announced as a forecast and almost
never confirmed. Even Saudi Aramco — the most transparent operator involved — never published the
date Abqaiq was actually back to full. I got a complete record for five events out of eighty.

**What I did find.** Geopolitical shocks don't show up where people look for them. They show up in
**refining margins**, not in the crude price — two to two and a half times more often. And a
chokepoint closure only moves price if the ships can't go around: the Red Sea closed, tankers went
round the Cape, and Brent *fell*. Hormuz closed, there is no way around, and Brent rose 48%.

**The honest summary.** Historical analogy, done systematically and tested honestly, didn't beat
simple rules on my data. But I can say precisely why, in three measured ways, and one of those
reasons — that the standard way of encoding these events throws away the magnitude — is a problem
for anyone selling geopolitical risk analytics, not just for me.

---

## 5. How to say it — your framing, cleaned up

Your own phrasing had the right spine. Keep the last clause especially; it explains why a history
major built this and a finance major didn't.

**Ten seconds:**
> I built a system to test whether the historical analogies people use in geopolitical risk analysis
> actually predict anything, because I'm suspicious of how vaguely history gets applied.

**Sixty seconds:**
> I'm a history major, and something bothered me: analysts constantly reason from precedent — *this
> looks like 1990* — and it's almost never tested. It's vague and it's subjective, and I wanted to
> know whether it survives being made precise.
>
> So I built the instrument. 313 dated shocks back to 1956, a world-state panel from 27 academic and
> government datasets, and a strict rule that the model may only use what was demonstrably knowable
> on the day it forecasts. I combined my own technical exposure and research work with **directed
> and reviewed parallel AI engineering sessions under a registration discipline** — every amendment
> committed before the code it governed, so the record can prove nothing was decided after seeing a
> number.
>
> The answer was no, and the reason is the interesting part: most of my events had no information
> provably available at the time, so what looked like skill was hindsight. And the way the whole
> field encodes these events — a flag saying something happened — throws away the magnitude, which I
> showed directly. When I tried to build the physical replacement, barrels at risk, I could only get
> a complete record for five events out of eighty, because the parties involved contest exactly the
> numbers you need.

**Written, for an application:**
> I designed and built a pre-registered forecasting instrument over the petroleum complex to test a
> claim my own discipline relies on and rarely examines: that historical precedent predicts how
> markets respond to geopolitical events. I combined technical exposure with research design,
> executed through directed and reviewed parallel AI engineering sessions under a registration
> discipline where every amendment was committed before the code it governed. The result was
> negative and specific — enforcing a point-in-time constraint showed most events carried no
> information available at the time, and the apparent signal was hindsight — and it produced two
> findings with commercial relevance: that geopolitical shocks land in refining margins rather than
> crude flat price, and that the event-flag encoding used across geopolitical risk analytics carries
> no information about the size of a response. I published four retractions of my own positive
> findings in the course of it.

**What not to say.** Don't say you proved historical analogy fails; say this implementation, under a
strict point-in-time constraint, did not outperform simple baselines, and name the three conditions
that failed. Don't say you built it alone; the orchestration framing is both accurate and more
interesting. Don't call it validated — the label audit is the gate and it is yours to close.
