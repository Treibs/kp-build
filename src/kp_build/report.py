"""Render a wikillm package as a self-contained, browsable HTML report — the HUMAN-facing view.

`CONTEXT.md` is the agent payload; this is the human one. Design: a quality-judgment INSTRUMENT, not
a document. Three priority zones in one column: (1) a sticky toolbar + an always-visible VERDICT CARD
that answers "is this package good?" in ~30s (does it help / are citations real / how much is here);
(2) a segmented TAB BAR over a single DETAIL panel — exactly one of Spine / Problems / Debates /
Benchmarks / Claims / Graph is shown at a time, so the page is never a six-section wall; (3) a
low-priority provenance footer. Progressive disclosure throughout: tab labels carry counts, claim
passages collapse behind a teaser, the base-vs-KP bars sit one expander deep, the graph builds lazily.
Everything degrades honestly (no fake scores when falsification didn't run; an empty open-problems
register reads as an amber coverage gap, not a green zero).

One file, zero external dependencies (inline CSS + vanilla JS), openable from `file://`. ALL package
text is HTML-escaped — a loaded package is treated as data, never markup.
"""

from __future__ import annotations

import glob
import html
import json
import math
import re
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
        return f"https://arxiv.org/abs/{_esc(p.arxiv_id)}"
    if p.doi:
        return f"https://doi.org/{_esc(p.doi)}"
    return ""


def _keychip(k: str) -> str:
    """A cite_key chip that cross-links to its row in the Spine tab."""
    return f'<a class="key keylink" data-key="{_esc(k)}" href="#tab-spine">{_esc(k)}</a>'


# ── verdict card (the always-visible 30-second judgment) ─────────────────────────────


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _bar_pair(name, b, k) -> str:
    def row(lbl, raw, cls):
        val = _num(raw)
        pct = 0 if val is None else max(0, min(100, round(val * 100)))
        txt = "—" if val is None else f"{val:.2f}"
        return (f'<div class="bar-row"><span class="bar-name">{lbl}</span>'
                f'<span class="bar-track"><span class="bar-fill {cls}" style="width:{pct}%"></span></span>'
                f'<span class="bar-val">{txt}</span></div>')
    return (f'<div class="metric"><div class="metric-h">{_esc(name)}</div>'
            + row("base", b, "base") + row("KP", k, "kp") + "</div>")


def _donut(verified: int, total: int) -> str:
    r = 32.0
    circ = 2 * math.pi * r
    frac = (verified / total) if total else 0.0
    off = circ * (1 - frac)
    return (f'<svg viewBox="0 0 84 84" class="donut" aria-hidden="true">'
            f'<circle cx="42" cy="42" r="{r}" fill="none" stroke="#e6e8ee" stroke-width="9"/>'
            f'<circle cx="42" cy="42" r="{r}" fill="none" stroke="#16a34a" stroke-width="9" stroke-linecap="round" '
            f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 42 42)"/>'
            f'<text x="42" y="47" text-anchor="middle" class="donut-num">{verified}/{total}</text></svg>')


def _tile_help(man: dict) -> str:
    f = man.get("falsification") or {}
    b, k = f.get("base") or {}, f.get("kp") or {}
    # ALWAYS show the "Not measured + run kp-build falsify" guidance unless there is a genuine measured
    # result (a real run with a verdict or base/kp data) — never an empty/half verdict tile.
    if not (f.get("run") and (f.get("verdict") or b or k)):
        return ('<div class="tile"><div class="tile-h">Does it help?</div>'
                '<div class="verdict neutral">Not measured</div>'
                '<div class="tile-sub">Run <code>kp-build falsify</code> to compare a package-loaded '
                'agent against unaided recall.</div></div>')
    verdict = str(f.get("verdict", ""))
    tone = "good" if "HELPS" in verdict else ("bad" if ("DID NOT" in verdict or "HURT" in verdict) else "warn")
    bf, kf = _num(b.get("f1")), _num(k.get("f1"))
    delta = ""
    if bf is not None and kf is not None:
        sign = "+" if kf >= bf else ""
        delta = f'<div class="delta">base f1 <b>{bf:.2f}</b> → KP <b>{kf:.2f}</b> <span class="d {tone}">({sign}{kf-bf:.2f})</span></div>'
    word = {"good": "HELPS", "warn": "TIE", "bad": "DOESN’T HELP"}[tone]
    fakes = b.get("fake_list") or []
    fakes_html = ""
    if fakes:
        items = "".join(f"<li><code>{_esc(x)}</code></li>" for x in fakes)
        fakes_html = (f'<div class="fakes"><div class="fakes-h">Base mislabeled / fabricated '
                      f'{len(fakes)} citation(s):</div><ul>{items}</ul></div>')
    detail = (f'<div id="help-detail" class="help-detail">'
              f'{_bar_pair("precision", b.get("precision"), k.get("precision"))}'
              f'{_bar_pair("recall", b.get("recall"), k.get("recall"))}'
              f'{_bar_pair("f1", bf, kf)}{fakes_html}</div>')
    return (f'<div class="tile"><div class="tile-h">Does it help?</div>'
            f'<div class="verdict {tone}"><span class="vbar"></span>{word}</div>{delta}'
            f'<button id="help-expand" class="expander">show base-vs-KP detail ▸</button>{detail}</div>')


