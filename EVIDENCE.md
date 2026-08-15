# EVIDENCE — every claim, one hop from its receipt

> **Red-team-1 (R7): the `validated` set is empty.** Under the single evidentiary bar (`EVALUATION.md` §0: SAR-standardized + regime-block-robust CI excluding zero + permutation-FDR) every claim below is **SUGGESTIVE**, not validated. The packs are kept — publishing a downgrade with its receipts is the integrity evidence. Numbers reconcile in `data/NUMBERS.md`; full disposition in `docs/red_team_1.md`.

Each claim has a machine pack at `data/evidence/<claim_id>.json` with its exact underlying episodes (event ids + dates + source URLs), CI, method, and commit hashes. Nulls are reported in `EDGE_PORTFOLIO.md` / `evaluation.json`.

| claim_id | tier | quantity | n | receipt |
|---|---|---|---|---|
| `edge.CC2_supply_gasoline_crack` | [SUGGESTIVE] | 2.9611$/bbl | 37 | `data/evidence/edge.CC2_supply_gasoline_crack.json` |
| `edge.CC5_fertilizer_corn` | [SUGGESTIVE] | 0.3631beta | 0 | `data/evidence/edge.CC5_fertilizer_corn.json` |
| `edge.copper_growth` | [SUGGESTIVE] | 3.8163% | 71 | `data/evidence/edge.copper_growth.json` |
| `edge.hy_credit_stress` | [SUGGESTIVE] | 1.4854% | 49 | `data/evidence/edge.hy_credit_stress.json` |
| `edge.palladium_supply` | [SUGGESTIVE] | 5.2181% | 75 | `data/evidence/edge.palladium_supply.json` |
| `hyp.H1` | [SUGGESTIVE] | 0.2524sigmas (BMP-standardized SCAR) | 87 | `data/evidence/hyp.H1.json` |
| `node.5y_breakeven` | [SUGGESTIVE] | 16.7429bps | 64 | `data/evidence/node.5y_breakeven.json` |
| `node.brent_oil` | [SUGGESTIVE] | 5.5615% | 87 | `data/evidence/node.brent_oil.json` |
| `node.heating_oil` | [SUGGESTIVE] | 5.5688% | 87 | `data/evidence/node.heating_oil.json` |
| `node.palladium` | [SUGGESTIVE] | 5.2181% | 75 | `data/evidence/node.palladium.json` |
| `node.platinum` | [SUGGESTIVE] | 7.2205% | 79 | `data/evidence/node.platinum.json` |
| `node.product_tankers` | [SUGGESTIVE] | 7.234% | 43 | `data/evidence/node.product_tankers.json` |
| `node.s&p_500` | [SUGGESTIVE] | 2.1192% | 87 | `data/evidence/node.s&p_500.json` |

*13 claims, all SUGGESTIVE post red-team-1. Every number is reproducible: `./repro.sh` rebuilds `oil.db` from zero, then the producer script regenerates the artifact.*
