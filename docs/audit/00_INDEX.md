# Audit evidence index

This directory contains only evidence needed to understand or verify the maintained public
research product. The complete six-week audit, superseded papers, experiments, tests, generated
artifacts, and planning history remain at git tag `full-research-archive-2026-09-03`.

- [`01_TIER1_design_defects.md`](01_TIER1_design_defects.md) records the estimand mismatches that
  forced withdrawal of the legacy price, candidate-pool, escalation, and availability claims.
- [`04_verified_sound.md`](04_verified_sound.md) records the scoring and inference components
  checked directly against their implementations.
- [`PROVENANCE_BOUNDARY.md`](PROVENANCE_BOUNDARY.md) distinguishes exact bundle reproduction from
  the upstream source-data chain that cannot be recreated from this repository alone.
- [`UNUSED_DATA_INVENTORY.md`](UNUSED_DATA_INVENTORY.md) explains why the available geopolitical
  fields did not enter the maintained computation at scale. Its legacy file-count inventory refers
  to the archive tag, not public HEAD.
- [`PUBLIC_PRODUCT_CLOSURE.md`](PUBLIC_PRODUCT_CLOSURE.md) records the public/archive boundary and
  verification history.
- [`FILE_CLASSIFICATION.csv`](FILE_CLASSIFICATION.csv) classifies every file retained in public
  HEAD. The archive tag contains the earlier exhaustive 1,770-file classification.

The authoritative result and limitations are in [`../PAPER.md`](../PAPER.md). This audit evidence
does not create additional current findings.
