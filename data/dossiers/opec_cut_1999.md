# OPEC's third cutback in two years: Vienna agrees a 1.7 mb/d cut          opec_cut_1999 · 1999-03-23 · day · opec_decision

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | press (contemporaneous wire report) | RFE/RL (Radio Free Europe/Radio Liberty), Charles Recknagel | "World: OPEC States Approve Cut In Oil Output" | dateline Prague, 24 March 1999 | https://www.rferl.org/a/1090869.html | 2026-09-02T23:10Z (session) | "OPEC oil ministers agreed yesterday to severely cut back their countries' oil output in a bid to raise low prices... The oil ministers of the 11 member states of the Organization of Petroleum Exporting Countries (OPEC) voted in a meeting in Vienna to cut the cartel's output of crude oil by 1.7 million barrels a day (bpd) for one year beginning April 1." / "As of last month, the cartel was overproducing its official production ceiling by almost two million barrels a day, with the main output increases registered by Iran, Iraq and Nigeria." / "In anticipation of the agreement, oil prices nudged up last week to reach a six-month high of almost $14 on Friday." / "The new OPEC cutback agreement is the third in two years and comes after both previous accords were sabotaged by overproduction by individual members." |
| S2 | secondary (scholarly, retrospective) | Oxford Institute for Energy Studies, *Oxford Energy Forum* (Robert Mabro) | "The Oil Price Crises of 1998–9 and 2008–9" | May 2009 | https://ora.ox.ac.uk/objects/uuid:8e176905-4979-44a5-bc97-3096e5adea6c/files/m4a6812aa146e42e81d9030805b94cc39 | 2026-09-02T21:45Z (session) | "The oil price initial fall and subsequent stagnation at low levels lasted throughout 1998 and until March 1999. A market almost entirely focused on the internal relationships between OPEC Members was by March 1999 convinced that OPEC unity had been restored by two events: an agreement between Iran and Saudi Arabia reached by the respective foreign ministers of these two countries in January 1999, and even more crucially by the election of Hugo Chávez to the presidency of Venezuela. Furthermore, the output cuts that the market had ignored for so long had at last begun to be seen biting..." |

`rferl.org` and `ora.ox.ac.uk` are genuinely independent registrable domains — this event clears the two-source *count* in clause (a), the only one of the four events in this batch to do so. Neither source is primary.

## Narrative

OPEC oil ministers, meeting in Vienna, agreed on 23 March 1999 to cut the cartel's crude output by 1.7 million barrels a day for one year beginning 1 April, a decision RFE/RL's Prague-datelined report of 24 March 1999 describes as having been reached "yesterday" [S1]. As of the previous month the cartel had been overproducing its official ceiling by almost two million barrels a day, with the largest increases from Iran, Iraq and Nigeria [S1]. RFE/RL calls this OPEC's third cutback agreement in two years, after the first two "were sabotaged by overproduction by individual members" [S1] — indirect corroboration that the March and June 1998 decisions in this batch were real, without dating or quantifying them. The market had priced in an agreement beforehand: "oil prices nudged up last week to reach a six-month high of almost $14 on Friday" [S1]. Mabro's contemporaneous account attributes the market's confidence that OPEC discipline would hold to two non-production events — a January 1999 Iran-Saudi foreign-ministry rapprochement and Hugo Chávez's election to Venezuela's presidency — plus a belated recognition that 1998's ignored cuts were finally "biting" [S2]. Analyst Julian Lee is quoted predicting prices could reach $18 a barrel by year-end with 75-80 percent compliance [S1]. (204 words)

## Knowable at

1999-03-23, `date_precision = day`. Reason: [S1] is datelined "Prague, 24 March 1999" and reports the OPEC vote as having happened "yesterday," placing the decision on 23 March 1999. This is independently confirmed and matches the current database value exactly.

## Entities

