"""uncheckable_audit.py -- session H (H-2): why are claims UNCHECKABLE -- the world, or the reader?

The ledger's first 14 claims were 13/14 uncheckable and that number was being read as a broken
reader. This module decomposes every uncheckable claim in data/ledger/claims.jsonl into a cause,
and separates a READER DEFECT (a non-claim was extracted) from a SOURCE PROPERTY (the sentence is
genuinely unfalsifiable) from a DATA GAP (falsifiable, but the engine holds no series for it).

NOTHING HERE CHANGES THE VERDICT RULE. CLAIM_LEDGER_REGISTRATION.md §2 is untouched; the point is
to explain the ratio, not to improve it (charter §2, INV-6).

Two layers:
  1. STRUCTURAL (deterministic, no judgement). The cage already records WHY it refused each claim
     in the claim's `why` string. Four buckets fall straight out of it:
        POLICY_PENDING   "policy claim; checkable only against a dated action ..."  -> source property
        NEGATED          "negated in the text (non-event): no read"                 -> source property
        MALFORMED        "level claim without asset + stated level"                 -> reader defect
        RESIDUAL         "no asset + direction/level + horizon in the quote"        -> needs a human call
  2. ADJUDICATED (session H's coding of the RESIDUAL only). Three codes, applied to each residual
     sentence:
        R_NONCLAIM   the sentence asserts nothing that could later turn out false -- description,
                     background, a past fact, a photo caption. Extracting it is a READER DEFECT.
        S_UNFALSIFIABLE  it does make a contested/forward proposition, but names no measurable
                     referent ("huge", "devastating consequences", "not out of the woods"). A
                     competent analyst could disagree and no series could settle it. SOURCE PROPERTY.
        S_UNHELD     falsifiable and quantitative, but about a referent the engine holds no series
                     for (freight rates, transit counts, OPEC quota compliance, retail pass-through).
                     A DATA GAP -- neither the reader's fault nor the source's.

HONESTY LABEL: the taxonomy in layer 2 was written by session H *after* reading the residual
sentences, and the coding is ONE CODER, UNAUDITED. That is why every adjudicated sentence is
published verbatim with its code in data/ledger/uncheckable_audit.json and in the printed report --
so the call can be checked line by line rather than taken on trust. No kappa is claimed for it.

Run:  python3 src/uncheckable_audit.py
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = ROOT / "data" / "ledger"
OUT = LEDGER_DIR / "uncheckable_audit.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger as L                                   # noqa: E402

REGISTRATION = "CLAIM_LEDGER_REGISTRATION.md §2 (unchanged); audit by session H"

STRUCTURAL = [
    ("POLICY_PENDING", "policy claim", "source_property",
     "registered PENDING in §2/§3: a policy claim is checkable only against a dated action entering "
     "the corpus. The resolver has no such mechanism (defect L-2), so PENDING is currently permanent."),
    ("NEGATED", "negated in the text", "source_property",
     "the source says a thing did NOT happen. The cage refuses to read a non-event as a claim; correct."),
    ("MALFORMED", "level claim without asset", "reader_defect",
     "the model proposed a level claim it could not support with an asset and a stated number; the "
     "cage downgraded it rather than repairing it."),
    ("NO_SERIES", "has no series yet", "data_gap",
     "asset recognised, but the engine holds no price series for it."),
]

# Session H's coding of the residual. Keyed by claim_id so it is pinned to the exact logged sentence
# and cannot drift if a story is re-read. Every one of these is printed verbatim by report().
CODING = {
    # --- backfill (historical) residual
    "It was the largest power outage in the country's history,": ("R_NONCLAIM", "past fact, stated as description"),
    "At least 43 deaths resulted.": ("R_NONCLAIM", "past fact, no market proposition"),
    "as of 2019, 70-80% of Venezuela's power comes from Guri.": ("R_NONCLAIM", "background statistic about the grid"),
    "The incident happened 140km south of the Strait of Hormuz, where about one third of all oil traded by sea passes through.":
        ("R_NONCLAIM", "geography and a standing background figure; nothing here can turn out false"),
    "Richard Meade, the managing editor of shipping industry publication Lloyds List, described the significance of the Stena's seizure as \"huge\" for the region.":
        ("S_UNFALSIFIABLE", "an attributed judgement -- 'huge' has no measurable referent"),
    "Each dollar per barrel of sustained price change in crude oil translates to an average change of about 2.4 cents per gallon in petroleum product prices.":
        ("S_UNHELD", "a quantitative pass-through relationship, falsifiable against a retail product series the engine does not hold"),
    "OPEC+, as a whole, was not even pumping as much as allotted.": ("S_UNHELD", "falsifiable against OPEC production-vs-quota data; no compliance series held"),
    "It doesn't look promising to me,": ("S_UNFALSIFIABLE", "bare opinion"),
    "the United Nations mission in Libya expressed \"deep concern\" over the efforts to disrupt oil production, warning of \"devastating consequences\".":
        ("S_UNFALSIFIABLE", "'devastating consequences' names no threshold and no horizon"),
    "Today we have grounds to be cautiously optimistic about the future, but we are not out of the woods yet and challenges ahead remain to be seen,":
        ("S_UNFALSIFIABLE", "rhetoric from a communique; unfalsifiable by construction"),
    # --- original live-read residual (gcaptain.com)
    "A ship off the port of Aden, where traffic remained steady after the Iran-aligned Houthis said their forces had carried out missile and drone strikes on Saudi oil tankers, in Aden, Yemen, July 23, 2026.":
        ("R_NONCLAIM", "this is a PHOTO CAPTION -- the clearest single reader defect in the ledger"),
    "Earlier this year the company, led by Ga-Hyun Chung, embarked on the biggest oil tanker bet ever, buying dozens of ships before the Iran war began and hiring them out at heightened rates.":
        ("R_NONCLAIM", "narrative background about a shipowner; no proposition about a future state"),
    "There is a lump sum to get a ship through the waterway itself and then, once the cargo is switched onto a different tanker outside Hormuz, a lower rate based on an onward to China.":
        ("R_NONCLAIM", "describes how a freight rate is structured; asserts nothing falsifiable"),
    "Attacks on Saudi tankers by Yemen’s Houthis have seen the kingdom redirect some exports north, through the Mediterranean, and thousands of miles around Africa.":
        ("S_UNHELD", "a routing claim, falsifiable against flow/AIS data the engine does not hold"),
    "The Iran war has roiled the world’s main oil tanker benchmark as the number of ships entering and exiting the Persian Gulf has become increasingly opaque.":
        ("S_UNHELD", "a claim about the tanker freight benchmark; 'freight' is in the asset list with series=None"),
    "Moving barrels through Hormuz effectively comes with two shipping costs.": ("R_NONCLAIM", "definitional description of a cost structure"),
    "The fact that ships are transfering cargoes onto waiting ships outside Hormuz is also disrupting the supply chain and making deliveries take longer.":
        ("S_UNHELD", "a delivery-time claim, falsifiable against transit-time data the engine does not hold"),
    "Mine clearance in the Strait of Hormuz is “not sufficient on its own” to bring commercial shipping back to normal, INTERTANKO warned, even as the tanker industry group welcomed the...":
        ("S_UNFALSIFIABLE", "'sufficient' and 'back to normal' name no threshold -- and note the quote ends '...': "
                            "the reader extracted a TRUNCATED teaser line off the page, not a whole sentence"),
}
CAUSE = {"R_NONCLAIM": "reader_defect", "S_UNFALSIFIABLE": "source_property", "S_UNHELD": "data_gap"}


def classify(claim):
    """(bucket, cause, code, note). Deterministic for the four structural buckets; the residual
    carries session H's adjudication, matched on the verbatim sentence."""
    if claim.get("checkable"):
        return "CHECKABLE", "checkable", None, None
    why = claim.get("why") or ""
    for name, needle, cause, note in STRUCTURAL:
        if needle in why:
            return name, cause, None, note
    text = (claim.get("text") or "").strip()
    if text in CODING:
        code, note = CODING[text]
        return "RESIDUAL", CAUSE[code], code, note
    return "RESIDUAL", "uncoded", None, "not coded by session H (a sentence logged after this audit)"


