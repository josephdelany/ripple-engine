"""audit_reader.py -- Joe's audit recorder for the READER gold set (session H, H-3).

Built on the model of src/audit_ies90.py, for the same reason: data/reader_eval/gold_100.jsonl was
coded by session A and the reader scores 84% against it -- a machine graded by a machine, labelled
"unaudited by Joe" and gated by nothing. This gives that number a way to become real.

Three things live here.

1. THE BLIND SHEET (--blind-sheet). A registered random 30 of the 100 (seed SEED, fixed below),
   emitted as headline + source only, with NO class, NO entities, NO date -- so a second coder can
   code them without seeing session A's answers. Written to data/reader_eval/blind_sheet_30.*.

2. INTER-CODER KAPPA (--kappa). Cohen's unweighted kappa on the 7 registered event classes plus
   `none`, between any two codings of the same headlines. Reported for A-vs-H (two Claude sessions),
   and for the READER against each coder, so it is visible whether the reader agrees with its own
   gold more than two coders agree with each other.
   *** THIS IS A DIAGNOSTIC, NOT AN AUDIT. *** Session A and session H are both Claude. A kappa
   between them measures whether the coding rule is legible, not whether it is right. Only Joe's
   answers (mode 3) can retire the "unaudited" label.

3. JOE'S AUDIT (default, resumable). Walks the same 30 headlines and asks Joe for HIS class before
   revealing anything. It deliberately differs from audit_ies90.py on one point: audit_ies90 shows
   the engine's level before asking, because there Joe is checking a label against source records;
   here showing the gold or the reader's call first would anchor the very judgement being measured,
   so both are hidden until Joe has answered. Answers are written after every row (resumable); a
   blank answer records nothing. `passed` is true only when every row is answered and kappa(Joe,
   reader) >= THRESHOLD.

Run:  python3 src/audit_reader.py --blind-sheet   # emit the 30 headlines with no labels
      python3 src/audit_reader.py --kappa         # inter-coder kappa (needs coding_H.jsonl)
      python3 src/audit_reader.py                 # Joe's audit, resume where he left off
      python3 src/audit_reader.py --status        # progress only, no questions
"""
import json
import random
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "data" / "reader_eval"
GOLD = EVAL / "gold_100.jsonl"
SHEET_JSON = EVAL / "blind_sheet_30.json"
SHEET_MD = EVAL / "blind_sheet_30.md"
CODING_H = EVAL / "coding_H.jsonl"                  # session H's blind coding
OUT = EVAL / "reader_audit.json"                    # Joe's answers
SCORE = EVAL / "score.json"
KAPPA_OUT = EVAL / "kappa_coders.json"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "state"))

SEED = 20260902                                     # registered before the sample was drawn
N_SAMPLE = 30
THRESHOLD = 0.6                                     # same bar as the IES-90 audit (WALK_FORWARD_PROTOCOL §1)
CLASSES = ("chokepoint_disruption", "conflict_escalation", "demand_shock", "infrastructure_attack",
           "opec_decision", "policy_response", "sanctions", "none")
MENU = {str(i + 1): c for i, c in enumerate(CLASSES)}


def load_gold(path=GOLD):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def sample_ids(gold=None):
    """The registered random 30. Deterministic in the gold's own ids, so the sheet is reproducible
    and cannot be re-drawn to a friendlier subset (REQ-H3-SAMPLE)."""
    gold = gold or load_gold()
    ids = sorted(str(g["id"]) for g in gold)
    return sorted(random.Random(SEED).sample(ids, min(N_SAMPLE, len(ids))))


def blind_sheet(echo=print):
    """Headline + source only. Never writes a class, an entity or a date: that is the whole point."""
    gold = load_gold()
    want = set(sample_ids(gold))
    rows = [{"id": str(g["id"]), "headline": g["headline"], "source_url": g.get("source_url")}
            for g in gold if str(g["id"]) in want]
    SHEET_JSON.write_text(json.dumps({"seed": SEED, "n": len(rows), "of": len(gold),
                                      "classes": list(CLASSES), "rows": rows}, indent=1))
    md = [f"# Blind coding sheet — {len(rows)} of {len(gold)} headlines (seed {SEED})", "",
          "Code each headline into ONE class. No labels from any other coder appear in this file.", "",
          "Classes: " + ", ".join(CLASSES), ""]
    for r in rows:
        md.append(f"- **{r['id']}** — {r['headline']}")
    SHEET_MD.write_text("\n".join(md) + "\n")
    echo(f"blind sheet: {len(rows)} headlines -> {SHEET_MD.relative_to(ROOT)} / {SHEET_JSON.relative_to(ROOT)}")
    echo("  contains headline + id only. No class, no entities, no date.")
    return rows


def _kappa(a, b, labels=CLASSES):
    import outcomes as O
    return O.cohen_kappa(list(a), list(b), labels=labels)


