# Verified sound

*Checked directly against code, not assumed. Several of these are genuine strengths and should be
claimed explicitly — they are unusual.*

**1. The scoring rules are correct.** CRPS is the proper `E|X−y| − ½E|X−X′|`, implemented in
O(n log n) on sorted atoms rather than the n² pairwise matrix. Brier is the multi-category form. RPS
follows Epstein (1969). `skill = 1 − engine/ref` is the standard skill score. *Checked first,
because an error here would invalidate every number in the project. There is none.*

**2. Diebold–Mariano is correctly implemented**, with a proper Harvey–Leybourne–Newbold small-sample
correction `√((T + 1 − 2h + h(h−1)/T)/T)` and two-sided p from t(T−1).

**3. The HAC variance estimator is correct** — Bartlett kernel, weights `1 − j/(lag+1)`.

**4. The stationary bootstrap is correct** — Politis–Romano geometric block lengths with circular
wrapping.

**5. The local projections are modern and correct.** Jordà (2005) with **Montiel Olea &
Plagborg-Møller (2021) lag augmentation**, dependent variable `y[t+h] − y[t−1]`, controls lagged to
t−1, HC1 primary with Newey–West(h) as diagnostic, cluster-collapsed shocks, BH-FDR across the
family. This is better than much published work.

**6. The filtration is honest and the baselines are not rigged.** Baselines draw from the *same*
filtration-constrained pool as the engine (`walk.py:255–296`). The leakage test deliberately breaks
the filtration and demonstrates that scores move.

**7. Sourced-or-unknown is enforced in code, not merely asserted.** `_outcome()` returns
`no_independent_outcome` rather than defaulting a level. `nulls stay null` is implemented.

**8. The test suite is real.** **915 test functions, 2,689 assertions, and zero tests without an
assertion.** Better discipline than most production codebases.

**Also verified:** reproducibility to a content digest across independent runs; registrations
committed before the code they govern (checkable by commit order); four published retractions of the
project's own positive findings.
