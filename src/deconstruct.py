"""
deconstruct.py -- ARTICLE DECONSTRUCTION. Break an article into its claims and answer
each one with the QUANT ENGINE, not an opinion.

The quant engine rules. This module pulls the discrete claims an article makes, tags
each (entities, event class, quantified figures, fact-vs-opinion), and binds every claim
that maps to a measurable event class to the engine's MEASURED evidence: the historical
base-rate market move for that class, the nearest verified precedents, and the live market
state. The verdict on each claim is rendered by the NUMBERS -- what history and the market
actually say -- never by a generated opinion. No LLM, no fabrication, $0.

For a NEWS article: here is each claim, and here is what history + the market say about an
event of this class. For an OP-ED: the same, deliberately replacing the writer's synthesis
with the data behind (or against) each assertion -- "eliminate the opinion, look at the data."

Reuses: src/brief.py (the quant reads), src/triage.py (deterministic entity/event extraction),
src/event_study.py (CAR math). Extraction is a real-paragraph scrape (nav/boilerplate filtered).
"""

import html as _html
import re
import sqlite3
from pathlib import Path

import triage as T
import event_study as ES
import brief as BR

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# --- claim/opinion detection (deterministic, transparent) ---------------------------------
OPINION = re.compile(r"\b(i believe|i think|in my view|we must|we should|it is clear that|"
                     r"make no mistake|frankly|the truth is|arguably|one might argue|"
                     r"i argue|i suspect|should have|ought to|op-?ed|opinion|commentary)\b", re.I)
FIRST_PERSON = re.compile(r"\b(I|we|our|my)\b")            # NB: not "us"/"US" (matches United States)
HYPO = re.compile(r"\b(could|would|may|might|if|possibly|potentially|threaten\w*|were to|risk of)\b", re.I)
CONCRETE = re.compile(r"\b(announced?|impos\w*|reimpos\w*|signed?|struck|seiz\w*|closed?|halt\w*|"
                      r"bann\w*|launch\w*|cut|raised?|declared?)\b", re.I)
# Negation — the single most damaging blind spot: "Iran did NOT close Hormuz", "NO sanctions
# imposed", "denied any plan". A negated event is a non-event; the engine must give no read.
NEG = re.compile(r"\b(no|not|never|without|denied|denies|deny|unfounded|avoided|refrain\w*|"
                 r"declined?|ruled? out|ruling out|unchanged|scrapp\w*|abandon\w*|call(ed)? off|"
                 r"no longer|fail\w* to|zero)\b", re.I)
# Polarity — an EASING/reversal ("sanctions LIFTED", "ceasefire", "reopened") is the opposite of
# an escalation and must not read the same. The class base rate is directionless (size); easing
# historically points the other way.
RELIEF = re.compile(r"\b(lift\w*|eas\w*|remov\w*|waiv\w*|rollback|roll back|suspend\w*|restore\w*|"
                    r"de-?escalat\w*|reopen\w*|resum\w*|unfreez\w*|normaliz\w*|ceasefire|truce|"
                    r"deal reached|agreement)\b", re.I)


def _negated(s):
    """True if an event trigger in the sentence is negated (a negation token shortly before it,
    or a 'no/without <event-noun>' construction). Conservative: over-flagging to no-read is safer
    than asserting the opposite of the article."""
    low = s.lower()
    if re.search(r"\b(no|not|without|denied|deny|denies|zero|ruled out)\s+\w{0,14}?\s*"
                 r"(sanction|strike|attack|blockade|closure|closing|cut|war|conflict|disrupt)", low):
        return True
    trigs = [m.start() for m in ASSERT.finditer(low)] + [m.start() for m in CONCRETE.finditer(low)]
    return any(0 <= t - m.end() <= 45 for m in NEG.finditer(low) for t in trigs)
