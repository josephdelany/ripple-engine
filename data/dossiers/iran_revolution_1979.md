# Iranian Revolution culminates     iran_revolution_1979 · 1979-02-11 · day (challenged — see Knowable at) · conflict_escalation (challenged — see Class)

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVII, *Energy Crisis, 1974–1980*, Doc. 189) | Telegram From the Embassy in Belgium to the Department of State, Subject: "Iranian Oil Squeeze: Time for an IEA Maximum Import Passthrough Price?" | Brussels, February 12, 1979, 1002Z | https://history.state.gov/historicaldocuments/frus1969-76v37/d189 | 2026-09-02T20:47Z (session) | "The spectacle of across the board cutbacks in oil supplies by the international oil majors to firm contract customers and of rising spot prices for crude and petroleum products in world oil markets brings with it an uncomfortable feeling of 'deja vu'." "In the coming oil squeeze of 1979–80 (assuming a continuing Iranian shortfall and unwillingness or inability of the Saudis, et al, to cover it), it would seem pointless to permit a repetition of our earlier experience." "Time is of the essence. Once spot prices skyrocket and the scramble really starts, it will be impossible to put the genie back in the bottle." |
| S2 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:25Z (session; local extracted text `hamilton_w16790.txt`) | "In January the Shah fled the country, and Sheikh Khomeini seized power in February. About a third of the lost Iranian production was made up by increases from Saudi Arabia and elsewhere." (printed p. 16 of the working paper) |

**Important limitation shared by both sources:** neither actually documents the political event the database records — the February 11, 1979 collapse of the Bakhtiar government and Khomeini's forces taking power. S1 is dated one day after and is exclusively about the oil-market consequence, written from Brussels (an IEA-adjacent post), not from Tehran or about the political mechanics. S2 gives only "February," not February 11 specifically, and frames the fact as "Khomeini seized power," without describing the Bakhtiar government's collapse the database's title implies ("culminates"). This session did not locate a primary or secondary source describing the political events of February 11 itself — see Knowable at and Status.

## Narrative

The day after the database's recorded event date, a U.S. Foreign Service officer in Brussels wrote to the Department of State warning of "an uncomfortable feeling of 'deja vu'" as international oil majors cut supplies to contract customers and spot prices rose, driven by "a continuing Iranian shortfall" that Saudi Arabia and others might be unable or unwilling to fully cover [S1]. The cable urged speed, warning that "once spot prices skyrocket... it will be impossible to put the genie back in the bottle" [S1] — evidence that by February 12 the U.S. government treated an ongoing, worsening Iranian supply disruption as an established, market-moving fact. Separately, a 2011 scholarly retrospective states that the Shah's January flight was followed by Khomeini seizing power "in February," with roughly a third of lost Iranian production eventually made up by Saudi Arabia and elsewhere [S2] — but this source does not specify a day within February, and this dossier does not assert February 11 on its authority. Neither retrieved source describes the domestic political mechanics of the transfer of power itself (the Bakhtiar government's fall, Khomeini's provisional government taking control) that the event's title claims culminated on this date; what is documented here is only the oil-market reaction the State Department was already discussing one day later [S1].

## Knowable at

**Cannot be confirmed to day precision from sources retrieved this session.** S1 is dated February 12, 1979 — one day after the database's event_date — and documents that an Iranian supply shortfall was an active, named policy concern by that point, but it discusses the oil market, not the political transfer of power the event nominally records. S2 gives only "February" for Khomeini's seizure of power, with no day. No source retrieved this session establishes that February 11 specifically, rather than some other day in the surrounding period, is the first day a market participant could have known the political fact the record claims.

## Entities

- `country.iran` — actor — per the existing `event_entities` rows; consistent with both sources' focus on Iran as the locus of the shortfall/political change [S1][S2].
- `country.iran` — target — as currently recorded, with the same duplication concern flagged in the companion dossiers `iran_oilworkers_strike_1978` and `shah_leaves_iran_1979`. Reported to Session A rather than resolved here.

## Class

Proposed class as currently coded: `conflict_escalation`. Codebook clause: "War, invasion, major military escalation involving a producer/transit state." As with `shah_leaves_iran_1979`, this is a defensible-but-imperfect fit: a domestic revolutionary government transition is not itself a war, invasion, or military escalation in the codebook's plain sense, though it is the culmination of a period of mass unrest and, per general historical knowledge outside what was sourced this session, did involve armed clashes between revolutionary and government forces — a claim this dossier does not cite because no retrieved source this session documents it. No other class in the closed set fits better. This is flagged as the same category of weak fit as `shah_leaves_iran_1979`, not resolved.

## Not known at the time

As of February 12, the State Department cable treated the Iranian shortfall as ongoing and its resolution as uncertain — contingent on whether Saudi Arabia and others would or could cover it [S1] — not as a settled matter. The eventual full scale of the disruption and the identity of Iran's new government are not established by anything retrieved this session for this specific date; S2's "about a third... made up by increases from Saudi Arabia" [S2] is a retrospective figure, not something knowable in real time in mid-February 1979.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `date_precision` | `day` | `month` (February 1979) — no source retrieved this session establishes February 11 specifically as the correct day; Hamilton gives only the month [S2], and the nearest primary document is dated February 12 and is about oil markets, not the political transition itself [S1]. | [S1][S2] |
| `source_url` | https://www.nber.org/papers/w16790 (secondary only) | Add https://history.state.gov/historicaldocuments/frus1969-76v37/d189 as a primary companion source, with the caveat above that it does not itself describe the political event | [S1] |
| `confidence` | medium | low — the codebook's "low (contested or unclear)" tier applies: this dossier could not locate, this session, a source that actually describes the political event the record names, only adjacent oil-market correspondence one day later and a scholarly source giving only a month. | [S1][S2] |
| `severity` | NULL | Not proposed. The retrieved sources describe the ongoing oil-market consequence of the broader Iranian shortfall (already underway since the strikes — see `iran_oilworkers_strike_1978`) rather than giving evidence specific to whatever happened on February 11 that would let severity be coded to this date rather than to the strike's onset. | — |
| `surprise` | NULL | Not proposed. No source retrieved this session states what was publicly expected about the political transition the day before. | — |

## Status

**partial — fails (a) (S1's primary content is about the oil market one day later, not the political event itself, so no source retrieved this session directly documents the claimed event), fails (c) (`knowable_at` cannot be set to day precision), and fails (e) (class is a defensible-but-weak fit, unconfirmed).** The narrative (b) and not-known-at-the-time (f) clauses are met in the qualified sense that they describe only what the retrieved sources actually say, which is less than the event's title claims. This is the weakest-sourced of the three `conflict_escalation`-coded events in this batch and the one most in need of a session with access to a source describing the February 11, 1979 political transition directly (a wire report, a Tehran-datelined cable, or the still-unpublished FRUS Vol. X, *Iran: Revolution, January 1977–November 1979*, which this session confirmed is listed as "Being Cleared" and not yet available).
