# One crisis, six dyads: what happens when an actor-list crisis dataset is read dyadically
*Session G, 2026-09-03. Written to be lifted into the paper. Registered as a deliverable in
`data/grid/g/G4_REGISTRATION.md` Amendment 3 §A3.6. Every claim below is checkable against files in
this repository; the checks are named line by line.*

## The claim, in one sentence

When a crisis dataset that records **which states were involved** is used to label **pairs** of
states, every crisis with *k* involved states produces up to *k(k−1)/2* pairs — including pairs of
states that were **allies in that crisis** — and the resulting panel records co-belligerents as
adversaries.

## The instance, named so it can be checked

**ICB v16, crisis 489, `SYRIA CHEMICAL WEAPONS III`, 2018-04-07 to 2018-04-14, crisis-level
`viol = 4`, `forout = 4`.**

Its actor file (`data/state/raw/icb/icb2v16.csv`) lists five actors, with their own violence codes:

| `cracid` | actor | actor-level `viol` |
|---|---|---|
| 2 | USA | 2 |
| 200 | UKG | 2 |
| 220 | FRN | 2 |
| 652 | SYR | **4** |
| 365 | RUS | 1 |

Four of those five are in this project's oil-relevant register set (France is coded
`consumer` only and is screened out before the grid). Four states make six pairs, and on the
dyad-date grid all six received **IES level 3 — "war" — on the dyadic basis**, at the three
month-end grid dates whose 90-day forward window contains 7–14 April 2018:

    country.gbr | country.russia          country.gbr | country.syr
    country.gbr | country.usa             country.russia | country.syr
    country.russia | country.usa          country.syr | country.usa

`country.gbr|country.usa` is the clearest case: **the United Kingdom and the United States,
co-belligerents in the same strike, recorded as being at war with each other.**

Verify it with:

```
python3 -c "
import sys; sys.path.insert(0,'src'); sys.path.insert(0,'src/state')
import ies90 as I
src = I.load_sources()
r = I.score_event('2018-01-31', {'country.gbr','country.usa'},
                  {frozenset(('country.gbr','country.usa'))}, {'country.gbr','country.usa'}, src)
print(r['level'], r['basis'], [x['rule'] for x in r['recs']])"
```

which prints `3 dyadic [... 'ICB.pair.wholly' ...]`.

## Why it happens — the mechanism, in the code

`src/state/ies90.py:score_icb` decides whether a crisis is *dyadic* evidence for a pair with

```python
dy = any(set(p) <= mem for p in pairs)     # A2.1: both members of a pair are crisis actors
```

`mem` is the crisis's **actor set**. The test asks *"are both of these states involved in this
crisis?"* — never *"were they on opposite sides?"*, because the actor list cannot answer that. It
then assigns the level from the **crisis-level** `viol`, discarding the per-actor `viol` codes in
the table above, so Russia (actor `viol` 1) and the United States (actor `viol` 2) both inherit the
crisis maximum of 4 → IES level 3.

**This is not an error in ICB.** ICB never claimed the actor list encodes sides. The error is in
reading an actor list as if it were a dyad list, and it is invisible in the use ICB was built for
(describing crises) and unavoidable in the use a dyad-date panel makes of it.

**Nor is it an error in the event-triggered corpus.** There, `outcomes._actors_and_pairs` builds the
pair from the event record's own coded `actor` and `target` roles, so the pair is adversarial before
ICB is consulted. The defect appears only when the pair is supplied mechanically — which is exactly
what a grid does. **The same dataset is safe in one design and wrong in the other.**

## The general form

For a crisis with *k* involved states in the register:

| *k* | pairs generated | of which adversarial (upper bound) |
|---|---|---|
| 2 | 1 | 1 |
| 3 | 3 | ≤ 2 |
| 4 | **6** | ≤ 4 |
| 5 | 10 | ≤ 6 |
| 6 | 15 | ≤ 9 |
| 8 | 28 | ≤ 16 |

The upper bound is the largest possible number of cross-side pairs, `⌊k/2⌋·⌈k/2⌉`, reached only if
the sides are equally split. Two consequences follow, and the second is the one that matters for
inference:

1. **A count of "distinct dyads" overstates the evidence.** *k(k−1)/2* rows come from **one**
   record. A panel that treats them as independent observations counts one crisis as six.
2. **A clustering correction will not find it.** Clustering on dyad, on date, or two-way on both
   treats those six as six clusters, because they *are* six distinct dyads on the same dates. The
   dependence is not statistical, it is definitional: the rows are re-readings of a single row in
   the source. Correcting it requires clustering on the **setter record id** (the ICB `crisno`, the
   MID `disno`, the MIDI `incidnum`, the COW `WarNum`), not on the unit of observation.

## The fix, and the fact that it costs nothing

**ICB v16 publishes a dyadic file, and it is already in this repository.**
`data/state/raw/icb/icb_dyads_v16.csv`, 1,388 rows, columns `crisno, statea, stateb, …`. For crisis
489 it records **four** dyads, and they are the adversarial ones:

| statea | stateb | trigger | terminated |
|---|---|---|---|
| 2 USA | 652 SYR | 2018-04-07 | 2018-04-14 |
| 200 UKG | 652 SYR | 2018-04-07 | 2018-04-14 |
| 220 FRN | 652 SYR | 2018-04-07 | 2018-04-14 |
| 2 USA | 365 RUS | 2018-04-08 | 2018-04-14 |

`UKG–USA` is **not** among them. Neither is `UKG–RUS`, `FRN–UKG`, `FRN–USA`, `FRN–RUS`, nor
`SYR–RUS`. ICB itself knows the UK and the US were on the same side. Of the six pairs the grid
generated for this crisis, **three are recorded by ICB as dyads (`gbr–syr`, `syr–usa`,
`russia–usa`) and three are not (`gbr–usa`, `gbr–russia`, `russia–syr`) — 50 % spurious on this
crisis.**

And the file is already read. `src/state/outcomes.py:load_icb` opens it —

```python
dy = pd.read_csv(P.raw_path("icb", "icb_dyads_v16.csv"), encoding="latin-1")
...
for r in dy.itertuples(index=False):
    for cc in (r.statea, r.stateb):
        e = C.from_ccode(cc)
        if e:
            members[int(r.crisno)].add(e)      # <- the pairing is discarded here
```

— and then **flattens each dyad row into an unordered actor set on the next line**. The pairing
information, which is precisely what distinguishes an adversary from an ally, is loaded and thrown
away one statement later. Keeping `dy` as a set of `frozenset({statea, stateb})` per `crisno`, and
testing pair membership against **that** instead of against `members`, removes the defect at no data
cost and no new source.

Two limits on the fix, stated so it is not oversold:

- ICB's dyad file spans **1918–2022** but carries 1,388 dyads against 512 crises, so a crisis with no
  dyad row falls back to the actor list and the defect returns for it. The fallback must be counted,
  not silent.
- It fixes ICB only. **UCDP GED remains location-resolved** in the cache used here (no dyad field),
  so a GED level is a death count for a country-window and is replicated across every dyad containing
  that country. That is a separate defect with a separate fix, and it is not addressed by anything
  above.

## Standing

`src/state/ies90.py` and `src/state/outcomes.py` are **session A's files**. Session G has not changed
either, and this note is a report, not a patch. It is written up rather than merely applied because a
concrete, reproducible statement about how a standard dataset behaves when repurposed is worth more
than a filter in one project's pipeline.

## Measured over the whole panel

Computed by `src/grid_labels.py --build` over the 333 month-ends of 1987-01-31 … 2014-09-30
(`PANEL.json.icb_replication`; the panel is 15,740 dyad-date cells on 156 dyads).

**ICB sets a level on 158 cells, from 25 distinct crises.**
Dyads per crisis: mean **2.24**, max **12**.
Distribution: **14** crises set 1 dyad · **3** crises set 2 dyads · **6** crises set 3 dyads · **1** crises set 6 dyads · **1** crises set 12 dyads.

Most crises are bilateral and generate one dyad, which is correct. The tail is where the
replication lives:

