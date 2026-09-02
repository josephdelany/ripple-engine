"""reader_eval.py -- Brief A-9: the desk measures its own reading (NORTH_STAR).

Scores reader.read_headlines on data/reader_eval/gold_100.jsonl (100 real corpus headlines 1990-2026, class + entities +
knowable date coded by hand IN THE CODEBOOK'S TERMS by session A, unaudited by Joe): class accuracy, entity F1 (micro,
over entity ids), date exactness. Writes data/reader_eval/score.json with the reader mode actually used per headline
(llm / regex_fallback / cached) so a fallback run can never pass as a model run. The gold is never edited by this code.

Run:  python3 src/reader_eval.py              # the reader in its normal (auto) mode
      python3 src/reader_eval.py --fallback   # the regex fallback only (sets the reader's off switch for this run)
"""
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
GOLD = ROOT / "data" / "reader_eval" / "gold_100.jsonl"
OUT = ROOT / "data" / "reader_eval" / "score.json"


def load_gold(path=GOLD):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def score(gold, reads):
    """Pure: (gold rows, reader outputs in the same order) -> the score dict."""
    n = len(gold)
    cls_ok = sum(1 for g, r in zip(gold, reads) if (r.get("event_class") or None) == g["gold_class"])
    tp = fp = fn = 0
    per_class = {}
    for g, r in zip(gold, reads):
        got = {e["id"] if isinstance(e, dict) else e for e in (r.get("entities") or [])}
        want = set(g["gold_entities"])
        tp += len(got & want); fp += len(got - want); fn += len(want - got)
        pc = per_class.setdefault(g["gold_class"], {"n": 0, "correct": 0})
        pc["n"] += 1; pc["correct"] += int((r.get("event_class") or None) == g["gold_class"])
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    dates = [(g["gold_knowable_date"], r.get("knowable") or r.get("date")) for g, r in zip(gold, reads)]
    dated = [1 for gd, rd in dates if rd]
    exact = sum(1 for gd, rd in dates if rd and str(rd)[:10] == gd)
    modes = Counter((r.get("reader") or {}).get("mode", "?") for r in reads)
    conf = Counter((g["gold_class"], r.get("event_class") or "none") for g, r in zip(gold, reads) if (r.get("event_class") or None) != g["gold_class"])
    return {"n": n, "class_accuracy": round(cls_ok / n, 4), "class_correct": cls_ok, "per_class": per_class,
            "entity_precision": round(prec, 4), "entity_recall": round(rec, 4), "entity_f1": round(f1, 4), "entity_tp_fp_fn": [tp, fp, fn],
            "date_exactness": {"n_with_a_reader_date": len(dated), "exact": exact,
                               "note": "read_headlines emits no date from a bare headline; exactness is scored only where the reader returned one"},
            "reader_modes": dict(modes), "top_confusions": [{"gold": g, "read": r, "n": c} for (g, r), c in conf.most_common(8)]}


def run(fallback=False):
    if fallback:
        os.environ["RIPPLE_READER"] = "off"
    import reader as R
    gold = load_gold()
    heads = [g["headline"] for g in gold]
    reads = R.read_headlines(heads, use_cache=not fallback)
    s = score(gold, reads)
    s.update({"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "gold": str(GOLD.relative_to(ROOT)),
              "gold_status": "coded by session A, unaudited by Joe", "reader_env": os.environ.get("RIPPLE_READER", "auto"),
              "model": (reads[0].get("reader") or {}).get("model") if reads else None,
              "label": "reader accuracy (unaudited gold)", "threshold_class": 0.8})
    OUT.write_text(json.dumps(s, indent=1))
    print(f"reader eval: class accuracy {s['class_accuracy']} ({s['class_correct']}/{s['n']}), entity F1 {s['entity_f1']}, modes {s['reader_modes']} -> {OUT.relative_to(ROOT)}")
    for c in s["top_confusions"]:
        print(f"   gold {c['gold']:<22} read {c['read']:<22} x{c['n']}")
    return s


if __name__ == "__main__":
    run(fallback="--fallback" in sys.argv)
