# The reproducibility boundary

*2026-09-03. What a reader of this repository can verify for themselves, and where that stops.
Every number below is produced by `python3 src/bundle_provenance.py` or by the command printed
beside it, against committed files.*

## The claim this repository may make

> The frozen central experiment reproduces byte-for-byte from a committed, transparent input
> bundle. The bundle itself cannot be re-derived and checked from a verifiable upstream source.

"Transparent input bundle" is accurate. **"Fully reproducible data pipeline" is not**, and must
not appear in the paper, the README, or any application document.

## What reproduces

`make reproduce-central` rebuilds `reads.jsonl`, `scores.jsonl` and `summary.json` in a temporary
directory from `data/structural_surface/input/` alone — no database, no network, no keys — and
requires SHA-256 equality with `data/structural_surface/manifest.json`. The three committed CSVs
match `bundle_manifest.json` on both hash and row count:

| file | rows | status |
|---|---:|---|
| `events.csv` | 313 | hash and row count match the frozen manifest |
| `market_observations.csv` | 29,458 | hash and row count match the frozen manifest |
| `situation_state.csv` | 11,089 | hash and row count match the frozen manifest |

That is the layer a reader can check, and it is checked on every run of
`src/bundle_provenance.py` and `tests/test_bundle_provenance.py`.

## Where it stops, and why

`bundle_manifest.json` records the SHA-256 of the database the CSVs were exported from
(`src/export_structural_surface_inputs.py`). That database is `data/oil.db`, which is gitignored
and 242 MB. It is not the same database any more:

| measurement | SHA-256 (first 6) |
|---|---|
| recorded in `bundle_manifest.json` at export | `840411…` |
| measured during the external review, 2026-09-03 | `9b5d4f…` |
| measured by `src/bundle_provenance.py`, 2026-09-03 21:4x | `81087e…` |

Three different values on the same day. The file is still being written by other work in this
repository, so **the exporting database no longer exists in a recoverable form**. This is not a
defect in the frozen experiment — the CSVs are the authoritative inputs and they are intact — but
it does mean the export step cannot be re-run and compared. `src/bundle_provenance.py` reports
this as `diverged` rather than passing silently; in a clean clone it reports `absent`.

Rebuilding `data/oil.db` from source would not close the gap either. Of the 11,089 committed
state rows, drawn from 134 distinct recorded sources, **4,717 (42.5%) come from files that must be
obtained by hand** — Stata and Excel distributions that no script in this repository can fetch:

| source | rows |
|---|---:|
| Caldara–Iacoviello GPR monthly export (`data_gpr_export.xls`) | 1,698 |
| EIA global surplus crude capacity 1970–2021 (`figure2.xlsx`) | 626 |
| Archigos v4.1 (`Archigos_4.1_stata14.dta`) | 572 |
| Polity5 (`p5v2018.xls`, local file) | 572 |
| SIPRI Military Expenditure Database (local file) | 563 |
| CSP Coups d'État 1946–2021 (`CSPCoupsAnnualv2021.xls`, local file) | 286 |
| CSP Major Episodes of Political Violence 1946–2018 (`MEPVv2018.xls`, local file) | 286 |
| EIA STEO Table 3d (`STEO_m.xlsx`) | 114 |

The remainder is a mix of free-but-networked (FRED), key-gated (EIA Open Data v2 needs
`EIA_API_KEY`; NYT needs `NYT_API_KEY`), request-gated (GSDB R5 by application) and
scraping-refusing (IMF DOTS) sources, catalogued in the header of `Makefile` and in
`data/gates/release_check_2026-09-02.md` §3. `data/state/raw/` and `data/cache/` are committed
nowhere.

This matters directly to the central result rather than only to the archive. The two panel fields
that enter half of all structural distances, and the one dyadic field that enters three
comparisons, come from exactly this category:

| field used in distances | source | rows |
|---|---|---:|
| `leader_tenure_days` | Archigos v4.1 (`Archigos_4.1_stata14.dta`) | 286 |
| `leader_change_last_365d` | Archigos v4.1 (`Archigos_4.1_stata14.dta`) | 286 |
| `mid_last_date` | COW Dyadic MID 4.03 (`dyadic_mid_4.03.csv`) | 41 |

```bash
python3 -c "
import csv,collections
rows=list(csv.DictReader(open('data/structural_surface/input/situation_state.csv')))
used={'leader_tenure_days','leader_change_last_365d','mid_last_date'}
for (f,s),n in collections.Counter((r['field'],r['source']) for r in rows if r['field'] in used).most_common():
    print(n,f,s)"
```

## What a reader should therefore do

1. **Verify the experiment**: `make reproduce-central`. This is exact and needs nothing but Python.
2. **Verify the inputs are the frozen ones**: `python3 src/bundle_provenance.py`. This is exact.
3. **Do not expect to verify the inputs against their sources.** Each row carries its own `source`,
   `obs_date`, `vintage`, `release` and `retrospective` flag, so a reader can check any individual
   row against the named dataset by obtaining that dataset themselves. That is auditability by
   receipt, not reproduction by pipeline, and the difference is the boundary.

## Relationship to the availability finding

This is a different statement from the paper's §5 availability result, and the two are often
confused. §5 says that only 671 of 11,029 panel-derived rows can *demonstrate* they were knowable
at their event date — a property of the recorded metadata. This document says the *CSV bundle
itself* cannot be rebuilt from its sources by anyone but its author. One is about what the
forecaster could have known; the other is about what a reader can re-run. Both are limits, and
neither implies the other.
