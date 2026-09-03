# Tripoli Agreement — Libya and the companies settle the Mediterranean terms     tripoli_agreement_1971 · 1971-04-02 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 88) | "Telegram From the Department of State to Certain Diplomatic Posts", subject "Libyan Oil Agreement" | Washington, April 2, 1971, 2311Z | https://history.state.gov/historicaldocuments/frus1969-76v36/d88 | 2026-09-03T02:3xZ (session) | "Oil Companies April 2 signed agreement with Libyans which will increase payments to Libyan government about 63 cents per barrel"; "New posted price (tax reference price) for 40 gravity oil will be 3.446 dollars up from 2.55 dollars per barrel"; "Oil companies have made similar offers to Iraq and Saudi Arabia for pipeline oil exported from Mediterranean."; "difference can be justified by location, transportation, gravity, and low sulphur advantages of Libyan crude" |
| S2 | primary — **same domain as S1** | U.S. Department of State, Office of the Historian (same volume, Doc. 87) | "Memorandum From the President's Assistant for National Security Affairs (Kissinger) to President Nixon" | Washington, March 27, 1971 | https://history.state.gov/historicaldocuments/frus1969-76v36/d87 | 2026-09-03T02:2xZ (session) | "Libya, which represents the Mediterranean countries, has demanded: —a substantial increase in the posted price of oil, on which taxes are based; —that the companies reinvest a portion of their profits in the producing countries" |

Both are primary and both are on history.state.gov, so this is **one** source domain under §1(a) and the record is partial. `docs/g/ROUTE_TESTS.md` records the second-domain routes tried this session.

## Narrative

On 2 April 1971 the oil companies signed an agreement with Libya, six weeks after the Gulf producers had settled at Tehran and on materially better terms. The State Department circulated the outcome to posts the same evening: the agreement "will increase payments to Libyan government about 63 cents per barrel", and the "New posted price (tax reference price) for 40 gravity oil will be 3.446 dollars up from 2.55 dollars per barrel" [S1] — a 35 % rise in the tax reference price, and roughly double the ~30¢ per barrel the Gulf states had obtained in February. Washington's own explanation of the gap was quality and geography rather than leverage: the "difference can be justified by location, transportation, gravity, and low sulphur advantages of Libyan crude" [S1]. The settlement did not stop at Libya. The same cable records that the companies "have made similar offers to Iraq and Saudi Arabia for pipeline oil exported from Mediterranean" [S1], which is the mechanism by which a Libyan term became a Mediterranean term. A week earlier the White House had described Libya as the state that "represents the Mediterranean countries" and had listed its demands as a posted-price increase and company reinvestment [S2].

## Knowable at

1971-04-02, day precision. Reason: the agreement was signed on 2 April and the State Department cable reporting it is timed the same day, 2311Z [S1]. Whether the terms were public that evening is not established by any source retrieved this session; what is established is that the United States government knew them on 2 April. `date_precision` stays `day`.

## Entities

- `country.libya` — actor — the signatory government [S1].
- `country.iraq`, `country.saudi_arabia` — affected — the states to which the same Mediterranean pipeline terms were then offered [S1].
- **Gap:** the register has no entity for an oil company; the counterparties in [S1] cannot be coded. Reported to Session A rather than invented.

## Class

Proposed class: `opec_decision`. Codebook clause: "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks". Libya was an OPEC member and this is the price-and-tax limb of that clause.
Alternative considered and rejected: `sanctions` ("Sanctions imposed, tightened, or lifted on a producer") — the coercion here runs from a producer to companies, not from anyone to a producer, and the v3 codebook amendment rule 2 puts producer self-management in `opec_decision`.
**Codebook gap:** as with Tehran, the clause names a *production* decision and this is a price decision. Recorded, not worked around; see `tehran_agreement_1971.md`.

## Not known at the time

That the Tehran/Tripoli settlements would be reopened within two years rather than holding to 1975; that Libya would move from price terms to expropriation (BP's holdings, later in 1971) and Iraq to outright nationalisation (June 1972, `iraq_ipc_nationalisation_1972.md`); and whether the "similar offers" to Iraq and Saudi Arabia for pipeline crude would be accepted [S1]. The posted-price figures in [S1] are tax reference prices, not transaction prices, and must not be stored as market prices.

## Proposed field changes

Not applicable — no row in `events`. If Joe admits it: `event_date` 1971-04-02; `date_precision` day; `type` opec_decision; `source_url` https://history.state.gov/historicaldocuments/frus1969-76v36/d88; `severity` **unknown** (no volumes are named in any source retrieved this session — the per-barrel figures are prices, not barrels); `surprise` **unknown**; `hostility` not applicable.

## Status

**partial — fails (a).** Two primary documents, one registrable domain, for the reason SPINE_REGISTRATION Amendment 2 registered in advance. Clauses (b)–(f) are met. This is the best-sourced of the three 1970–72 commercial records: the primary document is dated the **day of the event** and carries exact posted prices.
