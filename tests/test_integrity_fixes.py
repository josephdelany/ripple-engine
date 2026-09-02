"""2026-09-02 integrity fixes (data/integrity_report.txt): 36 DEAD series traced to four causes.
Each test pins one fix so the cause cannot silently return."""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def test_refresh_schedules_every_series_fetcher():
    """Cause 1: four fetchers that own 25 series were never in refresh.STEPS (hand-run only)."""
    import refresh
    scripts = {s for _, s, _ in refresh.STEPS}
    for f in ("src/fetch_wider_nodes.py", "src/fetch_energy_nodes.py",
              "src/fetch_ovx.py", "src/fetch_wti_monthly.py"):
        assert f in scripts, f"{f} is not scheduled in refresh.STEPS"
    order = [s for _, s, _ in refresh.STEPS]
    assert order.index("src/fetch_wider_nodes.py") < order.index("src/derive_signals.py")


def test_wider_nodes_keeps_hy_spread_live_and_retires_sp500():
    """Cause 2: fred.BAMLH0A0HYM2 was dropped from the fetcher while propagate.py still reads it;
    fred.SP500 was superseded by yf.sp500 and must read retired, not DEAD."""
    import fetch_wider_nodes as w
    assert "fred.BAMLH0A0HYM2" in w.FRED_NODES
    assert "retired 2026-07-30" in w.RETIRED["fred.SP500"]


def test_heartbeat_terminal_markers_read_closed():
    """A dated closed/delisted/retired marker is terminal from that date; 'ends' stays as before."""
    import heartbeat as h
    assert h.terminal_date("outcome=Yes; ends 2026-12-31; delisted 2026-09-02") == date(2026, 9, 2)
    assert h.terminal_date("superseded by yf.sp500; retired 2026-07-30") == date(2026, 7, 30)
    assert h.terminal_date("outcome=Yes; ends 2026-12-31") is None
    assert h.contract_end_date("outcome=Yes; ends 2026-12-31; closed 2026-09-02") == date(2026, 12, 31)


def test_predmkt_reconcile_plan_snapshot_closed_delisted_transient():
    """Cause 3: a tracked market that discovery no longer returns is looked up by slug --
    open -> snapshot, closed -> 'closed' mark, gone -> 'delisted' mark, transport error -> untouched."""
    import fetch_predmkt as p
    open_m = {"slug": "a-open", "active": True, "closed": False, "outcomes": '["Yes","No"]',
              "outcomePrices": '["0.41","0.59"]', "volume": "5000", "endDate": "2026-12-31"}
    responses = {"a-open": open_m, "b-closed": {**open_m, "slug": "b-closed", "closed": True},
                 "c-gone": [], "d-err": None}
    tracked = [(f"predmkt.polymarket.{s}", s, f"outcome=Yes; ends 2026-12-31") for s in
               ("a-open", "b-closed", "c-gone", "d-err", "e-discovered")]
    snaps, marks = p.reconcile_plan(tracked, {"e-discovered"}, lambda s: responses[s], "2026-09-02")
    assert [r["slug"] for r in snaps] == ["a-open"] and snaps[0]["prob"] == 0.41
    assert marks == [("predmkt.polymarket.b-closed", "closed 2026-09-02"),
                     ("predmkt.polymarket.c-gone", "delisted 2026-09-02")]


def test_predmkt_tracked_open_skips_ended_and_marked(tmp_path):
    import sqlite3
    import fetch_predmkt as p
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE series (series_id TEXT PRIMARY KEY, name TEXT, entity_id TEXT, unit TEXT, "
                 "frequency TEXT, source TEXT, source_url TEXT, notes TEXT)")
    rows = [("predmkt.polymarket.live", "ends 2026-12-31"),
            ("predmkt.polymarket.ended", "ends 2026-08-31"),
            ("predmkt.polymarket.marked", "ends 2026-12-31; delisted 2026-09-01"),
            ("fred.DGS10", None)]
    conn.executemany("INSERT INTO series (series_id, notes) VALUES (?,?)", rows)
    assert [s for s, _, _ in p.tracked_open(conn, "2026-09-02")] == ["predmkt.polymarket.live"]


def test_cadence_overrides_monthly_wtisplc_and_eia_spot_lag():
    """Cause 4: the fred.* glob judged the MONTHLY WTISPLC on a daily cadence (60/4 = DEAD with July
    posted); the EIA spots FRED re-publishes carry a ~1wk lag like DGASUSGULF already did."""
    import heartbeat as h
    o = h.load_overrides()
    assert h.override_for("fred.WTISPLC", o) == (30, 20)
    for sid in ("fred.DCOILBRENTEU", "fred.DCOILWTICO", "fred.DHHNGSP", "fred.DHOILNYH"):
        assert h.override_for(sid, o) == (1, 7)
    assert h.override_for("fred.DGS10", o) == (1, 3)     # the glob still governs the rest
