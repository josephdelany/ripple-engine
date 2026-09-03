"""
citation_guard.py -- every published number, and the path it resolves to. Session I.

WHAT THIS PROVES, AND WHAT IT DOES NOT. Read this before trusting it.

  It PROVES: the number printed in the prose still EXISTS somewhere in the declared
  record, and the run that record came from is still the current run.

  It does NOT prove: that the prose is citing the path the guard matched. A number
  can resolve by coincidence -- 150 appears in a dozen places. Where a claim resolves
  to more than one path the inventory says so and names them all, and the reader is
  the one who decides which was meant. This is an EXISTENCE and STALENESS guard, not
  a semantic one. It is not a substitute for reading.

  What it is FOR: after a re-run overwrites data/walk_forward/summary.json, nobody can
  hand-check 1,600 lines of prose. This makes the suite go red instead.

  The protection is GRADED, and the grades are not equal. Stated plainly so nobody
  reads a green suite as more than it is:

    STRONG   the run-id check. summary.json owns the run id and delta_experiment.json
             carries derived_from_run as a foreign key to it. When a re-run lands,
             this fails deterministically, every time, whatever happened to the
             numbers. This is the guard.
    SHARP    path-level drift on RESOLVED claims (n_paths <= 3). The exact field the
             number was traced to must still print it; a renamed or dropped field
             fails too.
    WEAK     object-level existence on AMBIGUOUS claims. It only notices when a value
             disappears from its object entirely, and a three-decimal number can
             survive elsewhere in the same file by coincidence. Most headline numbers
             are in this class, because summary.json legitimately stores the same
             quantity in a dozen places. Treat a green result here as "not obviously
             broken", never as "checked".

  A worked simulation of the Amendment 4 re-run (new run id, escalation scores moved)
  fires the STRONG check on summary.json and the SHARP check on three claims, and the
  WEAK check catches nothing. That is the honest measure of this file.

The design is lifted from two tests that already earned their place in
tests/test_figures_paper.py: the run-id assertion (a figure drawn from a superseded run
is red, never quietly stale) and the literal scan (which found a result typed into its
own author's docstring). Same idea, wider blast radius.

Three outputs, written to docs/:

  citation_inventory.json   the machine-readable inventory: every numeric token in the
                            five documents, classified, with its resolved paths
  CITATION_INVENTORY.md     the same thing for a person, UNSOURCED first

Every claim lands in exactly one class:

  RESOLVED   found in a declared object, at three or fewer named paths
  AMBIGUOUS  found, but in too many places to call any of them the citation
  DERIVED    arithmetic over stored fields rather than a stored value. The formula
             is declared HERE and EVALUATED; if it stops reproducing the printed
             number the claim falls back to UNSOURCED rather than being accepted.
  EXCEPTION  a number the guard is TOLD is not in a run object, with the committed
             file that does hold it. Registered here, in code, never inferred, and
             matched on the sentence as well as the value.
  SELF_REFERENTIAL
             resolves nowhere, and equals the sum of the numbers printed beside it.
             A denominator asserted by the sentence that uses it is the shape a
             fabricated denominator takes, so it is called out rather than left to
             look like a number nobody indexed. The paper's `477` was this shape
             until its predicate was published; it is DERIVED now.
  HISTORICAL resolves nowhere, and sits inside a correction, erratum or retraction
             region -- quoted as having been wrong, not asserted as right. A project
             that publishes its own corrections will always contain wrong numbers on
             purpose, and without this class every correction would make the guard
             noisier, penalising the one behaviour it exists to protect. Nothing in
             a correction region is checked for drift: a superseded number is
             SUPPOSED to leave the record.
  UNSOURCED  looks like a published quantity, found nowhere in the declared record.
             REPORTED, NOT FIXED. The guard never guesses at a source, and never
             invents one to make its own list shorter.
  EXCLUDED   not a claim at all -- a year, a section reference, a bibliography page
             range, a code span. The REASON is published for every one of them, so
             the filter itself can be audited rather than trusted.

The record is JSON and CSV. A CSV is read as {n_rows, n_columns, columns}, because
the documents cite those sheets for their row counts ("624 pre-1987 candidates") and
a JSON-only index left those numbers untraceable for a reason that had nothing to do
with the claim.

Run:  python3 src/citation_guard.py
"""

import csv
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

# The five documents that publish numbers to a reader.
DOCUMENTS = ["README.md", "docs/BRIEF.md", "docs/PAPER_DRAFT.md", "docs/EXPLAIN.md",
             "OPEN_ITEMS.md"]

# ---------------------------------------------------------------------------
# The declared record.
#
# A DECLARED registry, not a sweep of data/**. There are 146 JSON files in the tree;
# indexing all of them would let almost any number resolve to something and would make
# a green suite meaningless. These are the objects the five documents actually cite.
#
#   run_key    where this object records the run it belongs to. summary.json owns the
#              run id; delta_experiment.json carries derived_from_run, a foreign key
#              to it. An object with a run_key is checked for supersession.
#   stamp_key  a generated-at stamp for objects that are not walk runs. Recorded in the
#              inventory so a reader can see the vintage, but not a supersession gate.
# ---------------------------------------------------------------------------

