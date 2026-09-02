# The IES-90 label audit — what you are being asked, exactly

You are the human half of an inter-rater reliability check. The engine assigned an
escalation level to 30 events from coded records in ICB, COW MID, COW War and UCDP.
You read the same records and assign your own level. Cohen's κ measures whether an
independent reader agrees with the machine's mapping. **That is the only reason your
answers matter: they must be yours, formed from the record on screen.**

You are **not** being asked to recall history from memory. Every source record the
engine used is printed on the screen with a link to it. Read those, apply the
definitions below, answer.

---

## The window

Everything is judged inside **W = the 90 days after the event date shown**. Not
before it, not after it. `WALK_FORWARD_PROTOCOL.md` §1; `OUTCOME_MAPPING.md` §1.

## The four levels

Registered in `OUTCOME_MAPPING.md` (Amendment 1, §"IES-90"). The engine derives them
from source fields; you derive them from the same records.

| level | meaning | what the sources look like |
|---|---|---|
| **0** | none | no militarized record covering W |
| **1** | threat or display of force | MID `hihost` 2 or 3; ICB `viol` 1 (no violence) |
| **2** | use of force | MID `hihost` 4; ICB `viol` 2–3 (minor or serious clashes); UCDP state-based deaths in W |
| **3** | war | MID `hihost` 5; ICB `viol` 4 (full-scale war); a COW war spell overlapping W |

**Dyadic beats location** (Amendment 2, §A2.1). If a record matched *both* parties of
your event's pair, it sets the level. A record matched only through one country or a
location — every UCDP GED row, every COW intra-state war — is shown to you but does
not set the level, because it answers "was there violence in that country", not "did
these two escalate". The screen labels each record `dyadic` or `location`, and prints
`basis` for the engine's own choice.

## The DEAL flag

`OUTCOME_MAPPING.md:128` — **"a dated negotiated termination in W (1/0; null when
neither ICB nor MID covers W)."**

It is not "were there talks". It is: did the crisis or dispute *end*, inside those 90
days, by agreement. Two coded fields carry it, and both are printed for you:

- **ICB:** `forout ∈ {1, 2}` — formal or semi-formal agreement (`OUTCOME_MAPPING.md:40`)
- **MID:** `settlmnt = 1` — negotiated settlement (`OUTCOME_MAPPING.md:53`)
- **UCDP:** never sets it. The conflict-year file has no settlement code
  (`OUTCOME_MAPPING.md:64`)

So: if a printed ICB record shows `forout 1` or `forout 2`, or a MID record shows
`settlmnt 1`, and its dates fall in W → **y**. If the covering records show otherwise
→ **n**. If no ICB or MID record covers W at all → **blank**, which records "unknown".

## When to answer blank

Always, when the record on screen does not settle it. The project's rule is
sourced-or-unknown, and it applies to you too. A blank is data. A guess is
contamination — it corrupts κ, which is the number the §7 gate depends on.

## What disagreement means

If your level differs from the engine's, that is the audit *working*. Put the reason
in the note field — the field you checked, the record you read. Disagreements are the
output. κ ≥ 0.6 passes the gate; below that, `OUTCOME_MAPPING.md` §5's decision rule
applies and the labels are reconsidered. Neither outcome is a failure of the project;
one of them is a finding about it.

## Mechanics

Three prompts per row, each ending with Enter:

1. `YOUR level (0 / 1 / 2 / 3; s = skip, q = quit)` → one digit
2. `DEAL in the 90 days? (y / n / blank = unknown)` → `y`, `n`, or nothing
3. `note (blank ok)` → free text or nothing

Saved after every row. `q` stops and keeps everything. Re-running offers the rows you
skipped. `python3 src/audit_ies90.py --status` prints progress, κ, and pass/fail.

## Do it rested

κ measures careful independent judgment. Thirty rows read carelessly produce a number
that is worse than no number, because it enters the record as though it were an audit.
The gate can wait for a clear head; the record cannot be un-published.
