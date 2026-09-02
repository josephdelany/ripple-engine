"""nyt.py -- thin module: see stubs.py (nyt_load). Stops with instructions until its input is present."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stubs import nyt_load as load, NYT_FIELDS as FIELDS, NYT_INSTRUCTIONS as INSTRUCTIONS  # noqa: F401,E402

if __name__ == "__main__":
    load()
