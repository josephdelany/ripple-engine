"""
brief.py -- THE ANALYTICAL BRIEF. Quant insight injected into a news story, honestly.

WHAT THIS IS (and why it is not "AI slop"):
Newsrooms like NYT or Al Jazeera lead with the STORY. This engine leads with the
MEASURED history. brief.py fuses the two into one institutional-grade brief: it
takes a headline/paragraph/URL, classifies it deterministically (no LLM, no
fabrication), and assembles a structured brief that answers, in order:

  BOTTOM LINE (BLUF)  -- the one honest sentence, conclusion first.
  THE STORY           -- what happened, its entities and event class (sourced).
  THE QUANT READ      -- how oil HAS BEHAVED around events of this class: the base
                         rate |CAR+20| with n, range, IQR, a BOOTSTRAP 90% CI, and
                         where that sits vs a NULL baseline of ordinary 20-day moves
                         (lift, not a naked number). Plus the multi-horizon CAR path,
                         the cross-asset propagation (oil/gas/USD/gold/rates), and
                         today's amplifier state.
  PRECEDENT           -- the nearest VERIFIED corpus analogues (real events, dates,
                         measured moves, sources).
  MARKET NOW          -- Brent level + move, priced oil vol (OVX) percentile, GPR,
                         chokepoint flows -- the live state a shock would land in.
  PRICED vs OUR VIEW  -- THE GAP: the source-aware transmission read (supply/demand
                         channel + does the real move confirm it), the engine-vs-market
                         gap (under-priced risk / over-priced fear), what prediction
                         markets price, and the RESOLVING track record (honest, small-N).
  WHAT WOULD CHANGE IT-- observable, falsifiable invalidation criteria.

THE HONESTY GATES (enforced here, grounded in the research standard):
  * Association, never causation. We say events "were associated with" / "moved
    around", never "caused". (MacKinlay 1997; Shiller's own "no final proof of
    causality"; Cutler-Poterba-Summers: <=1/3 of large moves have identifiable news.)
  * Every conditional statistic ships with its base rate (base-rate neglect).
  * Magnitude and probability are separate numbers, never merged. This engine emits
    expected MAGNITUDE (size of the abnormal move), NOT an occurrence probability.
  * Small-N gates drive the output mode: n>=30 full; 10-29 caveat + wide CI; <10
    individual cases only; <4 a documented gap, never a fabricated rate.
  * Selection disclosure: the corpus is hand-curated on memorable events, so the
    measured move is an UPPER BOUND, not an unbiased estimate.
  * Clustering disclosure: overlapping events mean effective N < nominal N.
  * Oil confounder panel, always: global demand, OPEC+ supply, inventories, the
    dollar, the risk premium were also moving and are not isolated here (Kilian 2009).
  * Deterministic + reproducible: bootstrap/baseline use a fixed seed, so the same
    input yields the same brief. numpy does the arithmetic; the code never eyeballs it.

Reuses: triage (deterministic extraction + analogues + amplifier), event_study (the
CAR math), cross_asset (the edges/propagation labels), and the committed pipeline
artifacts (engine_read, gpr_signal, gaps, corroboration, predmkt, market_live,
portwatch). $0 / keyless / no LLM in the analysis.

Run:  python3 src/brief.py "Iran seizes a tanker in the Strait of Hormuz"
      python3 src/brief.py --daily        # today's top real story, auto-selected
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

import triage as T
import event_study as ES

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
DATA = ROOT / "data"

# Small-sample gates (research R4). Below MIN_STAT we do not estimate a rate.
N_FULL, N_CAVEAT, N_MIN = 30, 10, 4
BOOT_SEED = 7          # fixed -> the brief is reproducible (same data -> same CI)
BOOT_ITERS = 3000
BASELINE_N = 500       # random ordinary windows for the null distribution of |CAR+20|

# The oil-move confounders we must name every time (Kilian 2009: composition of the
# shock, not the headline, sets the price).
CONFOUNDERS = ("global demand, OPEC+ supply decisions, inventories, the US dollar, "
               "and the precautionary risk premium")

# Cross-asset panel for the brief: a curated, legible subset (series -> label, unit).
# Historical CARs come from the `edges` table (populated by cross_asset.py); live feeds
# being stale does not affect these -- they are measured over history.
CROSS_ASSET = [
    ("fred.DCOILBRENTEU", "Brent oil", "%"),
    ("fred.DHHNGSP", "US natgas", "%"),
    ("fred.DTWEXBGS", "US dollar (broad)", "%"),
    ("yf.gold", "Gold", "%"),
    ("yf.sp500", "S&P 500", "%"),
    ("fred.DGS10", "10Y yield", "bps"),
    ("fred.T5YIE", "5Y breakeven", "bps"),
]

_baseline_cache = {}


def _load_json(name, default=None):
    p = DATA / name
    if not p.exists():
        return default if default is not None else {}
    try:
        return json.loads(p.read_text())
    except (ValueError, OSError):
        return default if default is not None else {}


# --------------------------------------------------------------------------- stats

def _abs_car20(ret, date):
    """|CAR+20| in % for one date, or None if outside price history."""
    car = ES.car_for_event(ret, date)
    return abs(float(car[ES.PRE + 20])) * 100 if car is not None else None


def baseline_abs_car20(ret):
    """The NULL distribution: |CAR+20| of a random ORDINARY 20-day window. This is the
    denominator that turns a naked class number into a LIFT (research R1). Sampled once
    per price series with a fixed seed -> deterministic. Returns a numpy array (%)."""
    key = (id(ret), len(ret))
    if key in _baseline_cache:
        return _baseline_cache[key]
    rng = np.random.default_rng(BOOT_SEED)
    dates = ret.index
    lo, hi = ES.EST_START + 1, len(dates) - ES.POST - 1     # valid window for car_for_event
    out = []
    if hi > lo:
        picks = rng.integers(lo, hi, size=min(BASELINE_N, hi - lo))
        for pos in picks:
            car = ES.car_for_event(ret, dates[int(pos)])
            if car is not None:
                out.append(abs(float(car[ES.PRE + 20])) * 100)
    arr = np.array(out) if out else np.array([])
    _baseline_cache[key] = arr
    return arr


def bootstrap_ci(values, stat="median", alpha=0.10):
    """A percentile bootstrap CI for the mean/median of small, heavy-tailed, clustered
    event returns -- the parametric t-test is unsafe here (research R2). Fixed seed."""
    a = np.asarray(values, float)
    if len(a) < 2:
        return [None, None]
    rng = np.random.default_rng(BOOT_SEED)
    fn = np.median if stat == "median" else np.mean
    boots = [float(fn(rng.choice(a, size=len(a), replace=True))) for _ in range(BOOT_ITERS)]
    lo, hi = np.percentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return [round(float(lo), 2), round(float(hi), 2)]


def class_paths(conn, ret, etype):
    """Every CAR path (numpy array over t-PRE..t+POST) for events of this class, with
    their event_ids. Real corpus events only."""
    rows = conn.execute("SELECT event_id, event_date FROM events WHERE type=?", (etype,)).fetchall()
    out = []
    for eid, d in rows:
        car = ES.car_for_event(ret, d)
        if car is not None:
            out.append((eid, car))
    return out


def sample_gate(n):
    """Which honesty mode the sample size forces (research R4)."""
    if n >= N_FULL:
        return "full"
    if n >= N_CAVEAT:
        return "caveat"
    if n >= N_MIN:
        return "cases_only"
    return "insufficient"


# --------------------------------------------------------------------------- blocks

def quant_read(conn, ret, etype):
    """The measured behaviour of Brent around events of this class: base-rate |CAR+20|
    (mean/median, range, IQR, bootstrap CI), the null-baseline LIFT, the multi-horizon
    CAR path + curve, and the honest small-N gate + disclosures. Magnitude, not probability."""
    paths = class_paths(conn, ret, etype)
    n = len(paths)
    if n == 0:
        return None
    arrs = np.vstack([c for _, c in paths])                 # n x window
    abs20 = np.abs(arrs[:, ES.PRE + 20]) * 100              # |CAR+20| per event (%)
    mean_path = arrs.mean(axis=0) * 100                     # % CAR path
    se_path = (arrs.std(axis=0, ddof=1) / np.sqrt(n)) * 100 if n > 1 else np.zeros_like(mean_path)

    gate = sample_gate(n)
    med = round(float(np.median(abs20)), 2)
    mean = round(float(abs20.mean()), 2)

    # Null baseline -> lift. Where does this class's typical move sit among ordinary moves?
    base = baseline_abs_car20(ret)
    base_median = round(float(np.median(base)), 2) if len(base) else None
    pctile_of_class = (round(float((base < med).mean() * 100), 0)
                       if len(base) else None)              # class median at Pth pct of ordinary moves
    # Base rate: how often an ordinary 20-day window moves >= this class's median.
    base_rate_ge = (round(float((base >= med).mean() * 100), 0) if len(base) else None)

    horizons = []
    for h in ES.HORIZONS:
        col = arrs[:, ES.PRE + h] * 100
        horizons.append({"h": h, "mean_pct": round(float(col.mean()), 2),
                         "ci90": bootstrap_ci(col, stat="mean")})

    curve = [{"t": int(t), "mean": round(float(mean_path[i]), 3), "se": round(float(se_path[i]), 3)}
             for i, t in enumerate(range(-ES.PRE, ES.POST + 1))]

    return {
        "event_class": etype, "n": n, "gate": gate,
        "abs_car20": {
            "mean_pct": mean, "median_pct": med,
            "range_pct": [round(float(abs20.min()), 2), round(float(abs20.max()), 2)],
            "iqr_pct": [round(float(np.percentile(abs20, 25)), 2),
                        round(float(np.percentile(abs20, 75)), 2)],
            "ci90_median_pct": bootstrap_ci(abs20, stat="median"),
            "ci90_mean_pct": bootstrap_ci(abs20, stat="mean"),
        },
        "baseline": {"ordinary_median_pct": base_median, "n_windows": int(len(base)),
                     "class_median_percentile": pctile_of_class,
                     "base_rate_ge_class_median_pct": base_rate_ge},
        "car_horizons": horizons,          # signed mean CAR at +1/+5/+10/+20
        "car_curve": curve,                # for the SVG CAR curve (t=0 rule + SE band)
        "cross_asset": cross_asset_read(conn, etype),
        "disclosures": {
            "selection": ("The corpus is hand-curated on memorable, material events, so "
                          "this is an UPPER BOUND on the typical move, not an unbiased estimate."),
            "clustering": ("Some events overlap in time; the effective sample is below the "
                           "nominal n, so the interval is, if anything, optimistic."),
            "confounders": (f"Association, not cause: {CONFOUNDERS} were also moving and are "
                            "not isolated here. Most large oil moves have no single news cause."),
        },
    }


def cross_asset_read(conn, etype):
    """Class-mean cross-asset reaction from the `edges` table (event-study CARs beyond oil).
    Descriptive; historical; each labelled with its unit (% for prices, bps for yields)."""
    out = []
    for series, label, unit in CROSS_ASSET:
        row = conn.execute(
            "SELECT AVG(ed.car20), COUNT(*) FROM edges ed JOIN events e ON e.event_id=ed.event_id "
            "WHERE ed.target_series=? AND e.type=?", (series, etype)).fetchone()
        if row and row[0] is not None and row[1]:
            out.append({"label": label, "unit": unit,
                        "car20": round(float(row[0]), 2), "n": int(row[1])})
    return out


def precedent(conn, ret, ents, etype, k=5):
    """Nearest VERIFIED corpus analogues, with measured |CAR+20| and entity overlap (so a
    type-only match is visible as the weak precedent it is). Real events only."""
    entset = set(ents)
    scored = []
    for eid, d, t, title, url in conn.execute(
            "SELECT event_id, event_date, type, title, source_url FROM events"):
        eents = {r[0] for r in conn.execute(
            "SELECT entity_id FROM event_entities WHERE event_id=?", (eid,))}
        overlap = len(entset & eents)
        score = (2 if t == etype else 0) + overlap
        if score <= 0:
            continue
        scored.append((score, overlap, {
            "event_id": eid, "date": d, "type": t, "title": title, "source_url": url,
            "abs_car20_pct": _abs_car20(ret, d), "shared_entities": overlap}))
    scored.sort(key=lambda s: (s[0], s[2]["abs_car20_pct"] or 0), reverse=True)
    return [a for _, _, a in scored[:k]]


def market_now(conn):
    """The live state a shock would land in: Brent level + move, priced oil vol (OVX)
    percentile, GPR percentile + posture, chokepoint flow flags. Each carries an as-of."""
    ml = _load_json("market_live.json")
    assets = ml.get("assets") or {}
    brent = assets.get("live.brent") or {}
    gpr = _load_json("gpr_signal.json")
    g = gpr.get("gpr") or {}
    gap = (_load_json("gaps.json").get("live_gap") or {})
    pw = _load_json("portwatch.json").get("chokepoints") or []
    hot = [{"chokepoint": c.get("chokepoint"), "flag": c.get("flag"),
            "pct_of_median": c.get("pct_of_median"), "latest": c.get("latest")}
           for c in pw if c.get("flag") in ("reduced", "elevated")]
    return {
        "as_of": ml.get("as_of") or gpr.get("as_of"),
        "brent": {"level": brent.get("price"), "chg1d": brent.get("chg1d"),
                  "chg5d": brent.get("chg5d"), "as_of": brent.get("as_of")},
        "priced_oil_vol": {"ovx_percentile": gap.get("priced_ovx_pct"),
                           "ovx": gap.get("priced_ovx"),
                           "note": "OVX = options-implied oil vol; percentile is point-in-time."},
        "gpr": {"percentile": g.get("percentile"), "band": g.get("band"),
                "posture": g.get("posture"), "value": g.get("value")},
        "chokepoints_flagged": hot,
    }


def priced_vs_view(conn):
    """THE GAP -- where the engine's read meets what the market has priced. Source-aware
    transmission (supply/demand channel + does the real move confirm it), the engine-vs-
    market gap (under-priced risk / over-priced fear), what prediction markets price, and
    the RESOLVING, Brier-scored track record (published honestly, small-N and all)."""
    gpr = _load_json("gpr_signal.json")
    trans = gpr.get("transmission") or {}
    gaps = _load_json("gaps.json")
    live = gaps.get("live_gap") or {}
    led = gaps.get("ledger") or {}
    predmkt = _load_json("predmkt.json").get("markets") or []
    # Top prediction markets by volume -- context only, explicitly "priced", never a stat.
    top_mkts = sorted([m for m in predmkt if m.get("prob") is not None],
                      key=lambda m: m.get("volume", 0), reverse=True)[:5]
    return {
        "transmission": {"channel": trans.get("channel"), "expected": trans.get("expected"),
                         "actual": trans.get("actual"), "flag": trans.get("flag"),
                         "verdict": trans.get("verdict")},
        "gap": {"direction": live.get("gap_direction"), "engine_call": live.get("engine_call"),
                "ovx_percentile": live.get("priced_ovx_pct"), "notes": live.get("notes")},
        "prediction_markets": [{"question": (m.get("question") or "")[:110],
                                "prob_pct": round(float(m.get("prob", 0)) * 100),
                                "outcome": m.get("outcome"), "source": "Polymarket (priced, context only)"}
                               for m in top_mkts],
        "track_record": ({"n_scored": led.get("n_scored"),
                          "skill_vs_base": led.get("skill_vs_base"),
                          "brier": led.get("brier"), "base_rate_brier": led.get("base_rate_brier"),
                          "turbulence_base_rate": led.get("turbulence_base_rate"),
                          "caveat": ("SUGGESTIVE, small-N: the value is in the DISAGREEMENT cases, "
                                     "not the average; not yet a validated edge.")}
                         if led.get("n_scored") else None),
    }


def corroboration(conn, ents):
    """Multi-modal confirmation for the most relevant active situation (news + physical
    ship-transits + thermal fires + repricing markets). Confidence, not fact."""
    c = _load_json("corroboration.json")
    conv = c.get("convergence") or {}
    if not conv:
        return None
    # Prefer the situation with the most multi-modal confirmation.
    best = max(conv.items(), key=lambda kv: kv[1].get("n_multi_modal", 0), default=None)
    if not best:
        return None
    sid, s = best
    top = s.get("top") or {}
    return {"situation": sid.replace("situation.", ""),
            "n_events": s.get("n_events"), "n_multi_modal": s.get("n_multi_modal"),
            "max_modality_classes": s.get("max_modality_classes"),
            "confirmed_by": top.get("modality_classes") or ["news only"],
            "top_event": (top.get("headline") or "")[:90]}


# --------------------------------------------------------------------------- prose

def _pp(x, plus=True):
    if x is None:
        return "n/a"
    return f"{x:+.1f}" if plus else f"{x:.1f}"


def bottom_line(story, qr, amp, pv):
    """BLUF: the single honest lead sentence -- conclusion first, association not cause,
    magnitude with its base rate, and today's priced gap. No forecast of whether a shock
    occurs; only how oil has behaved when one of this class did."""
    if not qr:
        return (f"This reads as **{story['event_class'] or 'unclassified'}**, but the corpus has no "
                "measured precedent of this class yet — a documented gap, not a guess.")
    b = qr["abs_car20"]; base = qr["baseline"]; gate = qr["gate"]
    gapdir = (pv.get("gap") or {}).get("direction") or "aligned"
    gaptxt = {"under_priced_risk": "the market looks to be UNDER-pricing the risk",
              "over_priced_fear": "the market looks to be OVER-pricing the fear",
              "aligned": "the market is roughly in line with the engine"}.get(gapdir, gapdir)
    if gate in ("cases_only", "insufficient"):
        return (f"With only n={qr['n']} comparable events, we do not estimate a rate — but in those "
                f"cases oil's 20-day abnormal move ran {b['range_pct'][0]}–{b['range_pct'][1]}% "
                f"(median {b['median_pct']}%). Today the H1/VIX amplifier is {amp.get('state','?')} and "
                f"{gaptxt}.")
    lift = (f"about the {int(base['class_median_percentile'])}th percentile of ordinary 20-day moves"
            if base.get("class_median_percentile") is not None else "of uncertain size vs ordinary moves")
    return (f"**{story['event_class']}** events have historically been *associated with* a median "
            f"20-day abnormal Brent move of **{b['median_pct']}%** "
            f"(n={qr['n']}, 90% CI [{b['ci90_median_pct'][0]}, {b['ci90_median_pct'][1]}]%) — {lift}. "
            f"Today the H1/VIX amplifier is **{amp.get('state','?')}** and {gaptxt}.")


def synthesis(story, qr, mn, pv, corro):
    """A short, sourced synthesis paragraph -- the fusion of narrative and numbers, in the
    honest phrasings the research prescribes. Templated from real values; no LLM."""
    L = []
    if qr:
        b = qr["abs_car20"]; base = qr["baseline"]
        L.append(f"Across {qr['n']} verified events of this class, Brent's 20-day abnormal move "
                 f"was a median {b['median_pct']}% (mean {b['mean_pct']}%, range "
                 f"{b['range_pct'][0]}–{b['range_pct'][1]}%). For scale, an ordinary 20-day window "
                 f"moves a median {base['ordinary_median_pct']}%, and a move at least as large as this "
                 f"class's typical one happens on roughly {int(base['base_rate_ge_class_median_pct'])}% "
                 f"of ordinary windows — so this is "
                 f"{'a genuine amplification over' if (base.get('base_rate_ge_class_median_pct') or 100) < 45 else 'not clearly distinguishable from'} "
                 f"the everyday churn.")
    # The live divergence / transmission read.
    tr = pv.get("transmission") or {}
    if tr.get("verdict"):
        L.append(tr["verdict"])
    gp = pv.get("gap") or {}
    if gp.get("direction"):
        L.append(f"Against the market: the engine reads a **{gp['direction'].replace('_',' ')}** gap "
                 f"(engine call '{gp.get('engine_call')}' vs oil vol priced at the "
                 f"{gp.get('ovx_percentile')}th percentile).")
    if corro:
        L.append(f"Corroboration: the '{corro['situation']}' situation is confirmed across "
                 f"{corro['n_multi_modal']} multi-modal event(s) "
                 f"[{', '.join(corro['confirmed_by'])}] — confidence, not proof.")
    if qr:
        L.append(f"Caveat: {qr['disclosures']['confounders']} {qr['disclosures']['selection']}")
    return " ".join(L)


def what_would_change(story, qr, pv):
    """Observable, falsifiable invalidation markers -- the decision-relevant payload. Every
    item is something you could actually watch for (research R5/R8)."""
    items = [
        "A chokepoint flow disruption in PortWatch (Hormuz / Bab el-Mandeb transits falling "
        "materially below their median) — would move this from priced fear toward realised supply loss.",
        "Brent's realised 20-day volatility rising while OVX is already elevated — would resolve the "
        "over-priced-fear gap against the engine.",
    ]
    tr = pv.get("transmission") or {}
    if tr.get("channel") == "supply" and tr.get("actual") == "down":
        items.append("Brent turning UP on the same supply-fear theatre — would flip the current "
                     "divergence (risk hot, price falling) into a confirmed supply-premium repricing.")
    if story.get("event_class"):
        items.append(f"A second, entity-overlapping {story['event_class']} event within the window — "
                     "would strengthen a currently type-only precedent match.")
    return items


def confidence_tier(qr, corro):
    """A confidence label kept SEPARATE from likelihood (they are orthogonal). Driven by
    sample size and corroboration, not by how dramatic the number is."""
    if not qr:
        return {"tier": "insufficient", "why": "no measured precedent for this event class"}
    gate = qr["gate"]
    modal = (corro or {}).get("n_multi_modal", 0)
    if gate == "full" and modal >= 1:
        t = "moderate"
    elif gate in ("full", "caveat"):
        t = "low-moderate"
    else:
        t = "low"
    return {"tier": t, "why": f"sample gate={gate} (n={qr['n']}), "
                             f"multi-modal corroboration={modal}. Confidence is about evidence "
                             f"quality, NOT the probability of any outcome."}


# --------------------------------------------------------------------------- build

def build_brief(arg, source=None, url=None, date=None):
    """Assemble the full brief for one news item. Deterministic; reuses the engine."""
    t0 = time.perf_counter()
    text, was_url = T._text_from(arg)
    conn = sqlite3.connect(DB)
    ret = ES.load_returns(conn)
    ents, etype = T.extract(conn, text)
    amp = T.amplifier()

    story = {"input": arg[:240], "was_url": was_url, "source": source,
             "url": url, "date": date or T._guess_date(text),
             "entities": ents, "event_class": etype,
             "classification_note": "deterministic vocab/keyword extraction — no LLM, no fabrication"}

    qr = quant_read(conn, ret, etype) if etype else None
    prec = precedent(conn, ret, ents, etype) if etype else []
    mn = market_now(conn)
    pv = priced_vs_view(conn)
    corro = corroboration(conn, ents)
    conn.close()

    brief = {
        "generated_at": None,       # stamped by the caller/endpoint (kept out of the deterministic core)
        "as_of": mn.get("as_of"),
        "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
        "story": story,
        "amplifier": amp,
        "bottom_line": bottom_line(story, qr, amp, pv),
        "quant_read": qr,
        "precedent": prec,
        "market_now": mn,
        "priced_vs_view": pv,
        "corroboration": corro,
        "synthesis": synthesis(story, qr, mn, pv, corro),
        "what_would_change": what_would_change(story, qr, pv),
        "confidence": confidence_tier(qr, corro),
        "receipts": [
            "quant read: src/event_study.py (constant-mean CAR, MacKinlay 1997) over the coded corpus",
            "base rate + lift: null distribution of |CAR+20| on random ordinary windows (seed-fixed)",
            "cross-asset: the `edges` table (src/cross_asset.py, descriptive event study)",
            "amplifier / today: data/engine_read.json (H1 validated; see validation_claims.json)",
            "priced vs view: data/gpr_signal.json + data/gaps.json + data/predmkt.json",
            "corroboration: data/corroboration.json (multi-modal convergence)",
        ],
        "discipline": ("Expected MAGNITUDE, never an occurrence probability. Association, not cause. "
                       "Real corpus events only. Every number one hop from a stored computation."),
    }
    return brief


# --------------------------------------------------------------------------- daily

def pick_daily_story():
    """Auto-select today's top REAL story from the watcher queue. Materiality ranking:
    a story that names oil-relevant ENTITIES (Hormuz, Iran, OPEC, ...) AND classifies to an
    event class beats a type-only keyword match; ties break on the class's expected magnitude,
    then recency. Real RSS headlines only -- GDELT machine pings are excluded."""
    import csv as _csv
    p = DATA / "alert_queue.csv"
    if not p.exists():
        return None
    rows = list(_csv.DictReader(open(p, newline="", encoding="utf-8")))
    days = sorted({(r.get("timestamp_utc") or "")[:10] for r in rows if r.get("timestamp_utc")})
    if not days:
        return None
    day = days[-1]
    todays = [r for r in rows if (r.get("timestamp_utc") or "")[:10] == day
              and not (r.get("headline") or "").startswith("[GDELT]")]
    rates = T.base_rate_by_type()
    conn = sqlite3.connect(DB)
    best, best_key = None, None
    for r in todays:
        head = r.get("headline") or ""
        ents, t = T.extract(conn, head)
        if not t:
            continue
        # rank: (has real entities, expected magnitude, recency) -- entity match dominates.
        key = (1 if ents else 0, rates.get(t, 0.0), r.get("timestamp_utc") or "")
        if best_key is None or key > best_key:
            best, best_key = r, key
    conn.close()
    if not best:
        return None
    return {"headline": best.get("headline"), "source": best.get("source"),
            "url": best.get("url"), "when": best.get("timestamp_utc"), "day": day}


def build_daily_brief():
    """The Daily Brief: a full brief on today's auto-selected top story (or a documented gap)."""
    story = pick_daily_story()
    if not story:
        return {"error": "no classified real headline in the latest watcher day",
                "note": "run src/watcher.py (or the daily loop) to populate the queue"}
    b = build_brief(story["headline"], source=story.get("source"),
                    url=story.get("url"), date=(story.get("when") or "")[:10])
    b["daily_pick"] = {"day": story["day"], "when": story.get("when"),
                       "why": "highest expected-magnitude class among today's real (non-GDELT) headlines"}
    return b


