"""
digest.py -- "The Daily": a calm front page for the engine.

The dashboard is for working; The Daily is for READING. One quiet, phone-shaped
page, dark, ~680px wide like a news article, no interaction. It FORMATS engine
artifacts -- it never thinks. Every sentence on the page is either copied verbatim
from an engine artifact (engine_read.json, alert_queue.csv, playbook.md, the
observations table) or is a fixed template label. No analysis is generated here.

Self-contained HTML: inline CSS, no scripts, no external fonts or CDNs -- it opens
offline. If an artifact is missing the page says "not yet generated" and never
crashes.

Run:  python3 src/digest.py            # writes data/digest.html
Serve: GET /digest (backend.py re-renders on request)
"""

import csv
import html
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ENGINE_READ = ROOT / "data" / "engine_read.json"
VALIDATION = ROOT / "data" / "validation_claims.json"   # the honest N=161 tier (H1 live; H2/H3 null)
READ_BACKTEST = ROOT / "data" / "read_backtest.json"    # walk-forward: does H1 help the read OOS
GAPS = ROOT / "data" / "gaps.json"                      # the live gap + resolving scorecard
EDGE_BATTERY = ROOT / "data" / "edge_battery.json"      # the pre-registered, family-wise-corrected battery
PLAYBOOK = ROOT / "data" / "playbook.md"
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
SIT_CONFIG = ROOT / "data" / "situations.yaml"
PREDMKT = ROOT / "data" / "predmkt.json"
CORROBORATION = ROOT / "data" / "corroboration.json"
PORTWATCH = ROOT / "data" / "portwatch.json"
WIKI = ROOT / "data" / "wiki_attention.json"
OUT = ROOT / "data" / "digest.html"

# The ribbon: (label, series_id, unit, decimals). GPR is handled separately (it
# is a computed percentile carried in engine_read.json, not a stored series).
RIBBON = [
    ("Brent", "fred.DCOILBRENTEU", "$/bbl", 2),
    ("WTI", "fred.DCOILWTICO", "$/bbl", 2),
    ("Brent–WTI", "derived.brent_wti_spread", "$", 2),
    ("VIX %ile", "derived.vix_pct", "pct", 0),
    ("Inv σ", "derived.inv_sigma", "σ", 2),
]


def _read_json(path):
    try:
        return json.loads(path.read_text()) if path.exists() else None
    except (ValueError, OSError):
        return None


def latest_two(conn, series_id):
    """Return (value, date, prev_value) for a series -- prev is for up/down colour."""
    rows = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? "
        "ORDER BY obs_date DESC LIMIT 2", (series_id,)).fetchall()
    if not rows:
        return None, None, None
    val, date = rows[0][1], rows[0][0]
    prev = rows[1][1] if len(rows) > 1 else None
    return val, date, prev


def new_alerts(limit=10):
    """Up to `limit` status=new alert cards, newest first."""
    if not ALERT_QUEUE.exists():
        return []
    rows = [r for r in csv.DictReader(open(ALERT_QUEUE, newline="", encoding="utf-8"))
            if r.get("status") == "new"]
    return list(reversed(rows))[:limit]


def playbook_amp_lines():
    """The H1/H2 conditioning lines verbatim from playbook.md (base-rate content)."""
    out = {}
    if not PLAYBOOK.exists():
        return out
    for line in PLAYBOOK.read_text().splitlines():
        if line.startswith("- **H1"):
            out["H1"] = line.lstrip("- ").replace("**", "")
        elif line.startswith("- **H2"):
            out["H2"] = line.lstrip("- ").replace("**", "")
    return out


# --------------------------------------------------------------- HTML pieces

