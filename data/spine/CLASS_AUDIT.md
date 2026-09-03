# CLASS AUDIT — is every event in the geopolitical classes a hostile act?
*2026-09-02, Session F. All 75 events of `infrastructure_attack` and `chokepoint_disruption`,
each read against its own record and coded under the hostility precondition registered as
**OUTCOME_MAPPING Amendment 3 §A3.3** — which was committed before any count here was
computed. Nothing in `events` changes; no class is re-coded; no run is re-scored. This is a
reading of the existing record, published so it can be disputed row by row.*

## 1. The question and where it came from
Joe found the defect on the audit screen: events in the two geopolitical classes that are
not hostile acts at all, carrying an IES-90 escalation level. A keyword scan measured it at
7 candidates, of which 4 were held to be unambiguous non-hostile incidents
(`abqaiq_arabian_1977`, `suez_tropic_brilliance_2004`, `cpc_novorossiysk_storm_2022`,
`venezuela_blackout_2019`) and 3 were false positives of the scan's own vocabulary —
`kuwait_oil_fires_1991` and `me_sounion_2024` (hostile, correctly classed; caught on "fire"
and "ablaze") and `btc_pipeline_blast_2008` (contested; caught on "blast").

This audit does not take that scan on faith, and does not extend it. Every one of the 75
records was read in full — title, description, coded entities, source — and coded on what
the record says, with the four decisions that turn on an external fact checked against
sources outside the corpus. The result **confirms the scan's three exclusions and enlarges
its inclusion list from 4 to 9**, because the scan could only find events whose records
happened to contain a hazard word.

## 2. What was verified, and how
**Method.** All 75 records dumped from `data/oil.db` with their IES-90 rows, read one by one,
coded `hostile` / `hostile_unattributed` / `ambiguous` / `non_hostile` under Amendment 3
§A3.3. The coding is a human reading of the record — like the codebook itself, and like the
Admiralty and severity codings — not a regex, and it is published in full below so that
anyone can check it against the same sources.

**The four external checks** (the codings that turn on a fact not in the record):

| event | what was checked | finding |
|---|---|---|
| `abqaiq_arabian_1977` | was the 1977 Abqaiq fire an attack? | No. A buried 30-inch crude line failed at the gathering centre; the leak reached a power substation and ignited, 4 killed, 19 injured. A contemporaneous Capitol Hill rumour of Palestinian satchel charges was investigated and denied on the record by Aramco's president Frank Jungers — *"Absolutely not. It was a pipeline failure."* (Washington Post 1977-05-13 and 05-14; Process Safety Integrity case file 1977-05-11.) → **non_hostile**, with the rumour recorded |
| `druzhba_contamination_2019` | deliberate, but directed at whom? | Organochloride-contaminated crude was injected at a small private collection point in Samara to cover the months-long theft of on-spec crude from the same tanks. Eight arrests including four Transneft Druzhba employees; two fled abroad under international warrants. (Russian Investigative Committee via RFE/RL and Meduza 2019-05-08; OSW 2019-05-08; Oxford Energy Comment, Yermakov, 2019-06.) → **non_hostile** under tie-break 3: crime for private gain, not an act against an adversary |
| `btc_pipeline_blast_2008` | is the cause settled? | No, and it never was. The PKK claimed it (Al Jazeera 2008-08-07); US intelligence later attributed it to Russian cyber-sabotage of the pipeline's control system (Bloomberg 2014, reported via Eurasianet); that account was disputed in turn by ICS security researchers; the fire destroyed the evidence and the Turkish investigation could not establish whether a bomb was used. Because one live account is a technical failure, tie-break 1 does not apply. → **ambiguous** (Joe's reading confirmed) |
| `codelco_elteniente_2025` | collapse or attack? | A seismically triggered underground collapse at Codelco's El Teniente, fatal, taking the mine offline and cutting ~48,000 t from 2025 copper output. → **non_hostile** — and it is a copper mine, so `infrastructure_attack` fits it on neither axis |

**Result against the scan.** Confirmed: the 4 named unambiguous non-hostile events are
non-hostile; `kuwait_oil_fires_1991` and `me_sounion_2024` are hostile and correctly
classed; `btc_pipeline_blast_2008` is contested. **Not found by the scan** — five further
non-hostile events, none of which contains a hazard keyword:

| event | class | why the scan missed it | IES-90 level it carries |
|---|---|---|---|
| `iran_oilworkers_strike_1978` | infrastructure_attack | a **strike**: no hazard word, no attack either | **3 — war**, off the Iranian Revolution's intra-state war spell overlapping the window |
| `druzhba_contamination_2019` | chokepoint_disruption | "contamination" reads as deliberate | **2 — use of force**, off GED deaths in Russia |
| `suez_ever_given_2021` | chokepoint_disruption | "blocks the Suez Canal" — a grounding described by its effect | 0 |
| `kurdistan_ceyhan_halt_2023` | chokepoint_disruption | a state "halts" a pipeline — reads as coercion, is an ICC arbitration award | **2 — use of force**, off GED deaths in Turkey |
| `codelco_elteniente_2025` | infrastructure_attack | "collapse" of a copper mine | 0 |