RUN_OBJECTS = [
    {"path": "data/walk_forward/summary.json", "run_key": "run_id",
     "stamp_key": "generated_at", "role": "the published walk"},
    {"path": "data/walk_forward/delta_experiment.json", "run_key": "derived_from_run",
     "stamp_key": "computed_at", "role": "Amendment L/M, §11 -- derived from the walk"},
    {"path": "data/state/situation_knowable.json", "run_key": None,
     "stamp_key": "generated_at", "role": "the vintage filter's own counts"},
    {"path": "data/big_moves/summary.json", "run_key": None, "stamp_key": None,
     "role": "the big-moves census"},
    {"path": "data/walk_forward/big_moves_knew.json", "run_key": None,
     "stamp_key": None, "role": "big moves, what was knowable"},
    {"path": "data/reader_eval/score.json", "run_key": None, "stamp_key": None,
     "role": "the reader's gold-set score"},
    {"path": "data/state/outcomes_kappa.json", "run_key": None,
     "stamp_key": "generated_at", "role": "the retired label's kappa"},
    {"path": "data/acceptance_dod.json", "run_key": None, "stamp_key": "generated_at",
     "role": "definition of done"},
    {"path": "data/walk_forward/menu.json", "run_key": None, "stamp_key": None,
     "role": "the registered Hedge menu"},
    {"path": "data/grid/power_arithmetic.json", "run_key": None, "stamp_key": None,
     "role": "the grid study's effective-n arithmetic"},
    {"path": "data/grid/price/summary.json", "run_key": None, "stamp_key": None,
     "role": "the grid study, price side"},
    {"path": "data/grid/g/PANEL.json", "run_key": None, "stamp_key": None,
     "role": "the grid study, escalation panel"},
    # Last on purpose: 91,161 of the record's 100,961 numeric leaves are in this one
    # file, so anything checked against it first resolves by coincidence.
    {"path": "data/ripple/irf.json", "run_key": None, "stamp_key": "meta.when",
     "role": "the propagation study (91k leaves -- resolved last, see note above)"},
    # CSV sheets. The documents cite these for their ROW COUNTS ("624 pre-1987
    # candidates"), which no JSON records, so a JSON-only index left those numbers
    # untraceable for a reason that had nothing to do with the claim. A CSV reads
    # into {n_rows, n_columns, columns: {...}} so a count sits at depth 1 and a cell
    # at depth 3, and the specificity ranking prefers the count.
    {"path": "data/candidates/pre1987_candidates.csv", "run_key": None,
     "stamp_key": None, "role": "the pre-1987 candidate sheet"},
    {"path": "data/candidates/post1987_candidates.csv", "run_key": None,
     "stamp_key": None, "role": "the post-1987 candidate sheet"},
    {"path": "data/candidates/pre1987_candidates_outcomes.csv", "run_key": None,
     "stamp_key": None, "role": "pre-1987 candidates, outcome columns"},
    {"path": "data/candidates/pre1987_ranked.csv", "run_key": None,
     "stamp_key": None, "role": "pre-1987 candidates, ranked"},
]

# ---------------------------------------------------------------------------
# Registered exceptions: numbers that are genuinely NOT in any run object, with the
# committed file that does hold them. Each one is declared here, in code, reviewed --
# never inferred by the guard to make a list shorter. Adding one is a deliberate act.
# ---------------------------------------------------------------------------

EXCEPTIONS = [
    {"values": ["0.005", "0.0053"],
     "context": re.compile(r"parity|earlier run|one run earlier|before Amendment H|"
                           r"pre-Amendment", re.I),
     "sources": ["STATE_OF_THE_ENGINE.md (section 5)",
                 "data/handoffs/B_run_delta.md (193022Z column)"],
     "why": "the escalation skill from the run BEFORE Amendment H "
            "(walk_20260902T193022Z). summary.json publishes ONE run, so the "
            "before/after comparison cannot resolve there. Parsed and cross-checked "
            "by src/figures_paper.py:load_pre_amendment_h(), which fails if the two "
            "files disagree to 4 dp."},
    {"values": ["0.030", "0.03"],
     "context": re.compile(r"parity|earlier run|one run earlier|before Amendment H|"
                           r"pre-Amendment", re.I),
     "sources": ["STATE_OF_THE_ENGINE.md (section 5)",
                 "data/handoffs/B_run_delta.md (193022Z column)"],
     "why": "the PRICE skill from that same pre-Amendment-H run, quoted beside the "
            "escalation one. Same reason, same files."},
]

# ---------------------------------------------------------------------------
# Registered DERIVED claims: numbers the prose prints that are arithmetic over
# stored fields rather than stored values. Each declares its formula HERE, in code,
# and the formula is EVALUATED at build time -- if it does not reproduce the printed
# number the claim is left UNSOURCED rather than quietly accepted. That is the line
# between a demonstrated identity and a guess.
# ---------------------------------------------------------------------------

def _scored_irf_cells(objs):
    """Rows of data/ripple/irf.json that carry a verdict at all.

    The paper's propagation denominator. It went UNSOURCED on this guard's first run
    because section 12 asserted "477 node x shock cells" without stating the
    predicate that produced it. The predicate is now written into section 12 and
    Appendix A (1a18987), so it can be EVALUATED here rather than taken on trust.
    """
    return sum(1 for r in objs["data/ripple/irf.json"]["rows"]
               if r.get("verdict") is not None)


def _filtration_checks_total(objs):
    return sum(objs["data/walk_forward/summary.json"]["filtration_audit"]
               ["checks"].values())


