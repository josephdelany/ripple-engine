"""exposure_schema.py -- the loader and validator for data/exposure/blocks/*.json.

EXPOSURE_REGISTRATION.md §2, enforced rather than trusted:

    an event is COMPLETE only with all six required fields AND provenance on every filled
    numeric, and any numeric present without source_url / source_publisher / source_date is a
    HARD FAILURE, not a warning.

Two design decisions that are the whole point of the file:

1. **Status is COMPUTED, never read.** Six sessions filled six blocks in three different shapes;
   some declare a `status`, some do not, and a session marking its own work COMPLETE is not
   evidence that it is. `validate()` derives the status from the fields and then reports where a
   block's self-declared status disagrees with the computed one. A validator that trusts the
   thing it is validating is decoration.

2. **A measured zero is a value, not a missing field.** `capacity_affected_kbd: 0` on a foiled
   attack (block B, `saudi_abqaiq_foiled_2006`) means nothing was taken offline, and that is a
   finding. Treating it as absent is the same defect as `max(default=0)` treating an absence as
   zero, run backwards, and it would silently drop the cleanest observations in the corpus. Only
   the registered unknown markers count as missing.

Provenance is accepted in either shape, because §2 fixes the requirement and not the layout:
  * per-field: `provenance: {"<field>": {"source_url":…, "source_publisher":…, "source_date":…}}`
  * event-level: the flat `source_url` / `source_publisher` / `source_date` triple, which covers
    every numeric on that event when all three are present.
Per-field wins where both exist. §2 requires provenance on every *filled numeric*, so an event
whose six numerics come from six sources needs the per-field form; the flat triple cannot express
that and an event relying on it with numerics from different sources cannot be distinguished --
which is itself worth knowing, and is reported as `flat_provenance_covers_multiple_numerics`.

Run:  python3 src/exposure_schema.py            validate every block, write the coverage table
      python3 src/exposure_schema.py --strict   exit non-zero if any block has a hard failure
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCKS = ROOT / "data" / "exposure" / "blocks"
OUT_JSON = ROOT / "data" / "exposure" / "coverage.json"
OUT_MD = ROOT / "data" / "exposure" / "COVERAGE.md"
REGISTRATION = "EXPOSURE_REGISTRATION.md §2 (2026-09-03, commit 22da52f)"
GATE_N = 30            # §5: below this, Stage 1 is descriptive only and no verdict is issued

REQUIRED = ("asset_name", "asset_type", "capacity_nameplate_kbd", "capacity_affected_kbd",
            "days_to_partial_restore", "days_to_full_restore")
OPTIONAL = ("operator", "country_iso3", "export_share_pct", "downstream_dependency",
            "alt_routing_available", "prior_incidents_same_asset")
# the fields §2 calls numeric -- the ones that carry magnitude and therefore need provenance
NUMERIC = ("capacity_nameplate_kbd", "capacity_affected_kbd",
           "days_to_partial_restore", "days_to_full_restore", "export_share_pct")
PROV_KEYS = ("source_url", "source_publisher", "source_date")
# the registered markers for "no value". NOTE: 0 is NOT here, and must never be.
UNKNOWN_MARKERS = {"unknown", "", "n/a", "na", "none", "tbd", "-"}
ASSET_TYPES = {"refinery", "terminal", "field", "pipeline", "chokepoint", "processing", "storage"}
ONGOING = "ongoing"     # §2: permitted for days_to_full_restore, with a stamp date
NEVER = "never"         # a permanently closed asset (block G_accident, Amendment 1): restore never occurs


def is_filled(v):
    """True if the field carries a value. A numeric 0 is a value (§2 note 2 above); only the
    registered markers and None are missing."""
    if v is None:
        return False
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return True
    if isinstance(v, str):
        return v.strip().lower() not in UNKNOWN_MARKERS
    return bool(v)


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def provenance_for(event, field):
    """(prov_dict, source) where source is 'per_field' | 'event_flat' | None."""
    per = (event.get("provenance") or {}).get(field)
    if isinstance(per, dict) and all(is_filled(per.get(k)) for k in PROV_KEYS):
        return per, "per_field"
    flat = {k: event.get(k) for k in PROV_KEYS}
    if all(is_filled(flat.get(k)) for k in PROV_KEYS):
        return flat, "event_flat"
    return None, None


def validate_event(event):
    """Compute the event's status from its fields. Never reads `status`."""
    hard, notes = [], []
    filled_required = [f for f in REQUIRED if is_filled(event.get(f))]
    filled_numeric = [f for f in NUMERIC if is_filled(event.get(f))]

    # §2 THE RULE: every filled numeric names a source and a date, or it is a hard failure.
    prov_sources = {}
    for f in filled_numeric:
        prov, kind = provenance_for(event, f)
        prov_sources[f] = kind
        if prov is None:
            hard.append(f"{f} is filled ({event.get(f)!r}) with no complete provenance "
                        f"(needs {', '.join(PROV_KEYS)}, per-field or event-level)")

    # §2 vintage: nameplate from a post-event source must carry retrospective
    nf = "capacity_nameplate_kbd"
    if is_filled(event.get(nf)):
        prov, _ = provenance_for(event, nf)
        sd, ed = (prov or {}).get("source_date"), event.get("date")
        if prov and isinstance(sd, str) and isinstance(ed, str) and sd[:10] > ed[:10]:
            retro = prov.get("retrospective", event.get("retrospective"))
            if retro is not True:
                hard.append(f"{nf} comes from a source dated {sd[:10]}, after the event ({ed[:10]}), "
                            f"but retrospective is not true -- §2 requires the flag be carried")

    # §2: 'ongoing' is permitted for days_to_full_restore, with a stamp date
    dfr = event.get("days_to_full_restore")
    if isinstance(dfr, str) and dfr.strip().lower() == ONGOING:
        if not is_filled(event.get("ongoing_stamp_date")):
            hard.append("days_to_full_restore is 'ongoing' with no ongoing_stamp_date -- §2 permits "
                        "'ongoing' only with a stamp date")
    elif isinstance(dfr, str) and dfr.strip().lower() == NEVER:
        notes.append("days_to_full_restore is 'never': the asset did not reopen. A permanent closure is a "
                     "measured outcome, not a missing value, and is counted as filled.")
    elif is_filled(dfr) and not is_number(dfr):
        notes.append(f"days_to_full_restore is {dfr!r}: neither a number nor a registered literal "
                     f"('ongoing' with a stamp date, or 'never')")

    at = event.get("asset_type")
    if is_filled(at) and at not in ASSET_TYPES:
        notes.append(f"asset_type {at!r} is outside the registered enum {sorted(ASSET_TYPES)}")

    # a flat triple standing in for several numerics from possibly different sources
    if sum(1 for f, k in prov_sources.items() if k == "event_flat") > 1:
        notes.append("flat_provenance_covers_multiple_numerics: one event-level source triple is "
                     "standing in for more than one numeric; §2 asks for provenance per filled numeric")

    if hard:
        status = "INVALID"
    elif len(filled_required) == len(REQUIRED):
        status = "COMPLETE"
    elif filled_required:
        status = "PARTIAL"
    else:
        status = "EMPTY"
    return {"event_id": event.get("event_id"), "computed_status": status,
            "declared_status": event.get("status"), "hard_failures": hard, "notes": notes,
            "filled_required": filled_required,
            "missing_required": [f for f in REQUIRED if f not in filled_required],
            "filled_numeric": filled_numeric, "provenance_kind": prov_sources}


