# CLAUDE.md — Ripple Engine working rules

> **Every turn, read SESSION_CHARTER.md first, then PATH.md.** They override any memory of the task.

You are working inside a research engine with a pre-registered analysis. These rules are non-negotiable.

## What this repo is
An event-study engine measuring how geopolitical shocks ripple through oil prices, conditioned on market state. Canonical docs live one folder up in "News to Markets/": NORTH_STAR.md (vision + current place), CONDITIONED_RIPPLE_ENGINE.md (engine spec), EVENTS_CODEBOOK.md (event coding rules), BRIEF_SKELETON.md (registered analysis plan).

## Scientific integrity rules (highest priority)
1. **Pre-registration is binding.** BRIEF_SKELETON.md declares H1–H3 and a fixed decision rule (+5pp clustered amplification). Do NOT run, print, or summarize the conditioned H1/H2/H3 comparison until ALL THREE state variables (VIX, EIA inventories, COT) are loaded — they run together, once. Do not change windows, splits, or metrics after seeing any result.
2. **Never fabricate data or sources.** Every observation carries source_url + retrieved_at. Every event requires a real, verified source (see codebook). If data can't be fetched, say so — never fill gaps with plausible values.
3. **Point-in-time discipline.** State variables are measured at t−1 before events. No lookahead, ever.
4. **Honest reporting.** Failed hypotheses and null results are reported, not buried.

## Engineering rules
- ONE canonical database: data/oil.db, seven-table generic schema (see src/init_db.py). New data = new rows via small adapters (src/fetch_*.py). NEVER create parallel databases or new tables without explicit approval.
- Derived signals go in src/derive_signals.py with a pre-declared mechanism string. No mechanism, no metric.
- Small, focused scripts; heavy comments (the owner is learning); commit after each working step with a descriptive message.
- The legacy codebase in "News to Markets/" (engine/, newquant/, quant_engine/) is READ-ONLY reference. Do not import from it, extend it, or "fix" it.
- Two servers may be running: src/backend.py (port 5050) and openbb-api (port 6900). Don't kill them; don't bind their ports.
- requirements.txt is the dependency list; pip3 on this machine (Python 3.14, no venv currently).

## Scope discipline
Do exactly what the task brief asks — nothing extra. No speculative features, no refactors beyond the brief, no new frameworks. If something seems to need a bigger change, STOP and report back instead of doing it. Sprawl killed this project's predecessor; brevity of diff is a virtue.

## Owner
Joe is a beginner-turned-operator: explain what you did in plain language after each chunk, and prefer teaching-style commit messages and comments.
