# Iraq nationalises the Iraq Petroleum Company     iraq_ipc_nationalisation_1972 · 1972-06-01 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 124) | "Intelligence Note Prepared in the Bureau of Intelligence and Research (RECN–15)" | Washington, June 27, 1972 | https://history.state.gov/historicaldocuments/frus1969-76v36/d124 | 2026-09-03T02:2xZ (session) | "Iraq's nationalization of the Iraq Petroleum Company (IPC) on June 1"; "Two sobering realizations have been brought home by the Iraqi expropriation of IPC. Coming on the heels of Libya's expropriation of BP's holdings in that country and Algeria's seizure last year of majority interest in French companies operating there, Iraq's action has made the companies more acutely aware of how fragile the control they have over their concessions has now become."; "Iraq's difficulties in resuming oil exports from the expropriated fields—there have been no exports from these fields since the expropriation—have once again reminded producer countries of their dependence on the companies for distributing the oil."; OPEC members committed to "not increasing oil exports to make up for the reduction in flow from the former IPC held fields in northern Iraq" |

One source, one registrable domain. No second source was retrieved for this event this session; `docs/g/ROUTE_TESTS.md` records what was tried.

## Narrative

Iraq nationalised the Iraq Petroleum Company on 1 June 1972 [S1]. A US Bureau of Intelligence and Research note four weeks later set the act in a sequence rather than treating it as isolated: it came "on the heels of Libya's expropriation of BP's holdings in that country and Algeria's seizure last year of majority interest in French companies operating there", and it "made the companies more acutely aware of how fragile the control they have over their concessions has now become" [S1]. The physical consequence was an export stoppage, and it was still in force at the end of June: Iraq had "difficulties in resuming oil exports from the expropriated fields—there have been no exports from these fields since the expropriation" [S1]. That stoppage was not offset. OPEC members undertook to avoid "increasing oil exports to make up for the reduction in flow from the former IPC held fields in northern Iraq" [S1] — a collective decision not to replace the lost barrels, which converts a bilateral expropriation into a supply event. No source retrieved this session gives the barrels per day removed, and none is asserted here; the fields are identified only as "the former IPC held fields in northern Iraq" [S1].

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

**partial — fails (a).** One source, one registrable domain, and it is dated 26 days after the event. It is a primary US government record and it establishes the date, the export stoppage and the OPEC undertaking, but clause (a) requires two independent sources and this record has one. Clauses (b)–(f) are met.
