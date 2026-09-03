# CLASS AUDIT — is every event in the geopolitical classes a hostile act?
*2026-09-02, Session F. **All 187 events of the four geopolitical classes** —
`infrastructure_attack` (48), `chokepoint_disruption` (27), `conflict_escalation` (55),
`sanctions` (57) — each read against its own record and coded under the hostility
precondition registered as **OUTCOME_MAPPING Amendment 3 §A3.3**, with the four cases the
second pass exposed decided in **Amendment 3.2** before those classes were coded. The field
itself is canon: **`EVENTS_CODEBOOK.md`, amendment 2026-09-02, approved by Joe.** Nothing in
`events` changes; no class is re-coded; no run is re-scored. This is a reading of the
existing record, published so it can be disputed row by row.*

**Result: 151 hostile, 3 hostile-unattributed, 13 ambiguous, 20 non-hostile.
33 of 187 events (18%) are not G-scorable.**

## 1. The question and where it came from
Joe found the defect on the audit screen: events in the geopolitical classes that are not
hostile acts at all, carrying an IES-90 escalation level. The types name **what was
disrupted**, not **who did it**, so the classes conflate a hostile act with an incident, and
every consumer that treats class as a proxy for "geopolitical" inherits the conflation.

A keyword scan of the two damage classes measured it at 7 candidates, of which 4 were held
to be unambiguous non-hostile incidents. Reading all 75 records instead found **9**. Reading
the remaining 112 — `conflict_escalation` and `sanctions`, done second on Joe's instruction —
found **11 more**, in shapes the first pass could not have predicted. The audit is now
complete across all four geopolitical classes.

## 2. What was verified, and how
**Method.** All 187 records dumped from `data/oil.db` with their IES-90 rows and read one by
one — title, description, coded entities, source — then coded `hostile` /
`hostile_unattributed` / `ambiguous` / `non_hostile`. The coding is a human reading of the
record, like the codebook's own severity and surprise scales, and it is published in full
below so anyone can check it against the same sources. **Never coded from the outcome**: the
IES-90 column is shown beside each row because it is what the precondition would remove or
keep, and it played no part in the coding.

**Eight external checks** — the codings that turn on a fact not in the record:

| event | what was checked | finding |
|---|---|---|
| `abqaiq_arabian_1977` | was the 1977 Abqaiq fire an attack? | No. A buried 30-inch crude line failed; the leak reached a power substation and ignited; 4 killed, 19 injured. A Capitol Hill rumour of Palestinian satchel charges was investigated and denied on the record by Aramco's president — *"Absolutely not. It was a pipeline failure."* (Washington Post 1977-05-13/14.) → **non_hostile** |
| `druzhba_contamination_2019` | deliberate, but directed at whom? | Organochloride crude injected at a private collection point in Samara to cover months of theft of on-spec crude; eight arrests including four Transneft Druzhba employees, two fled abroad. (Investigative Committee via RFE/RL; Meduza 2019-05-08; Oxford Energy 2019-06.) → **non_hostile**, tie-break 3 |
| `btc_pipeline_blast_2008` | is the cause settled? | No, and never was. PKK claim (Al Jazeera 2008-08-07); later US attribution to Russian cyber-sabotage (Bloomberg 2014 via Eurasianet); disputed by ICS security researchers; the fire destroyed the evidence. One live account is a technical failure → **ambiguous** |
| `codelco_elteniente_2025` | collapse or attack? | A seismically triggered underground collapse, fatal, ~48,000 t of 2025 copper lost. → **non_hostile** — and a copper mine, so the class fits on neither axis |
| `kazakhstan_unrest_2022` | is "unrest over fuel prices" the whole event? | No — the record understates it. 227 killed including 19 police, 4,353 injured; security forces fired on crowds in Almaty on 5–6 January; CSTO troops deployed. (Kazakh prosecutors via Al Jazeera 2022-01-15; IPHR; Crisis Group.) → **hostile** under 3.2(d) |
| `gabon_coup_2023` | was force used, or was it a paper transfer? | Force. Officers seized power, placed President Bongo under house arrest, arrested his son; gunfire in Libreville. (CNN, Al Jazeera, CNBC 2023-08-30.) → **hostile** under 3.2(d); no reported deaths does not make a coup non-hostile |
| `drc_cobalt_ban_2025` | statecraft or price management? | Price management. ARECOMS suspended all cobalt exports for four months after prices hit a nine-year low below $10/lb, to curb oversupply and defend price; extended three months in June for the same reason. (ARECOMS decision 2025-02-22; IEA policy record; Project Blue.) → **non_hostile** under 3.2(c) |
| `chn_gage_2023` | retaliation, or industrial security? | Unsettled, and that is the finding. MOFCOM's own statement gives "national security and interests" under the 2020 Export Control Law and **names no country** (MOFCOM press conference 2023-07-06); every outside reading treats it as retaliation for the US chip controls of October 2022 (CSIS; Stimson; ORF America). → **ambiguous**, and the same for the four sibling licensing measures |

### 2.1 What the first pass found (the two damage classes)
Confirmed the scan's three exclusions: `kuwait_oil_fires_1991` and `me_sounion_2024` are
hostile and correctly classed (the scan caught them on "fire" and "ablaze"), and
`btc_pipeline_blast_2008` is contested. Found five the scan could not reach, because their
records contain no hazard word: `iran_oilworkers_strike_1978` (a labour strike carrying
**level 3, war**), `druzhba_contamination_2019` (**level 2**), `kurdistan_ceyhan_halt_2023`
(an ICC arbitration award, **level 2**), `suez_ever_given_2021`, `codelco_elteniente_2025`.

> **[Amendment 4, 2026-09-03.]** Two of the three levels quoted in that sentence have since
> moved, and the sentence is left as written because it is the record of what the first pass
> found. `druzhba_contamination_2019` is now **`—`** (`UNDATED.continuation`): the GED deaths
> in Russia that made it level 2 were already at that level across the pre-window, so they
> assert nothing about the event. `iran_oilworkers_strike_1978` **still carries level 3**, from
> the Iranian Revolution's intra-state spell, which began 58 days before the event and so does
> not cover the whole pre-window. That is the cleanest case in the corpus for why both rules
> are needed: Amendment 4 does not catch it, and the hostility precondition does.

### 2.2 What the second pass found (conflict_escalation and sanctions)
Three shapes, none of them visible from the first two classes:

1. **`conflict_escalation` contains eight industrial-relations events that are not conflicts
   at all** — `escondida_strike_2011`, `sa_platinum_strike_2014`, `escondida_strike_2017`,
   `lasbambas_blockade_2019`, `lasbambas_halt_2021`, `cuajone_shutdown_2022`,
   `peru_lasbambas_2022`, `escondida_strike_2024`. Copper and platinum strikes and community
   road blockades in Chile and Peru. The counterparty is an employer or a mine operator;
   there is no state, no adversary and no act of force. They are in the corpus for a good
   reason — they move metal prices — and they are in the wrong class for it. A ninth,
   `marikana_strike_2012`, is ambiguous only because the record bundles the strike with the
   police killing of 34 strikers.
2. **`sanctions` contains three producer price-management export bans** —
   `indonesia_nickel_ban_2019` (forcing domestic smelting), `indonesia_palm_ban_2022`
   (curbing domestic cooking-oil prices) and `drc_cobalt_ban_2025` (defending a collapsed
   cobalt price). Each is a producer managing its own market: the act of an `opec_decision`,
   filed under `sanctions`. **`drc_cobalt_ban_2025` carries IES-90 level 3 — war** — off GED
   deaths in the DRC. It is the worst single case in the corpus: a cobalt price-support
   measure scored as war.

   > **[Amendment 4, 2026-09-03: this is no longer true, and the sentence stands as the record
   > of why the second pass was run.]** `drc_cobalt_ban_2025` is now **`—`**
   > (`UNDATED.continuation`). The GED deaths in the DRC that produced "war" were already above
   > the war line across the whole pre-window — 3,555 in the 90 days *before* the event against
   > 315 inside the window — so under A4.2 they date nothing about this event and set no level.
   > The worst single case in the corpus was removed by a rule aimed at something else, which
   > is evidence for the two rules being independent rather than redundant: of the 33 events
   > Amendment 3 excludes and the 55 Amendment 4 excludes, only **3** are in both, and this is
   > one of them.
3. **Five of China's critical-minerals export controls name no counterparty.**
   `chn_gage_2023`, `chn_graphite_2023`, `chn_re_tech_2023`, `chn_antimony_2024` and
   `chn_re_magnets_2025` are licensing regimes stated as national-security policy, with no
   country in the measure and none in the coded entities — while `chn_ban_us_2024` (which
   names the United States) and `chn_5minerals_2025` (explicit retaliation for US tariffs)
   do name one. The same programme is half coded as statecraft and half not. They are
   `ambiguous`, and the fix is a record fix, not a target fix.

**Against the first pass's own conclusion.** The first pass said the non-hostile share was
"flat at about one in nine from 2000 on". Across all four classes it is higher and rises:
18% of all 187 events are not G-scorable, and by decade the 2010s and 2020s run at 20% and
18%. The earlier sentence was true of the two classes it described and is superseded here.

**Verified count: 20 non-hostile, 13 ambiguous, 3 hostile-but-unattributed, 151 hostile, of
187 — 33 events (18%) not G-scorable.**