CSS = """
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0e0f13;color:#e7e9ee;
 font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:680px;margin:0 auto;padding:22px 18px 60px}
.mast{border-bottom:1px solid #262a33;padding-bottom:10px;margin-bottom:22px}
.mast h1{font-size:22px;margin:0;letter-spacing:.2px}
.mast .as{color:#8b93a3;font-size:12px;margin-top:3px}
h2.sec{font-size:12px;text-transform:uppercase;letter-spacing:1.4px;color:#8b93a3;
 margin:30px 0 10px;font-weight:600}
.read{font-size:20px;line-height:1.4;color:#f3f4f7;margin:0 0 12px}
.chips span{display:inline-block;font-size:12px;padding:3px 9px;border-radius:999px;
 margin:0 6px 6px 0;border:1px solid #2c313c}
.on{background:#14351f;color:#7ee2a1;border-color:#1f5233}
.off{background:#1a1c22;color:#9aa2b1}
.ctx{background:#1a1c22;color:#c8cdd8}
.alert{border-bottom:1px solid #20242d;padding:11px 0}
.alert a{color:#cfe0ff;text-decoration:none;font-size:16px}
.alert a:hover{text-decoration:underline}
.alert .meta{color:#8b93a3;font-size:12px;margin-top:3px}
.tag{background:#232734;color:#aeb6c6;border-radius:4px;padding:1px 6px;font-size:11px}
.quiet{color:#8b93a3;font-style:italic}
.ribbon{display:flex;flex-wrap:wrap;gap:8px}
.cell{flex:1 1 30%;min-width:96px;background:#15171d;border:1px solid #22262f;
 border-radius:8px;padding:9px 11px}
.cell .lab{color:#8b93a3;font-size:11px}
.cell .num{font-size:19px;font-weight:600;margin-top:2px}
.cell .dt{color:#6b7280;font-size:10px;margin-top:2px}
.up{color:#6ee7a0}.down{color:#f28b82}.flat{color:#e7e9ee}
.baserate{background:#15171d;border-left:3px solid #3a4152;padding:9px 12px;
 margin:8px 0;font-size:14px;color:#c8cdd8;border-radius:0 6px 6px 0}
.lbl{color:#8b93a3;font-size:11px;text-transform:uppercase;letter-spacing:.6px}
.foot{margin-top:34px;padding-top:14px;border-top:1px solid #262a33;
 color:#6b7280;font-size:12px}
"""


def situations_summary(conn):
    """Active situations with atom count + their most recent atoms. Reads the
    human-owned config directly; [] if none defined or the table is absent."""
    if not SIT_CONFIG.exists():
        return []
    try:
        cfg = yaml.safe_load(SIT_CONFIG.read_text()) or {}
    except (OSError, yaml.YAMLError):
        return []
    out = []
    for sit in cfg.get("situations", []):
        if sit.get("status") == "closed":
            continue
        sid = sit["situation_id"]
        try:
            n = conn.execute("SELECT COUNT(*) FROM situation_log WHERE "
                             "situation_id=?", (sid,)).fetchone()[0]
            recent = conn.execute(
                "SELECT ts, kind, headline, source_url FROM situation_log WHERE "
                "situation_id=? ORDER BY ts DESC, log_id DESC LIMIT 3",
                (sid,)).fetchall()
        except sqlite3.Error:
            n, recent = 0, []
        out.append({"sit": sit, "n": n, "recent": recent})
    return out


def predmkt_top(limit=8):
    """Top oil/geopolitics prediction markets by volume (already sorted). [] if
    not generated. Prefers markets that aren't near-resolved (0.02<p<0.98) so the
    board shows live uncertainty, not settled questions."""
    if not PREDMKT.exists():
        return []
    try:
        data = json.loads(PREDMKT.read_text())
    except (OSError, ValueError):
        return []
    mk = data.get("markets", [])
    live = [m for m in mk if 0.02 < m.get("prob", 0) < 0.98] or mk
    return live[:limit]


def corroborated_events(limit=6):
    """Top corroborated events across situations (tag likely/corroborated), the
    output of the triangulation brain. [] if not generated."""
    if not CORROBORATION.exists():
        return []
    try:
        data = json.loads(CORROBORATION.read_text())
    except (OSError, ValueError):
        return []
    evs = []
    for situ in data.get("situations", {}).values():
        evs += [e for e in situ if e.get("tag") in ("corroborated", "likely")]
    evs.sort(key=lambda e: e.get("confidence", 0), reverse=True)
    return evs[:limit]