DERIVED = [
    {"values": ["477"],
     "context": re.compile(r"node.shock cells|cells transmit|of 477", re.I),
     "formula": _scored_irf_cells,
     "explain": "count of data/ripple/irf.json :: rows[*] whose `verdict` is not "
                "null -- 401 NULL + 21 TRANSMITTING + 55 INSUFFICIENT of 932 rows, "
                "455 unscored. Predicate registered in PAPER_DRAFT section 12 and "
                "Appendix A."},
    {"values": ["15784"],
     "context": re.compile(r"filtration audit|point-in-time checks|checks", re.I),
     "formula": _filtration_checks_total,
     "explain": "sum of data/walk_forward/summary.json :: filtration_audit.checks.* "
                "(six counters). Not stored as a single field, so it cannot resolve "
                "directly; the sum is recomputed here and must match what is printed."},
]


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

# Spans that are never prose claims: fenced code, inline code, link and image targets,
# bare URLs, and HTML comments. Blanked before tokenising so their digits never enter.
_SPAN_PATTERNS = [
    (re.compile(r"```.*?```", re.S), "code-fence"),
    (re.compile(r"`[^`\n]*`"), "inline-code"),
    (re.compile(r"\]\([^)]*\)"), "link-target"),
    (re.compile(r"https?://\S+"), "url"),
    (re.compile(r"<!--.*?-->", re.S), "html-comment"),
]

# A number as a reader sees it: optional sign (ASCII or typographic), digits with
# optional thousands separators, optional decimal part, optional percent.
_NUMBER = re.compile(
    r"(?<![\w.])([−+-]?)(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(%?)(?![\d])")

# Things that look numeric but name something rather than measure it. The preceding
# text decides; the reason is published for every exclusion so the filter is auditable.
_LABEL_BEFORE = re.compile(
    r"(?:§|Amendment\s|amendment\s|Step\s|Part\s|Tier\s|tier\s|RULE-|REQ-|ADR-|"
    r"H|M|C|D|G\d?|v|Figure\s|figure\s|Table\s|table\s|item\s|Item\s|§\s*|"
    r"finding\s|Finding\s|section\s|Section\s|commit\s|#|Order\s|"
    r"[A-Za-z]{2,}-)$")


def _blank_spans(text):
    """Replace non-prose spans with spaces, keeping every offset AND every newline.

    Newlines must survive: a code fence blanked to plain spaces silently merges its
    lines into the one before it, and every line number after the first fenced block
    in the document comes out wrong.
    """
    spans = []
    out = text
    for pattern, label in _SPAN_PATTERNS:
        def repl(m):
            spans.append((m.start(), m.end(), label))
            return "".join("\n" if ch == "\n" else " " for ch in m.group(0))
        out = pattern.sub(repl, out)
    return out, spans


# A paragraph or section that exists to publish a number that WAS wrong. A paper
# which corrects itself will always contain wrong numbers on purpose, and a guard
# that cannot tell those apart gets noisier every time the project does the right
# thing -- which is exactly backwards.
_CORRECTION_OPENER = re.compile(
    r"^\**\s*(?:correction|erratum|errata)\b|^\**\s*the correction\b|"
    r"^an earlier draft\b|^\**\s*retract", re.I)
# A paragraph can announce itself as a retraction inside its bolded lead-in rather
# than at character zero -- "**1.5 ~~A VALIDATED claim~~ - CLOSED, RETRACTED.**".
# A start-anchored rule missed exactly that, so the lead-in is searched too. Scoped
# to the paragraph's FIRST line and its first 120 characters, so a paragraph that
# merely mentions a retraction in passing is not swept in.
_CORRECTION_LEADIN = re.compile(
    r"RETRACTED|CORRECTION|ERRATUM|ERRATA|"
    r"correction of record|erratum|errata|retracted under")
_CORRECTION_LEADIN_WINDOW = 120
_CORRECTION_HEADING = re.compile(r"errat(?:a|um)|correction|retraction", re.I)


def _paragraph_is_a_correction(first_line):
    """Does this paragraph announce itself as a correction, erratum or retraction?"""
    head = first_line.strip()
    if _CORRECTION_OPENER.search(head):
        return True
    return bool(_CORRECTION_LEADIN.search(head[:_CORRECTION_LEADIN_WINDOW]))


def _correction_lines(text):
    """Lines inside a correction, erratum or retraction region.

    Two shapes, both published in the inventory so the rule can be audited:
      - a HEADING that names itself a correction, until the next heading of the
        same or a higher level;
      - a PARAGRAPH whose FIRST LINE announces itself as one, until the next blank
        line.

    This does NOT exempt every number in the region. A correction paragraph quotes
    the superseded value AND the current one, and the current one must still be
    checked. The region only gives an UNRESOLVED number permission to be there:
    HISTORICAL is (unresolved) AND (inside one of these). See build().
    """
    raw = text.splitlines()
    lines, heading_level = set(), None
    i = 0
    while i < len(raw):
        stripped = raw[i].strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if _CORRECTION_HEADING.search(stripped):
                heading_level = level
            elif heading_level is not None and level <= heading_level:
                heading_level = None
            if heading_level is not None:
                lines.add(i + 1)
            i += 1
            continue
        if not stripped:
            if heading_level is not None:
                lines.add(i + 1)
            i += 1
            continue
        # a paragraph: this line to the next blank or heading
        j = i
        while j < len(raw) and raw[j].strip() and not raw[j].strip().startswith("#"):
            j += 1
        if heading_level is not None or _paragraph_is_a_correction(raw[i]):
            lines.update(range(i + 1, j + 1))
        i = j
    return lines


