> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Working record of the pre-1973 admission and vintage work. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# G-7 REGISTRATION — the chokepoint flow register (PHYSICAL_EXPOSURE §2 T2), and a STRUCTURAL vintage stamp for the whole study
*2026-09-03, Session G. Registered BEFORE `src/g_vintage.py` and `src/g_chokepoint_register.py`
exist and BEFORE any exposure value is computed (charter §2 rule 2). Amendments dated and appended.*

## 0. Standing, and what was read or computed before this was written

`PHYSICAL_EXPOSURE_REGISTRATION.md` (66b1c30) is **Cowork's** document and G does not edit it. Joe
assigned G two parts of it on 2026-09-03: **§2 T2**, the chokepoint flow register, and **§3**, the
vintage-stamping discipline **for the whole study**. G writes only `docs/g/**`, `src/g_vintage.py`,
`src/g_chokepoint_register.py` and its own tests, and hands the rest to Cowork.

Read first, and named so the order is checkable: `PHYSICAL_EXPOSURE_REGISTRATION.md` §§0–8;
`WORLD_STATE_CODEBOOK.md` Amendment 1 (which §3 makes governing); `WALK_FORWARD_PROTOCOL.md`
Amendment F.1 (the standing Joe asked the filtration test to have); the PortWatch assets already in
the tree (`data/seed/ripple/portwatch.*.csv`, `data/portwatch.json`).

**Computed before this file was committed, and disclosed rather than presented later as a result:**
the *coverage* arithmetic in §5 — how many corpus events can carry a T2 value at all. It is a fact
about the inputs, it sizes the work, and knowing it could not bias an estimate because this
registration computes no estimate. **No exposure value, share or comparison was computed.**

## 1. The problem this must not repeat

G-3 established what a strict vintage rule does to this corpus: of 786 coded situation values, 726
vanished at *t*, and the remedy was per-field dated sources rather than code. The failure mode there
was that the date was **documentary** — carried beside the value, and therefore droppable by anyone
in a hurry. §3 of the physical-exposure registration says "every exposure value carries its
register's publication date". This registration makes that **structural**, on Joe's instruction:

> *"If a capacity or flow value can be read without its publication date, the schema is wrong."*

## 2. The stamped value, and the only way to read one

**A register entry is an object, never a number.** Fixed shape:

```
{ "value": float|None, "unit": str, "published": "YYYY-MM-DD", "reference_period": str,
  "source_id": str, "source_url": str, "retrieved_at": str, "quote": str }
```

`published` is the **release's publication date, never its reference year** (§3's trap, and
`WORLD_STATE_CODEBOOK.md` Amendment 1's `vintage`). `quote` is the verbatim sentence the number was
read from; a value with no quote may not enter the register.

**The reader API takes `t` and refuses to certify what it cannot.** There is no function anywhere in
`src/g_vintage.py` that returns a bare number from a stamped object without a date argument:

- `latest(register, key, t)` → the stamped entry with the greatest `published ≤ t`, or `None`.
  **Never** the newest entry, and never one published after `t`.
- `value_at(stamped, t)` → the float, and **raises `VintageError` if `published > t`**.
- There is deliberately **no** `.value` accessor, no `float(stamped)`, and no default `t`.

**Enforced by a test, not by care** (the pattern of Amendment 5 in `G4_REGISTRATION.md`, where the
nominal count stopped existing as a scalar): a test parses `src/g_vintage.py` and asserts that every
public function returning a value from a stamped object has a required, non-defaulted date parameter.
A future edit that adds a convenience accessor fails the suite.

## 3. The filtration assertion, in Amendment F.1's standing

Joe: *"a test that VOIDS the study on a single violation, in Amendment F.1's standing."*

`filtration_audit(rows)` runs over **every emitted exposure row**, on an independent path from the
code that built them (raw dates, never the functions being audited), and asserts for each:

1. every stamped term the row rests on has `published ≤ event_date`;
2. no row carries a term whose `published` is absent or unparseable;
3. no row was built from a register entry with `value: None` treated as `0`.

**A single violation sets `asserted: false` and voids the study**, exactly as F.1 voids a walk. The
count and the first violation are published either way. The audit is written so it can fail: a
companion test injects a deliberately post-dated term and asserts the audit catches it — an
enforcement nobody has seen fail is not an enforcement.

## 4. The register — four EIA releases, retrieved this session, quoted verbatim

Every figure below was fetched in this session's own fetch log; nothing is recalled. Where a release
does not give a chokepoint, the entry is **absent — not zero, not carried forward from another
release**.

