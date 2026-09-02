# Tanker Bridgeton strikes Iranian mine in first Earnest Will convoy     bridgeton_mine_strike_1987 · 1987-07-24 · day · chokepoint_disruption

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | eyewitness/participant account (contested as "primary" — see note below) | U.S. Naval Institute, *Proceedings* | "SS Bridgeton: The First Convoy" — interview with Capt. Frank C. Seitz, Jr., U.S. Merchant Marine, by Naval Institute editor Paul Stillwell | May 1988, Vol. 114/5/1,023 (interview conducted "recently" before publication, i.e. roughly 10 months after the event) | https://www.usni.org/magazines/proceedings/1988/may/ss-bridgeton-first-convoy | 2026-09-02 (session; exact time not logged) | "It felt like a 500-ton hammer hit us up forward." / "It was an M-08, a 1908 Russian design, bottom-moored, floating contact mine with contact horns, chemical horns, and a 115-kilogram charge." / "there had been four other minings before us" |
| S2 | press | United Press International (UPI Archives) | "The supertanker Bridgeton hit an underwater mine Friday morning..." | filed July 24, 1987, dateline "Aboard the USS Kidd in the Persian Gulf" | https://www.upi.com/Archives/1987/07/24/The-supertanker-Bridgeton-hit-an-underwater-mine-Friday-morning/4397554097600/ | 2026-09-02 (session; exact time not logged) | "The tanker hit the mine shortly before 7 a.m. local time as it was steaming about 120 miles southeast of Kuwait." / "'We've been hit. We've been hit,' he told the Kidd." / "The track record, however, would clearly point the finger to Iran." |

Domain independence: usni.org and upi.com are different registrable domains. **Primary-source status is contested and flagged rather than silently resolved.** SPINE_REGISTRATION.md §1(a) defines primary as "a document produced by a participant or an official body at the time." S1 is produced by a direct participant (the ship's master) but published roughly 10 months after the event, not "at the time" — it is a retrospective interview, not a contemporaneous record. S2 is contemporaneous (filed same day) but is press, which the registration explicitly says "is a legitimate second source and never the only one." Read strictly, neither retrieved source is unambiguously primary-and-contemporaneous; this dossier does not paper over that and marks the record partial on clause (a) below rather than asserting completeness.

## Narrative

At approximately 6:51 a.m. local Gulf time on July 24, 1987, the reflagged U.S. supertanker Bridgeton — 401,382 deadweight tons — struck a moored contact mine roughly 18 miles west of Farsi Island while leading the first Operation Earnest Will convoy toward Kuwait, escorted by the destroyer Kidd and frigates Fox and Crommelin [S1][S2]. Master Frank Seitz felt "a 500-ton hammer" and radioed "we've been hit, we've been hit" [S1][S2]. The blast tore a hole roughly ten meters by five meters below the waterline; shrapnel penetrated the main deck some 90 feet away [S1]. There were no injuries among the 26–31 people aboard, and the tanker — under Navy assessment reduced to about 85% cargo capacity — completed the voyage to Kuwait [S1][S2]. Responsibility was not established that day: Navy officers called it "not immediately known" but said the pattern — an M-08 mine matching four earlier strikes near the same waters — "clearly point[ed] the finger to Iran" [S1][S2]. What was known on July 24: a tanker had been mined near a known Iranian Revolutionary Guard staging point, damaging but not disabling it, days after the U.S. escort mission began. What was not yet established: formal, non-circumstantial attribution to Iran.

## Knowable at

1987-07-24, ~0651 local Gulf time (approximately 0351 UTC). Reason: UPI's wire, filed same-day from aboard the escorting USS Kidd, reports the explosion at "shortly before 7 a.m. local time" [S2]; this is a contemporaneous eyewitness/wire report, giving the finest precision retrieved this session.

## Entities

- `chokepoint.hormuz` — coded `location`. This dossier flags a geographic precision concern rather than proposing a change: the mine strike occurred near Farsi Island, roughly 120 miles southeast of Kuwait and well inside the Gulf proper [S2] — not at the Strait of Hormuz itself, which lies at the Gulf's southeastern mouth. No more precise entity_id (e.g. for Farsi Island or "Persian Gulf" generally, as distinct from the Hormuz chokepoint) exists in the entity register as queried this session. Reported as a gap for Session A rather than invented.
- `commodity.wti` — coded `affected_market`. Plausible but not independently confirmed by any source retrieved this session (neither S1 nor S2 names a specific benchmark).
- `country.iran` — coded `actor`. Supported only as a strong circumstantial attribution in both sources ("clearly point the finger to Iran" [S2]; Seitz's account that Farsi Island-based Iranians had "a very high chance of hitting us" [S1]) — not a confirmed claim of responsibility by Iran itself. This dossier affirms the role as reasonably supported by the codebook's evidentiary bar but notes the attribution was inferential on the day, which belongs in "Not known at the time" below.

## Class

Proposed class as coded: `chokepoint_disruption`. Codebook clause: "Transit through a strait/canal/pipeline is threatened or blocked." A mine strike on an escorted tanker in the Gulf's shipping channel is a direct, physical act of the kind this clause describes — well supported by S1 and S2.

Severity (coded 3, "meaningful volumes at risk; partial disruption plausible"): supported. A single major tanker was damaged (not sunk, not the chokepoint itself blocked), consistent with 3 rather than 4–5; the vessel continued its voyage at reduced capacity [S1][S2].

Surprise (coded 3, "plausible but not consensus; a live possibility"): the evidence is closer to the boundary between 2 and 3 than the audit's flat "3" suggests. Both sources show Navy officers explicitly and repeatedly worried about exactly this scenario the day before — Capt. Mathis is quoted (per S1's companion reporting referenced in the interview) worrying about "this strip of water," and four prior mine strikes on other vessels in the same waters were already known [S1]. That pattern arguably supports "2 — widely expected; extensive warning or visible build-up" as much as "3." This dossier does not silently change the value but flags it as a borderline, defensible-either-way call.

## Not known at the time

Formal responsibility for the mine was not established July 24 — it rested on circumstantial evidence (mine type, proximity to a known Iranian staging point) rather than a claim or forensic confirmation [S1][S2]. The extent of underwater hull damage was not known until divers surveyed it in Kuwait days later [S1]. Whether the escort concept itself would be judged to have "worked" (tanker survived, mission continued) versus "failed" (the very first convoy was hit) was contested in real time and is a matter of interpretation, not fact, on the day.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.usni.org/magazines/proceedings/1988/may/ss-bridgeton-first-convoy | keep, but add https://www.upi.com/Archives/1987/07/24/The-supertanker-Bridgeton-hit-an-underwater-mine-Friday-morning/4397554097600/ as a second, contemporaneous source | [S2] |
| `severity` | 3 | keep — supported | [S1][S2] |
| `surprise` | 3 | flag as borderline 2–3; do not silently change | [S1] |

## Status

partial — fails clause (a) on a strict reading: no source retrieved this session is unambiguously both primary (participant/official-body document) and contemporaneous ("at the time") — S1 is a participant account published ~10 months later; S2 is contemporaneous but explicitly press, not primary, under the registration's own text. Clauses (b), (c), (d), (e), and (f) are otherwise met, with the caveats on entity/geographic precision and the surprise-score boundary noted above.