| crisis | dyads it sets a level for | the dyads |
|---|---|---|
| crisis 393 GULF WAR | **12** | bhr–iraq, bhr–qatar, canada–usa, egypt–israel, gbr–iraq, iraq–saudi_arabia, iraq–syr, iraq–turkey, iraq–usa, israel–syr, kuwait–saudi_arabia, syr–turkey |
| crisis 412 IRAQ DEPLOY./KUWAIT | **6** | iraq–kuwait, iraq–saudi_arabia, iraq–usa, kuwait–saudi_arabia, kuwait–usa, saudi_arabia–usa |
| crisis 448 IRAN NUCLEAR II | **3** | gbr–iran, gbr–usa, iran–usa |
| crisis 440 IRAQ REGIME CHANGE | **3** | gbr–iraq, gbr–usa, iraq–usa |
| crisis 429 UNSCOM II | **3** | gbr–iraq, gbr–usa, iraq–usa |
| crisis 422 UNSCOM I | **3** | gbr–iraq, gbr–usa, iraq–usa |

**The worst case is not the Syrian one. It is `crisis 393 GULF WAR`, which sets a level for
12 dyads**, and the list is its own argument: alongside the adversarial pairs
(`iraq–usa`, `iraq–saudi_arabia`, `gbr–iraq`, `iraq–kuwait`) it contains **`canada–usa`**,
**`bhr–qatar`** and **`egypt–israel`** — three pairs of coalition partners or non-combatants,
each recorded at the crisis's own violence level, against each other.

Note also that `gbr–usa` recurs as a fabricated dyad across **five separate crises** — 406 Iraq
No-Fly Zone, 422 UNSCOM I, 429 UNSCOM II, 440 Iraq Regime Change, 448 Iran Nuclear II. It is not
one bad row; it is a systematic consequence of two states appearing together in crisis after
crisis as allies.

## The second limb: it fabricates ACTIVITY, not only levels

The measurement above counts the **labels** ICB replicates. There is a larger effect on the
**sample**, and it was found only once the full panel existed.

The panel's active-set rule admits a dyad when a dyadic-capable source records the pair in the
preceding five years. For ICB that test is the same co-actor containment, so **a crisis with k
register actors makes up to k(k−1)/2 dyads "active" for five full years.** The consequence is
visible in the panel's density, which is not uniform:

| | cells per grid date |
|---|---|
| 1987–1990 | ~32–36 |
| **1991–1995** | **~100–122** |
| 1996–2014 | ~18–43 |

At 1993-06-30, **108 of the 120 active dyads** qualify on a record that began in the Gulf War
window, and **89 of 120 qualify on ICB alone**.

**7,038 of the panel's 15,740 cells — 44.7% — fall in 1991-1995.** They are
not fabricated labels: 6,524 of them carry `opposed_side` evidence,
because MID and MIDI are covering and supply real levels (mostly zero). What is fabricated is
their **existence on the grid**. And they are the panel's least informative half:

| | cells | non-zero ΔIES | non-zero rate |
|---|---|---|---|
| 1991-1995 | 7,038 | 204 | **0.0311** |
| all other years | 8,702 | 956 | **0.1229** |

Nearly half the rows, **18%** of the signal, and
**0** dyads that appear nowhere else in the panel. This is the sharpest available
illustration of the difference between nominal n and informative n, and it is caused by a
dataset being read in a way it was not built for.

## What a reader should take from this

Not "ICB is bad data" — it is excellent data for the question it was built to answer. The
transferable claim is narrower and, we think, more useful:

> **An actor-list crisis dataset, used dyadically, silently converts co-belligerents into
> adversaries and multiplies one record into k(k−1)/2 observations — inflating both the label
> count and the sample, in a way no clustering correction detects, because the resulting rows
> are genuinely distinct dyads on genuinely distinct dates.**

Where the dataset ships a dyad-level file, as ICB v16 does, using it removes the label limb
entirely and the activity limb with it. Where it does not, the replication should be counted and
published, and the unit of clustering should be the **source record**, not the dyad-date.