def _reader_calls(ids):
    """The reader's class per gold id, taken from the scored run if present (never re-read here)."""
    gold = {str(g["id"]): g for g in load_gold()}
    if not SCORE.exists():
        return {}
    # score.json stores aggregates, not per-row calls; recover per-row by re-scoring from the cache.
    import reader as R
    heads = [gold[i]["headline"] for i in ids]
    reads = R.read_headlines(heads, use_cache=True)
    return {i: (r.get("event_class") or "none") for i, r in zip(ids, reads)}


def kappa_report(echo=print, with_reader=True):
    """A vs H (and Joe, and the reader) on the blind 30. A DIAGNOSTIC, not an audit."""
    gold = {str(g["id"]): g for g in load_gold()}
    ids = sample_ids()
    A = {i: (gold[i]["gold_class"] or "none") for i in ids}
    H = {}
    if CODING_H.exists():
        for l in open(CODING_H, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                H[str(r["id"])] = r["class"] or "none"
    joe = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text()).get("rows", []):
            joe[str(r["id"])] = r["joe_class"]
    rd = _reader_calls(ids) if with_reader else {}

    out = {"seed": SEED, "n_sample": len(ids), "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "labels": list(CLASSES), "threshold": THRESHOLD,
           "WARNING": "Session A and session H are both Claude. A-vs-H kappa measures whether the coding "
                      "rule is legible to a second reading, NOT whether the gold is right. It cannot retire "
                      "the 'unaudited' label; only Joe's answers can.",
           "pairs": {}}
    def add(name, x, y, note):
        common = [i for i in ids if i in x and i in y]
        if not common:
            out["pairs"][name] = {"n": 0, "kappa": None, "note": note + " (no overlap yet)"}
            return
        k, n, conf = _kappa([x[i] for i in common], [y[i] for i in common])
        agree = sum(1 for i in common if x[i] == y[i])
        out["pairs"][name] = {"n": n, "kappa": k, "raw_agreement": round(agree / len(common), 4),
                              "note": note, "confusion": conf}
    add("A_vs_H", A, H, "session A's gold vs session H's blind coding -- two Claude sessions (diagnostic)")

    # BLINDNESS CAVEAT (session H, found by its own test). The sheet hides every label, but the gold's
    # *id slug* is printed next to each headline and some slugs contain their own class as a word
    # ("russia_sectoral_sanctions_2014" -> sanctions; every "opec_*" -> opec_decision). On those rows a
    # coder can score without reading the headline, so the headline kappa is inflated by construction.
    # Published, not corrected: re-drawing the sheet after seeing the answers is exactly what the
    # registered seed exists to prevent. The honest lower bound is the kappa on the rows that do NOT
    # telegraph. Reported for every pair.
    def _telegraphs(i, cls):
        return any(t in i.lower() for t in str(cls).split("_") if len(t) > 3)
    tele = [i for i in ids if _telegraphs(i, A.get(i) or "none")]
    clean_ids = [i for i in ids if i not in tele]
    caveat = {"n_telegraphed": len(tele), "n_total": len(ids), "telegraphed_ids": tele,
              "why": "the id slug printed on the sheet contains a token of the row's own gold class, so "
                     "that row can be coded without reading the headline",
              "subset_kappa_excluding_telegraphed": {}}
    for name, pair in (("A_vs_H", (A, H)), ("reader_vs_A", (rd, A)), ("reader_vs_H", (rd, H))):
        x, y = pair
        common = [i for i in clean_ids if i in x and i in y]
        if len(common) > 1:
            k, n, _ = _kappa([x[i] for i in common], [y[i] for i in common])
            caveat["subset_kappa_excluding_telegraphed"][name] = {"kappa": k, "n": n}
    out["blindness_caveat"] = caveat
    if rd:
        add("reader_vs_A", rd, A, "the reader against the gold it is scored on")
        add("reader_vs_H", rd, H, "the reader against an independent blind coding")
    if joe:
        add("joe_vs_reader", joe, rd, "JOE vs the reader -- the only pair that can retire 'unaudited'")
        add("joe_vs_A", joe, A, "JOE vs session A's gold")
    KAPPA_OUT.write_text(json.dumps(out, indent=1))
    echo(f"inter-coder kappa on the registered blind {len(ids)} (seed {SEED}):")
    for name, d in out["pairs"].items():
        echo(f"  {name:16s} kappa={str(d['kappa']):8s} raw={d.get('raw_agreement')}  n={d['n']}  -- {d['note']}")
    echo(f"  -> {KAPPA_OUT.relative_to(ROOT)}")
    echo("  " + out["WARNING"])
    return out


# ----------------------------------------------------------------------------- Joe's audit

def load_out(path=OUT):
    if Path(path).exists():
        return json.loads(Path(path).read_text())
    return {"auditor": "joe", "protocol": "CLAIM_LEDGER_REGISTRATION.md Amendment 3 (the caged reader); "
                                          "audit on the model of WALK_FORWARD_PROTOCOL.md §1", "threshold": THRESHOLD,
            "sheet": str(SHEET_JSON.relative_to(ROOT)), "seed": SEED, "started_at": None, "dated": None,
            "rows": [], "n_rows": None, "n_done": 0, "kappa_joe_vs_reader": None, "passed": False}


