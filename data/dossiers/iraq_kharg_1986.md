# Iraqi air raid on Iran's Sirri Island oil terminal     iraq_kharg_1986 · 1986-08-12 · day · infrastructure_attack

**Note on event_id / title mismatch:** the database `event_id` is `iraq_kharg_1986` and the task brief describes it as "Iraqi strikes on Iranian export infrastructure," but the current `events.title` in the database is "Iraqi raids on Iran's Sirri Island oil terminal" — Sirri Island, not Kharg Island. Every source retrieved this session confirms the August 12, 1986 raid targeted **Sirri Island**, a separate Iranian export facility roughly 800 km southeast of Kharg. This dossier researches the Sirri Island event as titled in the database, and flags the `event_id` itself as misleading.

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | press (wire) | *The Christian Science Monitor*, carrying a Reuters wire report | "Iraqi jets hit crucial Iranian oil terminal" (byline: Reuters) | November 26, 1986 | https://www.csmonitor.com/1986/1126/ofill26.html | 2026-09-02T21:07Z (session) | "The Larak Island installations were thought to be out of Iraqi range until Aug. 12, when a devastating raid on Sirri Island, some 110 nautical miles farther inside the Gulf, forced the Iran to shift its operations to Larak." "Since the stepped-up Iraqi raids in August, Iranian oil exports have been significantly reduced." |
| S2 | secondary (scholarly monograph) | Center for Strategic and International Studies (Anthony H. Cordesman and Abraham R. Wagner) | *The Lessons of Modern War, Volume II: The Iran-Iraq War*, Chapter VII, §7.8 "Iraq Again Escalates the Air War" | May 1990 | https://csis-website-prod.s3.amazonaws.com/s3fs-public/legacy_files/files/media/csis/pubs/9005lessonsiraniraqii-chap07.pdf | 2026-09-02T20:52Z (session, retrieved for a companion dossier and reused here for directly relevant context) | "Iran also created an effective tanker shuttle. It leased six tankers and started to shuttle oil on its own vessels between Kharg and Sirri Island which was well over 800 kilometers further away from Iraq. Iran felt that Iraq's Exocet attacks were largely limited to the area south and immediately east of Kharg Island and that Sirri would be beyond the range of Iraqi attack aircraft." |

S1 and S2 are on different registrable domains (csmonitor.com vs. csis-website-prod.s3.amazonaws.com). Neither is primary: S1 is a contemporaneous wire report republished by a newspaper (press tier, filed roughly 3.5 months after the event, in a story primarily about a later, November 25, 1986 strike on Larak); S2 is a scholarly monograph written with hindsight in 1990. **No primary source was located or retrieved this session** — see failed-attempt log below.

## Retrieval attempts that failed or were unusable

- FRUS 1981–1988, Vols. XX and XXI — both "Being Cleared," not published (established researching companion dossiers this session).
- upi.com/Archives/1986/08/12/Iraqi-planes-bomb-Sirri-Island/... — a wire piece with a matching date, surfaced by search; HTTP 403 on fetch.
- CIA FOIA Electronic Reading Room — resolves only to the homepage.
- CSIS chapter 8 of the same monograph ("Phase Five: New Iranian Efforts at 'Final Offensives,' 1986-1987") was fetched in an attempt to find a direct, contemporaneous-to-1986 account of the Sirri raid; the PDF's text could not be reliably extracted by the fetch tool and was not read in full given time constraints, so no quote from it is used here.
- No American Presidency Project statement on this specific incident was located.

## Narrative

