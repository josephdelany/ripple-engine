"""The detector must be unable to see what it will later be compared against.

If `src/disruption_episodes.py` could read the event catalogue or any price series, the
declared-versus-realized comparison would be circular and worthless. That isolation is asserted in
the module docstring, which is worth nothing, so it is enforced here mechanically: the detector's
source and its entire first-party dependency graph are scanned for prohibited access.
"""
import ast
import re
from pathlib import Path

import pytest

import disruption_episodes as D

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Anything that would let detection see events, prices, or the un-committed research database.
FORBIDDEN_TOKENS = (
    "events.csv", "event_entities", "situation_state", "structural_surface",
    "oil.db", "reads.jsonl", "scores.jsonl", "summary.json",
    "DCOILBRENT", "DCOILWTI", "VIXCLS", "brent", "wti", "crps", "abnormal",
)

# Dates and names of well-known episodes. Hard-coding any of them would be tuning by another route.
FORBIDDEN_LITERALS = (
    "2021-03-23", "2021-03-25", "2023-12-01", "2024-01-11", "2026-03-04", "2026-03-02",
    "ever given", "evergiven", "houthi", "hormuz closure", "red sea", "abqaiq",
)


def first_party_dependency_graph(entry: Path):
    """Every module under src/ reachable from the detector, transitively."""
    seen, stack = set(), [entry]
    while stack:
        path = stack.pop()
        if path in seen or not path.exists():
            continue
        seen.add(path)
        tree = ast.parse(path.read_text(encoding="utf-8"))
        names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names += [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module.split(".")[0])
        for name in names:
            candidate = SRC / f"{name}.py"
            if candidate.exists():
                stack.append(candidate)
    return seen


def test_detector_dependency_graph_is_only_itself():
    """The detector imports no first-party module, so its blast radius is one file."""
    graph = first_party_dependency_graph(Path(D.__file__))
    assert graph == {Path(D.__file__)}, \
        f"detector reaches other first-party modules: {sorted(p.name for p in graph)}"


def test_no_prohibited_event_or_price_access_anywhere_in_the_graph():
    """No path to the catalogue, the state panel, the price series, or the research database."""
    for path in first_party_dependency_graph(Path(D.__file__)):
        text = path.read_text(encoding="utf-8").lower()
        # The docstring names what it refuses to touch; strip it before scanning for real use.
        body = re.sub(r'^""".*?"""', "", text, count=1, flags=re.S)
        hits = [t for t in FORBIDDEN_TOKENS if t.lower() in body]
        assert not hits, f"{path.name} references prohibited data: {hits}"


def test_no_famous_episode_is_hard_coded():
    """Parameters must come from the registration and the input's noise, never from an answer."""
    for path in first_party_dependency_graph(Path(D.__file__)):
        text = path.read_text(encoding="utf-8").lower()
        hits = [lit for lit in FORBIDDEN_LITERALS if lit in text]
        assert not hits, f"{path.name} hard-codes a known episode: {hits}"


def test_detector_reads_only_the_path_it_is_given(tmp_path, monkeypatch):
    """Dependency injection, not a hidden default. Detection works with the repo unreadable."""
    csv_path = tmp_path / "slice.csv"
    rows = ["series_id,obs_date,value"]
    import datetime as dt
    for route in D.IMPAIRMENT_ROUTES:
        for i in range(500):
            d = dt.date(2020, 1, 1) + dt.timedelta(days=i)
            rows.append(f"portwatch.{route}.n_tanker,{d.isoformat()},10")
    csv_path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    # Make the real input unreachable: if the detector secretly used it, this would fail.
    monkeypatch.setattr(D, "INPUT", tmp_path / "does_not_exist.csv")
    panel = D.load_panel(csv_path)
    episodes, coverage = D.detect_all(panel)
    assert episodes == []            # flat traffic contains no impairment
    assert set(coverage) == set(D.IMPAIRMENT_ROUTES)


def test_diagnostic_route_is_never_an_impairment_route():
    """Cape of Good Hope is a diversion destination; a fall there is not an impairment (§3)."""
    assert "cape_of_good_hope" in D.DIAGNOSTIC_ROUTES
    assert "cape_of_good_hope" not in D.IMPAIRMENT_ROUTES


def test_registered_parameters_match_the_registration_text():
    """The constants in code must be the ones that were committed before the detector existed."""
    text = (ROOT / "registrations" / "DISRUPTION_REALIZATION.md").read_text(encoding="utf-8")
    assert "R(t) < 0.70" in text and D.THRESHOLD == 0.70
    assert "[t−395, t−31]" in text and D.BASELINE_WINDOW == 365 and D.BASELINE_GAP == 30
    assert D.MIN_IMPAIRED_DAYS == 5 and "at least 5 impaired days" in text
    assert D.MAX_GAP == 2
