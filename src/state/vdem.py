"""vdem.py -- thin module: see stubs.py (vdem_load). Stops with instructions until its input is present."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stubs import vdem_load as load, VDEM_FIELDS as FIELDS, VDEM_INSTRUCTIONS as INSTRUCTIONS  # noqa: F401,E402

if __name__ == "__main__":
    load()
