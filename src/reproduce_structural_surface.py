"""Clean-clone reproducer for the frozen central experiment."""
import hashlib
import json
import tempfile
from pathlib import Path

import structural_surface_experiment as E

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "data" / "structural_surface"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    expected = json.loads((FROZEN / "manifest.json").read_text())["outputs"]
    with tempfile.TemporaryDirectory(prefix="ripple-central-") as d:
        out = Path(d)
        E.run(bundle=FROZEN / "input", out_dir=out, n_boot=2000)
        checked = {}
        for name in ("reads.jsonl", "scores.jsonl", "summary.json"):
            got = sha(out / name)
            want = expected[name]
            checked[name] = {"expected": want, "actual": got, "ok": got == want}
        print(json.dumps(checked, indent=2))
        if not all(x["ok"] for x in checked.values()):
            raise SystemExit("central experiment reproduction differs from frozen artifacts")
    print("central experiment reproduction: EXACT")


if __name__ == "__main__":
    main()
