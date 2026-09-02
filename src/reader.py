"""reader.py -- the reading layer: a CAGED LLM extractor (CLAIM_LEDGER_REGISTRATION.md, Amendment 3).

Replaces the regex layer (triage.classify_type / deconstruct.claims) on the v2 surfaces. Same
pattern as extract_events.py and apply_situation_agent.py: the model PROPOSES, deterministic
Python DECIDES what is allowed in, and nothing partial is repaired.

  input   a URL or pasted text (read_story), or a batch of headlines (read_headlines)
  output  title, event_class, entities with roles, claims typed per registration §2 -- each item
          validated by the cage; rejected items are listed with the reason, never silently dropped

The model is Claude through the local `claude` CLI on Joe's subscription (no API key, $0
marginal), run headless with NO tools and a fixed JSON schema (ops/reader_agent.md). Model
proposals are cached by content hash (data/reader/cache) so a story is read once. If the CLI is
unavailable the read falls back to the regex layer and every surface says `regex_fallback`.

Run:  python3 src/reader.py "<text or url>"          one story, printed
      python3 src/reader.py --headlines "a" "b" ...    a batch of headlines
"""
import hashlib
import html as _html
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
CACHE = DATA / "reader" / "cache"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_events import VALID_TYPES          # noqa: E402  the registered event vocabulary
import ledger as L                           # noqa: E402  asset -> series map, horizons, regex fallback typing

REGISTRATION = "CLAIM_LEDGER_REGISTRATION.md §2 + Amendment 3"
MODEL = os.environ.get("RIPPLE_READER_MODEL", "sonnet")
def _mode():
    return os.environ.get("RIPPLE_READER", "auto")     # auto | off  (off = regex fallback only; the test suite)
TIMEOUT_S = int(os.environ.get("RIPPLE_READER_TIMEOUT", "150"))
MAX_TEXT = 8000
MAX_CLAIMS = 12
BATCH = 40

KINDS = {"direction", "level", "flow", "escalation", "policy", "uncheckable"}
ROLES = {"actor", "target", "asset", "chokepoint", "location", "affected_market", "mention"}
GATE_ROLES = {"actor", "target", "asset", "chokepoint"}          # Amendment 3 rule 5
DIRECTIONS = {"up", "down", "disrupt", "resume", "escalate"}
MODALITIES = {"asserted", "hypothetical", "negated"}
ASSET_SERIES = {key: sid for key, _pat, sid in L.ASSET}          # brent, diesel_crack, gas, fertilizer, freight
ASSETS = set(ASSET_SERIES)
PETRO_TYPES = {"country", "chokepoint", "supplychain"}
PETRO_COMMODITIES = {"commodity." + c for c in ("brent", "wti", "crude_oil", "diesel", "gasoline", "gasoline_spot",
                                                 "natgas", "eu_gas", "lng_asia", "propane", "fertilizer", "petchem")}
PETRO_INSTITUTIONS = {"institution." + i for i in ("opec", "iea", "us_doe", "isprl", "china_reserve_bureau")}
TYPE_MEANING = {
    "chokepoint_disruption": "transit through a strait/canal/pipeline is threatened or blocked",
    "opec_decision": "OPEC/OPEC+ production decision or collapse of talks",
    "sanctions": "sanctions imposed, tightened, or lifted on a producer",
    "conflict_escalation": "war, invasion, major military escalation involving a producer/transit state",
    "infrastructure_attack": "direct strike on production, refining, or export infrastructure",
    "demand_shock": "a macro/health/policy event that abruptly changes demand",
    "policy_response": "deliberate government/agency market intervention (SPR/IEA releases, price controls)",
}
GENERIC_TITLES = {"press releases", "press release", "news", "home", "article", "untitled"}
_NUM = re.compile(r"-?\d+(?:[.,]\d+)*")
_BOILER = ("subscribe", "advertise", "cookie", "sign in", "newsletter", "all rights reserved",
           "read more", "follow us", "share this", "getty images")


# ----------------------------------------------------------------------------- text helpers

def _canon(s):
    """Whitespace- and quote-mark-normalised text for the verbatim check (Amendment 3 rule 3)."""
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def _numbers(s):
    """Numeric tokens in a string, normalised ('1,000' -> '1000', '110.0' -> '110')."""
    out = set()
    for m in _NUM.finditer(s or ""):
        tok = m.group().lstrip("-").replace(",", "")
        try:
            f = float(tok)
            out.add(str(int(f)) if f == int(f) else str(f))
        except ValueError:
            continue
    return out


