# Iran-Iraq ceasefire (UN Resolution 598)     iran_iraq_ceasefire_1988 · 1988-08-20 · day · policy_response (contested — see Class)

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | United Nations Peacekeeping (official UN record) | "United Nations Iran-Iraq Military Observer Group (UNIIMOG) — Background" | undated official mission-history page, describing events of August 1988 | https://peacekeeping.un.org/sites/default/files/past/uniimogbackgr.html | 2026-09-02 (session; exact time not logged) | "The ceasefire came into effect at 0300 GMT on 20 August 1988." / "This was achieved on 8 August, when he announced the agreement of both Iran and Iraq to a ceasefire with effect from 0300 GMT on 20 August" / "In its resolution 619 (1988) of 9 August, the Security Council approved the Secretary-General's report and decided to establish UNIIMOG immediately" |
| S2 | press | United Press International (UPI Archives) | "Iraq charges Iranian ceasefire violations" | filed August 21, 1988, dateline "Manama, Bahrain" | https://www.upi.com/Archives/1988/08/21/Iraq-charges-Iranian-ceasefire-violations/6492588139200/ | 2026-09-02 (session; exact time not logged) | "Iran and Iraq exchanged charges Sunday of minor violations of a U.N.-negotiated cease-fire in the 8-year-old Persian Gulf war, but a U.N. official said the 2-day-old truce appeared to be holding." |

Domain independence: peacekeeping.un.org and upi.com are different registrable domains; S1 is primary (an official UN mission record), satisfying clause (a). Note: `digitallibrary.un.org` returned HTTP 403 this session as expected per SPINE_REGISTRATION.md §4, but the separate `peacekeeping.un.org` subdomain was reachable and yielded a primary UN source — this is a route not listed in the registration's tested table and is reported here as newly usable.

**A UN Security Council Resolution 598 full-text page (peacemaker.un.org) was also retrieved this session** confirming: adopted July 20, 1987; "Iran formally accepted the resolution on July 17, 1988... Iraq reaffirmed its agreement the following day (July 18, 1988)." This is not used as one of the two counted sources above (same `un.org` family as S1, so not an independent second domain), but it corroborates the timeline.

## Narrative

UN Security Council Resolution 598, adopted July 20, 1987, called for an immediate Iran-Iraq ceasefire. Iran did not accept it until July 17, 1988; Iraq reaffirmed acceptance July 18 [S1, corroborated by the UN Peacemaker resolution text retrieved but not counted as S1/S2]. On August 8, 1988, UN Secretary-General Javier Pérez de Cuéllar announced both governments' agreement to a ceasefire effective 0300 GMT on August 20, 1988 [S1]. The Security Council approved his report and established the UN Iran-Iraq Military Observer Group (UNIIMOG) on August 9 via Resolution 619 [S1]. The ceasefire took effect as scheduled at 0300 GMT August 20, ending nearly eight years of war [S1]. The next day, UPI reported both sides trading accusations of minor violations (an alleged sniper killing, a boarded merchant ship) while a UN observer, Capt. Gary Yazichuck, said the truce "appeared to be holding," with troops visibly unarmed under white flags [S2]. No source retrieved this session states a barrel-per-day figure for Iranian or Iraqi production restored or war-risk premium removed by the ceasefire; Hamilton (2011, NBER WP 16790) was checked this session and does not discuss the 1987-88 tanker war or this ceasefire specifically, so it is not cited here.

## Knowable at

Two distinct, both-sourced dates matter here, and this dossier flags the tension between them rather than picking one silently. The ceasefire's **effective date** was 1988-08-20, 0300 GMT [S1] — matching the current `event_date`. But the **announcement** that this would happen was made 1988-08-08, when the Secretary-General "announced the agreement of both Iran and Iraq to a ceasefire with effect from 0300 GMT on 20 August" [S1]. Per the codebook's own date rule — "event_date = the first day the market could have known... not the date the effect showed up" — a reasonably attentive market participant could have known on August 8 that hostilities would end on August 20. This dossier does not change `event_date` (that decision is Joe's) but flags it as the single most codebook-relevant finding in this batch.

## Entities

- `country.iran` — coded `actor`; `country.iraq` — coded `target`. This dossier flags the pairing as an imperfect fit: a mutual, UN-brokered ceasefire is not a unilateral action by one country against another, and "target" implies an adversarial object of action that neither retrieved source supports for Iraq specifically — both countries accepted the same resolution on consecutive days [S1, UN Peacemaker text]. Consider both `actor`, or a role better suited to mutual compliance, which does not exist in the codebook's four-role set (actor/target/location/affected_market).
- **Gap reported, not invented**: no `institution.un` (or `institution.un_security_council`) entity exists in the entity register as queried this session, despite the UN Secretary-General and Security Council being the actual drivers of the ceasefire's timing per S1. This is reported to Session A as a missing entity the register should probably have, given how many Gulf-era events involve UN Security Council action.

## Class

Proposed class as coded: `policy_response`. This dossier assesses the fit as **not supported** and says so rather than silently accepting it. Codebook clause (amendment 2026-07-23): "deliberate government/agency market interventions (e.g. coordinated SPR/IEA strategic-reserve releases). Severity = scale of the intervention." A ceasefire ending a war is not a market intervention in the sense the clause defines — no reserve was released, no production or price policy was set. None of the other five pre-registered classes (`chokepoint_disruption`, `opec_decision`, `sanctions`, `conflict_escalation`, `infrastructure_attack`, `demand_shock`) fit either: this event is the *cessation* of conflict, and the codebook has no class for de-escalation. This dossier recommends Joe treat this as an open codebook gap — flagged, not silently resolved by forcing it into `policy_response` or inventing a new type.

## Not known at the time

On August 20, 1988, it was not known whether the ceasefire would hold — UPI's next-day report already documents disputed violation claims from both sides within the truce's first two days [S2]. The subsequent Geneva peace talks (scheduled to begin August 25 per S2) had not occurred; the ultimate territorial and prisoner-of-war settlement took years and was not resolved by the ceasefire itself. UNIIMOG's eventual February 1991 termination date was not knowable in August 1988.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://www.eia.gov (bare site root) | https://peacekeeping.un.org/sites/default/files/past/uniimogbackgr.html | [S1] |
| `type` | policy_response | flagged as unsupported by the retrieved evidence; no replacement proposed because no class in the closed set fits a ceasefire/de-escalation event — recommend Joe and Session A discuss a codebook amendment rather than this dossier picking one | [S1] |
| `event_date` | 1988-08-20 | not changed here, but flagged: 1988-08-08 (Secretary-General's announcement) is arguably the codebook-correct "first day the market could have known" date, versus 1988-08-20 as the date "the effect showed up" — the codebook explicitly says to use the former, not the latter | [S1] |
| `entities: country.iraq:target` | target | flagged as an imperfect fit for a mutual ceasefire; consider `actor` | [S1] |
| `entities` | (no UN institution entity) | gap reported to Session A: `institution.un` does not exist in the register | — |

## Status

partial — fails clause (e): the coded class (`policy_response`) is not supported by the codebook's own definition, and no better-fitting class exists in the closed set, so this is an unresolved codebook gap rather than a sourcing failure. Clause (a) is met (two independent domains, one primary — S1). Clauses (b), (c), (d), and (f) are addressed above, with (c) flagging a specific, sourced tension between the announcement date (Aug 8) and the effective date (Aug 20) that bears directly on the codebook's own date rule.
