# Yom Kippur War begins (Egypt/Syria vs Israel)     yom_kippur_war_1973 · 1973-10-06 · day · conflict_escalation

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXV, *Arab-Israeli Crisis and War, 1973*, Doc. 121) | "Minutes of Washington Special Actions Group Meeting" | Washington, October 7, 1973, 6:06–7:06 p.m. | https://history.state.gov/historicaldocuments/frus1969-76v25/d121 | 2026-09-02T20:33Z (session) | "The Syrians have a large force on the Heights—three infantry and one armored division." (Colby); "The number of Egyptians across the Canal changed from 3,000 men and 60 tanks to 15,000 men and 400 tanks in the course of the day." (Schlesinger); Kissinger characterized the Israelis as "unprepared." |
| S2 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:33Z (session) | "Syria and Egypt led an attack on Israel that began on October 6, 1973." (p. 14 of the extracted text, local copy `hamilton_w16790.txt`) |

S1 and S2 are on different registrable domains (history.state.gov vs. nber.org); S1 is primary (a contemporaneous U.S. government record), S2 is a scholarly working paper cited as secondary only, per its own cover note that NBER working papers are not peer-reviewed.

## Narrative

On October 6, 1973, Egypt and Syria attacked Israel, opening fronts across the Suez Canal and on the Golan Heights [S2]. The United States' first crisis meeting on the war, held the next evening, recorded Syrian forces on the Golan as "a large force ... three infantry and one armored division" and Egyptian forces crossing the Canal growing "from 3,000 men and 60 tanks to 15,000 men and 400 tanks in the course of the day" — figures reflecting October 6–7 intelligence, not October 6 alone [S1]. At that same meeting Secretary of State Kissinger characterized Israel as having been "unprepared" [S1], consistent with the attack's reputation as a strategic surprise. This dossier could not establish, from sources retrieved this session, Egypt's or Syria's 1973 oil production or the Suez Canal's transit status that day — the canal had been closed to shipping since the 1967 war, but no source fetched this session confirms that fact for October 1973, so it is not asserted here. The war itself did not immediately disrupt oil exports; that mechanism came eleven days later via the OAPEC embargo (a separate, later event) [S2].

## Knowable at

1973-10-06, day precision. Reason: this is the day fighting began, per Hamilton's chronology [S2]; the U.S. government was treating the war as an established, ongoing fact by its first WSAG meeting the next evening [S1]. No source retrieved this session gives the exact clock time of the attack or of first public/wire knowledge, so no finer-than-day precision is claimed.

## Entities

- `country.egypt` — actor — named as an attacking party in [S1] ("Egyptians across the Canal") and [S2].
- `country.israel` — target — the attacked state, per [S1] ("the Israelis") and [S2].
- **Gap:** `country.syria` does not exist in the entity register. Syria is co-named as an actor in both [S1] ("The Syrians have a large force on the Heights") and [S2] ("Syria and Egypt led an attack"). Reported to Session A rather than invented.

## Class

Proposed class: `conflict_escalation`. Codebook clause: "`conflict_escalation` | War, invasion, major military escalation involving a producer/transit state" — Egypt (a producer and, via the Suez Canal, a transit state) and Syria (a transit state for the Trans-Arabian pipeline network) attacking Israel is a direct fit. No alternative class in the closed set is defensible: this is not a sanctions action, an OPEC/OAPEC decision, a chokepoint disruption in the narrow sense (no source retrieved establishes the canal was carrying oil transit at the time), an infrastructure attack, or a demand shock.

## Not known at the time

The scale of Egyptian and Syrian forces committed was still being revised hour-to-hour on October 6–7 (the Egyptian force estimate roughly quintupled "in the course of the day" per [S1]) — the eventual outcome of the war (a negotiated cease-fire October 25 and disengagement agreements into 1974) was unknown on October 6, as was the fact that Arab oil producers would respond with a formal embargo eleven days later. This dossier does not treat the embargo as knowable on October 6 itself; it is coded as the separate event `oapec_embargo_1973`.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "Egypt and Syria attacked Israel on October 6, 1973, opening fronts across the Suez Canal and the Golan Heights; the U.S. government's first crisis meeting the next day recorded the attack as a strategic surprise to Israel and rapidly escalating force numbers on both fronts." | [S1][S2] |
| `source_url` | https://www.nber.org/papers/w16790 (secondary only) | https://history.state.gov/historicaldocuments/frus1969-76v25/d121 (primary) | [S1] |
| `severity` | NULL | 3 — "meaningful volumes at risk; partial disruption plausible." Reasoning: Egypt and Syria are producer/transit states but neither was a top-tier producer, and no source retrieved this session shows the war itself (as opposed to the subsequent embargo) physically interrupting production or transit on October 6. Proposed at 3 rather than higher because the disruption mechanism that actually moved barrels was the separate OAPEC decision of October 17, not the war's outbreak per se. | [S1][S2] |
| `surprise` | NULL | 5 — "genuine shock; essentially nobody was positioned for it." Reasoning: Kissinger's own contemporaneous characterization of Israel as "unprepared," recorded one day after the attack [S1], is the strongest available evidence. Caveat: this is a same-side, day-after assessment, not a retrieved day-before (October 5) press or intelligence estimate of expectations — no such source was retrieved this session, so confidence in this code should be treated as medium, not high. | [S1] |
| `date_precision` | day | day (unchanged) | [S1][S2] |
| `event_date` | 1973-10-06 | 1973-10-06 (unchanged) | [S1][S2] |

## Status

partial — fails (a) in spirit though not in letter: two independent-domain sources are present with one primary (S1, history.state.gov) and one secondary (S2, nber.org), satisfying the literal two-source/one-primary test. It is marked **partial** here because the primary source (S1) is dated October 7, one day after the event, not October 6 itself — no source dated October 6 was located or retrieved this session — and because the entity gap (`country.syria` missing from the register) means clause (d) cannot be fully closed until Session A acts. The narrative (clause b), knowable_at (c), class (e), and not-known-at-the-time (f) clauses are otherwise met.
