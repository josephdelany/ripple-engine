"""engine/ -- the predictive engine on the state (BUILD_V3 S5-S6; PATH Steps 6-8).

similarity.py  Step 6  block-wise weighted distance over the state vector, point-in-time standardized
read.py        Step 7  the read: G/P/F/M distributions with n, propagation per branch, differencing table
scoring.py     Step 8  strictly proper scores (Brier, log, CRPS, pinball, PIT) in closed form
learning.py    Step 8  the Hedge learning loop over the registered menu
inference.py   Step 8  DM/HLN, stationary block bootstrap, Reality Check / SPA, BH-FDR, permutation, power
Session B owns this package. Session A owns src/state/ (the panel) -- never edited from here.
"""
