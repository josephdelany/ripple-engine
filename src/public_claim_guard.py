"""Semantic guard for the authoritative public-product claims."""
import json
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "data" / "structural_surface" / "summary.json"
ABLATION = ROOT / "data" / "structural_surface" / "ablation" / "summary.json"
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
    a = json.loads(ABLATION.read_text())
    d20 = s["diagnostics_non_verdict"]["abnormal"]["20"]
    with (ROOT / "data" / "structural_surface" / "input" / "events.csv").open() as f:
        event_dates = [r["event_date"] for r in csv.DictReader(f)]
    market_surface = a["primary_explanatory"]["market_minus_surface_matched"]
    combined_market = a["primary_explanatory"]["combined_minus_market_matched"]
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
        "market_matched": a["mean_loss"]["market_matched"],
        "surface_matched": a["mean_loss"]["surface_matched"],
        "market_surface_difference": market_surface["mean_diff"],
        "market_surface_ci": market_surface["ci95"],
        "market_surface_holm": market_surface["dm_p_holm"],
        "combined_market_difference": combined_market["mean_diff"],
        "combined_market_ci": combined_market["ci95"],
        "combined_market_holm": combined_market["dm_p_holm"],
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
    ablation = {f"{e['market_matched']:.3f}", f"{e['surface_matched']:.3f}",
                f"{e['market_surface_difference']:.3f}",
                f"{e['market_surface_ci'][0]:.3f}", f"{e['market_surface_ci'][1]:.3f}",
                f"{e['market_surface_holm']:.3f}",
                f"{e['combined_market_difference']:+.3f}",
                f"{e['combined_market_ci'][0]:.3f}", f"{e['combined_market_ci'][1]:+.3f}",
                f"{e['combined_market_holm']:.3f}"}
    required = {
        "README.md": common | {f"{e['uniform']:.3f}"} | intervals | pvalues | ablation,
        "docs/PAPER.md": common | {f"{e['uniform']:.3f}"} | intervals | pvalues | ablation,
        "docs/RESUME.md": common | {f"{e['event_start']}–{e['event_end']}"} | intervals | ablation,
        "SUBMISSION_STATUS.md": common | {f"{e['uniform']:.3f}"} | intervals | ablation,
    }
    prohibited = (
        "beats simple baselines", "predicts oil prices", "validated forecasting skill",
        "structural analogy is validated", "proved historical analogies work",
        "full observable state outperforms", "full geopolitical state outperforms",
        "non-market state does not add demonstrated value",
        "nonmarket state does not add demonstrated value",
        "additional structural information has not yet shown value",
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
                # Match a complete displayed number, not a prefix of a more precise current one
                # (for example stale 8.336 must not flag current ablation value 8.3369).
                if re.search(rf"(?<![0-9.]){re.escape(stale)}(?![0-9])", line):
                    problems.append(f"{name}:{line_no}: superseded value {stale!r} ({why})")
        if name != "docs/RESUME.md":
            lower = body.lower()
            for phrase in prohibited:
                if phrase in lower:
                    problems.append(f"{name}: prohibited overclaim {phrase!r}")
        # Every quantitative public narrative must carry the newly verified boundary: the
        # nonmarket contrast uses event-level aggregation and is not a test of relational state.
        lower = body.lower()
        if "aggregation" not in lower or "relational" not in lower:
            problems.append(f"{name}: missing relational-aggregation qualification")
    return problems


def main():
    problems = violations()
    if problems:
        raise SystemExit("\n".join(problems))
    print("public claims: VERIFIED against central and ablation summaries")


if __name__ == "__main__":
    main()
