# data/state/local — licence-restricted inputs (never committed)

Loaders in `src/state/` read these files from this directory; the repo ships loaders, not files
(WORLD_STATE_SOURCES.md §6, BUILD_V3.md §4). Everything here except this README is gitignored.
If a file is absent its loader stops with instructions and its test is skipped, never faked.

| directory | file(s) | how to obtain | licence |
|---|---|---|---|
| `csp/` | `p5v2018.xls`, `CSPCoupsAnnualv2021.xls`, `MEPVv2018.xls` | https://www.systemicpeace.org/inscrdata.html (direct links on the page) | copyrighted; reproduction/redistribution prohibited without written permission — cite CSP/INSCR |
| `sipri/` | `SIPRI-Milex-data-1949-2025_v1.2.xlsx` (or the current file from the milex page) | https://www.sipri.org/databases/milex | SIPRI user terms; citation required |
| `gsdb/` | `GSDB_V5_dyadic.csv` (name as delivered) | request form at https://www.globalsanctionsdatabase.com/ (24 h; project title; non-commercial) — Joe | do not redistribute |
| `nyt/` | — (uses the `NYT_API_KEY` environment variable, never a file) | https://developer.nytimes.com/ free key | API terms |
| `ei/` | `EI-Stats-Review-ALL-data.xlsx` (2025 archive) or the 2026 file from the email gate | https://www.energyinst.org/statistical-review/resources-and-data-downloads | free public good; cite Energy Institute |
| `eia/` | — (uses the `EIA_API_KEY` environment variable) | https://www.eia.gov/opendata/ free registration | public domain |
