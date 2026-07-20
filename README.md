# Ripple Engine (energy + chokepoint flagship)

Measures how geopolitical shocks ripple through crude-oil prices — an **event study** over decades of daily data. Flagship build for the News-to-Markets project.

## Structure
- `src/fetch_prices.py` — pulls daily Brent & WTI prices from FRED (free, no key), cleans them, saves to a local SQLite database, and charts them.
- `data/` — the SQLite database (`oil.db`) and output charts.

## How to run
```
pip install -r requirements.txt
python3 src/fetch_prices.py
```
Then open `data/oil_prices.png`.

## Roadmap (this repo)
1. ✅ Price data pipeline → SQLite
2. ⬜ Geopolitical event database (energy/chokepoint shocks, hand-curated + sourced)
3. ⬜ Event study — measure the average price ripple around each event type
4. ⬜ Visualize the ripple + write the finding
