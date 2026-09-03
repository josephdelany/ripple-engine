# Iraq nationalises the Iraq Petroleum Company     iraq_ipc_nationalisation_1972 · 1972-06-01 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 124) | "Intelligence Note Prepared in the Bureau of Intelligence and Research (RECN–15)" | Washington, June 27, 1972 | https://history.state.gov/historicaldocuments/frus1969-76v36/d124 | 2026-09-03T02:2xZ (session) | "Iraq's nationalization of the Iraq Petroleum Company (IPC) on June 1"; "Two sobering realizations have been brought home by the Iraqi expropriation of IPC. Coming on the heels of Libya's expropriation of BP's holdings in that country and Algeria's seizure last year of majority interest in French companies operating there, Iraq's action has made the companies more acutely aware of how fragile the control they have over their concessions has now become."; "Iraq's difficulties in resuming oil exports from the expropriated fields—there have been no exports from these fields since the expropriation—have once again reminded producer countries of their dependence on the companies for distributing the oil."; OPEC members committed to "not increasing oil exports to make up for the reduction in flow from the former IPC held fields in northern Iraq" |
| S2 | secondary (scholarly working paper) | Oxford Institute for Energy Studies (Bassam Fattouh, *An Anatomy of the Crude Oil Pricing System*, WPM 40) | *An Anatomy of the Crude Oil Pricing System* | January 2011 | https://ora.ox.ac.uk/objects/uuid:8b957970-239c-4a4f-9cbe-21830381de16/files/m79290fef21a26a470deac8273cda795f | 2026-09-03T03:1xZ (session; PDF retrieved and text extracted locally) | "Iraq opted for nationalisation in 1972."; "The oil industry witnessed a major transformation in the early 1970s when some OPEC governments stopped granting new concessions and started to claim equity participation in their existing concessions, with a few of them opting for full nationalisation."; "In October 1972, after many rounds of negotiations, the oil companies agreed to an initial 25% participation which would reach 51% in 1983." |
| S3 | secondary (retrospective journal article) | Middle East Research and Information Project, *Middle East Report* No. 243 (Shawna Bader-Blau) | "Iraqi Unions vs. Big Oil" | June 26, 2007 | https://www.merip.org/2007/06/iraqi-unions-vs-big-oil/ | 2026-09-03T03:2xZ (session) | "With the rise of Iraqi nationalism in the succeeding decades, the Iraqi government fought for an increased share of oil wealth beyond the royalties allowed by the concession contracts. The foreign company resisted, until, in 1972, the Iraqi government nationalized it." |

S1 is primary and on history.state.gov. S2 (`ora.ox.ac.uk`) and S3 (`merip.org`) are two further registrable
domains, both secondary; §1(a) permits a scholarly secondary as the second source and never as the primary, and
S1 is the primary. Three independent domains attest the nationalisation. `docs/g/ROUTE_TESTS.md` records what was
tried, including the routes that failed.

## Narrative

Iraq nationalised the Iraq Petroleum Company on 1 June 1972 [S1]. A US Bureau of Intelligence and Research note four weeks later set the act in a sequence rather than treating it as isolated: it came "on the heels of Libya's expropriation of BP's holdings in that country and Algeria's seizure last year of majority interest in French companies operating there", and it "made the companies more acutely aware of how fragile the control they have over their concessions has now become" [S1]. The physical consequence was an export stoppage, and it was still in force at the end of June: Iraq had "difficulties in resuming oil exports from the expropriated fields—there have been no exports from these fields since the expropriation" [S1]. It was not offset: OPEC members undertook to avoid "increasing oil exports to make up for the reduction in flow from the former IPC held fields in northern Iraq" [S1], which converts a bilateral expropriation into a supply event. Two independent retrospective accounts confirm the act: "Iraq opted for nationalisation in 1972", against the participation agreement the other Gulf states signed in October 1972 at "an initial 25% participation" [S2]; and "the foreign company resisted, until, in 1972, the Iraqi government nationalized it" [S3]. No source retrieved this session gives the barrels per day removed, and none is asserted here; the fields are identified only as "the former IPC held fields in northern Iraq" [S1].

