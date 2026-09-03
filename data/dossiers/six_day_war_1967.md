# Six-Day War begins; Arab producers suspend deliveries     six_day_war_1967 · 1967-06-05 · day · conflict_escalation
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1964–1968, Vol. XIX, *Arab-Israeli Crisis and War, 1967*, Doc. 160) | "Telegram From the Department of State to the Embassy in Jordan" | Washington, June 5, 1967, 9:49 a.m. | https://history.state.gov/historicaldocuments/frus1964-68v19/d160 | 2026-09-03T02:2xZ (session) | "Israeli Representative here asks us to convey earnest desire of his government not do any harm to Jordan. They hope that hostilities between the two countries can be avoided or kept to a minimum." |
| S2 | primary | The American Presidency Project, University of California, Santa Barbara — Lyndon B. Johnson | "Address at the State Department's Foreign Policy Conference for Educators" | June 19, 1967 | https://www.presidency.ucsb.edu/documents/address-the-state-departments-foreign-policy-conference-for-educators | 2026-09-03T02:2xZ (session) | "If a single act of folly was more responsible for this explosion than any other, I think it was the arbitrary and dangerous announced decision that the Straits of Titan would be closed." (so transcribed in the APP text; the strait is the Straits of Tiran); "Our Nation has long been committed to free maritime passage through international waterways, and we, along with other nations, were taking the necessary steps to implement this principle when hostilities exploded."; "The right of innocent maritime passage must be preserved for all nations." |
| S1b | editorial (not primary) | U.S. Department of State, Office of the Historian (same volume, Doc. 180, Editorial Note) | "Editorial Note" | n/a (compiled) | https://history.state.gov/historicaldocuments/frus1964-68v19/d180 | 2026-09-03T02:2xZ (session) | "Iraq, Kuwait, and Algeria announced the suspension of oil deliveries to the United States and United Kingdom on June 6."; "Arab oil should be denied to countries committing aggression or participating in aggression against any Arab state." |

S1 (history.state.gov) and S2 (presidency.ucsb.edu) are two distinct registrable domains and both are primary — a contemporaneous State Department cable and a presidential address. S1b is FRUS editorial apparatus on the same domain as S1; it is cited for the oil-suspension fact and is **not** counted toward clause (a).

## Narrative

Fighting between Israel and its neighbours began on 5 June 1967. By 9:49 that morning Washington time the State Department was cabling Amman that Israel's representative wished to convey his government's "earnest desire ... not do any harm to Jordan" and hoped "hostilities between the two countries can be avoided or kept to a minimum" [S1] — a message that treats war as an established fact and Jordan's entry as the open question. Two weeks later President Johnson gave the United States' account of the cause: "If a single act of folly was more responsible for this explosion than any other, I think it was the arbitrary and dangerous announced decision that the Straits of Titan would be closed" [S2, transcribed thus; the Straits of Tiran]. He set the interest at stake as maritime: the United States "has long been committed to free maritime passage through international waterways" and had been "taking the necessary steps to implement this principle when hostilities exploded" [S2]. The oil mechanism arrived on the war's second day, when Iraq, Kuwait and Algeria announced the suspension of oil deliveries to the United States and the United Kingdom, on the principle that "Arab oil should be denied to countries committing aggression" [S1b]. No source retrieved this session gives barrels per day for that suspension, or establishes the Suez Canal's closure date, so neither is asserted here.

## Knowable at

1967-06-05, day precision. Reason: the United States government was acting on the outbreak as an established fact in a cable timed 9:49 a.m. Washington time that day [S1]. No source retrieved this session gives the clock time of the first Israeli strike or of first public knowledge, so no finer-than-day precision is claimed, and the 9:49 a.m. stamp is evidence of an upper bound on knowability, not of the event's own time.

## Entities

- `country.israel` — actor — the belligerent whose representative is speaking in [S1] and whose action Johnson is accounting for in [S2].
- `country.egypt` — target — the principal Arab belligerent; the Straits of Tiran closure that [S2] identifies as the precipitating act was Egypt's.
- `country.iraq`, `country.kuwait` — actor — the two register-named states that suspended oil deliveries on 6 June [S1b].
- `country.united_states`, `country.united_kingdom` — target — the states whose deliveries were suspended [S1b].
- **Gap:** `country.jordan`, `country.syria` and `country.algeria` do not exist in the entity register. Jordan is the addressee of [S1]; Algeria is a named participant in the delivery suspension [S1b]. Reported to Session A rather than invented.

## Class

Proposed class: `conflict_escalation`. Codebook clause: "`conflict_escalation` | War, invasion, major military escalation involving a producer/transit state" — Egypt is a producer and, through the Suez Canal, a transit state; Iraq and Kuwait, drawn in within a day, are producers.
Alternatives considered, both defensible on the episode but not on this date: `chokepoint_disruption` ("Transit through a strait/canal/pipeline is threatened or blocked"), which fires on the Straits of Tiran closure — an act that preceded 5 June and would be its own record; and `sanctions` ("Sanctions imposed, tightened, or lifted on a producer"), which fires on the 6 June suspension by Iraq, Kuwait and Algeria — a **different date and a different actor set**, and one whose target is a consumer rather than a producer, so the clause fits only loosely. Tie-break stated: the class is coded on the fact that defines 5 June, which is the war.

## Not known at the time

On 5 June the outcome was open in every direction that mattered to oil: whether Jordan would enter (the explicit subject of [S1]), whether the Arab producers would use the oil weapon and against whom (announced only the following day, [S1b]), how long the Suez Canal would be unavailable, and whether the fighting would spread to the Gulf. Johnson's attribution of cause to the Straits of Tiran closure is dated 19 June, two weeks after the fact, and is a belligerent's ally's account, not a contemporaneous neutral finding [S2]. The war's six-day length is in the name only in retrospect.

## Proposed field changes

Not applicable — no row in `events`. If Joe admits it, the values implied by this dossier are: `event_date` 1967-06-05; `date_precision` day; `type` conflict_escalation; `source_url` https://history.state.gov/historicaldocuments/frus1964-68v19/d160; `severity` **unknown** (no source retrieved this session gives barrels at risk on 5 June); `surprise` **unknown** (no source retrieved this session records a pre-5-June market or official expectation); `hostility` hostile (a state-on-state armed action; EVENTS_CODEBOOK Amendment 2026-09-02).

## Status

**complete.** (a) two independent registrable domains, both primary; (b) narrative 229 words with every claim marked; (c) knowable_at with reason and an explicit statement of what the 9:49 a.m. stamp does and does not establish; (d) register entities named, three register gaps reported to Session A; (e) class with the clause quoted, two alternatives named and the tie-break stated; (f) not-known-at-the-time separating 5 June from 6 and 19 June.
