# Nationalisation of the Suez Canal Company     suez_nationalisation_1956 · 1956-07-26 · day · chokepoint_disruption
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1955–1957, Vol. XVI, *Suez Crisis, July 26–December 31, 1956*, Doc. 2) | "Telegram From the Embassy in the United Kingdom to the Department of State" | London, July 27, 1956, 5 a.m. | https://history.state.gov/historicaldocuments/frus1955-57v16/d2 | 2026-09-03T02:1xZ (session) | "the unilateral decision of the Egyptian Government to expropriate the Suez Canal Company, without notice"; "Nasser had certainly breached the Canal company's concession"; concern whether expropriation "impaired maintenance and operation of Canal"; the aim of ensuring "maintenance Canal, freedom of transit through it, and reasonable tolls" |
| S1b | editorial (not primary) | U.S. Department of State, Office of the Historian (same volume, Doc. 1, Editorial Note) | "Editorial Note" | n/a (compiled) | https://history.state.gov/historicaldocuments/frus1955-57v16/d1 | 2026-09-03T02:1xZ (session) | "On July 26, 1956, during a broadcast address delivered from Alexandria, Egyptian President Gamal Abdel Nasser announced that he had signed into law a presidential decree nationalizing the Compagnie Universelle du Canal Maritime de Suez (henceforth referred to as the Suez Canal Company), effective immediately, and that while he spoke, Egyptian officials were taking over the administration and management of the Company." |
| S2 | primary | United Nations, Department of Peace Operations — UNEF I background (SPINE_REGISTRATION Amendment 1, A.1: UN mission histories are primary for the facts of a UN operation) | "First United Nations Emergency Force (UNEF I) — Background" | n/a (official mission history) | https://peacekeeping.un.org/sites/default/files/past/unef1backgr2.html | 2026-09-03T02:1xZ (session) | "President Gamal Abdel Nasser announced the nationalization of the Suez Canal Company a week later and declared that Canal dues would be used to finance the Aswan project."; "the Secretary-General had accepted the responsibility for organizing the task of clearing the Suez Canal as expeditiously as possible, that free and secure transit would be re-established through the Canal when it was cleared"; "The Canadian proposal was adopted by the General Assembly on the same morning and became resolution 998 (ES-I) of 4 November 1956" |
| S3 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/system/files/working_papers/w16790/w16790.pdf | 2026-09-03T02:2xZ (session; PDF retrieved and text extracted locally to the session scratchpad as `hamilton_w16790.txt`) | "During the conflict, 40 ships were sunk, blocking the canal through which 1-1/2 million barrels per day of oil were transported."; "Pumping stations for the Iraq Petroleum Company's pipeline, through which an additional half-million barrels per day moved through Syria to ports in the eastern Mediterranean, were also sabotaged."; "Total oil production from the Middle East fell by 1.7 mb/d in November 1956."; "that represents 10.1% of total world output at the time, which is a bigger fraction of world production than would be removed in any of the subsequent oil shocks" |

S1 (history.state.gov), S2 (peacekeeping.un.org) and S3 (nber.org) are three distinct registrable domains. S1 and S2 are primary; S3 is a working paper cited as secondary only, per its own cover note that NBER working papers are not peer-reviewed. S1b is FRUS editorial apparatus written by the Office of the Historian, not a contemporaneous record, and is cited for the date only — never as the primary.

## Narrative

On 26 July 1956, in a broadcast address from Alexandria, President Nasser announced a decree nationalising the Compagnie Universelle du Canal Maritime de Suez with immediate effect, and said Egyptian officials were taking over the Company's administration as he spoke [S1b]; the canal dues were to finance the Aswan dam [S2]. Within thirty hours the British government was describing the act to Washington as "the unilateral decision of the Egyptian Government to expropriate the Suez Canal Company, without notice", judging that Nasser "had certainly breached the Canal company's concession", and framing the Western objective as "maintenance Canal, freedom of transit through it, and reasonable tolls" [S1]. What was physically at risk was transit, not production: about 1½ million barrels per day of oil moved through the canal, and a further half-million barrels per day moved by the Iraq Petroleum Company's pipeline through Syria to the eastern Mediterranean [S3]. On the day, the loss was potential. It became actual only in the autumn, when 40 ships were sunk in the canal and the IPC pumping stations were sabotaged, and Middle East production fell by 1.7 mb/d in November 1956 — 10.1 % of world output [S3]. Clearance was organised by the UN Secretary-General [S2].

## Knowable at

1956-07-26, day precision. Reason: the nationalisation was announced in a public broadcast address that evening and took effect immediately [S1b]; the British Cabinet was acting on it by the following morning [S1]. No source retrieved this session gives the clock time of the broadcast or of first wire transmission, so no finer-than-day precision is claimed.

## Entities

- `country.egypt` — actor — the nationalising government, named in [S1], [S1b] and [S2].
- `chokepoint.suez_canal` — affected_market / location — the asset expropriated and the transit at risk [S1] [S3].
- `country.united_kingdom` — target — the state whose nationals' concession was expropriated and whose government responded [S1].
- **Gap:** `country.france` does not exist in the entity register. France was the Suez Canal Company's other principal shareholder state and a co-belligerent in the October action. Reported to Session A rather than invented.
- **Gap:** `country.syria` does not exist in the register; the IPC pipeline that carried the additional half-million b/d ran through Syria [S3].

## Class

Proposed class: `chokepoint_disruption`. Codebook clause: "`chokepoint_disruption` | Transit through a strait/canal/pipeline is threatened or blocked". On 26 July 1956 transit was **threatened**, which the clause covers explicitly, and the contemporaneous Western objective was stated in exactly those terms — "freedom of transit through it" [S1].
Alternative considered: `conflict_escalation` ("War, invasion, major military escalation involving a producer/transit state"), which fires for the Anglo-French-Israeli action of 29 October 1956. That is a **different event on a different date** and should be a separate record if admitted; it is not the 26 July event. Tie-break stated: the class is coded on the fact that defines the event date, not on what the episode later became.

## Not known at the time

That the canal would be physically blocked by sunk ships, that the IPC pipeline pumping stations would be sabotaged, and that Middle East production would fall 1.7 mb/d — all of that is November 1956 and none of it was established on 26 July [S3]. Nor was it known that Britain, France and Israel would act militarily, that the United States would oppose them, or that the UN would create an emergency force and take on the clearance of the canal [S2]. On the day the event was a change of ownership of a company, with the transit consequence entirely prospective. The 10.1 %-of-world-output figure is a retrospective computation and was not available to anyone in 1956.

## Proposed field changes

Not applicable — this event has no row in `events`. If Joe admits it, the admission values implied by this dossier are: `event_date` 1956-07-26; `date_precision` day; `type` chokepoint_disruption; `source_url` https://history.state.gov/historicaldocuments/frus1955-57v16/d2; `severity` **unknown** (no source retrieved this session establishes the barrels at risk *as assessed on 26 July*, and the 1.5 mb/d transit figure is Hamilton's retrospective statement of normal flow, not a contemporaneous risk assessment); `surprise` **unknown** (no source retrieved this session records a pre-26-July expectation).

## Status

**complete.** (a) two independent registrable domains with two primary sources (history.state.gov, peacekeeping.un.org) plus a scholarly secondary (nber.org); (b) narrative 203 words, every claim carrying its marker; (c) knowable_at with reason and precision; (d) entities from the register, with two register gaps reported to Session A rather than invented; (e) class with the codebook clause quoted, the alternative named and the tie-break stated; (f) an explicit not-known-at-the-time separating the July facts from the November ones.
