"""
apply_situation_agent.py -- the CAGE around the synthesizer agent (Slice 3b).

The scoped research agent (a Cowork worker, or Claude in-chat) does the one thing
an LLM is allowed to do here: EXTRACTION + SYNTHESIS PROSE. It reads a situation's
sourced atoms and returns a small JSON object:

    {
      "situation_id": "situation.israel_iran_war_2025",
      "typings":  [ {"source_url": "...", "kind": "chokepoint_disruption",
                     "actor_entity": "country.yemen"}, ... ],
      "synthesis": "Where we stand ... (prose, tagged inferred)",
      "gaps":      ["did Saudi flow resume?", ...]        # optional
    }

This file is the deterministic gate that decides whether that output is allowed in.
It NEVER runs an LLM and NEVER does analysis. It enforces, hard:
  * kind must be a REGISTERED event type (closed vocab) or 'unmapped';
  * actor_entity must be a MEMBER of the situation (closed vocab) or null;
  * every typing must target a real atom (source_url) of that situation;
  * the synthesis may introduce NO number that isn't already engine-computed
    (in the priced-state block) or present in a sourced atom headline -- so the
    agent literally cannot fabricate a figure;
  * typing refines the deterministic `kind` hint (status stays 'observed');
    the prose is written to a SEPARATE file tagged inferred -- observed and
    inferred are never blended in one atom.
Anything that fails is rejected wholesale with reasons; nothing partial is written.
Promotion into coded events remains the untouched human gate.

Run:  python3 src/apply_situation_agent.py <agent_output.json>
      python3 src/apply_situation_agent.py -           # read JSON from stdin
"""

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import situation  # noqa: E402  (deterministic helpers: paths, render, config)
from load_events import VALID_TYPES  # noqa: E402  (the registered event vocab)

ALLOWED_KINDS = set(VALID_TYPES) | {"unmapped"}
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _numbers(text):
    """Normalised numeric tokens in a string (sign stripped): '-7.5' -> '7.5'."""
    return {m.group().lstrip("-") for m in _NUM.finditer(text or "")}


def allowed_numbers(conn, sid, priced_md):
    """The ONLY numbers the synthesis may use: those the engine already computed
    (the priced-state block) or that appear in a sourced atom headline, plus plain
    calendar years. A number outside this set is a fabrication -> rejected."""
    allowed = set(_numbers(priced_md))
    for (headline,) in conn.execute(
            "SELECT headline FROM situation_log WHERE situation_id=?", (sid,)):
        allowed |= _numbers(headline)
    allowed |= {str(y) for y in range(1990, 2036)}   # years are always fine
    return allowed


def validate(agent_out, conn):
    """Return (errors, situation_dict). Empty errors == the output is clean."""
    errors = []
    sid = agent_out.get("situation_id")
    sit = next((s for s in situation.load_situations()
                if s["situation_id"] == sid), None)
    if sit is None:
        return [f"unknown situation_id '{sid}'"], None

    members = set(sit.get("member_entities", []))
    known_urls = {u for (u,) in conn.execute(
        "SELECT source_url FROM situation_log WHERE situation_id=?", (sid,))}

    for t in agent_out.get("typings", []):
        if t.get("kind") not in ALLOWED_KINDS:
            errors.append(f"kind '{t.get('kind')}' is not a registered event type")
        ae = t.get("actor_entity")
        if ae and ae not in members:
            errors.append(f"actor_entity '{ae}' is not a member of {sid}")
        if t.get("source_url") not in known_urls:
            errors.append(f"typing targets '{t.get('source_url')}', which is not "
                          f"an atom of {sid}")

    syn = (agent_out.get("synthesis") or "").strip()
    if not syn:
        errors.append("synthesis is empty")
    # include_markets=False: the fabrication guard's allowed-number set must be the
    # engine's stable computed numbers, not the volatile prediction-market board.
    priced = situation._priced_state_md(conn, sit, situation.load_engine_read(),
                                        include_markets=False)
    allowed = allowed_numbers(conn, sid, priced)
    bad = sorted(n for n in _numbers(syn) if n not in allowed)
    if bad:
        errors.append("synthesis introduces numbers not engine-computed and not in "
                      f"any sourced headline (fabrication guard): {bad}")
    return errors, sit


def apply(agent_out, conn):
    """Validate, then -- only if clean -- write the typings + the inferred
    synthesis file. Returns a result dict; writes nothing on any error."""
    errors, sit = validate(agent_out, conn)
    if errors:
        return {"applied": False, "errors": errors}

    sid = agent_out["situation_id"]
    # 1. Typings refine the deterministic `kind` hint + set actor. status stays
    #    'observed' -- typing is classification, not inference.
    for t in agent_out.get("typings", []):
        conn.execute(
            "UPDATE situation_log SET kind=?, actor_entity=? WHERE "
            "situation_id=? AND source_url=?",
            (t["kind"], t.get("actor_entity"), sid, t["source_url"]))
    conn.commit()

    # 2. The prose goes to a SEPARATE file, tagged inferred (never blended into an
    #    observed atom). render_dossier injects it in place of the pending stub.
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    situation.DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
    path = situation.DOSSIER_DIR / f"{sid}.synthesis.md"
    body = agent_out["synthesis"].strip()
    gaps = agent_out.get("gaps", [])
    if gaps:
        body += ("\n\n**Open questions (gaps to research):**\n"
                 + "\n".join(f"- {g}" for g in gaps))
    header = (f"<!-- status=inferred agent-authored generated={now} -->\n"
              f"_Synthesis — **inferred**, agent-authored ({now[:10]}). Uses only "
              f"engine-computed or sourced numbers._\n\n")
    path.write_text(header + body + "\n")
    return {"applied": True, "typings_applied": len(agent_out.get("typings", [])),
            "synthesis_chars": len(body), "gaps": len(gaps),
            "wrote": str(path.relative_to(situation.ROOT))}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    raw = sys.stdin.read() if sys.argv[1] == "-" else Path(sys.argv[1]).read_text()
    agent_out = json.loads(raw)
    conn = sqlite3.connect(situation.DB)
    result = apply(agent_out, conn)
    conn.close()
    print(json.dumps(result, indent=2))
    if not result.get("applied"):
        sys.exit(1)          # rejected -> non-zero so a caller notices


if __name__ == "__main__":
    main()
