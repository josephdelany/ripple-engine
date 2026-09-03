# Preserved research archive

This directory contains operational components removed from the active submission surface. They are kept for provenance and recovery, not as supported product features or current scientific claims.

`github-workflows/` contains the former daily tracker and 15-minute news watcher. They were moved out of `.github/workflows/` during public-product closure because they fetch live data, publish dashboards, send alerts, and commit generated state. A static research submission must not execute those operations.

The complete pre-closure repository is also recoverable at git tag `closure-core-frozen-2026-09-03`.
