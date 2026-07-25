# The Watcher — operating guide

The Watcher is a **live-news attention layer**. It reads free news streams (GDELT
2.0 + a small RSS list) and writes the items that hit Joe's net as **alert cards**.

**The one rule:** *the Watcher curates attention, it never concludes.* It codes
nothing and decides nothing. Only Joe promotes an alert into a candidate, and only
Joe turns a candidate into an event. The gate stays a gate.

## Run one cycle (manual — there is no scheduler)
```bash
python3 src/watcher.py            # one polite pass: GDELT latest 15-min file + RSS
python3 src/watcher.py --summary  # same, but prints a one-screen digest of new alerts
```
Each run does a single pass and exits. Alerts are **appended** to
`data/alert_queue.csv` (the Watcher never edits an existing row — the `status`
column is yours). Anything unreachable is printed and skipped; a partial cycle is
fine.

## The net (what it looks for) — both files are yours to edit
- `data/watch_keywords.txt` — one keyword per line (case-insensitive substring).
  Reloaded every cycle.
- `data/watch_feeds.txt` — `<name> <url>` per line. Feeds are verified at build
  time; a dead feed is removed and noted, never left silently broken.
- Plus the `entities` table (countries, chokepoints, commodities, institutions).

## An alert card
`timestamp_utc, source (gdelt|rss:feed), headline, url, matched_entities,
matched_keywords, heuristic_type, amp_context, status`.
- `heuristic_type` is a **labelled guess** at the closest playbook event type from
  keyword mapping — never a coding.
- `amp_context` is today's read line copied verbatim from `engine_read.json`.
- `status` ∈ `new | seen | promoted | dismissed` — **you** set it (edit the CSV).

## Promote an alert into a candidate (the human step)
```bash
python3 src/promote_alert.py           # list the current alerts with numbers
python3 src/promote_alert.py 7         # promote alert #7
```
This appends the alert to `data/candidate_review.csv` with **`joe_decision` BLANK**
and **severity/surprise BLANK**. It is now a candidate awaiting your coding — *not*
an event. To make it an event: code severity/surprise, set `joe_decision=approve`,
then run `apply_review.py` and `load_events.py`. (Optional: mark the alert's
`status=promoted` in `alert_queue.csv`.)

## Dashboard
The `alert_queue` widget in the backend shows the cards newest-first. Restart the
backend to pick it up (Joe's call).

## Where things live (all runtime artifacts, gitignored)
- `data/alert_queue.csv` — the alert cards (append-only).
- `data/watch_seen.db` — a tiny separate SQLite of story hashes, so the same
  story never alerts twice (keeps the canonical `oil.db` clean).

## Bounds (by design, forever)
Free sources only (GDELT + RSS; **no** X/Telegram, **no** scraping article bodies).
No keys, no daemons/cron. Nothing enters `events`, `quiet_events`, or candidate
*approval* without you. No verdicts, no probabilities of events occurring.
