# Tripoli Agreement — Libya and the companies settle the Mediterranean terms     tripoli_agreement_1971 · 1971-04-02 · day · opec_decision
*Session G candidate dossier. This event is NOT in `events`. Nothing enters `events` without Joe's admit line (SPINE_REGISTRATION §3).*

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 88) | "Telegram From the Department of State to Certain Diplomatic Posts", subject "Libyan Oil Agreement" | Washington, April 2, 1971, 2311Z | https://history.state.gov/historicaldocuments/frus1969-76v36/d88 | 2026-09-03T02:3xZ (session) | "Oil Companies April 2 signed agreement with Libyans which will increase payments to Libyan government about 63 cents per barrel"; "New posted price (tax reference price) for 40 gravity oil will be 3.446 dollars up from 2.55 dollars per barrel"; "Oil companies have made similar offers to Iraq and Saudi Arabia for pipeline oil exported from Mediterranean."; "difference can be justified by location, transportation, gravity, and low sulphur advantages of Libyan crude" |
| S2 | primary — **same domain as S1** | U.S. Department of State, Office of the Historian (same volume, Doc. 87) | "Memorandum From the President's Assistant for National Security Affairs (Kissinger) to President Nixon" | Washington, March 27, 1971 | https://history.state.gov/historicaldocuments/frus1969-76v36/d87 | 2026-09-03T02:2xZ (session) | "Libya, which represents the Mediterranean countries, has demanded: —a substantial increase in the posted price of oil, on which taxes are based; —that the companies reinvest a portion of their profits in the producing countries" |

| S3 | secondary (retrospective journal article) | Middle East Research and Information Project, *MERIP Reports* No. 120 (Michael Renner) | "Restructuring the World Energy Industry" | January 26, 1984 | https://www.merip.org/1984/01/restructuring-the-world-energy-industry/ | 2026-09-03T03:2xZ (session) | "The small OPEC oil price rise following the Tehran and Tripoli agreements of 1970-1971, and the subsequent 1973-1974 price explosion, reversed the steep decline in exploratory operations of the 1955-1970 period." |

S1 and S2 are primary and both are on history.state.gov, so this is **one** source domain under §1(a) and the record is partial. `docs/g/ROUTE_TESTS.md` records the second-domain routes tried this session.

## Narrative

On 2 April 1971 the oil companies signed an agreement with Libya, six weeks after the Gulf producers had settled at Tehran and on materially better terms. The State Department circulated the outcome to posts the same evening: the agreement "will increase payments to Libyan government about 63 cents per barrel", and the "New posted price (tax reference price) for 40 gravity oil will be 3.446 dollars up from 2.55 dollars per barrel" [S1] — a 35 % rise in the tax reference price, and roughly double the ~30¢ per barrel the Gulf states had obtained in February. Washington's own explanation of the gap was quality and geography rather than leverage: the "difference can be justified by location, transportation, gravity, and low sulphur advantages of Libyan crude" [S1]. The settlement did not stop at Libya. The same cable records that the companies "have made similar offers to Iraq and Saudi Arabia for pipeline oil exported from Mediterranean" [S1], which is the mechanism by which a Libyan term became a Mediterranean term. A week earlier the White House had described Libya as the state that "represents the Mediterranean countries" and had listed its demands as a posted-price increase and company reinvestment [S2]. A retrospective account pairs the two settlements as one episode — "the small OPEC oil price rise following the Tehran and Tripoli agreements of 1970-1971" [S3] — which is the only independent attestation of this agreement retrieved this session, and carries no figure.

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

**complete, narrowly** (upgraded 2026-09-03 from `partial — fails (a)`; the earlier status is preserved below).
(a) two independent registrable domains — `history.state.gov` (S1, S2, primary, and S1 dated the **day of the
event** with exact posted prices) and `merip.org` (S3, retrospective secondary); (b)–(f) were already met.
**Corroboration strength, stated, and it is the weakest of the four upgraded this session:** S3 contributes a
single sentence, written thirteen years later, which names "the Tehran and Tripoli agreements of 1970-1971" and
nothing else. It establishes that the agreement existed and is dated to that period. It does **not** corroborate
the date, the 63¢ per barrel, the $3.446/$2.55 tax reference prices, or the offers to Iraq and Saudi Arabia — all
of which rest on S1 alone. Clause (a) is met by the letter of §1(a); a reader who wants two substantive accounts
of this event does not have them, and Joe should admit it knowing that.

*Superseded status, 2026-09-03, kept as the record: "partial — fails (a). Two primary documents, one registrable
domain, for the reason SPINE_REGISTRATION Amendment 2 registered in advance."*
