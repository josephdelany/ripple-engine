"""
calibrate_corroboration.py -- calibrate the corroboration weights against resolved
outcomes (same log -> resolve -> score pattern as the reads ledger).

WHAT IS BEING CALIBRATED (and against what): the corroboration engine outputs a
CONFIDENCE that an event is real. Calibration asks: of the events it called ~60%
likely, do ~60% turn out real? To answer that we need RESOLVED LABELS, and the honest
ground truth is the human gate:
  * AUTO-POSITIVE: if a logged event's source_url later lands in the coded `events`
    table (promoted through the gate), it was real -> label 1.
  * NEGATIVE labels are a human judgement ("that corroborated cluster was noise") --
    we deliberately do NOT auto-assign 0 (absence of promotion != not real), because a
    biased auto-negative would wrongly collapse the engine's confidence.
So this is human-in-the-loop: it logs predictions, auto-confirms positives from the
gate, and surfaces the top unlabeled events for a quick real/not tag (the `label`
column of data/state/corroboration_log.csv). It refits the prior ONLY when there is a
balanced labeled set; until then it reports reliability and leaves the weights alone.

The refit is conservative: it calibrates the PRIOR to the observed base rate (the most
impactful, most directly estimable weight) and reports the observed real-rate by
independent-source count (the evidence for tuning the per-source decibans later). It
writes data/corroboration_weights.json, which corroborate.py reads next run.

Run:  python3 src/calibrate_corroboration.py
"""

import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CORR = ROOT / "data" / "corroboration.json"
LEDGER = ROOT / "data" / "state" / "corroboration_log.csv"
WEIGHTS = ROOT / "data" / "corroboration_weights.json"
REPORT = ROOT / "data" / "corroboration_calibration.json"
FIELDS = ["event_key", "situation_id", "made_at", "confidence", "n_independent",
          "headline", "source_urls", "resolved_at", "label"]
MIN_LABELS = 30            # need this many labeled events (both classes) to refit


def event_key(situation_id, headline):
    return hashlib.sha1(f"{situation_id}|{(headline or '').lower()}"
                        .encode("utf-8", "replace")).hexdigest()[:16]


def brier(preds, labels):
    """Mean squared error of probabilistic predictions (strictly proper)."""
    if not preds:
        return None
    return round(sum((p - y) ** 2 for p, y in zip(preds, labels)) / len(preds), 4)


def reliability_buckets(preds, labels, edges=(0, 0.25, 0.45, 0.75, 1.01)):
    """Per confidence band: mean predicted prob vs observed real-rate + n. This is
    the reliability diagram -- the core calibration diagnostic."""
    out = []
    for lo, hi in zip(edges, edges[1:]):
        idx = [i for i, p in enumerate(preds) if lo <= p < hi]
        if idx:
            mp = sum(preds[i] for i in idx) / len(idx)
            obs = sum(labels[i] for i in idx) / len(idx)
            out.append({"band": f"{lo:.2f}-{hi:.2f}", "n": len(idx),
                        "mean_pred": round(mp, 3), "observed_rate": round(obs, 3)})
    return out


def load_ledger():
    if not LEDGER.exists():
        return {}
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return {r["event_key"]: r for r in csv.DictReader(f)}


def log_predictions(rows, corr_data, now):
    """Upsert each current corroboration event into the ledger. The prediction is
    logged at FIRST sighting (confidence frozen then); later runs only refresh the
    source_urls (so a promotion can be matched)."""
    for sid, events in (corr_data.get("situations") or {}).items():
        for ev in events:
            k = event_key(sid, ev.get("headline"))
            urls = "|".join(ev.get("source_urls", []))
            if k in rows:
                rows[k]["source_urls"] = urls or rows[k]["source_urls"]
            else:
                rows[k] = {"event_key": k, "situation_id": sid, "made_at": now,
                           "confidence": ev.get("confidence"),
                           "n_independent": ev.get("n_independent_sources"),
                           "headline": ev.get("headline", "")[:120],
                           "source_urls": urls, "resolved_at": "", "label": ""}
    return rows


def auto_confirm(rows, coded_urls, now):
    """Gate ground truth: any logged event whose source_url is now a coded event ->
    label 1 (confirmed real). Positive-only; never auto-negative."""
    n = 0
    for r in rows.values():
        if r["label"] == "" and any(u in coded_urls for u in
                                    (r["source_urls"] or "").split("|") if u):
            r["label"], r["resolved_at"] = "1", now
            n += 1
    return n


def calibrate(rows):
    """Reliability over labeled rows; refit the prior to the observed base rate when
    there is a balanced, sufficient labeled set."""
    labeled = [(float(r["confidence"]), int(r["label"]), int(r["n_independent"] or 0))
               for r in rows.values() if r["label"] in ("0", "1") and r["confidence"]]
    n = len(labeled)
    if not n:
        return {"n_labeled": 0, "note": "no labeled events yet -- tag the `label` "
                "column (1=real, 0=noise) to begin calibrating."}
    preds = [p for p, _, _ in labeled]
    labs = [y for _, y, _ in labeled]
    pos, neg = sum(labs), n - sum(labs)
    report = {"n_labeled": n, "positives": pos, "negatives": neg,
              "base_rate": round(sum(labs) / n, 3), "brier": brier(preds, labs),
              "reliability": reliability_buckets(preds, labs)}
    # observed real-rate by independent-source count (evidence for tuning decibans).
    by_n = {}
    for _p, y, ni in labeled:
        by_n.setdefault(ni, []).append(y)
    report["real_rate_by_sources"] = {str(k): round(sum(v) / len(v), 3)
                                      for k, v in sorted(by_n.items())}
    report["refit"] = None
    if n >= MIN_LABELS and pos and neg:      # only refit on a real, balanced set
        report["refit"] = {"prior_prob": round(sum(labs) / n, 3)}
    return report


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = load_ledger()
    if CORR.exists():
        try:
            log_predictions(rows, json.loads(CORR.read_text()), now)
        except (ValueError, OSError):
            pass
    conn = sqlite3.connect(DB)
    coded = {u for (u,) in conn.execute("SELECT source_url FROM events") if u}
    conn.close()
    confirmed = auto_confirm(rows, coded, now)

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: r["made_at"]))

    rep = calibrate(rows)
    rep["as_of"] = now[:10]
    REPORT.write_text(json.dumps(rep, indent=2))

    if rep.get("refit"):
        base = json.loads(WEIGHTS.read_text()) if WEIGHTS.exists() else {}
        base.update(rep["refit"])
        WEIGHTS.write_text(json.dumps(base, indent=2))
        print(f"calibrate_corroboration -- REFIT prior to {rep['refit']['prior_prob']} "
              f"on {rep['n_labeled']} labeled events (Brier {rep['brier']}).")
    else:
        print(f"calibrate_corroboration -- {len(rows)} predictions logged, "
              f"{confirmed} gate-confirmed this run; "
              f"{rep.get('n_labeled', 0)} labeled. "
              f"{'Brier ' + str(rep['brier']) if rep.get('brier') is not None else 'Label events to calibrate.'}")


if __name__ == "__main__":
    main()