By the second half of 1985 Iran had built a tanker shuttle carrying crude from Kharg Island to Sirri Island, roughly 800 km further from Iraq, because it "felt that Iraq's Exocet attacks were largely limited to the area south and immediately east of Kharg Island and that Sirri would be beyond the range of Iraqi attack aircraft" [S2]. That assumption held until 12 August 1986, when Iraq struck Sirri directly. A contemporaneous wire report later described "the Larak Island installations were thought to be out of Iraqi range until Aug. 12, when a devastating raid on Sirri Island ... forced the Iran to shift its operations to Larak" [S1]. The raid therefore demonstrated that Iraqi aircraft could reach a facility Iran had chosen precisely because it was thought unreachable, and forced a second relocation further from Iraq. The same report notes that "since the stepped-up Iraqi raids in August, Iranian oil exports have been significantly reduced" [S1], though no barrel figure for that reduction was retrieved this session. Known on 12 August 1986: Iraqi aircraft had struck the Sirri Island terminal, an installation built on the premise of being beyond Iraqi reach [S1][S2]. Not established here: the aircraft type, squadron, or damage and casualty figures for that day, since S1 discusses the raid only in retrospect and S2's retrieved passage predates it.

## Knowable at

1986-08-12, day precision. Reason: S1, though written in November 1986, explicitly dates the Sirri raid to "Aug. 12." No source retrieved this session gives a time of day or names the first wire report of August 12 itself, so no finer-than-day precision is claimed.

## Entities

- `country.iraq` — actor — the attacking party, per S1 ("Iraqi jets," in the context of Sirri and the companion Larak raid) and consistent with S2's account of Iraqi Exocet campaigns against Iran's export shuttle. Matches the existing `event_entities` row.
- `country.iran` — target — Sirri Island was Iran's alternate export terminal, per S1 and S2. Matches the existing `event_entities` row.

## Class

Proposed class: `infrastructure_attack`, as currently coded. Codebook clause: "`infrastructure_attack` | Direct strike on production, refining, or export infrastructure." A direct air strike on an export oil terminal is a clean, uncontested fit.

## Not known at the time

On August 12, 1986, it was not yet known that Iran would go on to relocate its shuttle a second time, to Larak Island, or that Iraq would extend its reach even that far by November 25, 1986 — S1's own account frames the November raid on Larak as remarkable specifically because Larak "was thought to be out of Iraqi range," a belief the August 12 Sirri raid should arguably have already undermined but evidently had not fully dispelled by November. This dossier does not treat the November 1986 Larak strike as knowable from the August 12 Sirri event.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `event_id` | `iraq_kharg_1986` | Flag to Joe: the id references Kharg, but every retrieved source and the current `events.title` describe a strike on **Sirri Island**, a different facility roughly 800 km away. Recommend renaming to something like `iraq_sirri_1986` in a future migration, or confirming Joe intends `iraq_kharg_1986` as a legacy/arbitrary identifier unrelated to its content. | [S1][S2] |
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "On August 12, 1986, Iraqi aircraft struck Iran's Sirri Island oil export terminal — a facility Iran had built specifically because it believed it was beyond Iraqi aircraft range — forcing Iran to relocate its export shuttle again, to Larak Island; Iranian oil exports were significantly reduced following the August raids." | [S1][S2] |
| `severity` | NULL | 4 — "major producer/route affected; multi-week disruption plausible." Reasoning: S1 states Iranian oil exports were "significantly reduced" following the raids and that Iran had to relocate its entire alternate-export operation to a still more distant island — a major route disruption for a top-tier producer's export logistics, though no specific barrel figure was retrieved to support a higher (systemic) code. | [S1] |
| `surprise` | NULL | 4 — "unexpected; a real break from expectations." Reasoning: S2 directly documents that Iran selected Sirri specifically on the premise that it "would be beyond the range of Iraqi attack aircraft" — a stated, source-attested expectation that the August 12 raid broke. This is a case where the "day before" expectation is unusually well evidenced (via S2's account of why Sirri was chosen at all, established by mid-1985), even though S2 predates the August 1986 raid itself. | [S1][S2] |
| `date_precision` | day | day (unchanged) | [S1] |

## Status

partial — fails clause (a): no primary source was located or retrieved this session (UPI's contemporaneous August 12, 1986 wire item was found by search but returned HTTP 403 on every fetch attempt; FRUS volumes for this period are unpublished; CIA reading room unusable). Two independent-domain secondary/press sources (S1, S2) are present and corroborate the underlying fact pattern. Narrative (b), knowable_at (c), entities (d), and class (e) are well supported. The `event_id`/title mismatch is a separate data-quality issue flagged for Joe, not a sourcing failure.