def _numbers_in(context):
    """Every numeric value printed in a line of prose."""
    out = []
    for m in _NUMBER.finditer(context.replace("\u2212", "-")):
        sign, digits, frac = m.group(1), m.group(2), m.group(3) or ""
        v = float(digits.replace(",", "") + frac)
        out.append(-v if sign == "-" else v)
    return out


def self_referential_addends(claim, max_terms=5):
    """Does this number exist only as the sum of the numbers printed beside it?

    A denominator that resolves nowhere in the record but equals the parts listed
    in its own sentence is asserting itself. That is precisely the shape a
    fabricated denominator takes, so it gets its own class rather than sitting in
    UNSOURCED looking like a number nobody happened to index.
    """
    if claim["decimals"] != 0 or abs(claim["value"]) < 3:
        return None
    others = [v for v in _numbers_in(claim["context"])
              if v != claim["value"] and v > 0][:12]
    for k in range(2, min(max_terms, len(others)) + 1):
        for combo in itertools.combinations(others, k):
            if abs(sum(combo) - abs(claim["value"])) < 1e-9:
                return list(combo)
    return None


def _bibliography_lines(text):
    """Line numbers inside a References / Bibliography section.

    Journal volumes, issues and page ranges are numerals that measure nothing about
    this project. Excluded wholesale, by section, rather than by guessing at a shape.
    """
    inside, lines = False, set()
    for i, line in enumerate(text.splitlines(), start=1):
        if line.startswith("#"):
            inside = bool(re.search(r"references|bibliography|works cited",
                                    line, re.I))
        elif inside:
            lines.add(i)
    return lines


def _classify_exclusion(raw, digits, decimals, before, after):
    """Return a reason string if this token is not a published quantity, else None."""
    if decimals == 0 and "," not in digits and len(digits) == 4:
        n = int(digits)
        if 1900 <= n <= 2099:
            return "year"
    if after[:1] == "Z" and decimals == 0 and len(digits) == 6:
        return "run identifier (walk_...Z)"
    if _LABEL_BEFORE.search(before[-12:]):
        return "identifier (section, amendment, item or figure reference)"
    if re.match(r"^\s*[-–—]\s*\d", after) and decimals == 0 and len(digits) == 4:
        return "year range"
    if re.match(r"^\s*(?:st|nd|rd|th)\b", after):
        return "ordinal"
    return None


def extract_claims(rel_path, text):
    """Every numeric token in a document, classified, with its line and context."""
    blanked, _ = _blank_spans(text)
    biblio = _bibliography_lines(text)
    corrections = _correction_lines(text)
    line_starts = [0]
    for i, ch in enumerate(blanked):
        if ch == "\n":
            line_starts.append(i + 1)

    def line_of(pos):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    claims = []
    for m in _NUMBER.finditer(blanked):
        sign, digits, frac, pct = m.group(1), m.group(2), m.group(3) or "", m.group(4)
        raw = m.group(0)
        decimals = len(frac) - 1 if frac else 0
        before = blanked[max(0, m.start() - 40):m.start()]
        after = blanked[m.end():m.end() + 20]
        reason = _classify_exclusion(raw, digits, decimals, before, after)
        value = float(digits.replace(",", "") + frac)
        if sign in ("−", "-"):
            value = -value
        ln = line_of(m.start())
        if reason is None and ln in biblio:
            reason = "bibliography (journal volume, issue or page range)"
        doc_lines = text.splitlines()
        context = doc_lines[ln - 1].strip() if ln - 1 < len(doc_lines) else ""
        claims.append({
            "document": rel_path, "line": ln, "raw": raw.strip(),
            "value": value, "decimals": decimals, "percent": bool(pct),
            "context": context[:200],
            "excluded_because": reason,
            "in_correction_region": ln in corrections,
        })
    return claims


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

# Claims are printed to at most this many decimals; the lookup is built for each
# precision so resolution is a dict hit rather than a scan of every leaf.
MAX_DP = 6
# A value that occurs in dozens of places (0, 1, small counts) says nothing about
# WHICH field was meant. Above this many matches a claim is AMBIGUOUS, not RESOLVED:
# the value is in the record, but "traceable to a named path" would be a lie.
TRACEABLE_MAX_PATHS = 3


def show_path(segments):
    """A segment list rendered for a reader: tiers.daily.G.engine_vs.frozen.skill"""
    out = ""
    for seg in segments:
        out += f"[{seg}]" if isinstance(seg, int) else (f".{seg}" if out else str(seg))
    return out


def index_numeric_leaves(obj):
    """Every numeric leaf, as (value, path SEGMENTS).

    Segments, not a dotted string: this record contains keys that themselves
    contain dots (`C1_fixed_0.5`), so a dotted path cannot be parsed back and the
    path-level drift check would silently fail on exactly the claims it was built
    to protect. Found by that check failing on its first run.
    """
    leaves = []

    def walk(node, segments):
        if isinstance(node, bool):
            return
        if isinstance(node, (int, float)):
            leaves.append((float(node), tuple(segments)))
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, segments + [k])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, segments + [i])

    walk(obj, [])
    return leaves


