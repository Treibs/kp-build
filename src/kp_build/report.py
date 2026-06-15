"""Render a wikillm package as a self-contained, browsable HTML report — the HUMAN-facing view.

`CONTEXT.md` is the agent payload; this is the human one. One file, zero external dependencies
(inline CSS + vanilla JS), openable straight from `file://`. It shows:
  - the falsification scorecard (does the package actually help? base vs KP-loaded),
  - the verified citation spine (each paper linking out to arXiv / DOI),
  - the open-problems register, the debate map, the SOTA benchmark table, the claims, and
  - an interactive force-directed graph built from `index.json` (paper ↔ claim ↔ problem ↔ debate).

All package text is HTML-escaped (a loaded package is treated as data, never markup).
"""

from __future__ import annotations

import glob
import html
import json
from pathlib import Path

from .schema import (paper_from_md, claim_from_md, problem_from_md, debate_from_md,
                     benchmark_from_md)


def _esc(x) -> str:
    return html.escape(str(x), quote=True)


def _read_nodes(d: Path):
    def load(sub, fn):
        return [fn(Path(f).read_text(encoding="utf-8")) for f in sorted(glob.glob(str(d / sub / "*.md")))]
    return (load("papers", paper_from_md), load("claims", claim_from_md),
            load("open-problems", problem_from_md), load("debates", debate_from_md),
            load("benchmarks", benchmark_from_md))


def _paper_link(p) -> str:
    if p.arxiv_id:
        return f'https://arxiv.org/abs/{_esc(p.arxiv_id)}'
    if p.doi:
        return f'https://doi.org/{_esc(p.doi)}'
    return ""


def _bars(label, b, k) -> str:
    def row(name, val, cls):
        pct = 0 if val is None else round(val * 100)
        txt = "—" if val is None else f"{val:.2f}"
        return (f'<div class="bar-row"><span class="bar-name">{name}</span>'
                f'<span class="bar-track"><span class="bar-fill {cls}" style="width:{pct}%"></span></span>'
                f'<span class="bar-val">{txt}</span></div>')
    return (f'<div class="metric"><div class="metric-h">{_esc(label)}</div>'
            + row("base", b, "base") + row("KP", k, "kp") + '</div>')


def _scorecard(man: dict) -> str:
    f = man.get("falsification") or {}
    if not f.get("run"):
        return ('<section class="card muted"><h2>Falsification</h2>'
                '<p>Not run for this package. Run <code>kp-build falsify</code> to measure whether '
                'loading it beats unaided recall.</p></section>')
    b, k = f.get("base", {}), f.get("kp", {})
    verdict = str(f.get("verdict", ""))
    tone = "good" if "HELPS" in verdict else ("warn" if "TIE" in verdict else "bad")
    fakes = b.get("fake_list") or []
    fakes_html = ""
    if fakes:
        items = "".join(f"<li><code>{_esc(x)}</code></li>" for x in fakes)
        fakes_html = (f'<div class="fakes"><div class="fakes-h">Base agent mislabeled / fabricated '
                      f'({len(fakes)}) — caught by strict id↔title matching:</div><ul>{items}</ul></div>')
    return (f'<section class="card scorecard"><h2>Falsification — does the package help?</h2>'
            f'<div class="verdict {tone}">{_esc(verdict) or "(no verdict text)"}</div>'
            f'<div class="metrics">{_bars("precision", b.get("precision"), k.get("precision"))}'
            f'{_bars("recall (spine coverage)", b.get("recall"), k.get("recall"))}'
            f'{_bars("f1", b.get("f1"), k.get("f1"))}</div>'
            f'<div class="cov">base covered {_esc(b.get("spine_covered","?"))}/{_esc(b.get("spine_size","?"))} of the '
            f'verified spine; KP covered {_esc(k.get("spine_covered","?"))}/{_esc(k.get("spine_size","?"))}.</div>'
            f'{fakes_html}</section>')


