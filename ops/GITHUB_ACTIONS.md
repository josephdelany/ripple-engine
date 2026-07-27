# Ops — run the engine free on GitHub Actions

This makes the engine track, score, and **notify you** every day without any
computer of yours staying on. GitHub runs it in the cloud on a schedule, for free.
The LLM synthesis is NOT here — that stays on your Mac Pro (see `SYNTHESIZE.md`).

## What the workflow does (`.github/workflows/track.yml`)
Every day at 11:00 UTC (and on-demand from the Actions tab) GitHub:
1. rebuilds `oil.db` from the free sources (FRED, EIA, CFTC, GDELT, GPR, RSS),
2. restores the durable memory from the committed CSVs (`import_state.py`),
3. runs the live cycle (`refresh.py`: derive → engine read → watcher → situation
   memory → resolve reads → dashboard),
4. snapshots the memory back (`export_state.py`),
5. pushes any **high-signal + market-primed** alert to your phone (`notify.py` → ntfy),
6. commits the refreshed state and uploads The Daily (`digest.html`) as an artifact.

Nothing here uses a paid API. Cost: **$0** (free Actions minutes, free ntfy).

## One-time setup (you do this once, in the browser)

### 1. Push the repo to GitHub (private is fine)
```bash
# from the repo root, if it isn't on GitHub yet:
gh repo create ripple-engine --private --source=. --push
```

### 2. Add two secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**:
- **`EIA_API_KEY`** — your free EIA key (same one in `~/.openbb_platform/user_settings.json`).
  Without it the weekly-inventory (H2) series just goes stale; everything else still runs.
- **`NTFY_TOPIC`** — a hard-to-guess topic name you invent, e.g. `ripple-joe-8f3k`.
  (Optional: leave it unset and no phone pushes are sent — the run still works.)

### 3. Get the notifications on your phone
Install the **ntfy** app (iOS/Android), and **subscribe to the exact same topic**
you put in `NTFY_TOPIC`. That's it — anyone who knows the topic can post to it, so
keep the name private.

### 4. Enable + test
- Actions are on by default for the repo owner. Open the **Actions** tab → **track**
  → **Run workflow** to fire it once immediately (don't wait for 11:00 UTC).
- Check it goes green; the run commits a `chore(track): daily state …` commit and
  attaches `the-daily` (the dashboard HTML) as an artifact you can download.

## Viewing the dashboard
- **Simplest:** download the `the-daily` artifact from any run and open `digest.html`.
- **Optional (view from anywhere):** enable **GitHub Pages** and publish `digest.html`
  — a small add we can wire later; the artifact path is enough to start.

## Notes / gotchas
- Scheduled runs are **best-effort** (GitHub may delay them under load) and are
  **auto-disabled after 60 days of no repo activity** — any commit re-arms them.
- The big `oil.db` is never committed; only the small state CSVs +
  `alert_queue.csv` + `watch_seen.db` are. That's by design (see `import_state.py`).
- If `main` is branch-protected, allow the Actions bot to push, or point the commit
  step at a branch.
