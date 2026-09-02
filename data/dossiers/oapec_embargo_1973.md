# OAPEC oil embargo on states backing Israel     oapec_embargo_1973 · 1973-10-17 · day · sanctions

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, *Energy Crisis, 1969–1974*, Doc. 219) | "Minutes of Washington Special Actions Group Meeting" | Washington, October 17, 1973, 3:05–4:04 p.m. | https://history.state.gov/historicaldocuments/frus1969-76v36/d219 | 2026-09-02T20:33Z (session) | Secretary Kissinger: "We don't expect an oil cut-off now in the light of the discussions with the Arab Foreign Ministers this morning." Mr. Clements: "In the Mediterranean there has already been a cut-back by about 12% in the amount of crude available." |
| S2 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI) | "Minutes of Washington Special Actions Group Meeting" | Washington, October 19, 1973, 10:04–10:57 a.m. | https://history.state.gov/historicaldocuments/frus1969-76v36/d221 | 2026-09-02T20:33Z (session) | "2 million barrels a day cut" to Europeans (already implemented); Europe at "1–2 million barrels per day down"; European consumption "15 million barrels a day, 11 million of which comes from the Arabs"; U.S. impact "1% of US consumption" (Arab shipments only) to "3–4% of the US consumption" (if Europeans also cut exports). Governor Love characterized the Arab moves as "relatively moderate." |
| S3 | primary | U.S. Department of State, Office of the Historian (FRUS 1969–1976, Vol. XXXVI, Doc. 223) | "Memorandum Prepared in the Office of Economic Research, Central Intelligence Agency" | Washington, October 19, 1973 | https://history.state.gov/historicaldocuments/frus1969-76v36/d223 | 2026-09-02T20:33Z (session) | "Production will be reduced by not less than 5% a month until an Israeli withdrawal from occupied territories is completed and the 'legal rights' of the Palestinians are restored." Several states "have either announced or threatened a total embargo against the United States." Producers "promised to maintain oil deliveries to 'friendly' countries." |
| S4 | secondary | National Bureau of Economic Research, Working Paper 16790 (James D. Hamilton, *Historical Oil Shocks*, February 2011) | *Historical Oil Shocks* | February 2011 | https://www.nber.org/papers/w16790 | 2026-09-02T20:33Z (session) | "On October 17, the Arab members of the Organization of Petroleum Exporting Countries announced an embargo on oil exports to selected countries viewed as supporting Israel"; "Production from Arab members of OPEC in November was down 4.4 mb/d from what it had been in September, a shortfall corresponding to 7.5% of global output" (p. 14); "[Arab oil producers] had discussed the possibility of an embargo prior to the war" (Barsky and Kilian, cited p. 15). |

S1–S3 are primary, contemporaneous U.S. government records (history.state.gov); S4 is an independent-domain (nber.org) scholarly working paper cited as secondary, per its own not-peer-reviewed cover note.

## Narrative

On October 17, 1973, Arab members of OPEC announced a production cut of "not less than 5% a month" tied to Israeli withdrawal and Palestinian rights, with several producers threatening a total embargo on the United States [S3]. Notably, at a U.S. crisis meeting that same afternoon, Kissinger stated "we don't expect an oil cut-off now" after morning talks with Arab foreign ministers [S1] — the specific step taken that day was not yet confirmed to top U.S. officials hours before or as it was announced. By October 19, U.S. officials had concrete figures: roughly 2 million barrels/day cut from Europe, out of Europe's 15 mb/d consumption (11 mb/d Arab-sourced), and 1–4% of U.S. consumption at risk depending on European pass-through [S2]. The realized November shortfall — 4.4 mb/d, 7.5% of world output — was established only afterward [S4]. Hamilton reports Arab producers "had discussed the possibility of an embargo prior to the war" [S4], meaning the general threat, though not its exact timing, was foreseeable.

## Knowable at

1973-10-17, day precision. Reason: this is OAPEC's announcement date per [S3] and [S4]. Nuance: [S1] shows that within hours of the announcement, the specific fact of a cutoff was not yet confirmed to the White House's own crisis group ("we don't expect an oil cut-off now," 3:05 p.m. that day) — full contemporaneous confirmation, with quantified figures, is only documented in this dossier's sources as of October 19 [S2][S3]. Day precision on October 17 is retained because that is the announcement date reported by the only sources that state it explicitly [S3][S4]; no source retrieved this session gives a wire-report time for October 17 itself.

