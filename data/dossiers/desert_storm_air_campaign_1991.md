# Coalition air campaign begins against Iraq (Operation Desert Storm)     desert_storm_air_campaign_1991 · 1991-01-17 · day · conflict_escalation

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | The American Presidency Project (UC Santa Barbara), address by President George H.W. Bush | "Address to the Nation Announcing Allied Military Action in the Persian Gulf" | January 16, 1991, 9:01 p.m. | https://www.presidency.ucsb.edu/documents/address-the-nation-announcing-allied-military-action-the-persian-gulf | 2026-09-02 (session; exact time not logged) | "Just 2 hours ago, allied air forces began an attack on military targets in Iraq and Kuwait." / "These attacks continue as I speak. Ground forces are not engaged." / action "taken in accord with United Nations resolutions and with the consent of the United States Congress" |
| S2 | secondary | U.S. Department of State, Office of the Historian | "The Gulf War, 1991" (Milestones in the History of U.S. Foreign Relations, 1989–1992) | undated retrospective essay | https://history.state.gov/milestones/1989-1992/gulf-war | 2026-09-02 (session; exact time not logged) | "The result was UN Resolution 678, which authorized the use of force to compel Iraq to withdraw from Kuwait, but gave Iraq a forty-five day grace period to withdraw." / "After the deadline for withdrawal passed, the coalition led by the United States attacked Iraq by air." / the essay dates the air campaign's start as "January 16, 1991" |

