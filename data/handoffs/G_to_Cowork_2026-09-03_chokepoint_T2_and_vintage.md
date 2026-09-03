# G → Cowork, 2026-09-03 — T2 is a 25-event variable, and the vintage stamp is now structural

Joe assigned G two parts of `PHYSICAL_EXPOSURE_REGISTRATION.md` (66b1c30): **§2 T2**, the chokepoint
flow register, and **§3**, the vintage discipline for the whole study. Registered first in
`docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md`; built by `src/g_vintage.py` and
`src/g_chokepoint_register.py`; published at `docs/g/CHOKEPOINT_REGISTER.json` and
`docs/g/CHOKEPOINT_T2.{json,md}`. **G did not edit your registration and did not build T1 or T3.**

## 1. The number you need before §5's verdict words are applied

**T2 is constructible for 25 of 313 corpus events**, and it is Hormuz, Bab el-Mandeb and Suez only.

| | events |
|---|---|
| corpus | 313 (1973-10-06 … 2026-06-17) |
| predate the first EIA chokepoint release (**2011-03-02**) — no T2 term possible at all | **82 (26.2 %)** |
| name any chokepoint entity | 37 |
| …name an entity EIA quantifies nowhere (`libya_es_sider` ×2, `kirkuk_ceyhan_pipeline`, `gibraltar_strait`, `druzhba_pipeline`, `cpc_novorossiysk`, `taiwan_strait`) | 7 |
| …predate the first release | 5 |
| **T2 constructible** | **25** |

Of the 30 event-chokepoint rows, **23 carry a share**. And **four of the seven chokepoints you and
Joe named — Malacca, Turkish Straits, Panama, Cape of Good Hope — are named by *zero* corpus
events.** Their register entries exist for future use and contribute nothing to this study.

**This is a design fact, established before any estimate, not a result.** Whatever T2 shows it
cannot carry a corpus-wide claim, and §5's verdict words should be read against n = 25. G's
recommendation, which is yours to take or leave: **T3 is where the study lives**; T2 is a
supporting variable on a Red Sea / Hormuz subsample and should be described as one from the start
rather than after the estimate comes in thin.

## 2. Where the vintage rule bites, and it is not where you would guess

Two cases worth seeing, because they are the rule working rather than a defect:

- **`egypt_revolution_2011` (2011-01-25) is null by five weeks.** The first EIA chokepoint release
  is 2011-03-02. An analysis that used "the 2011 EIA figures" for a January 2011 event would look
  entirely reasonable and would be using a register that did not exist yet.
- **`hormuz_iran_threat_2011` and `egypt_coup_suez_2013` have a flow and no denominator.** The 2011
  release states no world-seaborne total; the first one that does is 2014-12-01 (56.5 mb/d). Under
  §4.1 T2 is **null, not imputed** — and specifically the 2011 release's "roughly a third of all
  seaborne traded oil" is **not** used to back-derive a denominator, because dividing 15.5 by 0.333
  manufactures three significant digits out of one. The numerator is still published, stamped.

## 3. The register — four releases, each figure with the sentence it was read from

All retrieved in this session's own fetch log from eia.gov; nothing recalled.

| published | ref | quantifies |
|---|---|---|
| **2011-03-02** — TIE #330 | 2009 | Hormuz 15.5 · Malacca 13.6 · Suez 1.8 · SUMED 1.1 · Bab el-Mandeb 3.2 · Turkish Straits 2.9 · Panama 0.8 · Danish Straits 3.3 |
| **2014-12-01** — TIE #18991 | 2013 | Hormuz 17 · Malacca 15.2 · **world seaborne 56.5** |
| **2017-08-04** — TIE #32352 | 2016 | Hormuz 18.5 · Suez 3.9 · SUMED 1.6 · Bab el-Mandeb 4.8 · **world maritime 59** (2015) |
| **2025-06-16** — TIE #65504 | 2024 | Hormuz 20 |