def _spine(papers) -> str:
    rows = []
    for p in papers:
        ok = p.verified.exists
        link = _paper_link(p)
        ident = (p.arxiv_id and f"arXiv:{_esc(p.arxiv_id)}{_esc(p.arxiv_version)}") or (p.doi and f"doi:{_esc(p.doi)}") or "—"
        ident_html = f'<a href="{link}" target="_blank" rel="noopener">{ident}</a>' if link else ident
        yr = f" ({_esc(p.year)})" if p.year else ""
        badge = '<span class="pill ok">verified</span>' if ok else f'<span class="pill no">{_esc(p.verified.status)}</span>'
        rows.append(f'<li class="{"" if ok else "dim"}"><code class="key">{_esc(p.cite_key)}</code> '
                    f'<span class="ptitle">{_esc(p.title)}</span>{yr} {badge}<br>'
                    f'<span class="ident">{ident_html}</span></li>')
    return f'<section class="card"><h2>Verified citation spine <span class="count">{sum(1 for p in papers if p.verified.exists)}/{len(papers)}</span></h2><ul class="spine">{"".join(rows)}</ul></section>'


def _problems(problems, verified) -> str:
    if not problems:
        return '<section class="card"><h2>Open problems</h2><p class="muted">None surfaced — likely a coverage gap.</p></section>'
    cards = []
    for op in problems:
        flags = " ".join(f'<code class="key">{_esc(k)}</code>' for k in op.flagged_by if k in verified)
        cards.append(f'<div class="op"><div class="op-stmt">{_esc(op.statement)}</div>'
                     f'<div class="op-why"><b>Why it matters:</b> {_esc(op.why_it_matters)}</div>'
                     f'<div class="op-flags">flagged by {flags} <span class="pill st">{_esc(op.status)}</span></div></div>')
    return f'<section class="card"><h2>Open problems <span class="count">{len(problems)}</span></h2>{"".join(cards)}</section>'


def _debates(debates, verified) -> str:
    if not debates:
        return ""
    cards = []
    for db in debates:
        pos = []
        for p in db.positions:
            who = " ".join(f'<code class="key">{_esc(k)}</code>' for k in p.papers if k in verified)
            if who:
                pos.append(f'<div class="pos"><div class="pos-h">{_esc(p.stance)} {who}</div>'
                           f'<div class="pos-s">{_esc(p.summary)}</div></div>')
        res = ' <span class="pill ok">resolved</span>' if db.resolved else ""
        cards.append(f'<div class="debate"><div class="dq">{_esc(db.question)}{res}</div>{"".join(pos)}</div>')
    return f'<section class="card"><h2>Open debates <span class="count">{len(debates)}</span></h2>{"".join(cards)}</section>'


def _benchmarks(benchmarks, verified) -> str:
    bs = [b for b in benchmarks if b.paper in verified]
    if not bs:
        return ""
    rows = "".join(f'<tr><td>{_esc(b.method)}</td><td>{_esc(b.dataset)}</td><td>{_esc(b.metric)}</td>'
                   f'<td class="num">{_esc(b.value)}</td><td><code class="key">{_esc(b.paper)}</code></td></tr>' for b in bs)
    return (f'<section class="card"><h2>Reported results (SOTA snapshot) <span class="count">{len(bs)}</span></h2>'
            f'<table class="sota"><thead><tr><th>method</th><th>dataset</th><th>metric</th><th>value</th><th>paper</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></section>')