def build_lookup(leaves):
    """{decimals: {rounded value: (paths, total count)}} -- O(1) resolution.

    Rounded at every precision a document might print, so a claim of -0.097 finds a
    stored -0.09655... because that rounding is what the reader was actually shown.
    """
    lookup = {dp: {} for dp in range(MAX_DP + 1)}
    for value, path in leaves:
        for dp in range(MAX_DP + 1):
            bucket = lookup[dp].setdefault(round(value, dp), [])
            bucket.append(path)
    return lookup


def _specificity(segments):
    """Rank candidate paths so the most plausible citation is shown first.

    Alphabetical order is useless here: it made -0.600 -- the engine's skill against
    persistence -- point at big_moves_knew[33].reads[5].engine_p50. A short path with
    no array indices (G_joint_across_tiers.skill) is far more likely to be the field
    a sentence is quoting than a deep one inside a per-event array.
    """
    depth = len(segments)
    n_index = sum(1 for seg in segments if isinstance(seg, int))
    return (n_index, depth, show_path(segments))


def resolve(claim, ordered_lookups, max_paths=4):
    """Where this claim's value sits in the record, in declared priority order.

    Resolution stops at the FIRST object that contains the value. The registry is
    ordered by how central an object is to what the documents publish, so a walk
    number resolves in summary.json rather than colliding with one of irf.json's
    91k leaves. Matches in lower-priority objects are still reported, as `also_in`,
    so nothing is hidden -- they just do not get to claim the citation.

    Sign-insensitive: prose says "scores 0.480 against us" as often as "-0.480".
    A percent claim also tries its fractional form (84% against a stored 0.84).
    """
    dp = min(claim["decimals"], MAX_DP)
    targets = {round(claim["value"], dp), round(-claim["value"], dp)}
    if claim["percent"]:
        targets |= {round(claim["value"] / 100.0, dp),
                    round(-claim["value"] / 100.0, dp)}
    primary, also_in = None, []
    for obj_path, lookup in ordered_lookups:
        table = lookup[dp]
        paths = sorted({p for t in targets for p in table.get(t, ())},
                       key=_specificity)
        if not paths:
            continue
        if primary is None:
            primary = {"object": obj_path, "segments": paths[:max_paths],
                       "n_paths": len(paths)}
        else:
            also_in.append({"object": obj_path, "n_paths": len(paths)})
    return primary, also_in


def resolve_in(claim, lookup, max_paths=4):
    """Does this claim's value still exist in ONE named object?

    The drift check must ask this, not "is it anywhere in the record". The
    propagation file holds 91k leaves and at three decimals contains almost every
    value in [-1, 1], so "anywhere" is always true and catches nothing. A walk
    number that resolved in summary.json has to still be in summary.json.
    """
    dp = min(claim["decimals"], MAX_DP)
    targets = {round(claim["value"], dp), round(-claim["value"], dp)}
    if claim["percent"]:
        targets |= {round(claim["value"] / 100.0, dp),
                    round(-claim["value"] / 100.0, dp)}
    table = lookup[dp]
    paths = sorted({p for t in targets for p in table.get(t, ())}, key=_specificity)
    return paths[:max_paths], len(paths)


def value_at(obj, segments):
    """The value at a path, given as segments. None if the path is gone.

    A re-run that renames or drops a field is as much a drift as one that changes
    a number, so a missing path is a failure, not a skip.
    """
    node = obj
    for seg in segments:
        if isinstance(seg, int):
            if not isinstance(node, list) or seg >= len(node):
                return None
            node = node[seg]
        else:
            if not isinstance(node, dict) or seg not in node:
                return None
            node = node[seg]
    if isinstance(node, bool) or not isinstance(node, (int, float)):
        return None
    return node


def still_at_path(claim, obj):
    """True while at least one of a RESOLVED claim's own paths still prints it.

    This is the sharp end of the guard. Object-level existence is a weak net: a
    three-decimal value can survive somewhere else in the same file by coincidence.
    Checking the exact field the number was traced to does not have that problem.
    """
    dp = min(claim["decimals"], MAX_DP)
    targets = {round(claim["value"], dp), round(-claim["value"], dp)}
    if claim["percent"]:
        targets |= {round(claim["value"] / 100.0, dp),
                    round(-claim["value"] / 100.0, dp)}
    for segments in claim.get("path_segments", []):
        v = value_at(obj, segments)
        if v is not None and round(float(v), dp) in targets:
            return True
    return False


def match_derived(claim, objs):
    """A registered derived claim, EVALUATED. Returns None unless it reproduces."""
    for d in DERIVED:
        if not d["context"].search(claim["context"]):
            continue
        for v in d["values"]:
            if abs(claim["value"]) != abs(float(v)):
                continue
            try:
                got = d["formula"](objs)
            except (KeyError, TypeError):
                return None
            if round(float(got), 6) == abs(claim["value"]):
                return {"explain": d["explain"], "recomputed": got}
            return None
    return None


def match_exception(claim):
    """A registered exception matches on BOTH the value and the sentence it sits in.

    Value alone is not enough: 0.005 also happens to be the price skill against
    random analogues in the current run, so a value-only rule would silently file a
    pre-Amendment-H escalation number under a live price field.
    """
    for exc in EXCEPTIONS:
        if not exc["context"].search(claim["context"]):
            continue
        for v in exc["values"]:
            dp = len(v.split(".")[1])
            if claim["decimals"] == dp and round(abs(claim["value"]), dp) == abs(float(v)):
                return exc
    return None


# ---------------------------------------------------------------------------