def load_blocks(path=BLOCKS):
    out = {}
    for f in sorted(Path(path).glob("*.json")):
        d = json.loads(f.read_text())
        out[d.get("block") or f.stem] = d
    return out


def validate_all(blocks=None):
    blocks = load_blocks() if blocks is None else blocks
    return {b: [validate_event(e) for e in d["events"]] for b, d in blocks.items()}


def gate_flags(blocks=None):
    """{block: counts_toward_gate}. A block may declare itself out of §5's gate -- G_accident does,
    under EXPOSURE_REGISTRATION Amendment 1, because §5's 30 is about the corpus of 75 and its rows
    are a separate accident comparison. Honoured rather than overridden: a block that says its rows
    do not count must not be able to carry the gate over the line."""
    blocks = load_blocks() if blocks is None else blocks
    return {b: bool(d.get("counts_toward_gate", True)) for b, d in blocks.items()}


def coverage(results, flags=None):
    """§5: coverage reported before any estimate -- COMPLETE / PARTIAL / EMPTY / INVALID by block
    and in total, against the registered gate of 30."""
    by_block, total = {}, Counter()
    hard, disagree = [], []
    for b, rows in sorted(results.items()):
        c = Counter(r["computed_status"] for r in rows)
        total += c
        by_block[b] = {"n": len(rows), **{k: c.get(k, 0) for k in ("COMPLETE", "PARTIAL", "EMPTY", "INVALID")}}
        for r in rows:
            if r["hard_failures"]:
                hard.append({"block": b, **{k: r[k] for k in ("event_id", "hard_failures")}})
            d = (r["declared_status"] or "").upper()
            if d and d != r["computed_status"] and not (d == "OUT_OF_UNIT_SCOPE"):
                disagree.append({"block": b, "event_id": r["event_id"],
                                 "declared": r["declared_status"], "computed": r["computed_status"]})
    if flags is None:
        try:
            flags = gate_flags()
        except Exception:
            flags = {}
    counted = {b for b in results if flags.get(b, True)}
    n_complete = sum(1 for b, rows in results.items() if b in counted
                     for r in rows if r["computed_status"] == "COMPLETE")
    excluded = sorted(b for b in results if b not in counted)
    return {"registration": REGISTRATION, "generated_by": "src/exposure_schema.py",
            "n_events": sum(v["n"] for v in by_block.values()), "by_block": by_block,
            "total": {k: total.get(k, 0) for k in ("COMPLETE", "PARTIAL", "EMPTY", "INVALID")},
            "gate": {"registered_minimum_complete": GATE_N, "n_complete": n_complete,
                     "blocks_counted": sorted(counted), "blocks_excluded_by_own_declaration": excluded,
                     "n_complete_including_excluded_blocks": total.get("COMPLETE", 0),
                     "gate_met": n_complete >= GATE_N,
                     "consequence_if_not_met": ("§5: Stage 1 is reported as DESCRIPTIVE ONLY and no verdict "
                                                "is issued -- registered in advance so it cannot be waived later")},
            "hard_failures": {"n": len(hard), "rows": hard},
            "declared_vs_computed_disagreements": {"n": len(disagree), "rows": disagree}}


