# Iraqi forces set fire to Kuwaiti oil wells     kuwait_oil_fires_1991 · 1991-02-22 · day · infrastructure_attack

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | Public Papers of the Presidents of the United States: George H. W. Bush, 1991, Book I (via govinfo.gov, U.S. Government Publishing Office) | "Remarks on the Persian Gulf Conflict" | February 22, 1991, 10:43 a.m. | https://www.govinfo.gov/content/pkg/PPP-1991-book1/html/PPP-1991-book1-doc-pg165.htm | 2026-09-02 (session; exact time not logged) | "Saddam has now launched a scorched-earth policy against Kuwait, anticipating perhaps that he will now be forced to leave. He is wantonly setting fires to and destroying the oil wells, the oil tanks, the export terminals, and other installations of that small country." |
| S2 | secondary | U.S. Department of Defense, Office of the Special Assistant to the Deputy Secretary of Defense for Gulf War Illnesses (OSAGWI) | "Environmental Exposure Report: Oil Well Fires" | originally published November 1998; this version "Last Update: August 2, 2000" (retrospective, not contemporaneous) | https://www.gulflink.osd.mil/owf_ii/owf_ii_s03.htm and https://www.gulflink.osd.mil/owf_ii/owf_ii_s01.htm | 2026-09-02 (session; exact time not logged) | "Iraq ignited or damaged more than 750 of Kuwait's 943 oil wells distributed among eight fields." / "the actual destruction of Kuwait's oil wells, coinciding with Coalition forces' air strikes, began on January 16, 1991." / "approximately 4-6 million barrels of crude oil and 70-100 million cubic meters of natural gas per day" were being burned. / "By late 1990, intelligence and other sources indicated that should Iraq's forces face the threat of forced ejection from Kuwait, Iraq would implement a 'scorched earth' policy toward Kuwait's oil infrastructure." |

Domain independence: govinfo.gov and gulflink.osd.mil are different registrable domains. S1 is a primary, contemporaneous presidential record; S2 is an official DoD report but was compiled and published years after the event (1998, updated 2000), so it is classed secondary/official-retrospective under this dossier's reading of clause (a), not primary. Clause (a)'s two-source/one-primary minimum is met.

**UPI Archives could not be retrieved this session.** Three UPI URLs surfaced by search as directly on point — a Feb. 22, 1991 wire ("Bush gives Iraq until noon Saturday to leave Kuwait"), a Feb. 25, 1991 wire, and a Nov. 6, 1991 wire on the fires being extinguished — all returned HTTP 403 on WebFetch this session. SPINE_REGISTRATION.md Amendment 1 records upi.com/Archives as a working route (tested July/August 1988 wires); this session's repeated 403s on 1991 URLs are reported as a possible route regression, not treated as evidence UPI never worked.

## Narrative

On February 22, 1991, President Bush announced that Iraq had "launched a scorched-earth policy against Kuwait," "wantonly setting fires to and destroying the oil wells, the oil tanks, the export terminals, and other installations" [S1] — this is the day the U.S. government publicly confirmed, in real time, that Kuwait's oil production system was being deliberately destroyed. A later DoD retrospective report states the physical destruction of wells actually began January 16, 1991, coincident with the start of the coalition air campaign, and escalated as Iraqi forces retreated in late February; ultimately more than 750 of Kuwait's 943 wells were ignited or damaged, burning an estimated 4-6 million barrels of crude oil per day at the peak [S2]. The same report states that "by late 1990," U.S. intelligence already anticipated Iraq would resort to a scorched-earth policy on its oil infrastructure if faced with forced ejection [S2] — the general threat, though not its exact start date, was foreseen months in advance. What officials and the public knew specifically on February 22 was Bush's own confirmation that the campaign of destruction was underway that day [S1]; the eventual scale (750-of-943 wells, months of fires) is a figure this dossier can source only from the 1998/2000 retrospective [S2], not from anything contemporaneous to February 22 itself.

## Knowable at