def _strip_tags(s):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def _sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", text or "")
    return [s.strip() for s in parts if 28 <= len(s.strip()) <= 400]


# ----------------------------------------------------------------------------- fetch + parse

def fetch(url, timeout=20):
    import requests
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (ripple-engine research)"})
    r.raise_for_status()
    return r.text


def body_from_html(raw):
    """Prose paragraphs of an article page (nav/boilerplate filtered). Deterministic."""
    m = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S | re.I)
    scope = m.group(1) if m else raw
    scope = re.sub(r"<(script|style|nav|aside|footer|header|form|figure)[^>]*>.*?</\1>", " ", scope, flags=re.S | re.I)
    paras = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", scope, re.S | re.I):
        t = _strip_tags(p)
        if len(t) >= 50 and any(ch in t for ch in ".?!") and not any(b in t.lower() for b in _BOILER):
            paras.append(t)
    return " ".join(paras)[:MAX_TEXT]


def title_from_html(raw, url, body=""):
    """The page's OWN title (Amendment 3 rule 4): first heading inside <article>, then og:title /
    twitter:title, then <h1>, then <title>; generic and code-polluted candidates skipped; a trailing
    ' - Site name' suffix removed. Falls back to the first sentence of the body. Never generated."""
    cands = []
    art = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S | re.I)
    if art:
        cands += re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", art.group(1), re.S | re.I)[:2]
    for pat in (r'property=["\']og:title["\'][^>]*content=["\']([^"\']+)',
                r'content=["\']([^"\']+)["\'][^>]*property=["\']og:title["\']',
                r'name=["\']twitter:title["\'][^>]*content=["\']([^"\']+)'):
        m = re.search(pat, raw, re.I)
        if m:
            cands.append(m.group(1))
    cands += re.findall(r"<h1[^>]*>(.*?)</h1>", raw, re.S | re.I)[:3]
    t = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    if t:
        cands.append(t.group(1))
    sn = re.search(r'property=["\']og:site_name["\'][^>]*content=["\']([^"\']+)', raw, re.I)
    site_name = _strip_tags(sn.group(1)).lower() if sn else ""
    host = (urlparse(url).netloc if url else "").replace("www.", "").lower()
    for c in cands:
        c = _strip_tags(c)
        if not (12 <= len(c) <= 220) or len(c.split()) < 3:
            continue
        if re.search(r"[<>{}=;]|\+=|function\(", c):
            continue
        low = c.lower()
        if low in GENERIC_TITLES or (site_name and low == site_name):
            continue
        parts = re.split(r"\s+[-|–—]\s+", c)
        if len(parts) > 1 and re.sub(r"\W", "", parts[-1].lower()) in host.replace(".", ""):
            c = " - ".join(parts[:-1]).strip()
        return c
    first = _sentences(body)
    return (first[0] if first else (body or "")[:160])[:160]


def prepare(arg):
    """(url, title, text, fetched, error). A URL is fetched and parsed; text is used as-is with its
    first sentence as the title."""
    a = (arg or "").strip()
    if re.match(r"^https?://\S+$", a):
        try:
            raw = fetch(a)
        except Exception as e:                                   # noqa: BLE001 -- the failure is reported, not hidden
            return {"url": a, "title": a, "text": a, "fetched": False, "error": f"fetch failed: {e}"}
        body = body_from_html(raw)
        title = title_from_html(raw, a, body)
        if len(body) < 120:
            body = title                                       # headline-only page: read the title
        return {"url": a, "title": title, "text": body, "fetched": True, "error": None}
    first = _sentences(a)
    return {"url": None, "title": (first[0] if first else a)[:160], "text": a[:MAX_TEXT], "fetched": False, "error": None}


# ----------------------------------------------------------------------------- vocabulary

_vocab = {"mtime": None, "data": None}