## 3. Every event, with its evidence
Coding values are Amendment 3 §A3.3; rules (a)–(d) cited in the evidence are Amendment 3.2.
`·de-escalatory` marks a row that is G-scorable under 3.2(b) — relief or settlement inside a
live adversarial dyad — so the direction of the act is never lost inside a `hostile` value.
The IES-90 column is the level the event carries **today**, with its basis and the rule that
fired: what the precondition would remove or keep, not a new computation. `—` is
`no_independent_outcome`, which since Amendment 4 has **two** reasons, distinguished by the
rule: `UNCOVERED` (no source covers the window, basis `uncovered`) and `UNDATED.continuation`
(a source *does* cover it but records only a conflict it cannot date inside the window — basis
`undated`).

> **Regenerated 2026-09-03 from `event_outcomes`, by Session K, on Joe's ruling.** Session F
> built this audit and no longer exists; the column is K's because K's Amendment 4 is what
> stranded it. **59 of 187 labels moved** under that amendment and 3 more changed basis or rule
> only, so the column was rebuilt from the database rather than patched at the one row
> `tests/test_hostility.py::test_rows_match_the_database` happened to name — hand-fixing that
> row would have left 58 silently wrong. Every row whose label moved carries a dated note
> saying so; **the hostility coding and the evidence prose are Session F's and are untouched**,
> including where a new label now contradicts the reasoning beside it. Those contradictions are
> marked, not reconciled.

### infrastructure_attack — 48 events (40 hostile, 3 hostile-unattributed, 2 ambiguous, 3 non-hostile)

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `abqaiq_arabian_1977` | 1977-05-11 | **non_hostile** | 0 (location, `NONE.covered`) | Accidental fire: a buried 30-inch crude line failed at the Abqaiq gathering centre, the leak reached a power substation and ignited (vehicles the ignition source); 4 killed. Contemporaneous sabotage rumour (Palestinian satchel charges) was investigated and denied on the record by Aramco president Frank Jungers: 'Absolutely not. It was a pipeline failure.' (Washington Post 1977-05-13/14; Process Safety Integrity case file.) |
| `iran_oilworkers_strike_1978` | 1978-10-31 | **non_hostile** | 3 (location, `WAR.intra.location`) | A labour action: oil workers struck and exports stopped. No act was directed at anyone's infrastructure; the infrastructure_attack class fits nothing in the record. Political coercion in a revolution, but no force, no target, no attacking party. |
| `kharg_strikes_1985` | 1985-08-15 | **hostile** | — (undated, `UNDATED.continuation`) | Iraqi air raids on Iran's Kharg export terminal; named state actor, dyad Iraq-Iran. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `iraq_kharg_1986` | 1986-08-12 | **hostile** | — (undated, `UNDATED.continuation`) | Iraqi aircraft struck Iran's Sirri Island terminal; named state actor, dyad Iraq-Iran. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `kuwait_oil_fires_1991` | 1991-02-22 | **hostile** | — (undated, `UNDATED.continuation`) | Retreating Iraqi forces set 600-730 Kuwaiti wells alight. Named state actor, deliberate destruction of an adversary's infrastructure. Correctly classed -- a keyword scan on 'fire' flags it falsely. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `iraq_pipeline_north_2004` | 2004-08-03 | **hostile** | 1 (location, `MIDI.single.overlap`) | Insurgent bombing of the Kirkuk-Ceyhan line at Al-Fateha. Actor class named (Iraqi insurgency), no individual group. **[Amendment 4, 2026-09-03: this label moved 3 → 1.** The level is now set by `MIDI.single.overlap`. The reasoning to the left was written against the old label and is left as written.**]** |
| `iraq_pipeline_south_2004` | 2004-08-27 | **hostile_unattributed** | — (undated, `UNDATED.continuation`) | Sabotage of the southern export pipelines. The record says 'saboteurs' and names no party or movement; H1 holds, H2 fails. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `nigeria_mend_ea_2006` | 2006-01-11 | **hostile** | 0 (location, `NONE.covered`) | MEND sabotage and kidnapping in the Niger Delta; named armed movement. |
| `nigeria_mend_forcados_2006` | 2006-02-18 | **hostile** | 0 (location, `NONE.covered`) | MEND attack on Shell's Forcados terminal and pipelines; named armed movement. |
| `saudi_abqaiq_foiled_2006` | 2006-02-24 | **hostile** | 0 (location, `NONE.covered`) | Al-Qaeda suicide car-bomb attempt on Abqaiq, repelled by guards. Named group; an attempted attack is a hostile act (and IES-90 asks about W, not about damage). |
| `nigeria_mend_bonga_2008` | 2008-06-19 | **hostile** | 0 (location, `NONE.covered`) | MEND boarded Shell's Bonga FPSO 120 km offshore and forced a shutdown; named armed movement. |
| `btc_pipeline_blast_2008` | 2008-08-05 | **ambiguous** | 0 (dyadic, `NONE.covered`) | Cause genuinely contested and never settled: the PKK claimed the Refahiye explosion (Al Jazeera 2008-08-07); US intelligence later attributed it to Russian cyber-sabotage of the control system (Bloomberg 2014, Eurasianet); that account was in turn disputed by ICS security researchers; the fire incinerated the evidence and the Turkish investigation could not establish whether a bomb was used. Tie-break 1 keeps a contested perpetrator hostile only where every live account is a hostile act -- here a technical failure remains live, so ambiguous. |
| `nda_bonny_2016` | 2016-02-10 | **hostile** | — (undated, `UNDATED.continuation`) | Niger Delta Avengers attack on the Bonny/Soku gas line; named armed movement. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `nigeria_nda_forcados_2016` | 2016-02-14 | **hostile** | — (undated, `UNDATED.continuation`) | Niger Delta Avengers bombed the Trans Forcados subsea line; named armed movement. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `nigeria_nda_escravos_2016` | 2016-05-25 | **hostile** | — (undated, `UNDATED.continuation`) | Niger Delta Avengers destroyed Chevron's Escravos feed lines; named armed movement. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `fujairah_tanker_sabotage_2019` | 2019-05-12 | **hostile_unattributed** | — (undated, `UNDATED.continuation`) | Limpet mines damaged four tankers off Fujairah. Unambiguously a deliberate attack; the UAE/Saudi/Norwegian technical report named only 'a state actor' and the record here names no party. H1 holds, H2 fails. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
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
| `ukr_odesa_strike_2023` | 2023-07-18 | **hostile** | — (undated, `UNDATED.continuation`) | Russian missile and drone strikes on Odesa and Chornomorsk export terminals; named state actor, dyad Russia-Ukraine. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `ukr_izmail_strike_2023` | 2023-08-02 | **hostile** | — (undated, `UNDATED.continuation`) | Russian drone strikes on the Izmail Danube grain port; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `russia_ustluga_strike_2024` | 2024-01-21 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on Novatek's Ust-Luga terminal; named state actor, dyad Ukraine-Russia. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_tuapse_strike_2024a` | 2024-01-25 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on Rosneft's Tuapse refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_marlin_luanda_2024` | 2024-01-26 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi ballistic missile set the naphtha tanker Marlin Luanda ablaze; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_volgograd_strike_2024` | 2024-02-03 | **hostile** | — (undated, `UNDATED.continuation`) | SBU drones hit Lukoil's Volgograd refinery; named state agency. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_rubymar_2024` | 2024-02-18 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi missile crippled the Rubymar, which later sank; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `russia_refineries_strikes_2024` | 2024-03-13 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone campaign against Ryazan and Novoshakhtinsk; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_slavyansk_strike_2024` | 2024-03-17 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on the Slavyansk-on-Kuban refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_novorossiysk_depots_2024` | 2024-05-17 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike on the Novorossiysk oil depots and terminals; named state actor. |
| `me_mv_tutor_2024` | 2024-06-12 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi drone-boat and missile attack sank the MV Tutor; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_chios_lion_2024` | 2024-07-15 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi unmanned surface vessel damaged the tanker Chios Lion; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_tuapse_strike_2024b` | 2024-07-22 | **hostile** | 3 (location, `GED.location.ge250`) | Ukrainian drone strike set the Tuapse refinery on fire; named state actor. |
| `me_sounion_2024` | 2024-08-21 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi attacks disabled and set fire to the laden crude tanker Sounion; named movement, claimed. Correctly classed -- a keyword scan on 'ablaze'/'fire' flags it falsely. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_novoshakhtinsk_strike_2024` | 2024-12-19 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drones and missiles set the Novoshakhtinsk refinery ablaze; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_ryazan_strike_2025a` | 2025-01-24 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian mass drone strike on the Rosneft Ryazan refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_volgograd_strike_2025` | 2025-01-31 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on Lukoil's Volgograd refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `cpc_kropotkinskaya_drone_2025` | 2025-02-17 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on the CPC Kropotkinskaya pumping station; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_novokuibyshevsk_strike_2025` | 2025-03-10 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike on Rosneft's Novokuibyshevsk refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `codelco_elteniente_2025` | 2025-07-31 | **non_hostile** | 0 (location, `NONE.covered`) | Industrial accident: a seismically triggered underground collapse at Codelco's El Teniente killed workers and took the mine offline. No party, no act -- and a copper mine, not oil, so the class fits on neither axis. |
| `rus_saratov_strike_2025a` | 2025-08-11 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian drone strike halted the Rosneft Saratov refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_ryazan_strike_2025b` | 2025-09-05 | **hostile** | — (undated, `UNDATED.continuation`) | Repeat Ukrainian drone strike on the Ryazan refinery; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |

### chokepoint_disruption — 27 events (18 hostile, 0 hostile-unattributed, 3 ambiguous, 6 non-hostile)

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `tanker_war_1984` | 1984-03-27 | **hostile** | 2 (location, `MID.single.wholly`) | Iraqi attacks on Gulf shipping; the Tanker War. Named state actor, armed attack. **[Amendment 4, 2026-09-03: this label moved 3 → 2.** The level is now set by `MID.single.wholly`. The reasoning to the left was written against the old label and is left as written.**]** |
| `earnest_will_1987` | 1987-07-22 | **ambiguous** | 1 (location, `MID.single.onset`) | A protective naval operation: the US reflagged Kuwaiti tankers and escorted them. A display of force by a named state, but defensive escort, not an act directed at an adversary. Tie-break 2 of A3.3 puts a protective deployment outside H1; it is listed rather than coded hostile because a display of force is inside IES-90's own level 1. **[Amendment 4, 2026-09-03: this label moved 3 → 1.** The level is now set by `MID.single.onset`. The reasoning to the left was written against the old label and is left as written.**]** |
| `bridgeton_mine_strike_1987` | 1987-07-24 | **hostile** | 2 (location, `ICB.single.wholly`) | The reflagged tanker Bridgeton struck an IRGC mine near Farsi Island. Mining a transit lane is a hostile act; actor named (Iran). **[Amendment 4, 2026-09-03: this label moved 3 → 2.** The level is now set by `ICB.single.wholly`. The reasoning to the left was written against the old label and is left as written.**]** |
| `suez_tropic_brilliance_2004` | 2004-11-08 | **non_hostile** | 0 (location, `NONE.covered`) | Navigational accident: the 89,000-tonne tanker lodged crosswise near Ismailiya and closed the canal for three days. No party, no act. |
| `hormuz_iran_threat_2011` | 2011-12-27 | **hostile** | 0 (location, `NONE.covered`) | Iran's vice-president threatened to close Hormuz against looming sanctions. An explicit threat of force by a named state -- inside H1 by its own terms, and level 1 of IES-90 is 'threat or display of force'. |
| `libya_jathran_blockade_2013` | 2013-08-01 | **ambiguous** | 0 (location, `NONE.covered`) | Armed Petroleum Facilities Guard units under Ibrahim Jathran shut Es Sider, Ras Lanuf and Zueitina over a revenue dispute with Tripoli. Armed coercion by a named party, but a domestic pay-and-autonomy dispute by the very force paid to guard the terminals; the cited source calls them protesters. Between armed blockade and industrial action, and listed as such. |
| `kirkuk_ceyhan_isis_2014` | 2014-03-02 | **hostile** | — (undated, `UNDATED.continuation`) | Repeated ISIS bombing of the Iraqi leg of the Kirkuk-Ceyhan line; named armed group. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `libya_ports_clashes_2014` | 2014-12-14 | **hostile** | — (undated, `UNDATED.continuation`) | Armed fighting between rival Libyan factions at the eastern terminals closed them. Hostile act; the parties are factions in a civil war, named as classes. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `bab_el_mandeb_houthi_tanker_2018` | 2018-04-03 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi attack on a Saudi crude tanker off Hodeidah; named movement, dyad Yemen(Houthi)-Saudi Arabia. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `saudi_suspends_bab_el_mandeb_2018` | 2018-07-25 | **ambiguous** | 0 (dyadic, `NONE.covered`) | The coded event is Riyadh's own decision to suspend crude transit after Houthi attacks on two of its tankers. The hostile act is the antecedent attack, not the suspension; tie-break 2 puts a precautionary state decision outside H1. Listed rather than coded non_hostile because the record folds the attacks into the same row. |
| `venezuela_blackout_2019` | 2019-03-07 | **non_hostile** | 0 (location, `NONE.covered`) | Nationwide grid collapse shut the Jose terminal and the Orinoco upgraders. The Maduro government alleged US and opposition sabotage; no evidence for it was produced and the sourced account is a power-system failure. Coded non_hostile with the allegation on the record. |
| `druzhba_contamination_2019` | 2019-04-20 | **non_hostile** | — (undated, `UNDATED.continuation`) | Deliberate, but crime for private gain, not an act against an adversary: organic-chloride crude was injected at a private collection point in Samara to cover the months-long theft of on-spec crude; eight arrests including four Transneft Druzhba employees, two fled abroad (Russian Investigative Committee; Meduza 2019-05-08; OSW; Oxford Energy Comment 2019-06). Tie-break 3 applies. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `grace1_seizure_2019` | 2019-07-04 | **hostile** | 0 (location, `NONE.covered`) | Royal Marines boarded and seized the laden tanker Grace 1 off Gibraltar. A forcible state seizure of another state's cargo is a militarized action in the MID sense, whatever its legal basis; named state actor, and it drew a reciprocal seizure. |
| `stena_impero_seizure_2019` | 2019-07-19 | **hostile** | 1 (location, `ICB.single.onset`) | IRGC seized the UK-flagged Stena Impero in Hormuz; named state actor, direct interference with transit. |
| `libya_haftar_blockade_2020` | 2020-01-18 | **hostile** | 3 (location, `GED.location.ge250`) | Pro-Haftar forces blockaded the eastern terminals and southern fields, cutting output from ~1.2 to ~0.32 mb/d. Armed blockade by a named party in a civil war. |
| `hankuk_chemi_seizure_2021` | 2021-01-04 | **hostile** | 0 (location, `NONE.covered`) | IRGC seized the tanker Hankuk Chemi in Hormuz; named state actor. |
| `suez_ever_given_2021` | 2021-03-23 | **non_hostile** | 0 (location, `NONE.covered`) | Navigational accident: the container ship grounded and blocked the canal. No party, no act. Missed by a keyword scan because the record says neither fire nor storm nor collapse. |
| `mercer_street_2021` | 2021-07-29 | **hostile** | 0 (location, `NONE.covered`) | One-way drone strike on the tanker Mercer Street off Oman, two killed; attributed to Iran by the US and UK and denied. Every live account is an attack -- tie-break 1. |
| `cpc_novorossiysk_storm_2022` | 2022-03-23 | **non_hostile** | 0 (location, `NONE.covered`) | Natural hazard: storm damage to the single-point moorings stopped loadings at the CPC Black Sea terminal. No party, no act. |
| `kurdistan_ceyhan_halt_2023` | 2023-03-25 | **non_hostile** | 2 (location, `GED.location.ge25`) | A legal and commercial action: Turkey stopped the Kirkuk-Ceyhan pipeline in compliance with an ICC arbitration award against it in Iraq's favour. A state act, but adjudicated dispute settlement, not an act directed adversarially. Fails H1. |
| `me_galaxy_leader_2023` | 2023-11-19 | **hostile** | — (undated, `UNDATED.continuation`) | Houthi helicopter raid seized the car carrier Galaxy Leader in the southern Red Sea; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `red_sea_attacks_2023` | 2023-12-01 | **hostile** | 3 (location, `GED.location.ge250`) | The Houthi campaign against commercial shipping at Bab el-Mandeb; named movement. |
| `me_maersk_diversions_2023` | 2023-12-15 | **hostile** | 3 (location, `GED.location.ge250`) | A Houthi drone strike near Bab el-Mandeb; the diversions are its consequence, and the coded act is the attack. |
| `redsea_houthi_resume_2025` | 2025-07-06 | **hostile** | — (undated, `UNDATED.continuation`) | Renewed Houthi attacks near Bab el-Mandeb, sinking the Magic Seas; named movement, claimed. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_druzhba_strike_2025a` | 2025-08-18 | **hostile** | — (undated, `UNDATED.continuation`) | Ukrainian strikes on the Unecha Druzhba pumping hub halted flows to Hungary and Slovakia; named state actor. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `rus_novorossiysk_terminal_2025` | 2025-11-14 | **hostile** | — (uncovered, `UNCOVERED`) | Ukrainian drone strike on the Sheskharis complex halted loadings at Novorossiysk; named state actor. |
| `hormuz_closure_2026` | 2026-03-04 | **hostile** | — (uncovered, `UNCOVERED`) | Iran declared Hormuz closed and attacked transiting tankers; named state actor. |

