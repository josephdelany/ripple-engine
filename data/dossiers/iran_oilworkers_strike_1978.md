# Iranian oil-workers strike halts exports (Revolution onset)     iran_oilworkers_strike_1978 · 1978-10-31 · day (challenged — see Class/Proposed changes) · infrastructure_attack (challenged)

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVII, *Energy Crisis, 1974–1980*, Doc. 168) | "Summary of Conclusions and Minutes of Policy Review Committee Meeting" | Washington, November 9, 1978, 3–4:23 p.m. | https://history.state.gov/historicaldocuments/frus1969-76v37/d168 | 2026-09-02T20:38Z (session) | "The Iranian shortfall will soon be felt in the oil market." "[I]f the Iranian strike is going to be prolonged, Secretary Blumenthal should press Kuwait, the UAE and the Saudis to increase their production as much as possible." "Kuwait and the UAE together had only 600,000 bpd of excess production capacity and in the entire world there was only 1.7 million bpd in excess capacity." |
| S2 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:25Z (session; local extracted text `hamilton_w16790.txt`) | "Strikes spread to the oil sector by the fall of 1978, bringing Iranian oil production down by 4.8 mb/d (or 7% of world production at the time) between October 1978 and January 1979. In January the Shah fled the country, and Sheikh Khomeini seized power in February. About a third of the lost Iranian production was made up by increases from Saudi Arabia and elsewhere." (printed p. 16 of the working paper) |

S1 and S2 are on different registrable domains (history.state.gov vs. nber.org); S1 is a contemporaneous U.S. government policy-committee record (primary); S2 is a scholarly working paper the NBER's own cover page says has not been peer-reviewed, cited here only as secondary. **Neither source gives October 31, 1978, specifically** — see Class and Proposed field changes below.

## Narrative

By early November 1978 the U.S. government was treating an ongoing Iranian oil-workers' strike as an established fact materially affecting the world oil market: a Policy Review Committee meeting on November 9 concluded "the Iranian shortfall will soon be felt in the oil market" and discussed pressing Kuwait, the UAE, and Saudi Arabia to raise output "if the Iranian strike is going to be prolonged" [S1]. The stakes were tight — combined Kuwaiti and UAE spare capacity was only 600,000 barrels a day, and world spare capacity as a whole was just 1.7 million b/d [S1], against a strike that eventually (per a 2011 scholarly retrospective, not a contemporaneous source) cut Iranian output by 4.8 million b/d, about 7% of then-world production, between October 1978 and January 1979 [S2]. That source dates the strikes only to "the fall of 1978" and does not give October 31 specifically [S2]. What was known contemporaneously, as of November 9, was that a strike was underway and its duration was uncertain enough that U.S. officials were already planning for a "prolonged" scenario [S1]; the eventual full magnitude, the Shah's flight, and Khomeini's accession were not yet facts on November 9 and are known only in hindsight, from S2.

## Knowable at

Cannot be pinned to October 31, 1978 from sources retrieved this session. The earliest retrieved documentary confirmation that "the Iranian strike" was a live, named policy concern is the Policy Review Committee meeting of **1978-11-09** [S1] — nine days after the database's current `event_date`. Hamilton [S2] places strikes reaching the oil sector only as generally "by the fall of 1978," with the cited 4.8 mb/d decline measured "between October 1978 and January 1979" — a range, not a day. No source retrieved this session establishes what specifically happened on October 31 itself, or that it was the first day the strike affected exports as opposed to some other day in the surrounding weeks.

## Entities

- `country.iran` — actor — per the existing `event_entities` rows; consistent with both sources, which discuss Iranian oil workers/strikers and the Iranian state as the locus of the disruption [S1][S2].
- `country.iran` — target — as currently recorded. This is a modeling oddity worth flagging to Session A rather than resolving here: coding Iran as both actor and target of its own workers' strike blurs who is doing what to whom. A strike is workers acting against employers/the state, not the state acting against itself. No replacement entity is proposed (no distinct "labor" or equivalent actor exists in the entity register, per this session's check of `entities.entity_id`), so this is reported as a gap, not silently changed.