def vocab(conn=None):
    """{entity_id: name} from the entities table (closed list). Cached on the DB mtime."""
    try:
        m = DB.stat().st_mtime
    except OSError:
        return {}
    if _vocab["mtime"] != m or _vocab["data"] is None:
        own = conn is None
        conn = conn or sqlite3.connect(DB)
        try:
            _vocab.update(mtime=m, data={eid: name for eid, name in conn.execute("SELECT entity_id, name FROM entities")})
        finally:
            if own:
                conn.close()
    return _vocab["data"]


def is_petro(entity_id):
    t = entity_id.split(".", 1)[0]
    return t in PETRO_TYPES or entity_id in PETRO_COMMODITIES or entity_id in PETRO_INSTITUTIONS


def qualifying_entities(entities, mode="llm"):
    """Entity ids that satisfy Amendment 3 rule 5: tracked petro entity in a gate role. Under the
    regex fallback roles are unknown ('mention'), so Amendment 2's presence rule applies, labelled."""
    out = []
    for e in entities or []:
        if not is_petro(e["id"]):
            continue
        if mode == "regex_fallback" or e.get("role") in GATE_ROLES:
            out.append(e["id"])
    return sorted(set(out))


# ----------------------------------------------------------------------------- the model call

STORY_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "event_class": {"type": ["string", "null"]},
        "event_date": {"type": ["string", "null"]},
        "confidence": {"type": ["string", "null"]},
        "entities": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                "properties": {"id": {"type": "string"}, "role": {"type": "string"}},
                                                "required": ["id", "role"]}},
        "unmapped": {"type": "array", "items": {"type": "string"}},
        "claims": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                              "properties": {"quote": {"type": "string"}, "kind": {"type": "string"},
                                                             "asset": {"type": ["string", "null"]},
                                                             "direction": {"type": ["string", "null"]},
                                                             "level": {"type": ["number", "null"]},
                                                             "horizon_days": {"type": ["integer", "null"]},
                                                             "modality": {"type": "string"}},
                                              "required": ["quote", "kind", "asset", "direction", "level", "horizon_days", "modality"]}},
    },
    "required": ["event_class", "event_date", "confidence", "entities", "unmapped", "claims"],
}
BATCH_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {"i": {"type": "integer"}, "event_class": {"type": ["string", "null"]},
                       "event_date": {"type": ["string", "null"]}, "confidence": {"type": ["string", "null"]},
                       "entities": STORY_SCHEMA["properties"]["entities"],
                       "claim": {"anyOf": [STORY_SCHEMA["properties"]["claims"]["items"], {"type": "null"}]}},
        "required": ["i", "event_class", "event_date", "confidence", "entities", "claim"]}}},
    "required": ["items"],
}


def system_prompt(voc):
    types = "\n".join(f"  - {t}: {TYPE_MEANING[t]}" for t in sorted(VALID_TYPES))
    ents = "; ".join(f"{eid} ({name})" for eid, name in sorted(voc.items()))
    return f"""You are the READER for a research engine that measures how oil-market developments ripple through prices. You do the one thing a model is allowed to do here: EXTRACTION. You never score, judge, forecast, or paraphrase. A deterministic validator rejects anything outside these rules.

EVENT CLASS -- the story's dominant development, a cause not a price move. Exactly one of:
{types}
Use null when the story is not a discrete development of one of these kinds (price recaps, earnings, commentary, unrelated news). Never invent a class.
EVENT_DATE -- the date the development happened, ISO YYYY-MM-DD, ONLY if the text states it (a dateline, "on 14 May", "Tuesday" with a stated week); otherwise null. Never today's date, never a guess.
CONFIDENCE -- your confidence in the event class: high | medium | low. (Amendment 6: extracted, never scored.)

ENTITIES -- only ids from this closed list, each with one role: actor (did it), target (it was done to), asset (the physical asset or commodity at stake), chokepoint (the strait/canal/pipeline at stake), location, affected_market, mention (named but not central). List a name that is central but not in the list under "unmapped" as plain text.
Closed list: {ents}

CLAIMS -- the story's checkable claims, EXTRACTIVE and VERBATIM: each quote must be copied exactly from the text (a full sentence or a clause). Never paraphrase, never merge sentences. At most {MAX_CLAIMS}. Each has:
  kind: direction (price goes up/down) | level (price reaches a stated number) | flow (barrels, cargoes, transits stop, halt, reroute or resume) | escalation (retaliation, widening, closure between named actors) | policy (OPEC/SPR/government action) | uncheckable (opinion, description, no asset+direction)
  asset: brent (crude oil, Brent, WTI, barrels) | diesel_crack (diesel, distillate, jet fuel, refining margins) | gas (LNG, natural gas, TTF, JKM, Henry Hub) | fertilizer (urea, ammonia) | freight (tanker rates, shipping rates, insurance) | null
  direction: up | down (price claims) | disrupt | resume (flow claims) | escalate (escalation) | null
  level: the price level stated IN THE QUOTE as a number, else null. Never introduce a number that is not in the quote.
  horizon_days: only if the quote itself states a horizon in days/weeks/months (convert to days); else null. The validator assigns registered defaults.
  modality: asserted | hypothetical (could, may, if, would) | negated (the text says it did NOT happen)
Prefer claims about prices, flows, and escalation. Include at most 3 uncheckable claims and only if they are central.

Reply with JSON matching the schema and nothing else."""


