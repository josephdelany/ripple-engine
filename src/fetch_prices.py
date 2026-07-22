"""
fetch_prices.py -- the first brick of the Ripple Engine.

What it does, in plain English:
1. Downloads decades of daily crude-oil prices (Brent and WTI) from FRED,
   the St. Louis Federal Reserve's free public database (no API key needed).
2. Cleans the data (drops days with no price).
3. Saves it into a local SQLite database (a single file: data/oil.db).
4. Draws a chart of both prices over time and saves it as data/oil_prices.png.

Run it with:   python3 src/fetch_prices.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # lets it save a chart without needing a screen
import matplotlib.pyplot as plt
import requests

# --- 1. Where FRED keeps the data (free, no API key needed) ---
# Each "series id" is one dataset. DCOILWTICO = WTI crude, DCOILBRENTEU = Brent crude.
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
SERIES = {"WTI": "DCOILWTICO", "Brent": "DCOILBRENTEU"}
# The canonical series ids the ANALYSIS actually reads (the observations table).
LABEL_TO_SERIES = {"WTI": "fred.DCOILWTICO", "Brent": "fred.DCOILBRENTEU"}

# Folders (data/ holds the database and the chart)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def fetch_one(name, series_id):
    """Download one price series from FRED and return it as a tidy table."""
    url = FRED.format(series=series_id)
    print(f"Downloading {name} ({series_id}) ...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()  # stop loudly if the download failed
    # FRED returns CSV text; read it into a pandas DataFrame (a table).
    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = ["date", "price"]                       # rename the two columns
    df["date"] = pd.to_datetime(df["date"])              # text -> real dates
    df["price"] = pd.to_numeric(df["price"], errors="coerce")  # "." -> missing
    df = df.dropna()                                     # drop days with no price
    df["commodity"] = name                               # label which oil this is
    print(f"  got {len(df):,} days, {df['date'].min().date()} to {df['date'].max().date()}")
    return df


def main():
    # --- 2. Download both series and stack them into one table ---
    frames = [fetch_one(name, sid) for name, sid in SERIES.items()]
    prices = pd.concat(frames, ignore_index=True)

    # --- 3. Save into a local SQLite database (a single file) ---
    db_path = DATA / "oil.db"
    conn = sqlite3.connect(db_path)
    prices.to_sql("prices", conn, if_exists="replace", index=False)

    # --- 3b. Keep the canonical `observations` table current too. THAT table
    # (not `prices`) is what the analysis reads, so the daily refresh must land
    # here or Brent/WTI silently go stale. Key = (series_id, obs_date, as_of);
    # as_of = obs_date to match the original migration, and INSERT OR REPLACE so
    # re-runs update each row in place and never create a duplicate.
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    obs = [
        (LABEL_TO_SERIES[r.commodity], r.date.strftime("%Y-%m-%d"),
         float(r.price), r.date.strftime("%Y-%m-%d"), now)
        for r in prices.itertuples()
    ]
    conn.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", obs)
    conn.commit()
    conn.close()
    print(f"\nSaved {len(prices):,} rows to {db_path} "
          f"(prices table + {len(obs):,} observations rows)")

    # --- 4. Draw a chart of both prices over time ---
    fig, ax = plt.subplots(figsize=(11, 5))
    for name in SERIES:
        sub = prices[prices["commodity"] == name]
        ax.plot(sub["date"], sub["price"], label=name, linewidth=0.8)
    ax.set_title("Crude Oil Prices (Brent vs WTI) - daily, from FRED")
    ax.set_ylabel("US$ per barrel")
    ax.legend()
    ax.grid(alpha=0.3)
    out = DATA / "oil_prices.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"Saved chart to {out}")


if __name__ == "__main__":
    main()
