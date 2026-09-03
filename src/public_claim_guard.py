"""Semantic guard for the authoritative public-product claims."""
import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "data" / "structural_surface" / "summary.json"
PUBLIC = (ROOT / "README.md", ROOT / "docs" / "PAPER.md", ROOT / "docs" / "RESUME.md")


def evidence():
    s = json.loads(SUMMARY.read_text())
    d20 = s["diagnostics_non_verdict"]["abnormal"]["20"]
    with (ROOT / "data" / "structural_surface" / "input" / "events.csv").open() as f:
        event_dates = [r["event_date"] for r in csv.DictReader(f)]
    return {
        "n": s["n_inferential_dates"],
        "structural": s["mean_loss"]["structural"],
        "surface": s["mean_loss"]["surface"],
        "difference": s["mean_loss_diff_structural_minus_surface"],
        "ci": s["ci95"],
        "p": s["dm"]["p_value"],
        "uniform": d20["structural_vs_uniform"]["mean_b"],
        "structure_uniform_difference": d20["structural_vs_uniform"]["mean_diff"],
        "structure_uniform_ci": d20["structural_vs_uniform"]["ci95"],
        "structure_uniform_p": d20["structural_vs_uniform"]["dm"]["p_value"],
        "surface_uniform_difference": d20["surface_vs_uniform"]["mean_diff"],
        "event_start": min(event_dates)[:4],
        "event_end": max(event_dates)[:4],
    }


def text():
    return {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PUBLIC}


def violations():
    e, docs = evidence(), text()
    common = {f"{e['n']}", f"{e['structural']:.3f}", f"{e['surface']:.3f}",
              f"{e['difference']:.3f}", f"{e['structure_uniform_difference']:.3f}"}
    required = {
        "README.md": common | {f"{e['uniform']:.3f}"},
        "docs/PAPER.md": common | {f"{e['uniform']:.3f}"},
        "docs/RESUME.md": common | {f"{e['event_start']}–{e['event_end']}"},
    }
    prohibited = (
        "beats simple baselines", "predicts oil prices", "validated forecasting skill",
        "structural analogy is validated", "proved historical analogies work",
    )
    problems = []
    for name, body in docs.items():
        normalized = body.replace("−", "-")
        missing = sorted(x for x in required[name] if x not in normalized)
        if missing:
            problems.append(f"{name}: missing frozen values {missing}")
        if name != "docs/RESUME.md":
            lower = body.lower()
            for phrase in prohibited:
                if phrase in lower:
                    problems.append(f"{name}: prohibited overclaim {phrase!r}")
    return problems


def main():
    problems = violations()
    if problems:
        raise SystemExit("\n".join(problems))
    print("public claims: VERIFIED against data/structural_surface/summary.json")


if __name__ == "__main__":
    main()
