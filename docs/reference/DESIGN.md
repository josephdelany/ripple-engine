> **REFERENCE — SPECIFICATION, NOT A RESULT.** A specification or codebook for the legacy engine's data and rules. It claims no finding; the authoritative result is in [`PAPER.md`](../PAPER.md).

# The desk — design specification

*2026-09-03. Written after reviewing the built desk against its own backend. This is a
specification, not a suggestion: every rule below is testable, and `tests/test_app_render.py`
should grow an assertion for each one marked **[T]**.*

---

## 0. The problem, stated exactly

The backend spends enormous effort separating three things:

1. **what the record shows** — measured, with *n*, from a named file
2. **what someone claimed** — a headline, an analyst, our own earlier draft
3. **how much either can be trusted** — an interval, a *p*, a verdict, a gate

The current front end renders all three in 11px monospace at one weight. A reader cannot
tell the engine's null result from the footnote naming the JSON path it came from. **The
interface destroys the distinction the project exists to make.** That is the defect. It is
not decoration, and it will not be fixed by restyling.

Second, unique problem: **the headline finding is an absence.** Almost every dashboard
pattern in existence is built to show that something is there. This desk must show — at a
glance, without apology, without looking broken — that an interval crosses zero, that 21
of 477 cells fired where 1–24 were expected by chance, that a test no longer rejects.
Absence has to look *deliberate*, not empty.

## 1. The one rule

> **Visual weight equals evidential weight.**

Three tiers, strictly. Nothing on any screen sits outside them.

| tier | what belongs here | treatment |
|---|---|---|
| **Finding** | the answer, in a sentence a person could say aloud | 22–28px, high contrast, one per screen region, never more than ~12 words |
| **Evidence** | the numbers that support it — skill, CI, *p*, *n*, rates | 13–15px, tabular figures, aligned decimals, mid contrast |
| **Provenance** | file paths, run ids, registration references, hashes | 11px, dimmed to ~55%, never above evidence, never bold |

A number without an interval is Evidence tier only if the interval genuinely does not
exist (a count). Otherwise it appears with its interval or not at all. **[T]**

## 2. The absence language

Registered, so it is used identically everywhere:

- **Zero line always drawn.** Any chart of an effect draws a 1px zero rule at full
  contrast, labelled. No exceptions. **[T]**
- **Interval as a bar, estimate as a tick.** A skill of −0.097 [−0.180, −0.018] is a
  horizontal bar spanning the interval with a tick at the point estimate — not a number in
  a cell.
- **Colour carries the verdict, not the sign.** Three states only:
  - `crosses zero` — neutral grey bar. This is the project's most common state and must
    look composed, not broken.
  - `excludes zero, engine worse` — amber
  - `excludes zero, engine better` — green
  Amber and green are used nowhere else in the interface. **[T]**
- **Every null gets a caption in plain words**, not a symbol: *"The interval crosses zero:
  no effect distinguishable from none at this sample size."*
- **Insufficient ≠ null.** A cell with too little data is hatched, never coloured, and
  labelled `insufficient (n=…)`.

## 3. Screen by screen

### 3.1 Story — the flagship, currently empty on arrival

**It must never load empty. [T]** On open with no selection it shows the most material
story from today's feed; if the feed is empty, the most recent corpus event.

Layout, in this order, each a labelled band down the page:

1. **The read** — Finding tier, one sentence generated from the object, e.g.
   *"Priced in. The market moved 8 days before this was reported."* Beneath it the
   as-of date, the class, and the entity chips.
2. **Is it priced?** — the fan chart, with the zero line, the realized path when known,
   and the priced-in fields (front spread, curve slope, OVX percentile, COT percentile)
   as four compact stat cells with "unknown before 2007" shown as literal `unknown`.
3. **Is the narrative right?** — claims extracted from the story, each with its verdict
   chip and `r`/`n`. **Uncheckable claims are collapsed behind a count**, not listed inline.
4. **What is the tail?** — the analog distribution with *n*, worst and best analog named
   and dated, "no adequate precedent" as a first-class state with its own panel.
5. **Where does it travel?** — measured IRFs from `data/ripple/irf.json` where they exist;
   where the hop is null, say so in the absence language rather than omitting the row.
6. **How much to trust this** — the §7 verdicts verbatim, each with its interval bar, the
   run id, the label-audit status, and the falsified hypotheses named. This band is
   Provenance-dense and that is correct — it is the only place small dim type dominates.

### 3.2 Feed — currently leads with noise

Order: **market state → material → in line → noise (collapsed) → blindspots.** The
LOUD/QUIET panels move below the fold; they are a diagnostic, not the lede. **[T]**

Each material item shows its gate ratio as a bar against the everyday base rate, not as a
bare number. The "Read something the feeds missed" box stays at the bottom as the side door.

### 3.3 Ledger — currently reads as broken

The screen presently shows 14 of 15 rows as `Uncheckable` and three scoreboards at 0.
Both are honest and both look like failure.