def _tile_citations(man: dict, verified: int, total: int) -> str:
    f = man.get("falsification") or {}
    base_fake = (f.get("base") or {}).get("fake") if f.get("run") else None
    unver = total - verified
    sub = "all citations verified" if unver == 0 else f"{unver} not verified (cannot anchor claims)"
    fab = (f'<a class="sub-chip bad keylink-fakes" href="#tab-spine">base fabricated {_esc(base_fake)}</a>'
           if base_fake else "")
    return (f'<div class="tile"><div class="tile-h">Are citations real?</div>'
            f'<div class="donut-wrap">{_donut(verified, total)}</div>'
            f'<div class="tile-sub">{_esc(sub)}</div>{fab}</div>')


def _tile_counts(counts: dict, via_expansion=None) -> str:
    rows = [("papers", counts["papers"]), ("claims", counts["claims"]),
            ("problems", counts["open_problems"]), ("debates", counts["debates"]),
            ("benchmarks", counts["benchmarks"])]
    cells = "".join(f'<div class="ct"><b>{_esc(v)}</b><span>{lbl}</span></div>' for lbl, v in rows)
    gap = ('<div class="gap-note">⚠ no open problems — treat coverage with suspicion</div>'
           if counts["open_problems"] == 0 else "")
    depth = (f'<div class="tile-sub">{_esc(via_expansion)} found via citation-graph expansion</div>'
             if via_expansion else "")
    return (f'<div class="tile"><div class="tile-h">How much is here?</div>'
            f'<div class="ct-grid">{cells}</div>{gap}{depth}</div>')


def _bottom_line(man: dict, verified: int, total: int, counts: dict) -> str:
    f = man.get("falsification") or {}
    parts = []
    if f.get("run"):
        b, k = f.get("base", {}), f.get("kp", {})
        bf, kf = _num(b.get("f1")), _num(k.get("f1"))
        if bf is not None and kf is not None:
            verb = "helps an agent" if kf > bf else ("ties unaided recall" if kf == bf else "did not beat unaided recall")
            parts.append(f"Loading this package {verb} (f1 {bf:.2f}→{kf:.2f}).")
    parts.append(f"{verified}/{total} citations verified against arXiv/Crossref.")
    if counts["open_problems"] == 0:
        parts.append("No open problems surfaced — a likely coverage gap.")
    return _esc(" ".join(parts))


def _verdict_card(man, verified, total, counts) -> str:
    via_exp = (man.get("coverage") or {}).get("papers_via_expansion")
    return (f'<section class="verdict-card">'
            f'<div class="tiles">{_tile_help(man)}{_tile_citations(man, verified, total)}{_tile_counts(counts, via_exp)}</div>'
            f'<div class="bottom-line">{_bottom_line(man, verified, total, counts)}</div></section>')


# ── detail panels (one shown at a time) ──────────────────────────────────────────────


def _panel_spine(papers) -> str:
    rows = []
    for p in papers:
        ok = p.verified.exists
        link = _paper_link(p)
        ident = (p.arxiv_id and f"arXiv:{_esc(p.arxiv_id)}{_esc(p.arxiv_version)}") or (p.doi and f"doi:{_esc(p.doi)}") or "—"
        ident_html = f'<a href="{link}" target="_blank" rel="noopener">{ident}</a>' if link else ident
        yr = f" ({_esc(p.year)})" if p.year else ""
        badge = '<span class="pill ok">verified</span>' if ok else f'<span class="pill no">{_esc(p.verified.status)}</span>'
        rows.append(f'<li id="paper-{_esc(p.cite_key)}" class="{"" if ok else "dim"}">'
                    f'<span class="dot paper"></span><code class="key">{_esc(p.cite_key)}</code> '
                    f'<span class="ptitle">{_esc(p.title)}</span>{yr} {badge}'
                    f'<div class="ident">{ident_html}</div></li>')
    ctrl = '<button id="verified-only" class="chip">verified only</button>'
    return f'<div class="panel-tools">{ctrl}</div><ul class="spine">{"".join(rows)}</ul>'