That is the substantive result of this audit: **the defect is roughly twice the size the
keyword measurement showed, and the two worst individual cases — a labour strike scored as
war, and an oil-theft cover-up scored as use of force — are both invisible to a keyword
scan.** A scan can only find the incidents that describe themselves as incidents.

**Verified count: 9 non-hostile, 5 ambiguous, 3 hostile-but-unattributed, 58 hostile, of 75.**
All 9 non-hostile events carry a non-null IES-90 level (four at 0, two at 2, one at 3, and
two — `abqaiq_arabian_1977` and `suez_tropic_brilliance_2004` — at 0). None is
`no_independent_outcome` today; under Amendment 3 all nine become so.

## 3. Every event, with its evidence
Coding values are Amendment 3 §A3.3. The IES-90 column is the level the event carries
**today**, with its basis and the rule that fired — i.e. what the precondition would remove
or keep, not a new computation. `—` is `no_independent_outcome` (uncovered window).

### infrastructure_attack — 48 events

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `abqaiq_arabian_1977` | 1977-05-11 | **non_hostile** | 0 (location, `NONE.covered`) | Accidental fire: a buried 30-inch crude line failed at the Abqaiq gathering centre, the leak reached a power substation and ignited (vehicles the ignition source); 4 killed. Contemporaneous sabotage rumour (Palestinian satchel charges) was investigated and denied on the record by Aramco president Frank Jungers: 'Absolutely not. It was a pipeline failure.' (Washington Post 1977-05-13/14; Process Safety Integrity case file.) |
| `iran_oilworkers_strike_1978` | 1978-10-31 | **non_hostile** | 3 (location, `WAR.intra.location`) | A labour action: oil workers struck and exports stopped. No act was directed at anyone's infrastructure; the infrastructure_attack class fits nothing in the record. Political coercion in a revolution, but no force, no target, no attacking party. |
| `kharg_strikes_1985` | 1985-08-15 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Iraqi air raids on Iran's Kharg export terminal; named state actor, dyad Iraq-Iran. |
| `iraq_kharg_1986` | 1986-08-12 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Iraqi aircraft struck Iran's Sirri Island terminal; named state actor, dyad Iraq-Iran. |
| `kuwait_oil_fires_1991` | 1991-02-22 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Retreating Iraqi forces set 600-730 Kuwaiti wells alight. Named state actor, deliberate destruction of an adversary's infrastructure. Correctly classed -- a keyword scan on 'fire' flags it falsely. |
| `iraq_pipeline_north_2004` | 2004-08-03 | **hostile** | 3 (location, `GED.location.ge250`) | Insurgent bombing of the Kirkuk-Ceyhan line at Al-Fateha. Actor class named (Iraqi insurgency), no individual group. |
| `iraq_pipeline_south_2004` | 2004-08-27 | **hostile_unattributed** | 3 (location, `GED.location.ge250`) | Sabotage of the southern export pipelines. The record says 'saboteurs' and names no party or movement; H1 holds, H2 fails. |
| `nigeria_mend_ea_2006` | 2006-01-11 | **hostile** | 0 (location, `NONE.covered`) | MEND sabotage and kidnapping in the Niger Delta; named armed movement. |
| `nigeria_mend_forcados_2006` | 2006-02-18 | **hostile** | 0 (location, `NONE.covered`) | MEND attack on Shell's Forcados terminal and pipelines; named armed movement. |
| `saudi_abqaiq_foiled_2006` | 2006-02-24 | **hostile** | 0 (location, `NONE.covered`) | Al-Qaeda suicide car-bomb attempt on Abqaiq, repelled by guards. Named group; an attempted attack is a hostile act (and IES-90 asks about W, not about damage). |
| `nigeria_mend_bonga_2008` | 2008-06-19 | **hostile** | 0 (location, `NONE.covered`) | MEND boarded Shell's Bonga FPSO 120 km offshore and forced a shutdown; named armed movement. |
| `btc_pipeline_blast_2008` | 2008-08-05 | **ambiguous** | 0 (dyadic, `NONE.covered`) | Cause genuinely contested and never settled: the PKK claimed the Refahiye explosion (Al Jazeera 2008-08-07); US intelligence later attributed it to Russian cyber-sabotage of the control system (Bloomberg 2014, Eurasianet); that account was in turn disputed by ICS security researchers; the fire incinerated the evidence and the Turkish investigation could not establish whether a bomb was used. Tie-break 1 keeps a contested perpetrator hostile only where every live account is a hostile act -- here a technical failure remains live, so ambiguous. |
| `nda_bonny_2016` | 2016-02-10 | **hostile** | 3 (location, `GED.location.ge250`) | Niger Delta Avengers attack on the Bonny/Soku gas line; named armed movement. |
| `nigeria_nda_forcados_2016` | 2016-02-14 | **hostile** | 3 (location, `GED.location.ge250`) | Niger Delta Avengers bombed the Trans Forcados subsea line; named armed movement. |
| `nigeria_nda_escravos_2016` | 2016-05-25 | **hostile** | 3 (location, `GED.location.ge250`) | Niger Delta Avengers destroyed Chevron's Escravos feed lines; named armed movement. |
| `fujairah_tanker_sabotage_2019` | 2019-05-12 | **hostile_unattributed** | 2 (location, `GED.location.ge25`) | Limpet mines damaged four tankers off Fujairah. Unambiguously a deliberate attack; the UAE/Saudi/Norwegian technical report named only 'a state actor' and the record here names no party. H1 holds, H2 fails. |
| `saudi_ew_pipeline_2019` | 2019-05-14 | **hostile** | 0 (location, `NONE.covered`) | Armed drones struck two East-West pipeline pump stations; Houthi movement named. |
| `gulf_of_oman_tanker_attacks_2019` | 2019-06-13 | **hostile** | 2 (location, `GED.location.ge25`) | Two tankers struck near Hormuz. Attribution to Iran was asserted and contested, but every live account is an attack -- tie-break 1 keeps it hostile. |
| `saudi_shaybah_2019` | 2019-08-17 | **hostile** | 2 (location, `ICB.single.wholly`) | Houthi drones struck the Shaybah field and its gas plant; named movement. |
| `abqaiq_attack_2019` | 2019-09-14 | **hostile** | 0 (location, `NONE.covered`) | Aerial attack removed a large share of Saudi processing capacity. Attribution contested between the Houthis' claim and the US/Saudi attribution to Iran; both are hostile acts -- tie-break 1. |
| `saudi_jeddah_depot_2020` | 2020-11-23 | **hostile** | 0 (location, `NONE.covered`) | A Quds-2 cruise missile hit a storage tank at Aramco's North Jeddah plant; Houthi movement named. |
| `ras_tanura_attack_2021` | 2021-03-07 | **hostile** | 0 (dyadic, `NONE.covered`) | Drone and missile attack on Ras Tanura and the Dhahran compound; Houthi movement named. |
| `colonial_pipeline_shutdown_2021` | 2021-05-07 | **ambiguous** | 0 (location, `NONE.covered`) | DarkSide ransomware; the shutdown itself was Colonial's own precautionary decision (DOE/CESER incident record). A directed attack on the victim, which distinguishes it from the Druzhba case, but extortion for private gain by a criminal group, which no covering source of IES-90 would ever carry. Between tie-breaks 2 and 3, and listed. |
| `uae_abudhabi_attack_2022` | 2022-01-17 | **hostile** | 0 (location, `NONE.covered`) | Drones and missiles struck ADNOC fuel trucks at Musaffah, three killed; Houthi movement named and claimed. |
| `saudi_jeddah_f1_2022` | 2022-03-25 | **hostile** | 0 (location, `NONE.covered`) | Houthi drones and missiles set two Aramco North Jeddah storage tanks alight during the Grand Prix; named movement, claimed. |
| `nord_stream_sabotage_2022` | 2022-09-26 | **hostile_unattributed** | 2 (location, `GED.location.ge25`) | Multiple ruptures on Nord Stream 1 and 2; deliberate underwater sabotage is not in doubt and the seismic/atmospheric record is published (ACP 2024), but no party is named in the record or established by any investigation. The clearest H1-yes / H2-no case in the corpus. |
| `ukr_odesa_strike_2023` | 2023-07-18 | **hostile** | 3 (location, `GED.location.ge250`) | Russian missile and drone strikes on Odesa and Chornomorsk export terminals; named state actor, dyad Russia-Ukraine. |
| `ukr_izmail_strike_2023` | 2023-08-02 | **hostile** | 3 (location, `GED.location.ge250`) | Russian drone strikes on the Izmail Danube grain port; named state actor. |
| `russia_ustluga_strike_2024` | 2024-01-21 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian drone strike on Novatek's Ust-Luga terminal; named state actor, dyad Ukraine-Russia. |
| `rus_tuapse_strike_2024a` | 2024-01-25 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian drone strike on Rosneft's Tuapse refinery; named state actor. |
| `me_marlin_luanda_2024` | 2024-01-26 | **hostile** | 3 (location, `GED.location.ge250`) | Houthi ballistic missile set the naphtha tanker Marlin Luanda ablaze; named movement, claimed. |
| `rus_volgograd_strike_2024` | 2024-02-03 | **hostile** | 2 (location, `GED.location.ge25`) | SBU drones hit Lukoil's Volgograd refinery; named state agency. |
| `me_rubymar_2024` | 2024-02-18 | **hostile** | 3 (location, `GED.location.ge250`) | Houthi missile crippled the Rubymar, which later sank; named movement, claimed. |
| `russia_refineries_strikes_2024` | 2024-03-13 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian drone campaign against Ryazan and Novoshakhtinsk; named state actor. |
| `rus_slavyansk_strike_2024` | 2024-03-17 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian drone strike on the Slavyansk-on-Kuban refinery; named state actor. |
| `rus_novorossiysk_depots_2024` | 2024-05-17 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike on the Novorossiysk oil depots and terminals; named state actor. |
| `me_mv_tutor_2024` | 2024-06-12 | **hostile** | 2 (location, `GED.location.ge25`) | Houthi drone-boat and missile attack sank the MV Tutor; named movement, claimed. |
| `me_chios_lion_2024` | 2024-07-15 | **hostile** | 2 (location, `GED.location.ge25`) | Houthi unmanned surface vessel damaged the tanker Chios Lion; named movement, claimed. |
| `rus_tuapse_strike_2024b` | 2024-07-22 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike set the Tuapse refinery on fire; named state actor. |
| `me_sounion_2024` | 2024-08-21 | **hostile** | 2 (location, `GED.location.ge25`) | Houthi attacks disabled and set fire to the laden crude tanker Sounion; named movement, claimed. Correctly classed -- a keyword scan on 'ablaze'/'fire' flags it falsely. |
| `rus_novoshakhtinsk_strike_2024` | 2024-12-19 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drones and missiles set the Novoshakhtinsk refinery ablaze; named state actor. |
| `rus_ryazan_strike_2025a` | 2025-01-24 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian mass drone strike on the Rosneft Ryazan refinery; named state actor. |
| `rus_volgograd_strike_2025` | 2025-01-31 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike on Lukoil's Volgograd refinery; named state actor. |
| `cpc_kropotkinskaya_drone_2025` | 2025-02-17 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike on the CPC Kropotkinskaya pumping station; named state actor. |
| `rus_novokuibyshevsk_strike_2025` | 2025-03-10 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike on Rosneft's Novokuibyshevsk refinery; named state actor. |
| `codelco_elteniente_2025` | 2025-07-31 | **non_hostile** | 0 (location, `NONE.covered`) | Industrial accident: a seismically triggered underground collapse at Codelco's El Teniente killed workers and took the mine offline. No party, no act -- and a copper mine, not oil, so the class fits on neither axis. |
| `rus_saratov_strike_2025a` | 2025-08-11 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian drone strike halted the Rosneft Saratov refinery; named state actor. |
| `rus_ryazan_strike_2025b` | 2025-09-05 | **hostile** | 2 (location, `GED.location.ge25`) | Repeat Ukrainian drone strike on the Ryazan refinery; named state actor. |

