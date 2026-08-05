"""
kappa_report.py -- Cohen's kappa per field, Joe's blind codes vs the corpus (FINAL_PLAN F2.2, machine side).

After Joe fills data/kappa_responses.csv (the blind sheet from kappa_sheet.py), this pairs his codes to
the corpus codes (via the hidden key) and computes Cohen's kappa per field: type, severity, surprise,
date. Threshold (BULLETPROOF Q5): kappa < 0.70 on any field -> that field's codebook criteria get ONE
documented revision pass. Writes data/kappa_report.md (goes into the paper's methods).

If Joe hasn't coded yet, it says so and writes a placeholder -- never invents agreement. numpy-free.

Run:  python3 src/kappa_report.py
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESP = ROOT / "data" / "kappa_responses.csv"
KEY = ROOT / "data" / "kappa_key.csv"
OUT = ROOT / "data" / "kappa_report.md"
THRESHOLD = 0.70


def cohen_kappa(a, b):
    """Cohen's kappa for two paired label lists (nominal). None if undefined."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return None if abs(1 - pe) < 1e-12 else round((po - pe) / (1 - pe), 3)


def _load(path):
    return {r["row_id"]: r for r in csv.DictReader(open(path, newline="", encoding="utf-8"))} \
        if path.exists() else {}


def run():
    resp, key = _load(RESP), _load(KEY)
    # only rows Joe actually coded (all four fields non-blank)
    coded = [rid for rid in key
             if rid in resp and all((resp[rid].get(f) or "").strip()
                                    for f in ("type", "severity", "surprise", "date"))]
    if not coded:
        return {"ran": False, "reason": "no coded rows yet in kappa_responses.csv (Joe fills the blind sheet first)",
                "n_key": len(key)}

    fields = {}
    for f in ("type", "severity", "surprise"):
        a = [(resp[r].get(f) or "").strip() for r in coded]
        b = [(key[r].get(f) or "").strip() for r in coded]
        agree = sum(x == y for x, y in zip(a, b))
        fields[f] = {"kappa": cohen_kappa(a, b), "exact_agree": round(agree / len(coded), 3),
                     "n": len(coded)}
    # ordinal within-1 for severity/surprise
    for f in ("severity", "surprise"):
        w1 = 0
        for r in coded:
            try:
                w1 += abs(int(resp[r][f]) - int(key[r][f])) <= 1
            except ValueError:
                pass
        fields[f]["within_1"] = round(w1 / len(coded), 3)
    # date: exact-day + within-3-days (kappa is not meaningful for a continuous date)
    from datetime import datetime
    exact = wd = 0
    for r in coded:
        try:
            ja = datetime.strptime((resp[r]["date"] or "")[:10], "%Y-%m-%d").date()
            ca = datetime.strptime((key[r]["date"] or "")[:10], "%Y-%m-%d").date()
            exact += ja == ca; wd += abs((ja - ca).days) <= 3
        except ValueError:
            pass
    fields["date"] = {"exact_agree": round(exact / len(coded), 3),
                      "within_3_days": round(wd / len(coded), 3), "n": len(coded), "kappa": None}
    return {"ran": True, "n_coded": len(coded), "fields": fields}


def write_md(r):
    L = ["# Inter-coder reliability (Cohen's kappa) -- F2.2 / BULLETPROOF Q5", ""]
    if not r.get("ran"):
        L += [f"*{r.get('reason')}* ({r.get('n_key', 0)} events in the blind sheet.)",
              "", "Run `python3 src/kappa_sheet.py`, have Joe code `data/kappa_responses.csv`,",
              "then re-run `python3 src/kappa_report.py`."]
        OUT.write_text("\n".join(L) + "\n"); return
    L += [f"Second coder (Joe) vs the corpus codes, on a blind sample of **n={r['n_coded']}** events",
          "(coded from sources only; codes hidden). Threshold: kappa < 0.70 on any field triggers one",
          "documented codebook-criteria revision pass.", "",
          "| field | Cohen's kappa | exact agreement | note |", "|---|---|---|---|"]
    f = r["fields"]
    L.append(f"| type | **{f['type']['kappa']}** | {f['type']['exact_agree']} | nominal |")
    L.append(f"| severity (1-5) | **{f['severity']['kappa']}** | {f['severity']['exact_agree']} | within-1: {f['severity']['within_1']} |")
    L.append(f"| surprise (1-5) | **{f['surprise']['kappa']}** | {f['surprise']['exact_agree']} | within-1: {f['surprise']['within_1']} |")
    L.append(f"| date | n/a (continuous) | {f['date']['exact_agree']} | within-3-days: {f['date']['within_3_days']} |")
    flags = [k for k in ("type", "severity", "surprise")
             if f[k]["kappa"] is not None and f[k]["kappa"] < THRESHOLD]
    L += ["", (f"**Below threshold (<{THRESHOLD}): {', '.join(flags)}** -> revise those fields' codebook "
               "criteria once, document the change." if flags else
               f"**All fields kappa >= {THRESHOLD}** -- inter-coder reliability is credentialed.")]
    OUT.write_text("\n".join(L) + "\n")


def main():
    r = run()
    write_md(r)
    if not r.get("ran"):
        print(f"kappa: {r.get('reason')}")
    else:
        f = r["fields"]
        print(f"kappa (n={r['n_coded']}): type {f['type']['kappa']}, severity {f['severity']['kappa']}, "
              f"surprise {f['surprise']['kappa']}, date exact {f['date']['exact_agree']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