def _panel_problems(problems, verified) -> str:
    if not problems:
        return '<p class="empty">No open problems surfaced — likely a coverage gap (the most valuable section is empty).</p>'
    cards = []
    for op in problems:
        flags = " ".join(_keychip(k) for k in op.flagged_by if k in verified)
        cards.append(f'<div class="row problem"><div class="row-stmt">{_esc(op.statement)}</div>'
                     f'<div class="row-sub"><b>Why it matters:</b> {_esc(op.why_it_matters)}</div>'
                     f'<div class="row-meta">flagged by {flags} <span class="pill st">{_esc(op.status)}</span></div></div>')
    return "".join(cards)


def _panel_debates(debates, verified) -> str:
    if not debates:
        return '<p class="empty">No debates surfaced.</p>'
    cards = []
    for db in debates:
        pos = []
        for p in db.positions:
            who = " ".join(_keychip(k) for k in p.papers if k in verified)
            if who:
                pos.append(f'<div class="pos"><div class="pos-h">{_esc(p.stance)} {who}</div>'
                           f'<div class="pos-s">{_esc(p.summary)}</div></div>')
        res = ' <span class="pill ok">resolved</span>' if db.resolved else ""
        cards.append(f'<div class="row debate"><div class="dq">{_esc(db.question)}{res}</div>{"".join(pos)}</div>')
    return "".join(cards)


def _panel_benchmarks(benchmarks, verified) -> str:
    bs = [b for b in benchmarks if b.paper in verified]
    if not bs:
        return '<p class="empty">No reported results.</p>'
    rows = "".join(f'<tr><td>{_esc(b.method)}</td><td>{_esc(b.dataset)}</td><td>{_esc(b.metric)}</td>'
                   f'<td class="num">{_esc(b.value)}</td><td>{_keychip(b.paper)}</td></tr>' for b in bs)
    return ('<table class="sota"><thead><tr><th>method</th><th>dataset</th><th>metric</th><th>value</th>'
            f'<th>paper</th></tr></thead><tbody>{rows}</tbody></table>')


def _conf_dots(conf) -> str:
    n = {"high": 3, "medium": 2, "low": 1}.get(conf, 2)
    dots = "".join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(3))
    return f'<span class="dots" title="confidence: {_esc(conf)}">{dots}</span>'


def _panel_claims(claims, verified) -> str:
    cs = [c for c in claims if c.paper in verified]
    if not cs:
        return '<p class="empty">No claims.</p>'
    order = {"result": 0, "finding": 1, "method": 2, "definition": 3}
    cs.sort(key=lambda c: order.get(c.claim_type, 9))
    types = sorted({c.claim_type for c in cs})
    chips = ('<div class="panel-tools"><span class="chips">'
             '<button class="chip active" data-t="all">all</button>'
             + "".join(f'<button class="chip" data-t="{_esc(t)}">{_esc(t)}</button>' for t in types)
             + '</span><button id="expand-all" class="chip">expand all quotes</button></div>')
    items = []
    for c in cs:
        corr = [k for k in c.corroborated_by if k in verified]
        meta = f'{_keychip(c.paper)} {_conf_dots(c.confidence)}'
        if corr:
            meta += f' <span class="corr">corroborated×{len(corr)}</span>'
        grounded = getattr(c, "grounded", "unchecked")
        flagged = (not c.survived_refuter) or grounded == "ungrounded"
        passage = ""
        if c.supporting_passage and not flagged:        # don't surface a refuted/ungrounded claim's passage
            teaser = _esc(c.supporting_passage[:90]) + ("…" if len(c.supporting_passage) > 90 else "")
            passage = (f'<button class="passage-toggle">show passage ▸</button>'
                       f'<span class="teaser">{teaser}</span>'
                       f'<blockquote>{_esc(c.supporting_passage)}</blockquote>')
        marks = "" if c.survived_refuter else ' <span class="pill no">⚠ refuter broke this</span>'
        if grounded == "grounded":
            marks += ' <span class="pill ok">✓ grounded</span>'
        elif grounded == "ungrounded":
            marks += ' <span class="pill no">⚠ passage not in paper</span>'
        items.append(f'<div class="row claim{" refuted" if flagged else ""}" data-t="{_esc(c.claim_type)}">'
                     f'<span class="tag t-{_esc(c.claim_type)}">{_esc(c.claim_type)}</span>{marks}'
                     f'<div class="cstmt">{_esc(c.statement)}</div>{passage}'
                     f'<div class="row-meta">{meta}</div></div>')
    return chips + f'<div id="claims">{"".join(items)}</div>'


