# Libya's posted-price confrontation with the oil companies     libya_posted_price_confrontation_1970 · 1970-09-23 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 55) | "Telegram From the Embassy in Libya to the Department of State" | Tripoli, September 23, 1970, 2148Z | https://history.state.gov/historicaldocuments/frus1969-76v36/d55 | 2026-09-03T02:1xZ (session) | "Libyans are not bluffing. They have already assured, through deals with Oxy and three American partners Oasis, production of approximately 1.5 mbd."; "it seems to us almost certain that, in confrontation with majors acting in concert, LARG would promptly force shut-in of their production—probably halting all operations which they control. This would mean a loss of about 1.5 mbd."; "only action LARG has taken is to block shipments of crude for which Shell is consignor, i.e. ban exports of Shell 'owned' crude." |
| S2 | secondary — **context only, does not name Libya** | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/system/files/working_papers/w16790/w16790.pdf | 2026-09-03T02:2xZ (session; text extracted locally) | "The rupture of the Trans-Arabian pipeline in May 1970 in Syria may have helped precipitate a second 8% jump in the nominal price of oil later that year." |

| S3 | secondary (scholarly working paper) | Oxford Institute for Energy Studies (Bassam Fattouh, *An Anatomy of the Crude Oil Pricing System*, WPM 40) | *An Anatomy of the Crude Oil Pricing System* | January 2011 | https://ora.ox.ac.uk/objects/uuid:8b957970-239c-4a4f-9cbe-21830381de16/files/m79290fef21a26a470deac8273cda795f | 2026-09-03T03:1xZ (session; PDF retrieved and text extracted locally) | "In September 1970 the Libyan government reached an agreement with Occidental in which this independent oil company agreed to pay income taxes on the basis of increased posted price and to make retroactive payment to compensate for the lost revenue since 1965. Occidental was the ideal company to pressurise: unlike the majors, it relied heavily on Libyan production and did not have much access to oil in other parts of the world. Soon afterwards, all other companies operating in Libya submitted to these new terms."; "Other developments in the early 1970s, such as Libya’s production cutbacks and the sabotage of the Saudi Tapline in Syria, tightened further the supply-demand balance." |

S1 is primary and on history.state.gov; **S3 is on ora.ox.ac.uk, a second registrable domain, and it does attest
this event** — a settlement in September 1970 between the Libyan government and Occidental on an increased posted
price, with the other companies following. Under §1(a) a scholarly working paper may serve as the second source and
never as the primary; S1 is the primary. S2 is on nber.org — a second registrable domain — but it does **not** attest the Libyan confrontation; it attests only that the nominal oil price rose about 8 % later in 1970 and attributes that to a different cause. It is therefore not accepted as corroboration of this event, and the record is marked partial accordingly rather than rounded up.

## Narrative

By late September 1970 the Libyan Arab Republic Government was forcing the oil companies operating in Libya to accept higher posted prices, and the US embassy in Tripoli judged the threat credible: "Libyans are not bluffing. They have already assured, through deals with Oxy and three American partners Oasis, production of approximately 1.5 mbd" [S1]. The physical stake was stated in the trade's units: if the majors resisted in concert, the embassy expected the government "would promptly force shut-in of their production—probably halting all operations which they control. This would mean a loss of about 1.5 mbd" [S1]. The coercion actually in force was narrower: "only action LARG has taken is to block shipments of crude for which Shell is consignor, i.e. ban exports of Shell 'owned' crude" [S1]. What was known on the day was an asymmetry: a government that had already settled with the independents and could shut in the majors, against companies weighing whether resistance would make Tripoli "pause and finally shrink from all out confrontation" [S1]. The confrontation the embassy was weighing settled that month: Libya "reached an agreement with Occidental in which this independent oil company agreed to pay income taxes on the basis of increased posted price", after which "all other companies operating in Libya submitted to these new terms" [S3]. Separately, and on a different cause, the nominal price rose about 8 % later in 1970 [S2]. No source retrieved states Libya's posted price before or after, so no price figure is asserted.

## Knowable at