| release | published | ref. period | chokepoints quantified |
|---|---|---|---|
| EIA *Today in Energy* #330, "Maritime chokepoints critical to petroleum markets" | **2011-03-02** | 2009 | Hormuz 15.5 · Malacca 13.6 · Suez 1.8 · SUMED 1.1 · Bab el-Mandeb 3.2 · Bosporus 2.9 · Panama 0.8 · Danish Straits 3.3 |
| EIA *TIE* #18991, "World oil transit chokepoints critical to global energy security" | **2014-12-01** | 2013 | Hormuz 17 · Malacca 15.2 · **world seaborne 56.5** |
| EIA *TIE* #32352, "Three important oil trade chokepoints are located around the Arabian Peninsula" | **2017-08-04** | 2016 (world 2015) | Hormuz 18.5 · Suez 3.9 · SUMED 1.6 · Bab el-Mandeb 4.8 · **world maritime 59** (2015) |
| EIA *TIE* #65504, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint" | **2025-06-16** | 2024 | Hormuz 20 |

**Cape of Good Hope is quantified by none of them.** It is registered as a **gap**, in every release,
and is `None` — never zero. Four of the seven chokepoints Joe named (Malacca, Turkish Straits, Panama,
Cape) are additionally named by **zero corpus events** (§5), so their register entries exist for
future use and contribute nothing to this study today.

### 4.1 The denominator, and the rule that stops it being invented

T2 is `FLOW(k, vintage(t)) / WORLD_SEABORNE(vintage(t))`. Only two of the four releases state a world
figure, and **they state different quantities**: 56.5 mb/d "of the world's oil production in 2013
moved on maritime routes" (2014 release) and "nearly 59 million b/d of global petroleum and other
liquids production moved on maritime routes in 2015" (2017 release). Registered, before any share is
computed:

- the denominator must come from a release with `published ≤ t`; the **same** release as the numerator
  where that release states one, otherwise the latest world figure published ≤ t;
- a denominator is **never** back-derived from a rounded share (the 2011 release says Hormuz was
  "roughly a third of all seaborne traded oil" — dividing 15.5 by 0.333 would manufacture a figure to
  three significant digits out of one, and is forbidden);
- where no world figure is published ≤ t, **T2 is null, not imputed**, and the event is counted in the
  exclusion table. The numerator in kb/d is still published, stamped, because it is knowable.

## 5. Coverage, computed before this was written and disclosed here

- The corpus is **313 events, 1973-10-06 → 2026-06-17**. The first EIA chokepoint release is
  **2011-03-02**, so **82 events (26.2 %) predate any release** and can carry no T2 term under §3's
  rule at all.
- **37 events name a chokepoint entity.** Of those, **6 name entities EIA does not quantify**
  (`libya_es_sider` ×2, `kirkuk_ceyhan_pipeline`, `gibraltar_strait`, `druzhba_pipeline`,
  `cpc_novorossiysk`, `taiwan_strait`) and **5 predate the first release**.
- **T2 is constructible for 25 events**, all 2011–2026, and they are Hormuz, Bab el-Mandeb and Suez
  only.

Registered as a consequence, before any estimate: **T2 is a 25-event variable in a 313-event corpus.**
Whatever it shows, it cannot carry a corpus-wide claim, and §5 of the physical-exposure registration's
verdict words must be read against that n. This is reported to Cowork as a **design fact**, not as a
result, and it is the main thing G was able to establish before writing code.

## 6. The PortWatch cross-check, with its limits stated first

PortWatch daily tanker series for all seven chokepoints are already in the tree (2019-01-01 →),
`data/seed/ripple/portwatch.<slug>.capacity_tanker.csv`. The cross-check is **shares, never levels**:
PortWatch measures transiting tanker capacity (AIS-derived), EIA measures barrels of oil; they are
different quantities and no conversion is asserted. Registered:

- for each event with `t ≥ 2019-01-01`, the chokepoint's share of the seven-chokepoint PortWatch total
  over the 90 days **strictly before** *t*, beside the EIA share;
- published as a **rank agreement** (Spearman across the chokepoints) and a per-chokepoint ratio, as a
  **diagnostic that gates nothing**;
- PortWatch's own publication lag (~1 week, `data/portwatch.json`) is applied: observations dated
  within 7 days of *t* are excluded, so the cross-check obeys the same filtration as the register.
- **Cape of Good Hope is a route, not a strait**, and a transit count there is not comparable to a
  chokepoint flow; it is reported and excluded from the rank statistic, and that exclusion is
  registered here rather than decided when the number is seen.

## 7. Outputs

`docs/g/CHOKEPOINT_REGISTER.json` (the register, every entry stamped), `docs/g/CHOKEPOINT_T2.json`
and `.md` (per-event T2 with its terms, the exclusion table, the filtration audit, the PortWatch
cross-check), `src/g_vintage.py`, `src/g_chokepoint_register.py`, `tests/test_g_vintage.py`,
`tests/test_g_chokepoint_register.py`, and a handoff to Cowork.

## 8. What this registration does not do

It computes no local projection, fits nothing, and makes no claim about whether exposure carries
information — §§4–5 of the physical-exposure registration are Cowork's and untouched. It does not
write to `events`, `observations` or any other table. It does not edit
`PHYSICAL_EXPOSURE_REGISTRATION.md`. It does not build T1 or T3.
