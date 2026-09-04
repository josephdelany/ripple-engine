"""Semantic guard for the authoritative public-product claims."""
import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "data" / "structural_surface" / "summary.json"
# SUBMISSION_STATUS.md restates the entire result set and decides whether the product may be called
# ready, so it is guarded exactly like the others. It was unguarded until 2026-09-03.
PUBLIC = (ROOT / "README.md", ROOT / "docs" / "PAPER.md", ROOT / "docs" / "RESUME.md",
          ROOT / "SUBMISSION_STATUS.md")

# Values this project PUBLISHED and then CORRECTED. The guard is otherwise a presence test, so a document
# could carry the current number and a superseded one side by side and still pass -- which is how the
# 2026-09-03 off-by-one in the central target (commits 07b760c, c2dacc4) could have shipped unnoticed.
# Add to this list whenever a published figure is superseded; never remove an entry.
SUPERSEDED = {
    "8.337": "pre-off-by-one structural CRPS (now 8.341)",
    "8.336": "pre-off-by-one structural CRPS, 4sf",
    "8.782": "pre-off-by-one surface CRPS (now 8.784)",
    "8.392": "pre-off-by-one uniform CRPS (now 8.390)",
    "8.391": "pre-off-by-one uniform CRPS, 4sf",
    "-0.446": "pre-off-by-one primary difference (now -0.444)",
    "-0.445": "pre-off-by-one primary difference, 4sf",
    "1.57": "pre-off-by-one primary p-value mantissa (now 8.65)",
    "-0.055": "pre-off-by-one structural-vs-uniform difference (now -0.049)",
    "-0.623": "pre-off-by-one primary CI lower bound (now -0.613)",
    "-0.115": "pre-off-by-one structural-vs-uniform CI lower bound (now -0.112)",
}


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
    # The interval bounds and p-values are the most quotable figures in the paper and were untested until
    # 2026-09-03. `p` renders as a superscripted power of ten, so only its mantissa is matched.
    intervals = {f"{e['ci'][0]:.3f}", f"{e['ci'][1]:.3f}",
                 f"{e['structure_uniform_ci'][0]:.3f}", f"{e['structure_uniform_ci'][1]:.3f}"}
    pvalues = {f"{e['p']:.2e}".split("e")[0], f"{e['structure_uniform_p']:.3f}"}
    required = {
        "README.md": common | {f"{e['uniform']:.3f}"} | intervals | pvalues,
        "docs/PAPER.md": common | {f"{e['uniform']:.3f}"} | intervals | pvalues,
        "docs/RESUME.md": common | {f"{e['event_start']}–{e['event_end']}"} | intervals,
        "SUBMISSION_STATUS.md": common | {f"{e['uniform']:.3f}"} | intervals,
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
        # Exclusivity, not just presence: a superseded figure surviving beside the current one is the
        # failure mode this guard exists to catch. Reported with its line so it can be found.
        current = {v for vals in required.values() for v in vals}
        for line_no, line in enumerate(normalized.splitlines(), 1):
            for stale, why in SUPERSEDED.items():
                if stale in current:
                    continue          # a value that is superseded elsewhere but current here is not stale
                if stale in line:
                    problems.append(f"{name}:{line_no}: superseded value {stale!r} ({why})")
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
