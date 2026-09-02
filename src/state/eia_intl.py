"""eia_intl.py -- thin module: see stubs.py (eia_intl_load). Stops with instructions until its input is present."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stubs import eia_intl_load as load, EIA_INTL_FIELDS as FIELDS, EIA_INTL_INSTRUCTIONS as INSTRUCTIONS  # noqa: F401,E402

if __name__ == "__main__":
    load()