- **Lead with the checkable.** One Finding-tier line: *"14 claims logged, 1 checkable,
  1 pending resolution. The board turns live at n = 8."*
- **Uncheckable claims collapse behind their count.** They are logged, not displayed. **[T]**
- **A scoreboard with no resolved claims shows the horizon**, not a zero:
  *"First resolution due 2026-09-22."*
- Reader accuracy stays visible, labelled `unaudited gold`.

### 3.4 Walk — good content, no hierarchy

- The four verdict cards become **two**: escalation and price, each Finding tier, each with
  its interval bar and its plain-language caption.
- The baseline tables keep every number but gain the interval bars and lose the boxes.
- **The learning curve needs a zero rule and a frozen-engine line labelled in place.** A
  flat line with no reference communicates nothing.
- "Stand at a date" moves to the top of the screen — it is the demo, and it is the thing a
  visitor will click first.

### 3.5 Big moves — the strongest screen; leave the structure

Only two changes: the class table gets interval bars against the everyday base rate rather
than bare percentages, and `anticipated` becomes a visible column rather than an inline tag.

## 4. Typography and grid

- One typeface for prose (system sans), one for figures (system mono, tabular numerals).
  **Numbers never in a proportional face. [T]**
- 8px baseline grid; 1100px max content width; three densities of vertical rhythm
  (32 / 16 / 8) and nothing between.
- Dark ground stays. Contrast: Finding ≥ 12:1, Evidence ≥ 7:1, Provenance ≥ 4.5:1
  against the ground. **[T]**
- No card borders where a spacing rule will do. The current interface is a grid of boxes;
  boxes are the cheapest possible hierarchy and read as a template.

## 5. The record bar

Currently a 200-character string. Becomes a fixed strip of **named fields**:

```
CORPUS 313 · GEO 187 · LABELS 184 · READS 313 · G null (−0.097) · P null (−0.071)
RUN 003422Z · AUDIT 1/30 · as of 2026-08-25
```

Each field labelled above its value in Provenance tier; the two verdicts in Evidence tier
with their colour from §2. It is a status line, not a sentence. **[T]**

## 6. What must not happen

- No number appears without the file it came from being reachable in one click.
- No word stronger than the record: no "predicts", "validated", "signal", "confirms".
  The existing test that greps for VALIDATED extends to this list. **[T]**
- No decorative chart. Every mark encodes an estimate, an interval, or a count.
- No empty state that looks like a bug. Every empty region states *why* it is empty and
  *when* it will fill.
- No colour outside: ground, three text tiers, amber, green, and the hatch for insufficient.

## 7. Precedents, and what is taken from each

- **Bloomberg Terminal** — density is not the enemy of clarity; hierarchy is earned by
  importance, and a strict luminance ladder does the work that boxes and borders do badly.
- **Metaculus** — a forecast is shown *with* its track record and calibration, never alone;
  the interface treats being wrong as ordinary and displays it without shame.
- **Uncertainty-visualisation literature** (Wilke; Hullman et al.) — intervals as shaded
  bands rather than error bars, and a plain-language caption for every interval: *"we are
  95% sure the value falls in this range."*
- **Our World in Data / FT** — one sentence of finding above every chart, and the source
  line beneath it, always.

Sources consulted are listed in the commit message for this file.

---

## Amendment 1 — the propagation band's binding to `data/ripple/irf.json`
*2026-09-03. Registered before the code that reads under it (SESSION_CHARTER §2 rule 2).*

§3.1 band 5 ("Where does it travel?") said *measured IRFs from `data/ripple/irf.json`*
without saying **which** of the 932 estimates. This amendment fixes the selection, the
interval, and the words, so the band cannot be re-cut after seeing it.

Until now band 5 was wired to `src/propagate.py`, which conditioned its contributing
events on `sr_outcome_90` — a label retired at κ≈0 on 2026-09-02 (OUTCOME_MAPPING.md
Amendment 1). Nothing may condition on a retired label. The filter goes; the band moves
to the registered local projections.

### A1.1 Selection — one class, every registered cell

For a story of class `C`, the band shows every row of `data/ripple/irf.json` with:

| field | value | why |
|---|---|---|
| `shock` | `C` | the story's own class; the seven corpus classes map 1:1 onto the registered shock sets |
| `spec` | `total` | the primary specification. `crude_conditioned` is the mechanism decomposition and carries **no verdict** — it is not a display layer |
| `sample` | `full` | excludes the gas structural-break subsamples (`pre_/post_2009`, registration [2.7]) |

That is **53 cells** for each of the seven classes. All 53 are shown. **The band is never
filtered by verdict, by significance, or by whether the interval is interesting.** Where a
class is absent from the file the band states that and shows nothing.

### A1.2 What each cell displays

At the row's own registered `headline_h` (never a horizon chosen after the fact):

- **estimate** — `beta`
- **band** — `[lo95, hi95]`, Eicker–Huber–White HC1, the registered primary standard error
  (Montiel Olea & Plagborg-Møller 2021). `lo90/hi90` and the Newey–West `se_nw` are carried
  as Provenance, never as the headline band.