def _cli():
    return shutil.which("claude") if _mode() != "off" else None


def _call(system, user, schema, model=None, timeout=None):
    """One headless call: no tools, fixed schema, session not persisted. Returns (obj|None, meta)."""
    meta = {"mode": "llm", "model": model or MODEL, "secs": None, "error": None}
    cli = _cli()
    if not cli:
        meta.update(mode="regex_fallback", error="claude CLI unavailable" if _mode() != "off" else "reader off (RIPPLE_READER=off)")
        return None, meta
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    t0 = time.perf_counter()
    try:
        r = subprocess.run([cli, "-p", "--no-session-persistence", "--tools", "", "--model", meta["model"],
                            "--system-prompt", system, "--output-format", "json", "--json-schema", json.dumps(schema), user],
                           capture_output=True, text=True, timeout=timeout or TIMEOUT_S, env=env, cwd=tempfile.gettempdir())
        meta["secs"] = round(time.perf_counter() - t0, 1)
        d = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {}
        obj = d.get("structured_output")
        if obj is None and d.get("result"):
            try:
                obj = json.loads(d["result"])
            except ValueError:
                obj = None
        if d.get("is_error") or obj is None:
            meta.update(mode="regex_fallback", error=(d.get("result") or r.stderr or "no structured output")[:200])
            return None, meta
        return obj, meta
    except subprocess.TimeoutExpired:
        meta.update(mode="regex_fallback", error=f"timeout after {timeout or TIMEOUT_S}s", secs=round(time.perf_counter() - t0, 1))
        return None, meta
    except (OSError, ValueError) as e:
        meta.update(mode="regex_fallback", error=str(e)[:200])
        return None, meta


def _cache_key(kind, text, model=None):
    return hashlib.sha1(f"{model or MODEL}|{kind}|{_canon(text)}".encode("utf-8", "replace")).hexdigest()


