"""Generate the exhaustive public-product closure classification."""
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "audit" / "FILE_CLASSIFICATION.csv"

CORE = {
    "README.md", "Makefile", "requirements.txt", "LICENSE", "CITATION.cff",
    "docs/PAPER.md", "docs/RESUME.md", "docs/README.md", "docs/EVENTS_CODEBOOK.md", "docs/DEMO.md",
    "docs/audit/PUBLIC_PRODUCT_CLOSURE.md",
    "registrations/STRUCTURAL_SURFACE_EXPERIMENT.md",
    "src/structural_surface_experiment.py", "src/reproduce_structural_surface.py",
    "src/export_structural_surface_inputs.py", "src/structural_surface_demo.py",
    "src/classify_public_product.py", "src/public_claim_guard.py",
    "tests/test_structural_surface_experiment.py", "tests/test_structural_surface_demo.py",
    "tests/test_public_claim_guard.py", "docs/audit/FILE_CLASSIFICATION.csv",
}
DEPENDENCY = {"src/engine/inference.py", "src/engine/scoring.py",
              "src/engine/__init__.py", "docs/reference/WORLD_STATE_CODEBOOK.md"}
EVIDENCE = {"docs/ABNORMAL_RETURN_RESULT.md"}


def classify(path):
    if path in CORE or path.startswith("data/structural_surface/"):
        return "maintained_core"
    if path in DEPENDENCY:
        return "required_dependency"
    if path in EVIDENCE or path.startswith("docs/audit/"):
        return "evidence_audit"
    if path.startswith(("src/backend", "src/api", "src/terminal", "src/app")) or \
       path.endswith((".html", ".css")) or path.startswith("ops/"):
        return "archive_interface_operations"
    if path.startswith(("scaffolding/", "data/handoffs/")) or \
       path.endswith(".md") or path.startswith("docs/"):
        return "archive_planning_narrative"
    if path.startswith("tests/"):
        return "archive_scientific_tests"
    if path.startswith("data/"):
        return "archive_generated_data"
    return "archive_scientific_code"


def main():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    paths = sorted(set(tracked) | {"src/classify_public_product.py", "docs/audit/FILE_CLASSIFICATION.csv"})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "classification"])
        w.writerows((p, classify(p)) for p in paths)
    print(f"classified {len(paths)} files -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