## Knowable at

1972-06-01, day precision. Reason: the nationalisation date is stated as a fact in a primary US government document [S1]. The document is dated 27 June 1972, so what it establishes is the event's date, not the day the market learned of it; a nationalisation decree of this kind is normally announced, but no source retrieved this session records the announcement, and the inference is therefore left out. `date_precision` stays `day` on the stated date.

## Entities

- `country.iraq` — actor — the nationalising state [S1].
- `country.libya` — affected — named in [S1] as the precedent (BP's holdings).
- **Gap:** the register has no entity for an oil company (IPC, BP), and no `country.algeria`, `country.france` — both named in [S1]. Reported to Session A rather than invented.
- **Gap:** the register has no entity for the northern Iraq producing region or the Kirkuk–Mediterranean pipeline system through which those fields exported; `chokepoint.kirkuk_ceyhan_pipeline` is a later asset and is **not** used here, because [S1] names no pipeline.

## Class

Proposed class: `opec_decision`. Two clauses are in play and neither is a clean fit, so both are named as §1(e) requires. "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks" fires on the second half of the event — OPEC's collective undertaking not to replace the lost northern-Iraq flow [S1] — and Iraq is an OPEC member acting on its own output, which the v3 codebook amendment rule 2 assigns here. "`sanctions` | Sanctions imposed, tightened, or lifted on a producer" does **not** fire: the coercion runs from the producer to companies, and the clause requires a producer as the target.
Tie-break stated: `opec_decision`, on the OPEC undertaking and on rule 2.
**Codebook gap, reported rather than worked around:** an expropriation is not a production decision, and the closed set has no class for it. Three of the six records in this Session G batch (Libya 1970, Tehran 1971, Tripoli 1971) hit the same wall, and IPC 1972 is the clearest case. Session G's recommendation to Joe and Session E is a v3 class for concession and ownership changes; it is not decided here.

## Not known at the time

How long the export stoppage would last, whether Iraq could market the crude without the companies (the note frames this as the open question, and as a general lesson about "their dependence on the companies for distributing the oil" [S1]), and whether the OPEC undertaking not to backfill would hold. Also unknown: that this sequence — Algeria 1971, Libya 1971, Iraq 1972 — was the beginning of the transfer of pricing power that would be complete by 1973/74. [S1] is dated 27 June and is itself already a retrospective on a 1 June act; nothing in it should be treated as knowable on 1 June except the fact and date of the nationalisation.

## Proposed field changes

Not applicable — no row in `events`. If Joe admits it: `event_date` 1972-06-01; `date_precision` day; `type` opec_decision; `source_url` https://history.state.gov/historicaldocuments/frus1969-76v36/d124; `severity` **unknown** — the export stoppage is established but its size is not, and a severity code without barrels would be a plausible value rather than a measurement; `surprise` **unknown**; `hostility` not applicable.

## Status

**complete** (upgraded 2026-09-03 from `partial — fails (a)`; the earlier status is preserved below).
(a) three independent registrable domains — `history.state.gov` (S1, primary), `ora.ox.ac.uk` (S2) and `merip.org`
(S3) — with the primary requirement met by S1; (b)–(f) were already met.
**Corroboration strength, stated:** S2 and S3 are both retrospective and both attest the fact and the **year**;
neither attests the **day** (1 June), which rests on S1 alone, and neither gives barrels. S2 additionally places
the act against the October 1972 participation agreement the other Gulf states signed, which is context [S1] does
not carry. The record's remaining weakness is unchanged and is not a sourcing failure: **no source retrieved by
any session gives the volume removed**, so `severity` stays `unknown`.

*Superseded status, 2026-09-03, kept as the record: "partial — fails (a). One source, one registrable domain, and
it is dated 26 days after the event." The second and third domains existed and were not tested in the first pass.*