FIGURE = re.compile(r"(\$\s?\d[\d,.]*\s?(?:billion|million|trillion|bn|bbl|barrels?|bpd|%)?"
                    r"|\b\d[\d,.]*\s?(?:%|percent|billion|million|trillion|barrels?|bpd|"
                    r"basis points|bps|mb/?d)\b)", re.I)
ASSERT = re.compile(r"\b(will|would|could|plans?|announce\w*|impos\w*|threat\w*|cut|halt|ban|"
                    r"sanction\w*|target\w*|collapse|crater|surge|spike|escalat\w*|strike\w*|"
                    r"seiz\w*|block\w*|retaliat\w*)\b", re.I)
_BOILER = ("subscribe", "advertise", "cookie", "sign in", "newsletter", "all rights reserved",
           "read more", "follow us", "share this", "watch cbs", "getty images")


def _sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", text or "")
    return [s.strip() for s in parts if 28 <= len(s.strip()) <= 400]


def article_type(text):
    """Fact (reportage) vs opinion (op-ed), by transparent markers. An op-ed is not taken on
    the writer's authority -- it is evaluated against the data, claim by claim."""
    words = max(len((text or "").split()), 1)
    op = len(OPINION.findall(text or ""))
    fp = len(FIRST_PERSON.findall(text or ""))
    # density only meaningful on a real article (>=150 words); short inputs lean on the marker count
    density = round((op * 4 + fp) / (words / 1000.0), 1) if words >= 150 else None
    is_op = op >= 3 or (density is not None and density > 12)
    return {"type": "opinion" if is_op else "fact",
            "opinion_markers": op, "first_person": fp, "density_per_1k": density,
            "note": ("Reads as an op-ed. The engine evaluates each assertion against measured "
                     "data rather than accepting the writer's synthesis." if is_op else
                     "Reads as reportage. Each claim is still bound to the measured evidence below.")}


def extract_body(arg):
    """(text, url, was_url). If arg is a URL, fetch the real article and pull prose paragraphs
    (nav/boilerplate filtered). Falls back to the raw arg as text."""
    a = (arg or "").strip()
    if not re.match(r"^https?://", a):
        return a, None, False
    try:
        import requests
        raw = requests.get(a, timeout=15,
                           headers={"User-Agent": "Mozilla/5.0 (ripple-engine research)"}).text
    except Exception:
        return a, a, True
    m = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S | re.I)
    scope = m.group(1) if m else raw
    scope = re.sub(r"<(script|style|nav|aside|footer|header|form|figure)[^>]*>.*?</\1>",
                   " ", scope, flags=re.S | re.I)
    paras = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", scope, re.S | re.I):
        t = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", p))).strip()
        if len(t) >= 50 and any(ch in t for ch in ".?!") and not any(b in t.lower() for b in _BOILER):
            paras.append(t)
    body = " ".join(paras)
    if len(body) < 120:                                  # fall back to a headline-only read
        title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
        body = re.sub(r"\s+", " ", _html.unescape(title.group(1))).strip() if title else a
    return body[:8000], a, True


def _figures(s):
    return list(dict.fromkeys(m if isinstance(m, str) else m[0] for m in FIGURE.findall(s)))[:5]


def claims(conn, text, k=9):
    """The article's salient claims: sentences that name an entity, an event, a figure, or an
    assertive verb. Real sentences, verbatim -- extractive, no paraphrase."""
    out, seen = [], set()
    for s in _sentences(text):
        key = s.lower()[:80]
        if key in seen:
            continue
        ents, etype = T.extract(conn, s)
        figs = _figures(s)
        if not (etype or ents or figs or ASSERT.search(s)):
            continue
        seen.add(key)
        # A hypothetical clause ("Iran could close Hormuz") is a possibility, not an event -- the
        # base rate is for events that occurred, so we answer it as "if it occurs".
        hypo = bool(HYPO.search(s)) and not bool(CONCRETE.search(s))
        neg = _negated(s)
        pol = "easing" if (RELIEF.search(s) and not neg) else "escalation"
        out.append({"text": s, "entities": ents, "event_class": etype, "figures": figs,
                    "assertive": bool(ASSERT.search(s)),
                    "modality": "hypothetical" if hypo else "asserted",
                    "negated": neg, "polarity": pol})
    # rank the most evidence-bearing claims first
    out.sort(key=lambda c: (bool(c["event_class"]), len(c["entities"]), len(c["figures"]),
                            c["assertive"]), reverse=True)
    return out[:k]


