# Iraq's mid-August 1985 air raids on Kharg Island's T-Jetty loading terminal     kharg_strikes_1985 · 1985-08-15 (see date challenge below) · day · infrastructure_attack

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | secondary (scholarly monograph) | Center for Strategic and International Studies (Anthony H. Cordesman and Abraham R. Wagner) | *The Lessons of Modern War, Volume II: The Iran-Iraq War*, Chapter VII, §7.8 "Iraq Again Escalates the Air War" | May 1990 | https://csis-website-prod.s3.amazonaws.com/s3fs-public/legacy_files/files/media/csis/pubs/9005lessonsiraniraqii-chap07.pdf | 2026-09-02T20:52Z (session) | "In mid-August, however, Iraq began a far more serious set of attacks on Kharg Island whose timing strongly indicates they were a response to the new 'Sirri Shuttle'. These air raids began on August 14. While the new attacks did not damage Iran's newly repaired Sea Island terminal, they did seriously damage the main offshore loading point of 'T-Jetty.' They were followed by another major attack on 25 August, and may have temporarily cut Kharg's export capacity by about 30 percent."; "Iran felt that Iraq's Exocet attacks were largely limited to the area south and immediately east of Kharg Island and that Sirri would be beyond the range of Iraqi attack aircraft."; "Nearly 90 percent of Iran's wartime oil exports had to be exported from Kharg Island, and this made it a key target." |

**Only one source, on one registrable domain, was retrieved this session.** This dossier fails clause (a) outright (not merely "in spirit") — no second independent domain and no primary source were obtained, despite the attempts logged below.

## Retrieval attempts that failed or were unusable

- FRUS 1981–1988, Vol. XX and Vol. XXI (Iran/Iraq) — both "Being Cleared," not published (as established researching `tanker_war_1984`; the finding applies here too).
- CIA FOIA Electronic Reading Room, including a specific-looking search hit — resolves only to the Reading Room homepage on fetch, no document text obtainable.
- upi.com/Archives/1985/08/25/... (an August 25, 1985 UPI wire item on a second Kharg raid, surfaced by search) — HTTP 403.
- digital.bentley.umich.edu (a digitized *Michigan Daily* page from the relevant date range, likely reprinting AP/UPI wire copy) — HTTP 403, both on the direct page and its "download_text" variant.
- www.globalsecurity.org/military/world/iran/kharg.htm — HTTP 403.
- Christian Science Monitor site search for an August 1985 Kharg article — no matching article found in this session's search results (csmonitor.com is confirmed reachable in general, since it was used successfully for `carter_doctrine_1980` and `iraq_kharg_1986`, but no August 1985 Kharg-specific article surfaced).
- American Presidency Project — no Reagan statement on this specific incident located.

## Narrative

By spring/summer 1985, Iran had built an alternate export route — the "Sirri Shuttle" — to work around Iraqi Exocet attacks concentrated near Kharg Island, on the reasoning that Sirri Island, roughly 800 km further from Iraq, would be "beyond the range of Iraqi attack aircraft" [S1]. Iraq had mostly avoided direct strikes on Kharg itself before this, with a single symbolic raid on May 30, 1985 [S1]. In mid-August 1985, that changed: Iraq opened a new, more serious bombing campaign against Kharg's loading terminal, which Cordesman and Wagner assess was "a response to the new 'Sirri Shuttle'" [S1]. The raids "began on August 14" by this source's account, seriously damaged the main "T-Jetty" offshore loading point (though not the separately repaired Sea Island terminal), and were followed by a second major raid on August 25 — together assessed as having "temporarily cut Kharg's export capacity by about 30 percent" [S1]. The physical stake was substantial: Kharg handled "nearly 90 percent of Iran's wartime oil exports" [S1], making it, in Cordesman and Wagner's words, "a key target." What was known in mid-August 1985: Iraq had resumed serious strikes on Iran's primary export terminal after months of relative restraint toward Kharg itself. What is not established by the single source retrieved this session: the exact calendar date within the August 14–15 window most consistent with the database's current `1985-08-15` coding, or any independent, contemporaneous confirmation of the raid or its effects.

## Knowable at

