# What is in the database, and what the experiment actually uses

*2026-09-03. An inventory of collected-but-unused data, and of what can safely be removed. Every
count below is a live query against `data/oil.db` or `git ls-files`, reproducible with the command
printed beside it.*

**Archive scope.** File-count and disk-usage sections describe the complete pre-separation tree at
tag `full-research-archive-2026-09-03`. Public HEAD now retains only the maintained product and audit
evidence. The database/state-coverage analysis remains applicable because it is independently
checked against the committed frozen bundle.

## Summary

The maintained experiment uses **4.3%** of the market data and, of roughly forty collected
geopolitical state variables, **two**. The rest is not missing, corrupt, or unreachable. It is
excluded by one clause in one filter. That is the most important unused asset in this repository
and the reason `docs/PAPER.md` §6 has to say the full-state question is untested.

Separately: `src/` is clean and there is almost nothing to delete there. The disk weight is in
gitignored working data, not in the repository.

## 1. Market data: 769 of 772 series unused

| | series | observations |
|---|---:|---:|
| in `observations` | 772 | 678,280 |
| used by the central experiment | 3 | 29,458 (4.3%) |
| **unused** | **769** | **648,822** |

The experiment reads Brent, WTI and VIX. Also collected and never used: S&P 500 (24,784 obs), the
Treasury curve (`DGS2`/`DGS5`/`DGS10`, ~45,000), the daily Caldara–Iacoviello GPR series
(`GPRD`, `GPRD_ACT`, `GPRD_THREAT`, 15,219 each), dollar crosses, refined-product cracks and
equity names.

```sql
SELECT COUNT(DISTINCT series_id), COUNT(*) FROM observations;
```

This is not waste — most of it was collected for the ripple/propagation study, which was
withdrawn. It is inventory, and it is why the ripple data must not be deleted lightly (§4).

## 2. Geopolitical state: collected in bulk, filtered to almost nothing

`situation_state` holds 11,089 rows across ~50 fields. Coverage is good: most fields carry
**227 to 313 events**. Here is what the registered availability rule leaves:

| field | rows collected | events | rows passing the strict rule |
|---|---:|---:|---:|
| `leader_tenure_days` | 286 | 227 | **286** |
| `leader_change_last_365d` | 286 | 227 | **286** |
| `polity2`, `polity_durable` | 286 each | 227 | **0** |
| `cinc` (COW capability) | 286 | 227 | 2 |
| `milex_cow`, `milper_cow` | 286 each | 227 | 2 each |
| `milex_sipri`, `milex_gdp_share_sipri` | 277 / 286 | 223 / 227 | **0** |
| `coup_last_5y` | 286 | 227 | **0** |
| `mepv_regional_war` | 286 | 227 | **0** |
| `oil_rents_gdp` | 284 | 227 | **0** |
| `ucdp_active_conflicts`, `ucdp_intensity_max` | 586 each | 313 | 3 each |
| `ucdp_battle_deaths` | 512 | 294 | 3 |
| `surplus_capacity_world` | 626 | 313 | **0** |
| `kilian_igrea`, `gpr*_monthly` | 313 / 302 each | 313 / 302 | **0** |
| `unga_ideal_point_distance` (alignment) | 45 | 42 | 2 |
| `atop_defense_pact` (alliance) | 41 | 39 | 11 |

### The single clause that does it

The rule is `entity_id != 'situation' AND obs_date ≤ event_date AND vintage ≤ event_date AND
release ≤ event_date AND retrospective = 0` (`src/structural_surface_experiment.py`,
`strict_panel_rows`). Of the 11,089 committed state rows, 60 are `situation`-coded and excluded by
the first clause, leaving **11,029 panel rows** — the base the experiment's own
`availability_audit` uses. Decomposed over those:

| exclusion reason | rows |
|---|---:|
| `obs_date` after the event | **0** |
| `vintage` after the event | **0** |
| **`release` after the event** | **10,150** |
| `retrospective = 1` | 2,682 |

(Over all 11,089 rows including the 60 `situation` ones, `release` excludes 10,210. The two bases
differ by exactly those 60 rows; the panel base is the one quoted everywhere else in the project,
and the counts here are asserted against `summary.json` in `tests/test_unused_data_inventory.py`.)

**`release ≤ event_date` is doing all the work.** `release` is the release date of the *dataset
version* parsed — Polity5 (2018), COW NMC v7.0, SIPRI, UCDP v26.1 (2026). For an event in 1990,
a dataset released in 2018 fails by 28 years. Under this rule no modern compilation can ever be
admitted for any historical event, so the filter does not measure what an analyst could have
known in 1990; it measures whether *this specific file* existed in 1990.

The two Archigos leader fields survive only because their release metadata was recorded
differently, not because leadership was more knowable than conflict intensity.

