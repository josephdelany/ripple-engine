# B1 situation-record spot audit (20 events)

Method: consistency check of each coding against the stored event record (title/type/entities)
and the corpus-observed outcome. NOTE: a fresh source re-fetch is not performed here; codings
derive from data already sourced in oil.db (event_entities coded from each event's source_url)
and the corpus's own dated events. Fields needing external source reading (alliance, diplomatic,
target_capacity, physical volume) are coded 'unknown' by design.

| date | type | actor→target | scope | tempo | outcome+90 | actor prop. | conf | title |
|---|---|---|---|---|---|---|---|---|
| 2026-03-04 | chokepoint_d | iran→hormuz | isolated | nth | CONTAINED | 0.286 | 0.588 | Iran declares the Strait of Hormuz closed |
| 2026-02-28 | conflict_esc | israel→iran | isolated | nth | LIMITED_RETALIATION | 0.333 | 0.425 | US and Israel strike Iran (Feb 2026 escalati |
| 2025-11-14 | chokepoint_d | unknown→russia | campaign | nth | CONTAINED | — | 0.562 | Ukrainian drone strike halts oil loadings at |
| 2025-09-05 | infrastructu | unknown→russia | campaign | nth | LIMITED_RETALIATION | — | 0.425 | Ukrainian drone strike on Rosneft Ryazan ref |
| 2025-08-18 | chokepoint_d | unknown→russia | campaign | nth | LIMITED_RETALIATION | — | 0.575 | Ukrainian strike halts Druzhba pipeline oil  |
| 2025-08-11 | infrastructu | unknown→russia | campaign | nth | LIMITED_RETALIATION | — | 0.425 | Ukrainian drone strike halts Rosneft Saratov |
| 2025-07-31 | infrastructu | unknown→chile | isolated | nth | CONTAINED | — | 0.412 | Codelco El Teniente collapse 2025 |
| 2025-07-14 | sanctions | usa→russia | campaign | nth | WIDENING | 0.529 | 0.45 | Trump threatens 100pct secondary tariffs on  |
| 2025-07-06 | chokepoint_d | unknown→bab_el_mandeb | isolated | nth | CONTAINED | — | 0.588 | Houthis resume Red Sea attacks sinking Magic |
| 2025-06-22 | conflict_esc | unknown→hormuz | isolated | nth | CONTAINED | — | 0.588 | US strikes Iranian nuclear sites Fordow Nata |
| 2025-06-13 | conflict_esc | israel→iran | isolated | nth | CONTAINED | 0.333 | 0.412 | Israel-Iran war onset (Operation Rising Lion |
| 2025-04-04 | sanctions | china→unknown | isolated | nth | RESOLUTION_BY_DEAL | 0.5 | 0.45 | China export controls on seven rare earths a |
| 2025-03-24 | sanctions | usa→venezuela | war | nth | RESOLUTION_BY_DEAL | 0.529 | 0.45 | US 25pct secondary tariff on buyers of Venez |
| 2025-03-15 | conflict_esc | unknown→bab_el_mandeb | isolated | nth | CONTAINED | — | 0.588 | US launches Operation Rough Rider air campai |
| 2025-03-10 | infrastructu | unknown→russia | campaign | nth | CONTAINED | — | 0.412 | Ukrainian drone strike on Rosneft Novokuibys |
| 2025-02-26 | sanctions | usa→venezuela | campaign | nth | RESOLUTION_BY_DEAL | 0.529 | 0.45 | US revokes Chevron Venezuela oil license |
| 2025-02-22 | sanctions | unknown→congo_drc | isolated | first | CONTAINED | — | 0.412 | DRC suspends all cobalt exports |
| 2025-02-17 | infrastructu | unknown→russia | campaign | nth | LIMITED_RETALIATION | — | 0.425 | Ukrainian drone strike on CPC Kropotkinskaya |
| 2025-02-05 | sanctions | usa→iran | war | nth | WIDENING | 0.529 | 0.45 | US restores maximum-pressure campaign on Ira |
| 2025-02-04 | sanctions | china→unknown | war | nth | WIDENING | 0.5 | 0.45 | China export controls on tungsten tellurium  |