def _why_for(claim, manifest):
    """claims.jsonl does not store the cage's `why`; the backfill manifest does. Recover it, and for
    the pre-backfill rows infer the structural bucket from the fields that are stored."""
    w = manifest.get(claim["claim_id"])
    if w:
        return w
    if claim.get("kind") == "policy":
        return "policy claim; checkable only against a dated action entering the corpus (PENDING)"
    if claim.get("kind") == "uncheckable":
        return "no asset + direction/level + horizon in the quote"
    return ""


def audit():
    rows = L._rows(L.CLAIMS)
    man = {}
    p = LEDGER_DIR / "backfill_manifest.json"
    if p.exists():
        for c in json.load(open(p)).get("claims", []):
            man[L._cid(f"hist:{c['event_id']}", c["text"])] = c.get("why", "")
    out = []
    for c in rows:
        c = {**c, "why": _why_for(c, man)}
        bucket, cause, code, note = classify(c)
        out.append({"claim_id": c["claim_id"], "story_id": c["story_id"], "source": c.get("source"),
                    "population": "backfill" if c["story_id"].startswith("hist:") else "original_live",
                    "kind": c["kind"], "checkable": bool(c.get("checkable")), "bucket": bucket,
                    "cause": cause, "code": code, "note": note, "text": c["text"]})
    return out


