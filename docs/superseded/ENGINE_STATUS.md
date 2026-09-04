> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# ENGINE STATUS — where the ripple engine stands

> **SUPERSEDED — 2026-09-03.** This document dates from the project's v1 period (July
> 2026) and describes a "validated" portfolio that no longer exists. Every claim it calls
> validated has since been retracted or downgraded, each by a test registered before it
> ran: **H1** — geopolitical shocks amplifying ~5pp harder under volatility stress — did
> not survive a VIX-matched placebo (`docs/red_team_1.md`); **five of the six**
> stress-amplification propagation edges were retracted under a pre-registered re-test
> (`data/ripple/retraction_six.json`); the propagation chain is silent, with 21 of 477
> cells transmitting against 1–24 expected by chance (`docs/RIPPLE_FINDINGS.md`); and the
> walk-forward engine is significantly **worse** than the base rate on both targets once
> the vintage rule binds (`docs/PAPER_DRAFT.md` §8).
>
> Nothing below has been edited. This project annotates its record; it does not rewrite
> it. For the current state read `README.md`, `docs/PAPER_DRAFT.md` and `EDGE_PORTFOLIO.md`.


*The one-page orientation. For the live machine-readable verdict see `data/engine_status.json`
(`engine_status` MCP tool). For how to use it, `TALKING_TO_IT.md`. For the method, `METHOD.md`.*

## What it is
A validation-first event-study engine: it measures how geopolitical/supply shocks **ripple** through
oil and related markets, **conditioned on market state**, and reports only what survives a real
statistical gate — with honest nulls and airtight receipts. It **feeds you the material**; you write the
read.

## The validated portfolio (claims you can stand behind)
Each is CI-excludes-zero, multiple-testing corrected, and survives leave-one-cluster-out. Receipts:
`data/evidence/<claim_id>.json` (`get_evidence_pack`).

| claim | effect | n | receipt |
|---|---|---|---|
| **H1** — VIX-stress amplifies the oil ripple | +5.0pp [0.8, 8.9] | 86 | `hyp.H1` |
| ripple → **Brent oil** | +5.0% | 86 | `node.brent_oil` |
| ripple → **Heating oil** | +4.3% | 86 | `node.heating_oil` |
| ripple → **5Y breakeven** | +16.7bps | 63 | `node.5y_breakeven` |
| ripple → **S&P 500** | +1.8% | 86 | `node.s&p_500` |
| ripple → **Platinum** | +7.3% | 78 | `node.platinum` |
| ripple → **Product tankers** (supply-chain) | +7.2% | 43 | `node.product_tankers` |
| **copper** under a growth regime | +4.3% | 70 | `edge.copper_growth` |
| **HY credit** under credit stress | +1.7% | 48 | `edge.hy_credit_stress` |

## Suggestive (a lead, not a claim)
- **Mispricing / under-priced-risk** — when the engine flags under-priced risk, realized turbulence
  follows (Wilson [0.69, 0.99] vs 0.52 base, n=14). Small-N, in-sample direction — **never shipped as
  validated**; grows toward a real test as the ledger accrues.

## Honest nulls (reported, not hidden — refusing to chase these is the integrity)
H2 (tight inventories), H3 (positioning), the analogue forecaster (miscalibration, not power),
`chokepoint>sanction` (fairly tested after the clustering fix), natural gas, wheat, CNY/USD, USD, corn,
soybeans, gold/copper miners, dry-bulk freight, most producer→commodity supply-chain edges.

## How it stays sound (inspectable)
- **Negative-control placebo** — shuffling H1's labels collapses the edge (CI spans zero): not signal in
  noise. (`evaluation.json`, `get_evaluation`.)
- **Surface consistency** — the same number is identical across every surface.
- **Pre-registration** — the battery is frozen before results (`PRE_REGISTRATION.md`, git tags); dated
  amendments only.
- **Point-in-time** — state read at t−1; no lookahead (tested).

## Verified-conflict backbone (UCDP)
The gold-standard Uppsala Conflict Data Program feed is integrated ($0, free-token, kept out of the
repo): complete 1989→2025 monthly fatalities (`ucdp.fat_global` + regions). It's used two ways —
(1) a **4th corroboration modality** (`verified_conflict`) that confirms news-sourced conflict situations
against vetted fatality data (logic proven on historical dates; *dormant for the freshest live news*
because UCDP's annual GED lags ~6–18 months — UCDP's monthly *Candidate* set is the recency follow-on);
and (2) a pre-registered **conditioner** (`conflict_intensity_gold`) — honestly **null**, reported not
chased. So the conflict signal is *verified*, not merely news-inferred.

## The living loop (it grows itself, safely)
Live news → **caged LLM extraction** (Cowork worker, no API key) → codebook gate (`load_events.check`) →
corroboration-tiered admission → review queue. It **cannot fabricate** (every admitted event keeps a
real source_url; the LLM's numbers never auto-enter canon; uncertain events queue for you). See
`ops/extract_agent.md`, `get_review_queue`.

## The four surfaces
1. **Text Claude** (MCP, primary) — `orient_on_topic`, `test_hypothesis`, `get_evidence_pack`, … (`TALKING_TO_IT.md`).
2. **Digest** — `data/digest.html` (`./go`).
3. **Cockpit** — OpenBB widgets on `:5050` (`./go`).
4. **Bench** — `python3 src/research.py …`.

## Run it
- `./go --refresh` — pull free data, rebuild the reads, open the digest, start the cockpit.
- Scheduled: `ops/com.ripple.refresh.plist` (daily) + `ops/com.ripple.watch.plist` (hourly news).
- **`python3 src/acceptance.py`** → COMMISSIONED/DEGRADED (the "is it ready?" button).
- **$0 / keyless** engine core; single-user personal tool held to an inspectable quality bar.

*Verdict right now: see `python3 src/status.py`.*
