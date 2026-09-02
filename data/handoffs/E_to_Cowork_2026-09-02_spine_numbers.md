# Handoff E → Cowork, 2026-09-02: exact spine numbers for §3 of the paper and the README

`docs/PAPER_DRAFT.md` §3 is the most honest section in the paper and it is right on every
figure I could check. Session E has now measured the same layer mechanically
(`src/spine_audit.py`, published at `data/spine/AUDIT.md`, re-runnable), so the places where
§3 says "a substantial share" can carry a number instead. Everything below is computed from
`data/oil.db`, not from prose.

## What §3 already gets right (independently reproduced)

| §3 claim | audit |
|---|---|
| 313 events | 313 |
| "0 of 313 record two independent sources" | 0 of 313 have ≥ 2 distinct source domains, counting `www.`-stripped domains across `source_url` **and** every URL inside `sr_json.sources` — i.e. the generous reading, and it is still zero |
| "median length of 148 characters" | 148 |
| "8 events in the 1970s, 11 in the 1980s, 16 in the 1990s, 43 in the 2000s, 85 in the 2010s, 150 in the 2020s" | exactly those six figures |

## What can now replace the qualitative phrases

§3 currently says field provenance is "recorded in `sr_json` under a sourced-or-unknown rule,
but a substantial share of those field sources are null or self-referential
(`corpus:density`, `corpus:observed`)". The share, over 3,443 field-source slots:

| provenance of an `sr_json` field source | share |
|---|---|
| external URL | 11.9 % |
| corpus-derived (`corpus:…`) | 25.0 % |
| null | 63.1 % |

Suggested wording: *"Of the field-source slots recorded in `sr_json`, 11.9 % carry an
external URL, 25.0 % are corpus-derived and therefore cannot corroborate the corpus, and
63.1 % are null."*

## Three facts §3 does not yet state, all of which strengthen it

1. **49 of 313 records (15.7 %) still carry drafting scaffolding in the description** — 17
   reading "[deep-history tier 1970-1989; events-only]" and 32 reading "DRAFT coding". By
   decade: 1970s 8, 1980s 10, 1990s 6, 2000s 4, 2010s 11, 2020s 10. §3 says "some carry draft
   coding notes in the text"; the number is 49.
2. **9 events cite a bare site root rather than a document** — all `https://www.eia.gov`.
   They satisfy "every event MUST be sourced" while citing nothing a reader can open. The
   cause is traced: the deep-history seed's `_meta` names the "EIA energy chronology" as an
   anchor source, and that page no longer exists (checked 2026-09-02; the surviving weekly
   petroleum page carries no timeline). This is worth a clause because it is a concrete
   instance of the provenance problem §3 describes in general terms.
3. **No description in the corpus reaches 700 characters** — roughly a 120-word narrative.
   §3's "a sentence, not a case narrative" is exactly right, and 0 of 313 is the number.

## One number in §3 that needs a footnote, not a correction

§3 is about the corpus, but if the paper anywhere reports IES-90 coverage: 184 events carry
an independent IES-90 level, 3 are flagged `no_independent_outcome`, and **126 are
uncovered**. The 126 are not a gap in the labelling — they are exactly the three
non-geopolitical classes, which have no ICB/MID/UCDP record by construction:
`policy_response` 57, `opec_decision` 52, `demand_shock` 17. Stating that prevents a reader
taking 126/313 as a coverage failure.

## What is changing, and what the paper should say until it lands

Session E is rewriting records to `SPINE_REGISTRATION.md`: two independent source domains
with at least one primary, a 120–250 word narrative citing each claim, `knowable_at` with its
reason, and an explicit "what was not known at the time". The pre-1990 tier is in progress.
Nothing has entered `events` — every change is a proposal under `data/spine/patches/` for
Joe to admit — so **no number in the paper changes yet**.

§3's closing sentence ("Repair is registered and under way … Until that lands, every result
in this paper should be read as conditional on a corpus whose historical arm is thin") stays
true and should stay. When a batch is admitted I will send the re-run audit numbers, and the
sentence can name what actually improved, measured the same way.

## Two things the paper should probably not claim

- The `data/candidates/REGISTRATION.md` repair §3 cites produces **candidate dossiers for
  pre-1987 admission**; it does not repair the 313 records already in the corpus. Those are
  two different repairs and §3 currently reads as though the one covers the other.
- If any draft says the corpus follows a two-source rule, it should say the rule governs
  future admissions and is not yet a property of any existing record. The audit is the
  citation for that.

## Added 2026-09-02, after the pre-1990 pass: the encyclopaedia finding

`src/spine_audit.py` now counts encyclopaedia domains separately. **31 of 313 events
(9.9%) cite Wikipedia as their `source_url`, and all 31 have no other citable domain**;
32 `sr_json` field-source slots cite it too. By decade: 1990s 4, 2000s 11, 2010s 5,
2020s 11 — most of them OPEC decisions sourced to Wikipedia's "<year> world oil market
chronology" pages.

The codebook's inclusion criterion 2 requires "a primary or major-wire source exists. No
source = not in the dataset." By the corpus's own rule these 31 records are not sourced.
§3 currently describes provenance weakness in terms of *single* sources and null field
provenance; this is a stronger and simpler statement, and it is measured:

> *"Thirty-one of the 313 records cite an encyclopaedia as their only source, which the
> codebook's own inclusion rule does not admit."*

This is the number I would put in §3 if only one new figure can be added, because it is
the one a reviewer will find on their own.

## What the pre-1990 pass produced, for §3's "repair is under way" sentence

Nineteen dossiers, all nineteen pre-1990 records, at `data/dossiers/<event_id>.md`; 17 of
19 pass the mechanical check in `src/spine_check.py`, 2 are honest partials, none claims
more than it shows. Primary documents newly cited include FRUS minutes of the Washington
Special Actions Group meetings of 17 and 19 October 1973 and the CIA Office of Economic
Research memorandum of 19 October 1973, a Kissinger memorandum of 19 March 1974,
Brzezinski's memorandum of 4 November 1979 written the day the Tehran embassy was seized,
Carter's State of the Union of 23 January 1980, Executive Order 12170, Reagan's report to
Congress on Operation Praying Mantis, and the UN's UNIIMOG mission history.

**No corpus number has changed.** The patches are proposals in `data/spine/patches/`
awaiting Joe, so the audit still reads 313 events and 0 with two source domains. The
paper's §3 figures are all still correct as printed, and should not be updated yet.

Two findings the paper may want regardless, because they are about the record rather than
the repair: the 1980s tier cannot be primary-sourced because FRUS 1981–1988 Volumes XX and
XXI (Iran, Iraq) and FRUS 1969–76 Volume X (Iran 1977–79) are unpublished and still "Being
Cleared" — the declassification queue, not our effort, is the binding constraint on that
decade. And one record, `iran_air_655_1988`, meets the sourcing standard while failing the
codebook's inclusion criterion 3, since no supply, transit or refining mechanism can be
stated for it.

— Session E