**Cape of Good Hope is quantified by none of them** and is registered as a **gap — `None`, never
`0.0`** — in every release. A chokepoint a release omits is *absent from that release*, never
carried forward as if it had been restated: `latest()` will read a 2014 figure at a 2020 date, but
the value it hands back is stamped **2014-12-01**, and the audit checks that date, not the read date.

Two denominators exist and **they are different quantities**: 56.5 mb/d "of the world's oil
production in 2013 moved on maritime routes" and "nearly 59 million b/d of global petroleum and
other liquids production" in 2015. G used each release's own where present and did not reconcile
them; if you need one series, that is a decision for you and it needs its own registration.

## 4. §3 made structural, which is the part that generalises beyond T2

Joe's instruction was that if a value can be read without its publication date, the schema is wrong.
`src/g_vintage.py` implements that, and it is meant for **T1 and T3 as well as T2**:

- a register entry is an **object, never a number**: `{value, unit, published, reference_period,
  source_id, source_url, retrieved_at, quote}`, and an entry with no verbatim quote cannot be built;
- **`published` is the release date, never the reference year** — your §3's trap, checked by a test
  that asserts every entry's publication year is later than its reference year;
- **the only way to obtain a number is `value_at(stamped, t)`**, which raises `VintageError` when
  `published > t`. There is no `.value`, no `float()`, no default `t`. `latest(register, key, t)`
  returns the newest entry **on or before `t`** — never the newest;
- `register_summary()` deliberately returns provenance and **no values**, so it cannot be used to
  dodge the date;
- a test parses the module and asserts every value-returning function has a **required,
  non-defaulted** date parameter. A future convenience accessor fails the suite rather than
  quietly reintroducing an undated read.

**Please build T1 and T3 on this module rather than beside it.** T1's capacity registers are exactly
where §3's trap bites hardest — the EI Statistical Review's reference year and publication date are
a year apart — and the module makes that impossible to get wrong by omission.

## 5. The filtration assertion, in Amendment F.1's standing, as Joe asked

`filtration_audit(rows)` runs over every emitted row on an **independent path** — raw dates only; a
test asserts it never calls `value_at` or `latest` — and checks that every stamped term has
`published ≤ event_date`, that no term has an absent or unparseable date, and that no null term was
treated as zero. **A single violation sets `asserted: false` and `voided: true`.**

On the published build: **48 terms over 30 rows, 0 violations, `asserted: true`.**

It is written so it can fail, and that is tested rather than asserted: companion tests inject a
term published eight years after its event, an unstamped bare float, a row with an unparseable date,
and a null term flagged as zeroed — and each must be caught. An enforcement nobody has seen fail is
not an enforcement.

## 6. The PortWatch cross-check (§6) — shares, never levels; gates nothing

PortWatch tanker-capacity series for all seven chokepoints are in the tree from 2019-01-01. For each
event date from 2019, G computes each chokepoint's share of the seven-chokepoint total over the 90
days **strictly before** `t`, with PortWatch's own ~1-week tail lag applied so the cross-check obeys
the same filtration as the register.

**Rank agreement is strong: Spearman +0.943 across 2019–2024, easing to +0.886 from mid-2024** (the
Red Sea diversion period, which is what you would expect to move it). Six chokepoints enter the
statistic; **Cape of Good Hope is excluded by registration, not by choice after seeing the number** —
it is a route, not a strait, and a transit count there is not comparable to a chokepoint flow.

Stated limit: PortWatch measures transiting tanker capacity from AIS, EIA measures barrels of oil.
**Shares only. No conversion is asserted**, and the agreement is evidence that the register's
*ordering* is right, not that its levels are.

## 7. What G did not do

No local projection, no fit, no claim about whether exposure carries information — §§4–5 are yours.
No writes to `events`, `observations` or any table. T1 and T3 untouched. And G has **not** reconciled
the two world-seaborne definitions, because choosing between them is a registered decision and it is
not G's to make.
