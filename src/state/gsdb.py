"""gsdb.py -- thin module: see stubs.py (gsdb_load). Stops with instructions until its input is present."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stubs import gsdb_load as load, GSDB_FIELDS as FIELDS, GSDB_INSTRUCTIONS as INSTRUCTIONS  # noqa: F401,E402

if __name__ == "__main__":
    load()
