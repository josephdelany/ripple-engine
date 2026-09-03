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


# --- §1 the three tiers, §2 strict colour, §4 no boxes -------------------------------------------------------

def test_amber_and_green_appear_nowhere_but_an_interval_verdict():
    """§2: "Amber and green are used nowhere else in the interface." Strict, per the ruling of 2026-09-03: colour
    means an interval that excludes zero and nothing else. Claim chips, Material, the fan path, the learning curve
    and the outcome distribution all separate by weight, ground and rule instead."""
    html = app()
    uses = re.findall(r"[^\n]*var\(--(?:hot|cool)\)[^\n]*", html)
    assert len(uses) == 2, f"amber/green used {len(uses)} times:\n" + "\n".join(u.strip()[:110] for u in uses)
    assert any(".iv-worse" in u and "--hot" in u for u in uses), "amber is the excludes-zero-engine-worse state"
    assert any(".iv-better" in u and "--cool" in u for u in uses), "green is the excludes-zero-engine-better state"


def test_no_colour_outside_the_permitted_palette():
    """§6: ground, three text tiers, amber, green, and the hatch. The yellow --warn is retired."""
    html = app()
    assert "--warn" not in html, "yellow is outside the permitted palette"
    stray = set(re.findall(r'"(#[0-9a-fA-F]{6})"', html))
    assert not stray, f"hard-coded hex in markup instead of a palette token: {stray}"


def test_there_is_one_absence_language_not_two():
    """§2 registers the language "so it is used identically everywhere". The propagation band carried a private
    .ib/.v-* implementation of the same idea; it now consumes the shared component. Amendment 1 A1.3 maps the
    file's verdicts onto the §2 states: NULL -> crosses, TRANSMITTING -> better, INSUFFICIENT -> hatch."""
    html = app()
    assert ".v-NULL" not in html and ".v-TRANSMITTING .bar" not in html, "the private interval bar must be gone"
    band = html[html.index("function travelBand("):html.index("const esc=")]
    assert "interval(c.estimate" in band, "band 5 must draw through the shared interval() helper"
    assert re.search(r"iv-\$\{st\}", band), "band 5 rows carry the shared state class"


def test_the_three_tiers_are_declared_as_classes():
    """§1: three tiers, strictly; nothing on any screen sits outside them."""
    html = app()
    for cls, size in ((".t-find", 24), (".t-ev", 13.5), (".t-prov", 11)):
        m = re.search(re.escape(cls) + r"\{[^}]*font-size:([\d.]+)px", html)
        assert m, f"{cls} must be declared"
        assert abs(float(m.group(1)) - size) < 4, f"{cls} is {m.group(1)}px, outside its tier band"


def test_cards_carry_no_border():
    """§4: no card borders where a spacing rule will do."""
    html = app()
    m = re.search(r"\.card\{([^}]*)\}", html)
    assert m and "border:0" in m.group(1), "the card border is the cheapest possible hierarchy; spacing does the work"


# --- §3.1 the Story page ------------------------------------------------------------------------------------

def test_the_story_never_loads_empty():
    """§3.1 [T]: "It must never load empty." On open with no selection it shows the most material story from
    today's feed; if the feed is empty, the most recent corpus event."""
    html = app()
    assert re.search(r"function\s+loadDefaultStory\s*\(", html)
    assert re.search(r"boot\(\)\s*\{[^}]*loadDefaultStory\(\)", html), "the default story must load at boot"
    fn = html[html.index("async function loadDefaultStory("):html.index("async function readEvent(")]
    assert "/api/feed" in fn and "/api/events" in fn, "feed first, then the corpus"
    assert "emptyState(" in fn, "if even the record is unreachable, say why rather than showing a blank"


def test_the_story_is_the_registered_spine_in_order():
    """§3.1 AS AMENDED by Amendment 2 A2.8 (adopted 2026-09-03): the six numbered bands become a narrative
    spine — Question, what was knowable, what the record predicted, what happened, where it travelled, what
    we got wrong. The order is still registered and still enforced; only the form changed.

    This test was rewritten rather than deleted when the spec changed. The old assertion (six `N · Title`
    headings) was correct against §3.1 as first written and is wrong against §3.1 as amended; a registered
    spec changes by dated amendment and its test follows the amendment.
    """
    html = app()
    bands = re.findall(r'data-band="(\d)"', html)
    assert bands == ["1", "2", "3", "4", "5", "6"], bands
    assert "theRead(s)" in html                       # band 1 is the question: the record's own words
    for n, words in ((2, "What was knowable, and was it priced?"),
                     (3, "What the story claimed"),
                     (4, "What happened next, in comparable cases"),
                     (5, "Where it travelled"),
                     (6, "What we got wrong")):
        assert f"<h2>{words}</h2>" in html, f"band {n} must be '{words}'"


def test_a28_each_spine_section_opens_with_a_registered_sentence():
    """A2.8: the spine's sections state their finding through the registry, never by hand."""
    html = app()
    for sid in ("case.knowable.none", "case.knowable.some", "case.priced", "case.priced.none",
                "case.claims", "case.tail", "case.tail.none", "case.tail.thin",
                "case.travel", "case.travel.none"):
        assert f"'{sid}'" in html, f"{sid} is registered in Appendix A but never rendered"


def test_a28_the_desk_does_not_compose_a_finding_by_hand():
    """theRead() used to assemble the opening line out of two different populations. It may not come back:
    a Finding-tier string built by concatenating measured values is what the registry exists to replace."""
    html = app()
    read = html.split("function theRead(s){", 1)[1].split("\nfunction ", 1)[0]
    assert "bits.push" not in read, "theRead is composing a sentence by hand again"
    assert "verbatim(" in read, "band 1's finding must be the record's own words, marked verbatim"


def test_uncheckable_claims_collapse_behind_their_count():
    """§3.1(3) [T]: "Uncheckable claims are collapsed behind a count, not listed inline." They are logged, not
    displayed."""
    html = app()
    assert re.search(r"un\.length\s*\?\s*`<details><summary>\$\{un\.length\}", html)
    assert "uncheckable claim${un.length===1?'':'s'}" in html


def test_quoted_material_is_marked_so_the_inventory_can_find_it():
    """Amendment 1 A1.2: the desk's own copy is bound by §6; what a source said is reported as the source said it,
    inside a data-verbatim node carrying its source."""
    html = app()
    assert re.search(r"function\s+verbatim\s*\(", html)
    assert "data-verbatim" in html
    assert "verbatim(s.title" in html, "the corpus title is the record's words"
    assert re.search(r'class="q">\$\{verbatim\(', html), "claim text is the source's words"