### conflict_escalation — 55 events (44 hostile, 0 hostile-unattributed, 3 ambiguous, 8 non-hostile)

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `yom_kippur_war_1973` | 1973-10-06 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Egypt and Syria attacked Israel across the Suez Canal and the Golan; named states, armed attack. |
| `shah_leaves_iran_1979` | 1979-01-16 | **ambiguous** | 3 (location, `WAR.intra.location`) | The coded act is a ruler leaving the country. Amendment 3.2(d): a political turning point inside a revolution, not itself an act of force. The conflict around it is unambiguous; this row is not. |
| `iran_revolution_1979` | 1979-02-11 | **hostile** | 3 (location, `WAR.intra.location`) | The Revolution culminates: armed uprising overthrowing a state, with the army's resistance collapsing in street fighting. 3.2(d); parties identified as classes. |
| `iran_hostage_crisis_1979` | 1979-11-04 | **hostile** | — (undated, `UNDATED.continuation`) | Seizure of the US embassy and its staff by an identified party (the students, with state acquiescence) against a state. Forcible seizure, one of H1's own examples. **[Amendment 4, 2026-09-03: this label moved 0 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `iran_iraq_war_1980` | 1980-09-22 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Iraq launched ground and air attacks on Iranian territory; named states. |
| `praying_mantis_1988` | 1988-04-18 | **hostile** | 2 (dyadic, `MID.pair.wholly`) | US forces destroyed two Iranian oil platforms and sank Iranian vessels; named states, use of force. |
| `iran_air_655_1988` | 1988-07-03 | **hostile** | 0 (dyadic, `NONE.covered`) | USS Vincennes downed Iran Air 655. The missile launch was a deliberate use of force by a named state inside a live adversarial dyad during a combat engagement; the target identification was mistaken, the act was not accidental in H1's sense. |
| `iraq_invades_kuwait_1990` | 1990-08-02 | **hostile** | 3 (dyadic, `WAR.inter.pair`) | Invasion; named states. |
| `desert_storm_air_campaign_1991` | 1991-01-17 | **hostile** | 1 (dyadic, `MID.pair.onset`) | Coalition air war on Iraq; named states. **[Amendment 4, 2026-09-03: this label moved 3 → 1.** The level is now set by `MID.pair.onset`. The reasoning to the left was written against the old label and is left as written.**]** |
| `operation_desert_fox_1998` | 1998-12-16 | **hostile** | 2 (dyadic, `MIDI.pair.overlap`) | US and UK airstrikes on Iraqi weapons and military targets, ordered on the record; named states. |
| `september_11_attacks_2001` | 2001-09-11 | **hostile** | 3 (location, `WAR.inter.single`) | Coordinated attacks on the US by a named movement. (The record notes Joe may reclassify the type as demand_shock; that is a class question, not a hostility question, and is left alone.) |
| `iraq_war_begins_2003` | 2003-03-20 | **hostile** | 3 (dyadic, `MIDI.pair.overlap,WAR.inter.pair`) | Invasion of Iraq; named states. |
| `nigeria_warri_shutin_2003` | 2003-03-23 | **hostile** | 0 (location, `NONE.covered`) | Ijaw militia attacks forced evacuation and shut-in of ~800 kb/d; named armed group. |
| `israel_hezbollah_war_2006` | 2006-07-12 | **hostile** | 2 (dyadic, `MIDI.pair.overlap`) | Hezbollah cross-border raid triggering a 34-day war; named parties. |
| `turkey_pkk_incursion_2008` | 2008-02-21 | **hostile** | 2 (dyadic, `MIDI.pair.overlap`) | Turkish ground incursion into northern Iraq; named state. |
| `russia_georgia_war_2008` | 2008-08-08 | **hostile** | 2 (dyadic, `MIDI.pair.overlap`) | Russian invasion of Georgia; named states. |
| `egypt_revolution_2011` | 2011-01-25 | **hostile** | 0 (location, `NONE.covered`) | Mass uprising against the state, lethally repressed (roughly 850 killed) and ending in Mubarak's removal. Amendment 3.2(d): armed uprising and state violence, parties identified as classes. The record's framing as 'unrest threatening Suez transit' understates the event -- flagged to E. |
| `libya_civil_war_2011` | 2011-02-17 | **hostile** | 3 (location, `GED.location.ge250`) | Uprising escalating into civil war; parties identified. |
| `escondida_strike_2011` | 2011-07-21 | **non_hostile** | 0 (location, `NONE.covered`) | A two-week union work stoppage at a copper mine. Amendment 3.2(c): the counterparty is the employer. No adversary, no state, no act of force. |
| `sudan_heglig_war_2012` | 2012-04-10 | **hostile** | 2 (location, `MIDI.single.overlap`) | South Sudan's army captured Heglig; cross-border fighting between named states. **[Amendment 4, 2026-09-03: this label moved 3 → 2.** The level is now set by `MIDI.single.overlap`. The reasoning to the left was written against the old label and is left as written.**]** |
| `marikana_strike_2012` | 2012-08-16 | **ambiguous** | 0 (location, `NONE.covered`) | The record bundles two things: a wildcat wage strike (the supply mechanism, 3.2(c) non-hostile) and police killing 34 strikers (lethal force by an identified state party, H1). The coded event is the strike; the massacre is what makes it a conflict record. Named as ambiguous rather than forced either way. |
| `egypt_coup_suez_2013` | 2013-07-03 | **hostile** | 0 (location, `NONE.covered`) | Military removal of a sitting president, with lethal repression following. 3.2(d). |
| `sa_platinum_strike_2014` | 2014-01-23 | **non_hostile** | 0 (location, `NONE.covered`) | A five-month AMCU wage strike across three platinum producers. 3.2(c). |
| `mosul_isis_offensive_2014` | 2014-06-10 | **hostile** | 2 (location, `MIDI.single.overlap`) | ISIS overran Mosul; named armed group taking territory. 3.2(d). **[Amendment 4, 2026-09-03: this label moved 3 → 2.** The level is now set by `MIDI.single.overlap`. The reasoning to the left was written against the old label and is left as written.**]** |
| `libya_essider_clashes_2014` | 2014-12-13 | **hostile** | — (undated, `UNDATED.continuation`) | Armed fighting near the two largest export terminals; parties identified as factions. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `saudi_intervention_yemen_2015` | 2015-03-26 | **hostile** | 0 (dyadic, `NONE.covered`) | Saudi-led coalition air campaign in Yemen; named states. |
| `escondida_strike_2017` | 2017-02-09 | **non_hostile** | 0 (location, `NONE.covered`) | A 44-day union strike at the world's largest copper mine. 3.2(c). |
| `kirkuk_seizure_2017` | 2017-10-16 | **hostile** | — (undated, `UNDATED.continuation`) | Iraqi forces retook Kirkuk from Kurdish control by military action; named parties. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `libya_oil_crescent_2018` | 2018-06-14 | **hostile** | 0 (location, `NONE.covered`) | Fighters under Jedran stormed and closed the Es Sider and Ras Lanuf terminals; armed seizure by a named party. |
| `libya_sharara_2018` | 2018-12-08 | **hostile** | 2 (location, `GED.location.ge25`) | Armed tribesmen seized the 315,000 b/d El Sharara field, forcing force majeure; armed seizure. |
| `lasbambas_blockade_2019` | 2019-02-02 | **non_hostile** | 0 (location, `NONE.covered`) | A 60-day community road blockade over haulage through local land. 3.2(c): the counterparty is the mine operator. |
| `iraq_nasiriya_2019` | 2019-12-28 | **ambiguous** | — (undated, `UNDATED.continuation`) | Anti-government protesters cut power and shut the field. The coded act is an unarmed protest occupation (3.2(c) shape), but it sits inside Iraq's Tishreen uprising, which the state repressed lethally (3.2(d) shape). The record does not settle which the row is about. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `soleimani_strike_2020` | 2020-01-03 | **hostile** | — (undated, `UNDATED.continuation`) | US strike killing an Iranian commander; named states. **[Amendment 4, 2026-09-03: this label moved 0 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `lasbambas_halt_2021` | 2021-09-27 | **non_hostile** | 0 (location, `NONE.covered`) | Community road blockades forced the operator to halt the mine. 3.2(c). |
| `kazakhstan_unrest_2022` | 2022-01-05 | **hostile** | 0 (location, `NONE.covered`) | The record's 'nationwide unrest over fuel prices' understates it: 227 killed including 19 police, 4,353 injured, security forces firing on crowds in Almaty on 5-6 January, and a CSTO military deployment (Kazakh prosecutors via Al Jazeera 2022-01-15; IPHR; Crisis Group). Amendment 3.2(d): a violently repressed uprising with a foreign troop deployment, parties identified. Understatement flagged to E. |
| `russia_invades_ukraine_2022` | 2022-02-24 | **hostile** | 3 (location, `GED.location.ge250`) | Full-scale invasion; named states. |
| `cuajone_shutdown_2022` | 2022-03-14 | **non_hostile** | 0 (location, `NONE.covered`) | A community blockade of the reservoir and rail line suspended the mine for over 50 days. 3.2(c). |
| `peru_lasbambas_2022` | 2022-04-20 | **non_hostile** | 0 (location, `NONE.covered`) | Community members occupied the property and the operator suspended output. 3.2(c). |
| `tw_pelosi_drills_2022` | 2022-08-04 | **hostile** | 0 (location, `NONE.covered`) | Live-fire drills and missile launches encircling Taiwan, closing shipping zones: a display of force by a named state, which is one of H1's own examples. |
| `grain_deal_collapse_2023` | 2023-07-17 | **hostile** | — (undated, `UNDATED.continuation`) | Russia withdrew from the Black Sea Grain Initiative, closing safe passage for Ukrainian grain in an active war. A coercive act by a named state against an adversary; 3.2(a). **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `gabon_coup_2023` | 2023-08-30 | **hostile** | 0 (location, `NONE.covered`) | Army officers seized power, placed President Bongo under house arrest and arrested his son; gunfire in Libreville (CNN, Al Jazeera, CNBC 2023-08-30). 3.2(d); no deaths reported does not make a coup non-hostile. |
| `israel_hamas_war_2023` | 2023-10-07 | **hostile** | 3 (location, `GED.location.ge250`) | Hamas attack on Israel and the onset of the Gaza war; named parties. |
| `me_us_uk_strikes_2024` | 2024-01-11 | **hostile** | — (undated, `UNDATED.continuation`) | About 70 US and UK strikes on Houthi sites; named states. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_damascus_consulate_2024` | 2024-04-01 | **hostile** | 2 (location, `GED.location.ge25`) | Israeli airstrike destroying Iran's Damascus consulate and killing IRGC commanders; attribution to Israel is universal though unclaimed at the time. |
| `iran_strikes_israel_apr_2024` | 2024-04-13 | **hostile** | — (undated, `UNDATED.continuation`) | 300+ Iranian drones and missiles fired at Israel; named states, claimed. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_haniyeh_2024` | 2024-07-31 | **hostile** | 2 (location, `GED.location.ge25`) | Assassination of Hamas's leader in Tehran; attributed to Israel and unclaimed -- every live account is a killing, so tie-break 1 keeps it hostile. |
| `escondida_strike_2024` | 2024-08-13 | **non_hostile** | 0 (location, `NONE.covered`) | Union workers struck after wage talks collapsed. 3.2(c). |
| `me_nasrallah_2024` | 2024-09-27 | **hostile** | 2 (location, `GED.location.ge25`) | Israeli airstrike killing Hezbollah's leader in Beirut; named state, claimed. |
| `iran_strikes_israel_oct_2024` | 2024-10-01 | **hostile** | — (undated, `UNDATED.continuation`) | About 180 Iranian ballistic missiles fired at Israel; named states, claimed. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `myanmar_re_seizure_2024` | 2024-10-20 | **hostile** | — (undated, `UNDATED.continuation`) | The Kachin Independence Army seized the rare-earth mining towns; named armed movement taking territory. 3.2(d). **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `me_days_of_repentance_2024` | 2024-10-26 | **hostile** | 2 (location, `GED.location.ge25`) | Israeli strikes on Iranian military sites; named states, claimed. |
| `me_rough_rider_2025` | 2025-03-15 | **hostile** | 3 (location, `GED.location.ge250`) | Large-scale US air campaign against the Houthis; named state. |
| `israel_iran_war_2025` | 2025-06-13 | **hostile** | 3 (location, `GED.location.ge250`) | Israeli air campaign against Iran opening a 12-day war; named states. |
| `me_midnight_hammer_2025` | 2025-06-22 | **hostile** | — (undated, `UNDATED.continuation`) | US strikes on three Iranian nuclear sites; named state. **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `iran_israel_us_strike_2026` | 2026-02-28 | **hostile** | — (uncovered, `UNCOVERED`) | US and Israeli strikes on Iran; named states. |

