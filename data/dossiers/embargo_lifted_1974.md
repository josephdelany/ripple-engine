# Arab oil embargo lifted     embargo_lifted_1974 · 1974-03-18 · day · sanctions

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 342) | "Memorandum From the President's Assistant for National Security Affairs (Kissinger) to President Nixon" — subject "Arab Lifting of the Oil Embargo" | Washington, March 19, 1974 | https://history.state.gov/historicaldocuments/frus1969-76v36/d342 | 2026-09-02T20:33Z (session) | "The Arab oil ministers yesterday announced their decision to lift their oil embargo against the US, saying that this decision would be reviewed at their June 1 meeting. Algeria explicitly made the lifting 'provisional' until June 1, and neither Syria nor Libya associated itself with the official announcement." Also: "the decision to lift the embargo is subject to review at an oil ministers' meeting June 1 ... the embargo might be reimposed then if there is inadequate progress on disengagement." |
| S2 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, Doc. 287) | "Message From Royal Adviser Adham and Prince Saud ibn Faisal of Saudi Arabia to the President's Assistant for National Security Affairs (Kissinger)" | Jidda, January 22, 1974 | https://history.state.gov/historicaldocuments/frus1969-76v36/d287 | 2026-09-02T20:33Z (session) | Proposed terms: "immediate total lifting of the oil boycott (on everyone) and return to September production levels for a fix[ed] period of 90 days," after which "the boycott would be reimposed if 'satisfactory' progress is not being made." Sadat and Faisal "trying to get the embargo lifted as fast as is humanly possible." |
| S3 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, Doc. 307) | "Letter From President Nixon to King Faisal of Saudi Arabia" | Washington; forwarded Feb. 6, handed to Saudi Ambassador Feb. 7, 1974 | https://history.state.gov/historicaldocuments/frus1969-76v36/d307 | 2026-09-02T20:33Z (session) | "Your Majesty will surely understand my deep concern and disappointment that your efforts to bring about a prompt end of the oil embargo against the United States have not succeeded." "I fear that if the ending of the embargo at the meeting of Oil Ministers in Tripoli on February 14 is now made dependent on conclusion of a disengagement agreement on the Syrian front..." |
| S4 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:33Z (session) | "[Barsky and Kilian] noted ... that the embargo was lifted without the achievement of its purported political objectives." No specific lifting date is given by Hamilton. |

S1–S3 are primary, contemporaneous U.S. government records (history.state.gov); S4 is an independent-domain (nber.org) scholarly source cited as secondary. No press source was retrieved this session for this event.

## Narrative

Arab oil ministers announced on March 17–18, 1974 that they would lift the embargo against the United States, a decision reported "yesterday" in a Kissinger memorandum to Nixon dated March 19 [S1]. The lifting was conditional and incomplete: Algeria made its participation "provisional" until a June 1 review, and "neither Syria nor Libya associated itself with the official announcement" [S1] — the embargo continued against the U.S. from those two states. The path there had been long: in January, Saudi and Egyptian intermediaries proposed an immediate lift tied to a 90-day trial with reimposition if progress stalled [S2], and by early February Nixon was writing to King Faisal expressing "deep concern and disappointment" that a prompt end had not been achieved, after the lifting had been made contingent on Syrian-Israeli disengagement at the February 14 Tripoli oil ministers' meeting [S3]. Hamilton notes only that the embargo ultimately "was lifted without the achievement of its purported political objectives" [S4], without giving a specific date.

## Knowable at

1974-03-18, day precision. Reason: [S1] is dated March 19, 1974 and refers to the Arab oil ministers' announcement as having occurred "yesterday" — i.e., March 18. This directly supports the database's existing event_date and day precision; no source retrieved this session gives a more specific time-of-day. Location: general reporting located this announcement at a Vienna meeting of Arab oil ministers, but no source fetched this session names Vienna directly — [S1] identifies only "the Arab oil ministers" and does not give a location, so this dossier does not assert Vienna as sourced.

