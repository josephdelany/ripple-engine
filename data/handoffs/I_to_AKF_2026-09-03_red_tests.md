# I → A, K, F — four red tests on `v2-day1`, none of them mine

*2026-09-03. Session I, reporting rather than patching: charter §1 says defects in
another session's tree are written here, never fixed in place.*

Full suite on the tree at `eab463f`: **4 failed, 771 passed, 13 skipped, 1 xfailed**
(773s). Session I's own two files (`tests/test_figures_paper.py`,
`tests/test_citation_guard.py`) are green, 21/21, and none of the four failures
references Session I code. I committed on top of this red tree because I cannot fix
any of it without editing your files.

| test | owner | what it asserts |
|---|---|---|
| `test_audit_ies90.py::test_a_non_hostile_row_tells_joe_the_target_would_not_score_it` | **K** | `assert 'non_hostile' in ''` — the regenerated audit sheet has an empty field where the note belongs |
| `test_audit_ies90.py::test_joes_answered_row_survives_the_regeneration` | **K** | `joe == joe and 0 == 1` — Joe's one answered row did **not** survive regeneration |
| `test_hostility.py::test_rows_match_the_database` | **F** | rows vs `data/oil.db` |
| `test_design_spec.py::test_the_story_has_six_bands_in_the_registered_order` | **A** | band 2 must be `Is it priced`; `src/app.html` no longer emits it |

The second one looks the most expensive to leave: an audit row Joe has already
answered being lost on regeneration is the kind of defect that silently costs the
label audit its progress, and Amendment 4.2 (`ba77988`) just changed how that sheet
is built. Worth a look before the re-run rather than after.

Nothing here is a request for Session I. Reported so it is not mistaken for
background noise in a suite that is otherwise green.

---

## Update, later on 2026-09-03 — two of the four are fixed, F's have changed shape

Re-run on the settled tree: **2 failed, 842 passed, 14 skipped, 1 xfailed** (371s).

K's two `test_audit_ies90.py` failures and A's `test_design_spec.py` band-order failure
are **gone** — thank you. What remains is F's, and it is not the same test as before:

| test | was | now |
|---|---|---|
| `test_hostility.py::test_rows_match_the_database` | failing | passing |
| `test_hostility.py::test_section_6_impact_recomputes_from_the_sealed_scores` | — | **failing** |
| `test_hostility.py::test_section_6_set_matches_the_published_summary` | — | **failing** |

Both new ones are §6-of-the-hostility-audit against the sealed scores and the published
summary, so they look like the same underlying disagreement seen from two directions.
Still not Session I's to fix; still reported rather than patched.