def _graph_data(index: dict) -> dict:
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
                nodes.append({"id": nid, "type": typ, "label": nid,
                              "title": n.get("title", "") if typ == "paper" else ""})
    edges = [{"from": e["from"], "to": e["to"]} for e in index.get("edges", [])
             if e.get("from") in ids and e.get("to") in ids]
    return {"nodes": nodes, "edges": edges}


def build_report(pkg_dir: str | Path) -> str:
    d = Path(pkg_dir)
    man = json.loads((d / "wikillm.json").read_text(encoding="utf-8"))
    know = json.loads((d / "knowledge.json").read_text(encoding="utf-8")) if (d / "knowledge.json").is_file() else {}
    index = json.loads((d / "index.json").read_text(encoding="utf-8")) if (d / "index.json").is_file() else {}
    papers, claims, problems, debates, benchmarks = _read_nodes(d)
    verified_set = {p.cite_key for p in papers if p.verified.exists}
    verified, total = len(verified_set), len(papers)

    counts = {"papers": verified, "claims": len([c for c in claims if c.paper in verified_set]),
              "open_problems": len(problems), "debates": len(debates),
              "benchmarks": len([b for b in benchmarks if b.paper in verified_set])}

    s = man.get("stats", {})
    sp = man.get("source_span", {})
    span = f"{sp.get('oldest')}–{sp.get('newest')}" if sp.get("oldest") else "n/a"
    name = know.get("name", "@kp/?")
    chips = "".join(f'<span class="chip-meta">{_esc(t)}</span>' for t in [
        f"{name}@{know.get('version', '?')}", f"built {man.get('built', '?')}",
        f"{s.get('papers_verified', verified)}/{s.get('papers_total', total)} verified",
        f"years {span}"])

    panels = [
        ("spine", "Spine", counts["papers"], _panel_spine(papers)),
        ("problems", "Problems", counts["open_problems"], _panel_problems(problems, verified_set)),
        ("debates", "Debates", counts["debates"], _panel_debates(debates, verified_set)),
        ("benchmarks", "Benchmarks", counts["benchmarks"], _panel_benchmarks(benchmarks, verified_set)),
        ("claims", "Claims", counts["claims"], _panel_claims(claims, verified_set)),
        ("graph", "Graph", len(_graph_data(index)["nodes"]), '<div class="ghint">drag nodes · hover for titles · '
         '<span class="lg paper">paper</span><span class="lg claim">claim</span>'
         '<span class="lg problem">problem</span><span class="lg debate">debate</span>'
         '<span class="lg benchmark">benchmark</span></div><div id="graph"></div>'),
    ]
    tabbar = "".join(
        f'<button id="tab-btn-{key}" class="tab{" active" if i == 0 else ""}" data-tab="{key}" role="tab" '
        f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="tab-{key}" '
        f'tabindex="{"0" if i == 0 else "-1"}">{_esc(label)}'
        f'<span class="badge">{_esc(cnt)}</span></button>'
        for i, (key, label, cnt, _) in enumerate(panels))
    panes = "".join(
        f'<section class="panel" id="tab-{key}" role="tabpanel" aria-labelledby="tab-btn-{key}" '
        f'style="display:{"block" if i == 0 else "none"}">{body}</section>'
        for i, (key, label, cnt, body) in enumerate(panels))

    gdata = json.dumps(_graph_data(index)).replace("</", "<\\/")
    body = (f'{_verdict_card(man, verified, total, counts)}'
            f'<div class="tabbar" role="tablist">{tabbar}</div>{panes}'
            f'<footer class="prov"><button id="view-all" class="chip">view all / print</button> '
            f'<details class="method"><summary>what was searched</summary>'
            f'<pre>{_esc(json.dumps(man.get("coverage", {}), indent=2))}</pre></details>'
            f'<div class="foot">Generated by kp-build · a wikillm knowledge package · confidence is corpus-relative</div></footer>')

    subs = {"__TITLE__": _esc(man.get("topic", "wikillm package")), "__SCOPE__": _esc(man.get("scope", "")),
            "__CHIPS__": chips, "__BODY__": body, "__GRAPH__": gdata}
    # ONE pass over the template — a replacement value that happens to contain another placeholder
    # (e.g. a package whose topic is literally "__GRAPH__") is never re-scanned/expanded.
    return _PLACEHOLDER_RE.sub(lambda m: subs[m.group(0)], _TEMPLATE)