## Class

Proposed class as currently coded: `infrastructure_attack`. Codebook clause: "`infrastructure_attack` | Direct strike on production, refining, or export infrastructure." **This class does not fit, and the evidence retrieved this session supports saying so plainly.** A labor strike — workers withholding labor — is not a "direct strike" on infrastructure in the codebook's sense of an attack; nothing in either retrieved source describes physical damage, sabotage, or an assault on any pipeline, refinery, field, or terminal. Both sources use "strike" only in the labor sense: S1 refers explicitly to "the Iranian strike" in the context of a labor/production stoppage, not an attack [S1]; S2 frames it as workers' strikes spreading "to the oil sector," a mechanism of withheld labor, not physical destruction [S2].

No class in the closed six-type set is a clean fit. The two next-closest candidates:
- `demand_shock` — wrong; this is a supply-side event, not a demand-side one.
- `conflict_escalation` — the codebook clause is "War, invasion, major military escalation involving a producer/transit state." A national labor strike is not itself a war, invasion, or military escalation, though it occurred as part of the broader anti-Shah revolutionary movement that both sources connect to political upheaval [S2].

Neither is defensible as a direct fit. This is flagged for Joe rather than silently reclassified, per SPINE_REGISTRATION.md §1(e): the corpus may need a class this event genuinely belongs in (e.g., something like a labor-disruption or non-violent-supply-disruption type) that does not currently exist in the pre-registered set.

## Not known at the time

As of the November 9, 1978 meeting — the earliest point this session can document contemporaneous awareness — officials did not yet know whether the strike would be "prolonged" [S1]; that was explicitly framed as a contingency, not a certainty. The eventual scale (4.8 mb/d, 7% of world production), the Shah's departure in January 1979, and Khomeini's seizure of power in February 1979 were all future events not yet known on November 9, and are drawn from a 2011 retrospective [S2], not from anything contemporaneous.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `type` | `infrastructure_attack` | Flag for Joe — no source retrieved supports this class; nearest defensible alternative (`conflict_escalation`) is also a stretch. Do not silently reclassify. | [S1][S2] |
| `date_precision` | `day` | `month` (October 1978) — no retrieved source establishes October 31 as a specific, first-knowable day; Hamilton gives only a month-scale range and the earliest primary confirmation found is November 9. | [S1][S2] |
| `source_url` | https://www.nber.org/papers/w16790 (secondary only, already correctly cited as such) | Add https://history.state.gov/historicaldocuments/frus1969-76v37/d168 as a primary companion source | [S1] |
| `confidence` | medium | medium (unchanged) — a single solid primary source (S1) plus a scholarly secondary (S2), per the codebook's "medium (single solid source)" tier; not "high," since S1 and S2 do not independently corroborate a specific date. | [S1][S2] |
| `severity` | NULL | Proposed 4 — "major producer/route affected; multi-week disruption plausible." Reasoning, by expected disruption not price reaction: by November 9 the shortfall was already assessed against a world spare-capacity cushion of only 1.7 mmbd [S1], and the strike was explicitly being planned for on a "prolonged" basis [S1] — a major-producer, multi-week disruption was a live, officially-discussed contingency at that point, even though the ultimate 4.8 mb/d figure [S2] was not yet known. | [S1] |
| `surprise` | NULL | Not proposed. No source retrieved this session states what was publicly expected the day before the strike began (whichever day that was), which the codebook requires for a surprise code ("code by what was publicly expected the day before"). Coding this from the November 9 document would improperly use nine-days-later information. | — |

## Status

**partial — fails (a) in the exact-date sense (no source pins the day-31), fails (c) (`knowable_at` cannot be set to a specific day), and fails (e) (class is actively disputed, not confirmed).** Clause (b) is met in the qualified sense that every claim in the narrative carries a source marker, but the narrative itself documents that neither source supports the record's specific date. Clause (f) is met. Two independent-domain sources with one primary are present, satisfying the letter of clause (a)'s two-source/one-primary test, but the deeper problem — that neither source actually dates the event to October 31 — is more consequential than a technical pass/fail and is why this is marked partial rather than complete.
