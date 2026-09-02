# Iran-Iraq War begins     iran_iraq_war_1980 · 1980-09-22 · day · conflict_escalation

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian, *Foreign Relations of the United States, 1977–1980*, Volume XVIII, Middle East Region; Arabian Peninsula, Document 93 | Memorandum From the President's Assistant for National Security Affairs (Brzezinski) [to President Carter] | Washington, November 5, 1980 | https://history.state.gov/historicaldocuments/frus1977-80v18/d93 | 2026-09-02T20:44Z (session) | "On September 22, war between Iran and Iraq commenced with ground and air attacks on Iranian territory by Iraqi forces." (footnote); "the impact of the loss of Iraqi oil is yet to be felt"; "Saudi Arabia and others are helping make up for the Iraqi shortfall." |
| S2 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:30Z (session) | "1980-1981: Iran-Iraq War. Iranian production had returned to about half of its pre-revolutionary levels later in 1979, but was knocked out again when Iraq (second panel of Figure 11) launched a war against the country in September of 1980. The combined loss of production from the two countries again amounted to about 6% of world production at the time, though within a few months, this shortfall had been made up elsewhere (see Figure 13)." (p. 17 of the working paper as printed; local extracted copy `hamilton_w16790.txt`) |

S1 and S2 are on different registrable domains (history.state.gov vs. nber.org). S1 is primary — a contemporaneous U.S. government memorandum, though dated six weeks after the war's outbreak; S2 is a scholarly working paper, cited as secondary only per its own cover note that NBER working papers are not peer-reviewed.

## Narrative

On September 22, 1980, Iraq launched ground and air attacks on Iranian territory, opening the Iran-Iraq War [S1][S2]. Iraq's action came as Iran's oil production was still recovering from the 1978-79 revolution, at roughly half its pre-revolutionary level [S2]; Iraq's own output was then knocked out as well, and Hamilton estimates the combined loss from both countries at about 6% of world oil production at the time [S2]. A U.S. National Security Council memorandum written six weeks later, on November 5, 1980, records that "the impact of the loss of Iraqi oil is yet to be felt" but that "Saudi Arabia and others are helping make up for the Iraqi shortfall" [S1] — direct contemporaneous confirmation that outside producers were already offsetting the loss within weeks, consistent with Hamilton's later finding that the shortfall was "made up elsewhere" within a few months [S2]. What was known on the day: that Iraqi forces had struck Iranian territory by ground and air. What was not yet known on September 22 itself: the scale of the combined production loss (a figure only calculable after the fact, per S2) and whether or how quickly other producers would compensate — the only contemporaneous U.S. government assessment retrieved this session is dated six weeks later and already treats the offset as underway [S1].

## Knowable at

1980-09-22, day precision. Reason: this is the date on which Iraqi ground and air attacks on Iranian territory are recorded to have begun, per a footnote in a contemporaneous U.S. government memorandum [S1] and confirmed independently by Hamilton's chronology [S2]. No source retrieved this session gives a clock time or identifies the first wire report of the day, so no finer-than-day precision is claimed.

## Entities

- `country.iraq` — actor — "war between Iran and Iraq commenced with ... attacks on Iranian territory by Iraqi forces" [S1]; "Iraq ... launched a war against the country" [S2]. Matches the existing `event_entities` row.
- `country.iran` — target — the state whose territory was attacked, per both S1 and S2. Matches the existing `event_entities` row.

## Class

Proposed class: `conflict_escalation`, as currently coded. Codebook clause: "`conflict_escalation` | War, invasion, major military escalation involving a producer/transit state." Both Iraq and Iran were major OPEC oil producers at the time [S2], and this was a full war launched by one against the other, not a lesser skirmish — a clean, uncontested fit. No alternative class in the closed set is defensible.

## Not known at the time

On September 22, 1980, the eventual duration of the war (it lasted until 1988) and its full economic toll were unknown. The specific "about 6% of world production" combined-loss figure, and the fact that the shortfall would be "made up elsewhere" within a few months, are conclusions Hamilton draws with hindsight from a 2011 vantage point [S2] — they were not stated, and could not have been stated with that precision, on the day itself. The November 5, 1980 memorandum [S1], while contemporaneous to the broader autumn 1980 period, was still written more than a month after the war began and reflects six weeks of unfolding market response, not day-one knowledge.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.nber.org/papers/w16790 (secondary only) | https://history.state.gov/historicaldocuments/frus1977-80v18/d93 (primary) | [S1] |
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "On September 22, 1980, Iraq launched ground and air attacks on Iranian territory, opening the Iran-Iraq War; the combined loss of Iraqi and Iranian oil production has been estimated at about 6% of world production at the time, made up elsewhere within a few months." | [S1][S2] |
| `severity` | NULL | 5 — "systemic; a top producer or a critical chokepoint materially disrupted." Reasoning: this coding rests on the physical-stake figure in S2 (about 6% of world oil production knocked out, from two major Gulf producers simultaneously) and on S1's contemporaneous confirmation that the Iraqi shortfall specifically was material enough that other producers had to compensate — not on any price reaction. A case for 4 instead of 5 could be made on the grounds that the shortfall was absorbed within months [S2], but the initial simultaneous loss from two major producers is judged to meet the "top producer ... materially disrupted" bar. | [S1][S2] |
| `surprise` | NULL | Propose leaving NULL. Reasoning: no source retrieved this session states what oil-market participants expected on September 21, 1980, the day before the attack. Border skirmishes and Iraq's abrogation of the 1975 Algiers Accord in the days prior are widely reported in general histories, but this dossier retrieved no contemporaneous (day-before) primary or press source establishing the specific market expectation, so per the codebook's own rule ("code by what was publicly expected the day before, using contemporaneous reporting — never with hindsight"), a number is not proposed. This is a documented gap, not a finding of "fully expected." | — (gap; no source) |
| `date_precision` | day | day (unchanged) | [S1][S2] |
| `event_date` | 1980-09-22 | 1980-09-22 (unchanged) | [S1][S2] |

## Status

partial — fails clause (c)/(f) in a minor way and clause (a) in spirit: S1, the primary source, is dated November 5, 1980 (six weeks after the event) rather than September 22 or 23, 1980 — no source dated at or within a day or two of the event itself was located or retrieved this session, despite search attempts. The two-source/one-primary literal test is satisfied (S1 primary on history.state.gov, S2 secondary on nber.org, different domains). Narrative (b), entities (d), and class (e) are cleanly met. Surprise is left an explicit, documented NULL rather than guessed.
