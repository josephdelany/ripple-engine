> **REFERENCE — SPECIFICATION, NOT A RESULT.** Event-record documentation for the history spine. It claims no finding; the authoritative result is in [`PAPER.md`](../PAPER.md).

# Proposed amendment to EVENTS_CODEBOOK.md — five coding gaps found by the pre-1990 pass

*Session E, 2026-09-02. **Proposed, not applied.** The canonical `EVENTS_CODEBOOK.md`
lives one directory up, in the separate `News to Markets` repository, outside this repo's
history. Session E will not edit a canonical document in another repository where the
change could not be reviewed alongside the evidence that motivated it. The amendment text
is therefore written here, with the dossier that produced each finding named, for Joe to
apply or reject.*

**Nothing in this proposal reclassifies any event.** The closed set of seven classes is
what stops post-hoc reclassification, and changing it changes what the engine retrieves as
an analog. Every gap below is recorded as a gap.

---

## Proposed text

> **Amendment 2026-09-02 (Session E — coding gaps found while sourcing the 1970–1989
> tier).** Nineteen pre-1990 records were taken to the SPINE_REGISTRATION standard. Five
> gaps in this codebook were found. No class is added, removed or reassigned by this
> amendment; each gap is recorded so that coders stop resolving it silently and
> differently.
>
> **1. The `sanctions` class is written one-directionally.** The table reads "Sanctions
> imposed, tightened, or lifted **on a producer**", i.e. the producer is the target. In
> `oapec_embargo_1973` and `embargo_lifted_1974` the producer states are the *actors*,
> imposing an export restriction on consuming states. Both readings are sanctions in
> substance. Until Joe rules, code either direction as `sanctions` and state the direction
> in the description.
>
> **2. `infrastructure_attack` says "strike" and coders have read it two ways.** The
> definition is "Direct strike on production, refining, or export infrastructure". A
> *labour* strike is not a strike in that sense, yet `iran_oilworkers_strike_1978` — whose
> physical effect was among the largest in the corpus, 4.8 mb/d or about 7% of world
> production — is coded there. An *accidental* fire has no actor at all, yet
> `abqaiq_arabian_1977` is coded there with Saudi Arabia as both actor and target. Neither
> a strike-by-workers nor an accident is a direct attack, and the closed set has nowhere
> else to put them.
>
> **3. `policy_response` is defined as market intervention and is being used for
> declaratory and diplomatic events.** The 2026-07-23 amendment defines it as "deliberate
> government/agency market interventions (e.g. coordinated SPR/IEA strategic-reserve
> releases)". `carter_doctrine_1980` is a declaratory security commitment that moved no
> barrels, and `iran_iraq_ceasefire_1988` is a war ending. Neither is a market
> intervention.
>
> **4. The severity scale cannot express a shock whose sign is reversed.** Severity is
> coded 1–5 by "expected disruption", from "no physical supply at risk" to "systemic".
> The largest oil event of the 1980s was a price *collapse* — Hamilton (NBER 16790)
> writes that it "represented an 'oil shock' for the producers" — and a scale that runs
> from no-disruption to severe-disruption has no value for it. `opec_price_collapse_1986`
> currently carries severity NULL for want of a codeable value.
>
> **5. Inclusion criterion 3 needs to be enforced, not merely stated.** The criterion
> requires "a mechanism you can state in one sentence" by which the event could affect
> supply, demand or the risk premium. `iran_air_655_1988` is well documented by primary
> sources and has no such mechanism: no infrastructure, tanker or chokepoint was involved.
> A record can meet the sourcing standard and fail the inclusion standard, and the
> codebook should say what happens then.
>
> **6. Sourcing: an encyclopaedia is not a source.** Inclusion criterion 2 requires "a
> primary or major-wire source". Measured on 2026-09-02 by `src/spine_audit.py`: 31 of 313
> records cite an encyclopaedia as their `source_url`, and all 31 have no other citable
> domain. Encyclopaedias may orient a search and are never cited.

---

## Where each gap came from

| gap | dossier | evidence |
|---|---|---|
| 1, sanctions direction | `oapec_embargo_1973`, `embargo_lifted_1974` | FRUS 1969-76 v36 d219/d221/d223; Kissinger memo of 19 March 1974 |
| 2, "strike" ambiguity | `iran_oilworkers_strike_1978`, `abqaiq_arabian_1977` | Hamilton NBER 16790 on the 4.8 mb/d fall; eleven failed retrieval routes for the 1977 fire |
| 3, policy_response | `carter_doctrine_1980`, `iran_iraq_ceasefire_1988` | Carter's State of the Union, 23 January 1980; UN UNIIMOG mission history |
| 4, severity sign | `opec_price_collapse_1986` | Hamilton NBER 16790: "$27/barrel in 1985 to $12/barrel at the low point in 1986" |
| 5, inclusion criterion 3 | `iran_air_655_1988` | Reagan's statement; the ICJ case record |
| 6, encyclopaedia sourcing | corpus-wide | `data/spine/AUDIT.md`, computed |

## What Joe has to decide

Gaps 1 and 6 are clarifications and could be applied as written. Gaps 2, 3, 4 and 5 cannot
be closed without either widening the closed set — which changes the analog pool and
therefore every read the engine produces — or accepting that some records are filed in the
nearest available class and saying so on the surfaces. That is a modelling decision, not a
documentation one, and it is Joe's.
