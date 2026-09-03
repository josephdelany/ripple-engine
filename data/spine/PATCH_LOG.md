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

- `iran_iraq_ceasefire_1988` **keeps 1988-08-20**. This line previously said the record
  moved to 1988-08-08 and that was wrong: it was written against an earlier build of the
  patch, before `src/spine_patch.py` was hardened. The dossier's cell reads "not changed
  here, but flagged: 1988-08-08 ... is arguably the codebook-correct first day the market
  could have known", which the hardened parser correctly reads as a no-change. The date
  question is real and stays with Joe; the record's `source_url` did move, to the UN's
  UNIIMOG mission history.
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

### `1990s_b` — nine records, 1995–1999

Built 2026-09-02. **19 proposed field changes, 2 `needs_joe`, 33 left unchanged.**

Events: `iran_eo12959_embargo_1995`, `thai_baht_float_1997`, `korea_imf_bailout_1997`,
`opec_jakarta_quota_increase_1997`, `opec_cut_march_1998`, `opec_cut_june_1998`,
`russia_default_ltcm_1998`, `operation_desert_fox_1998`, `opec_cut_1999`.

- Two more **encyclopaedia citations replaced**: `opec_cut_march_1998` moves to an Oxford
  University research-archive item and `russia_default_ltcm_1998` to the BIS Quarterly
  Review of November 1998. With `kuwait_oil_fires_1991` in `1990s_a`, three of the four
  pre-2000 encyclopaedia-only records are now sourced to a real document.
- **`opec_cut_june_1998` could not be replaced.** The dossier records every route tried and
  the row is flagged `needs_joe` rather than proposing a value. This is Amendment 2 of the
  registration meeting a specific record: OPEC decisions are not sourceable by free routes.
- **A date is challenged and not changed.** `korea_imf_bailout_1997` is dated 1997-11-21,
  and the contemporaneous BIS account places Korea's formal turn to the IMF in December. No
  retrieved source confirms 21 November, so the dossier flags the conflict, drops
  `confidence` from `high` to `medium`, and leaves the date for Joe.
- `thai_baht_float_1997` proposes `surprise` 4 → 2, because the BIS review describes weeks
  of visible pressure before the float; the source the record previously cited turns out to
  be a retrospective written about twenty-five years later, not a contemporaneous document.

---

## Applied

*The first batch was applied on 2026-09-02. Entries are appended below by
`src/spine_apply.py`; the prose note for that batch is here.*

**Note on `pre1990_a`, applied 2026-09-02.** Before applying, the month-precision question
was answered from the code rather than assumed: `date_precision` appears zero times in
`src/walk.py` and `src/engine/`, and `Corpus.tier_of` keys on the date alone against the
first day of the daily price series (1987-05-20), so all ten records were already monthly
tier and the two precision changes moved no tier, no analog pool and no score. No
`event_date` row existed in the batch at all — only the precision label changed.
`descriptions ≥ 700 chars` stayed at 0, which is correct: the narratives live in the
dossiers and the patch writes a one-paragraph summary into `events.description`.

When Joe applies a batch, append a row here recording: the batch, the date, who approved it,
which rows were applied and which were declined, and the `src/spine_audit.py` numbers before
and after. The audit is the scoreboard; a patch that does not move it did not do anything.

### APPLIED `pre1990_a` — 2026-09-02T23:43:46+00:00, approved by joe

29 field changes across 9 events; 1 rows skipped. Backup: `data/backups/oil_20260902_234317_pre_spine_apply.db.gz`.