1991-02-22, day precision, per Bush's same-day public remarks confirming the scorched-earth policy was underway [S1] — this matches the current `event_date`. This dossier flags a real tension, not resolved here: [S2] states the wells' physical destruction "began on January 16, 1991," coincident with the opening of the air campaign, seven days before Bush's February 22 statement first named it publicly to this dossier's sources. If a market participant could have learned of well destruction before February 22 through some contemporaneous channel, the codebook's date rule ("the first day the market could have known") could point earlier than February 22 — but no source retrieved this session establishes an earlier public disclosure date, so day precision on February 22 is retained on the strength of [S1] alone.

## Entities

- `country.iraq` — actor — matches current coding; supported by [S1] ("Saddam has now launched...He is wantonly setting fires").
- `country.kuwait` — target — matches current coding; supported by [S1] ("against Kuwait") and [S2] (Kuwait's wells).
- `commodity.brent` — affected_market — retained; no source retrieved this session gives a contract-specific figure, only physical barrels burned [S2].
- No entity gap identified this session.

## Class

Proposed class: `infrastructure_attack` (unchanged). Codebook clause: "`infrastructure_attack` | Direct strike on production, refining, or export infrastructure." [S1] directly supports this: Iraq is described as "setting fires to and destroying the oil wells, the oil tanks, the export terminals" — production (wells), storage (tanks), and export (terminals) infrastructure all named. No other closed-set class fits as well; `conflict_escalation` was considered and rejected because the codebook's mechanism for that class (war/invasion/military escalation) is already coded separately for the broader Gulf War, and this record's distinguishing fact is the infrastructure destruction itself.

## Not known at the time

The eventual total (more than 750 of Kuwait's 943 wells ignited or damaged) and the burn-rate estimate (4-6 million barrels of crude and 70-100 million cubic meters of gas per day) are figures this dossier can source only to the 1998/2000 DoD retrospective [S2], not to anything contemporaneous with February 22, 1991; on the day itself, only the fact that a systematic campaign of destruction was underway was public [S1], not its ultimate scope. How long the fires would burn, and how much Kuwaiti export capacity would be restored and when, were not established by February 22 (this dossier did not retrieve a source for the fires' actual end date and does not assert one).

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://en.wikipedia.org/wiki/Kuwaiti_oil_fires | https://www.govinfo.gov/content/pkg/PPP-1991-book1/html/PPP-1991-book1-doc-pg165.htm | [S1] |
| `severity` | 4 | unchanged — evidence supports 4 ("Major producer/route affected; multi-week disruption plausible"). [S2]'s >750-of-943-wells and multi-month duration are consistent with 4; this dossier does not find grounds in the retrieved sources to argue for 5 ("systemic... a top producer... materially disrupted"), since Kuwait's pre-war output (~1.5-2 mb/d) was a meaningful but not top-tier share of contemporaneous world supply, and [S2]'s 4-6 mb/d figure is a fire's fuel-consumption estimate, not a stated lost-export-capacity figure. | [S1][S2] |
| `surprise` | 2 | unchanged — evidence supports 2 ("widely expected; extensive warning or visible build-up"). [S2]: intelligence "by late 1990" anticipated a conditional scorched-earth policy; this is exactly the "extensive warning" the 2-level describes, not a "genuine shock" (4-5) or "fully anticipated... scheduled" (1). | [S2] |
| `date_precision` | day | unchanged | [S1] |
| `event_date` | 1991-02-22 | not changed here, but flagged: [S2] dates the physical start of well destruction to 1991-01-16, seven days before the February 22 date this dossier's only contemporaneous source [S1] confirms publicly. No source retrieved this session establishes a public disclosure date earlier than February 22, so this dossier does not propose a change, only flags the tension for Joe. | [S1][S2] |
| `confidence` | (not queried this session) | medium — one contemporaneous primary source [S1] plus one non-contemporaneous but authoritative official secondary source [S2]; no independent press corroboration was obtainable this session (UPI blocked, see Sources). | [S1][S2] |

## Status

partial — fails the spirit, though not the letter, of clause (a): two independent domains are present with one primary [S1] and one secondary [S2], meeting the stated minimum, but no contemporaneous press source could be retrieved this session (UPI Archives, a route SPINE_REGISTRATION.md records as working, returned HTTP 403 on every 1991 URL tried) and the only truly primary, contemporaneous source is a single document [S1]. Clauses (b) narrative, (c) knowable_at (with an explicitly flagged, unresolved date tension), (d) entities, (e) class, and (f) not-known-at-the-time are met.