def write_md(cov):
    L = ["# EXPOSURE COVERAGE — how many of the 75 reached COMPLETE, and why the rest did not", "",
         f"*Generated by `src/exposure_schema.py` under {REGISTRATION}. Status is **computed from the "
         f"fields**, never read from a block's own `status` — a session marking its own work COMPLETE "
         f"is not evidence that it is. Where the two disagree, the disagreement is listed below.*", ""]
    g = cov["gate"]
    if g["gate_met"]:
        L += [f"> **§5 GATE MET: {g['n_complete']} COMPLETE against a registered minimum of {GATE_N}.**", ""]
    else:
        L += [f"> **§5 GATE NOT MET: {g['n_complete']} COMPLETE against a registered minimum of "
              f"{GATE_N}.** Stage 1 is therefore reported as **descriptive only and no verdict is "
              f"issued** — registered in advance, in §5, so it cannot be waived now that the number "
              f"is known.", ""]
    L += [f"**{cov['n_events']} events across {len(cov['by_block'])} blocks.**", "",
          "| block | n | COMPLETE | PARTIAL | EMPTY | INVALID |", "|---|---:|---:|---:|---:|---:|"]
    for b, v in cov["by_block"].items():
        L.append(f"| {b} | {v['n']} | {v['COMPLETE']} | {v['PARTIAL']} | {v['EMPTY']} | {v['INVALID']} |")
    t = cov["total"]
    L.append(f"| **total** | **{cov['n_events']}** | **{t['COMPLETE']}** | **{t['PARTIAL']}** "
             f"| **{t['EMPTY']}** | **{t['INVALID']}** |")
    ex = g.get("blocks_excluded_by_own_declaration") or []
    if ex:
        L += ["", f"The §5 gate is counted over **{', '.join(g['blocks_counted'])}** only. "
              f"{', '.join(ex)} declares `counts_toward_gate: false` (EXPOSURE_REGISTRATION Amendment 1) "
              f"and that declaration is honoured, not overridden: a block saying its own rows do not count "
              f"cannot carry the gate over the line. COMPLETE across **all** blocks including the excluded "
              f"one is **{g['n_complete_including_excluded_blocks']}**, published here so the exclusion is "
              f"visible rather than silent.", ""]
    hf = cov["hard_failures"]
    L += ["", "## Hard failures — §2's rule, not a warning", "",
          "*\"Any numeric present without `source_url` / `source_publisher` / `source_date` is a HARD "
          "FAILURE.\" An event with one cannot be COMPLETE whatever else it carries: it is INVALID, "
          "because an unsourced magnitude is invisible downstream and that is the failure that "
          "produced `severity`.*", ""]
    if not hf["rows"]:
        L += ["None. Every filled numeric in every block names a source and a date.", ""]
    else:
        L += [f"**{hf['n']} event(s):**", "", "| block | event | failure |", "|---|---|---|"]
        for r in hf["rows"]:
            for f in r["hard_failures"]:
                L.append(f"| {r['block']} | `{r['event_id']}` | {f} |")
        L.append("")
    dv = cov["declared_vs_computed_disagreements"]
    L += ["## Declared status vs computed status", ""]
    if not dv["rows"]:
        L += ["No disagreements: every block's self-declared status matches the computed one.", ""]
    else:
        L += [f"**{dv['n']} disagreement(s).** The computed value governs.", "",
              "| block | event | declared | computed |", "|---|---|---|---|"]
        for r in dv["rows"]:
            L.append(f"| {r['block']} | `{r['event_id']}` | {r['declared']} | **{r['computed']}** |")
        L.append("")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    res = validate_all()
    cov = coverage(res)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"coverage": cov, "events": res}, indent=1, ensure_ascii=False))
    write_md(cov)
    t = cov["total"]
    print(f"exposure coverage: {cov['n_events']} events across {len(cov['by_block'])} blocks")
    for b, v in cov["by_block"].items():
        print(f"  {b}: n={v['n']:<3} COMPLETE {v['COMPLETE']:<3} PARTIAL {v['PARTIAL']:<3} "
              f"EMPTY {v['EMPTY']:<3} INVALID {v['INVALID']}")
    print(f"  TOTAL: COMPLETE {t['COMPLETE']}  PARTIAL {t['PARTIAL']}  EMPTY {t['EMPTY']}  INVALID {t['INVALID']}")
    g = cov["gate"]
    print(f"  §5 gate: {g['n_complete']} / {GATE_N} -> {'MET' if g['gate_met'] else 'NOT MET (Stage 1 descriptive only)'}")
    print(f"  hard failures: {cov['hard_failures']['n']}; declared-vs-computed disagreements: "
          f"{cov['declared_vs_computed_disagreements']['n']}")
    print(f"  -> {OUT_JSON.relative_to(ROOT)} + {OUT_MD.relative_to(ROOT)}")
    if "--strict" in sys.argv and cov["hard_failures"]["n"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
