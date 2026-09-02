# Operation Earnest Will begins (US reflagging/escort)     earnest_will_1987 · 1987-07-22 · day · chokepoint_disruption (contested — see Class)

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian, *Foreign Relations of the United States, 1981–1988*, Volume I, Document 302 | "Remarks by President Reagan [on United States Policy in the Persian Gulf]" | May 29, 1987, Washington | https://history.state.gov/historicaldocuments/frus1981-88v01/d302 | 2026-09-02 (session; exact time not logged) | "The use of the vital sealanes of the Persian Gulf will not be dictated by the Iranians." / "Freedom of navigation is not an empty cliche of international law. It is essential to the health and safety of America." |
| S2 | press | United Press International (UPI Archives) | "The three U.S. Navy warships guarding the two Kuwaiti [oil tankers]..." | filed July 22, 1987, dateline "Aboard the USS Fox in the Gulf of Oman" | https://www.upi.com/Archives/1987/07/22/The-three-US-Navy-warships-guarding-the-two-Kuwaiti/7305553924800/ | 2026-09-02 (session; exact time not logged) | "The very large crude oil carrier, Bridgeton, and the liquid petroleum gas tanker, the Gas Prince, both of which swapped Kuwaiti flags for American banners Tuesday morning, will be guided north to Kuwait..." / "As of late Tuesday, the nine-ship Navy Middle East Force was still awaiting President Reagan's go-ahead for the operation." |

S1 (history.state.gov) and S2 (upi.com) are independent registrable domains, satisfying two sources. Only S1 meets the SPINE_REGISTRATION.md §1(a) "primary" test cleanly (a Presidential remarks record); it is dated May 29, 1987 — the policy rationale for the escort, not a same-day statement on the reflagging/convoy departure itself. No presidential document, FRUS entry, or Federal Register item dated July 21–24, 1987 was found this session (FRUS Vol. I, ch. 8 has no document between June 12 and August 10, 1987 — verified by listing the full table of contents). This is a genuine gap: the primary source anchoring this record is not contemporaneous with the coded event_date.

## Narrative

On July 21, 1987, two Kuwaiti-owned vessels, the tanker Bridgeton and the gas carrier Gas Prince, exchanged Kuwaiti colors for the U.S. flag [S2]. The next morning, July 22, the U.S. Navy Middle East Force — the frigate Fox, destroyer Kidd, and frigate Crommelin — prepared to escort the two reflagged ships roughly 600 miles through the Strait of Hormuz to Kuwait, the first convoy of what the Navy called Operation Earnest Will [S2]. As of the evening before departure, the convoy was still "awaiting President Reagan's go-ahead" [S2]: this was a presidential-level decision, acted on by the United States at Kuwait's request (Kuwait's tankers were the vessels reflagged) [S2]. Two months earlier, Reagan had framed the policy rationale publicly: "The use of the vital sealanes of the Persian Gulf will not be dictated by the Iranians" [S1]. No source retrieved this session states a barrel-per-day figure for Kuwaiti exports at risk; the only retrieved trade-unit detail is vessel-specific — the Bridgeton's reported deadweight tonnage of roughly 400,000 tons [S2]. What was known by July 22: the reflagging had occurred and a Navy-escorted transit was imminent, publicly reported in advance, including planned routing near Iran's declared "exclusion zone" [S2].

## Knowable at

Two distinct sub-events are conflated under one event_date. The flag-transfer ceremony occurred the morning of July 21, 1987 (reported "Tuesday morning" in a wire filed July 22) [S2]. The escorted Gulf transit itself — what the Navy branded "Earnest Will" — got under way the morning of July 22, 1987, after Reagan's approval, per the same wire [S2]. Reason for day precision: UPI's dateline and same-day reporting from aboard the escort ships fixes both dates; no finer (hour-level) timestamp was retrieved this session for either the reflagging ceremony or the convoy's actual departure time.

## Entities

