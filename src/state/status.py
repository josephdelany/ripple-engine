"""status.py -- one command for the state panel (PATH Step 2 acceptance): which loaders are green, stubbed,
or failed, and coverage per block per decade -- printed as computed, never recited.

    python3 src/state/status.py            report only (reads state_panel)
    python3 src/state/status.py --load     run every loader first (network for free sources; local files
                                           for licence-restricted ones; stubs report their instructions)
"""
import importlib
import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

# the register's loaders, in the framework's pipeline order (§6 A1-A13 + the market/physical extras)
LOADERS = ["eia_surplus", "eia_nymex", "eia_steo", "eia_intl", "ei_review", "gpr", "kilian",
           "cow_nmc", "cow_mid", "atop", "icb", "ucdp", "archigos", "voeten", "wdi",
           "sipri", "polity", "csp", "vdem", "gsdb", "dots", "nyt"]
OUT = P.DATA / "state" / "status.json"


def run_loaders(conn, names=None):
    res = {}
    for name in names or LOADERS:
        try:
            m = importlib.import_module(name)
        except ImportError as e:
            res[name] = {"status": "missing", "note": str(e)}; continue
        try:
            n = m.load(conn)
            res[name] = {"status": "green", "rows": int(n), "fields": list(getattr(m, "FIELDS", []))}
        except P.MissingInput as e:
            res[name] = {"status": "stub", "note": str(e), "fields": list(getattr(m, "FIELDS", []))}
        except Exception as e:                                       # noqa: BLE001 -- reported, never hidden
            res[name] = {"status": "failed", "note": f"{type(e).__name__}: {str(e)[:300]}", "trace": traceback.format_exc(limit=3)}
    return res


def report(conn, loaders=None):
    cov = P.coverage(conn)
    cb = P.codebook()
    loaded_fields = set(cov["fields"])
    unloaded = sorted(f for f in cb if f not in loaded_fields)
    out = {"generated_at": P.now(), "loaders": loaders or {}, "n_rows": cov["n_rows"], "blocks_by_decade": cov["blocks"],
           "fields": cov["fields"], "fields_registered": len(cb), "fields_loaded": len(loaded_fields), "fields_unloaded": unloaded}
    return out


def print_report(r):
    print(f"state_panel: {r['n_rows']} rows; {r['fields_loaded']} of {r['fields_registered']} registered fields loaded")
    if r["loaders"]:
        g = [k for k, v in r["loaders"].items() if v["status"] == "green"]
        print(f"loaders: {len(g)} green -- {', '.join(g)}")
        for k, v in r["loaders"].items():
            if v["status"] != "green":
                print(f"  {v['status'].upper():7s} {k}: {v.get('note', '')[:160]}")
    print("coverage (rows) per block per decade:")
    decades = sorted({d for b in r["blocks_by_decade"].values() for d in b})
    print("  " + "block".ljust(10) + "".join(d.rjust(8) for d in decades))
    for b, row in r["blocks_by_decade"].items():
        print("  " + b.ljust(10) + "".join(str(row.get(d, 0)).rjust(8) for d in decades))
    print("fields loaded (n rows, entities, first..last, source):")
    for f, v in sorted(r["fields"].items()):
        print(f"  {f:28s} {v['n']:>7d} {v['entities']:>4d}  {v['first']}..{v['last']}  {v['source'][:60]}")
    if r["fields_unloaded"]:
        print(f"registered but not loaded ({len(r['fields_unloaded'])}): {', '.join(r['fields_unloaded'])}")


def main():
    conn = P.connect()
    try:
        loaders = run_loaders(conn) if "--load" in sys.argv else None
        r = report(conn, loaders)
    finally:
        conn.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=1, default=str))
    print_report(r)


if __name__ == "__main__":
    main()
