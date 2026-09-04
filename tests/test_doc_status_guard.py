"""A reader must be able to tell a current claim from a withdrawn one without reading a CSV."""
import pytest

import doc_status_guard as G


def test_every_tracked_markdown_declares_its_status():
    """The whole point: no plausible-looking document is silent about what it is."""
    found = G.problems()
    assert not found, "\n".join(found)


def test_the_public_product_is_not_labelled_superseded():
    """The dangerous direction of the error — the real paper wearing a retraction banner."""
    for path in ("README.md", "docs/PAPER.md", "docs/RESUME.md", "SUBMISSION_STATUS.md"):
        assert G.is_authoritative(path)
        assert not G.BANNER.match(G.first_line(path)), f"{path} carries a status banner"


def test_known_traps_carry_a_banner():
    """The specific files the external review named as easy to mistake for current guidance."""
    for path in ("docs/RIPPLE_FINDINGS.md", "docs/VISION_AND_BUILD.md",
                 "docs/HOW_TO_TALK_ABOUT_IT.md", "docs/README_v2_technical.md",
                 "OPEN_ITEMS.md", "PATH.md", "scaffolding/NORTH_STAR.md"):
        if not (G.ROOT / path).exists():
            continue  # slim public HEAD omits traps preserved at the recovery tag
        assert not G.is_authoritative(path), f"{path} must not be treated as authoritative"
        assert G.BANNER.match(G.first_line(path)), f"{path} has no status banner"


def test_only_the_four_declared_statuses_are_accepted():
    """A free-text banner would let the vocabulary drift back into meaninglessness."""
    assert G.STATUSES == ("SUPERSEDED", "ARCHIVED", "REFERENCE", "WORKING NOTE")
    assert G.BANNER.match("> **SUPERSEDED — NOT A CURRENT CLAIM.** x")
    assert G.BANNER.match("> **ARCHIVED LEGACY REGISTER — NOT CURRENT PROJECT STATUS.** x")
    assert not G.BANNER.match("> **NOTE.** x")
    assert not G.BANNER.match("# A heading")
    assert not G.BANNER.match("Some prose about being archived.")


def test_directories_that_are_their_own_label_are_exempt():
    """`archive/` and `data/` say what they are by location; the guard does not double-label them."""
    assert all(not p.startswith(G.EXEMPT_DIRS) for p in G.tracked_markdown())


def test_guard_exits_nonzero_when_a_banner_is_missing(monkeypatch):
    """The gate must actually fail, not print and pass."""
    monkeypatch.setattr(G, "problems", lambda: ["docs/FAKE.md: no status banner on line 1"])
    with pytest.raises(SystemExit):
        G.main()