### chokepoint_disruption — 27 events

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `tanker_war_1984` | 1984-03-27 | **hostile** | 3 (location, `WAR.inter.single`) | Iraqi attacks on Gulf shipping; the Tanker War. Named state actor, armed attack. |
| `earnest_will_1987` | 1987-07-22 | **ambiguous** | 3 (location, `WAR.intra.location`) | A protective naval operation: the US reflagged Kuwaiti tankers and escorted them. A display of force by a named state, but defensive escort, not an act directed at an adversary. Tie-break 2 of A3.3 puts a protective deployment outside H1; it is listed rather than coded hostile because a display of force is inside IES-90's own level 1. |
| `bridgeton_mine_strike_1987` | 1987-07-24 | **hostile** | 3 (location, `WAR.intra.location,WAR.inter.single`) | The reflagged tanker Bridgeton struck an IRGC mine near Farsi Island. Mining a transit lane is a hostile act; actor named (Iran). |
| `suez_tropic_brilliance_2004` | 2004-11-08 | **non_hostile** | 0 (location, `NONE.covered`) | Navigational accident: the 89,000-tonne tanker lodged crosswise near Ismailiya and closed the canal for three days. No party, no act. |
| `hormuz_iran_threat_2011` | 2011-12-27 | **hostile** | 0 (location, `NONE.covered`) | Iran's vice-president threatened to close Hormuz against looming sanctions. An explicit threat of force by a named state -- inside H1 by its own terms, and level 1 of IES-90 is 'threat or display of force'. |
| `libya_jathran_blockade_2013` | 2013-08-01 | **ambiguous** | 0 (location, `NONE.covered`) | Armed Petroleum Facilities Guard units under Ibrahim Jathran shut Es Sider, Ras Lanuf and Zueitina over a revenue dispute with Tripoli. Armed coercion by a named party, but a domestic pay-and-autonomy dispute by the very force paid to guard the terminals; the cited source calls them protesters. Between armed blockade and industrial action, and listed as such. |
| `kirkuk_ceyhan_isis_2014` | 2014-03-02 | **hostile** | 3 (location, `GED.location.ge250`) | Repeated ISIS bombing of the Iraqi leg of the Kirkuk-Ceyhan line; named armed group. |
| `libya_ports_clashes_2014` | 2014-12-14 | **hostile** | 2 (location, `GED.location.ge25`) | Armed fighting between rival Libyan factions at the eastern terminals closed them. Hostile act; the parties are factions in a civil war, named as classes. |
| `bab_el_mandeb_houthi_tanker_2018` | 2018-04-03 | **hostile** | 3 (location, `GED.location.ge250`) | Houthi attack on a Saudi crude tanker off Hodeidah; named movement, dyad Yemen(Houthi)-Saudi Arabia. |
| `saudi_suspends_bab_el_mandeb_2018` | 2018-07-25 | **ambiguous** | 0 (dyadic, `NONE.covered`) | The coded event is Riyadh's own decision to suspend crude transit after Houthi attacks on two of its tankers. The hostile act is the antecedent attack, not the suspension; tie-break 2 puts a precautionary state decision outside H1. Listed rather than coded non_hostile because the record folds the attacks into the same row. |
| `venezuela_blackout_2019` | 2019-03-07 | **non_hostile** | 0 (location, `NONE.covered`) | Nationwide grid collapse shut the Jose terminal and the Orinoco upgraders. The Maduro government alleged US and opposition sabotage; no evidence for it was produced and the sourced account is a power-system failure. Coded non_hostile with the allegation on the record. |
| `druzhba_contamination_2019` | 2019-04-20 | **non_hostile** | 2 (location, `GED.location.ge25`) | Deliberate, but crime for private gain, not an act against an adversary: organic-chloride crude was injected at a private collection point in Samara to cover the months-long theft of on-spec crude; eight arrests including four Transneft Druzhba employees, two fled abroad (Russian Investigative Committee; Meduza 2019-05-08; OSW; Oxford Energy Comment 2019-06). Tie-break 3 applies. |
| `grace1_seizure_2019` | 2019-07-04 | **hostile** | 0 (location, `NONE.covered`) | Royal Marines boarded and seized the laden tanker Grace 1 off Gibraltar. A forcible state seizure of another state's cargo is a militarized action in the MID sense, whatever its legal basis; named state actor, and it drew a reciprocal seizure. |
| `stena_impero_seizure_2019` | 2019-07-19 | **hostile** | 1 (location, `ICB.single.onset`) | IRGC seized the UK-flagged Stena Impero in Hormuz; named state actor, direct interference with transit. |
| `libya_haftar_blockade_2020` | 2020-01-18 | **hostile** | 3 (location, `GED.location.ge250`) | Pro-Haftar forces blockaded the eastern terminals and southern fields, cutting output from ~1.2 to ~0.32 mb/d. Armed blockade by a named party in a civil war. |
| `hankuk_chemi_seizure_2021` | 2021-01-04 | **hostile** | 0 (location, `NONE.covered`) | IRGC seized the tanker Hankuk Chemi in Hormuz; named state actor. |
| `suez_ever_given_2021` | 2021-03-23 | **non_hostile** | 0 (location, `NONE.covered`) | Navigational accident: the container ship grounded and blocked the canal. No party, no act. Missed by a keyword scan because the record says neither fire nor storm nor collapse. |
| `mercer_street_2021` | 2021-07-29 | **hostile** | 0 (location, `NONE.covered`) | One-way drone strike on the tanker Mercer Street off Oman, two killed; attributed to Iran by the US and UK and denied. Every live account is an attack -- tie-break 1. |
| `cpc_novorossiysk_storm_2022` | 2022-03-23 | **non_hostile** | 0 (location, `NONE.covered`) | Natural hazard: storm damage to the single-point moorings stopped loadings at the CPC Black Sea terminal. No party, no act. |
| `kurdistan_ceyhan_halt_2023` | 2023-03-25 | **non_hostile** | 2 (location, `GED.location.ge25`) | A legal and commercial action: Turkey stopped the Kirkuk-Ceyhan pipeline in compliance with an ICC arbitration award against it in Iraq's favour. A state act, but adjudicated dispute settlement, not an act directed adversarially. Fails H1. |
| `me_galaxy_leader_2023` | 2023-11-19 | **hostile** | 3 (location, `GED.location.ge250`) | Houthi helicopter raid seized the car carrier Galaxy Leader in the southern Red Sea; named movement, claimed. |
| `red_sea_attacks_2023` | 2023-12-01 | **hostile** | 3 (location, `GED.location.ge250`) | The Houthi campaign against commercial shipping at Bab el-Mandeb; named movement. |
| `me_maersk_diversions_2023` | 2023-12-15 | **hostile** | 3 (location, `GED.location.ge250`) | A Houthi drone strike near Bab el-Mandeb; the diversions are its consequence, and the coded act is the attack. |
| `redsea_houthi_resume_2025` | 2025-07-06 | **hostile** | 2 (location, `GED.location.ge25`) | Renewed Houthi attacks near Bab el-Mandeb, sinking the Magic Seas; named movement, claimed. |
| `rus_druzhba_strike_2025a` | 2025-08-18 | **hostile** | 2 (location, `GED.location.ge25`) | Ukrainian strikes on the Unecha Druzhba pumping hub halted flows to Hungary and Slovakia; named state actor. |
| `rus_novorossiysk_terminal_2025` | 2025-11-14 | **hostile** | — (uncovered, `UNCOVERED`) | Ukrainian drone strike on the Sheskharis complex halted loadings at Novorossiysk; named state actor. |
| `hormuz_closure_2026` | 2026-03-04 | **hostile** | — (uncovered, `UNCOVERED`) | Iran declared Hormuz closed and attacked transiting tankers; named state actor. |


