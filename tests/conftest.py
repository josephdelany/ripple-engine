"""Put src/ on the import path so the tests can import the engine modules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
