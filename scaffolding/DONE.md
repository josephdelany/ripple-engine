# Definition of Done — the Intelligence Desk

The frozen bar for "finished." Every item is met and has evidence. This is the target
the build was held to; if a future change breaks one, it is not done again.

## What it is
A single local web app — `http://127.0.0.1:5050/workbench` — that fuses a news STORY
with the MEASURED market history and the current priced state, and presents one honest,
institutional-grade analytical brief. Built for a non-engineer to use daily and to present.

## Done checklist

**1. Usable end-to-end by a non-engineer.** ✓
- Open the page → the Daily Brief is already there. Type any headline/paragraph/URL → a full
  brief in <1s. Click a Wire item → its brief. Write in Notes, insert the brief's figures,
  export a sourced markdown draft. Search the 296-event corpus. Print/PDF for presenting.

**2. Institutional quality, not "AI slop."** ✓ (two design-critique rounds + fixes)
- Tokenised type scale (no half-pixels), 8px rhythm, luminance-layered surfaces, two-font
  discipline (sans prose / mono numbers), tabular figures, semantic colour double-encoded
  (sign + hue), direct labels, inline SVG charts (CAR curve with event-day rule + SE band,
  diverging cross-asset bars, sparkline), a real masthead, print/PDF tokens for ink-on-paper.

**3. Honest — never fabricates or overclaims.** ✓ (see `BRIEF_STANDARD.md`; enforced in tests)
- BLUF leads with the lift verdict, not a scary number; magnitude stated as size-not-direction
  (with a coin-flip caveat at small n); base rate + bootstrap CI on every conditional stat;
  small-N gates; selection/clustering/confounder disclosures; association-not-cause language;
  expected magnitude, never an occurrence probability; confidence kept separate from likelihood;
  real corpus events only, each sourced; a documented gap (never a guess) when a story doesn't
  classify; the market-wide gap is labelled standing, not restated per story; corroboration
  cannot borrow conviction across unrelated situations.

**4. Robust in a live demo.** ✓ (adversarial QA round + fixes; 20-input sweep, 0 failures)
- Every realistic oil headline classifies (inflected verbs included); off-topic/garbage/empty
  degrade to a clean gap or error box, never a broken half-brief; prediction-market panel is
  oil-topical, de-duplicated, future-dated only; no leaked None/NaN/undefined; charts survive
  degenerate/negative-only data.

**5. Runs on fresh data.** ✓ (pipeline refreshed; as-of surfaced; staleness flagged)
- Data current as of the last daily run; the masthead shows DATA AS OF and flags a stale panel.

**6. Self-operating.** ◐ (documented; install blocked in this environment)
- The daily/hourly launchd jobs keep data fresh; `ops/com.ripple.desk.plist` (KeepAlive) keeps
  the server serving without a Claude session — one-command install in `ops/INSTALL.md`. Not
  auto-installed here (the sandbox blocked persistent-agent install); until installed, run
  `python3 src/backend.py` in a Terminal.

**7. Tested.** ✓
- `tests/test_brief.py` (17), `tests/test_triage.py` (5, incl. inflection regressions),
  `tests/test_workbench.py` (7). Full suite: 173 passed, 1 pre-existing failure
  (`test_st2`: engine_status RED because some live feeds — Yahoo Finance, Polymarket — are
  dead in this environment; a data-source health issue, not the desk. Not weakened.).

## Known limits (honest)
- Keyword classification can mislabel (a labour "strike" reads as an "attack"); the brief shows
  the matched term so it is transparent and challengeable, not silent.
- Secondary live feeds (Yahoo/Polymarket) are dead here → `engine_status` RED; the brief's core
  (Brent/VIX/GPR/OVX/gap + historical cross-asset) does not depend on them.
- The `/workbench` server runs only while its process lives; make it permanent via the launchd
  agent above.
