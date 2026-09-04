"""Clean-checkout reproducer for the registered component/concentration ablation."""
import hashlib
import json
import tempfile
from pathlib import Path

import structural_component_ablation as A


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    expected = json.loads((A.OUT / "manifest.json").read_text())["outputs"]
    with tempfile.TemporaryDirectory(prefix="ripple-ablation-") as directory:
        out = Path(directory)
        A.run(out_dir=out, n_boot=2000)
        checked = {name: {"expected": digest, "actual": sha(out / name)}
                   for name, digest in expected.items()}
        for record in checked.values():
            record["ok"] = record["expected"] == record["actual"]
        print(json.dumps(checked, indent=2))
        if not all(record["ok"] for record in checked.values()):
            raise SystemExit("component ablation reproduction differs from frozen artifacts")
    print("component ablation reproduction: EXACT")


if __name__ == "__main__":
    main()