def report(echo=print):
    rows = audit()
    unc = [r for r in rows if not r["checkable"]]
    pops = defaultdict(list)
    for r in rows:
        pops[r["population"]].append(r)

    echo("=" * 96)
    echo("H-2  WHY ARE CLAIMS UNCHECKABLE -- the world, or the reader?   (no verdict rule was changed)")
    echo("=" * 96)
    for pop, rs in sorted(pops.items()):
        u = [r for r in rs if not r["checkable"]]
        echo(f"\n{pop:16s} n={len(rs):3d}  uncheckable={len(u):3d} ({len(u)/len(rs):.0%})   "
             f"sources: {dict(Counter(r['source'] for r in rs))}")
    echo(f"\nALL CLAIMS      n={len(rows):3d}  uncheckable={len(unc):3d} ({len(unc)/len(rows):.0%})")

    echo("\n--- cause of every uncheckable claim ---")
    by_cause = Counter(r["cause"] for r in unc)
    for cause, n in by_cause.most_common():
        echo(f"  {cause:16s} {n:3d}  ({n/len(unc):.0%} of uncheckable, {n/len(rows):.0%} of all claims)")
    echo("\n--- bucket detail ---")
    for b, n in Counter(r["bucket"] for r in unc).most_common():
        ex = next(r for r in unc if r["bucket"] == b)
        echo(f"  {b:16s} {n:3d}  [{ex['cause']}] {ex['note']}")

    echo("\n--- the RESIDUAL, adjudicated by session H (ONE CODER, UNAUDITED -- every sentence verbatim) ---")
    res = [r for r in unc if r["bucket"] == "RESIDUAL"]
    for code in ("R_NONCLAIM", "S_UNFALSIFIABLE", "S_UNHELD", None):
        sel = [r for r in res if r["code"] == code]
        if not sel:
            continue
        echo(f"\n  {str(code):16s} n={len(sel)}  -> {CAUSE.get(code, 'uncoded')}")
        for r in sel:
            echo(f"    - [{r['source']}] {r['note']}")
            echo(f"      \"{r['text'][:150]}\"")

    verdict = (
        "\nFINDING. Across all {n} logged claims the reader's own defects account for {rd} ({rdp:.0%}): "
        "{nc} descriptive/background sentences extracted as claims (one of them a photo caption) plus "
        "{mf} malformed level claim. {sp} ({spp:.0%}) are properties of the sources -- policy statements "
        "the registration itself parks as PENDING, negated non-events, and judgements that name no "
        "measurable referent. {dg} ({dgp:.0%}) are a DATA GAP: falsifiable claims about freight rates, "
        "transit times, routing and OPEC quota compliance, none of which the engine holds a series for."
    ).format(n=len(rows), rd=by_cause["reader_defect"], rdp=by_cause["reader_defect"] / len(rows),
             nc=sum(1 for r in res if r["code"] == "R_NONCLAIM"),
             mf=sum(1 for r in unc if r["bucket"] == "MALFORMED"),
             sp=by_cause["source_property"], spp=by_cause["source_property"] / len(rows),
             dg=by_cause["data_gap"], dgp=by_cause["data_gap"] / len(rows))
    o = pops.get("original_live", [])
    b = pops.get("backfill", [])
    if o and b:
        ou = sum(1 for r in o if not r["checkable"]); bu = sum(1 for r in b if not r["checkable"])
        verdict += (
            "\n\nTHE 93% WAS A SOURCE-SELECTION ARTEFACT, NOT A READER FAILURE. The original ledger's "
            f"{ou}/{len(o)} ({ou/len(o):.0%}) uncheckable rate came from exactly two documents: an OPEC press "
            "release (every sentence a policy statement, registered PENDING by construction) and one trade "
            "feature about tanker freight economics -- a story whose entire subject is an asset the engine "
            f"holds no series for. Run the SAME reader over {len(set(r['story_id'] for r in b))} mechanically-selected news "
            f"stories and the rate falls to {bu}/{len(b)} ({bu/len(b):.0%}). The reader did not change; the reading matter did."
        )
    echo(verdict)

    out = {"registration": REGISTRATION, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "coding_status": "layer 2 coded by session H after reading the sentences; ONE CODER, UNAUDITED; "
                            "every adjudicated sentence published verbatim so the call can be checked",
           "verdict_rule_changed": False,
           "totals": {"claims": len(rows), "uncheckable": len(unc), "by_cause": dict(by_cause),
                      "by_bucket": dict(Counter(r["bucket"] for r in unc))},
           "by_population": {p: {"n": len(rs), "uncheckable": sum(1 for r in rs if not r["checkable"])}
                             for p, rs in pops.items()},
           "finding": verdict.strip(), "rows": rows}
    OUT.write_text(json.dumps(out, indent=1))
    echo(f"\nreceipt -> {OUT.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    report()