def _cache_get(key):
    p = CACHE / f"{key}.json"
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def _cache_put(key, proposal, meta):
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / f"{key}.json").write_text(json.dumps({"proposal": proposal, "model": meta.get("model"),
                                                    "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}, ensure_ascii=False))


# ----------------------------------------------------------------------------- the cage

def cage_claim(c, text, has_actor):
    """Validate one proposed claim against the text and the registration. Returns (claim|None, reason).
    The cage downgrades (to uncheckable) and rejects (fabrication); it never upgrades or repairs."""
    q = _canon(c.get("quote") if isinstance(c, dict) else "")
    if len(q) < 12:
        return None, "empty or too-short quote"
    if q not in _canon(text):
        return None, "quote not in the text (fabrication guard)"
    kind = c.get("kind")
    if kind not in KINDS:
        return None, f"kind '{kind}' not registered"
    why = []
    asset = c.get("asset") if c.get("asset") in ASSETS else None
    if c.get("asset") and asset is None:
        why.append(f"asset '{c.get('asset')}' not in the asset list")
    direction = c.get("direction") if c.get("direction") in DIRECTIONS else None
    modality = c.get("modality") if c.get("modality") in MODALITIES else "asserted"
    level = None
    if c.get("level") is not None:
        try:
            lv = float(c["level"])
            tok = str(int(lv)) if lv == int(lv) else str(lv)
            if tok in _numbers(q):
                level = lv
            else:
                why.append(f"level {c['level']} is not stated in the quote (fabrication guard)")
        except (TypeError, ValueError):
            why.append("level is not a number")
    horizon = None
    if c.get("horizon_days") is not None:
        try:
            h = int(c["horizon_days"])
            if str(h) in _numbers(q):
                horizon = h
        except (TypeError, ValueError):
            pass
    if kind != "level":
        level = None                                           # a number on a non-level claim carries no meaning here
    out = {"kind": kind, "asset": asset, "series": ASSET_SERIES.get(asset), "direction": direction, "level": level,
           "modality": modality, "text": q, "quote": q}
    if modality == "negated" and kind != "uncheckable":
        why.append("negated in the text (non-event): no read")
        kind = "uncheckable"
    if kind == "direction":
        if not (asset and direction in ("up", "down")):
            why.append("direction claim without asset + up/down"); kind = "uncheckable"
    elif kind == "level":
        if not (asset and level is not None):
            why.append("level claim without asset + stated level"); kind = "uncheckable"
        elif direction not in ("up", "down"):
            direction = None                                   # ledger.verdict_for sets it from the price at knowability
    elif kind == "flow":
        asset = asset or "brent"
        direction = direction if direction in ("disrupt", "resume") else "disrupt"
        out.update(asset=asset, series=ASSET_SERIES.get(asset) or ASSET_SERIES["brent"])
    elif kind == "escalation":
        if not has_actor:
            why.append("escalation claim with no actor/target entity in the story"); kind = "uncheckable"
        else:
            out.update(asset="escalation", series=None); direction = "escalate"
    if kind in ("direction", "level", "flow"):
        out.update(horizon_days=horizon or L.PRICE_HORIZON_TD, horizon_unit="trading", checkable=bool(out["series"] or ASSET_SERIES.get(asset)))
        if not out["checkable"]:
            why.append(f"asset '{asset}' has no series yet")
    elif kind == "escalation":
        out.update(horizon_days=horizon or L.ESCALATION_HORIZON_CD, horizon_unit="calendar", checkable=True)
    elif kind == "policy":
        out.update(asset="policy", series=None, horizon_days=horizon or L.ESCALATION_HORIZON_CD, horizon_unit="calendar", checkable=False)
        why.append("policy claim; checkable only against a dated action entering the corpus (PENDING)")
    else:
        out.update(horizon_days=None, horizon_unit=None, checkable=False)
        if not why:
            why.append("no asset + direction/level + horizon in the quote")
    out.update(kind=kind, direction=direction, why="; ".join(why) if why else {
        "direction": f"direction claim on {asset} at +{out.get('horizon_days')} trading days",
        "level": f"level claim: ${level:.0f} on {asset} within +{out.get('horizon_days')} trading days" if level is not None else "",
        "flow": "flow claim (barrels/transits stop or resume); price proxy until flow history exists",
        "escalation": "escalation claim between actors; resolves on +90d corpus outcome",
    }.get(kind, ""))
    return out, None


_ISO = re.compile(r"^(19|20)\d{2}-\d{2}-\d{2}$")


def _iso_or_none(v):
    """Amendment 6: a stated ISO date or None -- never the capture date."""
    v = (v or "").strip()[:10]
    return v if _ISO.match(v) else None


def cage(proposal, text, voc, class_hint=None):
    """Validate a whole proposal. Returns the caged read (never partial repair; rejects listed)."""
    rejected = []
    p = proposal if isinstance(proposal, dict) else {}
    model_class = p.get("event_class")
    ec = model_class
    if ec is not None and ec not in VALID_TYPES:
        rejected.append({"what": "event_class", "value": ec, "reason": "not a registered event type"})
        ec = None
    entities, seen = [], set()
    for e in p.get("entities") or []:
        eid, role = (e or {}).get("id"), (e or {}).get("role")
        if eid not in voc:
            rejected.append({"what": "entity", "value": eid, "reason": "not in the entities table"}); continue
        if role not in ROLES:
            rejected.append({"what": "entity_role", "value": f"{eid}:{role}", "reason": "role not registered"}); continue
        if eid in seen:
            continue
        seen.add(eid)
        entities.append({"id": eid, "name": voc[eid], "type": eid.split(".", 1)[0], "role": role})
    unmapped = sorted({_canon(u)[:80] for u in (p.get("unmapped") or []) if isinstance(u, str) and _canon(u)})
    has_actor = any(e["role"] in ("actor", "target") for e in entities)
    claims, seen_q = [], set()
    for c in (p.get("claims") or [])[:MAX_CLAIMS * 2]:
        out, reason = cage_claim(c, text, has_actor)
        if out is None:
            rejected.append({"what": "claim", "value": (c or {}).get("quote", "")[:120] if isinstance(c, dict) else str(c)[:120], "reason": reason}); continue
        if out["text"].lower() in seen_q:
            continue
        seen_q.add(out["text"].lower())
        claims.append(out)
        if len(claims) >= MAX_CLAIMS:
            break
    conf = p.get("confidence") if p.get("confidence") in ("high", "medium", "low", "fallback") else None
    return {"event_class": class_hint or ec, "model_class": model_class, "event_date": _iso_or_none(p.get("event_date")), "confidence": conf,
            "entities": entities, "unmapped": unmapped, "claims": claims, "rejected": rejected}


def to_ledger_claim(c, event_class, entity_ids):
    """The ledger-shaped claim (ledger.verdict_for / log_claims contract)."""
    return {**c, "event_class": event_class, "entities": list(entity_ids or [])}


# ----------------------------------------------------------------------------- regex fallback (labelled)

def _fallback_story(conn, text, class_hint=None):
    import triage as T
    sents = _sentences(text) or [text]
    ents_all, classes, claims, seen = set(), Counter(), [], set()
    for s in sents[:40]:
        ents, et = T.extract(conn, s)
        ents_all |= set(ents)
        if et:
            classes[et] += 1
        for clause in L.split_clauses(s):
            hypo = bool(re.search(r"\b(could|would|may|might|if|possibly|potentially|threaten\w*|were to|risk of)\b", clause, re.I))
            t = L.type_claim(clause, et or class_hint, ents, "hypothetical" if hypo else "asserted")
            if t["text"].lower() in seen or (t["kind"] == "uncheckable" and not et):
                continue
            seen.add(t["text"].lower())
            t["quote"] = t["text"]
            claims.append(t)
    etype = class_hint or (classes.most_common(1)[0][0] if classes else None)
    claims.sort(key=lambda c: c["checkable"], reverse=True)
    voc = vocab(conn)
    return {"event_class": etype, "model_class": None, "unmapped": [],
            "entities": [{"id": e, "name": voc.get(e, e), "type": e.split(".", 1)[0], "role": "mention"} for e in sorted(ents_all)],
            "claims": claims[:MAX_CLAIMS], "rejected": []}


# ----------------------------------------------------------------------------- public reads

def read_story(arg, class_hint=None, proposal=None, conn=None, use_cache=True, model=None):
    """Read one story (URL or text). `proposal` lets a caller (tests) supply a recorded model output,
    so the cage is exercised without the CLI. Returns the caged read plus provenance."""
    prep = prepare(arg)
    text = prep["text"]
    own = conn is None
    conn = conn or sqlite3.connect(DB)
    try:
        voc = vocab(conn)
        meta = {"mode": "llm", "model": model or MODEL, "cached": False, "secs": None, "error": None}
        if proposal is None:
            key = _cache_key("story", text, model)
            hit = _cache_get(key) if use_cache else None
            if hit:
                proposal, meta["cached"], meta["model"] = hit["proposal"], True, hit.get("model")
            else:
                proposal, m = _call(system_prompt(voc), f"TITLE: {prep['title']}\n\nTEXT:\n{text}", STORY_SCHEMA, model=model)
                meta.update(m)
                if proposal is not None:
                    _cache_put(key, proposal, meta)
        else:
            meta["mode"] = "recorded"
        if proposal is None:
            r = _fallback_story(conn, text, class_hint)
            meta["mode"] = "regex_fallback"
        else:
            r = cage(proposal, text, voc, class_hint)
        ids = [e["id"] for e in r["entities"]]
        r["claims"] = [to_ledger_claim(c, r["event_class"], ids) for c in r["claims"]]
        r.update(title=prep["title"], url=prep["url"], was_url=bool(prep["url"]), fetched=prep["fetched"], fetch_error=prep["error"],
                 text_chars=len(text), qualifying_entities=qualifying_entities(r["entities"], meta["mode"]),
                 reader={**meta, "registration": REGISTRATION})
        return r
    finally:
        if own:
            conn.close()


def read_headlines(heads, proposals=None, conn=None, use_cache=True, model=None):
    """Read a list of headlines (the Feed): batched model calls, cached per headline, regex fallback
    per headline when the model is unavailable. Returns one caged read per headline, in order."""
    own = conn is None
    conn = conn or sqlite3.connect(DB)
    try:
        voc = vocab(conn)
        results = [None] * len(heads)
        todo = []
        for i, h in enumerate(heads):
            if proposals is not None:
                results[i] = ("recorded", proposals[i], None); continue
            hit = _cache_get(_cache_key("headline", h, model)) if use_cache else None
            if hit:
                results[i] = ("llm", hit["proposal"], {"cached": True, "model": hit.get("model")})
            else:
                todo.append(i)
        for start in range(0, len(todo), BATCH):
            idx = todo[start:start + BATCH]
            user = "HEADLINES (one item per line; return one object per index i):\n" + "\n".join(f"[{i}] {heads[i]}" for i in idx)
            obj, meta = _call(system_prompt(voc), user, BATCH_SCHEMA, model=model, timeout=TIMEOUT_S + 60)
            got = {it.get("i"): it for it in (obj or {}).get("items", [])} if obj else {}
            for i in idx:
                it = got.get(i)
                if it is None:
                    results[i] = ("regex_fallback", None, {"error": meta.get("error") or "headline missing from batch reply", "model": meta.get("model")})
                else:
                    prop = {"event_class": it.get("event_class"), "event_date": _iso_or_none(it.get("event_date")), "confidence": it.get("confidence") or None,
                            "entities": it.get("entities") or [], "unmapped": [], "claims": [it["claim"]] if it.get("claim") else []}
                    _cache_put(_cache_key("headline", heads[i], model), prop, meta)
                    results[i] = ("llm", prop, {"cached": False, "model": meta.get("model"), "secs": meta.get("secs")})
        out = []
        for i, h in enumerate(heads):
            mode, prop, meta = results[i]
            if prop is None:
                import triage as T
                etype = T.classify_type(h)
                ents, _ = T.extract(conn, h)
                t = L.type_claim(h, etype)
                r = {"event_class": etype, "event_date": None, "confidence": "fallback", "model_class": None, "unmapped": [], "rejected": [],
                     "entities": [{"id": e, "name": voc.get(e, e), "type": e.split(".", 1)[0], "role": "mention"} for e in ents],
                     "claims": [t] if t["kind"] != "uncheckable" else []}
                mode = "regex_fallback"
            else:
                r = cage(prop, h, voc)
            ids = [e["id"] for e in r["entities"]]
            r["claims"] = [to_ledger_claim(c, r["event_class"], ids) for c in r["claims"]]
            r.update(headline=h, qualifying_entities=qualifying_entities(r["entities"], mode),
                     reader={"mode": mode, **(meta or {}), "registration": REGISTRATION})
            out.append(r)
        return out
    finally:
        if own:
            conn.close()


# ----------------------------------------------------------------------------- CLI

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    if sys.argv[1] == "--headlines":
        for r in read_headlines(sys.argv[2:]):
            print(f"{str(r['event_class']):22s} {r['reader']['mode']:15s} ents={[(e['id'], e['role']) for e in r['entities']]} "
                  f"qualifying={r['qualifying_entities']} :: {r['headline'][:70]}")
        return
    r = read_story(" ".join(sys.argv[1:]))
    print(f"TITLE   {r['title']}\nCLASS   {r['event_class']} (model said {r['model_class']})  reader={r['reader']['mode']} "
          f"model={r['reader'].get('model')} cached={r['reader'].get('cached')} secs={r['reader'].get('secs')} err={r['reader'].get('error')}")
    print(f"ENTITIES {[(e['id'], e['role']) for e in r['entities']]}  unmapped={r['unmapped']}  qualifying={r['qualifying_entities']}")
    for c in r["claims"]:
        print(f"  [{c['kind']:11s}] asset={c['asset']} dir={c['direction']} level={c['level']} h={c['horizon_days']} chk={c['checkable']} :: {c['text'][:90]}")
    for x in r["rejected"]:
        print(f"  REJECTED {x['what']}={str(x['value'])[:60]!r}: {x['reason']}")


if __name__ == "__main__":
    main()
