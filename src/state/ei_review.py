"""ei_review.py -- thin module: see stubs.py (ei_load). Stops with instructions until its input is present."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stubs import ei_load as load, EI_FIELDS as FIELDS, EI_INSTRUCTIONS as INSTRUCTIONS  # noqa: F401,E402

if __name__ == "__main__":
    load()