That is why the strict count is 671 rows, and why the "structural" arm collapses to four market
fields plus, half the time, two leader fields. **The paper's availability finding is real and
should stand, but it is a finding about dataset release metadata, not about historical
knowability** — §5 already says this ("availability could not be demonstrated", "a feasibility
and metadata finding"). This inventory quantifies which clause is responsible.

### What follows, and what does not

This does **not** license re-running the experiment with a looser filter to get a better answer.
That is exactly the move `INV-6` and the registration exist to prevent, and a rule relaxed after
seeing that the strict one gave a null is not a rule.

What it does establish is that a **prospectively registered** arm using a defensible
contemporaneous-availability rule — for instance, admitting a value whose *observation period*
closed before the event and whose source series was published on a known schedule, rather than
requiring the specific modern file to predate the event — is **feasible on data already
collected**, covering 227+ events. That is the shortest route from "untested" to "tested" for
the project's founding question, and it needs a registration written before it is run. It is
recorded here as an option, not started.

## 3. Housekeeping: what can go, and what cannot

### `src/` is clean — nothing to gain

Of 244 Python files, **12** (36 KB total) have no importer, no test, and no reference in the
Makefile, docs or ops. **None of them should be deleted, and the reason is worth recording,
because the obvious reading of that statistic is wrong.**

Six are 0.3 KB stubs for licence-gated sources (`src/state/{eia_intl,vdem,gsdb,dots,ei_review,nyt}.py`)
that document why a loader cannot run. The other six looked like genuine dead code until they were
opened. They are one-shot analysis scripts, and every one writes a **committed, published** output:

| file | writes | committed? |
|---|---|---|
| `src/engine/abnormal_price.py` | `docs/ABNORMAL_RETURN_RESULT.md` | yes |
| `src/engine/amendment_p_run.py` | `docs/ABNORMAL_RETURN_RESULT.md` | yes |
| `src/engine/diagnostic_basis.py` | cited by `docs/audit/01_TIER1_design_defects.md` | yes |
| `src/cc2_robustness.py` | `data/cc2_seasonal.json` | yes |
| `src/claim_subsets.py` | `data/endogenous_flags.json`, `data/h1_subsets.json` | yes |
| `src/regime_block.py` | `data/h1_regimeblock.json` | yes |

They have no importer because nothing imports a script you run once. Deleting them would leave six
published artifacts with no code that produces them — a published finding whose generator is gone
is the exact provenance defect this repository keeps catching, and `docs/ABNORMAL_RETURN_RESULT.md`
already had one of these (commit `aab9ec1`, its evidence was untracked while a published document
cited it).

**"No importer" is not "dead code" in a research repository. There is nothing to delete in `src/`,
and the 36 KB it would save is not worth the risk of being wrong about which script produced which
number.**

### Tracked files: `data/` is 1,159 of 1,764, but most is load-bearing

| directory | tracked files | size |
|---|---:|---:|
| `data/candidates` | 707 | 2.3 MB |
| `data/structural_surface` | 11 | 29.4 MB |
| `data/walk_forward` | 22 | 17.4 MB |
| `data/ledger` | 23 | 12.7 MB |
| `data/ripple` | 10 | 10.8 MB |

`data/structural_surface` is the maintained product. The other four look like dead legacy weight
and are not: `src/citation_guard.py` declares `data/ripple/irf.json`,
`data/walk_forward/summary.json`, `data/candidates/pre1987_candidates.csv` and others as run
objects, and `data/ripple/irf.json` alone holds 91,161 of the record's 100,961 numeric leaves.
**Deleting them turns published numbers untraceable and breaks the citation guard** — the
opposite of what this project is for. They are evidence, and evidence for withdrawn claims is
still evidence. Move them behind `archive/` if the clutter matters; do not delete them.

### The disk weight is gitignored, not tracked

The working tree is 975 MB; the repository content is ~95 MB.

| path | size | tracked? | verdict |
|---|---:|---|---|
| `data/oil.db` | 240 MB | no | live database, keep |
| `data/backups/` | **199 MB** | no | 11 gzipped snapshots, Aug 1 – Sep 3; **see below** |
| `data/state/raw/` | 119 MB | no | source files for the state loaders, not re-downloadable (§ provenance) — keep |
| `data/candidates/dossiers/` | 96 MB | mostly no | 1,596 files on disk, 707 tracked |
| `data/cache/ucdp_ged_26.1.json` | 38 MB | no | one cached source file, keep |
| `.git` | 119 MB | — | history |

**On the backups.** Before recommending removal I checked whether any of them is the database the
frozen input bundle was exported from — the one `docs/audit/PROVENANCE_BOUNDARY.md` records as
lost. Every snapshot was decompressed and hashed against
`84041119e76371c48e07abbf62e4e60c7e1c995b33560430bad34f84318e1012`:

| snapshot | sha256 (first 12) |
|---|---|
| `oil_20260801_152407` … `oil_20260831_202523` (7 files, 11–13 MB) | none match |
| `oil_2026090{2,3}_*_pre_spine_apply` (4 files, 29 MB each, all within 18 minutes) | none match |

**No match.** The exporting database is genuinely unrecoverable — the last snapshot predates the
bundle export — so the provenance boundary stands as written, and the backups are confirmed not
to hold the one thing that would have made them irreplaceable. The four `pre_spine_apply`
snapshots taken within eighteen minutes of each other are redundant with one another.

```bash
for f in data/backups/*.db.gz; do echo "$(gzip -dc "$f" | shasum -a 256 | cut -c1-12)  $f"; done
```

## 4. Recommended actions, in order of value

1. **Register and run a defensible-availability arm** on the state data already collected (§2).
   This is the only item here that changes what the project can claim. Needs a registration first.
2. **Delete redundant database snapshots** — keep the newest, the oldest, and one `pre_spine_apply`;
   remove the other eight. Saves roughly 150 MB. Irreversible, so it needs Joe's word.
3. **Do not delete anything in `src/`.** The twelve files with no importer are either
   documentation stubs or the one-shot generators of committed outputs (§3). This recommendation
   was the reverse on first draft and was corrected after opening the files.
4. **Do not delete** `data/walk_forward`, `data/ledger`, `data/ripple` or `data/candidates`. They
   are the traceability substrate for every published and withdrawn number, and
   `src/citation_guard.py` declares several of them as run objects. Archive if needed.

The honest total: **the only material, safe saving in this repository is about 150 MB of redundant
database snapshots, which are gitignored and therefore were never slowing down git, tests or
search in the first place.** Nothing that was making the project feel heavy is deletable; what was
making it hard to navigate was 135 unlabelled documents, and those are now labelled and
machine-checked (`src/doc_status_guard.py`).
