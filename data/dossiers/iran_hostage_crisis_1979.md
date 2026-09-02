# US embassy hostage crisis begins in Tehran     iran_hostage_crisis_1979 · 1979-11-04 · day · conflict_escalation

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1977–1980, Vol. XI, Part 1, *Iran: Hostage Crisis, November 1979–September 1980*, Doc. 1) | Memorandum From the President's Assistant for National Security Affairs (Brzezinski) to President Carter, Subject: "Takeover of Embassy Tehran" | Washington, November 4, 1979 | https://history.state.gov/historicaldocuments/frus1977-80v11p1/d1 | 2026-09-02T20:31Z (session) | "[T]he students penetrated the security barricades within the Embassy and have apparently taken the Embassy duty personnel hostage, tying their hands behind their backs." The demonstrators' own characterization, reported in the memo: "a peaceful sit-in demonstration." Additionally reported by the document, in substance rather than as an exact quotation retrieved this session: roughly 3,000 Iranian student demonstrators were involved; Chargé Laingen was away from the Embassy at the Iranian Foreign Ministry at the time; the memo was transmitted the same day while President Carter was at Camp David. |
| S2 | primary | U.S. National Archives and Records Administration, Federal Register codification | Executive Order 12170, "Blocking Iranian Government Property" | November 14, 1979 | https://www.archives.gov/federal-register/codification/executive-order/12170.html | 2026-09-02T20:32Z (session) | "I, JIMMY CARTER, President of the United States, find that the situation in Iran constitutes an unusual and extraordinary threat to the national security, foreign policy and economy of the United States and hereby declare a national emergency to deal with that threat." The order blocks "all property and interests in property of the Government of Iran, its instrumentalities and controlled entities and the Central Bank of Iran." |

S1 (history.state.gov) and S2 (archives.gov) are on different registrable domains and both are primary contemporaneous U.S. government records. S1 is dated the day of the event itself; S2 is dated ten days later and documents the U.S. government's formal emergency response rather than the seizure itself, but independently corroborates that "the situation in Iran" was, by November 14, treated by the President as an ongoing national-security emergency traceable to the Embassy takeover.

## Narrative

On the morning of November 4, 1979, Iranian students occupied the U.S. Embassy in Tehran; per the same-day memorandum National Security Advisor Brzezinski sent President Carter, the students "penetrated the security barricades within the Embassy and have apparently taken the Embassy duty personnel hostage, tying their hands behind their backs," while themselves describing their action as "a peaceful sit-in demonstration" [S1]. The memo reports the demonstrators as numbering roughly 3,000 and records that Chargé d'Affaires Bruce Laingen was not in the Embassy at the time, being at the Iranian Foreign Ministry, and that the memo itself was relayed to Carter, then at Camp David, the same day [S1]. Ten days later, Carter formally found that "the situation in Iran constitutes an unusual and extraordinary threat to the national security, foreign policy and economy of the United States," declaring a national emergency and blocking "all property and interests in property of the Government of Iran" and its central bank [S2] — an asset-freeze response, not itself a description of the November 4 seizure, but independent confirmation that the U.S. government treated the takeover as the origin of a major, ongoing state-level crisis. What was known within hours on November 4 was that hostages had been taken and the Embassy's normal channel (Laingen) was unavailable; not yet known was how many hostages, for how long, or what Iran's government would do in response.

## Knowable at

**1979-11-04, day precision.** S1 is a document dated the day of the event itself, describing events "that morning" in Tehran and relayed to Washington the same day [S1] — this is as close to first-knowledge as a retrieved document gets in this dossier. No source retrieved this session gives an exact clock time for the seizure itself in Tehran (only that Brzezinski's memo reporting it was itself in circulation in Washington that day), so no finer-than-day precision beyond "November 4" is claimed.

## Entities

- `country.iran` — actor — per the existing `event_entities` rows; the students are described throughout S1 as Iranian, and S2 addresses "the Government of Iran" directly as the entity whose property is blocked in response.
- `country.usa` — target — per the existing `event_entities` rows; the U.S. Embassy and its personnel are the object of the action in S1, and S2 is a U.S. government emergency response protecting U.S. national security and economic interests.

## Class

Proposed class: `conflict_escalation`. Codebook clause: "War, invasion, major military escalation involving a producer/transit state." This is the cleanest fit of the five events in this batch: the seizure of a foreign embassy and its personnel by nationals acting within a producer state, followed by that state's government declining to intervene to release them, is a direct state-to-state escalation, corroborated by the U.S. government's own contemporaneous framing of it as a "national emergency" and "extraordinary threat" [S2]. No alternative class in the closed set fits better — it is not a chokepoint disruption, an OPEC decision, an infrastructure attack, or a demand shock, and while `sanctions` names the U.S. response (S2 is itself an economic-sanctions instrument), the *event* being coded is the seizure, not the sanction.

## Not known at the time

On November 4 itself, per S1, the exact number of hostages was not yet specified beyond "Embassy duty personnel" being held, and the demonstrators' own claim to be conducting a "peaceful sit-in" was contemporaneously reported without being verified or accepted at face value. Not known on November 4: that the crisis would last 444 days, that it would not be resolved by negotiation for over a year, or the full economic-sanctions response that followed — S2, dated ten days later, is itself part of that unfolding response and is not evidence of what was known on November 4.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.eia.gov (bare site root, not a document, per SPINE_REGISTRATION.md §4/AUDIT) | https://history.state.gov/historicaldocuments/frus1977-80v11p1/d1 (primary, same-day) | [S1] |
| `confidence` | medium | high — two independent primary sources, mutually consistent, one dated the day of the event itself ("multiple primary sources agree," per the codebook's top confidence tier). | [S1][S2] |
| `severity` | NULL | Not proposed with a specific number. Neither retrieved source quantifies a barrels-per-day or export-volume figure at risk from the Embassy seizure itself — this event is fundamentally diplomatic/political rather than a direct physical-supply event, and this dossier does not invent a trade-unit figure to satisfy the codebook's severity framing where none was retrieved. A future session should look for contemporaneous EIA or IEA assessments of Iranian export status specifically as of November 1979 before proposing a number. | — |
| `surprise` | NULL | Not proposed. No source retrieved this session documents what was publicly expected about an embassy seizure the day before, November 3 — the codebook requires day-before public expectation, not hindsight, and this dossier does not have that source. | — |

## Status

**partial — fails only the severity/surprise numeric coding (f is otherwise met; a, b, c, d, and e are met).** Two independent-domain primary sources were retrieved, one dated the event's own day; the narrative carries a `[Sn]` marker on every claim (with the ~3,000-demonstrator figure and Laingen's location explicitly marked as paraphrased-from-source rather than verbatim quotation, since this session's fetch of S1 returned those facts in indirect rather than quoted form); `knowable_at` is set to day precision on strong evidence; entities and class are both clean fits. This is the best-sourced dossier in this batch. What remains open is a quantified severity code, which would require a source this session did not retrieve.