def read_csv_object(path):
    """A CSV as an indexable object: its shape first, then its numeric columns.

    Shape first because shape is what the prose cites -- the paper says "624
    pre-1987 candidates" and means the number of rows in this file.
    """
    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    columns = {}
    for field in (rows[0].keys() if rows else []):
        vals = []
        for r in rows:
            try:
                vals.append(float(str(r[field]).replace(",", "")))
            except (TypeError, ValueError):
                continue
        if vals:
            columns[field] = vals
    return {"n_rows": len(rows),
            "n_columns": len(rows[0]) if rows else 0,
            "columns": columns}


def load_object(path):
    """Read a declared object: JSON as itself, CSV via read_csv_object."""
    if path.suffix.lower() == ".csv":
        return read_csv_object(path)
    return json.loads(path.read_text())


def _get(obj, dotted):
    node = obj
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def load_record():
    """The declared record: each object, its run id, its stamp, its numeric index."""
    record = []
    for spec in RUN_OBJECTS:
        p = ROOT / spec["path"]
        if not p.exists():
            raise FileNotFoundError(
                f"{spec['path']} is declared in RUN_OBJECTS but is not in the tree. "
                f"The guard reads it; fix the registry or restore the file.")
        obj = load_object(p)
        leaves = index_numeric_leaves(obj)
        record.append({
            "path": spec["path"], "role": spec["role"],
            "run_id": _get(obj, spec["run_key"]) if spec["run_key"] else None,
            "run_key": spec["run_key"],
            "stamp": _get(obj, spec["stamp_key"]) if spec["stamp_key"] else None,
            "lookup": build_lookup(leaves),
            "n_leaves": len(leaves),
            "obj": obj,
        })
    return record


def current_run_id(record):
    """The run id the whole record is supposed to be on: summary.json's."""
    for r in record:
        if r["path"] == "data/walk_forward/summary.json":
            return r["run_id"]
    raise KeyError("summary.json is not in RUN_OBJECTS")


def build():
    record = load_record()
    ordered_lookups = [(r["path"], r["lookup"]) for r in record]
    objs = {r["path"]: r["obj"] for r in record}
    run_id = current_run_id(record)

    claims = []
    for doc in DOCUMENTS:
        p = ROOT / doc
        if not p.exists():
            raise FileNotFoundError(f"{doc} is declared in DOCUMENTS but is not in the tree")
        claims.extend(extract_claims(doc, p.read_text()))

    for c in claims:
        if c["excluded_because"]:
            c["status"] = "EXCLUDED"
            continue
        exc = match_exception(c)
        der = match_derived(c, objs)
        primary, also_in = resolve(c, ordered_lookups)
        if der:
            c["status"] = "DERIVED"
            c["why"] = der["explain"]
            c["recomputed"] = der["recomputed"]
            if primary:
                c["coincidental_object"] = primary["object"]
                c["coincidental_paths"] = [
                    f"{primary['object']} :: {show_path(seg)}"
                    for seg in primary["segments"]]
        elif exc:
            # Declared and reviewed, so it wins over any run-object match. Where the
            # value ALSO occurs in the record that is recorded, not hidden -- it is
            # the clearest evidence in this file of how easily a number resolves by
            # coincidence.
            c["status"] = "EXCEPTION"
            c["paths"] = exc["sources"]
            c["why"] = exc["why"]
            if primary:
                c["coincidental_object"] = primary["object"]
                c["coincidental_paths"] = [
                    f"{primary['object']} :: {show_path(seg)}"
                    for seg in primary["segments"]]
        elif primary is None:
            addends = self_referential_addends(c)
            if c["in_correction_region"]:
                # Quoted as having been wrong, not asserted as right. Without this
                # class every correction the project publishes makes the guard
                # noisier, which would penalise the one behaviour it exists to
                # protect.
                c["status"] = "HISTORICAL"
                c["why"] = ("inside a correction / erratum / retraction region: a "
                            "superseded number quoted deliberately, not a live claim")
            elif addends:
                c["status"] = "SELF_REFERENTIAL"
                c["addends"] = addends
                c["why"] = ("resolves nowhere in the record, and equals the sum of "
                            "the numbers printed beside it "
                            f"({' + '.join(_fmt_addend(a) for a in addends)}). The "
                            "sentence is its own source.")
            else:
                c["status"] = "UNSOURCED"
        else:
            c["object"] = primary["object"]
            c["path_segments"] = [list(seg) for seg in primary["segments"]]
            c["paths"] = [f"{primary['object']} :: {show_path(seg)}"
                          for seg in primary["segments"]]
            c["n_paths"] = primary["n_paths"]
            if also_in:
                c["also_in"] = also_in
            c["status"] = ("RESOLVED" if primary["n_paths"] <= TRACEABLE_MAX_PATHS
                           else "AMBIGUOUS")

    inventory = {
        "generated_by": "src/citation_guard.py",
        "what_this_proves": (
            "A RESOLVED number still EXISTS in the declared record at the named path. "
            "It does NOT prove the prose cites that path; a number may resolve by "
            "coincidence, and n_paths says how often it occurs. This is an existence "
            "and staleness guard, not a semantic one."),
        "current_run_id": run_id,
        "record": [{**{k: r[k] for k in ("path", "role", "run_key", "run_id",
                                         "stamp")},
                    "numeric_leaves": r["n_leaves"]} for r in record],
        "documents": DOCUMENTS,
        "traceable_max_paths": TRACEABLE_MAX_PATHS,
        "counts": {s: sum(1 for c in claims if c["status"] == s)
                   for s in ("RESOLVED", "EXCEPTION", "DERIVED", "AMBIGUOUS",
                             "SELF_REFERENTIAL", "HISTORICAL", "UNSOURCED",
                             "EXCLUDED")},
        "claims": claims,
    }
    return inventory


