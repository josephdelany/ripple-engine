# Full system audit — index

*2026-09-03. Independent adversarial audit of the Ripple Engine. Scope: 54,667 lines of source
across `src/`, the walk-forward core, retrieval, scoring, inference, baseline construction, corpus
admission, the outcome mapping, local projections, the 915-function test suite, and every published
data artefact. All line references are to committed code; all counts were recomputed from the
database and the published JSON rather than taken from prose.*

---

## The one-paragraph verdict

**The engineering is sound and the targets are mis-specified.** The scoring rules, the inference
machinery, the local projections and the test suite are correct — several are better than what is
typically found in published applied work. But **both of the project's two outcome variables measure
something other than what the paper says they measure**, and the retrieval design constrains what
the central null can mean far more narrowly than the abstract claims. That is a much better problem
to have than the reverse: target definitions are fixable, rotten infrastructure is not.

---

## The documents

| file | contents |
|---|---|
| `01_TIER1_design_defects.md` | **A1–A3.** Three defects that determine the headline results independently of anything about historical analogy. Read this first. |
| `02_TIER2_claims_and_implementation.md` | **B1–B6.** Published claims that do not survive scrutiny, plus implementation issues that weaken the inference. |
| `03_TIER3_structural.md` | **C1–C7.** Structural limits on interpretation. Not defects; boundaries. |
| `04_verified_sound.md` | What was checked and found correct. Not consolation — several of these are genuine strengths and should be claimed. |
| `05_remediation_plan.md` | Ordered, costed plan. Two items are the whole job. |
| `06_exact_restatements.md` | Drop-in replacement text for every claim that must change. |

---

## Severity summary

| tier | count | meaning |
|---|---|---|
| **Tier 1** | 3 | The result follows from the design, not from the phenomenon. Must be restated or re-run. |
| **Tier 2** | 6 | Published claims that fail, or implementation choices that weaken inference. |
| **Tier 3** | 7 | Boundaries on what the evidence can support. Disclose, do not fix. |
| **Sound** | 8 | Verified correct. Claim these. |

**Total remediation to a defensible state: ~9 hours, of which 3 are the author's label audit.**