def _claims(claims, verified) -> str:
    cs = [c for c in claims if c.paper in verified]
    if not cs:
        return ""
    order = {"result": 0, "finding": 1, "method": 2, "definition": 3}
    cs.sort(key=lambda c: order.get(c.claim_type, 9))
    types = sorted({c.claim_type for c in cs})
    chips = '<button class="chip active" data-t="all">all</button>' + "".join(
        f'<button class="chip" data-t="{_esc(t)}">{_esc(t)}</button>' for t in types)
    items = []
    for c in cs:
        corr = [k for k in c.corroborated_by if k in verified]
        meta = f'<code class="key">{_esc(c.paper)}</code> · {_esc(c.confidence)}'
        if corr:
            meta += f' · corroborated×{len(corr)}'
        passage = f'<blockquote>{_esc(c.supporting_passage)}</blockquote>' if c.supporting_passage else ""
        items.append(f'<div class="claim" data-t="{_esc(c.claim_type)}"><span class="tag t-{_esc(c.claim_type)}">{_esc(c.claim_type)}</span>'
                     f'<div class="cstmt">{_esc(c.statement)}</div>{passage}<div class="cmeta">{meta}</div></div>')
    return (f'<section class="card"><h2>Claims <span class="count">{len(cs)}</span></h2>'
            f'<div class="chips">{chips}</div><div id="claims">{"".join(items)}</div></section>')


def _graph_data(index: dict, verified: set) -> dict:
    kinds = [("papers", "paper", "cite_key"), ("claims", "claim", "id"),
             ("open_problems", "problem", "id"), ("debates", "debate", "id"),
             ("benchmarks", "benchmark", "id")]
    nodes, ids = [], set()
    for key, typ, idf in kinds:
        for n in index.get(key, []):
            nid = n.get(idf)
            if typ == "paper" and not n.get("verified"):
                continue
            if nid and nid not in ids:
                ids.add(nid)
                label = nid if typ != "paper" else nid
                nodes.append({"id": nid, "type": typ, "label": label,
                              "title": n.get("title", "") if typ == "paper" else ""})
    edges = [{"from": e["from"], "to": e["to"], "rel": e.get("rel", "")}
             for e in index.get("edges", []) if e.get("from") in ids and e.get("to") in ids]
    return {"nodes": nodes, "edges": edges}


def build_report(pkg_dir: str | Path) -> str:
    d = Path(pkg_dir)
    man = json.loads((d / "wikillm.json").read_text(encoding="utf-8"))
    know = json.loads((d / "knowledge.json").read_text(encoding="utf-8")) if (d / "knowledge.json").is_file() else {}
    index = json.loads((d / "index.json").read_text(encoding="utf-8")) if (d / "index.json").is_file() else {}
    papers, claims, problems, debates, benchmarks = _read_nodes(d)
    verified = {p.cite_key for p in papers if p.verified.exists}

    s = man.get("stats", {})
    sp = man.get("source_span", {})
    span = f"{sp.get('oldest')}–{sp.get('newest')}" if sp.get("oldest") else "n/a"
    name = know.get("name", "@kp/?")
    chips = "".join(f'<span class="chip-meta">{_esc(t)}</span>' for t in [
        f"{name}@{know.get('version','?')}", f"built {man.get('built','?')}",
        f"{s.get('papers_verified','?')}/{s.get('papers_total','?')} verified",
        f"source years {span}"])
    counts = "".join(f'<div class="stat"><b>{_esc(v)}</b><span>{lbl}</span></div>' for v, lbl in [
        (s.get("papers_verified", 0), "papers"), (s.get("claims", 0), "claims"),
        (s.get("open_problems", 0), "open problems"), (s.get("debates", 0), "debates"),
        (s.get("benchmarks", 0), "benchmarks")])

    gdata = json.dumps(_graph_data(index, verified)).replace("</", "<\\/")
    body = (
        _scorecard(man)
        + f'<section class="card"><div class="stats">{counts}</div></section>'
        + '<section class="card"><h2>Package graph</h2><div class="ghint">drag nodes · hover for titles · '
          '<span class="lg paper">paper</span><span class="lg claim">claim</span>'
          '<span class="lg problem">problem</span><span class="lg debate">debate</span>'
          '<span class="lg benchmark">benchmark</span></div><div id="graph"></div></section>'
        + _spine(papers) + _problems(problems, verified) + _debates(debates, verified)
        + _benchmarks(benchmarks, verified) + _claims(claims, verified)
    )

    return (_TEMPLATE
            .replace("__TITLE__", _esc(man.get("topic", "wikillm package")))
            .replace("__SCOPE__", _esc(man.get("scope", "")))
            .replace("__CHIPS__", chips)
            .replace("__BODY__", body)
            .replace("__GRAPH__", gdata))


