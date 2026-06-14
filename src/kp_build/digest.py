"""CONTEXT.md — the token-bounded field briefing an agent loads.

This is what makes the package compute-amortizing: load it, skip the research. It is ordered by
value (papers spine → open problems → debates → key claims) and truncated from the bottom so the
high-value sections always survive a token budget.
"""

from __future__ import annotations

from .schema import Package

# crude token estimate; good enough for budgeting (~4 chars/token).
def _toks(s: str) -> int:
    return len(s) // 4


def build_context(pkg: Package, *, built: str, max_tokens: int = 6000) -> str:
    verified = {p.cite_key: p for p in pkg.papers if p.verified.exists}

    head = [
        f"# Field briefing: {pkg.topic}",
        "",
        f"*A wikillm knowledge package (built {built}). Load this to inherit the research landscape "
        f"of this topic. Confidence is corpus-relative. Every cited paper was verified to exist "
        f"(arXiv/Crossref); do not invent citations beyond this list.*",
        "",
        f"**Scope:** {pkg.scope}",
        "",
    ]

    # 1. Verified papers (the spine) — always include.
    papers_sec = ["## Verified papers (the citation spine)", ""]
    for p in pkg.papers:
        if not p.verified.exists:
            continue
        ident = p.arxiv_id and f"arXiv:{p.arxiv_id}" or (p.doi and f"doi:{p.doi}") or ""
        yr = f" ({p.year})" if p.year else ""
        papers_sec.append(f"- **[{p.cite_key}]** {p.title}{yr}. {ident}")
    papers_sec.append("")

    # 2. Open problems (the heart) — always include.
    prob_sec = ["## Open problems (where new work goes)", ""]
    probs = [op for op in pkg.open_problems if any(k in verified for k in op.flagged_by)]
    for op in probs:
        flags = ", ".join(f"[{k}]" for k in op.flagged_by if k in verified)
        prob_sec.append(f"- **{op.statement}** ({op.status}) — {op.why_it_matters} *Flagged by {flags}.*")
    if not probs:
        prob_sec.append("- (none surfaced — likely a coverage gap; treat with suspicion.)")
    prob_sec.append("")

    # 3. Debates — always include.
    deb_sec = ["## Open debates / contested points", ""]
    debs = [d for d in pkg.debates if any(k in verified for pos in d.positions for k in pos.papers)]
    for d in debs:
        deb_sec.append(f"- **{d.question}**" + ("  *(resolved)*" if d.resolved else ""))
        for pos in d.positions:
            who = ", ".join(f"[{k}]" for k in pos.papers if k in verified)
            deb_sec.append(f"    - *{pos.stance}* ({who}): {pos.summary}")
    if not debs:
        deb_sec.append("- (none surfaced.)")
    deb_sec.append("")

    # 4. Key claims by type — truncatable tail.
    claim_sec = ["## Key grounded claims", ""]
    by_type: dict[str, list] = {}
    for c in pkg.claims:
        if c.paper in verified:
            by_type.setdefault(c.claim_type, []).append(c)
    for t in ("result", "finding", "method", "definition"):
        cs = by_type.get(t) or []
        if cs:
            claim_sec.append(f"### {t.capitalize()}s")
            for c in cs:
                claim_sec.append(f"- {c.statement} *([{c.paper}], {c.confidence})*")
            claim_sec.append("")

    fixed = "\n".join(head + papers_sec + prob_sec + deb_sec)
    claims_txt = "\n".join(claim_sec)
    if _toks(fixed) + _toks(claims_txt) <= max_tokens:
        return fixed + "\n" + claims_txt

    # Trim claims to fit (high-value sections are never dropped).
    budget = max_tokens - _toks(fixed)
    kept, used = ["## Key grounded claims (truncated to fit token budget)", ""], 0
    for line in claim_sec[2:]:
        t = _toks(line) + 1
        if used + t > budget:
            kept.append(f"\n*(+{len(claim_sec) - len(kept)} more claims omitted — see `claims/`.)*")
            break
        kept.append(line); used += t
    return fixed + "\n" + "\n".join(kept) + "\n"