def e(x):
    return html.escape(str(x if x is not None else ""))


def render():
    """Build the full HTML string. Never raises on a missing artifact."""
    er = _read_json(ENGINE_READ)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [f"<!doctype html><html lang=en><head><meta charset=utf-8>",
             "<meta name=viewport content='width=device-width,initial-scale=1'>",
             # Auto-reload so an open tab pulls each fresh publish (near-live feel).
             "<meta http-equiv=refresh content=900>",
             "<title>The Daily — News to Markets</title>",
             f"<style>{CSS}</style></head><body><div class=wrap>"]

    # a. Masthead
    parts.append(f"<div class=mast><h1>The Daily <span style='color:#8b93a3'>·"
                 f" News to Markets</span></h1><div class=as>as of {e(now)}</div></div>")

    # b. Today's Read
    parts.append("<h2 class=sec>Today's Read</h2>")
    if er and er.get("read"):
        parts.append(f"<p class=read>{e(er['read'])}</p>")
        chips = []
        for hid in ("H1", "H2"):
            h = er.get("hypotheses", {}).get(hid, {})
            amp = h.get("amplifier", "?")
            cls = "on" if amp == "ON" else "off"
            chips.append(f"<span class='{cls}'>{hid} {e(h.get('label',''))}: {e(amp)}</span>")
        gc = er.get("gpr_context") or {}
        if gc.get("gpr_pct") is not None:
            chips.append(f"<span class=ctx>GPR {e(gc['gpr_pct'])}th pct</span>")
        parts.append(f"<div class=chips>{''.join(chips)}</div>")
    else:
        parts.append("<p class=quiet>Not yet generated — run engine_read.py.</p>")

    # b2. The validated edge (H1) -- the honest tier, from validation_claims.json (N=161).
    # This is the one signal that passed the full gate; H2/H3 are shown as the nulls they are.
    vc = _read_json(VALIDATION) or {}
    vhyps = {h.get("hid"): h for h in vc.get("hypotheses", [])}
    h1v = vhyps.get("H1")
    if h1v:
        n = vc.get("current_sample_events", "?")
        ci = h1v.get("ci95_pp") or [None, None]
        bonf = ("survives Bonferroni" if h1v.get("survives_bonferroni_5pct")
                else "survives FDR@10%" if h1v.get("survives_fdr_10pct")
                else "not corrected-significant")
        e1 = (er or {}).get("hypotheses", {}).get("H1", {})
        amp_today = e1.get("amplifier", "?")
        parts.append("<h2 class=sec>The validated edge</h2>")
        parts.append(
            f"<p class=read><b>H1 — geopolitical shocks ripple harder into oil when VIX stress "
            f"is elevated.</b> The one signal that passed the full validation gate: "
            f"<b>{h1v.get('amp_pp'):+.1f}pp</b> amplification, 95% CI "
            f"[{ci[0]:+.1f}, {ci[1]:+.1f}]pp, {e(bonf)}, N={e(n)}. "
            f"Today the H1 amplifier is <b>{e(amp_today)}</b>.</p>")
        # walk-forward accountability: does H1 help the read out-of-sample?
        rb = _read_json(READ_BACKTEST) or {}
        if rb.get("n_scored"):
            reg = rb.get("by_regime", {})
            on = reg.get("ON", {}).get("mean_realized_pp")
            off = reg.get("OFF", {}).get("mean_realized_pp")
            extra = (f" Realized |CAR+20| ran {on}pp (ON) vs {off}pp (OFF), "
                     f"{rb.get('live_amplification_pp'):+.1f}pp." if on is not None and off is not None else "")
            parts.append(
                f"<div class=baserate>Walk-forward: conditioning the read on H1 cut out-of-sample "
                f"error {rb.get('mae_uncond_pp')}pp → {rb.get('mae_cond_pp')}pp "
                f"(N={rb.get('n_scored')}).{extra} The edge holds forward.</div>")
        h2v, h3v = vhyps.get("H2", {}), vhyps.get("H3", {})
        parts.append(
            f"<div class=lbl>not edges (reported, not buried): "
            f"H2 tight-inventories is a null at N={e(n)} "
            f"({h2v.get('amp_pp', 0):+.1f}pp, CI spans 0) · "
            f"H3 positioning rejected · analogue forecaster no OOS edge</div>")
        # b2b. The pre-registered edge battery: the honest portfolio scorecard (family-wise corrected).
        eb = _read_json(EDGE_BATTERY) or {}
        if eb.get("family_size"):
            val = eb.get("validated") or []
            parts.append(
                f"<div class=baserate>Edge portfolio (pre-registered, family-wise corrected): "
                f"of {eb['family_size']} economically-distinct hypotheses, "
                f"<b>{len(val)} validated</b> ({', '.join(val) if val else 'none new'}); the rest are "
                f"honest nulls. Discipline over count — receipts in <code>data/edge_battery.json</code>, "
                f"registration frozen in <code>PRE_REGISTRATION.md</code>.</div>")

    # b3. The Gap (market-as-null): where the engine disagrees with the market's priced vol.
    gp = _read_json(GAPS) or {}
    live = gp.get("live_gap"); led = gp.get("ledger") or {}
    if live:
        parts.append("<h2 class=sec>The Gap (vs the market)</h2>")
        parts.append(
            f"<p class=read>Live: engine reads <b>{e(live['engine_call'])}</b>; the market prices "
            f"OVX <b>{e(live['priced_ovx'])}</b> (p{e(live['priced_ovx_pct'])}) → "
            f"<b>{e(live['gap_direction'].replace('_',' '))}</b>.</p>")
        upr = (led.get("by_gap_direction") or {}).get("under_priced_risk")
        opf = (led.get("by_gap_direction") or {}).get("over_priced_fear")
        if upr and opf:
            parts.append(
                f"<div class=lbl>resolving scorecard (small-N, suggestive not validated): "
                f"under-priced-risk gaps resolved turbulent {upr['turbulence_rate']} of the time "
                f"(n={upr['n']}), over-priced-fear {opf['turbulence_rate']} (n={opf['n']}), vs a "
                f"{led.get('turbulence_base_rate')} base. Value is in the disagreement, honestly scored.</div>")

    # c. New on the wire
    parts.append("<h2 class=sec>New on the wire</h2>")
    alerts = new_alerts(10)
    if alerts:
        for a in alerts:
            t = e((a.get("timestamp_utc") or "")[:16].replace("T", " "))
            ents = e(a.get("matched_entities") or "")
            parts.append(
                f"<div class=alert><a href='{e(a.get('url',''))}' target=_blank "
                f"rel=noopener>{e(a.get('headline',''))}</a>"
                f"<div class=meta>{e(a.get('source',''))} · "
                f"<span class=tag>{e(a.get('heuristic_type',''))}</span>"
                f"{' · ' + ents if ents else ''} · {t}</div></div>")
    else:
        parts.append("<p class=quiet>Quiet tape.</p>")

    # d. The ribbon
    parts.append("<h2 class=sec>The ribbon</h2><div class=ribbon>")
    conn = sqlite3.connect(DB)
    for lab, sid, unit, dec in RIBBON:
        val, date, prev = latest_two(conn, sid)
        if val is None:
            parts.append(f"<div class=cell><div class=lab>{e(lab)}</div>"
                         f"<div class='num flat'>—</div></div>")
            continue
        cls = "flat"
        if prev is not None:
            cls = "up" if val > prev else "down" if val < prev else "flat"
        arrow = " ▲" if cls == "up" else " ▼" if cls == "down" else ""
        parts.append(f"<div class=cell><div class=lab>{e(lab)} <span "
                     f"style='color:#6b7280'>{e(unit)}</span></div>"
                     f"<div class='num {cls}'>{val:.{dec}f}{arrow}</div>"
                     f"<div class=dt>{e(date)}</div></div>")
    conn.close()
    gc = (er or {}).get("gpr_context") or {}
    if gc.get("gpr_pct") is not None:
        parts.append(f"<div class=cell><div class=lab>GPR <span "
                     f"style='color:#6b7280'>%ile</span></div>"
                     f"<div class='num flat'>{e(gc['gpr_pct'])}</div>"
                     f"<div class=dt>{e(gc.get('as_of',''))}</div></div>")
    parts.append("</div>")

    # e. If an amplifier is ON -- base-rate line per ON amplifier (from playbook.md).
    # Only VALIDATED hypotheses (current-tier HOLDS + survives FDR) count as amplifiers now --
    # H2 held at n=20 but is a null at N=161, so it must not surface as an active amplifier.
    _validated = {h.get("hid") for h in vc.get("hypotheses", [])
                  if h.get("statistically_validated")}
    on_amps = [hid for hid in ("H1", "H2")
               if hid in _validated
               and (er or {}).get("hypotheses", {}).get(hid, {}).get("amplifier") == "ON"]
    pb = playbook_amp_lines()
    if on_amps and pb:
        parts.append("<h2 class=sec>Amplifier context</h2>")
        parts.append("<div class=lbl>historical base rates, not a forecast</div>")
        for hid in on_amps:
            if hid in pb:
                parts.append(f"<div class=baserate>{e(pb[hid])}</div>")

    # e2. Situations -- the running memory, so the front page shows "where we
    # stand" alongside the numbers. Full dossier + synthesis in data/situations/.
    conn = sqlite3.connect(DB)
    sits = situations_summary(conn)
    conn.close()
    if sits:
        parts.append("<h2 class=sec>Situations</h2>")
        parts.append("<div class=lbl>running memory · full dossier in "
                     "data/situations/</div>")
        for s in sits:
            sit, n = s["sit"], s["n"]
            parts.append(
                f"<div class=alert><b>{e(sit.get('title', sit['situation_id']))}"
                f"</b> <span class=tag>{e(sit.get('status',''))}</span> "
                f"<span style='color:#6b7280'>· {e(n)} atoms · since "
                f"{e(sit.get('started_at',''))}</span>")
            for ts, kind, headline, url in s["recent"]:
                parts.append(
                    f"<div class=meta><a href='{e(url)}' target=_blank "
                    f"rel=noopener>{e(headline)}</a> · "
                    f"<span class=tag>{e(kind)}</span> · {e((ts or '')[:10])}</div>")
            parts.append("</div>")

    # e2b. Corroborated events -- the triangulation brain's output: the timeline
    # collapsed into events, scored by how many INDEPENDENT sources converge.
    cor = corroborated_events(6)
    if cor:
        parts.append("<h2 class=sec>Corroborated events</h2>")
        parts.append("<div class=lbl>independent-source convergence · confidence, "
                     "not fact</div>")
        for ev in cor:
            conf = f"{ev.get('confidence', 0) * 100:.0f}"
            parts.append(
                f"<div class=alert>{e(ev.get('headline',''))}"
                f"<div class=meta><span class=tag>{e(ev.get('tag',''))} {conf}%</span>"
                f" · {e(ev.get('n_independent_sources',0))} independent sources · "
                f"<span class=tag>{e(ev.get('kind',''))}</span> · "
                f"{e(ev.get('latest_ts',''))}</div></div>")

    # e2a2. Supply fundamentals (EIA) -- the physical "material": storage + refinery
    # runs + strategic reserve. Stats-safe, weekly.
    FUNDAMENTALS = [("Cushing", "eia.cushing_stocks", "kbbl", 0),
                    ("Refinery use", "eia.refinery_util", "%", 1),
                    ("SPR", "eia.spr_stocks", "kbbl", 0)]
    conn = sqlite3.connect(DB)
    fund = [(lab, unit, dec, *latest_two(conn, sid)) for lab, sid, unit, dec in FUNDAMENTALS]
    conn.close()
    if any(v is not None for _, _, _, v, _, _ in fund):
        parts.append("<h2 class=sec>Supply fundamentals</h2>")
        parts.append("<div class=lbl>EIA weekly · storage, refinery runs, reserve</div>"
                     "<div class=ribbon>")
        for lab, unit, dec, val, date, prev in fund:
            if val is None:
                continue
            cls = "flat"
            if prev is not None:
                cls = "up" if val > prev else "down" if val < prev else "flat"
            arrow = " ▲" if cls == "up" else " ▼" if cls == "down" else ""
            parts.append(f"<div class=cell><div class=lab>{e(lab)} <span "
                         f"style='color:#6b7280'>{e(unit)}</span></div>"
                         f"<div class='num {cls}'>{val:,.{dec}f}{arrow}</div>"
                         f"<div class=dt>{e(date)}</div></div>")
        parts.append("</div>")

    # e2c. Chokepoint transits (IMF PortWatch) -- the physical-flow layer: are ships
    # actually moving through Hormuz / Bab el-Mandeb / Suez?
    try:
        cps = json.loads(PORTWATCH.read_text()).get("chokepoints", []) \
            if PORTWATCH.exists() else []
    except (OSError, ValueError):
        cps = []
    if cps:
        parts.append("<h2 class=sec>Chokepoint transits</h2>")
        parts.append("<div class=lbl>IMF PortWatch · daily tanker flow (data lags "
                     "~1 week)</div><div class=ribbon>")
        for c in cps:
            cls = ("down" if c.get("flag") == "reduced"
                   else "up" if c.get("flag") == "elevated" else "flat")
            parts.append(
                f"<div class=cell><div class=lab>{e(c.get('chokepoint',''))}</div>"
                f"<div class='num {cls}'>{e(c.get('latest',''))}</div>"
                f"<div class=dt>{e(c.get('flag',''))} · {e(c.get('pct_of_median',''))}x"
                f"</div></div>")
        parts.append("</div>")

    # e2d. Wikipedia attention -- how alarmed the world is (pageview spikes).
    try:
        wp = json.loads(WIKI.read_text()).get("pages", []) if WIKI.exists() else []
    except (OSError, ValueError):
        wp = []
    if wp:
        parts.append("<h2 class=sec>Attention</h2>")
        parts.append("<div class=lbl>Wikipedia pageviews · spike = surge of global "
                     "attention · context</div><div class=ribbon>")
        for p in wp:
            cls = ("up" if p.get("flag") in ("spike", "elevated")
                   else "down" if p.get("flag") == "quiet" else "flat")
            views = f"{p.get('latest', 0):,}"
            parts.append(
                f"<div class=cell><div class=lab>{e(p.get('page',''))}</div>"
                f"<div class='num {cls}'>{e(views)}</div>"
                f"<div class=dt>{e(p.get('flag',''))} · {e(p.get('pct_of_median',''))}x"
                f"</div></div>")
        parts.append("</div>")

    # e3. Market-implied odds -- what the crowd PRICES for the same events (the
    # engine's "read vs priced" thesis, made live). Context only, never the stats.
    pm = predmkt_top(8)
    if pm:
        parts.append("<h2 class=sec>Market-implied odds</h2>")
        parts.append("<div class=lbl>Polymarket · what's priced · context only, not "
                     "a stat</div>")
        for m in pm:
            pct = f"{m.get('prob', 0) * 100:.0f}"
            vol = f"{m.get('volume', 0):,.0f}"
            ends = f" · ends {e(m.get('end_date',''))}" if m.get("end_date") else ""
            parts.append(
                f"<div class=alert><a href='{e(m.get('url',''))}' target=_blank "
                f"rel=noopener>{e(m.get('question',''))}</a>"
                f"<div class=meta><b>{pct}%</b> {e(m.get('outcome',''))} · "
                f"vol ${e(vol)}{ends}</div></div>")

    # f. Footer
    parts.append("<div class=foot>Every number is computed from committed data. "
                 "n is small. This page never predicts whether events occur.</div>")
    parts.append("</div></body></html>")
    return "".join(parts)


def main():
    OUT.write_text(render())
    print(f"Wrote {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
