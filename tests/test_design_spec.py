"""DESIGN.md, the rules checkable without a browser or a database.

DESIGN.md Amendment 1 A1.3: nothing in the spec would have been verified in CI — both jsdom tests skip where node is
absent, and the render test additionally skips whenever data/oil.db is, which is always in CI. "A rule that can only
be checked where the checker never runs is not a rule." So the spec's rules split: this file is static and runs
everywhere (it is listed in conftest's DB_FREE_FILES and needs neither node nor a database); the jsdom tests carry
the DOM-structure rules and may skip.

Each test names the section of DESIGN.md it enforces.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src" / "app.html"
BIG = ROOT / "src" / "big_moves.html"
DESIGN = ROOT / "DESIGN.md"

# §6: no word stronger than the record. Amendment 1 A1.2 splits the rule -- absolute for strings the desk writes
# itself, inventoried for verbatim quoted material.
BANNED = ("predicts", "validated", "signal", "confirms")
BANNED_RE = re.compile(r"\b(" + "|".join(BANNED) + r")\b", re.I)


def app():
    return APP.read_text()


def palette():
    """The CSS custom properties declared in :root, as {name: #rrggbb}."""
    return dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", app()))


def _luminance(hex_colour):
    h = hex_colour.lstrip("#")
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = _luminance(a), _luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# --- §4 typography and contrast ------------------------------------------------------------------------------

def test_the_three_tiers_meet_the_contrast_the_spec_requires():
    """§4, and Amendment 1 A1.1: measured from the palette, never trusted from the hex. The spec's own Provenance
    value failed this at 3.65 when it was written; a test that reads the file is why that was found."""
    p = palette()
    ground = p["bg"]
    required = {"t": 12.0, "t2": 7.0, "t3": 4.5}          # Finding, Evidence, Provenance
    for name, need in required.items():
        got = contrast(ground, p[name])
        assert got >= need, f"--{name} {p[name]} measures {got:.2f}:1 against {ground}, needs {need}:1"


def test_numbers_are_never_in_a_proportional_face():
    """§4: one typeface for prose, one for figures, tabular numerals."""
    css = app()
    assert "tabular-nums" in css, "figures must be tabular so decimals align down a column"
    assert re.search(r"\.num\s*\{[^}]*var\(--mono\)", css), ".num must render in the mono face"
    assert "--mono:" in css and "--sans:" in css


# --- §2 the absence language ---------------------------------------------------------------------------------

def test_amber_and_green_exist_and_the_ground_and_tiers_are_declared():
    """§2/§6: the permitted palette is ground, three text tiers, amber, green, and the hatch."""
    p = palette()
    for required in ("bg", "t", "t2", "t3", "hot", "cool"):
        assert required in p, f"--{required} is missing from :root"


# --- §6 vocabulary -------------------------------------------------------------------------------------------

def _desk_written_strings(html):
    """Every literal the desk writes itself: HTML text nodes outside <script>/<style>, plus the string and template
    literals inside the script. Data the page receives at runtime is not here -- that is what the jsdom inventory
    test covers (Amendment 1 A1.2)."""
    body = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html)
    text_nodes = re.sub(r"<[^>]+>", " ", body)
    script = "\n".join(re.findall(r"<script>([\s\S]*?)</script>", html))
    script = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", " ", script)          # comments are not rendered
    # A build-time data embed (big_moves_page.py writes `const D={...}` on one line) is the RECORD, not the desk's
    # copy: it carries corpus titles verbatim. Amendment 1 A1.2 inventories those, so they are not scanned here.
    script = re.sub(r"^\s*const\s+[A-Z]\w*\s*=\s*[\[{].*$", " ", script, flags=re.M)
    literals = re.findall(r"'([^'\\\n]*)'|\"([^\"\\\n]*)\"|`([^`\\]*)`", script)
    return text_nodes + " " + " ".join(x for tup in literals for x in tup)


@pytest.mark.parametrize("page", [APP, BIG])
def test_the_desk_never_writes_a_word_stronger_than_the_record(page):
    """§6 + Amendment 1 A1.2, the absolute half: labels, captions, headings, verdict text, generated sentences.
    Verbatim quoted material is exempt and is inventoried by the jsdom test instead -- a rule that forced the desk
    to alter "Russia confirms floating wheat export tax" would make the interface edit the record to satisfy a lint."""
    if not page.exists():
        pytest.skip(f"{page.name} absent")
    hits = sorted({m.group(0).lower() for m in BANNED_RE.finditer(_desk_written_strings(page.read_text()))})
    assert not hits, f"{page.name} writes {hits} in its own copy; §6 bans it in every string the desk writes itself"


