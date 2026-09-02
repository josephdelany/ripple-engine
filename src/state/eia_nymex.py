"""eia_nymex.py -- WS-M05 curve_m1_m4_spread: EIA NYMEX crude futures contracts 1-4 (RCLC1..RCLC4), daily.

Source (register §3): https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm -- the four hist_xls files. Public
domain, keyless. The series END 2024-04-05 (EIA: "futures prices after April 5, 2024, are not available");
the post-2024 curve is a different field/source (WS-M06, never spliced: WS-R5).
Value = contract 1 minus contract 4 in $/bbl: positive = backwardation, negative = contango.
A daily print is knowable on its date (vintage = obs_date); release = the files' HTTP Last-Modified.
Note: the RCLC1 file's first observation is 1983-04-04 (PATH.md cites 1983-03-30; the file is the record).

Run:  python3 src/state/eia_nymex.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

SOURCE = "EIA NYMEX futures contracts 1-4 (RCLC1..RCLC4 daily, ends 2024-04-05)"
BASE = "https://www.eia.gov/dnav/pet/hist_xls/{sid}d.xls"
CONTRACTS = ["RCLC1", "RCLC2", "RCLC3", "RCLC4"]
RELEASE_FALLBACK = "2024-04-08"          # the first weekday after the series' last print
FIELDS = ["curve_m1_m4_spread"]


def fetch(force=False):
    out = {}
    for sid in CONTRACTS:
        out[sid] = P.fetch_file(BASE.format(sid=sid), P.raw_path("eia_nymex", f"{sid}d.xls"), force=force)
    return out


def read_contract(path):
    """The 'Data 1' sheet: a 'Date' header row then (date, price). Returns a Series indexed by date."""
    if str(path).endswith(".csv"):                                   # a sliced fixture of the same two columns
        d = pd.read_csv(path, header=None)
    else:
        d = pd.read_excel(path, sheet_name="Data 1", header=None)
    hdr = d.index[d.iloc[:, 0].astype(str).str.strip() == "Date"]
    if len(hdr) == 0:
        raise ValueError(f"{path}: no 'Date' header row in 'Data 1' -- layout changed; STOP")
    body = d.iloc[hdr[0] + 1:, :2].dropna()
    s = pd.Series(pd.to_numeric(body.iloc[:, 1], errors="coerce").values, index=pd.to_datetime(body.iloc[:, 0]))
    return s.dropna()


def parse(paths, release):
    """paths: {sid: path}. Spread rows on every date where both contract 1 and 4 print."""
    c1, c4 = read_contract(paths["RCLC1"]), read_contract(paths["RCLC4"])
    both = pd.concat([c1.rename("m1"), c4.rename("m4")], axis=1).dropna()
    return [{"entity_id": "world", "field": "curve_m1_m4_spread", "obs_date": d.date().isoformat(),
             "value": round(float(r.m1 - r.m4), 4), "unit": "USD/bbl", "source": SOURCE,
             "vintage": d.date().isoformat(), "release": release}
            for d, r in both.iterrows()]


def load(conn=None, force=False):
    got = fetch(force)
    paths = {sid: p for sid, (p, _m) in got.items()}
    release = P.vintage_from(got["RCLC1"][1], RELEASE_FALLBACK)
    rows = parse(paths, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("eia_nymex", n, FIELDS, f"release {release}; a daily print is knowable on its date; first {rows[0]['obs_date']} last {rows[-1]['obs_date']}")
    return n


if __name__ == "__main__":
    load()