| field change | from | to |
|---|---|---|
| `yom_kippur_war_1973`.description | Yom Kippur War begins (Egypt/Syria vs Israel) [deep-history  | Egypt and Syria attacked Israel on October 6, 1973, opening fronts across the Su |
| `yom_kippur_war_1973`.source_url | https://www.nber.org/papers/w16790 | https://history.state.gov/historicaldocuments/frus1969-76v25/d121 |
| `yom_kippur_war_1973`.severity | None | 3 |
| `yom_kippur_war_1973`.surprise | None | 5 |
| `oapec_embargo_1973`.description | OAPEC oil embargo on states backing Israel [deep-history tie | Arab OPEC members announced a production cut of at least 5%/month tied to Israel |
| `oapec_embargo_1973`.source_url | https://www.nber.org/papers/w16790 | https://history.state.gov/historicaldocuments/frus1969-76v36/d223 |
| `oapec_embargo_1973`.severity | None | 5 |
| `oapec_embargo_1973`.surprise | None | 3 |
| `oapec_embargo_1973`.confidence | medium | high |
| `embargo_lifted_1974`.description | Arab oil embargo lifted [deep-history tier 1970-1989; events | Arab oil ministers announced March 18, 1974 that they would lift the embargo on  |
| `embargo_lifted_1974`.source_url | https://www.eia.gov | https://history.state.gov/historicaldocuments/frus1969-76v36/d342 |
| `embargo_lifted_1974`.surprise | None | 2 |
| `iran_oilworkers_strike_1978`.date_precision | day | month |
| `iran_oilworkers_strike_1978`.source_url | https://www.nber.org/papers/w16790 | https://history.state.gov/historicaldocuments/frus1969-76v37/d168 |
| `iran_oilworkers_strike_1978`.severity | None | 4 |
| `shah_leaves_iran_1979`.source_url | https://www.nber.org/papers/w16790 | https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-979 |
| `shah_leaves_iran_1979`.confidence | medium | high |
| `iran_revolution_1979`.date_precision | day | month |
| `iran_revolution_1979`.source_url | https://www.nber.org/papers/w16790 | https://history.state.gov/historicaldocuments/frus1969-76v37/d189 |
| `iran_revolution_1979`.confidence | medium | low |
| `iran_hostage_crisis_1979`.source_url | https://www.eia.gov | https://history.state.gov/historicaldocuments/frus1977-80v11p1/d1 |
| `iran_hostage_crisis_1979`.confidence | medium | high |
| `carter_doctrine_1980`.source_url | https://www.eia.gov | https://www.presidency.ucsb.edu/documents/the-state-the-union-address-delivered- |
| `carter_doctrine_1980`.description | Carter Doctrine: US will use force to defend Gulf oil [deep- | In his January 23, 1980 State of the Union address, President Carter declared th |
| `carter_doctrine_1980`.severity | None | 1 |
| `carter_doctrine_1980`.surprise | None | 2 |
| `iran_iraq_war_1980`.source_url | https://www.nber.org/papers/w16790 | https://history.state.gov/historicaldocuments/frus1977-80v18/d93 |
| `iran_iraq_war_1980`.description | Iran-Iraq War begins [deep-history tier 1970-1989; events-on | On September 22, 1980, Iraq launched ground and air attacks on Iranian territory |
| `iran_iraq_war_1980`.severity | None | 5 |

Skipped:

- `iran_oilworkers_strike_1978`.type — needs_joe: the builder could not reduce it to a clean value

Scoreboard before → after:

| measure | before | after |
|---|---|---|
| events with ≥2 source domains | 0 | 9 |
| encyclopaedia-only source_url | 31 | 31 |
| bare site-root source_url | 9 | 6 |
| drafting scaffolding | 49 | 44 |
| descriptions ≥700 chars | 0 | 0 |

### APPLIED `pre1990_b` — 2026-09-02T23:59:04+00:00, approved by joe

13 field changes across 8 events; 7 rows skipped. Backup: `data/backups/oil_20260902_235832_pre_spine_apply.db.gz`.

| field change | from | to |
|---|---|---|
| `tanker_war_1984`.severity | None | 2 |
| `tanker_war_1984`.surprise | None | 2 |
| `kharg_strikes_1985`.description | Iraq intensifies air strikes on Iran's Kharg Island oil term | Iraq opened a new, more serious phase of air raids on Kharg Island's export term |
| `kharg_strikes_1985`.severity | None | 3 |
| `opec_price_collapse_1986`.description | Saudi abandons swing-producer role; 1986 price collapse [dee | Saudi Arabia abandoned its role as OPEC's swing producer after cutting its own o |
| `opec_price_collapse_1986`.severity | None | 5 |
| `iraq_kharg_1986`.description | Iraqi raids on Iran's Sirri Island oil terminal [deep-histor | On August 12, 1986, Iraqi aircraft struck Iran's Sirri Island oil export termina |
| `iraq_kharg_1986`.severity | None | 4 |
| `iraq_kharg_1986`.surprise | None | 4 |
| `earnest_will_1987`.source_url | https://www.eia.gov | https://www.upi.com/Archives/1987/07/22/The-three-US-Navy-warships-guarding-the- |
| `praying_mantis_1988`.source_url | https://www.asil.org/insights/volume/8/issue/25/world-court- | https://asil.org/insights/volume-8-issue-25-2/ |
| `iran_air_655_1988`.source_url | https://www.eia.gov | https://www.presidency.ucsb.edu/documents/statement-the-destruction-iranian-jetl |
| `iran_iraq_ceasefire_1988`.source_url | https://www.eia.gov | https://peacekeeping.un.org/sites/default/files/past/uniimogbackgr.html |

Skipped:

- `kharg_strikes_1985`.event_date — needs_joe: the builder could not reduce it to a clean value
- `kharg_strikes_1985`.date_precision — needs_joe: the builder could not reduce it to a clean value
- `opec_price_collapse_1986`.event_date — needs_joe: the builder could not reduce it to a clean value
- `opec_price_collapse_1986`.date_precision — needs_joe: the builder could not reduce it to a clean value
- `bridgeton_mine_strike_1987`.surprise — needs_joe: the builder could not reduce it to a clean value
- `praying_mantis_1988`.surprise — needs_joe: the builder could not reduce it to a clean value
- `iran_iraq_ceasefire_1988`.type — needs_joe: the builder could not reduce it to a clean value

Scoreboard before → after:

| measure | before | after |
|---|---|---|
| events with ≥2 source domains | 9 | 12 |
| encyclopaedia-only source_url | 31 | 31 |
| bare site-root source_url | 6 | 3 |
| drafting scaffolding | 44 | 41 |
| descriptions ≥700 chars | 0 | 0 |

### APPLIED `1990s_a` — 2026-09-03T00:01:26+00:00, approved by joe

7 field changes across 6 events; 3 rows skipped. Backup: `data/backups/oil_20260903_000028_pre_spine_apply.db.gz`.

| field change | from | to |
|---|---|---|
| `iraq_invades_kuwait_1990`.source_url | https://digitallibrary.un.org/record/94220 | https://www.presidency.ucsb.edu/documents/remarks-and-exchange-with-reporters-th |
| `iraq_un_661_embargo_1990`.source_url | https://unscr.com/en/resolutions/661/ | https://www.presidency.ucsb.edu/documents/executive-order-12724-blocking-iraqi-g |
| `kuwait_oil_fires_1991`.source_url | https://en.wikipedia.org/wiki/Kuwaiti_oil_fires | https://www.govinfo.gov/content/pkg/PPP-1991-book1/html/PPP-1991-book1-doc-pg165 |
| `kuwait_oil_fires_1991`.confidence | high | medium |
| `iraq_un_986_ofp_1995`.source_url | https://digitallibrary.un.org/record/176622 | https://ofac.treasury.gov/media/5406/download |
| `ilsa_sanctions_1996`.surprise | 2 | 1 |
| `iraq_ofp_exports_begin_1996`.source_url | https://www.un.org/depts/oip/background/oilexports.html | https://press.un.org/en/1997/19971204.sc6452.html |

Skipped:

- `iraq_invades_kuwait_1990`.surprise — needs_joe: the builder could not reduce it to a clean value
- `desert_storm_air_campaign_1991`.description — needs_joe: the builder could not reduce it to a clean value
- `ilsa_sanctions_1996`.description — needs_joe: the builder could not reduce it to a clean value

Scoreboard before → after:

| measure | before | after |
|---|---|---|
| events with ≥2 source domains | 12 | 17 |
| encyclopaedia-only source_url | 31 | 30 |
| bare site-root source_url | 3 | 3 |
| drafting scaffolding | 41 | 41 |
| descriptions ≥700 chars | 0 | 0 |

### APPLIED `1990s_b` — 2026-09-03T00:02:11+00:00, approved by joe

16 field changes across 8 events; 2 rows skipped. Backup: `data/backups/oil_20260903_000145_pre_spine_apply.db.gz`.

| field change | from | to |
|---|---|---|
| `iran_eo12959_embargo_1995`.description | Clinton's Executive Order 12959 imposed a total US trade and | Executive Order 12959 (May 6, 1995) imposed a total U.S. embargo on trade with a |
| `thai_baht_float_1997`.source_url | https://www.bot.or.th/en/our-roles/special-measures/Tom-Yum- | https://www.bis.org/publ/r_qt9711.pdf |
| `thai_baht_float_1997`.description | Bank of Thailand abandons the dollar peg; baht falls 15-20%  | On 2 July 1997 the Thai authorities abandoned the currency peg after 'a first ma |
| `thai_baht_float_1997`.surprise | 4 | 2 |
| `thai_baht_float_1997`.confidence | medium | high |
| `korea_imf_bailout_1997`.source_url | https://www.washingtonpost.com/archive/politics/1997/11/21/s | https://www.bis.org/publ/r_qt9802.pdf |
| `korea_imf_bailout_1997`.confidence | high | medium |
| `opec_jakarta_quota_increase_1997`.description | Conference of 26 Nov - 1 Dec 1997 lifts ceiling from 25 to 2 | OPEC's Conference of oil ministers, meeting in Jakarta 26 November – 1 December  |
| `opec_jakarta_quota_increase_1997`.source_url | https://www.oxfordenergy.org/wpcms/wp-content/uploads/2010/1 | https://ora.ox.ac.uk/objects/uuid:4e02651d-eab4-4af2-8f38-9bc41ae07f50/files/mab |
| `opec_cut_march_1998`.surprise | 3 | 2 |
| `opec_cut_march_1998`.description | OPEC's 104th extraordinary meeting cut output by 1.245 milli | OPEC met in Vienna on 30 March 1998 to formalize production cuts, following a se |
| `opec_cut_march_1998`.source_url | https://en.wikipedia.org/wiki/1998_world_oil_market_chronolo | https://ora.ox.ac.uk/objects/uuid:4e02651d-eab4-4af2-8f38-9bc41ae07f50/files/mab |
| `russia_default_ltcm_1998`.source_url | https://en.wikipedia.org/wiki/1998_Russian_financial_crisis | https://www.bis.org/publ/r_qt9811.pdf |
| `russia_default_ltcm_1998`.description | Russia defaulted on domestic debt and let the ruble collapse | On 17 August 1998, 'the Russian authorities' decision to float the rouble and de |
| `operation_desert_fox_1998`.description | Four days of US/UK airstrikes on Iraqi military and WMD targ | On December 16, 1998, Clinton ordered strikes whose 'mission is to attack Iraq's |
| `opec_cut_1999`.description | Vienna meeting ratifies the Hague framework (agreed ~10 days | OPEC's 11 member states voted in Vienna on 23 March 1999 to cut crude output by  |

Skipped:

- `opec_cut_june_1998`.source_url — needs_joe: the builder could not reduce it to a clean value
- `opec_cut_june_1998`.confidence — needs_joe: the builder could not reduce it to a clean value

Scoreboard before → after:

| measure | before | after |
|---|---|---|
| events with ≥2 source domains | 17 | 22 |
| encyclopaedia-only source_url | 30 | 28 |
| bare site-root source_url | 3 | 3 |
| drafting scaffolding | 41 | 39 |
| descriptions ≥700 chars | 0 | 1 |