_PLACEHOLDER_RE = re.compile(r"__(?:TITLE|SCOPE|CHIPS|BODY|GRAPH)__")


_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — wikillm report</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1a1c22;--mut:#6b7280;--line:#e6e8ee;--acc:#4f46e5;
--paper:#4f46e5;--claim:#0d9488;--problem:#d97706;--debate:#9333ea;--benchmark:#2563eb;
--good:#16a34a;--warn:#d97706;--bad:#dc2626;--shadow:0 1px 2px rgba(20,20,40,.05)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:14.5px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.tabnum,.bar-val,.donut-num,.num,.delta b{font-variant-numeric:tabular-nums}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px 70px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em}
a{color:var(--benchmark)}
/* header */
.accent{height:4px;background:linear-gradient(90deg,#312e81,#4f46e5)}
.toolbar{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);
border-bottom:1px solid var(--line)}
.toolbar .in{max-width:1040px;margin:0 auto;padding:9px 20px;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.t-topic{font-size:18px;font-weight:600;line-height:1.2}
.t-scope{color:var(--mut);font-size:12.5px;max-width:560px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer;border:0;background:none;font-family:inherit;text-align:left;padding:0}
.t-scope.open{white-space:normal}
.chips-meta{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap}
.chip-meta{background:#eef0fb;color:#3730a3;border-radius:99px;padding:2px 9px;font-size:11.5px;font-weight:500}
/* verdict card */
.verdict-card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);margin:18px 0 14px;overflow:hidden}
.tiles{display:grid;grid-template-columns:1.25fr .85fr 1fr}
.tile{padding:18px 20px;border-right:1px solid var(--line)}.tile:last-child{border-right:0}
.tile-h{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);font-weight:600;margin-bottom:10px}
.verdict{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:15px;padding:7px 12px 7px 0;border-radius:8px}
.verdict .vbar{width:4px;align-self:stretch;border-radius:3px}
.verdict.good{color:#14532d}.verdict.good .vbar{background:var(--good)}
.verdict.warn{color:#7c2d12}.verdict.warn .vbar{background:var(--warn)}
.verdict.bad{color:#7f1d1d}.verdict.bad .vbar{background:var(--bad)}
.verdict.neutral{color:var(--mut);font-weight:600;background:var(--bg);padding:7px 12px}
.delta{font-size:13.5px;margin:2px 0 8px}.delta .d{font-weight:700}.delta .d.good{color:var(--good)}.delta .d.warn{color:var(--warn)}.delta .d.bad{color:var(--bad)}
.tile-sub{color:var(--mut);font-size:12.5px;margin-top:4px}
.expander{background:none;border:0;color:var(--acc);font-size:12.5px;cursor:pointer;padding:4px 0}
.help-detail{display:none;margin-top:6px}
.metric{margin:7px 0}.metric-h{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.03em}
.bar-row{display:flex;align-items:center;gap:7px;margin:3px 0}.bar-name{width:30px;font-size:11px;color:var(--mut)}
.bar-track{flex:1;background:var(--bg);border:1px solid var(--line);border-radius:99px;height:9px;overflow:hidden}
.bar-fill{display:block;height:100%}.bar-fill.base{background:#cbd5e1}.bar-fill.kp{background:var(--acc)}
.bar-val{width:32px;text-align:right;font-size:12px}
.fakes{margin-top:9px;background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:8px 11px}
.fakes-h{font-size:12px;font-weight:600;color:#9a3412;margin-bottom:4px}.fakes ul{margin:0;padding-left:16px}.fakes li{font-size:11.5px;margin:2px 0}
.donut-wrap{display:flex;justify-content:center}.donut{width:84px;height:84px}.donut-num{font-size:17px;font-weight:700;fill:var(--ink)}
.sub-chip{display:inline-block;margin-top:8px;font-size:11.5px;border-radius:99px;padding:2px 9px;text-decoration:none}
.sub-chip.bad{background:#fee2e2;color:#b91c1c}
.ct-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px 16px}
.ct{display:flex;flex-direction:column}.ct b{font-size:21px;line-height:1}.ct span{color:var(--mut);font-size:11.5px}
.gap-note{margin-top:9px;background:#fffbeb;border:1px solid #fde68a;color:#92400e;font-size:11.5px;border-radius:8px;padding:6px 9px}
.bottom-line{border-top:1px solid var(--line);padding:11px 20px;color:#374151;font-size:13.5px;background:#fcfcfd}
/* tab bar */
.tabbar{position:sticky;top:43px;z-index:20;display:flex;gap:4px;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);overflow-x:auto}
.tab{flex:0 0 auto;background:var(--card);border:1px solid var(--line);border-radius:9px;padding:6px 12px;font-size:13px;color:var(--mut);cursor:pointer;font-weight:500;display:inline-flex;align-items:center;gap:7px}
.tab.active{background:var(--acc);color:#fff;border-color:var(--acc)}
.badge{font-size:11px;font-variant-numeric:tabular-nums;background:var(--bg);color:var(--mut);border-radius:99px;padding:0 7px;min-width:18px;text-align:center}
.tab.active .badge{background:rgba(255,255,255,.25);color:#fff}
/* panels */
.panel{background:var(--card);border:1px solid var(--line);border-top:0;border-radius:0 0 12px 12px;padding:16px 20px;margin-bottom:18px}
.panel-tools{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.empty{color:var(--mut)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:3px 11px;font-size:12px;cursor:pointer;color:var(--mut)}
.chip.active{background:var(--acc);color:#fff;border-color:var(--acc)}
.key{background:#eef0fb;color:var(--acc);border-radius:5px;padding:1px 6px;text-decoration:none}
a.keylink{cursor:pointer}
.dot{display:inline-block;width:9px;height:9px;border-radius:99px;vertical-align:middle;margin-right:3px}
.dot.paper{background:var(--paper)}
/* spine */
ul.spine{list-style:none;margin:0;padding:0}
ul.spine li{padding:9px 0 9px 10px;border-bottom:1px solid var(--line);border-left:3px solid var(--paper);border-radius:2px;margin-bottom:2px}
ul.spine li:last-child{border-bottom:0}ul.spine li.dim{opacity:.5;border-left-color:#cbd5e1}
ul.spine li.flash{background:#eef0fb;transition:background .3s}
.ptitle{font-weight:600}.ident{color:var(--mut);font-size:12px;margin-top:2px}.ident a{text-decoration:none}.ident a:hover{text-decoration:underline}
.pill{font-size:10.5px;border-radius:99px;padding:1px 8px;vertical-align:middle}
.pill.ok{background:#dcfce7;color:#15803d}.pill.no{background:#fee2e2;color:#b91c1c}.pill.st{background:var(--bg);color:var(--mut);border:1px solid var(--line)}
/* rows (problems/debates/claims) */
.row{padding:11px 0 11px 11px;border-bottom:1px solid var(--line);border-left:3px solid var(--line)}
.row:last-child{border-bottom:0}
.row.problem{border-left-color:var(--problem)}.row.debate{border-left-color:var(--debate)}.row.claim{border-left-color:var(--claim)}
.row.refuted{opacity:.62;border-left-color:var(--bad)}
.row-stmt{font-weight:600;margin-bottom:3px}.row-sub{color:#374151;font-size:13px;margin-bottom:4px}
.row-meta{color:var(--mut);font-size:12px;margin-top:5px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dq{font-weight:600;margin-bottom:7px}
.pos{border-left:2px solid var(--debate);padding:2px 0 2px 10px;margin:6px 0}.pos-h{font-size:13px;font-weight:600}.pos-s{font-size:13px;color:#374151}
.corr{background:#ecfdf5;color:#065f46;border-radius:5px;padding:0 6px;font-size:11px}
/* benchmarks */
table.sota{width:100%;border-collapse:collapse;font-size:13px}
table.sota th{text-align:left;color:var(--mut);font-weight:600;border-bottom:2px solid var(--line);padding:6px 8px}
table.sota td{border-bottom:1px solid var(--line);padding:6px 8px}td.num{font-weight:600}
/* claims */
.tag{font-size:10.5px;border-radius:5px;padding:1px 7px;color:#fff;text-transform:uppercase;letter-spacing:.03em}
.t-result{background:var(--claim)}.t-finding{background:var(--benchmark)}.t-method{background:var(--debate)}.t-definition{background:var(--mut)}
.cstmt{margin:6px 0 0}
.passage-toggle{background:none;border:0;color:var(--acc);font-size:12px;cursor:pointer;padding:5px 0 0;display:block}
.teaser{color:var(--mut);font-size:12.5px;font-style:italic}
.claim blockquote{display:none;margin:5px 0 0;padding:5px 11px;border-left:3px solid var(--line);color:#374151;font-size:12.5px;background:var(--bg);border-radius:0 6px 6px 0}
.dots{display:inline-flex;gap:3px}.dots i{width:6px;height:6px;border-radius:99px;background:var(--line)}.dots i.on{background:var(--claim)}
/* graph */
.ghint{color:var(--mut);font-size:12px;margin-bottom:8px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.lg{display:inline-flex;align-items:center;gap:5px}.lg::before{content:"";width:9px;height:9px;border-radius:99px}
.lg.paper::before{background:var(--paper)}.lg.claim::before{background:var(--claim)}.lg.problem::before{background:var(--problem)}.lg.debate::before{background:var(--debate)}.lg.benchmark::before{background:var(--benchmark)}
#graph{width:100%;height:500px;border:1px solid var(--line);border-radius:9px;background:#fcfcfd;cursor:grab}
/* footer */
.prov{margin-top:6px;color:var(--mut)}.method{margin:10px 0;font-size:12.5px}.method pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;overflow:auto;font-size:11.5px}
.foot{font-size:12px;text-align:center;margin-top:8px}
/* view-all / print: un-tab into a linear stack */
body.viewall .tabbar{display:none}body.viewall .panel{display:block!important;border-radius:12px;border-top:1px solid var(--line);margin-bottom:14px}
body.viewall .claim blockquote{display:block!important}body.viewall .teaser,body.viewall .passage-toggle{display:none}
@media print{.toolbar{position:static}.tabbar,.expander,.passage-toggle,.panel-tools,#view-all{display:none}
 .panel{display:block!important;border:1px solid #ccc;border-radius:8px;margin-bottom:12px;break-inside:avoid}.claim blockquote{display:block!important}.help-detail{display:block!important}}
@media (max-width:760px){.tiles{grid-template-columns:1fr}.tile{border-right:0;border-bottom:1px solid var(--line)}.chips-meta{margin-left:0;width:100%}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
</style></head>
<body>
<div class="accent"></div>
<div class="toolbar"><div class="in"><span class="t-topic">__TITLE__</span><button class="t-scope" id="scope" aria-expanded="false" title="click to expand">__SCOPE__</button><span class="chips-meta">__CHIPS__</span></div></div>
<div class="wrap">__BODY__</div>
<script>
const G=__GRAPH__;
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const tabs=$$('.tab'),panels=$$('.panel');let cur='spine',graphBuilt=false;
function activate(id,push){
  if(!tabs.some(t=>t.dataset.tab===id))id='spine';cur=id;
  tabs.forEach(t=>{const on=t.dataset.tab===id;t.classList.toggle('active',on);t.setAttribute('aria-selected',on?'true':'false');t.setAttribute('tabindex',on?'0':'-1');});
  panels.forEach(p=>p.style.display=(p.id==='tab-'+id)?'block':'none');
  if(id==='graph'&&!graphBuilt){buildGraph();graphBuilt=true;}
  if(push)history.replaceState(null,'','#tab-'+id);
}
tabs.forEach(t=>t.onclick=()=>activate(t.dataset.tab,true));
$('.tabbar').addEventListener('keydown',e=>{
  const i=tabs.findIndex(t=>t.classList.contains('active'));let j=null;
  if(e.key==='ArrowRight')j=(i+1)%tabs.length;if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
  if(j!==null){activate(tabs[j].dataset.tab,true);tabs[j].focus();e.preventDefault();}});
const h0=(location.hash.match(/^#tab-(\w+)/)||[])[1];activate(h0||'spine',false);
// scope expand
const sc=$('#scope');if(sc)sc.onclick=()=>{const open=sc.classList.toggle('open');sc.setAttribute('aria-expanded',open?'true':'false');};
// cite-key cross-links
function jump(key){activate('spine',true);const r=document.getElementById('paper-'+key);
  if(r){r.scrollIntoView({block:'center'});r.classList.add('flash');setTimeout(()=>r.classList.remove('flash'),1200);}}
$$('.keylink').forEach(a=>a.onclick=e=>{e.preventDefault();jump(a.dataset.key);});
$$('.keylink-fakes').forEach(a=>a.onclick=e=>{e.preventDefault();activate('spine',true);});
// claim passages
$$('.passage-toggle').forEach(b=>b.onclick=()=>{const bq=b.parentElement.querySelector('blockquote');
  const open=getComputedStyle(bq).display!=='none';bq.style.display=open?'none':'block';b.textContent=open?'show passage ▸':'hide passage ▾';});
const ea=$('#expand-all');if(ea)ea.onclick=()=>{$$('#tab-claims blockquote').forEach(bq=>bq.style.display='block');
  $$('.passage-toggle').forEach(b=>b.textContent='hide passage ▾');};
// claims filter
$$('.chip[data-t]').forEach(c=>c.onclick=()=>{$$('.chip[data-t]').forEach(x=>x.classList.remove('active'));c.classList.add('active');
  const t=c.dataset.t;$$('.claim').forEach(el=>el.style.display=(t==='all'||el.dataset.t===t)?'':'none');});
// help expander
const he=$('#help-expand');if(he)he.onclick=()=>{const d=$('#help-detail');const open=getComputedStyle(d).display!=='none';
  d.style.display=open?'none':'block';he.textContent=open?'show base-vs-KP detail ▸':'hide base-vs-KP detail ▾';};
// verified-only
const vo=$('#verified-only');if(vo)vo.onclick=()=>{const on=vo.classList.toggle('active');
  $$('#tab-spine li.dim').forEach(li=>li.style.display=on?'none':'');vo.textContent=on?'show all':'verified only';};
// view all / print
const va=$('#view-all');if(va)va.onclick=()=>{const on=document.body.classList.toggle('viewall');
  if(on){panels.forEach(p=>p.style.display='block');if(!graphBuilt){buildGraph();graphBuilt=true;}}else{activate(cur,false);}
  va.textContent=on?'tabbed view':'view all / print';};
// lazy force-directed graph
function buildGraph(){
  const el=$('#graph');if(!el||!G.nodes.length)return;
  const W=el.clientWidth||900,H=500,COL={paper:'#4f46e5',claim:'#0d9488',problem:'#d97706',debate:'#9333ea',benchmark:'#2563eb'};
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
      n.x=Math.max(16,Math.min(W-16,n.x));n.y=Math.max(16,Math.min(H-16,n.y));});}
  E.forEach(e=>{const l=document.createElementNS(NS,'line');l.setAttribute('x1',N[e.s].x);l.setAttribute('y1',N[e.s].y);
    l.setAttribute('x2',N[e.t].x);l.setAttribute('y2',N[e.t].y);l.setAttribute('stroke','#d4d7e0');svg.appendChild(l);});
  let drag=null;
  N.forEach((n,i)=>{const g=document.createElementNS(NS,'g');g.style.cursor='grab';
    const c=document.createElementNS(NS,'circle'),r=n.type==='paper'?7+Math.min(6,deg[i]||0):5;
    c.setAttribute('cx',n.x);c.setAttribute('cy',n.y);c.setAttribute('r',r);c.setAttribute('fill',COL[n.type]||'#888');
    c.setAttribute('stroke','#fff');c.setAttribute('stroke-width','1.5');
    const tt=document.createElementNS(NS,'title');tt.textContent=n.type+': '+n.label+(n.title?' — '+n.title:'');c.appendChild(tt);g.appendChild(c);
    if(n.type==='paper'){const tx=document.createElementNS(NS,'text');tx.setAttribute('x',n.x+r+2);tx.setAttribute('y',n.y+3);
      tx.setAttribute('font-size','9');tx.setAttribute('fill','#555');tx.textContent=n.label;g.appendChild(tx);}
    g.onmousedown=ev=>{drag={i,c,g,n};ev.preventDefault();};svg.appendChild(g);});
  svg.addEventListener('mousemove',ev=>{if(!drag)return;const p=svg.getBoundingClientRect();
    const x=(ev.clientX-p.left)/p.width*W,y=(ev.clientY-p.top)/p.height*H;drag.n.x=x;drag.n.y=y;
    drag.c.setAttribute('cx',x);drag.c.setAttribute('cy',y);
    drag.g.querySelectorAll('text').forEach(t=>{t.setAttribute('x',x+10);t.setAttribute('y',y+3);});
    E.forEach((e,k)=>{if(e.s===drag.i||e.t===drag.i){const l=svg.querySelectorAll('line')[k];
      l.setAttribute('x1',N[e.s].x);l.setAttribute('y1',N[e.s].y);l.setAttribute('x2',N[e.t].x);l.setAttribute('y2',N[e.t].y);}});});
  window.addEventListener('mouseup',()=>drag=null);
}
</script>
</body></html>"""
