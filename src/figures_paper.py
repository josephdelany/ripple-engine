"""
figures_paper.py -- the three paper figures. Session I.

Three PNGs into docs/figures/, 150 dpi, legible at half size. They generate NO
analysis: every number is READ from a committed file and every figure carries the
path it was read from. If a source file changes, the figures change; if a source
file is missing or its shape has moved, this script raises rather than drawing
something plausible.

  fig1_vintage.png              the project's whole argument in one image
                                left  -- the corpus, split by whether any state
                                         field was knowable at t
                                right -- escalation Brier skill vs climatology,
                                         before and after Amendment H
  fig2_escalation_baselines.png Brier levels, lower is better: persistence,
                                climatology, the engine, M13 recalibrated
  fig3_price_baselines.png      price CRPS skill vs each of the four baselines

Sources, in full (nothing else is read):

  data/walk_forward/summary.json   the published run. Everything except the
                                   pre-Amendment-H comparison.
  data/state/situation_knowable.json  the vintage filter's own counts.
  STATE_OF_THE_ENGINE.md           section 5 -- the pre-Amendment-H point
                                   estimate at full precision (run 193022Z).
  data/handoffs/B_run_delta.md     the 193022Z column -- that estimate's 95% CI.

  The last two are needed because summary.json publishes ONE run and the
  before/after panel needs two. This is stated on the figure itself, not
  hidden: the right panel names all three files. The two are cross-checked
  against each other (same estimate to 4 dp) and the script fails if they
  disagree.

Design rules obeyed -- DESIGN.md section 2, "the absence language":
  - the zero rule is drawn on every chart of an effect, at full contrast, labelled
  - an interval is a BAR; the estimate is a TICK on it; never a bare number
  - colour carries the verdict, never the sign:
        crosses zero .................. neutral grey  (composed, not broken)
        excludes zero, engine worse ... amber
        excludes zero, engine better .. green
  - every null carries its caption in plain words
  - insufficient is hatched, never coloured

Ground is light, not the desk's dark: these figures are for docs/BRIEF.md,
README.md and the paper, which render on a light page. DESIGN section 2 (the
absence language) governs and is obeyed exactly; section 4's dark ground is a
property of the desk interface and does not travel to print. The three text
tiers keep their section 4 contrast floors and the script asserts them.

Run:  python3 src/figures_paper.py
"""

import json
import re
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "figures"

SUMMARY = "data/walk_forward/summary.json"
KNOWABLE = "data/state/situation_knowable.json"
STATE_OF = "STATE_OF_THE_ENGINE.md"
RUN_DELTA = "data/handoffs/B_run_delta.md"

# The run whose numbers STATE_OF_THE_ENGINE.md section 5 and B_run_delta.md's
# third column describe: the last run before Amendment H was enforced.
PRE_H_RUN = "walk_20260902T193022Z"


# ---------------------------------------------------------------------------
# palette -- DESIGN.md section 1 (three tiers) and section 2 (three verdicts)
# ---------------------------------------------------------------------------

GROUND = "#ffffff"
FINDING = "#101010"     # section 4 floor: >= 12:1
EVIDENCE = "#2b2a26"    # section 4 floor: >=  7:1
PROVENANCE = "#6f6d66"  # section 4 floor: >= 4.5:1 (the desk's Amendment A1.1 defect,
                        # not repeated here)

VERDICT_COLOR = {
    "crosses_zero": "#6f6d66",           # neutral grey
    "excludes_zero_worse": "#a15c00",    # amber
    "excludes_zero_better": "#14713f",   # green
}
VERDICT_CAPTION = {
    "crosses_zero":
        "The interval crosses zero: no effect distinguishable from none at this "
        "sample size.",
    "excludes_zero_worse":
        "The 95% interval excludes zero, and the engine is on the wrong side of it.",
    "excludes_zero_better":
        "The 95% interval excludes zero in the engine's favour.",
}

MONO = ["DejaVu Sans Mono"]   # ships with matplotlib; numbers are never proportional


