"""Big Moves page — the market-defined significance screen, built from real data.

Reads data/big_moves/<asset>.json (produced under BIG_MOVES_REGISTRATION.md) and
writes src/big_moves.html with the data embedded, so the page opens from disk or
is served by the backend. Nothing here computes; it only renders what the
registered pipeline produced. Every number on the page traces to those files.
"""
import json, pathlib, datetime as dt

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ["brent", "wti", "diesel_crack"]
data = {a: json.load(open(ROOT / "data" / "big_moves" / f"{a}.json")) for a in ASSETS}
TYPE_LABEL = {"policy_response": "Policy response", "demand_shock": "Demand shock", "opec_decision": "OPEC decision",
              "conflict_escalation": "Conflict escalation", "chokepoint_disruption": "Chokepoint disruption",
              "sanctions": "Sanctions", "infrastructure_attack": "Infrastructure attack"}

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ripple Engine — Big moves</title>
<style>
:root{{--bg:#0f1114;--s1:#161a1f;--s2:#1d2228;--line:#2a3038;--line2:#3a424c;--t:#e8e6e1;--t2:#a9a69f;--t3:#6f6d67;--up:#e0653a;--dn:#3fbf95;--warn:#e0a33a;--mono:ui-monospace,Menlo,Consolas,monospace}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--t);font:14px/1.5 -apple-system,Inter,Segoe UI,Helvetica,Arial,sans-serif}}
.top{{display:flex;align-items:center;gap:20px;padding:10px 22px;border-bottom:1px solid var(--line)}}.brand{{font-weight:600}}.brand small{{color:var(--t3);font-weight:400;margin-left:8px}}
.nav{{display:flex;gap:4px}}.nav span{{color:var(--t2);padding:6px 12px;border-radius:6px}}.nav span.on{{color:var(--t);background:var(--s2)}}
main{{max-width:1240px;margin:0 auto;padding:18px 22px 60px}}h1{{font-size:22px;font-weight:500;margin:0 0 4px}}h2{{font-size:12px;font-weight:500;color:var(--t3);text-transform:uppercase;letter-spacing:.6px;margin:18px 0 10px}}
.muted{{color:var(--t2)}}.dim{{color:var(--t3)}}.mono{{font-family:var(--mono);font-size:12.5px}}
.card{{background:var(--s1);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.tabs{{display:flex;gap:6px;margin:14px 0}}.tabs button{{background:var(--s1);border:1px solid var(--line);color:var(--t2);padding:6px 12px;border-radius:6px;cursor:pointer;font:inherit}}.tabs button.on{{color:var(--t);border-color:var(--line2);background:var(--s2)}}
.stats{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}}.stats .card .v{{font-size:22px;font-weight:500}}.stats .card .l{{font-size:12px;color:var(--t2)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}th{{text-align:left;color:var(--t3);font-weight:500;font-size:12px;padding:6px 8px;border-bottom:1px solid var(--line2)}}td{{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
.up{{color:var(--up)}}.dn{{color:var(--dn)}}.noev{{color:var(--t3);font-style:italic}}.ant{{color:var(--warn);font-family:var(--mono);font-size:11px;margin-left:4px}}
.two{{display:grid;grid-template-columns:3fr 2fr;gap:16px}}
.bar{{height:8px;background:var(--s2);border-radius:3px;position:relative;margin-top:4px}}.bar i{{position:absolute;left:0;top:0;height:100%;border-radius:3px;background:var(--t2)}}.bar b{{position:absolute;top:-3px;width:2px;height:14px;background:var(--warn)}}
.legend{{font-size:12px;color:var(--t2);display:flex;gap:16px;margin:6px 0 0}}.legend i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}}
.note{{font-size:12.5px;color:var(--t2);border-left:2px solid var(--line2);padding:4px 12px;margin:10px 0}}
</style></head><body>
<div class="top"><div class="brand">Ripple Engine <small>the record, read live</small></div><div class="nav"><span>Feed</span><span>Story</span><span class="on">Big moves</span><span>Ledger</span></div>
<span class="mono dim" style="margin-left:auto">built {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC · data/big_moves/*.json · BIG_MOVES_REGISTRATION.md</span></div>
<main>
<h1>Big moves</h1>
<p class="muted" style="margin:0">Every time this market actually changed, and what was knowable while it did. Significance is defined here — by the top 5% of 20- and 60-day moves in each asset's own history — not by anyone's severity score.</p>
<div class="tabs" id="tabs"></div>
<div id="view"></div>
<h2>Definitions and disclosures</h2>
<div class="note">Episode = a cluster of dates whose trailing 20- or 60-day move is in the asset's top 5% (two-sided). Onset = the price extreme before the move; end = the date of the largest move. Attribution = every corpus event knowable between onset − 7 days and end, stamped with its lag from onset; lag over 20 days is marked <span class="ant">anticipated</span>: the market moved first. Registration and its two dated amendments are in <span class="mono">BIG_MOVES_REGISTRATION.md</span>. "Policy response" is endogenous by construction (OPEC cuts and SPR releases are reactions to moves) and is shown for completeness, not as a driver. "Attributed" means knowable in the window; causation is never asserted by the machine.</div>
</main>
<script>
const D={json.dumps(data)};
const LABEL={json.dumps(TYPE_LABEL)};
const tabs=document.getElementById('tabs'),view=document.getElementById('view');
Object.keys(D).forEach((a,i)=>{{const b=document.createElement('button');b.textContent=D[a].label;b.className=i?'':'on';b.onclick=()=>{{[...tabs.children].forEach(x=>x.className='');b.className='on';render(a)}};tabs.appendChild(b)}});
function fmt(e,kind){{return kind==='price'?`${{e.sign}}${{Math.abs(e.change).toFixed(0)}}%`:`${{e.sign}}$${{Math.abs(e.change).toFixed(1)}}`}}
function render(a){{const d=D[a];const eps=d.episodes;const kind=d.kind;
 const yrs=[];for(let y=1986;y<=2026;y+=4)yrs.push(y);
 const X=y=>30+(y-1986)*(1160/41);
 let svg=`<svg viewBox="0 0 1200 220" width="100%"><line x1="30" y1="120" x2="1190" y2="120" stroke="#3a424c"/>`;
 yrs.forEach(y=>svg+=`<text x="${{X(y)}}" y="212" font-size="10.5" fill="#6f6d67" text-anchor="middle">${{y}}</text><line x1="${{X(y)}}" y1="120" x2="${{X(y)}}" y2="126" stroke="#3a424c"/>`);
 const mx=Math.max(...eps.map(e=>Math.abs(e.change)));
 eps.forEach(e=>{{const y=+e.onset.slice(0,4)+(+e.onset.slice(5,7)-1)/12;const hh=Math.max(6,Math.abs(e.change)/mx*95);const up=e.sign==='+';
  const col=!e.events.length?'#6f6d67':(up?'#e0653a':'#3fbf95');
  svg+=`<rect x="${{X(y)-2.5}}" y="${{up?120-hh:120}}" width="5" height="${{hh}}" fill="${{col}}" rx="1"><title>${{e.onset}} → ${{e.end}}: ${{fmt(e,kind)}}\\n${{e.events.map(v=>v.title).join('\\n')||'no identified event'}}</title></rect>`;
  if(Math.abs(e.change)>0.45*mx) svg+=`<text x="${{X(y)}}" y="${{up?114-hh:134+hh}}" font-size="10" fill="#a9a69f" text-anchor="middle">${{e.onset.slice(0,4)}} ${{fmt(e,kind)}}</text>`;}});
 svg+='</svg>';
 const base=d.everyday_base_rate_pct;
 const stats=`<div class="stats"><div class="card"><div class="l">Episodes, ${{d.first.slice(0,4)}}–${{d.last.slice(0,4)}}</div><div class="v">${{d.n_episodes}}</div></div>
 <div class="card"><div class="l">No identified event in corpus</div><div class="v">${{d.no_identified_event}} <span class="dim" style="font-size:14px">(${{Math.round(100*d.no_identified_event/d.n_episodes)}}%)</span></div></div>
 <div class="card"><div class="l">Market moved before the catalyst</div><div class="v">${{eps.filter(e=>e.events.length&&e.events.every(v=>v.anticipated)).length}} <span class="dim" style="font-size:14px">episodes</span></div></div>
 <div class="card"><div class="l">Everyday base rate (any day inside a big-move window)</div><div class="v">${{base==null?'—':base+'%'}}</div></div></div>`;
 const pb=Object.entries(d.p_big_given_class).sort((x,y)=>y[1][0]/y[1][1]-x[1][0]/x[1][1]);
 const pbt=`<table><tr><th>Event class</th><th>Inside a big move</th><th>Rate</th><th style="width:34%">vs everyday ${{base==null?'':base+'%'}}</th></tr>`+pb.map(([t,[k,n]])=>{{const r=100*k/n;return `<tr><td>${{LABEL[t]||t}}${{t==='policy_response'?' <span class="ant">endogenous</span>':''}}</td><td class="mono">${{k}} of ${{n}}</td><td class="mono">${{r.toFixed(0)}}%</td><td><div class="bar"><i style="width:${{Math.min(100,r)}}%"></i>${{base==null?'':`<b style="left:${{Math.min(100,base)}}%"></b>`}}</div></td></tr>`}}).join('')+'</table>';
 const pc=Object.entries(d.p_class_given_big).sort((x,y)=>y[1][0]-x[1][0]);
 const pct=`<table><tr><th>Event class</th><th>Big moves with one</th><th>Share</th></tr>`+pc.map(([t,[k,n]])=>`<tr><td>${{LABEL[t]||t}}</td><td class="mono">${{k}} of ${{n}}</td><td class="mono">${{(100*k/n).toFixed(0)}}%</td></tr>`).join('')+`<tr><td class="noev">No identified event</td><td class="mono">${{d.no_identified_event}} of ${{d.n_episodes}}</td><td class="mono">${{(100*d.no_identified_event/d.n_episodes).toFixed(0)}}%</td></tr></table>`;
 const rows=eps.slice().reverse().map(e=>`<tr><td class="mono">${{e.onset}} → ${{e.end}}<div class="dim">${{e.days}}d</div></td><td class="mono ${{e.sign==='+'?'up':'dn'}}">${{fmt(e,kind)}}<div class="dim">${{kind==='price'?'$'+e.from_+' → $'+e.to:e.from_+' → '+e.to}}</div></td><td>${{e.events.length?e.events.map(v=>`<div>${{v.title}} <span class="dim mono">${{v.date}}</span>${{v.anticipated?`<span class="ant">anticipated ${{v.lag_days}}d</span>`:`<span class="dim mono" style="font-size:11px;margin-left:4px">${{v.lag_days>=0?'+':''}}${{v.lag_days}}d</span>`}}</div>`).join(''):'<span class="noev">No identified event — corpus gap or non-event move</span>'}}</td></tr>`).join('');
 view.innerHTML=`<div class="card">${{svg}}<div class="legend"><span><i style="background:#e0653a"></i>up, attributed</span><span><i style="background:#3fbf95"></i>down, attributed</span><span><i style="background:#6f6d67"></i>no identified event</span><span class="dim">hover a bar for its events</span></div></div>
 <h2>${{d.label}} — ${{d.series}}</h2>${{stats}}
 <div class="two" style="margin-top:16px"><div><h2>Which kinds of things sit inside big moves — P(big move | class)</h2>${{pbt}}<p class="dim" style="font-size:12px">Reading: a class whose bar clears the everyday marker is more often found inside a big move than any random day is. This is the materiality gate's input.</p></div>
 <div><h2>What has ever changed this market — P(class | big move)</h2>${{pct}}</div></div>
 <h2>Every episode, newest first</h2><div class="card" style="padding:0 8px"><table><tr><th style="width:190px">Onset → end</th><th style="width:120px">Move</th><th>Knowable during the move (lag from onset)</th></tr>${{rows}}</table></div>`;}}
render('brent');
</script></body></html>"""
out = ROOT / "src" / "big_moves.html"
out.write_text(html)
print(f"wrote {out} ({len(html)//1024} KB)")