1970-09-23, day precision — and this is a **floor, not the event's onset**. Reason: the earliest dated document retrieved this session that establishes the confrontation is the Tripoli embassy telegram of 23 September 1970, 2148Z [S1]. The telegram plainly describes a situation already under way (the Occidental and Oasis settlements are in the past tense, and the Shell export ban is in force), so the true first-knowability is earlier. No source retrieved this session dates the Libyan demands, the Occidental settlement, or the Shell ban, so an earlier date would be a guess and is not entered. If this record is admitted, `knowable_at` should be revisited when a document from earlier in 1970 is retrieved.

## Entities

- `country.libya` — actor — the Libyan Arab Republic Government, "LARG" throughout [S1].
- `chokepoint.libya_es_sider` — affected_market — the register's Libyan export point; the crude at issue is Libyan export crude [S1]. **Caveat:** [S1] names no terminal, so this mapping is the register's nearest asset and not a sourced fact; it should be dropped if Joe prefers strict sourcing.
- `country.united_states` — affected — the "three American partners Oasis" and Occidental are US companies [S1].
- **Gap:** the register has no entity for an oil company. Occidental, the Oasis partners and Shell are the counterparties in [S1] and cannot be coded. Reported to Session A rather than invented.

## Class

Proposed class: `opec_decision`. Codebook clause: "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks". Libya was an OPEC member and the event is a producer government's decision over production and price terms, with a shut-in explicitly in prospect [S1]. The v3 codebook amendment of 2026-09-02 rule 2 points the same way: "A producer restricting its own exports to manage its own market is `opec_decision`, not `sanctions`."
Alternative considered: `policy_response` ("deliberate government/agency market interventions"), which is defined in the codebook by consumer-government examples (SPR/IEA releases) and fits poorly. Tie-break stated: `opec_decision` is chosen because the actor is a producer government acting on its own output.
**Codebook gap, reported rather than worked around:** the closed set has no class for a host-government/concession-holder dispute — a posted-price fight, a participation demand or a nationalisation. Every 1970–1973 episode of that shape is being pushed into `opec_decision` by elimination. Session G recommends this to Joe and Session E as a v3 codebook question; it is not decided here.

## Not known at the time

Whether the majors would concede or be shut in; whether a Libyan success would be copied by the Gulf producers (it was, at Tehran five months later); and the size of the price increase that would follow. The 1.5 mb/d figure in [S1] is a US embassy estimate of what *could* be lost, written in the conditional, not a realised loss — a distinction that must survive into any severity coding. The 8 % price rise of late 1970 [S2] was neither known on 23 September nor, on the only source retrieved, attributed to Libya.

## Proposed field changes

Not applicable — no row in `events`. If Joe admits it: `event_date` 1970-09-23 (a floor, see Knowable at); `date_precision` day; `type` opec_decision; `source_url` https://history.state.gov/historicaldocuments/frus1969-76v36/d55; `severity` **unknown** — the 1.5 mb/d in [S1] is conditional on a confrontation that did not occur in that form, and coding severity from it would present a contingency as a measurement; `surprise` **unknown**; `hostility` not applicable (`opec_decision` is one of the three classes the codebook exempts).

## Status

**complete** (upgraded 2026-09-03 from `partial — fails (a)`; the earlier status is preserved below).
(a) two independent registrable domains — `history.state.gov` (primary, contemporaneous, S1) and `ora.ox.ac.uk`
(scholarly secondary, S3) — with the primary requirement met by S1; (b)–(f) were already met.
**Corroboration strength, stated:** S3 is retrospective (2011) and substantive on this event: it names the month,
the counterparty (Occidental), the mechanism (income tax on an increased posted price, with retroactive payment)
and the sequel (the other companies following). It does **not** corroborate the 1.5 mb/d figure, which remains
S1's conditional estimate alone.

*Superseded status, 2026-09-03, kept as the record: "partial — fails (a). One primary source on one registrable
domain. The only second domain retrieved this session (nber.org, [S2]) does not mention Libya and cannot
corroborate the event." That conclusion was reached without testing `ora.ox.ac.uk`, a route Session E had already
proven working. The error was the search's, not the archive's; see `docs/g/ROUTE_TESTS.md` §"What the second pass
changed".*