def _relative_luminance(hex_color):
    """WCAG relative luminance of an #rrggbb string."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(fg, bg=GROUND):
    """WCAG contrast ratio. Used to assert the section 4 floors, not to trust hexes."""
    a, b = _relative_luminance(fg), _relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def assert_contrast():
    """DESIGN section 4: Finding >= 12:1, Evidence >= 7:1, Provenance >= 4.5:1.

    Measured, never assumed -- this is the check the desk's own spec failed
    (DESIGN.md Amendment A1.1). Verdict colours are held to the Provenance
    floor because they are read as text as well as drawn as bars.
    """
    floors = [(FINDING, 12.0, "finding"), (EVIDENCE, 7.0, "evidence"),
              (PROVENANCE, 4.5, "provenance")]
    floors += [(c, 4.5, f"verdict:{k}") for k, c in VERDICT_COLOR.items()]
    for color, floor, name in floors:
        ratio = contrast(color)
        if ratio < floor:
            raise AssertionError(
                f"{name} {color} measures {ratio:.2f}:1 against the ground, "
                f"below the DESIGN section 4 floor of {floor}:1")
    return {name: round(contrast(c), 2) for c, _, name in floors}


def verdict_of(lo, hi):
    """DESIGN section 2. Three states, decided by the interval, never by the sign.

    'worse'/'better' are the ENGINE's side of the comparison, so the caller
    passes an interval already oriented as engine-minus-reference skill.
    """
    if lo <= 0.0 <= hi:
        return "crosses_zero"
    return "excludes_zero_better" if lo > 0.0 else "excludes_zero_worse"


# ---------------------------------------------------------------------------
# sources -- read, never typed
# ---------------------------------------------------------------------------

def _read(rel):
    p = ROOT / rel
    if not p.exists():
        raise FileNotFoundError(f"{rel} is not in the tree; this script reads it")
    return p


def load_summary():
    return json.loads(_read(SUMMARY).read_text())


def load_knowable():
    return json.loads(_read(KNOWABLE).read_text())


def _num(text):
    """Every number in a string, with the typographic minus normalised to ASCII."""
    return [float(x) for x in re.findall(r"[-+]?\d+\.\d+", text.replace("−", "-"))]


def load_pre_amendment_h():
    """The escalation skill from the run BEFORE Amendment H, with its 95% CI.

    Not in summary.json -- that file publishes one run. The point estimate comes
    at full precision from STATE_OF_THE_ENGINE.md section 5; the interval from
    the 193022Z column of B_run_delta.md. Both are asserted to be describing
    PRE_H_RUN, and the two estimates are cross-checked to 4 dp.
    """
    # --- point estimate, STATE_OF_THE_ENGINE.md section 5 -------------------
    soe = _read(STATE_OF).read_text()
    section = soe.split("## 5. The walk")
    if len(section) < 2:
        raise ValueError(f"{STATE_OF}: section 5 (the walk) not found")
    body = section[1].split("\n## ")[0]
    if PRE_H_RUN not in body:
        raise ValueError(
            f"{STATE_OF} section 5 no longer describes {PRE_H_RUN}; it has been "
            f"re-run. The before/after panel needs a source for the pre-Amendment-H "
            f"number -- find it and repoint this loader, do not guess.")
    m = re.search(r"daily tier:.*?G skill vs climatology "
                  r"(-?\d+\.\d+) \(dm_p (-?\d+\.\d+)\)", body)
    if not m:
        raise ValueError(f"{STATE_OF} section 5: daily G skill line did not parse")
    skill, dm_p = float(m.group(1)), float(m.group(2))

    # --- interval, B_run_delta.md, the 193022Z column ------------------------
    delta = _read(RUN_DELTA).read_text()
    header = next((ln for ln in delta.splitlines()
                   if ln.startswith("| comparison |")), None)
    if header is None:
        raise ValueError(f"{RUN_DELTA}: the comparison table header is gone")
    cols = [c.strip() for c in header.strip().strip("|").split("|")]
    short = PRE_H_RUN.split("T")[1]          # '193022Z'
    if short not in cols:
        raise ValueError(f"{RUN_DELTA}: no column for {short}; columns are {cols}")
    idx = cols.index(short)
    row = next((ln for ln in delta.splitlines()
                if ln.startswith("| G Brier vs climatology, skill |")), None)
    if row is None:
        raise ValueError(f"{RUN_DELTA}: the 'G Brier vs climatology, skill' row is gone")
    cell = [c.strip() for c in row.strip().strip("|").split("|")][idx]
    vals = _num(cell)
    if len(vals) < 4:
        raise ValueError(f"{RUN_DELTA}: could not parse estimate+CI+p from {cell!r}")
    est_4dp, lo, hi, p = vals[0], vals[1], vals[2], vals[3]

    # --- the two files must agree -------------------------------------------
    if round(skill, 4) != round(est_4dp, 4):
        raise AssertionError(
            f"{STATE_OF} says {skill} and {RUN_DELTA} says {est_4dp} for the same "
            f"run {PRE_H_RUN}. They disagree; the figure is not drawn.")
    if not (lo <= skill <= hi):
        raise AssertionError(f"pre-Amendment-H estimate {skill} sits outside its "
                             f"own interval [{lo}, {hi}]")
    return {"skill": skill, "ci95": [lo, hi], "dm_p": dm_p, "p_reported": p,
            "run_id": PRE_H_RUN,
            "sources": [f"{STATE_OF} section 5", f"{RUN_DELTA} ({short} column)"]}


# ---------------------------------------------------------------------------
# drawing primitives -- DESIGN section 2
# ---------------------------------------------------------------------------

# One vertical stack under every axes, at fixed figure fractions, so nothing
# collides: units -> direction cue -> the absence caption -> provenance.
FIGSIZE = (13.0, 7.6)
BOTTOM = 0.345
Y_UNITS = 0.285
Y_DIRECTION = 0.240
Y_CAPTION = 0.196
Y_PROVENANCE = 0.012


def zero_rule(ax, label):
    """DESIGN section 2: 'Any chart of an effect draws a 1px zero rule at full
    contrast, labelled. No exceptions.' The label sits inside the plot area,
    to the right of the line, where nothing else is drawn."""
    ax.axvline(0.0, color=FINDING, lw=1.0, zorder=4)
    ax.annotate(label, xy=(0.0, 1.0), xycoords=("data", "axes fraction"),
                xytext=(5, -4), textcoords="offset points",
                ha="left", va="top", fontsize=8.5, color=FINDING, fontfamily=MONO)


def interval_bar(ax, y, est, lo, hi, state, height=0.30):
    """The interval as a bar; the estimate as a tick. Never a number in a cell."""
    color = VERDICT_COLOR[state]
    ax.barh(y, hi - lo, left=lo, height=height, color=color, alpha=0.30,
            edgecolor=color, linewidth=1.0, zorder=3)
    ax.plot([est, est], [y - height / 2, y + height / 2],
            color=color, lw=2.4, solid_capstyle="butt", zorder=5)


def fmt(x, dp=3):
    """Signed, fixed width, typographic minus. Tabular figures everywhere."""
    return f"{x:+.{dp}f}".replace("-", "\u2212")


def pval(p):
    return f"$p$ = {p:.3f}" if p >= 0.001 else "$p$ < 0.001"


def wrap(text, width):
    """Wrap to `width`, keeping any line break the caller wrote deliberately."""
    return "\n".join("\n".join(textwrap.wrap(line, width)) if line.strip() else line
                     for line in text.split("\n"))


def heading(fig, title, standfirst, width=132):
    """Finding tier, then one Evidence-tier sentence. DESIGN section 1."""
    fig.suptitle(title, x=0.008, y=0.972, ha="left", fontsize=17.5,
                 color=FINDING, fontweight="bold")
    fig.text(0.008, 0.916, wrap(standfirst, width), fontsize=10.8, color=EVIDENCE,
             ha="left", va="top", linespacing=1.45)


def units(fig, text, x=0.008, ha="left"):
    fig.text(x, Y_UNITS, text, fontsize=10.5, color=EVIDENCE, ha=ha, va="top")


def direction(fig, x0, x1, left="\u25c0  engine worse", right="engine better  \u25b6",
              emphasis=False):
    fig.text(x0, Y_DIRECTION, left, fontsize=11.5 if emphasis else 9.6,
             color=FINDING if emphasis else EVIDENCE, ha="left", va="top",
             fontweight="bold" if emphasis else "normal")
    fig.text(x1, Y_DIRECTION, right, fontsize=9.6, color=EVIDENCE,
             ha="right", va="top")


def caption(fig, text, x=0.008, width=150):
    """DESIGN section 2: every null gets a caption in plain words, not a symbol."""
    fig.text(x, Y_CAPTION, wrap(text, width), fontsize=9.3, color=EVIDENCE,
             ha="left", va="top", linespacing=1.5)


def provenance(fig, text):
    """DESIGN section 1: file paths are Provenance tier -- dimmed, never bold."""
    fig.text(0.008, Y_PROVENANCE, text, fontsize=7.6, color=PROVENANCE,
             fontfamily=MONO, ha="left", va="bottom", linespacing=1.5)


def style():
    plt.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 150,
        "figure.facecolor": GROUND, "savefig.facecolor": GROUND,
        "axes.facecolor": GROUND,
        "font.size": 10.5, "text.color": EVIDENCE,
        "axes.labelcolor": EVIDENCE, "axes.edgecolor": PROVENANCE,
        "xtick.color": EVIDENCE, "ytick.color": EVIDENCE,
        "axes.grid": False, "axes.axisbelow": True,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.unicode_minus": True,
    })


# A value label may pass over the zero rule. It sits ON the ground, never on the
# line: an opaque backing box in the ground colour, drawn above the rule.
LABEL_BOX = {"facecolor": GROUND, "edgecolor": "none", "pad": 1.6}


def row_label(ax, x, y, text, color, fontsize=11):
    ax.annotate(text, xy=(x, y), ha="left", va="bottom", fontsize=fontsize,
                color=color, fontfamily=MONO, bbox=LABEL_BOX, zorder=6)


def row_name(ax, y, name, sub, emphasis=False):
    """A row's label in the left margin: the name, then a smaller second line.

    Drawn rather than set as a tick label because a two-line tick label centres
    on the row and collides with itself; these stack cleanly around the row.
    """
    ax.annotate(name, xy=(0.0, y), xycoords=("axes fraction", "data"),
                xytext=(-10, 2), textcoords="offset points",
                ha="right", va="bottom", fontsize=11.5,
                color=FINDING if emphasis else EVIDENCE,
                fontweight="bold" if emphasis else "normal")
    ax.annotate(sub, xy=(0.0, y), xycoords=("axes fraction", "data"),
                xytext=(-10, -3), textcoords="offset points",
                ha="right", va="top", fontsize=9.2, color=PROVENANCE)


def axes_span(ax):
    """An axes' left and right edge in figure coordinates.

    Asked of the axes rather than written as a constant. The right panel's hardcoded
    x-position happened to equal persistence's Brier score after the Amendment 4
    re-run, and tripped the no-literal-results test -- a false alarm, but a true
    signal that magic layout numbers and published results were sharing a namespace.
    The layout now has no bare numbers left to collide with, and this docstring
    quotes none either, which is why the value is described rather than printed.
    """
    box = ax.get_position()
    return box.x0, box.x1


def mono_ticks(ax):
    ax.tick_params(axis="x", labelsize=9.5)
    for lab in ax.get_xticklabels():
        lab.set_fontfamily(MONO)


# ---------------------------------------------------------------------------
# figure 1 -- the vintage figure: the argument in one image
# ---------------------------------------------------------------------------

def fig1_vintage(summary, knowable, pre_h):
    daily_g = summary["tiers"]["daily"]["G"]["engine_vs"]["climatology"]
    post = {"skill": daily_g["skill"], "ci95": daily_g["ci95"],
            "dm_p": daily_g["dm_p"], "n": daily_g["n"]}

    total = knowable["events"]
    without = knowable["events_with_no_situation_field_at_t"]
    with_state = total - without                      # derived, never typed
    kept_fields = knowable["kept"]
    dropped_fields = knowable["dropped_after_t"]

    fig, (axl, axr) = plt.subplots(1, 2, figsize=FIGSIZE,
                                   gridspec_kw={"width_ratios": [1.0, 1.0]})
    fig.subplots_adjust(left=0.040, right=0.980, top=0.800, bottom=BOTTOM,
                        wspace=0.44)

    heading(fig, "The vintage rule, and what it cost",
            "Enforcing \u201cknowable on the day\u201d on the per-event state fields "
            "(Amendment H) emptied the state vector \u2014 and the engine\u2019s parity "
            "with the base rate went with it.", width=168)

    # -- left panel: the cause ----------------------------------------------
    axl.set_title(f"{without} of {total} events have no state field knowable at $t$",
                  loc="left", fontsize=14, color=FINDING, pad=18)
    axl.barh(0, with_state, left=0, height=0.34, color=PROVENANCE, alpha=0.85,
             edgecolor=PROVENANCE, linewidth=1.0, zorder=3)
    # DESIGN section 2: insufficient is hatched, never coloured.
    axl.barh(0, without, left=with_state, height=0.34, facecolor=GROUND,
             edgecolor=PROVENANCE, hatch="////", linewidth=1.0, zorder=3)

    axl.annotate(f"{with_state}", xy=(with_state / 2, 0.22), ha="center",
                 va="bottom", fontsize=15, color=FINDING, fontfamily=MONO,
                 fontweight="bold")
    axl.annotate("with a state field\nknowable at $t$",
                 xy=(with_state / 2, 0.52), ha="center", va="bottom",
                 fontsize=10.2, color=EVIDENCE, linespacing=1.45)
    axl.annotate(f"{without}", xy=(with_state + without / 2, 0.22), ha="center",
                 va="bottom", fontsize=15, color=FINDING, fontfamily=MONO,
                 fontweight="bold")
    axl.annotate("with none \u2014 retrieval falls back\nto the market block alone",
                 xy=(with_state + without / 2, 0.52), ha="center", va="bottom",
                 fontsize=10.2, color=EVIDENCE, linespacing=1.45)
    axl.annotate(f"{100 * with_state / total:.1f}%", xy=(with_state / 2, -0.24),
                 ha="center", va="top", fontsize=9.6, color=PROVENANCE,
                 fontfamily=MONO)
    axl.annotate(f"{100 * without / total:.1f}%",
                 xy=(with_state + without / 2, -0.24), ha="center", va="top",
                 fontsize=9.6, color=PROVENANCE, fontfamily=MONO)

    axl.set_xlim(0, total)
    axl.set_ylim(-0.58, 1.45)
    axl.set_yticks([])
    axl.set_xticks([0, with_state, total])
    mono_ticks(axl)

    # -- right panel: the consequence ---------------------------------------
    axr.set_title("Escalation Brier skill vs climatology, before and after",
                  loc="left", fontsize=14, color=FINDING, pad=18)

    rows = [
        ("after Amendment H", summary["run_id"].split("walk_")[1],
         post["skill"], post["ci95"][0], post["ci95"][1], post["dm_p"]),
        ("before Amendment H", pre_h["run_id"].split("walk_")[1],
         pre_h["skill"], pre_h["ci95"][0], pre_h["ci95"][1], pre_h["dm_p"]),
    ]
    xlo, xhi = -0.30, 0.23
    label_x = xlo + 0.012
    for i, (label, run, est, lo, hi, p) in enumerate(rows):
        state = verdict_of(lo, hi)
        interval_bar(axr, i, est, lo, hi, state, height=0.26)
        row_label(axr, label_x, i + 0.20,
                  f"{fmt(est)}  [{fmt(lo)}, {fmt(hi)}]   {pval(p)}",
                  VERDICT_COLOR[state])
        axr.annotate(f"run {run}", xy=(label_x, i - 0.20), ha="left", va="top",
                     fontsize=8.2, color=PROVENANCE, fontfamily=MONO)

    axr.set_yticks([0, 1])
    axr.set_yticklabels([r[0] for r in rows], fontsize=11.5, color=EVIDENCE)
    axr.tick_params(axis="y", length=0, pad=8)
    axr.set_ylim(-0.85, 1.75)
    axr.set_xlim(xlo, xhi)
    mono_ticks(axr)
    zero_rule(axr, "0 = parity with the base rate")

    # -- the stack under both panels ----------------------------------------
    left_x0, _ = axes_span(axl)
    right_x0, right_x1 = axes_span(axr)
    units(fig, f"events in the corpus  (n = {total})", x=left_x0)
    units(fig, f"Brier skill vs climatology, 95% CI   (daily tier, "
               f"n = {post['n']} scored escalation reads)", x=right_x0)
    direction(fig, right_x0, right_x1)
    caption(fig,
            f"Left \u2014 at field level, {kept_fields} situation fields survive "
            f"the rule and {dropped_fields} are dropped as dated after $t$.\n"
            f"Right, before \u2014 " + VERDICT_CAPTION["crosses_zero"] + "\n"
            f"Right, after \u2014 the interval excludes zero: the engine is "
            f"significantly worse than the base rate it was built to beat.",
            width=165)
    provenance(fig,
               f"left   {KNOWABLE}  \u00b7  events, "
               f"events_with_no_situation_field_at_t, kept, dropped_after_t\n"
               f"right  {SUMMARY}  \u00b7  tiers.daily.G.engine_vs.climatology  "
               f"(run {summary['run_id']})\n"
               f"       {pre_h['sources'][0]}  \u00b7  {pre_h['sources'][1]}  "
               f"\u2014 the before-run is not in summary.json, which publishes "
               f"one run\n"
               f"drawn by  src/figures_paper.py")
    return fig, {"total": total, "with_state": with_state, "without": without,
                 "kept_fields": kept_fields, "dropped_fields": dropped_fields,
                 "post": post, "pre": pre_h}


# ---------------------------------------------------------------------------
# figure 2 -- escalation baselines, as levels
# ---------------------------------------------------------------------------

def fig2_escalation_baselines(summary):
    g = summary["tiers"]["daily"]["G"]
    ev = g["engine_vs"]
    items = g["items_vs_climatology"]
    clim = ev["climatology"]
    n = clim["n"]

    # Four levels. In every block 'engine_mean' is that block's own mean score and
    # 'ref_mean' is the reference's. Each is read; none is arithmetic of ours.
    rows = [
        {"label": "persistence", "sub": "the dyad\u2019s own IES-90, carried forward",
         "brier": ev["persistence"]["ref_mean"],
         "cmp": ("engine skill vs this baseline", ev["persistence"]["skill"],
                 ev["persistence"]["ci95"], ev["persistence"]["dm_p"])},
        {"label": "climatology", "sub": "the unconditional base rate",
         "brier": clim["ref_mean"],
         "cmp": ("engine skill vs this baseline", clim["skill"], clim["ci95"],
                 clim["dm_p"])},
        {"label": "the engine", "sub": "Hedge mixture, 13-item menu",
         "brier": clim["engine_mean"], "cmp": None},
        {"label": "M13 recalibrated", "sub": "walk-forward isotonic / Platt (Amendment C)",
         "brier": items["M13_recalibrated"]["engine_mean"],
         "cmp": ("M13 skill vs climatology", items["M13_recalibrated"]["skill"],
                 items["M13_recalibrated"]["ci95"],
                 items["M13_recalibrated"]["dm_p"])},
    ]
    rows.sort(key=lambda r: r["brier"])              # best (lowest) first

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.235, right=0.965, top=0.800, bottom=BOTTOM)

    heading(fig, "Escalation: what each rule actually scores",
            "A rule using only the dyad\u2019s own last 90 days beats the "
            "state-conditioned analogue engine. Recalibration, registered in advance "
            "as the explanation for the null, made it worse.", width=150)

    ys = list(range(len(rows)))[::-1]                # best at the top
    for y, r in zip(ys, rows):
        is_engine = r["cmp"] is None
        if is_engine:
            color, alpha = FINDING, 0.92
        else:
            color = VERDICT_COLOR[verdict_of(r["cmp"][2][0], r["cmp"][2][1])]
            alpha = 0.30
        ax.barh(y, r["brier"], height=0.40, color=color, alpha=alpha,
                edgecolor=color, linewidth=1.1, zorder=3)
        ax.annotate(f"{r['brier']:.3f}", xy=(r["brier"], y), xytext=(10, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=13.5, color=FINDING, fontfamily=MONO,
                    fontweight="bold" if is_engine else "normal")
        if is_engine:
            note = "the engine itself \u2014 the thing being compared, so no verdict"
        else:
            title, sk, ci, pv = r["cmp"]
            note = (f"{title}:  {fmt(sk)}  [{fmt(ci[0])}, {fmt(ci[1])}]   "
                    f"{pval(pv)}")
        ax.annotate(note, xy=(0.0, y - 0.27), xycoords=("data", "data"),
                    xytext=(4, 0), textcoords="offset points",
                    ha="left", va="top", fontsize=9.2, color=PROVENANCE,
                    fontfamily=MONO)
        row_name(ax, y, r["label"], r["sub"], emphasis=is_engine)

    ax.set_yticks([])
    ax.set_ylim(-0.80, len(rows) - 0.42)
    ax.set_xlim(0, max(r["brier"] for r in rows) * 1.16)
    mono_ticks(ax)
    # DESIGN section 2: the zero rule is drawn, at full contrast, labelled.
    # On a proper score, zero is a perfect forecast -- and the 'better' end.
    zero_rule(ax, "0 = a perfect forecast")
    ax_x0, ax_x1 = axes_span(ax)

    units(fig, f"Brier score \u2014 multi-category over IES-90 levels 0\u20133, "
               f"horizon (d, d+90]   (n = {n} scored escalation reads)", x=ax_x0)
    direction(fig, ax_x0, ax_x1, left="\u25c0  LOWER IS BETTER", right="worse  \u25b6",
              emphasis=True)
    caption(fig,
            "Bar colour is the verdict on the comparison printed beneath the bar, "
            "never the level: amber where the 95% interval excludes zero against the "
            "engine. The engine\u2019s own bar carries no verdict.",
            x=ax_x0, width=125)
    provenance(fig,
               f"{SUMMARY}   (run {summary['run_id']})\n"
               f"  levels     tiers.daily.G.engine_vs.<persistence|climatology>"
               f".ref_mean  \u00b7  ...engine_vs.climatology.engine_mean  \u00b7  "
               f"...items_vs_climatology.M13_recalibrated.engine_mean\n"
               f"  intervals  ...engine_vs.<ref>.skill / .ci95 / .dm_p   \u00b7   "
               f"...items_vs_climatology.M13_recalibrated.skill / .ci95 / .dm_p\n"
               f"drawn by  src/figures_paper.py")
    return fig, rows


# ---------------------------------------------------------------------------
# figure 3 -- price baselines, as skill
# ---------------------------------------------------------------------------

def fig3_price_baselines(summary):
    ev = summary["tiers"]["daily"]["P"]["engine_vs"]
    order = ["persistence", "frozen", "random_analogs", "climatology"]
    rows = [{"ref": k, **ev[k]} for k in order]
    n = rows[0]["n"]

    pretty = {"persistence": ("vs persistence", "last observed level, carried forward"),
              "frozen": ("vs frozen", "the same mixture, weights never updated"),
              "random_analogs": ("vs random analogues",
                                 "same k, drawn at random from the corpus"),
              "climatology": ("vs climatology", "the unconditional distribution")}

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.235, right=0.965, top=0.800, bottom=BOTTOM)

    heading(fig, "Price: CRPS skill against each of the four baselines",
            "The engine beats persistence and its own frozen self, is "
            "indistinguishable from random analogues, and loses to the unconditional "
            "distribution.", width=150)

    ys = list(range(len(rows)))[::-1]
    states = []
    for y, r in zip(ys, rows):
        lo, hi = r["ci95"]
        state = verdict_of(lo, hi)
        states.append(state)
        interval_bar(ax, y, r["skill"], lo, hi, state, height=0.30)
        row_label(ax, lo, y + 0.22,
                  f"{fmt(r['skill'])}  [{fmt(lo)}, {fmt(hi)}]   {pval(r['dm_p'])}",
                  VERDICT_COLOR[state])
        row_name(ax, y, pretty[r["ref"]][0], pretty[r["ref"]][1])

    ax.set_yticks([])
    ax.set_ylim(-0.80, len(rows) - 0.32)
    lo_all = min(r["ci95"][0] for r in rows)
    hi_all = max(r["ci95"][1] for r in rows)
    span = hi_all - lo_all
    ax.set_xlim(lo_all - 0.12 * span, hi_all + 0.12 * span)
    mono_ticks(ax)
    zero_rule(ax, "0 = no better, no worse")
    ax_x0, ax_x1 = axes_span(ax)

    units(fig, f"CRPS skill, engine vs baseline, 95% CI   (daily tier, "
               f"+20 trading days, n = {n} scored price reads)", x=ax_x0)
    direction(fig, ax_x0, ax_x1)
    # DESIGN section 2: every null gets a caption in plain words, not a symbol.
    null_refs = [pretty[r["ref"]][0][3:] for r, st in zip(rows, states)
                 if st == "crosses_zero"]
    caption(fig,
            "Grey \u2014 " + VERDICT_CAPTION["crosses_zero"]
            + (f"  Here: {', '.join(null_refs)}." if null_refs else "")
            + "\nAmber \u2014 the interval excludes zero and the engine is worse.   "
              "Green \u2014 the interval excludes zero and the engine is better.",
            x=ax_x0, width=125)
    provenance(fig,
               f"{SUMMARY}   (run {summary['run_id']})\n"
               f"  tiers.daily.P.engine_vs.<persistence|frozen|random_analogs|"
               f"climatology>.skill / .ci95 / .dm_p / .n\n"
               f"drawn by  src/figures_paper.py")
    return fig, rows


# ---------------------------------------------------------------------------

def main():
    style()
    ratios = assert_contrast()

    summary = load_summary()
    knowable = load_knowable()
    pre_h = load_pre_amendment_h()

    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {
        "drawn_by": "src/figures_paper.py",
        "sources": {
            "summary": {"path": SUMMARY, "run_id": summary["run_id"],
                        "generated_at": summary["generated_at"]},
            "knowable": {"path": KNOWABLE, "generated_at": knowable["generated_at"]},
            "pre_amendment_h": {"paths": pre_h["sources"], "run_id": pre_h["run_id"]},
        },
        "contrast_ratios_vs_ground": ratios,
        "figures": {},
    }

    f1, d1 = fig1_vintage(summary, knowable, pre_h)
    f1.savefig(OUT / "fig1_vintage.png", dpi=150)
    plt.close(f1)
    receipt["figures"]["fig1_vintage.png"] = {
        "events": d1["total"], "with_state_knowable_at_t": d1["with_state"],
        "without": d1["without"], "fields_kept": d1["kept_fields"],
        "fields_dropped_after_t": d1["dropped_fields"],
        "skill_before_amendment_h": {"est": d1["pre"]["skill"],
                                     "ci95": d1["pre"]["ci95"],
                                     "dm_p": d1["pre"]["dm_p"],
                                     "run_id": d1["pre"]["run_id"]},
        "skill_after_amendment_h": {"est": d1["post"]["skill"],
                                    "ci95": d1["post"]["ci95"],
                                    "dm_p": d1["post"]["dm_p"],
                                    "n": d1["post"]["n"]},
    }

    f2, d2 = fig2_escalation_baselines(summary)
    f2.savefig(OUT / "fig2_escalation_baselines.png", dpi=150)
    plt.close(f2)
    receipt["figures"]["fig2_escalation_baselines.png"] = {
        "brier": {r["label"]: r["brier"] for r in d2}}

    f3, d3 = fig3_price_baselines(summary)
    f3.savefig(OUT / "fig3_price_baselines.png", dpi=150)
    plt.close(f3)
    receipt["figures"]["fig3_price_baselines.png"] = {
        "crps_skill": {r["ref"]: {"est": r["skill"], "ci95": r["ci95"],
                                  "dm_p": r["dm_p"], "n": r["n"]} for r in d3}}

    (OUT / "figures.json").write_text(json.dumps(receipt, indent=1) + "\n")

    for name in ("fig1_vintage.png", "fig2_escalation_baselines.png",
                 "fig3_price_baselines.png", "figures.json"):
        print(f"wrote docs/figures/{name}  "
              f"({(OUT / name).stat().st_size:,} bytes)")
    print(f"run {summary['run_id']}; contrast floors measured: {ratios}")


if __name__ == "__main__":
    main()
