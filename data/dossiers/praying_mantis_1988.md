# US Navy Operation Praying Mantis strikes Iranian oil platforms     praying_mantis_1988 · 1988-04-18 · day · conflict_escalation

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | The American Presidency Project (UC Santa Barbara), reproducing the official text of Reagan's report to Congress | "Letter to the Speaker of the House of Representatives and the President Pro Tempore of the Senate on the United States Military Strike in the Persian Gulf" | April 19, 1988 | https://www.presidency.ucsb.edu/documents/letter-the-speaker-the-house-representatives-and-the-president-pro-tempore-the-senate-5 | 2026-09-02 (session; exact time not logged) | "On April 14, 1988, the USS SAMUEL B. ROBERTS struck a mine in international waters of the Persian Gulf." / "In response to this attack on the ROBERTS and commencing at approximately 1:00 a.m. (EDT), April 18, 1988, Armed Forces of the United States assigned to the Joint Task Force Middle East...attacked and effectively neutralized the Sassan and Sirri Platforms." / "U.S. Forces were attacked by the Iranian PTG JOSHAN, FFG SAHAND, and FFG SABALAN. In response to these attacks, U.S. Forces severely damaged or sank the Iranian vessels." |
| S2 | secondary, scholarly/professional legal commentary | American Society of International Law, *ASIL Insights*, Vol. 8, Issue 25 | "The World Court Finds that U.S. Attacks on Iranian Oil Platforms in 1987-1988 Were Not Justifiable as Self-Defense, but the United States Did Not Violate the Applicable Treaty with Iran," by Pieter H.F. Bekker | published November 11, 2003 | https://asil.org/insights/volume-8-issue-25-2/ (**note**: the URL in the database, `https://www.asil.org/insights/volume/8/issue/25/world-court-finds-us-attacks-iranian-oil-platforms-1987-1988-were-not`, now 404s/redirects to an unrelated 2004 ASIL Insight on Slobodan Milošević's right of self-representation — confirmed by fetching it this session; the article actually about Oil Platforms lives at the URL given here) | 2026-09-02 (session; exact time not logged) | "On April 14, 1988, the U.S. frigate Samuel B. Roberts struck a mine in international waters near Bahrain. Five days later, the U.S. attacked and destroyed the Nasr and Salman platforms belonging to the National Iranian Oil Company." / "the Court found that... the attacks against Iranian oil installations carried out by U.S. forces in 1987-1988 could not be justified, under Article XX(1)(d) of the Treaty, as being necessary to protect the essential security interests of the U.S." |

Domain independence: presidency.ucsb.edu and asil.org are different registrable domains; S1 is primary (a Presidential report to Congress), satisfying clause (a). **Important sourcing correction:** the database's current `source_url` for this event is dead/misdirected and does not resolve to the cited article; the working URL is recorded above.

**Discrepancy not resolved:** S1 (Reagan's letter, dated the day after the strike) names the "Sassan and Sirri Platforms" struck at ~1:00 a.m. EDT April 18. S2 (built on the ICJ's later judgment) names the "Nasr and Salman platforms," struck "five days" after the April 14 mining — i.e., April 19. These may be the same installations under U.S. military versus Iranian/ICJ naming conventions, or a genuine date/target discrepancy between the contemporaneous U.S. report and the later international-legal record; this dossier does not adjudicate it and reports both readings.

## Narrative

On April 14, 1988, the U.S. frigate Samuel B. Roberts struck a mine in international waters of the Persian Gulf near Bahrain [S1][S2]. In response, at approximately 1:00 a.m. EDT on April 18 (per Reagan's report) — or, per the ICJ record synthesized in S2, "five days later" — U.S. forces of the Joint Task Force Middle East attacked and destroyed Iranian oil platforms, named "Sassan and Sirri" in Reagan's letter and "Nasr and Salman" in the ASIL account [S1][S2]. Iranian naval vessels (the Joshan, Sahand, and Sabalan) engaged U.S. forces and were "severely damaged or sank" [S1]. The operation, code-named Praying Mantis, was the U.S.'s second platform strike in six months, following an October 1987 attack on the Rashadat complex after the Sea Isle City missile strike [S2]. Physically, the stake was narrow: the ICJ later found the targeted platforms were, at the time of both 1987 and 1988 strikes, either under repair and inoperative or subject to a standing U.S. embargo on Iranian oil and services, meaning no direct U.S.–Iran oil commerce flowed through them that day [S2]. What was known April 18: a U.S. retaliatory strike had destroyed named Iranian platforms and damaged Iranian naval assets, days after a mine had struck a U.S. warship.

## Knowable at

1988-04-18, ~0100 EDT (~0500 UTC), per Reagan's official report citing that as the strike's commencement time [S1]. Reason: this is the U.S. government's own contemporaneous account of when hostilities began; no same-day (April 18) wire or press report was retrieved and quoted this session to independently corroborate same-day public knowledge, so the knowable_at time rests on S1 alone.

## Entities

- `country.usa` — actor — confirmed [S1].
- `country.iran` — target — confirmed; platforms and naval vessels were the objects of the U.S. strike [S1][S2].
- `commodity.brent` — affected_market — plausible as the standard international benchmark for a Gulf-oil-adjacent event, but not independently confirmed by either retrieved source naming a specific benchmark.

## Class

Proposed class as coded: `conflict_escalation`. Codebook clause: "War, invasion, major military escalation involving a producer/transit state." Well supported: this was a direct naval engagement between U.S. and Iranian forces involving sunk/damaged warships, inside an active war (the Iran-Iraq/Tanker War) [S1][S2].

Severity (coded 2, "localized, small volumes, easily substituted"): supported, and arguably generously coded even at 2 — S2's synthesis of the ICJ judgment establishes the struck platforms were inoperative or already embargoed at the time of both 1987 and 1988 strikes, meaning the *expected* physical disruption to oil actually reaching market was minimal [S2].

Surprise (coded 3, "plausible but not consensus"): this dossier flags a case for a lower value. The October 1987 Rashadat strike had already established a clear U.S. retaliation pattern (Iranian attack on shipping → U.S. platform strike) six months earlier [S2]; a retaliatory strike following the April 14 Roberts mining fits a precedent the market had already seen once. That argues for something closer to "2 — widely expected," not "3." Not silently changed here.

## Not known at the time

The ICJ's eventual finding — that the U.S. strikes were an unlawful use of force not justified as self-defense, though not a treaty violation — was not known or even litigated until Iran filed suit in 1992 and the Court ruled in 2003, 15 years later [S2]. Whether the Iranian naval vessels sunk that day (Joshan, and the disputed fate of Sahand and Sabalan) were fully destroyed versus damaged, and the platforms' exact operational status, were not settled in real time by any source retrieved this session.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.asil.org/insights/volume/8/issue/25/world-court-finds-us-attacks-iranian-oil-platforms-1987-1988-were-not (dead/misdirected) | https://asil.org/insights/volume-8-issue-25-2/ | [S2] |
| `severity` | 2 | keep — supported, arguably generous given inoperative-platform finding | [S2] |
| `surprise` | 3 | flag as possibly overstated given the October 1987 precedent; do not silently change | [S2] |

## Status

complete — two independent-domain sources retrieved, one primary (S1) and one scholarly secondary built on a primary legal judgment (S2); narrative, knowable_at, entities, class, and "not known at the time" clauses are all supported by retrieved, quoted material. The unresolved platform-naming/date discrepancy between S1 and S2 is disclosed above rather than silently resolved, and the source_url correction is flagged for Joe's patch review.