def show(r, i, n, echo=print):
    echo("=" * 78)
    echo(f"[{i}/{n}]  id {r['id']}")
    echo(f"  HEADLINE: {r['headline']}")
    if r.get("source_url"):
        echo(f"  source  : {r['source_url']}")
    echo("  (the gold label and the reader's call are hidden until you answer, so they cannot anchor you)")
    for k, c in MENU.items():
        echo(f"    {k}) {c}")


def ask_row(ask):
    while True:
        v = ask("  YOUR class (number, s = skip, q = quit): ").strip().lower()
        if v in ("q", "quit"):
            return "quit"
        if v in ("s", "skip", ""):
            return None
        if v in MENU:
            break
        echo_opts = ", ".join(MENU)
        print(f"  enter one of {echo_opts}, s or q")
    note = ask("  note (why; blank ok): ").strip()
    return {"joe_class": MENU[v], "joe_note": note}


def run(ask=input, echo=print):
    gold = {str(g["id"]): g for g in load_gold()}
    ids = sample_ids()
    rows = OrderedDict((i, {"id": i, "headline": gold[i]["headline"], "source_url": gold[i].get("source_url")}) for i in ids)
    out = load_out()
    out["started_at"] = out.get("started_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
    done = {str(r["id"]) for r in out["rows"]}
    echo(f"Reader gold audit -- {len(done)} of {len(rows)} answered. Auditor: joe. q to stop; answers save as you go.")
    echo("Each headline is coded by you FIRST; the gold and the reader's call are revealed after.")
    rd = _reader_calls(ids)
    n = len(rows)
    for i, (rid, r) in enumerate(rows.items(), 1):
        if rid in done:
            continue
        show(r, i, n, echo)
        ans = ask_row(ask)
        if ans == "quit":
            break
        if ans is None:
            echo("  skipped (nothing recorded)")
            continue
        g = gold[rid]["gold_class"] or "none"
        rc = rd.get(rid, "none")
        echo(f"  -> you: {ans['joe_class']}   session A's gold: {g}   the reader: {rc}"
             + ("   [all three agree]" if ans["joe_class"] == g == rc else ""))
        out["rows"].append({**r, **ans, "gold_class_A": g, "reader_class": rc,
                            "answered_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        finalize(out, n)
        OUT.write_text(json.dumps(out, indent=1))
    finalize(out, n)
    OUT.write_text(json.dumps(out, indent=1))
    echo(f"saved {OUT.name}: {out['n_done']}/{out['n_rows']} answered, kappa(joe,reader)={out['kappa_joe_vs_reader']}, passed {out['passed']}")
    return out


def finalize(out, n_rows):
    rows = out["rows"]
    k_r, n_r, conf = _kappa([r["joe_class"] for r in rows], [r["reader_class"] for r in rows]) if rows else (None, 0, {})
    k_a, _, _ = _kappa([r["joe_class"] for r in rows], [r["gold_class_A"] for r in rows]) if rows else (None, 0, {})
    out["n_rows"] = n_rows
    out["n_done"] = len(rows)
    out["kappa_joe_vs_reader"] = k_r
    out["kappa_joe_vs_gold_A"] = k_a
    out["confusion_joe_x_reader"] = conf
    out["passed"] = bool(n_rows and len(rows) == n_rows and k_r is not None and k_r >= THRESHOLD)
    out["dated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return out


def status():
    """What every surface showing reader accuracy must read before it prints a number."""
    ids = sample_ids() if GOLD.exists() else []
    st = {"audited_by_joe": False, "n_done": 0, "n_rows": len(ids), "kappa_joe_vs_reader": None,
          "passed": False, "threshold": THRESHOLD, "seed": SEED}
    if OUT.exists():
        o = json.loads(OUT.read_text())
        st.update(n_done=o.get("n_done", 0), kappa_joe_vs_reader=o.get("kappa_joe_vs_reader"),
                  passed=bool(o.get("passed")), audited_by_joe=bool(o.get("n_done")), dated=o.get("dated"))
    if KAPPA_OUT.exists():
        kk = json.loads(KAPPA_OUT.read_text())
        st["kappa_A_vs_H"] = (kk.get("pairs", {}).get("A_vs_H") or {}).get("kappa")
        st["kappa_A_vs_H_n"] = (kk.get("pairs", {}).get("A_vs_H") or {}).get("n")
    kv = st.get("kappa_A_vs_H")
    st["label"] = ("reader accuracy, audited by Joe (kappa {k} vs the reader, n={n})".format(
        k=st["kappa_joe_vs_reader"], n=st["n_done"]) if st["passed"] else
        "reader accuracy: UNAUDITED (inter-coder kappa {k} between sessions A and H, n={n}; "
        "both are Claude -- a legibility check, not a human audit)".format(
            k=kv if kv is not None else "not yet computed", n=st.get("kappa_A_vs_H_n", 0)))
    return st


if __name__ == "__main__":
    if "--blind-sheet" in sys.argv:
        blind_sheet()
    elif "--kappa" in sys.argv:
        kappa_report()
    elif "--status" in sys.argv:
        print(json.dumps(status(), indent=1))
    else:
        run()