def _evidence(et, qr, prec):
    """Compact measured evidence for a claim's event class, lifted from the quant engine."""
    if not et or not qr:
        return None
    a = qr["abs_car20"]; base = qr["baseline"]; d = qr["direction"]
    top = (prec or [None])[0]
    return {
        "event_class": et, "n": qr["n"], "gate": qr["gate"],
        "median_move_pct": a["median_pct"], "iqr_pct": a["iqr_pct"],
        "ci90_pct": a["ci90_median_pct"], "ordinary_median_pct": base["ordinary_median_pct"],
        "class_percentile": base["class_median_percentile"],
        "direction_up_pct": d["up_pct"],
        "cross_asset": qr["cross_asset"][:5],
        "nearest_precedent": (None if not top else {
            "date": top["date"], "title": top["title"], "abs_car20_pct": top["abs_car20_pct"],
            "source_url": top["source_url"], "shared_entities": top["shared_entities"]}),
    }


def _verdict(et, qr, hypothetical=False, negated=False, polarity="escalation"):
    """The engine's one-line answer to a claim, rendered by the numbers. Honesty gates:
    NEGATED events (article says it didn't happen / is reversed) get no read; EASING/reversal is
    flagged (the directionless base rate points the other way); 'materially larger' needs the class
    median 90% CI to clear the BASELINE's 90% CI (a valid CI-to-CI test); the base rate is always
    surfaced ('an ordinary month moves this much X% of the time'); the fat tail is dated; small
    samples flagged; a hypothetical clause is answered 'if it occurs'."""
    if not et:
        return {"stance": "no_class", "text": "This claim doesn't map to an event class the engine "
                "measures — no market read."}
    if negated:
        return {"stance": "negated", "text": (f"The article reports this {et.replace('_', ' ')} did NOT "
                "happen (or is being reversed). The engine gives no market read on a non-event — a "
                "measured base rate applies to events that occurred.")}
    if not qr:
        return {"stance": "insufficient", "text": f"'{et}' has no measured precedent in the corpus."}
    a = qr["abs_car20"]; base = qr["baseline"]
    p = base.get("class_median_percentile"); med = a["median_pct"]; om = base.get("ordinary_median_pct")
    ci_lo = (a.get("ci90_median_pct") or [None])[0]; base_ci = base.get("ordinary_median_ci90") or [None, None]
    rng_hi = a["range_pct"][1]; n = qr["n"]; gate = qr["gate"]; brate = base.get("base_rate_ge_class_median_pct")
    mx = a.get("max_event") or {}
    small = f" Small sample (n={n}) — treat as indicative." if gate != "full" else ""
    iff = "If it occurs, " if hypothetical else ""
    ease = ("This is an EASING/reversal — the base rate below is directionless (size only), and an "
            "easing has historically pointed the opposite way to an escalation. " if polarity == "easing" else "")
    tail = (f" The class is fat-tailed: the worst case, “{mx.get('title', '')[:52]}” ({(mx.get('date') or '')[:7]}), "
            f"moved {rng_hi}%." if mx.get("title") else f" Fat-tailed; worst case {rng_hi}%.")
    baserate = (f" An ordinary month moves at least this much about {int(brate)}% of the time."
                if brate is not None else "")
    pc = f"the {BR._ordinal(p)} percentile of ordinary moves" if p is not None else "of uncertain rank"
    material = (ci_lo is not None and base_ci[1] is not None and ci_lo > base_ci[1])
    if material:
        return {"stance": "material",
                "text": (f"{ease}{iff}history (n={n} {et} events) shows a median {med}% 20-day oil move — {pc}, "
                         f"and its 90% CI clears the everyday baseline's, so **materially larger than normal**."
                         f"{baserate}{tail}{small}")}
    return {"stance": "in_line",
            "text": (f"{ease}{iff}history (n={n} {et} events) shows a median {med}% 20-day oil move — {pc} "
                     f"(everyday median ~{om}%), so the TYPICAL move is in line with normal oil volatility."
                     f"{baserate}{tail}{small}")}