## 4. The ambiguous five, named as ambiguous
These are not "probably hostile" or "probably not". They are events where the record does
not settle it, and Amendment 3 §A3.3 excludes them from G-scoring while listing them by
name, so that a later decision — Joe's, or a better source — can move them either way
without anything having been quietly assumed.

| event | date | the two readings | IES-90 today |
|---|---|---|---|
| `earnest_will_1987` | 1987-07-22 | A US naval reflagging and escort operation. **Display of force by a named state** (and IES-90's own level 1 is "threat or display of force") vs **a protective deployment**, which tie-break 2 puts outside H1. | 3 (location) |
| `btc_pipeline_blast_2008` | 2008-08-05 | **PKK bombing / Russian cyber-sabotage** vs **technical failure**; never settled, evidence incinerated. | 0 |
| `libya_jathran_blockade_2013` | 2013-08-01 | **Armed blockade** by Petroleum Facilities Guard units under Jathran vs **an industrial and revenue dispute** by the force paid to guard the terminals — the cited source calls them protesters. | 0 |
| `saudi_suspends_bab_el_mandeb_2018` | 2018-07-25 | The row folds two things together: **Houthi attacks on two Saudi tankers** (hostile) and **Riyadh's own decision to suspend transit** (tie-break 2: a precautionary state decision is not itself a hostile act). The coded actor is Saudi Arabia. | 0 |
| `colonial_pipeline_shutdown_2021` | 2021-05-07 | **A directed ransomware attack** by DarkSide vs **extortion for private gain** (tie-break 3), with the shutdown itself Colonial's own precautionary decision. No covering source of IES-90 would ever carry it. | 0 |

Two of the five (`saudi_suspends_bab_el_mandeb_2018`, and arguably
`libya_jathran_blockade_2013`) are ambiguous because **the record bundles an act with a
response to it**. That is a record-quality question for Session E, not a target question, and
it is raised in the handoff rather than resolved here.

## 5. Counts by class and by decade

| class | hostile | hostile_unattributed | ambiguous | non_hostile | total |
|---|---:|---:|---:|---:|---:|
| `infrastructure_attack` | 40 | 3 | 2 | 3 | 48 |
| `chokepoint_disruption` | 18 | 0 | 3 | 6 | 27 |
| **both** | **58** | **3** | **5** | **9** | **75** |

| decade | hostile | hostile_unattributed | ambiguous | non_hostile | total | non-hostile share |
|---|---:|---:|---:|---:|---:|---:|
| 1970s | 0 | 0 | 0 | 2 | 2 | 100% |
| 1980s | 4 | 0 | 1 | 0 | 5 | 0% |
| 1990s | 1 | 0 | 0 | 0 | 1 | 0% |
| 2000s | 5 | 1 | 1 | 1 | 8 | 12% |
| 2010s | 13 | 1 | 2 | 2 | 18 | 11% |
| 2020s | 35 | 1 | 1 | 4 | 41 | 10% |
| **all** | **58** | **3** | **5** | **9** | **75** | **12%** |

Two things in those tables are worth saying out loud.

**Both 1970s records are non-hostile.** The two oldest events in these classes — the 1977
Abqaiq pipeline fire and the 1978 oil-workers' strike — are the only two the corpus has
before 1984, and neither is an attack. The deep-history tier reached back for *oil supply
disruptions* and filed them under a class named for attacks. Whatever the walk learns about
`infrastructure_attack` before 1980, it learns from two incidents.

**The non-hostile share is stable at about one in nine from 2000 on** (12%, 11%, 10% by
decade) and does not shrink as the corpus modernises. This is not a legacy-records problem
that the recent, better-sourced events grow out of. It is what the class definition does.

## 6. Impact on the published walk — reported, not applied
Amendment 3 §A3.5: **no published run is re-scored.** These numbers say how much of the
published G result rests on events for which the G target is undefined. They are an impact
statement for the paper's limitations section, and a handoff to Session B for v3.

Set: the **150 daily-tier scored G reads** of run `walk_20260902T210135Z`
(`data/walk_forward/summary.json` → `/tiers/daily/G`, n = 150), being the daily-tier reads
that passed burn-in and carry both an engine and a climatology G score.

| | n | level-0 | share |
|---|---:|---:|---:|
| **as published** | 150 | 63 | **42.0%** |
| excluding the 6 `non_hostile` (the Amendment 3 rule as registered) | 144 | 59 | **41.0%** |
| also excluding the 3 `ambiguous` | 141 | 56 | **39.7%** |
| also excluding the 2 `hostile_unattributed` (the strictest reading) | 139 | 56 | **40.3%** |

**Affected: 9 of the 150 reads (6.0%)** — 6 non-hostile, 3 ambiguous. Named, with the level
each contributed:

| event | coding | level in the run |
|---|---|---:|
| `venezuela_blackout_2019` | non_hostile | 0 |
| `druzhba_contamination_2019` | non_hostile | **2** |
| `suez_ever_given_2021` | non_hostile | 0 |
| `cpc_novorossiysk_storm_2022` | non_hostile | 0 |
| `kurdistan_ceyhan_halt_2023` | non_hostile | **2** |
| `codelco_elteniente_2025` | non_hostile | 0 |
| `btc_pipeline_blast_2008` | ambiguous | 0 |
| `saudi_suspends_bab_el_mandeb_2018` | ambiguous | 0 |
| `colonial_pipeline_shutdown_2021` | ambiguous | 0 |

The other five affected events (`abqaiq_arabian_1977`, `iran_oilworkers_strike_1978`,
`suez_tropic_brilliance_2004`, `earnest_will_1987`, `libya_jathran_blockade_2013`) are
already outside the 150 — the first two are monthly-tier, and all five fail the walk's
burn-in. They are outside the headline G result but inside the corpus, so they still teach
the engine as analogues: `iran_oilworkers_strike_1978` carries **level 3, war** wherever it
is retrieved as a precedent.

**Reading the numbers honestly.** The effect on the headline is small: n falls by 6 (4%) and
the level-0 share by about one point, 42.0% → 41.0%. Two things follow, and only two.
1. The defect is **not** a level-0 inflation story. Four of the six non-hostile reads in the
   150 are level 0, but so is 42% of the whole set; removing them barely moves the base rate.
   The two that are *not* level 0 are the damaging ones — a contaminated pipeline reading as
   use of force, an arbitration award reading as use of force — because those are the cases
   where the location fallback manufactured escalation out of nothing to do with the event.
2. The engine's G skill against climatology is **not** materially explained by these events,
   and this audit gives no ground to claim otherwise in either direction. What it removes is
   not error but **9 reads that should never have been asked**, and the honest statement for
   the paper is that the target was mis-specified for 6% of the scored G reads, in a way that
   cannot be corrected in this run and is corrected in v3.

Nothing above changes `summary.json`, `scores.jsonl` or `reads.jsonl`. Per Amendment 3
§A3.5, every surface reporting G from this run carries: *"scored before Amendment 3;
includes 6 non-hostile events for which the G target is undefined (9 counting ambiguous) —
`data/spine/CLASS_AUDIT.md` §6."*

## 7. Proposal (not applied) — should the two classes split into hostile and non-hostile?
*A written proposal for Joe, per the brief. Nothing here is applied, and no codebook change
is made: `EVENTS_CODEBOOK.md` is Session E's file and a class change is a Joe decision under
SESSION_CHARTER §2 rule 3.*

### 7.1 The general defect
The codebook names its classes after **what was disrupted** — a pipeline, a strait, a
refinery — and the six original types read as a taxonomy of *causes*: an OPEC decision, a
sanction, a war. `infrastructure_attack` and `chokepoint_disruption` are the two that
straddle it. `infrastructure_attack` says "attack" and takes accidents; `chokepoint_disruption`
says "disruption" and takes both a mined tanker and a grounded one. So the classes conflate a
**hostile act** with an **incident**, and every consumer that treats class as a proxy for
"geopolitical" — IES-90, the G target, the escalation analogues, the per-class Big Moves
rates — inherits the conflation. The other five classes do not have this problem:
`opec_decision`, `sanctions`, `policy_response`, `demand_shock` and `conflict_escalation` all
name an act or an actor, not a piece of damaged equipment.

### 7.2 The proposal
Split each into a hostile and a non-hostile subclass, as a **new field, not a new type**:

| existing type | hostile subclass | non-hostile subclass | count today |
|---|---|---|---|
| `infrastructure_attack` | `infrastructure_attack` (unchanged) | `infrastructure_incident` | 43 hostile* / 3 non-hostile / 2 ambiguous |
| `chokepoint_disruption` | `chokepoint_interdiction` | `chokepoint_incident` | 18 hostile* / 6 non-hostile / 3 ambiguous |

(*hostile including the 3 `hostile_unattributed`. Full split: 61 hostile, 9 non-hostile,
5 ambiguous.)

**Recommended form: keep the seven types and add a `hostility` field.** Renaming types would
break `p_class_given_big`, the analogue retrieval, the menus, every registered per-class
number and every published figure, for an effect a field achieves exactly. A field is
additive, is what Amendment 3 already requires the engine to carry, and lets the
ambiguous five be *ambiguous* rather than forced into one bucket — which a type cannot do.
The subclass names above are then views on `(type, hostility)`, not new canon.

### 7.3 What it would do to the Big Moves per-class rates
`p_big_given_class` = events of the class falling inside a big-move window (onset − 7 d
daily, − 31 d monthly, to end), over events of the class inside the asset's coverage. Rules
and episodes exactly as published (`BIG_MOVES_REGISTRATION.md` Amendment 2,
`data/big_moves/*.json`); only the class denominators are split. **Not applied.**

| asset | class | as published | hostile only | non-hostile only | ambiguous |
|---|---|---|---|---|---|
| Brent (daily, from 1987-05) | `infrastructure_attack` | 5/44 = 11.4% | 5/41 = **12.2%** | 0/1 = 0% | 0/2 |
| Brent | `chokepoint_disruption` | 4/26 = 15.4% | 3/17 = **17.6%** | 1/6 = 16.7% | 0/3 |
| WTI (daily, from 1986-01) | `infrastructure_attack` | 6/45 = 13.3% | 6/42 = **14.3%** | 0/1 = 0% | 0/2 |
| WTI | `chokepoint_disruption` | 4/26 = 15.4% | 4/17 = **23.5%** | 0/6 = 0% | 0/3 |
| WTI monthly (from 1946) | `infrastructure_attack` | 12/48 = 25.0% | 11/43 = **25.6%** | 0/3 = 0% | 1/2 |
| WTI monthly | `chokepoint_disruption` | 9/27 = 33.3% | 6/18 = **33.3%** | 3/6 = 50.0% | 0/3 |

Read with the n's in view, because they are small:
- **The clean result is WTI daily `chokepoint_disruption`: 15.4% → 23.5%**, because all four
  big-move-adjacent chokepoint events are hostile and six non-hostile events sit in the
  denominator diluting the rate by half. That is the shape the split is supposed to reveal —
  a hostile interdiction of a strait moves oil, a ship running aground in one mostly does not.
- **`infrastructure_attack` barely moves** (11.4% → 12.2% Brent, 13.3% → 14.3% WTI, 25.0% →
  25.6% monthly): only 3 of its 48 events are non-hostile, so there is little to remove.
- **The monthly chokepoint row runs the other way**, 33.3% published → 33.3% hostile with
  non-hostile at 3/6 = 50%: at 31 days before onset and monthly episodes the windows are wide
  enough that a grounding or a storm often sits inside one. This is a warning about attribution
  width at the monthly tier, not evidence that groundings move oil, and it is the row that
  most needs Joe's eye.
- Every cell is single-digit-to-low-double-digit n. **None of these differences is
  significant**, and the proposal does not rest on them: it rests on the classes meaning two
  different things. The rates are given because the brief asked what the split would do, and
  the honest answer is "it sharpens one row out of six and the n's are too small to test".

### 7.4 What the split would cost
The corpus loses no event. The published Big Moves numbers stay as published (same
retroactivity bar as Amendment 3 §A3.5): a split changes future computations, not the
registered ones. The real costs are (a) `p_big_given_class` denominators of 17–18 for the
hostile chokepoint rate, which is thin and must be labelled thin; and (b) someone must code
`hostility` for `conflict_escalation` and `sanctions` too before the field is used anywhere,
or the four geopolitical classes will be split two ways.

### 7.5 Recommendation
**Adopt the field, not the rename**, and only after the remaining two geopolitical classes
are audited the same way. Amendment 3 already requires the coding to exist for G-scoring, so
the field is being paid for regardless; the question is only whether it is also exposed as a
class view. Recommend yes for the surfaces and the Big Moves table, no for the `events.type`
enum.

## 8. Receipts
- Coding rule: `OUTCOME_MAPPING.md` Amendment 3 §A3.3 (committed before any count here).
- Events and IES-90 rows: `data/oil.db` (`events`, `event_entities`, `event_outcomes`
  `source='ies90'`), 75 rows in the two classes.
- Walk numbers: `data/walk_forward/scores.jsonl`, run `walk_20260902T210135Z`, daily tier,
  `burn_in_ok` and both engine and climatology G scored → n = 150, matching
  `summary.json` `/tiers/daily/G/engine_vs/climatology/n`.
- Big Moves: `data/big_moves/{brent,wti,wti_monthly}.json`, episodes and coverage as
  published; attribution window from `src/big_moves.py` `TIERS[*]["attr_before_days"]`.
- Checked by `tests/test_hostility.py`: every event of the two classes appears here exactly
  once, its date, class and IES-90 level match the DB, the coding vocabulary is the
  Amendment 3 vocabulary, the count tables agree with the rows, and the §6 impact figures
  recompute from `scores.jsonl`.
- Not touched: `events`, `data/walk_forward/**`, `data/dossiers/**`, `data/spine/patches/**`,
  `EVENTS_CODEBOOK.md`, `src/**`.