# --------------------------------------------------------------------------- CLI

def _fmt_cli(b):
    if b.get("error"):
        return f"BRIEF -- {b['error']}"
    L = ["=" * 78, "ANALYTICAL BRIEF", "=" * 78,
         f"BOTTOM LINE: {b['bottom_line']}", "",
         f"STORY: {b['story']['input']}",
         f"  class={b['story']['event_class']}  entities={', '.join(b['story']['entities']) or 'none'}"]
    qr = b["quant_read"]
    if qr:
        a = qr["abs_car20"]
        L += ["", f"QUANT READ (n={qr['n']}, gate={qr['gate']}):",
              f"  |CAR+20| median {a['median_pct']}% (90% CI {a['ci90_median_pct']}), "
              f"mean {a['mean_pct']}%, range {a['range_pct']}%, IQR {a['iqr_pct']}%",
              f"  baseline: ordinary 20d median {qr['baseline']['ordinary_median_pct']}%, "
              f"class median at ~{qr['baseline']['class_median_percentile']}th pct of ordinary moves",
              "  cross-asset: " + " | ".join(f"{c['label']} {c['car20']:+}{c['unit']}(n={c['n']})"
                                              for c in qr["cross_asset"])]
    L += ["", "PRECEDENT:"]
    for a in b["precedent"]:
        mag = f"{a['abs_car20_pct']:.1f}%" if a["abs_car20_pct"] is not None else "n/a"
        L.append(f"  {a['date']} |CAR20|={mag:>6} [{a['shared_entities']} shared] {a['title'][:46]}")
    mn = b["market_now"]
    L += ["", f"MARKET NOW: Brent {mn['brent'].get('level')} ({_pp(mn['brent'].get('chg5d'))}% 5d) · "
          f"OVX p{mn['priced_oil_vol'].get('ovx_percentile')} · GPR p{mn['gpr'].get('percentile')} "
          f"({mn['gpr'].get('band')})"]
    pv = b["priced_vs_view"]
    L += [f"PRICED vs VIEW: gap={pv['gap'].get('direction')} · {(pv['transmission'].get('verdict') or '')[:100]}"]
    L += ["", "SYNTHESIS:", "  " + b["synthesis"], "",
          "WHAT WOULD CHANGE IT:"] + [f"  - {x}" for x in b["what_would_change"]]
    L += ["", f"CONFIDENCE: {b['confidence']['tier']} ({b['confidence']['why']})",
          f"DISCIPLINE: {b['discipline']}", f"latency {b['latency_ms']}ms"]
    return "\n".join(L)


def main():
    if "--daily" in sys.argv:
        b = build_daily_brief()
    elif len(sys.argv) >= 2:
        b = build_brief(" ".join(a for a in sys.argv[1:] if not a.startswith("--")))
    else:
        print('usage: python3 src/brief.py "<headline or text>" | --daily [--json]')
        return
    if "--json" in sys.argv:
        print(json.dumps(b, indent=2, default=str))
    else:
        print(_fmt_cli(b))


if __name__ == "__main__":
    main()