def public_sentiment(conn, ents, etype):
    """The measured public-mood layer (the 'quantified anguish'): coverage tone, geopolitical-risk
    percentile, attention spikes, conflict-media intensity -- all REAL signals the engine already
    tracks. Sentiment as data, not vibes."""
    out = {}
    gpr = BR._load_json("gpr_signal.json").get("gpr") or {}
    if gpr.get("percentile") is not None:
        out["geopolitical_risk"] = {"percentile": gpr["percentile"], "band": gpr.get("band"),
                                    "posture": gpr.get("posture")}
    tone = BR._load_json("gdelt_tone.json")
    tones = tone.get("topics") or tone.get("summary") or []
    if isinstance(tones, list) and tones:
        out["coverage_tone"] = [{"topic": t.get("topic"), "tone": t.get("tone"), "mood": t.get("mood")}
                                for t in tones][:6]
    att = [p for p in BR._load_json("wiki_attention.json").get("pages", [])
           if p.get("flag") in ("spike", "elevated")]
    if att:
        out["attention_spikes"] = [{"page": p.get("page"), "x_median": p.get("pct_of_median"),
                                    "flag": p.get("flag")} for p in att[:5]]
    ci = [s for s in BR._load_json("conflict_intensity.json").get("situations", [])
          if s.get("band") in ("surge", "elevated")]
    if ci:
        out["conflict_media"] = [{"situation": s.get("situation"), "band": s.get("band"),
                                  "tone": s.get("tone")} for s in ci[:5]]
    out["note"] = ("Measured public-mood signals (news tone, geopolitical-risk index, attention, "
                   "conflict-media volume) — sentiment as data, context to the cold measurement.")
    return out


def market_alignment(dominant_qr, mn):
    """History vs the tape RIGHT NOW: what this event class typically did to oil, set against
    what oil is actually doing today, and whether the live move is confirming or diverging from
    the risk (source-aware transmission from gpr_signal). Aligns the article to live market data."""
    if not dominant_qr:
        return None
    gpr = BR._load_json("gpr_signal.json")
    tr = gpr.get("transmission") or {}
    brent = mn.get("brent") or {}
    med = dominant_qr["abs_car20"]["median_pct"]
    chg5 = brent.get("chg5d")
    flag = tr.get("flag")
    if flag in ("divergence", "watch"):
        stance = "diverging"
        read = ("History implies a move of that size; the tape right now is NOT confirming it — "
                f"Brent is {chg5:+.1f}% over 5 days against elevated risk." if chg5 is not None else
                "History implies a move; the live tape is not confirming it.")
    elif flag in ("confirmed", "consistent"):
        stance = "confirming"
        read = (f"The live tape is moving with the risk — Brent {chg5:+.1f}% over 5 days — consistent "
                "with the historical pattern." if chg5 is not None else
                "The live tape is moving consistently with the historical pattern.")
    else:
        stance = "neutral"
        read = (f"Brent is roughly flat ({chg5:+.1f}% 5d); no clear live confirmation either way."
                if chg5 is not None else "No clear live signal from the tape.")
    return {"history_median_pct": med, "brent_chg5d": chg5, "brent_chg1d": brent.get("chg1d"),
            "gpr_band": (mn.get("gpr") or {}).get("band"), "stance": stance,
            "transmission_verdict": tr.get("verdict"), "read": read}