## Entities

- `country.saudi_arabia` — actor — Saudi Arabia is the lead intermediary pressing for the lift throughout [S2] and [S3], though not named as a signatory in the retrieved text of [S1] itself.
- `country.usa` — target — the embargo's object throughout [S1][S2][S3].
- **Gaps:** `country.syria`, `country.libya`, and `country.algeria` do not exist in the entity register. All three are materially relevant to this event specifically — Syria and Libya as non-participants in the March 18 announcement, Algeria as a provisional participant [S1] — and none can be added to `event_entities` without the entities existing first. Reported to Session A rather than invented.

## Class

Proposed class: `sanctions`. Codebook clause: "`sanctions` | Sanctions imposed, tightened, or lifted on a producer" — the "lifted" branch of this clause is the direct fit; this is the reversal of the same OAPEC sanctions action coded as `oapec_embargo_1973`. As with that event, the clause's phrasing ("on a producer") describes the producer as target rather than actor/imposer, which is the reverse of the actual roles here; flagged, not silently resolved. No alternative closed-set class fits better.

## Not known at the time

On March 18–19, 1974, it was not known whether the lift would hold: [S1] explicitly notes the decision was "subject to review" on June 1 and that reimposition was implied "if there is inadequate progress on disengagement" — i.e., contemporaries knew this was conditional, not final. It was also not known on March 18 whether Syria and Libya would eventually join the lift (this dossier did not retrieve a source establishing when, or whether, they did). The retrospective judgment that the embargo achieved none of its stated political objectives [S4] is a later scholarly assessment, not a March 1974 contemporaneous one.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "Arab oil ministers announced March 18, 1974 that they would lift the embargo on the U.S.; the lift was conditional (review set for June 1) and partial — Algeria's participation was explicitly 'provisional,' and Syria and Libya did not associate with the announcement." | [S1] |
| `source_url` | https://www.eia.gov (bare site root, not a document) | https://history.state.gov/historicaldocuments/frus1969-76v36/d342 (primary) | [S1] |
| `severity` | NULL | Proposed: leave NULL. Reasoning: the codebook's severity scale (1–5) is defined for disruptive events by expected barrels/day at risk; it gives no clear method for coding a partial, conditional *relief* event where the volume actually restored on March 18 specifically is not established by any source retrieved this session (Syria and Libya's continued embargo, and Algeria's provisional status, mean the true March-18 volume is smaller and unquantified). A null is the honest measurement here, not an omission. | [S1] |
| `surprise` | NULL | 2 — "widely expected; extensive warning or visible build-up." Reasoning: the lift had been under active, months-long negotiation since at least January 1974 [S2][S3], with a specific trigger event (the February 14 Tripoli meeting) already publicly anticipated [S3] — this was a visible, protracted build-up, not a surprise, even though its exact final date and partial scope were not fixed until the announcement itself. | [S1][S2][S3] |
| `confidence` | medium | medium (unchanged). Reasoning: only one primary source (S1) pins the exact March 18 date; S2 and S3 establish the lead-up but not the date itself, so this does not meet the codebook's "high" bar of multiple primary sources agreeing on the same fact. | [S1] |
| `date_precision` | day | day (unchanged) — supported directly by [S1]. | [S1] |
| `event_date` | 1974-03-18 | 1974-03-18 (unchanged) — directly confirmed by [S1]'s "yesterday" reference in a March 19 memo. | [S1] |

## Status

partial — fails (a): only one independent domain (history.state.gov, three documents) carries a primary source; the second domain present (nber.org, S4) does not corroborate the specific March 18 date or the Algeria/Syria/Libya details — it only supplies general context. No press source and no second primary-source domain were retrieved this session confirming the March 18 date or location (a repeatedly reported "Vienna" location could not be sourced this session and is explicitly not asserted above). It also fails (d) pending the three missing entities. Clauses (b) narrative, (c) knowable_at, (e) class, and (f) not-known-at-the-time are met.
