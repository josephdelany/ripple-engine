# Evidence pack -- flagship

_Frozen numbers this paper cites, copied verbatim from committed results files. Each is stamped with its source file and the git commit hash of the run that produced it. No number here is retyped or recomputed._

## Registered verdict (n=20, confirmatory)
_source: `data/registered_run_results.txt` @ commit `16e6c01`_
```
H1 HOLDS (clustered +10.3 pp in predicted direction)
H2 HOLDS (clustered +5.4 pp in predicted direction)
H3 FAILS (clustered -6.8 pp in predicted direction)
```

## Expanded-sample verdict (n=30, alongside)
_source: `data/expanded_run_results.txt` @ commit `2233d3c`_
```
H1   HOLDS (+10.3 pp)                  HOLDS (+8.8 pp)
H2   HOLDS (+5.4 pp)                   HOLDS (+6.3 pp)
H3   FAILS (-6.8 pp)                   FAILS (-3.7 pp)
```

## Conflict-escalation Brent ripple (clustered)
_source: `data/cross_asset_results.txt` @ commit `5bab18c`_
```
conflict_escalation      15         -2.2%       -0.1%       +0.5%     -1.7bps     -1.4bps       -0.9%
conflict_escalation      15         +1.5%       +0.0%       +0.6%     +0.3bps     +2.3bps       -0.3%
conflict_escalation      13     -0.3%     +0.4%     -0.9%
```

## H1 under standardization (robustness lens)
_source: `data/inference_results.txt` @ commit `1ea3b3e`_
```
H1 (VIX) read: the amplification stays in the predicted direction after removing each event's own volatility (+0.56 sigma), so it is not purely volatility clustering -- but its permutation significance weakens from p=0.0225 (raw) to p=0.1201 (standardized), so at this sample size the standardized effect is suggestive, not conclusive.
```

