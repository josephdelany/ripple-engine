"""
fetch_cot.py -- CFTC Commitment of Traders: managed-money positioning in WTI.

WHY (this is the H3 data):
The pre-registered hypothesis H3 says shocks land harder when speculative
positioning is crowded. The CFTC publishes, every week, exactly who holds what
in the futures market. "Managed money" = hedge funds / CTAs -- the speculative
crowd. Net long = their longs minus their shorts. When that number sits at an
extreme of its own history, the trade is crowded and fragile.

DATA SOURCE (free, no key):
CFTC "Disaggregated Futures Only" historical files, published as yearly zips at
cftc.gov/files/dea/history/. One combined archive covers 2006-2016, then one
zip per year. We filter to the NYMEX WTI contract (CFTC market code 067651).

Writes one series into the canonical schema:  cftc.mm_net_wti
(managed-money net-long contracts, weekly, Tuesday-dated)

Run:  python3 src/fetch_cot.py        (takes a minute or two; ~20 downloads)
"""

import io
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

BASE = "https://www.cftc.gov/files/dea/history/"
# One combined archive for 2006-2016, then yearly files.
ARCHIVES = ["fut_disagg_txt_hist_2006_2016.zip"] + [
    f"fut_disagg_txt_{y}.zip" for y in range(2017, datetime.now().year + 1)
]

WTI_CODE = "067651"  # CFTC contract market code for NYMEX WTI crude oil

SERIES_ID = "cftc.mm_net_wti"
SERIES_ROW = (
    SERIES_ID, "Managed Money Net Long - WTI (contracts)", "commodity.wti",
    "contracts", "weekly", "CFTC",
    "https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm",
    "H3 conditioning input: crowded speculative positioning is fragile; "
    "extremes of net-long amplify shock transmission via forced unwinds.",
)


def parse_archive(content):
    """Read every .txt inside a COT zip and return WTI rows (date, net_long)."""
    frames = []
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        for name in z.namelist():
            if not name.lower().endswith(".txt"):
                continue
            df = pd.read_csv(z.open(name), low_memory=False)
            df.columns = [c.strip() for c in df.columns]
            # Column names are stable across years in the disaggregated files.
            code_col = "CFTC_Contract_Market_Code"
            date_col = "Report_Date_as_YYYY-MM-DD"
            if code_col not in df.columns or date_col not in df.columns:
                continue
            wti = df[df[code_col].astype(str).str.strip() == WTI_CODE].copy()
            if wti.empty:
                continue
            wti["net"] = (
                pd.to_numeric(wti["M_Money_Positions_Long_All"], errors="coerce")
                - pd.to_numeric(wti["M_Money_Positions_Short_All"], errors="coerce")
            )
            wti["date"] = pd.to_datetime(wti[date_col], errors="coerce")
            frames.append(wti[["date", "net"]].dropna())
    return pd.concat(frames) if frames else pd.DataFrame(columns=["date", "net"])


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    all_frames = []
    for archive in ARCHIVES:
        url = BASE + archive
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            part = parse_archive(r.content)
            print(f"{archive:<38} {len(part):>5} WTI weekly rows")
            all_frames.append(part)
        except Exception as e:
            print(f"{archive:<38} skipped ({type(e).__name__})")

    if not all_frames:
        print("\nNothing downloaded - check your internet connection and try again.")
        return

    data = (
        pd.concat(all_frames)
        .drop_duplicates(subset="date")
        .sort_values("date")
    )
    print(f"\nTotal: {len(data):,} weekly observations, "
          f"{data['date'].min().date()} to {data['date'].max().date()}")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)", SERIES_ROW)
    payload = [
        (SERIES_ID, d.strftime("%Y-%m-%d"), float(v), d.strftime("%Y-%m-%d"), now)
        for d, v in zip(data["date"], data["net"])
    ]
    cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", payload)
    conn.commit()

    total = cur.execute(
        "SELECT COUNT(*) FROM observations WHERE series_id = ?", (SERIES_ID,)
    ).fetchone()[0]
    print(f"Saved {total:,} rows as {SERIES_ID}. "
          f"Next: python3 src/derive_signals.py to compute the percentile signal.")
    conn.close()


if __name__ == "__main__":
    main()