### sanctions — 57 events (49 hostile, 0 hostile-unattributed, 5 ambiguous, 3 non-hostile)

| event_id | date | hostility | IES-90 | evidence for the coding |
|---|---|---|---|---|
| `oapec_embargo_1973` | 1973-10-17 | **hostile** | 0 (dyadic, `NONE.covered`) | Arab producers cut output and threatened a total embargo on the US, tied to Israeli withdrawal. 3.2(a): non-kinetic coercion by named states against a named state. |
| `embargo_lifted_1974` | 1974-03-18 | **hostile** ·de-escalatory | 0 (dyadic, `NONE.covered`) | The embargo on the US lifted, conditionally and partially. 3.2(b): a de-escalatory act inside the same identified adversarial dyad; the level and the DEAL flag are both defined for it. |
| `iraq_un_661_embargo_1990` | 1990-08-06 | **hostile** | 3 (location, `WAR.inter.single`) | UN comprehensive sanctions and a total oil embargo on Iraq after the invasion of Kuwait. 3.2(a). |
| `iraq_un_986_ofp_1995` | 1995-04-14 | **hostile** ·de-escalatory | 2 (location, `MIDI.single.overlap`) | UNSCR 986 permitting limited Iraqi exports, easing the total embargo. 3.2(b). |
| `iran_eo12959_embargo_1995` | 1995-05-06 | **hostile** | 0 (location, `NONE.covered`) | EO 12959, a total US trade and investment embargo on Iran. 3.2(a). |
| `ilsa_sanctions_1996` | 1996-08-05 | **hostile** | 0 (dyadic, `NONE.covered`) | ILSA: US secondary sanctions on foreign firms investing in Iranian and Libyan petroleum. 3.2(a). |
| `iraq_ofp_exports_begin_1996` | 1996-12-10 | **hostile** ·de-escalatory | 3 (location, `GED.location.ge250`) | First Iraqi exports under oil-for-food, returning capped volumes to market. 3.2(b). |
| `iraq_oil_export_ban_2002` | 2002-04-08 | **hostile** | 2 (location, `MIDI.single.overlap`) | Iraq halted ~1.8 mb/d of its own exports for 30 days to protest Israel's West Bank incursion. A producer restricting exports, but explicitly as a political act against a named adversary -- 3.2(a), not 3.2(c). |
| `iraq_sanctions_lifted_2003` | 2003-05-22 | **hostile** ·de-escalatory | 1 (location, `MIDI.single.overlap`) | UNSCR 1483 lifting economic sanctions on Iraq. 3.2(b). |
| `libya_sanctions_lifted_2004` | 2004-04-23 | **hostile** ·de-escalatory | 0 (location, `NONE.covered`) | ILSA application terminated and sanctions eased after Libya's WMD renunciation. 3.2(b). |
| `iran_cisada_2010` | 2010-07-01 | **hostile** | 2 (location, `MIDI.single.overlap,GED.location.ge25`) | CISADA penalising suppliers to Iran's refined-petroleum and petroleum-investment sectors. 3.2(a). |
| `sanc_2011_11_21` | 2011-11-21 | **hostile** | 2 (location, `MID.single.wholly,MIDI.single.overlap`) | EO 13590 authorising sanctions on suppliers to Iran's petroleum and petrochemical sectors. 3.2(a). |
| `ndaa_cbi_sanctions_2011` | 2011-12-31 | **hostile** | 1 (dyadic, `MIDI.pair.overlap`) | NDAA s.1245 blocking the Central Bank of Iran and threatening third-country banks. 3.2(a). |
| `eu_iran_oil_embargo_2012` | 2012-01-23 | **hostile** | 2 (location, `MIDI.single.overlap`) | EU Council Decision banning import, purchase and transport of Iranian crude. 3.2(a). |
| `swift_cutoff_iran_2012` | 2012-03-15 | **hostile** | 2 (location, `MID.single.wholly,MIDI.single.overlap`) | SWIFT disconnecting 30 Iranian banks under EU directive. 3.2(a). |
| `sanc_2013_11_24` | 2013-11-24 | **hostile** ·de-escalatory | 2 (location, `MIDI.single.overlap`) | The JPOA interim deal pausing further cuts to Iranian exports. 3.2(b). |
| `russia_sectoral_sanctions_2014` | 2014-07-16 | **hostile** | 2 (location, `MIDI.single.overlap`) | First US sectoral sanctions on Russian energy financing under EO 13662. 3.2(a). |
| `russia_oiltech_ban_2014` | 2014-09-12 | **hostile** | 2 (location, `MIDI.single.overlap`) | US and EU ban on Arctic, deepwater and shale oil technology and services for Russia. 3.2(a). |
| `iran_jcpoa_agreed_2015` | 2015-07-14 | **hostile** ·de-escalatory | 0 (location, `NONE.covered`) | The JCPOA agreed, opening the path to lifting oil sanctions. 3.2(b): the clearest case for the de-escalatory rule -- a negotiated settlement inside a live dyad, exactly what the DEAL flag measures. |
| `iran_implementation_day_2016` | 2016-01-16 | **hostile** ·de-escalatory | 0 (location, `NONE.covered`) | IAEA verification and the lifting of nuclear-related oil sanctions. 3.2(b). |
| `qatar_gulf_blockade_2017` | 2017-06-05 | **hostile** | 0 (location, `NONE.covered`) | Saudi Arabia, the UAE, Egypt and Bahrain cut ties and closed land, air and sea links to Qatar. A blockade by named states against a named state. |
| `venezuela_financial_sanctions_2017` | 2017-08-25 | **hostile** | 0 (dyadic, `NONE.covered`) | EO 13808 barring dealings in new PDVSA and government debt. 3.2(a). |
| `iran_sanctions_reimposed_2018` | 2018-05-08 | **hostile** | 0 (dyadic, `NONE.covered`) | US withdrawal from the JCPOA and signalled restoration of oil sanctions. 3.2(a). |
| `iran_metals_windown_2018` | 2018-08-06 | **hostile** | 0 (location, `NONE.covered`) | First tranche of reimposed US sanctions on Iran taking effect. 3.2(a). |
| `iran_oil_snapback_2018` | 2018-11-05 | **hostile** | 1 (location, `ICB.single.onset`) | US energy, shipping and banking sanctions reimposed on Iran with eight waivers. 3.2(a). |
| `venezuela_sanctions_2019` | 2019-01-28 | **hostile** | — (undated, `UNDATED.continuation`) | US sanctions on PDVSA exports. 3.2(a). **[Amendment 4, 2026-09-03: this label moved 0 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `sanc_2019_04_08` | 2019-04-08 | **hostile** | 1 (location, `ICB.single.onset`) | US designation of the IRGC as a Foreign Terrorist Organization. 3.2(a). |
| `us_ends_iran_waivers_2019` | 2019-04-22 | **hostile** | 1 (dyadic, `ICB.pair.onset`) | US ends all significant-reduction exceptions for buyers of Iranian crude. 3.2(a). |
| `iran_pgpic_sanctions_2019` | 2019-06-07 | **hostile** | 2 (location, `GED.location.ge25`) | OFAC designation of Iran's largest petrochemical group and 39 subsidiaries. 3.2(a). |
| `venezuela_asset_freeze_2019` | 2019-08-05 | **hostile** | 0 (dyadic, `NONE.covered`) | EO 13884 blocking all Venezuelan government property. 3.2(a). |
| `indonesia_nickel_ban_2019` | 2019-09-02 | **non_hostile** | 0 (location, `NONE.covered`) | Indonesia banned nickel ore exports two years early to force downstream smelting at home. 3.2(c): industrial policy with no adversary; the counterparty is the world ore market. |
| `rosneft_trading_venez_2020` | 2020-02-18 | **hostile** | 0 (location, `NONE.covered`) | OFAC designation of Rosneft Trading for handling Venezuelan crude. 3.2(a). |
| `indonesia_palm_ban_2022` | 2022-04-28 | **non_hostile** | 0 (location, `NONE.covered`) | Palm-oil export ban to curb domestic cooking-oil prices. 3.2(c): a domestic price measure, no adversary. |
| `sanc_2022_06_03` | 2022-06-03 | **hostile** | 0 (location, `NONE.covered`) | EU sixth package banning seaborne imports of Russian crude and products. 3.2(a). |
| `sanc_2022_10_06` | 2022-10-06 | **hostile** | 2 (location, `GED.location.ge25`) | EU eighth package establishing the legal basis for the G7 price cap. 3.2(a). |
| `us_chips_2022` | 2022-10-07 | **hostile** | 0 (location, `NONE.covered`) | US export controls on advanced computing chips and chipmaking equipment, with a foreign-direct-product rule, aimed at China's AI and supercomputing capability. The target state is named in the measure. 3.2(a). |
| `eu_embargo_price_cap_2022` | 2022-12-05 | **hostile** | 0 (location, `NONE.covered`) | EU seaborne embargo and the G7 $60 price cap entering force. 3.2(a). |
| `products_price_cap_2023` | 2023-02-05 | **hostile** | 0 (location, `NONE.covered`) | G7 price cap extended to Russian refined products. 3.2(a). |
| `chn_gage_2023` | 2023-07-03 | **ambiguous** | 0 (location, `NONE.covered`) | MOFCOM export licensing on gallium and germanium, stated on the record as protecting 'national security and interests' under the 2020 Export Control Law and naming no country (MOFCOM press conference 2023-07-06), and read universally as retaliation for the US chip controls of October 2022 (CSIS, Stimson, ORF America). Adversarial in effect, industrial-security in form; the record does not settle which, so it is not settled here. |
| `venezuela_gl44_relief_2023` | 2023-10-18 | **hostile** ·de-escalatory | 0 (location, `NONE.covered`) | OFAC GL 44 authorising Venezuelan oil transactions after the Barbados agreement. 3.2(b). |
| `chn_graphite_2023` | 2023-10-20 | **ambiguous** | 0 (location, `NONE.covered`) | MOFCOM export permits for graphite, framed as licensing and naming no counterparty. Same shape as chn_gage_2023. |
| `russia_pricecap_enforce_2023` | 2023-11-16 | **hostile** | — (undated, `UNDATED.continuation`) | OFAC sanctions on three Sovcomflot tankers for breaching the price cap. 3.2(a). **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `chn_re_tech_2023` | 2023-12-21 | **ambiguous** | 0 (location, `NONE.covered`) | China banned export of rare-earth extraction, separation and magnet technology. No counterparty named; strategic leverage in effect. Same shape as chn_gage_2023. |
| `sanc_2024_02_23` | 2024-02-23 | **hostile** | — (undated, `UNDATED.continuation`) | OFAC designation of Sovcomflot and 14 crude tankers under EO 14024. 3.2(a). **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `russia_metals_ban_2024` | 2024-04-12 | **hostile** | — (undated, `UNDATED.continuation`) | Coordinated US and UK prohibition on Russian aluminium, copper and nickel at the LME and CME. 3.2(a). **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `venezuela_gl44_revoked_2024` | 2024-04-17 | **hostile** | 0 (location, `NONE.covered`) | GL 44 allowed to lapse and oil sanctions reimposed after the blocked election. 3.2(a) -- a re-imposition, not relief. |
| `chn_antimony_2024` | 2024-08-15 | **ambiguous** | 0 (location, `NONE.covered`) | MOFCOM export licensing on antimony, no counterparty named. Same shape as chn_gage_2023. |
| `sanc_2024_10_11` | 2024-10-11 | **hostile** | 2 (location, `GED.location.ge25`) | OFAC determination widening secondary sanctions on Iran's petroleum sector after Iran's missile attack on Israel. 3.2(a). |
| `chn_ban_us_2024` | 2024-12-03 | **hostile** | 0 (location, `NONE.covered`) | China's first outright export ban naming the United States, on gallium, germanium, antimony and superhard materials. The counterparty is named in the measure, so 3.2(a) rather than the ambiguous licensing shape. |
| `russia_shadow_fleet_sanctions_2025` | 2025-01-10 | **hostile** | — (undated, `UNDATED.continuation`) | OFAC action against two Russian producers and 183 shadow-fleet tankers. 3.2(a). **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `chn_5minerals_2025` | 2025-02-04 | **hostile** | 0 (location, `NONE.covered`) | Export licensing on tungsten, tellurium, bismuth, indium and molybdenum, announced by the record as retaliation for new US tariffs, with the US coded as an actor on the event. Named counterparty, so 3.2(a). |
| `us_iran_maxpressure_2025` | 2025-02-05 | **hostile** | 0 (location, `NONE.covered`) | Presidential memorandum directing agencies to drive Iranian oil exports toward zero. 3.2(a). |
| `drc_cobalt_ban_2025` | 2025-02-22 | **non_hostile** | — (undated, `UNDATED.continuation`) | ARECOMS suspended all DRC cobalt exports for four months after prices fell to a nine-year low below $10/lb, to curb oversupply and defend price; extended three months in June 2025 for the same reason (ARECOMS decision 2025-02-22; IEA policy record; Project Blue). 3.2(c): a producer managing its own market -- the act of an opec_decision, filed under sanctions. **[Amendment 4, 2026-09-03: this label moved 3 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |
| `us_chevron_venez_2025` | 2025-02-26 | **hostile** | 0 (location, `NONE.covered`) | Revocation of Chevron's licence to operate in Venezuela. 3.2(a). |
| `us_venez_sectariff_2025` | 2025-03-24 | **hostile** | 0 (location, `NONE.covered`) | Order allowing 25% secondary tariffs on any country importing Venezuelan crude. 3.2(a). |
| `chn_re_magnets_2025` | 2025-04-04 | **ambiguous** | 0 (location, `NONE.covered`) | Case-by-case export licensing on seven medium and heavy rare earths and permanent magnets. Counterparty described only as Western manufacturers, not named in the measure. Same shape as chn_gage_2023. |
| `us_russia_sectariff_2025` | 2025-07-14 | **hostile** | — (undated, `UNDATED.continuation`) | Threatened 100% secondary tariffs on buyers of Russian energy within 50 days. An explicit threat of economic coercion against a named state; 3.2(a). **[Amendment 4, 2026-09-03: this label moved 2 → —.** Every record on the chosen basis is undated-for-W — a conflict already running at the event date, or a source that cannot place its level inside the window — so the target is not defined for this event (A4.2 rule 2). The reasoning to the left was written against the old label and is left as written.**]** |

## 4. The thirteen ambiguous, named as ambiguous
Not "probably hostile" or "probably not" — events where the record does not settle it.
Amendment 3 §A3.3 excludes them from G-scoring and lists them by name.

> **`ambiguous` is a terminal state, not a pending decision.** Ruled by Joe, 2026-09-02, and
> registered as `OUTCOME_MAPPING.md` Amendment 3.3. Under the sourced-or-unknown rule
> (SESSION_CHARTER §2.1) the record does not settle these thirteen, and adjudicating them
> anyway would supply a fact the evidence lacks — the same error as filling a `severity` to
> avoid a blank. **They are not a to-do. No later session should "resolve", "clear", "close
> out" or re-code them**, and none of them is a Joe gate. What can change one is *new
> evidence in the record* — a source that settles the cause, or a Session E patch that
> unbundles a row that holds two acts — never a judgement call made because the value is
> inconvenient. Until then the answer to "was this a hostile act?" is: the record does not
> say, and that is published as the answer.

| event | date | class | the two readings |
|---|---|---|---|
| `shah_leaves_iran_1979` | 1979-01-16 | conflict_escalation | The coded act is a ruler leaving the country — 3.2(d) makes a political turning point inside a revolution ambiguous, though the conflict around it is not. |
| `earnest_will_1987` | 1987-07-22 | chokepoint_disruption | **Display of force by a named state** (IES-90's own level 1) vs **a protective escort**, which tie-break 2 puts outside H1. |
| `btc_pipeline_blast_2008` | 2008-08-05 | infrastructure_attack | **PKK bombing / Russian cyber-sabotage** vs **technical failure**; never settled, evidence incinerated. |
| `marikana_strike_2012` | 2012-08-16 | conflict_escalation | The record bundles a **wildcat wage strike** (the supply mechanism, 3.2(c)) with **police killing 34 strikers** (lethal state force). The coded event is the strike; the massacre is what makes it a conflict record. |
| `libya_jathran_blockade_2013` | 2013-08-01 | chokepoint_disruption | **Armed blockade** by Petroleum Facilities Guard units vs **a revenue dispute** by the force paid to guard the terminals — the cited source calls them protesters. |
| `chn_gage_2023` | 2023-07-03 | sanctions | **Retaliation for the US chip controls** (every outside reading) vs **national-security licensing** (MOFCOM's own statement, naming no country). |
| `chn_graphite_2023` | 2023-10-20 | sanctions | As `chn_gage_2023`: a licensing regime with no counterparty named in the measure or in the coded entities. |
| `chn_re_tech_2023` | 2023-12-21 | sanctions | As `chn_gage_2023`. |
| `saudi_suspends_bab_el_mandeb_2018` | 2018-07-25 | chokepoint_disruption | The row folds **Houthi attacks on two Saudi tankers** together with **Riyadh's own decision to suspend transit**; the coded actor is Saudi Arabia, and tie-break 2 puts a precautionary decision outside H1. |
| `iraq_nasiriya_2019` | 2019-12-28 | conflict_escalation | An **unarmed protest occupation** of a field (3.2(c) shape) inside **the lethally repressed Tishreen uprising** (3.2(d) shape). |
| `colonial_pipeline_shutdown_2021` | 2021-05-07 | infrastructure_attack | **A directed ransomware attack** vs **extortion for private gain** (tie-break 3); the shutdown itself was Colonial's own precautionary decision. |
| `chn_antimony_2024` | 2024-08-15 | sanctions | As `chn_gage_2023`. |
| `chn_re_magnets_2025` | 2025-04-04 | sanctions | As `chn_gage_2023`; the counterparty is described only as Western manufacturers. |

**They are not thirteen unrelated hard cases — they are four repeating patterns**, which is
more useful to Joe than the list:
- **Five identical rows** (the China licensing measures) that one record fix would settle
  together: name the counterparty in the measure, or state that none is named.
- **Three rows that bundle an act with the response to it** (`saudi_suspends_bab_el_mandeb_2018`,
  `marikana_strike_2012`, `libya_jathran_blockade_2013`) — the codebook's date rule wants one
  dated act per row and these hold two.
- **Two rows that are a turning point inside a conflict rather than an act of force**
  (`shah_leaves_iran_1979`, `iraq_nasiriya_2019`).
- **Three genuinely unsettled causes** (`btc_pipeline_blast_2008`, `colonial_pipeline_shutdown_2021`,
  `earnest_will_1987`) — the only three where more record work would not help.

## 5. Counts by class and by decade

| class | hostile | hostile_unattributed | ambiguous | non_hostile | total | not G-scorable |
|---|---:|---:|---:|---:|---:|---:|
| `infrastructure_attack` | 40 | 3 | 2 | 3 | 48 | 5 (10%) |
| `chokepoint_disruption` | 18 | 0 | 3 | 6 | 27 | 9 (33%) |
| `conflict_escalation` | 44 | 0 | 3 | 8 | 55 | 11 (20%) |
| `sanctions` | 49 | 0 | 5 | 3 | 57 | 8 (14%) |
| **all four** | **151** | **3** | **13** | **20** | **187** | **33 (18%)** |

| decade | hostile | hostile_unattributed | ambiguous | non_hostile | total | not G-scorable |
|---|---:|---:|---:|---:|---:|---:|
| 1970s | 5 | 0 | 1 | 2 | 8 | 3 (38%) |
| 1980s | 7 | 0 | 1 | 0 | 8 | 1 (12%) |
| 1990s | 9 | 0 | 0 | 0 | 9 | 0 (0%) |
| 2000s | 14 | 1 | 1 | 1 | 17 | 2 (12%) |
| 2010s | 43 | 1 | 4 | 7 | 55 | 11 (20%) |
| 2020s | 73 | 1 | 6 | 10 | 90 | 16 (18%) |
| **all** | **151** | **3** | **13** | **20** | **187** | **33 (18%)** |

Three things in those tables that the totals alone do not say.

**The defect is not concentrated in the class named for attacks.** `infrastructure_attack` is
the *cleanest* of the four at 10% not-scorable. The worst is `chokepoint_disruption` at 33% —
a class defined by a *place* rather than an act, so anything that stops traffic through the
place qualifies — followed by `conflict_escalation` at 20%, which is high only because eight
mining strikes are filed in it. A reader who assumed the problem lived in the class that says
"attack" would have looked in the wrong place.

**The 1970s are the thinnest and the worst.** Eight events, three of them not G-scorable
(38%): the 1977 Abqaiq pipeline fire, the 1978 oil-workers' strike, and the Shah's departure.
Whatever the walk learns about the 1970s it learns from five hostile events.

**The share does not fall as the corpus modernises.** 20% in the 2010s, 18% in the 2020s,
against 12% in the 2000s and 0% in the 1990s. It rises, because the corpus's recent growth
brought in metals and minerals events — strikes, blockades, export bans — that were coded
into geopolitical classes for want of a better one. This is not a legacy-records problem.

## 6. Impact on the published walk — reported, not applied

> **[Amendment 4, 2026-09-03 — every figure in this section is on the PRE-Amendment-4 target
> and is NOT recomputed here.]** The 150 scored reads, the 42.0% level-0 share and the three
> exclusion rows below were all computed against the labels as they stood before the ongoing-
> conflict rule reached COW War and UCDP GED. Against the rebuilt target, **49 of the 172
> scored daily G reads leave the G target entirely** and 53 lose a knowable pre-window level.
> Recomputing this section now would mix a pre-amendment run's reads with a post-amendment
> target — the exact move A3.5 and A4.7 both forbid.
>
> **State at 2026-09-03 05:35Z, and why the two §6 tests are red.** Session B's run
> `walk_20260903T052633Z` — the first under Amendment 4 — has written all 313 rows to
> `reads/scores/weights.jsonl`, but `summary.json` still describes the previous run
> `walk_20260903T003422Z` (sealed 00:35Z, registration *"Amendment 1 + 1.1 + 2"*, 184 labels,
> G n 150). B is still computing the summary. So the scores file and the summary currently
> describe **different runs**, and `test_section_6_impact_recomputes_from_the_sealed_scores`
> and `test_section_6_set_matches_the_published_summary` fail on exactly that gap: the scores
> file's latest run carries **100** scored G reads, the published summary says 150. That is B's
> run landing, not a defect in this audit, and **§6 is deliberately left alone rather than
> restated against a run nobody has published yet.** When B's summary lands, §6 is recomputed
> from the scores file — which is what those two tests exist to force — and the pre- and
> post-amendment runs are reported separately, never pooled.
>
> Counts: `data/state/ies90_amendment4_counts.json`; handoff:
> `data/handoffs/K_to_F_2026-09-03_class_audit_stale.md`.

Amendment 3 §A3.5: **no published run is re-scored.** These numbers say how much of the
published G result rests on events for which the G target is undefined. They are an impact
statement for the paper's limitations section and a handoff to Session B for v3.

Set: the **150 daily-tier scored G reads** of the current published run — the reads that
passed burn-in and carry both an engine and a climatology G score, matching
`summary.json` `/tiers/daily/G/engine_vs/climatology/n` = 150. (Session B re-ran the walk
during this session; the run id changed, the set and every figure below did not. The audit
and its test read the run out of the scores file rather than naming it, so a re-run does not
silently invalidate this section — it recomputes it.)

| | n | level-0 | share |
|---|---:|---:|---:|
| **as published** | 150 | 63 | **42.0%** |
| excluding the 17 `non_hostile` (the Amendment 3 rule as registered) | 133 | 49 | **36.8%** |
| also excluding the 10 `ambiguous` | 123 | 40 | **32.5%** |
| also excluding the 2 `hostile_unattributed` (the strictest reading) | 121 | 40 | **33.1%** |

**Every diagnostic of this target publishes the level-0 share both with and without the
`ambiguous` events, as the table above does** — required by Amendment 3.3 §2 and asserted by
`tests/test_hostility.py::test_the_ambiguous_diagnostic_is_published_both_ways`. Because
`ambiguous` is terminal, the choice of whether to count those thirteen can never be settled by
evidence; publishing both figures is therefore not a courtesy but the only honest way to
report the target, and it lets a reader who disagrees with any single ambiguous coding read
off the other bound without a re-run. Neither figure is the headline: the registered rule
excludes `ambiguous` from G-scoring, so **36.8% is the share under Amendment 3** and 32.5% is
the bound that also drops them from the denominator.

**Affected: 27 of the 150 reads (18.0%)** — 17 non-hostile, 10 ambiguous. By class:

| class | scored G reads | non_hostile | ambiguous | affected |
|---|---:|---:|---:|---:|
| `infrastructure_attack` | 38 | 1 | 2 | 3 (8%) |
| `chokepoint_disruption` | 17 | 5 | 1 | 6 (35%) |
| `conflict_escalation` | 46 | 8 | 2 | 10 (22%) |
| `sanctions` | 49 | 3 | 5 | 8 (16%) |
| **all** | **150** | **17** | **10** | **27 (18%)** |

The 17 non-hostile reads, with the level each contributed — **the three non-zero ones are the
damage**:

| event | class | level |
|---|---|---:|
| `drc_cobalt_ban_2025` | sanctions | **3 — war** |
| `druzhba_contamination_2019` | chokepoint_disruption | **2** |
| `kurdistan_ceyhan_halt_2023` | chokepoint_disruption | **2** |
| `venezuela_blackout_2019`, `suez_ever_given_2021`, `cpc_novorossiysk_storm_2022`, `codelco_elteniente_2025`, `indonesia_nickel_ban_2019`, `indonesia_palm_ban_2022`, `escondida_strike_2011`, `sa_platinum_strike_2014`, `escondida_strike_2017`, `lasbambas_blockade_2019`, `lasbambas_halt_2021`, `cuajone_shutdown_2022`, `peru_lasbambas_2022` | (mixed) | 0 |

Six more affected events are outside the 150 on tier or burn-in — `abqaiq_arabian_1977`,
`iran_oilworkers_strike_1978`, `shah_leaves_iran_1979`, `earnest_will_1987`,
`suez_tropic_brilliance_2004`, `libya_jathran_blockade_2013` — but they are still **retrieved
as analogues**, which does not show up in the headline: an oil-workers' strike sits in the
precedent set carrying level 3, war.

### 6.1 Reading the numbers honestly, and a correction to the first pass
**The first pass understated this, and the direction has changed.** Reporting only
`infrastructure_attack` and `chokepoint_disruption`, this section previously said 9 of 150
reads affected (6.0%) and the level-0 share moving 42.0% → 41.0%, and concluded "the effect
on the headline is small" and "this is not a level-0 inflation story". Across all four
classes it is **27 of 150 (18.0%)** and the level-0 share moves **42.0% → 36.8%**, five
points, because 14 of the 17 non-hostile reads are level 0. Both earlier sentences are
withdrawn: the affected fraction is three times larger, and it *is* substantially a level-0
story once the mining strikes and export bans are counted. The two-class numbers were correct
for the two classes; the conclusion drawn from them was not safe to generalise, and it was
drawn before the other 112 records had been read.

What still holds, and what follows:
1. **The three non-zero non-hostile reads remain the qualitative damage.** A cobalt export
   ban reading as **war**, a contaminated pipeline and an arbitration award reading as *use
   of force* — those are cases where the location fallback manufactured escalation out of
   events with no adversary. The other 14 are level 0, which is the right answer for the
   wrong reason: an event with no adversary has nothing to record in the window.
2. **The base rate the engine is scored against moves by five points.** Climatology is
   estimated from this outcome distribution, so removing the non-hostile reads changes the
   comparison the engine is judged against, not merely the engine's own score. That makes
   this a limitation on *both* sides of the skill comparison and it must be reported as such —
   in whichever direction it turns out to run, which cannot be known until B re-runs.
3. **No claim about skill is made here, in either direction.** What the audit removes is not
   error but **27 reads that should never have been asked**. The honest statement for the
   paper is that the target was mis-specified for 18% of the scored G reads, that this
   cannot be corrected in the published run, and that it is corrected in v3.

Nothing above changes `summary.json`, `scores.jsonl` or `reads.jsonl`. Per §A3.5, every
surface reporting G from this run carries: *"scored before Amendment 3; includes 17
non-hostile events for which the G target is undefined (27 counting ambiguous) —
`data/spine/CLASS_AUDIT.md` §6."*

## 7. The class split — approved as a field, and Joe's two closing rulings
*Both gates this audit left open were ruled by Joe on 2026-09-02. Nothing in this section is
outstanding; §7.0 records the rulings so that a later session reading §4 or §7.3 does not
mistake a settled question for an open one.*

### 7.0 The rulings, 2026-09-02
**Ruling 1 — the thirteen `ambiguous` events stay ambiguous.** Ambiguous is a terminal state
under the sourced-or-unknown rule, not a pending decision: the record does not settle them,
and adjudicating anyway would supply a fact the evidence lacks. Registered as
`OUTCOME_MAPPING.md` Amendment 3.3; stated in §4 above; the both-ways diagnostic it requires
is in §6 and is tested.

**Ruling 2 — both class placements stay exactly as coded.** The eight mining strikes and
blockades stay in `conflict_escalation`; the three producer export bans stay in `sanctions`.
Reason, in Joe's words: moving them *after seeing results* would rewrite `p_class_given_big`,
the analogue retrieval and every published per-class number — which is precisely what
registration exists to prevent. The `hostility` field already removes the harm (neither group
is G-scored under Amendment 3). The correct placement is registered as a **v3 codebook item,
applied prospectively only** — `EVENTS_CODEBOOK.md` amendment 2026-09-02 (v3 placement).
Details in §7.3.

### 7.1 The field itself
Joe approved CLASS_AUDIT §7.5's recommendation on 2026-09-02: **a `hostility` field, not new
`events.type` values.** It is registered in `EVENTS_CODEBOOK.md` (amendment 2026-09-02) with
the four values, the coding rules and the tie-breaks, and in `OUTCOME_MAPPING.md` Amendments
3, 3.1 and 3.2. The `type` enum stays at seven values; no published per-class number changes;
the field changes future computations only. The reasoning that earned the approval stands:
renaming would break `p_class_given_big`, the analogue retrieval and every registered
per-class number for an effect a field achieves exactly, and a field can hold `ambiguous`,
which a type cannot — a point the second pass made expensive to ignore, since 13 of 187
events need that value.

### 7.2 What the split would do to the Big Moves per-class rates
`p_big_given_class` = events of the class inside a big-move window (onset − 7 d daily, − 31 d
monthly, to end) over events of the class inside the asset's coverage. Rules and episodes
exactly as published (`BIG_MOVES_REGISTRATION.md` Amendment 2, `data/big_moves/*.json`); only
the class denominators are split. **Not applied.**

| asset | class | as published | hostile only | non-hostile only |
|---|---|---|---|---|
| Brent (daily, from 1987-05) | `infrastructure_attack` | 5/44 = 11.4% | 5/41 = **12.2%** | 0/1 = 0% |
| Brent | `chokepoint_disruption` | 4/26 = 15.4% | 3/17 = **17.6%** | 1/6 = 16.7% |
| WTI (daily, from 1986-01) | `infrastructure_attack` | 6/45 = 13.3% | 6/42 = **14.3%** | 0/1 = 0% |
| WTI | `chokepoint_disruption` | 4/26 = 15.4% | 4/17 = **23.5%** | 0/6 = 0% |
| WTI monthly (from 1946) | `infrastructure_attack` | 12/48 = 25.0% | 11/43 = **25.6%** | 0/3 = 0% |
| WTI monthly | `chokepoint_disruption` | 9/27 = 33.3% | 6/18 = **33.3%** | 3/6 = 50.0% |

Read with the n's in view: the clean result is **WTI daily `chokepoint_disruption`, 15.4% →
23.5%**, where all four big-move-adjacent chokepoint events are hostile and six non-hostile
ones sit in the denominator diluting the rate by half — a hostile interdiction of a strait
moves oil, a ship aground in one mostly does not. `infrastructure_attack` barely moves, having
only three non-hostile events. The monthly chokepoint row runs the other way (non-hostile 3/6)
because a 31-day attribution window is wide enough to catch a grounding or a storm inside an
episode; that is a warning about attribution width at the monthly tier, not evidence that
groundings move oil, and it is the row that most needs Joe's eye. **Every cell is
single-digit-to-low-double-digit n and none of these differences is significant**; the case
for the split rests on the classes meaning two different things, not on these rates.

### 7.3 What the second pass adds to the class question
The oil assets above cannot see the second pass's main finding, because eight of the eleven
new non-hostile events are metals events. The equivalent split for copper, platinum, nickel,
cobalt and rare earths is **not computed here**: those series are not in
`data/big_moves/*.json`, and computing a new per-class rate on a new asset is a registered
computation belonging to whoever owns Big Moves, not a by-product of an audit. What the audit
can say without computing anything is that the eight Chile/Peru mining strikes and the three
producer export bans are the *reason* a metals Big Moves table would differ from the oil one,
and that a `hostility` split is the field that would separate them.

### 7.4 The two class placements — ruled: they stay as coded
Two groups sit in a class that fits them on no axis, and the `hostility` field marks that
without fixing it:
- **Eight mining strikes and community blockades in `conflict_escalation`** —
  `escondida_strike_2011/2017/2024`, `sa_platinum_strike_2014`, `lasbambas_blockade_2019`,
  `lasbambas_halt_2021`, `cuajone_shutdown_2022`, `peru_lasbambas_2022`. They belong in a
  labour-and-supply class, which does not exist.
- **Three producer price-management export bans in `sanctions`** — `indonesia_nickel_ban_2019`,
  `indonesia_palm_ban_2022`, `drc_cobalt_ban_2025`. Each is functionally an `opec_decision`:
  a producer restricting its own output to move a price. `opec_decision` is not G-scored at
  all, which is the treatment these three should have had from the start.

**Ruled 2026-09-02: neither group moves.** The reason is registration, not classification.
These placements were identified *after* the walk was run and the per-class results were in
view; re-classing them now would rewrite `p_class_given_big`, the analogue retrieval and every
published per-class number, with the new values chosen by someone who had already seen the old
ones. That is the exact move the pre-registration discipline exists to prevent, and it is not
made less so by the fact that the new placement would be more accurate. The audit agrees with
the ruling and would have recommended it: the **harm** — eleven events with no adversary being
scored on an escalation target — is already removed by the `hostility` field, so what remains
is a labelling improvement being weighed against a registration breach, and the trade is not
close.

**Registered for v3, prospective only** (`EVENTS_CODEBOOK.md` amendment 2026-09-02, "v3
placement"): the correct placement rules are written down now, while the reasoning is fresh
and before any result depends on them, and they bind **only events admitted after the v3
codebook takes effect**. No existing event is re-classed by them, then or later. Two things
follow that a future session must not get wrong:
1. **A v3 corpus is not comparable to this one on a per-class basis.** Events admitted under
   v3 placement rules and events already in the corpus will use the same class names for
   different populations. Any per-class number that spans the boundary must say so, or must
   be computed on one side of it.
2. **The eleven events keep their classes forever**, including in v3. "Prospective only" means
   the old rows are never revisited — not that they are revisited later when it is convenient.

## 8. Receipts
- Coding rule: `OUTCOME_MAPPING.md` Amendment 3 §A3.3 (values, tie-breaks) and Amendment 3.2
  (rules (a)–(d) for `conflict_escalation` and `sanctions`), each committed **before** the
  events it governs were coded and before any count here was computed. Field registered in
  `EVENTS_CODEBOOK.md`, amendment 2026-09-02, approved by Joe.
- Events and IES-90 rows: `data/oil.db` (`events`, `event_entities`, `event_outcomes`
  `source='ies90'`) — 187 rows in the four geopolitical classes.
- Walk numbers: `data/walk_forward/scores.jsonl`, latest run, daily tier, `burn_in_ok` and
  both engine and climatology G scored → n = 150, matching `data/walk_forward/summary.json`
  `/tiers/daily/G/engine_vs/climatology/n`. The run is read from the file, never named.
- Big Moves: `data/big_moves/{brent,wti,wti_monthly}.json`, episodes and coverage as
  published; attribution window from `src/big_moves.py` `TIERS[*]["attr_before_days"]`.
- Checked by `tests/test_hostility.py`: every event of the four classes appears here exactly
  once, its date, class and IES-90 level match the DB, the coding vocabulary is the registered
  vocabulary, the count tables agree with the rows, and the §6 impact figures recompute from
  `scores.jsonl` against whatever run it currently holds.
- Not touched: `events`, `data/walk_forward/**`, `data/dossiers/**`, `data/spine/patches/**`,
  `src/**`.