def historical_record(conn, ret, etype, ents, limit=14):
    """'What history says' -- the FULL measured record for the dominant class: every coded corpus
    event of that class with its measured 20-day Brent move + source, entity-matched first. The
    actual past, with numbers -- not an encyclopedia (the engine is market history, honestly)."""
    if not etype:
        return None
    entset = set(ents)
    rows = conn.execute("SELECT event_id, event_date, title, source_url FROM events WHERE type=? "
                        "ORDER BY event_date DESC", (etype,)).fetchall()
    out = []
    for eid, d, title, url in rows:
        eents = {r[0] for r in conn.execute(
            "SELECT entity_id FROM event_entities WHERE event_id=?", (eid,))}
        c = ES.car_for_event(ret, d)
        move = round(abs(float(c[ES.PRE + 20])) * 100, 1) if c is not None else None
        out.append({"date": d, "title": (title or "")[:80], "source_url": url,
                    "abs_car20_pct": move, "shared_entities": len(entset & eents)})
    out.sort(key=lambda r: (r["shared_entities"], r["abs_car20_pct"] or 0), reverse=True)
    shown = min(limit, len(out))
    return {"event_class": etype, "n_total": len(out), "events": out[:limit],
            "note": (f"The {shown} most entity-relevant of {len(out)} coded {etype} events, each with its "
                     "measured 20-day Brent move. Real, sourced — the engine's history is measured market "
                     "outcomes, not a geopolitical encyclopedia.")}


def deconstruct(arg):
    """Deconstruct an article (URL or text) into claims, each answered by the quant engine."""
    import time
    t0 = time.perf_counter()
    text, url, was_url = extract_body(arg)
    conn = sqlite3.connect(DB)
    ret = ES.load_returns(conn)
    at = article_type(text)
    cs = claims(conn, text)
    all_ents = [e for c in cs for e in c["entities"]]
    # compute the quant read ONCE per distinct event class (the engine rules; reuse it)
    per_class = {}
    for c in cs:
        et = c["event_class"]
        if et and et not in per_class:
            per_class[et] = {"quant": BR.quant_read(conn, ret, et),
                             "precedent": BR.precedent(conn, ret, all_ents, et, k=4)}
    for c in cs:
        et = c["event_class"]
        pc = per_class.get(et, {})
        c["evidence"] = _evidence(et, pc.get("quant"), pc.get("precedent"))
        c["verdict"] = _verdict(et, pc.get("quant"), hypothetical=(c.get("modality") == "hypothetical"),
                                negated=c.get("negated", False), polarity=c.get("polarity", "escalation"))
    # Dominant class = the class the article's claims MOST refer to (salience), tie-broken by
    # sample size. More robust than a priority-ordered full-text classify (which would pick a
    # chokepoint mentioned once in a retaliation clause over the article's actual sanctions topic).
    from collections import Counter as _Counter
    freq = _Counter(c["event_class"] for c in cs if c["event_class"] and not c.get("negated"))
    dominant = (max(freq, key=lambda e: (freq[e], per_class[e]["quant"]["n"]
                    if per_class.get(e, {}).get("quant") else 0)) if freq else None)
    mn = BR.market_now(conn)
    # Only surface the (global) public-mood signals when the article actually has a measurable
    # geopolitical/market class -- otherwise showing "geopolitical risk 93rd pct" on an unrelated
    # article overclaims (an unrelated signal presented as if about the input).
    sentiment = public_sentiment(conn, all_ents, dominant) if dominant else {}
    record = historical_record(conn, ret, dominant, all_ents) if dominant else None
    dq = per_class.get(dominant, {}).get("quant") if dominant else None
    alignment = market_alignment(dq, mn) if dominant else None
    conn.close()
    # The subject to pulse for live unrest/agitation coverage (most-cited country/chokepoint).
    from collections import Counter as _C
    # exclude negated claims from the subject pick too
    all_ents = [e for c in cs if not c.get("negated") for e in c["entities"]] or all_ents
    ef = _C(e for e in all_ents if e.startswith(("country.", "chokepoint.")))
    pulse_query = ef.most_common(1)[0][0].split(".")[-1].replace("_", " ").title() if ef else None
    n_material = sum(1 for c in cs if (c["verdict"] or {}).get("stance") == "material")
    return {
        "input": (arg or "")[:200], "was_url": was_url, "url": url,
        "article_type": at,
        "headline_read": _headline_read(at, cs, per_class, dominant, n_material),
        "n_claims": len(cs), "claims": cs,
        "event_classes": sorted(per_class.keys()),
        "dominant_class": dominant,
        "historical_record": record,
        "market_alignment": alignment,
        "pulse_query": pulse_query,
        "market_now": mn, "public_sentiment": sentiment,
        "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
        "discipline": ("Every claim is answered by measured history + live market data, never by a "
                       "generated opinion. Expected magnitude, not a probability. Real corpus events only."),
    }


