# Tehran Agreement — the six Gulf OPEC states settle with the companies     tehran_agreement_1971 · 1971-02-14 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 86) | "Memorandum From C. Fred Bergsten of the National Security Council Staff to the President's Assistant for National Security Affairs (Kissinger)" | Washington, March 9, 1971 | https://history.state.gov/historicaldocuments/frus1969-76v36/d86 | 2026-09-03T02:3xZ (session) | "State's memorandum (Tab A) informs you of the details of an agreement signed on February 14 between the six Persian Gulf members of the Organization of Exporting Countries (OPEC)."; "Payments by the companies to the governments will increase about 30¢ per barrel in 1971 (from the current rate in the Gulf of about 95¢ to about $1.25) and about 50¢ per barrel by 1975 to reach a total of about $1.45."; "Total revenue to the Persian Gulf states will increase by about $1.4 billion in 1971 as a result of the settlement, and by nearly $12 billion over the five-year period."; "The agreement applies only to crude oil exported directly from terminals in the Persian Gulf." |
| S2 | primary — **same domain as S1** | U.S. Department of State, Office of the Historian (same volume, Doc. 87) | "Memorandum From the President's Assistant for National Security Affairs (Kissinger) to President Nixon" | Washington, March 27, 1971 | https://history.state.gov/historicaldocuments/frus1969-76v36/d87 | 2026-09-03T02:2xZ (session) | references "the Tehran agreement" and "companies and Persian Gulf producers in Tehran"; "Libya, which represents the Mediterranean countries, has demanded: —a substantial increase in the posted price of oil, on which taxes are based; —that the companies reinvest a portion of their profits in the producing countries" |

Both documents are primary and both are on history.state.gov. Under SPINE_REGISTRATION §1(a) — "Independent means different publishers, not two pages of one site" — this is **one** source domain, and the record is partial for that reason. Routes tried for a second domain and their results are in `docs/g/ROUTE_TESTS.md`.

## Narrative

On 14 February 1971 the six Persian Gulf members of OPEC signed an agreement with the international oil companies [S1]. Its terms were quantified for the White House three weeks later: company payments to the governments would rise "about 30¢ per barrel in 1971 (from the current rate in the Gulf of about 95¢ to about $1.25)" and by "about 50¢ per barrel by 1975 to reach a total of about $1.45", worth "about $1.4 billion in 1971" and "nearly $12 billion over the five-year period" [S1]. The agreement was deliberately partial in geography: it "applies only to crude oil exported directly from terminals in the Persian Gulf" [S1], which left the Mediterranean outlets — Libyan crude and the pipeline barrels from Iraq and Saudi Arabia — outside it and set up the second negotiation. That was live and unsettled at the end of March, with Libya "which represents the Mediterranean countries" demanding "a substantial increase in the posted price of oil, on which taxes are based" and company reinvestment in the producing countries [S2]. No source retrieved this session gives the Gulf posted price before or after 14 February, or the volume of crude covered, so neither is asserted.

## Knowable at

1971-02-14, day precision. Reason: the agreement's signature date is stated as a fact in a primary US government document — "an agreement signed on February 14" [S1]. The document itself is dated 9 March 1971, so what is established is the date of the event, not that its terms were publicly known on the day. No source retrieved this session establishes when the terms were published, so a market-knowability timestamp is not claimed and `date_precision` stays `day` on the signature.

## Entities

- `country.iran`, `country.iraq`, `country.saudi_arabia`, `country.kuwait` — actor — four of the six Gulf OPEC signatories, named collectively in [S1] as "the six Persian Gulf members of the Organization of Exporting Countries (OPEC)". **Caveat:** [S1] does not enumerate the six; these four are the register-named Gulf OPEC members of 1971 and the mapping is inference from the register, not from the source. Qatar and Abu Dhabi/UAE are the other two by the same inference and are flagged below.
- **Gap:** the register has no entity for an oil company, and none for Qatar or the United Arab Emirates. Reported to Session A rather than invented.

## Class

Proposed class: `opec_decision`. Codebook clause: "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks" — an agreement concluded by six OPEC members acting together over the price and tax terms of their crude is the price limb of that clause, and the source names OPEC explicitly [S1].
Alternative considered: `policy_response` ("deliberate government/agency market interventions"), rejected because the codebook defines it by consumer-government examples and the actors here are producer governments.
**Codebook gap, reported rather than worked around:** the clause says "production decision", and this is a *price and tax* decision with no production term. It is being classed `opec_decision` by elimination. See the same note in `libya_posted_price_confrontation_1970.md`; Session G recommends a v3 codebook question to Joe and Session E rather than deciding it here.

## Not known at the time

That the Mediterranean producers would extract better terms seven weeks later at Tripoli, and that the Gulf agreement's five-year horizon would not survive two. [S1]'s revenue figures are projections over 1971–1975 made in March 1971, not measurements, and must not be stored as measured values (INV-5 in spirit: an inferred value and a measured value are not the same column). Whether the settlement would hold at all was open: the whole point of the Mediterranean exclusion was that a second, harder negotiation was still to come [S2].

## Proposed field changes

Not applicable — no row in `events`. If Joe admits it: `event_date` 1971-02-14; `date_precision` day; `type` opec_decision; `source_url` https://history.state.gov/historicaldocuments/frus1969-76v36/d86; `severity` **unknown** (no barrels are named in any source retrieved this session); `surprise` **unknown**; `hostility` not applicable.

## Status

**partial — fails (a).** Two primary documents, one registrable domain. This is the OPEC-sourcing failure SPINE_REGISTRATION Amendment 2 registered in advance; `docs/g/ROUTE_TESTS.md` records the routes tried this session and what each returned. Clauses (b)–(f) are met.