## Entities

- `country.saudi_arabia` — actor — Saudi Arabia is not individually named quoted in S1–S3's retrieved text, but is corroborated as a lead OAPEC actor by [S4] and by the broader FRUS record of Saudi Oil Minister Yamani's threats referenced in [S1] ("New York Times article by Edward Cowan mentioning ... Yamani's threat of production cuts," per S1's fetched summary).
- `country.usa` — target — named as the object of embargo threats in [S3] ("total embargo against the United States").
- **Gap:** no `institution.oapec` entity exists in the register (only `institution.opec`). OAPEC (Organization of Arab Petroleum Exporting Countries) is a distinct body from OPEC and is the actual actor in [S3] and [S4]. Reported to Session A rather than invented or substituted.

## Class

Proposed class: `sanctions`. Codebook clause: "`sanctions` | Sanctions imposed, tightened, or lifted on a producer." Note for the codebook maintainers: the one-line description's phrasing ("on a producer") describes sanctions where a producer is the target; here the producer states are the actors imposing an export/production sanction on a consuming state (`country.usa`, target). The mechanism — an embargo conditioned on political demands — is unambiguously a sanctions action in substance, and no other closed-set class fits (`opec_decision` is defined as an "OPEC/OPEC+" production decision, and this action was taken by OAPEC, a distinct, all-Arab body, with an explicit political-embargo character beyond a production-quota decision). Class is not changed; the definitional asymmetry is flagged for review, not silently resolved.

## Not known at the time

The precise magnitude of the eventual shortfall (4.4 mb/d / 7.5% of global output, November data) was not knowable on October 17–19; officials on October 19 worked from partial, Europe-centric estimates (~2 mb/d) [S2]. Which countries would ultimately face a total embargo versus a graduated cut, and for how long, was undetermined on October 17 — Libya, Abu Dhabi, Kuwait and Saudi Arabia are named in [S3] as having "either announced or threatened" total embargoes, not confirmed to have imposed one. The eventual doubling of the posted price by Gulf producers on January 1, 1974 [S4] was not part of the October 17 decision.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `description` | Title + "[deep-history tier 1970-1989; events-only]" | "Arab OPEC members announced a production cut of at least 5%/month tied to Israeli withdrawal, with several producers threatening a total embargo on the U.S.; U.S. officials did not yet expect a cutoff hours before the announcement, and had only partial (Europe-centric) shortfall estimates two days later." | [S1][S2][S3] |
| `source_url` | https://www.nber.org/papers/w16790 (secondary only) | https://history.state.gov/historicaldocuments/frus1969-76v36/d223 (primary) | [S3] |
| `severity` | NULL | 5 — "Systemic; a top producer or a critical chokepoint materially disrupted." Reasoning: a ~2 mb/d cut to Europe known within 48 hours [S2], and a realized 4.4 mb/d / 7.5%-of-world-output shortfall [S4], with Saudi Arabia (a top producer) among the actors — this is systemic-scale by the codebook's own examples. | [S2][S4] |
| `surprise` | NULL | 3 — "plausible but not consensus; a live possibility." Reasoning: the general threat of an "oil weapon" had been discussed among Arab producers before the war [S4], but the specific action on October 17 was explicitly not expected by Kissinger hours before it happened [S1] — neither fully anticipated (1–2) nor a genuine shock (4–5). | [S1][S4] |
| `confidence` | medium | high — three independent FRUS documents (S1, S2, S3), each a distinct contemporaneous U.S. government record, agree on the announcement, its conditions, and its early-assessed scale. | [S1][S2][S3] |
| `date_precision` | day | day (unchanged) | [S3][S4] |
| `event_date` | 1973-10-17 | 1973-10-17 (unchanged) | [S3][S4] |

## Status

partial — fails (a) in letter: while two independent domains are present with three primary sources (S1–S3, history.state.gov) and one secondary (S4, nber.org), satisfying the two-source/one-primary minimum, it is marked **partial** because no press source was retrieved this session (contemporaneous press is explicitly a legitimate second-source category under clause (a) and would strengthen this record), and because the `institution.oapec` entity gap under clause (d) is unresolved pending Session A. Clauses (b) narrative, (c) knowable_at, (e) class, and (f) not-known-at-the-time are met.