_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — wikillm report</title>
<style>
:root{--ink:#1a1c22;--mut:#6b7280;--line:#e6e8ee;--bg:#f6f7f9;--card:#fff;--acc:#4f46e5;
--paper:#4f46e5;--claim:#0d9488;--problem:#d97706;--debate:#9333ea;--benchmark:#2563eb;
--good:#16a34a;--warn:#d97706;--bad:#dc2626;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px 80px}
header{background:linear-gradient(135deg,#312e81,#4f46e5);color:#fff;padding:34px 20px 30px;margin-bottom:22px}
header .wrap{padding-bottom:0}h1{margin:0 0 6px;font-size:26px;line-height:1.2}
.scope{color:#dfe0fb;max-width:820px;margin:0 0 14px}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chip-meta{background:rgba(255,255,255,.16);border-radius:99px;padding:3px 11px;font-size:12.5px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:0 0 18px;box-shadow:0 1px 2px rgba(20,20,40,.04)}
.card.muted{color:var(--mut)}h2{margin:0 0 14px;font-size:17px;display:flex;align-items:center;gap:9px}
.count{background:var(--bg);color:var(--mut);border:1px solid var(--line);border-radius:99px;font-size:12px;padding:1px 9px;font-weight:600}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em}
.key{background:#eef0fb;color:var(--acc);border-radius:5px;padding:1px 6px}
/* scorecard */
.verdict{font-weight:700;padding:10px 14px;border-radius:9px;margin-bottom:16px}
.verdict.good{background:#dcfce7;color:#14532d}.verdict.warn{background:#fef3c7;color:#7c2d12}.verdict.bad{background:#fee2e2;color:#7f1d1d}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.metric-h{font-size:12.5px;color:var(--mut);font-weight:600;margin-bottom:6px;text-transform:uppercase;letter-spacing:.03em}
.bar-row{display:flex;align-items:center;gap:8px;margin:4px 0}.bar-name{width:34px;font-size:12px;color:var(--mut)}
.bar-track{flex:1;background:var(--bg);border-radius:99px;height:10px;overflow:hidden;border:1px solid var(--line)}
.bar-fill{display:block;height:100%}.bar-fill.base{background:#cbd5e1}.bar-fill.kp{background:var(--acc)}
.bar-val{width:36px;text-align:right;font-size:12.5px;font-variant-numeric:tabular-nums}
.cov{color:var(--mut);font-size:13px;margin-top:12px}
.fakes{margin-top:14px;background:#fff7ed;border:1px solid #fed7aa;border-radius:9px;padding:10px 14px}
.fakes-h{font-size:13px;font-weight:600;color:#9a3412;margin-bottom:6px}.fakes ul{margin:0;padding-left:18px}.fakes li{margin:3px 0;font-size:12.5px}
/* stats */
.stats{display:flex;flex-wrap:wrap;gap:26px}.stat{display:flex;flex-direction:column}.stat b{font-size:24px}.stat span{color:var(--mut);font-size:12.5px}
/* spine */
ul.spine{list-style:none;margin:0;padding:0}ul.spine li{padding:9px 0;border-bottom:1px solid var(--line)}ul.spine li:last-child{border:0}
ul.spine li.dim{opacity:.55}.ptitle{font-weight:600}.ident{color:var(--mut);font-size:12.5px}.ident a{color:var(--benchmark);text-decoration:none}.ident a:hover{text-decoration:underline}
.pill{font-size:11px;border-radius:99px;padding:1px 8px;vertical-align:middle}.pill.ok{background:#dcfce7;color:#15803d}.pill.no{background:#fee2e2;color:#b91c1c}.pill.st{background:var(--bg);color:var(--mut);border:1px solid var(--line)}
/* problems / debates */
.op{padding:11px 0;border-bottom:1px solid var(--line)}.op:last-child{border:0}.op-stmt{font-weight:600;margin-bottom:4px}
.op-why{color:#374151;font-size:13.5px;margin-bottom:5px}.op-flags{color:var(--mut);font-size:12.5px}
.debate{padding:12px 0;border-bottom:1px solid var(--line)}.debate:last-child{border:0}.dq{font-weight:600;margin-bottom:8px}
.pos{border-left:3px solid var(--debate);padding:2px 0 2px 12px;margin:7px 0}.pos-h{font-size:13px;font-weight:600}.pos-s{font-size:13px;color:#374151}
/* benchmarks */
table.sota{width:100%;border-collapse:collapse;font-size:13px}table.sota th{text-align:left;color:var(--mut);font-weight:600;border-bottom:2px solid var(--line);padding:6px 8px}
table.sota td{border-bottom:1px solid var(--line);padding:6px 8px}td.num{font-weight:600;font-variant-numeric:tabular-nums}
/* claims */
.chips{margin-bottom:12px}.chip{background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:3px 12px;font-size:12.5px;cursor:pointer;color:var(--mut)}
.chip.active{background:var(--acc);color:#fff;border-color:var(--acc)}
.claim{padding:11px 0;border-bottom:1px solid var(--line)}.claim:last-child{border:0}
.tag{font-size:11px;border-radius:5px;padding:1px 7px;color:#fff;text-transform:uppercase;letter-spacing:.03em}
.t-result{background:var(--claim)}.t-finding{background:var(--benchmark)}.t-method{background:var(--debate)}.t-definition{background:var(--mut)}
.cstmt{margin:6px 0 0}.claim blockquote{margin:6px 0 0;padding:5px 12px;border-left:3px solid var(--line);color:#374151;font-size:13px;background:var(--bg);border-radius:0 6px 6px 0}
.cmeta{color:var(--mut);font-size:12.5px;margin-top:5px}
/* graph */
.ghint{color:var(--mut);font-size:12.5px;margin-bottom:8px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.lg{display:inline-flex;align-items:center;gap:5px}.lg::before{content:"";width:10px;height:10px;border-radius:99px;display:inline-block}
.lg.paper::before{background:var(--paper)}.lg.claim::before{background:var(--claim)}.lg.problem::before{background:var(--problem)}.lg.debate::before{background:var(--debate)}.lg.benchmark::before{background:var(--benchmark)}
#graph{width:100%;height:520px;border:1px solid var(--line);border-radius:9px;background:#fcfcfd;cursor:grab}
.footer{color:var(--mut);font-size:12px;text-align:center;margin-top:10px}
</style></head>
<body>
<header><div class="wrap"><h1>__TITLE__</h1><p class="scope">__SCOPE__</p><div class="chips">__CHIPS__</div></div></header>
<div class="wrap">__BODY__
<div class="footer">Generated by kp-build · a wikillm knowledge package · confidence is corpus-relative</div></div>
<script>
// claims filter
document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));c.classList.add('active');
  const t=c.dataset.t;document.querySelectorAll('.claim').forEach(el=>{el.style.display=(t==='all'||el.dataset.t===t)?'':'none';});
});
// force-directed graph (self-contained)
const G=__GRAPH__;
(function(){
  const el=document.getElementById('graph');if(!el||!G.nodes.length)return;
  const W=el.clientWidth||900,H=520,COL={paper:'#4f46e5',claim:'#0d9488',problem:'#d97706',debate:'#9333ea',benchmark:'#2563eb'};
  const NS='http://www.w3.org/2000/svg',svg=document.createElementNS(NS,'svg');
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width','100%');svg.setAttribute('height',H);el.appendChild(svg);
  const N=G.nodes.map((n,i)=>({...n,x:W/2+Math.cos(i)*180+(i%7)*9,y:H/2+Math.sin(i)*150+(i%5)*9,vx:0,vy:0}));
  const idx={};N.forEach((n,i)=>idx[n.id]=i);
  const E=G.edges.map(e=>({s:idx[e.from],t:idx[e.to]})).filter(e=>e.s!=null&&e.t!=null);
  const deg={};E.forEach(e=>{deg[e.s]=(deg[e.s]||0)+1;deg[e.t]=(deg[e.t]||0)+1;});
  for(let it=0;it<320;it++){
    for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++){
      let dx=N[i].x-N[j].x,dy=N[i].y-N[j].y,d2=dx*dx+dy*dy||1,f=2600/d2,d=Math.sqrt(d2);
      dx/=d;dy/=d;N[i].vx+=dx*f;N[i].vy+=dy*f;N[j].vx-=dx*f;N[j].vy-=dy*f;}
    E.forEach(e=>{let a=N[e.s],b=N[e.t],dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)||1,f=(d-70)*0.02;
      dx/=d;dy/=d;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;});
    N.forEach(n=>{n.vx+=(W/2-n.x)*0.004;n.vy+=(H/2-n.y)*0.004;n.x+=Math.max(-12,Math.min(12,n.vx));n.y+=Math.max(-12,Math.min(12,n.vy));n.vx*=0.82;n.vy*=0.82;
      n.x=Math.max(16,Math.min(W-16,n.x));n.y=Math.max(16,Math.min(H-16,n.y));});
  }
  E.forEach(e=>{const l=document.createElementNS(NS,'line');l.setAttribute('x1',N[e.s].x);l.setAttribute('y1',N[e.s].y);
    l.setAttribute('x2',N[e.t].x);l.setAttribute('y2',N[e.t].y);l.setAttribute('stroke','#d4d7e0');l.setAttribute('stroke-width','1');svg.appendChild(l);});
  let drag=null;
  N.forEach((n,i)=>{const g=document.createElementNS(NS,'g');g.style.cursor='grab';
    const c=document.createElementNS(NS,'circle');const r=n.type==='paper'?7+Math.min(6,(deg[i]||0)):5;
    c.setAttribute('cx',n.x);c.setAttribute('cy',n.y);c.setAttribute('r',r);c.setAttribute('fill',COL[n.type]||'#888');
    c.setAttribute('stroke','#fff');c.setAttribute('stroke-width','1.5');
    const tt=document.createElementNS(NS,'title');tt.textContent=(n.type+': '+n.label+(n.title?' — '+n.title:''));c.appendChild(tt);
    g.appendChild(c);
    if(n.type==='paper'){const tx=document.createElementNS(NS,'text');tx.setAttribute('x',n.x+r+2);tx.setAttribute('y',n.y+3);
      tx.setAttribute('font-size','9');tx.setAttribute('fill','#555');tx.textContent=n.label;g.appendChild(tx);}
    g.onmousedown=ev=>{drag={i,c,g,n};ev.preventDefault();};svg.appendChild(g);});
  svg.addEventListener('mousemove',ev=>{if(!drag)return;const pt=svg.getBoundingClientRect();
    const x=(ev.clientX-pt.left)/pt.width*W,y=(ev.clientY-pt.top)/pt.height*H;drag.n.x=x;drag.n.y=y;
    drag.c.setAttribute('cx',x);drag.c.setAttribute('cy',y);
    drag.g.querySelectorAll('text').forEach(t=>{t.setAttribute('x',x+10);t.setAttribute('y',y+3);});
    E.forEach((e,k)=>{if(e.s===drag.i||e.t===drag.i){const l=svg.querySelectorAll('line')[k];
      l.setAttribute('x1',N[e.s].x);l.setAttribute('y1',N[e.s].y);l.setAttribute('x2',N[e.t].x);l.setAttribute('y2',N[e.t].y);}});});
  window.addEventListener('mouseup',()=>drag=null);
})();
</script>
</body></html>"""