# ---------------------------------------------------------------------------

def render_markdown(inv):
    c = inv["counts"]
    total = sum(c.values())
    lines = [
        "# Citation inventory — every published number and where it resolves",
        "",
        f"*Generated by `src/citation_guard.py` from the record at run "
        f"`{inv['current_run_id']}`. Do not edit by hand: regenerate.*",
        "",
        "## What this file proves, and what it does not",
        "",
        "A **RESOLVED** number still exists in the declared record at the named path.",
        "It does **not** prove the prose is citing that path — a number can resolve by",
        "coincidence, and `n_paths` says how many places it occurs. This is an existence",
        "and staleness guard, not a semantic one, and it is not a substitute for reading.",
        "",
        "The protection is **graded**, and the grades are not equal:",
        "",
        "| grade | what it covers | how it behaves on a re-run |",
        "|---|---|---|",
        "| **strong** | the run id itself | fails deterministically, every time |",
        "| **sharp** | RESOLVED claims | the exact field must still print the number |",
        "| **weak** | AMBIGUOUS claims | only notices if the value leaves the file entirely |",
        "",
        "Most headline numbers are AMBIGUOUS, because `summary.json` legitimately stores",
        "the same quantity in a dozen places. **Treat a green result there as \"not",
        "obviously broken\", never as \"checked\".** A green suite means the run is",
        "current; it does not mean any sentence has been validated, and this guard must",
        "never be quoted as though it validated the paper.",
        "",
        "**UNSOURCED is reported, never fixed.** The guard does not guess at a source for",
        "a number it cannot find, and never invents one to shorten its own list.",
        "",
        "## The declared record",
        "",
        "Resolution runs in this order and stops at the first object that holds the",
        "value, so a walk number is not captured by the 91k leaves of the propagation",
        "file. Later matches are recorded as `also_in`, never as the citation.",
        "",
        "| # | object | role | run id | stamp | numeric leaves |",
        "|---:|---|---|---|---|---:|",
    ]
    for i, r in enumerate(inv["record"], start=1):
        lines.append(f"| {i} | `{r['path']}` | {r['role']} | "
                     f"{('`' + r['run_id'] + '`') if r['run_id'] else '—'} | "
                     f"{r['stamp'] or '—'} | {r['numeric_leaves']:,} |")
    lines += [
        "",
        "## Counts",
        "",
        "| class | n | meaning |",
        "|---:|---:|---|",
        f"| RESOLVED | {c['RESOLVED']} | traceable to at most "
        f"{inv['traceable_max_paths']} named paths |",
        f"| EXCEPTION | {c['EXCEPTION']} | registered as living outside the run objects |",
        f"| DERIVED | {c['DERIVED']} | arithmetic over stored fields, recomputed here |",
        f"| SELF_REFERENTIAL | {c['SELF_REFERENTIAL']} | **a denominator that sums "
        f"only from its own sentence** |",
        f"| HISTORICAL | {c['HISTORICAL']} | quoted as having been wrong, inside a "
        f"correction region |",
        f"| AMBIGUOUS | {c['AMBIGUOUS']} | in the record, but in too many places to "
        f"call it a citation |",
        f"| UNSOURCED | {c['UNSOURCED']} | **found nowhere in the declared record** |",
        f"| EXCLUDED | {c['EXCLUDED']} | not a claim (year, identifier, bibliography, "
        f"code span) |",
        f"| | **{total}** | numeric tokens scanned across "
        f"{len(inv['documents'])} documents |",
        "",
        "## UNSOURCED — what we cannot trace",
        "",
        "Reported, not fixed. Each of these is a number a reader is shown that the guard",
        "could not find anywhere in the declared record. Some will be arithmetic done in",
        "the prose, some quote a handoff or an amendment rather than a run object, and",
        "some may be wrong. Deciding which is a person's job, not the guard's.",
        "",
        "| document | line | number | context |",
        "|---|---:|---:|---|",
    ]
    for cl in inv["claims"]:
        if cl["status"] == "UNSOURCED":
            ctx = cl["context"].replace("|", "\\|")[:130]
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | {ctx} |")
    if not any(cl["status"] == "UNSOURCED" for cl in inv["claims"]):
        lines.append("| — | — | — | *nothing untraceable in the current documents* |")

    n_corr = sum(1 for cl in inv["claims"] if cl.get("in_correction_region")
                 and cl["status"] != "EXCLUDED")
    lines += ["", "## SELF_REFERENTIAL — the sentence is its own source", "",
              "A number that resolves **nowhere** in the record and happens to equal the",
              "sum of the numbers printed beside it. A denominator asserted by the same",
              "sentence that uses it is exactly the shape a fabricated one takes, so it",
              "gets its own class rather than sitting in UNSOURCED looking like a number",
              "nobody happened to index.",
              "",
              "The paper's `477` was this shape on the guard's first run — it resolved",
              "only as 21 + 401 + 55 from the sentence asserting it. It is now DERIVED,",
              "because the predicate behind it was written into section 12 and Appendix A",
              "and can be evaluated. The guard was right to flag it; the paper was wrong",
              "not to state its own predicate. This class exists to catch the next one.",
              "",
              "| document | line | number | sums from | context |",
              "|---|---:|---:|---|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "SELF_REFERENTIAL":
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{' + '.join(str(a) for a in cl['addends'])} | "
                         f"{cl['context'][:90].replace('|', chr(92) + '|')} |")
    if not any(cl["status"] == "SELF_REFERENTIAL" for cl in inv["claims"]):
        lines.append("| — | — | — | — | *none in the current documents* |")

    lines += ["", "## HISTORICAL — quoted as having been wrong", "",
              "A project that publishes its own corrections will always contain wrong",
              "numbers on purpose. These sit inside a correction, erratum or retraction",
              "region and resolve nowhere in the record — which is what a superseded",
              "number should do. Without this class every correction the project",
              "publishes would make the guard noisier, penalising the one behaviour it",
              "exists to protect.",
              "",
              f"{n_corr} claim(s) in total sit inside a correction region; the ones that",
              "still resolve are classed normally and marked `correction region` in the",
              "tables below. **No claim in a correction region is checked for drift** —",
              "a superseded number is expected to leave the record.",
              "",
              "| document | line | number | context |", "|---|---:|---:|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "HISTORICAL":
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{cl['context'][:110].replace('|', chr(92) + '|')} |")

    lines += ["", "## DERIVED — arithmetic over stored fields, recomputed and checked",
              "",
              "These are printed numbers that are not stored anywhere as a single field.",
              "The formula is declared in `src/citation_guard.py` and **evaluated**: if it",
              "stops reproducing the printed number the claim falls back to UNSOURCED",
              "rather than being quietly accepted.",
              "",
              "| document | line | number | recomputed | from |",
              "|---|---:|---:|---:|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "DERIVED":
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{cl['recomputed']} | {cl['why']} |")

    lines += ["", "## EXCEPTION — registered as living outside the run objects", "",
              "A registered exception matches on the value **and** the sentence around",
              "it. Value alone is not enough, and the `also matches` column below is why:",
              "the pre-Amendment-H escalation skill happens to equal several unrelated",
              "live fields. A value-only rule would have filed it under one of them.",
              "",
              "| document | line | number | holds it | also matches (coincidence) |",
              "|---|---:|---:|---|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "EXCEPTION":
            coin = cl.get("coincidental_paths") or []
            coin_s = "<br>".join("`" + c + "`" for c in coin[:3]) if coin else "—"
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{', '.join('`' + s + '`' for s in cl['paths'])} | {coin_s} |")

    lines += ["", "## AMBIGUOUS — in the record, but not traceable to one path", "",
              "The value is present, so a re-run that changed it would still be caught.",
              "But it occurs in more than "
              f"{inv['traceable_max_paths']} places in its object, so the guard will not",
              "claim to know which field the prose meant. Listed with the first few.",
              "",
              "| document | line | number | n_paths | first matches |",
              "|---|---:|---:|---:|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "AMBIGUOUS":
            shown = "<br>".join("`" + p + "`" for p in cl["paths"][:2])
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{cl['n_paths']} | {shown} |")

    lines += ["", "## RESOLVED — the number, and where it is in the record", "",
              "`n_paths` is how many places the value occurs in the resolving object.",
              "", "| document | line | number | n_paths | resolves to |",
              "|---|---:|---:|---:|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "RESOLVED":
            shown = "<br>".join("`" + p + "`" for p in cl["paths"])
            more = "" if cl["n_paths"] <= len(cl["paths"]) else \
                f"<br>… and {cl['n_paths'] - len(cl['paths'])} more"
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{cl['n_paths']} | {shown}{more} |")

    lines += ["", "## EXCLUDED — not claims, and why", "",
              "Published so the filter itself can be audited rather than trusted.", "",
              "| document | line | number | excluded because |", "|---|---:|---:|---|"]
    for cl in inv["claims"]:
        if cl["status"] == "EXCLUDED":
            lines.append(f"| `{cl['document']}` | {cl['line']} | `{cl['raw']}` | "
                         f"{cl['excluded_because']} |")
    return "\n".join(lines) + "\n"


def main():
    inv = build()
    (OUT / "citation_inventory.json").write_text(json.dumps(inv, indent=1) + "\n")
    (OUT / "CITATION_INVENTORY.md").write_text(render_markdown(inv))
    c = inv["counts"]
    print(f"run {inv['current_run_id']}")
    print(f"  RESOLVED  {c['RESOLVED']}   traceable to <= "
          f"{inv['traceable_max_paths']} named paths")
    print(f"  EXCEPTION {c['EXCEPTION']}   registered as outside the run objects")
    print(f"  DERIVED   {c['DERIVED']}   arithmetic over stored fields, recomputed")
    print(f"  SELF_REF  {c['SELF_REFERENTIAL']}   <- a denominator that sums only "
          f"from its own sentence")
    print(f"  HISTORICAL {c['HISTORICAL']}  quoted as having been wrong, in a "
          f"correction region")
    print(f"  AMBIGUOUS {c['AMBIGUOUS']}   in the record, in too many places to cite")
    print(f"  UNSOURCED {c['UNSOURCED']}   <- reported, not fixed")
    print(f"  EXCLUDED  {c['EXCLUDED']}   not claims (year, identifier, code span)")
    print("wrote docs/citation_inventory.json, docs/CITATION_INVENTORY.md")


if __name__ == "__main__":
    main()