- **n** — `n_events`, always beside the estimate; `T` as Provenance
- **verdict** — `TRANSMITTING` / `NULL` / `INSUFFICIENT` verbatim from the file. The band
  never computes a verdict of its own.
- **unit** — `%` for `log` / `log1p` transforms; index points for `lvl` / `pp`

### A1.3 Verdict → colour → caption (the §2 absence language, bound)

| verdict | state | colour | caption |
|---|---|---|---|
| `NULL` | `crosses_zero` | neutral grey | *"The interval crosses zero: no effect distinguishable from none at this sample size."* |
| `NULL` + `fragile` | `crosses_zero` | neutral grey | *"Reported null and flagged fragile: the EHW interval excludes zero, Newey–West does not."* |
| `TRANSMITTING` | `excludes_zero` | green | *"The 95% interval excludes zero under both standard errors, and the estimate sits outside the state-matched placebo band."* |
| `INSUFFICIENT` | `insufficient` | hatch, never coloured | *"insufficient (n=…): below the registered minimum of 15 events."* |

**Amber is not used in this band.** §2 reserves amber for *excludes zero, engine worse* — a
walk-forward comparison against a baseline. A local projection has no baseline to be worse
than, so the amber state does not arise here. It is left unused rather than repurposed.

The zero line is drawn on every cell (§2), including the insufficient ones.

### A1.4 Order, and the finding sentence

Cells are grouped by the registration's hop ladder, in this order, and within a hop in the
order the registration lists the nodes:

`0` crude · `1` refined products & cracks · `2` physical flow & stocks · `3` gas & LNG ·
`4` fertiliser & coal · `x` macro cross-asset · `e` equity proxies

The Finding-tier sentence above the band is a count, not an adjective:

> *"k of 53 registered cells transmit for this class."*

Where `k = 0` the sentence says so in words — *"No cell transmits for this class"* — and the
band is still drawn in full. **A class with nothing transmitting is the finding, not an
empty state.** **[T]**

### A1.5 Provenance carried with the band

`data/ripple/irf.json` · `meta.registration` (RIPPLE_REGISTRATION.md + Amendments A, B) ·
`meta.when` · `meta.seed` · `meta.n_placebo`. Displayed in Provenance tier, per §1.

### A1.6 What this amendment does not do

It does not re-run, re-estimate, or re-cut anything in `data/ripple/`. It is a read. The
estimates were computed once under the sealed registration and are displayed as computed.

---

## Amendment 1 — 2026-09-03, after session A read the spec against the code

*Two errors in §4 and §6 as first written, and one rule the spec did not have. Registered
before the build starts. Nothing above is edited.*

**A1.1 The spec failed its own contrast rule.** §4 requires Provenance ≥ 4.5:1 against the
ground; the colour as built measures **3.65**. Provenance becomes `#8a8880`, which clears
4.5:1 with headroom. Finding and Evidence pass as they stand. A test measures all three
rather than trusting the hex values.

**A1.2 The forbidden-word rule was unimplementable as written.** §6 bans "predicts",
"validated", "signal", "confirms" and the existing test greps all rendered text. But the
desk must render corpus titles **verbatim** — and three live records contain a banned
substring, including the event title *"Russia confirms floating wheat export tax"*. A rule
that forces the desk to alter a source title is worse than no rule: it would make the
interface edit the record to satisfy a lint.

The rule splits, as session A proposed:

- **Absolute ban on every string the desk writes itself** — labels, captions, verdict text,
  headings, generated sentences. No exception, no escape hatch.
- **Verbatim quoted material** — corpus titles, headline text, claim text, source
  sentences — renders inside a node marked `data-verbatim` with its source attribute. The
  test **inventories** these rather than banning them: it asserts every banned word found
  in rendered text sits inside a `data-verbatim` node, and prints the inventory so a
  reviewer can see exactly which source strings carry them. **[T]**

The distinction is the project's own: what the desk asserts is bound by the record; what a
source said is reported as the source said it.

**A1.3 Nothing in this spec would have been verified in CI.** Both jsdom tests skip where
node is absent, and the render test additionally skips whenever the database is, which is
always in CI. The spec's rules therefore split into two files: `tests/test_design_spec.py`,
which is static and runs everywhere (contrast ratios, palette membership, vocabulary,
tier-class presence), and the jsdom tests, which cover DOM structure and may skip. **A
rule that can only be checked where the checker never runs is not a rule. [T]**

**A1.4 A render test had silently stopped testing.** `tests/test_app_render.py` strips the
page bootstrap with a regex anchored to `loadFeed();`; that line now reads
`loadFeed(); loadRecord();`, the anchor no longer matches, and the boot path has been
running inside the test — passing only because both calls swallow their own fetch failure.
Session A found this while reading the spec against the code. The replacement must not
depend on matching a source line: strip by a stable marker the page emits for the purpose,
and assert the marker exists. **[T]**