def test_the_banned_list_is_the_one_the_spec_registers():
    """If DESIGN.md §6 changes its list, this test must be updated with it rather than drifting from the spec."""
    spec = DESIGN.read_text()
    for w in BANNED:
        assert f'"{w}"' in spec, f"{w} is enforced here but not named in DESIGN.md §6"


# --- §5 and the harness contract -----------------------------------------------------------------------------

def test_the_record_bar_sits_above_every_screen():
    """§5: it is a status line for the whole desk, not a panel inside one screen."""
    html = app()
    assert html.index('id="recordbar"') < html.index("<main>")


def test_the_page_emits_the_boot_marker_the_harnesses_strip_by():
    """Amendment 1 A1.4: the old harness anchored to the source line `loadFeed();`. The line changed, the anchor
    stopped matching, and the bootstrap ran inside the test for weeks -- passing only because both calls swallow
    their own fetch failure. The marker is the contract; if it disappears the harnesses exit 3 rather than pass."""
    html = app()
    assert re.search(r"/\* @boot-start \*/[\s\S]*?/\* @boot-end \*/", html), "the boot block must be delimited by the markers"
    assert html.count("/* @boot-start */") == 1 and html.count("/* @boot-end */") == 1


def test_an_unknown_hash_still_shows_a_screen():
    """/app#nonsense used to hide every screen, leaving a blank page."""
    assert "SCREENS" in app() and re.search(r"show\(\s*SCREENS\.has\(", app())


# --- the standing constraints --------------------------------------------------------------------------------

def test_the_desk_stays_one_file_with_no_dependency_and_no_cdn():
    """The constraint that does not move: no new dependency, no CDN, single file."""
    html = app()
    for tag in re.findall(r"<script[^>]*\bsrc\s*=\s*[\"']([^\"']+)", html) + \
               re.findall(r"<link[^>]*\bhref\s*=\s*[\"']([^\"']+)", html):
        assert not re.match(r"https?://|//", tag), f"external resource {tag}: no CDN"
    # every fetch the page makes is same-origin and under /api/
    for url in re.findall(r"api\(\s*[`'\"]([^`'\"]+)", html):
        assert url.startswith("/api/"), f"{url} is not a same-origin API path"


# --- §2 the absence language, as source rules (the DOM behaviour is in tests/test_app_render.py) --------------

def test_the_absence_language_exists_as_one_shared_helper_set():
    """§2 says the language is registered "so it is used identically everywhere" — so it is one set of functions,
    not a habit each screen repeats. The governing pattern is the forest plot: one zero rule, one shared domain."""
    html = app()
    for fn in ("verdictOf", "caption", "domainOf", "interval", "forest", "wilson", "emptyState", "verbatim"):
        assert re.search(r"function\s+" + fn + r"\s*\(", html), f"{fn}() must be the one implementation"


def test_only_three_verdict_states_plus_insufficient():
    """§2: three states only. Amber and green carry the verdict, never the sign."""
    html = app()
    states = set(re.findall(r"\.iv-([a-z]+)", html))
    assert states == {"crosses", "worse", "better", "insufficient", "hatch"}, states
    assert re.search(r"\.iv-crosses[^{]*\{[^}]*var\(--t3\)", html), "crosses-zero must be neutral grey"
    assert re.search(r"\.iv-worse[^{]*\{[^}]*var\(--hot\)", html), "engine worse must be amber"
    assert re.search(r"\.iv-better[^{]*\{[^}]*var\(--cool\)", html), "engine better must be green"


def test_insufficient_is_hatched_and_never_coloured():
    """§2: insufficient is not null. It is hatched, never coloured, and labelled with its n."""
    html = app()
    assert ".iv-insufficient .span{stroke:none}" in html
    assert 'pattern id="hatch"' in html and ".iv-hatch{fill:url(#hatch)}" in html


def test_the_interval_is_a_span_and_never_a_bar_grown_from_zero():
    """A bar anchored at a baseline makes readers judge points inside it as likelier than points outside
    (within-the-bar bias), so the mark spans the interval and the estimate is a tick on it."""
    html = app()
    fn = html[html.index("function interval("):html.index("function forest(")]
    assert 'class="span"' in fn and 'class="tick"' in fn
    assert "<rect" not in fn.replace('<rect class="iv-hatch"', ""), "the only rect is the insufficient hatch"


def test_the_interval_component_always_draws_the_zero_rule():
    """§2: any chart of an effect draws a zero rule at full contrast, labelled. No exceptions.
    The learning curve gains its own labelled rule in step 6; this covers the shared component."""
    html = app()
    fn = html[html.index("function interval("):html.index("function forest(")]
    assert 'class="zero"' in fn, "interval() must draw the zero rule"
    assert fn.index('class="zero"') < fn.index('class="span"'), "the zero rule is drawn under the interval, not over it"
    assert ".iv .zero{stroke:var(--t2)" in html, "the zero rule is drawn at full contrast, not dimmed"