Domain independence: presidency.ucsb.edu and history.state.gov are different registrable domains. S1 is a primary, contemporaneous document (the President's own address, delivered as the strikes were underway); S2 is a retrospective Office of the Historian essay (undated, written after the fact) and is treated as secondary, not primary, satisfying clause (a)'s two-source/one-primary minimum without resting on it for the primary leg.

**Not retrieved this session, despite attempts:** unscr.com/en/resolutions/678/ (HTTP 403, repeated); congress.gov (bill text and overview pages, HTTP 403, repeated) for the January 12–14, 1991 Authorization for Use of Military Force Against Iraq (Pub. L. 102-1); govinfo.gov's scanned Statutes-at-Large PDF for the same law (image-only PDF, no extractable text this session); upi.com/Archives (HTTP 403 on every URL tried this session, including the exact URL cited as working in the iran_iraq_ceasefire_1988 dossire, indicating the route is currently blocked, not that this specific article is unavailable); nber.org/papers/w16790 abstract page mentions "the first Persian Gulf War in 1990-91" only in passing, with no January 1991 detail, and the PDF fetch returned unreadable binary/image content this session. None of these are cited.

## Narrative

On January 16, 1991, at 9:01 p.m., President George H.W. Bush addressed the nation to announce that "allied air forces began an attack on military targets in Iraq and Kuwait" roughly two hours earlier, with ground forces not yet engaged [S1]. The action followed UN Security Council Resolution 678, which had authorized force and "gave Iraq a forty-five day grace period to withdraw" from Kuwait, a deadline that expired January 15, 1991 [S2]. Bush stated the strikes were "taken in accord with United Nations resolutions and with the consent of the United States Congress" [S1], reflecting that both international and domestic authorization had already been secured before the attack began. The physical stake was the continued Iraqi occupation of Kuwait and, with it, Kuwaiti and regional Gulf crude output and transit; neither retrieved source states a barrels-per-day figure for this specific date. Because the 45-day deadline had been public since late November 1990, the fact that force could follow noncompliance was broadly telegraphed [S2]; the precise hour of the first strikes was still new information when Bush spoke [S1].

## Knowable at

1991-01-16, 9:01 p.m. (with market-relevant effect on the 1991-01-17 trading day), day precision. Reason: Bush's address is the first confirmed public statement that strikes had begun, delivered after the ~2-hour-old "began" strikes he described [S1]; S2 separately dates the campaign's onset to "January 16, 1991" [S2]. U.S. equity and most oil-futures markets had closed hours before the 9:01 p.m. ET address, so the fact reached most exchange-based trading only at the next open; overnight and Asia/Europe markets could have known before their local opens on January 17. `event_date` = 1991-01-17 (unchanged) is consistent with this if it reflects the first full trading day the news was priced globally; the codebook's own instruction to "note in description" a post-close release applies here and is not currently reflected in the description field.

## Entities

- `country.usa` — actor — confirmed: Bush states the attack was launched by "allied air forces" under U.S. presidential authority and with "the consent of the United States Congress" [S1].
- `country.iraq` — target — confirmed: "attack on military targets in Iraq" [S1].
- `country.kuwait` — currently coded `location`; S1's own text names Kuwait among the places struck ("military targets in Iraq and Kuwait" [S1]), which is consistent with `location` (Iraqi occupying forces inside Kuwaiti territory were themselves targets) but is not itself evidence for a stronger `target` coding; not proposed to change without further sourcing.
- **Gap, reported not invented:** no `institution.un` or `institution.un_security_council` entity exists in the register, despite Resolution 678's deadline being the operative legal trigger named in S2. No coalition-partner entities (UK, France, Saudi Arabia as an active belligerent, etc.) exist as separate `actor` roles in this event's current entity set; not added here since S1/S2 do not individually name them as I retrieved the text.

## Class

Proposed class: `conflict_escalation` (unchanged). Codebook clause: "`conflict_escalation` | War, invasion, major military escalation involving a producer/transit state." The launch of a large-scale coalition air campaign against Iraq, an OPEC producer occupying Kuwait, is unambiguously a major military escalation; no other closed-set class fits as well (`sanctions` and `opec_decision` do not describe kinetic military action). No alternative class considered necessary.

## Not known at the time

On January 16–17, 1991, the duration and outcome of the air campaign, the subsequent ground war (which did not begin until late February), and the scale of the Kuwaiti oil-well fires Iraqi forces would later set (a separate, later event in this corpus) were not yet known. Neither retrieved source gives a contemporaneous barrels-per-day estimate of Kuwaiti or Iraqi output at risk as of January 16–17 specifically; that quantification is not established by this dossier's sources and is not asserted.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `description` | "DRAFT coding, awaiting Joe's review" language retained in current description | Drop the "DRAFT coding" language once Joe reviews this dossier; substantively, current description ("US-led coalition begins the air war on Iraq after the Jan 15 UN withdrawal deadline...") is supported by [S1][S2] and needs no factual change | [S1][S2] |
| `severity` | 5 | unchanged — 5 ("systemic; a top producer or a critical chokepoint materially disrupted") is plausible given a top producer (Iraq) and an occupied producer (Kuwait) both under direct military attack, but neither retrieved source gives a contemporaneous bpd-at-risk figure to confirm the top of the scale; flagged as supported by category but not by a quantified figure in what was retrieved this session | [S1][S2] |
| `surprise` | 2 | unchanged — 2 ("widely expected; extensive warning or visible build-up") is supported: the 45-day grace period from Resolution 678 was public since late November 1990 and its January 15 deadline had already passed two days before the attack began [S2], meaning that force following noncompliance was broadly anticipated even though the exact hour of the first strikes was new information [S1] | [S2] |
| `source_url` | https://www.presidency.ucsb.edu/documents/address-the-nation-announcing-allied-military-action-the-persian-gulf | unchanged | [S1] |
| `event_date` | 1991-01-17 | unchanged, but flag: Bush's address was delivered 9:01 p.m. ET January 16 describing strikes as already ~2 hours underway [S1]; S2 also dates the campaign's start to "January 16, 1991" [S2]. Day precision on Jan 17 is defensible only as "the first day most trading venues could act on the news"; recommend the `description` field note the post-close timing per the codebook's own instruction | [S1][S2] |
| `date_precision` | day | unchanged | [S1][S2] |

## Status

partial — fails (a) in spirit though not in letter: two independent domains are present (presidency.ucsb.edu, history.state.gov) with one primary (S1), meeting the minimum, but no press source and no second primary/official document (UN resolution text, congressional authorization) could be retrieved this session — unscr.com, congress.gov, govinfo.gov's scanned statute, and upi.com all failed or returned unreadable content on every attempt. Clauses (b) narrative, (c) knowable_at, (d) entities (with a reported gap), (e) class, and (f) not-known-at-the-time are met on the sources actually retrieved.