Contested — see below. S1 gives "August 14" as the date the raids began, which does not match the database's current `1985-08-15`. This dossier could not resolve the one-day discrepancy from the single source retrieved this session: it may reflect a genuine difference between when the raid occurred (S1's "August 14") and when it was announced or reported in the Gulf/international press (potentially a day later given time-zone and wire-cycle effects), but no second source was retrieved to adjudicate this. Recommendation: treat `event_date` as uncertain within a two-day window (1985-08-14 to 1985-08-15) pending a second, independently retrieved source, rather than asserting either date as settled.

## Entities

- `country.iraq` — actor — the attacking party per S1. Matches the existing `event_entities` row.
- `country.iran` — target — Kharg Island is Iran's terminal, and Iran built the Sirri Shuttle specifically in response to the ongoing threat to Kharg [S1]. Matches the existing `event_entities` row.

## Class

Proposed class: `infrastructure_attack`, as currently coded. Codebook clause: "`infrastructure_attack` | Direct strike on production, refining, or export infrastructure." S1 describes a direct air strike on Kharg's "T-Jetty" offshore loading point — export infrastructure in the codebook's own terms — a clean, uncontested fit.

## Not known at the time

In mid-August 1985, it was not yet known how sustained this new phase of attacks on Kharg would be; S1's own account shows Iraq going on to hit Kharg "at least 37 different times" by mid-November and "nearly 60 major air strikes" by the end of 1985, with a single raid on September 19 cutting export production by up to 50% — an escalation not knowable from the August 14/15 raid alone. Also not known at the time: S1's later analysis (drawing on Wharton Econometrics and Petroleum Finance Company work) that Iranian oil exports were, over the full year, "far more affected by the growing world oil glut than by Iraqi bombing" — a retrospective judgment about relative causes, not a fact available in August 1985.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `event_date` | 1985-08-15 | Do not change without a second source. If forced to choose from the single source retrieved this session, 1985-08-14 is what S1 states, but this dossier does not recommend overwriting the current value on a single secondary source alone. | [S1] — single source, flagged as insufficient to patch |
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "Iraq opened a new, more serious phase of air raids on Kharg Island's export terminal in mid-August 1985 (a source retrieved this session dates the start to August 14), seriously damaging the 'T-Jetty' loading point and temporarily cutting Kharg's export capacity by an estimated 30 percent; assessed as a response to Iran's newly established 'Sirri Shuttle' alternate export route." | [S1] |
| `severity` | NULL | 3 — "meaningful volumes at risk; partial disruption plausible." Reasoning: S1's own figure is a *temporary* ~30% cut to Kharg's export capacity from the August 14/25 raids specifically (as distinct from the fuller campaign's later, larger effects in September–November) — meaningful but partial and temporary, on the source's own characterization ("temporarily cut"). A case for 4 could be made given Kharg's ~90% share of Iran's wartime exports, but this dossier codes the August event itself, not the campaign's eventual cumulative effect. | [S1] |
| `surprise` | NULL | Propose leaving NULL. Reasoning: no source retrieved this session states what was expected in Gulf shipping/oil circles on August 13, 1985, the day before. S1's own framing ("timing strongly indicates they were a response to the new 'Sirri Shuttle'") is the author's later analytical inference about Iraqi motive, not a contemporaneous day-before expectation, and Iran's own strategic bet — that Sirri put its alternate shuttle "beyond the range of Iraqi attack aircraft" — was about the Sirri route, not about whether Kharg itself would be struck again after months of restraint. Coding surprise from this would risk conflating two different questions. | — (gap; no source) |
| `date_precision` | day | day, but flag the unresolved one-day discrepancy above | [S1] |

## Status

partial — fails clause (a) outright: only one source, on one domain, was retrieved this session, despite seven distinct additional-route attempts (FRUS x2, CIA reading room, UPI, Bentley digital newspapers, globalsecurity.org, CSMonitor site search, American Presidency Project) all failing or returning nothing usable. The narrative (b) and class (e) are supportable from the single source available; knowable_at (c) is explicitly left contested due to an unresolved one-day date discrepancy between the source and the current database value; entities (d) are supported. Severity is proposed with reasoning; surprise is left an honest, documented NULL.