def _headline_read(at, cs, per_class, dominant, n_material):
    """The one honest sentence at the top: what the DATA says about this article's central claim.
    States the typical move AND the tail (never 'ordinary' alone on a fat-tailed class), and only
    claims 'materially larger' when the median's 90% CI clears the everyday baseline."""
    if not dominant or not per_class.get(dominant, {}).get("quant"):
        return ("No claim in this article maps to an event class the engine measures — the data offers "
                "no market read on it.")
    qr = per_class[dominant]["quant"]; a = qr["abs_car20"]; base = qr["baseline"]
    p = base.get("class_median_percentile"); med = a["median_pct"]
    om = base.get("ordinary_median_pct"); ci_lo = (a.get("ci90_median_pct") or [None])[0]
    base_ci = base.get("ordinary_median_ci90") or [None, None]
    rng_hi = a["range_pct"][1]
    kind = "opinion piece" if at["type"] == "opinion" else "report"
    tail = f" — but the class is fat-tailed, with a worst case of {rng_hi}% on record"
    if ci_lo is not None and base_ci[1] is not None and ci_lo > base_ci[1]:
        return (f"This {kind} centres on **{dominant}**. On the measured record (n={qr['n']}), events of that "
                f"class moved oil a median **{med}%** over 20 days — the {BR._ordinal(p)} percentile of "
                f"ordinary moves, **materially larger than everyday volatility**{tail}. Size, not direction.")
    return (f"This {kind} centres on **{dominant}**. On the measured record (n={qr['n']}), the TYPICAL 20-day "
            f"oil move was **{med}%** — about the {BR._ordinal(p)} percentile of ordinary moves (everyday "
            f"median ~{om}%){tail}. So the central move is usually in line with normal volatility, though the "
            f"tail is real; the framing outruns the median.")


# --- CLI ----------------------------------------------------------------------------------
def main():
    import sys
    import json
    if len(sys.argv) < 2:
        print('usage: python3 src/deconstruct.py "<text>" | <url> [--json]')
        return
    d = deconstruct(" ".join(a for a in sys.argv[1:] if not a.startswith("--")))
    if "--json" in sys.argv:
        print(json.dumps(d, indent=2, default=str))
        return
    print("=" * 78)
    print(f"ARTICLE DECONSTRUCTION  [{d['article_type']['type'].upper()}]  latency {d['latency_ms']}ms")
    print("=" * 78)
    print("READ:", d["headline_read"])
    print(f"\n{d['n_claims']} claims · classes: {', '.join(d['event_classes']) or 'none'}\n")
    for i, c in enumerate(d["claims"], 1):
        print(f"[{i}] {c['text'][:100]}")
        print(f"     class={c['event_class'] or '—'} entities={', '.join(c['entities']) or 'none'} "
              f"figures={c['figures'] or '—'}")
        print(f"     VERDICT: {c['verdict']['text']}")
        print()


if __name__ == "__main__":
    main()