- `country.usa` — actor — confirmed: the U.S. Navy conducted the escort at presidential authorization [S1][S2]. Matches existing coding.
- `chokepoint.hormuz` — currently coded `target` in `event_entities`. This dossier proposes reclassifying to `location`: nothing was attacking or threatening to seize the Strait of Hormuz on this date; the convoy transited it. "Target" does not fit any of the codebook's four defined roles (actor/target/location/affected_market) for what the Strait's role actually was in this event [S2].
- `country.kuwait` — proposed addition, role `actor`: the tankers reflagged were Kuwaiti-owned, and the operation was undertaken at Kuwait's request; `country.kuwait` already exists in the entity register (confirmed this session) so this is not a new-entity request, only a role proposal [S2].
- No commodity entity is currently coded for this event. This dossier does not propose adding one: no source retrieved this session states a benchmark-crude linkage stronger than "the Bridgeton will fill with crude oil" from press reporting not directly quoted here, and inventing a commodity role without a retrieved quote tying it to a specific benchmark would not be sourced.

## Class

Proposed class as coded: `chokepoint_disruption`. Codebook clause: "Transit through a strait/canal/pipeline is threatened or blocked." The fit is imperfect and the challenge is recorded rather than silently resolved: this event is the U.S. *response* to an ongoing chokepoint threat (Iranian mine and speedboat attacks against Gulf shipping), not the threatening or blocking act itself — no source retrieved this session shows Iran acting on this date to threaten or block transit. `policy_response` was considered as an alternative but its codebook definition — "deliberate government/agency market interventions (e.g. coordinated SPR/IEA strategic-reserve releases)" — does not fit a military escort operation either. No class in the closed set cleanly covers "an escort operation to counter a standing chokepoint threat." `chokepoint_disruption` is retained as the least-bad fit because the event marks the point the market could recognize materially elevated transit risk in the Strait, but this is a judgment call, flagged for Joe.

## Not known at the time

On July 22, 1987, it was not known that the Bridgeton would strike a mine two days later (see `bridgeton_mine_strike_1987`), that the escort concept itself would be tested within 48 hours of its first transit, or how many total convoys "Earnest Will" would eventually run. No source retrieved this session establishes what specific intelligence, if any, the Navy held about mine-laying near Farsi Island as of July 22.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.eia.gov (bare site root) | https://www.upi.com/Archives/1987/07/22/The-three-US-Navy-warships-guarding-the-two-Kuwaiti/7305553924800/ (press, contemporaneous) plus https://history.state.gov/historicaldocuments/frus1981-88v01/d302 (primary, but not same-day) | [S1][S2] |
| `event_date` | 1987-07-22 | Flag no change here, but note the ambiguity: the reflagging ceremony itself was July 21; the first escorted transit began July 22. Which sub-event the title "US reflags Kuwaiti tankers" is meant to date is not resolved by this dossier — reported as a gap for Joe. | [S2] |
| `entities: chokepoint.hormuz:target` | target | location | [S2] |
| `entities` | (no `country.kuwait`) | add `country.kuwait:actor` | [S2] |
| `severity` | NULL | not proposed — no source retrieved this session quantifies expected disruption to Gulf oil flows from the reflagging decision itself (as distinct from the later Bridgeton mining) | — |
| `surprise` | NULL | not proposed — the reflagging policy had been publicly debated since at least March 1987 per background reporting, but no source retrieved and quoted this session establishes a specific "day-before" expectation baseline for July 21–22 specifically | — |

## Status

partial — fails clause (a) in substance: the only primary source retrieved (S1) is not dated to the event or the surrounding week, and no War Powers Resolution letter, Federal Register item, or FRUS document covering the July 21–24, 1987 window could be located this session despite a direct search of the FRUS volume's full table of contents. Clause (c) is also weakened by the conflated reflagging-vs-convoy-departure dates. Clauses (b), (d), (e), and (f) are addressed with the caveats stated above.
