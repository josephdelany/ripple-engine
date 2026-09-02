# Data licences

Code and project documents: MIT (`LICENSE`). Data: each source under its own
terms. The verified register with URLs, variables, coverage and retrieval dates is
`WORLD_STATE_SOURCES.md` (world state) and, when it lands, `RIPPLE_SOURCES.md`
(ripple). This page is the licence view only.

## Committed to the repository (free, redistributable with citation)

| Source | Use here | Terms as recorded in the register |
|---|---|---|
| FRED (Federal Reserve Bank of St. Louis) | price spine, rates, FX, breakevens, VIX; seed `data/seed/wtisplc_monthly.txt` | FRED terms of use; series republished with attribution |
| Correlates of War — NMC v7, MID 5, War | actors, dyads, IES-90 | free with citation |
| ATOP 5.1 | alliances | free with citation |
| ICB v16 | crises, IES-90 | free with citation |
| UCDP 26.1 (GED, dyadic) | conflicts, IES-90 | CC BY |
| V-Dem v16 | regime fields | CC BY-SA |
| GPR / GPRH (Caldara & Iacoviello) | system block, placebo matching | CC BY |
| EIA | surplus capacity, NYMEX curves, weekly physical series | US public domain |
| Kilian index of global real economic activity | market block | cite |
| Energy Institute Statistical Review | production/consumption | cite; the 2026 xlsx obtained through the email gate stays local |
| UNGA ideal points (Voeten) | system block | cite |
| World Bank WDI | country fields | CC BY 4.0 |
| Archigos | leaders | cite |
| IMF PortWatch (when loaded) | chokepoint transits | open, cite |
| JODI-Oil (when loaded) | monthly physical | open, cite |
| World Bank Commodity Price Data (when loaded) | monthly LNG, fertilizer | CC BY 4.0 |

## Held locally, git-ignored, never committed

| Source | Reason |
|---|---|
| Center for Systemic Peace — Polity5, Coups, MEPV | redistribution prohibited |
| Global Sanctions Data Base (GSDB R5) | by request, non-commercial; obtained by the author |
| SIPRI | terms of use |
| NYT Archive API responses | API terms |
| Energy Institute 2026 workbook | email-gated download |
| Baltic Exchange tanker indices | licensed; not obtained — recorded as a gap |

The loaders refuse to write these to a tracked path; `.gitignore` covers their
directories; the release check (`data/gates/release_check_*.md`) asserts none is
tracked.

## What the licences do not permit us to do

Redistribute CSP or GSDB rows; commit NYT text; present Baltic index values we do
not have. Where a number would require one of these, the project writes
"unknown" or "gap", never an estimate.
