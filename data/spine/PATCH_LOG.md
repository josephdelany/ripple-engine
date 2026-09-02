# Patch log — the spine

*Append-only. One entry per patch batch. A batch is **proposed** when
`src/spine_patch.py` writes it and **applied** only when Joe runs the admit line himself;
this file records both, so that the history of the corpus is readable without diffing the
database. Session E never applies a patch (charter §2 rule 3).*

Columns in each batch table: the events it covers, how many field changes it proposes, how
many of those could not be reduced to a clean value and are flagged `needs_joe`, and the
dossier status behind it.

---

## Proposed, awaiting Joe

### `pre1990_a` — ten records, 1973–1980

Built 2026-09-02 from `data/dossiers/`. **30 proposed field changes, 1 `needs_joe`, 20
fields the dossiers deliberately leave unchanged.**

Events: `yom_kippur_war_1973`, `oapec_embargo_1973`, `embargo_lifted_1974`,
`abqaiq_arabian_1977`, `iran_oilworkers_strike_1978`, `shah_leaves_iran_1979`,
`iran_revolution_1979`, `iran_hostage_crisis_1979`, `carter_doctrine_1980`,
`iran_iraq_war_1980`.

The changes worth reading before applying:
- six `source_url` upgrades from a bare `eia.gov` root or a working paper to a primary
  document (FRUS, the American Presidency Project, the Federal Register);
- `iran_oilworkers_strike_1978` and `iran_revolution_1979` drop from `day` to `month`
  precision, because no retrieved source pins the day;
- `abqaiq_arabian_1977` proposes **nothing at all**: eleven retrieval routes returned no
  source, so every field on it rests on nothing and the honest state of each is `unknown`.

### `pre1990_b` — nine records, 1984–1988

Built 2026-09-02. **20 proposed field changes, 7 `needs_joe`, 13 left unchanged.**

Events: `tanker_war_1984`, `kharg_strikes_1985`, `opec_price_collapse_1986`,
`iraq_kharg_1986`, `earnest_will_1987`, `bridgeton_mine_strike_1987`,
`praying_mantis_1988`, `iran_air_655_1988`, `iran_iraq_ceasefire_1988`.

- `iran_iraq_ceasefire_1988` moves from **1988-08-20 to 1988-08-08**, the date the UN
  records the ceasefire being announced, per the codebook's rule that an event is dated to
  the first day the market could have known.
- `opec_price_collapse_1986` loses `day` precision. Two defensible anchors were found and
  neither could be adjudicated; both fall in 1985.
- `praying_mantis_1988` gets a working `source_url`; the one in the database no longer
  serves the article it cites.
- The seven `needs_joe` rows are mostly assessments of existing severity and surprise codes
  ("keep", "borderline 2–3"), which are judgements rather than values.

### `1990s_a` — seven records, 1990–1996

Built 2026-09-02. **10 proposed field changes, 3 `needs_joe`, 33 left unchanged.**

Events: `iraq_invades_kuwait_1990`, `iraq_un_661_embargo_1990`,
`desert_storm_air_campaign_1991`, `kuwait_oil_fires_1991`, `iraq_un_986_ofp_1995`,
`ilsa_sanctions_1996`, `iraq_ofp_exports_begin_1996`.

- `kuwait_oil_fires_1991` replaces a **Wikipedia** citation with the Public Papers of the
  Presidents via `govinfo.gov`. Its `confidence` drops from `high` to `medium`, because only
  one contemporaneous source could be retrieved.
- `iraq_invades_kuwait_1990` and `iraq_un_986_ofp_1995` replace `digitallibrary.un.org`
  citations, which return 403 today, with a presidential document and a Treasury document.
- `ilsa_sanctions_1996` proposes `surprise` 2 → 1, on the codebook's own rule that a
  scheduled, consensus-expected action is 1.
- A date tension is **flagged and not proposed** on `kuwait_oil_fires_1991`: a Defense
  Department report dates the start of well destruction to 1991-01-16, seven days before
  the 1991-02-22 date the only contemporaneous source confirms publicly. No retrieved source
  establishes an earlier *public* date, so the dossier declines to move it.

---

## Applied

*(nothing yet — no patch has been applied; the `events` table is unchanged by Session E)*

When Joe applies a batch, append a row here recording: the batch, the date, who approved it,
which rows were applied and which were declined, and the `src/spine_audit.py` numbers before
and after. The audit is the scoreboard; a patch that does not move it did not do anything.