- `institution.opec` — actor — unchanged, well supported: [S1] states "the oil ministers of the 11 member states of ... OPEC ... voted."
- Considered and **not** added: `country.saudi_arabia` and `country.venezuela`. [S2] names Saudi Arabia (via the January 1999 Iran-Saudi rapprochement) and Venezuela (via Chávez's election) as context for why the market trusted the March 1999 decision would hold, but neither source frames either country as the specific *actor* deciding this event the way [S1] in the `opec_cut_march_1998` dossier names Saudi Arabia and Venezuela as direct parties to that decision's Riyadh negotiation. Adding them here would overreach the sourcing.
- `commodity.brent` — affected_market — unchanged; [S1] prices the pre-decision market in dollars per barrel without naming a specific benchmark, so this is neither confirmed nor contradicted.

## Class

Proposed class: `opec_decision`, as currently coded. Codebook clause: "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks." Fits cleanly and is not contested by either source.

## Not known at the time

Per [S1], compliance with prior OPEC agreements had been a "tough challenge," and the analyst quoted (Julian Lee) built in an explicit assumption of only 75-80 percent compliance — full realization of the announced 1.7 mb/d cut was a hoped-for outcome, not a known one, at the time of the decision. Per [S2], the durability of the Saudi-Venezuela-Iran rapprochement underlying the market's restored confidence was itself only weeks to months old in March 1999 (the Iran-Saudi foreign-ministry agreement dated to January 1999, Chávez's election to February 1999); its staying power could be inferred from recent diplomatic signals but was not something contemporaries could know with certainty.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `event_date` | 1999-03-23 | unchanged — confirmed | [S1] |
| `date_precision` | day | unchanged | [S1] |
| `source_url` | https://www.rferl.org/a/1090869.html | unchanged — independently re-retrieved and confirmed this session | [S1] |
| `surprise` | 2 | unchanged — **confirmed**, not merely unaddressed: [S1] shows prices already rising in anticipation before the vote ("oil prices nudged up last week to reach a six-month high"), and [S2] shows market confidence in restored OPEC unity had been building since January 1999 on the back of two named diplomatic/political events. "Widely expected; extensive warning or visible build-up" is a good match to the evidence. | [S1][S2] |
| `severity` | 3 | leave unchanged — [S1] gives 1.7 million b/d as a directly confirmed figure, larger than either unconfirmed 1998 figure in this batch; this dossier has no codebook-based grounds to recode 3 vs. 4 and does not propose one | — |
| `description` | "Vienna meeting ratifies the Hague framework (agreed ~10 days earlier so partially telegraphed) totalling ~2.1 mb/d with non-OPEC; launched the 1999 price recovery. DRAFT coding." | "OPEC's 11 member states voted in Vienna on 23 March 1999 to cut crude output by 1.7 million b/d for one year from 1 April 1999 — OPEC's third cutback agreement in two years. As of February 1999 the cartel had been overproducing its ceiling by almost 2 million b/d, chiefly via Iran, Iraq and Nigeria. Prices had already risen in anticipation before the vote." | [S1] |

## Status

partial — fails clause (a) on the primary sub-requirement only: two independent domains **are** retrieved this session ([S1] rferl.org, [S2] ora.ox.ac.uk), satisfying the two-source count — a genuine improvement over the other three events in this batch, none of which cleared the two-domain bar. No primary source was retrieved; the same routes tried and failed for the other three events in this batch (opec.org 402; oxfordenergy.org direct 403; eia.gov 403; iea.org 403; imf.org/elibrary.imf.org 403; crsreports.congress.gov 403; upi.com/Archives 403; bis.org 404; fraser.stlouisfed.org no search endpoint; federalreserve.gov 404/irrelevant; govinfo.gov ERP-1999 and Congressional Record retrieved but irrelevant; api.govinfo.gov 401; web.archive.org blocked to this tool; duckduckgo.com/html CAPTCHA-blocked; bing.com/search generic/non-specific; presidency.ucsb.edu functional but no relevant hit for a March-May 1999 window) were tried again for this event with the same results. Narrative (b), knowable-at (c), class (e), and not-known-at-the-time (f) are all well supported. Entities (d): no changes proposed; `institution.opec:actor` is well supported and no other role fits cleanly enough to add without over-reaching the sources. Surprise is the one field in this whole batch that this dossier can say is **confirmed**, not just left unaddressed, by the retrieved evidence.
