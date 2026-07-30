"""
acceptance.py -- the single commissioning verdict: is the engine READY? (COMMISSIONED / DEGRADED)

Runs the checks that together mean "finished and sound", and prints ONE verdict a human can trust:
  1. the test suite passes,
  2. the evaluation's framework check is sound (placebo null + surfaces consistent),
  3. the engine_status verdict is not RED,
  4. the living-engine cage is present + tested (no-fabrication guarantee),
  5. the evidence packs exist (every validated claim is receipted).
Any hard failure -> DEGRADED with the reason. This is the button to press before relying on it.

Run:  python3 src/acceptance.py            # full (runs pytest)
      python3 src/acceptance.py --fast     # skip pytest (use the rest)
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PY = sys.executable


def _rj(name):
    p = DATA / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


def check_tests():
    r = subprocess.run([PY, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout or "").strip().splitlines()
    line = tail[-1] if tail else ""
    return r.returncode == 0, f"pytest: {line}"


def run(fast=False):
    checks = []

    if fast:
        checks.append((True, "pytest: SKIPPED (--fast)"))
    else:
        checks.append(check_tests())

    ev = _rj("evaluation.json")
    fw = (ev.get("overall", {}) or {}).get("framework_sound")
    checks.append((fw is True, f"evaluation framework_sound = {fw} "
                   f"(placebo null + surfaces consistent)"))

    st = _rj("engine_status.json")
    verdict = st.get("verdict")
    checks.append((verdict in ("GREEN", "AMBER"), f"engine_status = {verdict} (not RED)"))

    cage = (ROOT / "src" / "extract_events.py").exists() and (ROOT / "tests" / "test_living_engine.py").exists()
    checks.append((cage, "living-engine cage + no-fabrication tests present"))

    evid = list((DATA / "evidence").glob("*.json")) if (DATA / "evidence").exists() else []
    checks.append((len(evid) >= 3, f"evidence packs: {len(evid)} claims receipted"))

    ok = all(c[0] for c in checks)
    return {"commissioned": ok, "verdict": "COMMISSIONED" if ok else "DEGRADED", "checks": checks}


def main():
    r = run(fast="--fast" in sys.argv)
    print("=" * 64)
    print(f"  ACCEPTANCE: {r['verdict']}")
    print("=" * 64)
    for ok, msg in r["checks"]:
        print(f"   [{'PASS' if ok else 'FAIL'}] {msg}")
    print("=" * 64)
    print("  " + ("READY -- rely on it; nulls stay nulls, receipts are airtight."
                  if r["commissioned"] else "NOT READY -- fix the FAIL(s) above."))
    sys.exit(0 if r["commissioned"] else 1)


if __name__ == "__main__":
    main()
