# Ops — the synthesis ritual (Mac Pro, on-demand, $0)

GitHub Actions tracks the world for you (data, memory, calibration, phone alerts).
This is the other half: when you sit down to actually *read* a situation, you write
the **"where we stand"** synthesis. It runs on your Mac Pro on your existing Claude
subscription — **no Anthropic API, no per-token cost** — and everything the model
writes passes through the deterministic cage before it's saved.

## When to do it
Whenever you want a fresh narrative read (e.g. after a phone alert, or once a
morning). The deterministic dossier — timeline + priced-state — is always current
from the cloud; this fills in the prose.

## The ritual
```bash
cd "News to Markets/ripple-engine"

# 1. Get the latest cloud-tracked state.
git pull

# 2. Rebuild oil.db locally from the pulled state (from zero; restores memory).
bash repro.sh            # or: python3 src/init_db.py && python3 src/import_state.py && python3 src/refresh.py
```

3. **Synthesize in Claude Desktop** (the MCP server is already installed — see
   `MCP.md`). In a chat:
   > *"Use get_situation for situation.israel_iran_war_2025, then write the
   > 'where we stand' synthesis and the typings as JSON per ops/situation_agent.md."*

   Save the model's JSON to `out.json`.

4. **Run it through the cage** (rejects fabricated numbers / out-of-vocab labels):
```bash
   python3 src/apply_situation_agent.py out.json
   python3 src/situation.py        # re-render the dossier with the synthesis
```

5. **Commit the synthesis + typings** so the cloud (and your phone view) carry it:
```bash
   python3 src/export_state.py
   git add data/state data/situations/*.synthesis.md 2>/dev/null; git commit -m "synth: where we stand"; git push
```

## Rules (the cage enforces these; you don't have to police them)
- The model may only use numbers the engine already computed or that appear in a
  sourced headline — no invented prices/targets.
- It types atoms only from the registered event vocab and the situation's members.
- It never forecasts whether an event will occur, and never touches the human gate.

## Optional: hands-free later
If you'd rather the prose be written unattended, the same contract can run as a
Claude **Cowork** scheduled task (still your subscription, no API). It's cloud, so
it needs the engine's small outputs pushed to it — a later add. On-demand here is
the simplest start and keeps everything local.
