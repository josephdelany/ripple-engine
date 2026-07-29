"""
story.py -- the STORIES layer (thin first version).

A "story" is a human-curated, self-updating view onto signals the engine already tracks
(data/stories/<id>.yaml). This assembles a story's LIVE STATE from those signals, detects
MATERIAL CHANGES since the last run (the phone-ping trigger), and writes a plain read.

This is the disciplined MVP from STORIES_HUB_PLAN.md: a story is a view + a change-detector,
NOT (yet) the full gap/hypothesis/Brier machinery -- that follows the roadmap. Deterministic
assembly; the thesis prose is human-curated in the yaml (no LLM in the loop, no fabrication).

First story: opec_fiscal_stress (IMF breakeven vs live Brent).
Run:  python3 src/story.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STORIES = ROOT / "data" / "stories"
BREAKEVENS = ROOT / "data" / "breakevens.json"

# severity order so we can tell when a producer's stress WORSENS.
SEVERITY = {"comfortable": 0, "balanced": 1, "stress": 2, "acute stress": 3, "n/a": -1}


def worsened(prev_band, new_band):
    """Did the stress band get worse? Pure -- unit-tested."""
    return SEVERITY.get(new_band, -1) > SEVERITY.get(prev_band, -1)


def detect_changes(prev_board, new_board):
    """Material changes vs last run: a producer whose stress worsened, or Brent crossing a
    producer's breakeven (gap sign flip). These are the things worth a notification."""
    prev = {r["country"]: r for r in prev_board}
    changes = []
    for r in new_board:
        p = prev.get(r["country"])
        if not p:
            continue
        if worsened(p.get("band"), r.get("band")):
            changes.append(f"{r['country']}: stress worsened {p.get('band')} -> {r.get('band')}")
        pg, ng = p.get("gap"), r.get("gap")
        if pg is not None and ng is not None and (pg >= 0) != (ng >= 0):
            direction = "fell below" if ng < 0 else "rose above"
            changes.append(f"{r['country']}: Brent {direction} its breakeven (gap {pg:+.1f} -> {ng:+.1f})")
    return changes


def nearest_watch(watch_dates, today):
    """The next upcoming watch date (event + days away), or None."""
    upcoming = [w for w in (watch_dates or []) if w.get("date", "") >= today]
    if not upcoming:
        return None
    w = min(upcoming, key=lambda w: w["date"])
    days = (datetime.fromisoformat(w["date"]).date() - datetime.fromisoformat(today).date()).days
    return {"date": w["date"], "event": w.get("event", ""), "days_away": days}


def assemble(story_id="opec_fiscal_stress"):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    today = now[:10]
    cfg = yaml.safe_load((STORIES / f"{story_id}.yaml").read_text())
    be = json.loads(BREAKEVENS.read_text()) if BREAKEVENS.exists() else {}
    board = be.get("producers", [])
    brent = be.get("brent")
    n_under = sum(1 for r in board if r.get("gap") is not None and r["gap"] < 0)

    state_path = STORIES / f"{story_id}.state.json"
    prev = json.loads(state_path.read_text()) if state_path.exists() else {}
    changes = detect_changes(prev.get("board", []), board)
    whats_next = nearest_watch(cfg.get("watch_dates"), today)

    most = board[0] if board else {}
    read = (f"{cfg['title']}. {' '.join(cfg['thesis'].split())} "
            f"Now: {n_under}/{len(board)} producers underwater at Brent ${brent}. "
            f"Most stressed: {most.get('country','?')} (gap {most.get('gap','?')}).")
    if whats_next:
        read += f" Next catalyst: {whats_next['event']} in {whats_next['days_away']}d ({whats_next['date']})."

    state = {"story_id": story_id, "title": cfg["title"], "as_of": today, "generated_at": now,
             "brent": brent, "n_underwater": n_under, "board": board,
             "whats_next": whats_next, "watch_gauges": cfg.get("watch_gauges", []),
             "changes": changes, "read": read}
    state_path.write_text(json.dumps(state, indent=2))
    return state


def main():
    s = assemble()
    print(f"story[{s['story_id']}] -- {s['n_underwater']}/{len(s['board'])} underwater "
          f"@ Brent ${s['brent']}. Most stressed: {s['board'][0]['country'] if s['board'] else '?'}.")
    if s["changes"]:
        print("  CHANGES (would ping):")
        for c in s["changes"]:
            print(f"    - {c}")
    else:
        print("  no material change since last run.")
    if s["whats_next"]:
        print(f"  next: {s['whats_next']['event']} ({s['whats_next']['days_away']}d)")


if __name__ == "__main__":
    main()
