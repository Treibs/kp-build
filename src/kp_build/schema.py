"""wikillm package schema — the node types and their markdown (de)serialization.

A package is a set of four node kinds, all anchored to a verified-citation spine:
- Paper        : a verified citation object (the spine)
- Claim        : a grounded finding/result/method anchored to a Paper + verbatim passage
- OpenProblem  : a gap the field has not closed, flagged by ≥1 Paper (the heart)
- Debate       : a contested point with competing positions

Every node serializes to a markdown file with YAML frontmatter, so a package is a portable,
human-diffable, agent-loadable directory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import yaml

SCHEMA_VERSION = "wikillm/1"

CLAIM_TYPES = ("result", "method", "finding", "definition")
CONFIDENCE = ("high", "medium", "low")
PROBLEM_STATUS = ("open", "partially-addressed")

_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(text: str, *, max_words: int = 8) -> str:
    """Deterministic id slug: lowercase, hyphenated, first ``max_words`` words."""
    cleaned = _SLUG.sub("-", text.lower()).strip("-")
    words = [w for w in cleaned.split("-") if w]
    return "-".join(words[:max_words]) or "node"


# ── nodes ───────────────────────────────────────────────────────────────────────


@dataclass
class Verification:
    """Result of checking a paper against a real citation index.

    ``exists`` is the SHIP gate: True only for a STRONG verification — an explicit identifier
    (arXiv id / DOI) that resolves AND whose canonical title strictly matches the claimed title.
    A title-only search hit is ``status='unconfirmed'`` with ``exists=False`` (it can NOT anchor a
    shipped claim) — this is what stops the tool laundering a fabricated title against an unrelated
    real work. ``status`` distinguishes the failure modes so they are never conflated:
      verified | unconfirmed | id-title-mismatch | not-found | error | unverified
    """

    exists: bool = False
    status: str = "unverified"
    via: str = "unverified"           # "arxiv" | "crossref" | "unverified"
    canonical_title: str = ""
    match_score: float = 0.0
    checked: str = ""                 # YYYY-MM-DD


@dataclass
class Paper:
    """A verified citation object — the spine. A claim may only cite a verified paper."""

    cite_key: str
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    arxiv_id: str = ""
    arxiv_version: str = ""            # e.g. "v3" — pin the version a claim was read against
    doi: str = ""
    url: str = ""
    verified: Verification = field(default_factory=Verification)
    key_contributions: List[str] = field(default_factory=list)


@dataclass
class Claim:
    """A grounded, paper-anchored claim. ``confidence`` is corpus-relative."""

    id: str
    statement: str
    paper: str                        # cite_key of the anchoring Paper
    supporting_passage: str
    claim_type: str = "finding"
    confidence: str = "medium"
    corroborated_by: List[str] = field(default_factory=list)  # other cite_keys


@dataclass
class OpenProblem:
    """A gap the field has not closed — flagged by ≥1 paper's future-work/limitations."""

    id: str
    statement: str
    flagged_by: List[str] = field(default_factory=list)       # cite_keys
    status: str = "open"
    why_it_matters: str = ""


@dataclass
class Position:
    stance: str
    papers: List[str] = field(default_factory=list)           # cite_keys
    summary: str = ""


@dataclass
class Debate:
    """A contested point with competing positions."""

    id: str
    question: str
    positions: List[Position] = field(default_factory=list)
    resolved: bool = False


@dataclass
class Benchmark:
    """A reported result on a named dataset/metric — feeds the SOTA-numbers table a paper needs."""

    id: str
    name: str                          # human label, e.g. "MT-Bench wall-clock speedup"
    dataset: str = ""
    metric: str = ""                   # e.g. "speedup", "tokens/s", "accuracy"
    value: str = ""                    # kept as str: "2.8x", "76.4", ...
    method: str = ""                   # the approach this number is for
    paper: str = ""                    # cite_key it comes from


@dataclass
class Package:
    """The whole knowledge package."""

    topic: str
    scope: str
    papers: List[Paper] = field(default_factory=list)
    claims: List[Claim] = field(default_factory=list)
    open_problems: List[OpenProblem] = field(default_factory=list)
    debates: List[Debate] = field(default_factory=list)
    benchmarks: List[Benchmark] = field(default_factory=list)
    #: Coverage honesty (SPEC promise): what the survey searched, so the gap is explicit.
    #: e.g. {"sub_questions":[...], "queries":[...], "seed_papers":[...], "expansion_hops":1}
    coverage: dict = field(default_factory=dict)


# ── markdown (de)serialization ──────────────────────────────────────────────────


def _fm(d: dict, body: str = "") -> str:
    """Render a node as YAML-frontmatter markdown."""
    front = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, default_flow_style=False).strip()
    return f"---\n{front}\n---\n\n{body}".rstrip() + "\n"


def _split(text: str) -> tuple[dict, str]:
    parts = re.split(r"(?m)^---[ \t]*$", text, maxsplit=2)
    if len(parts) < 3:
        return {}, text
    return (yaml.safe_load(parts[1]) or {}), parts[2].strip()


def paper_to_md(p: Paper) -> str:
    d = asdict(p)
    body = ""
    if p.key_contributions:
        body = "## Key contributions\n\n" + "\n".join(f"- {c}" for c in p.key_contributions)
    return _fm(d, body)


def paper_from_md(text: str) -> Paper:
    fm, _ = _split(text)
    v = fm.get("verified") or {}
    return Paper(
        cite_key=fm["cite_key"], title=fm.get("title", ""), authors=list(fm.get("authors") or []),
        year=fm.get("year"), venue=fm.get("venue", ""), arxiv_id=fm.get("arxiv_id", ""),
        arxiv_version=fm.get("arxiv_version", ""), doi=fm.get("doi", ""), url=fm.get("url", ""),
        verified=Verification(**{k: v.get(k) for k in
                                 ("exists", "status", "via", "canonical_title", "match_score", "checked")
                                 if k in v}),
        key_contributions=list(fm.get("key_contributions") or []),
    )


def paper_ref_str(p: "Paper") -> str:
    """A self-contained identifier string for a paper (so a chunk resolves to a real id)."""
    if p.arxiv_id:
        return f"arXiv:{p.arxiv_id}{p.arxiv_version}"
    if p.doi:
        return f"doi:{p.doi}"
    return ""


def claim_to_md(c: Claim, *, paper_ref: str = "") -> str:
    d = asdict(c)
    if paper_ref:
        d["paper_ref"] = paper_ref           # denormalized id so the chunk resolves standalone (FMT-8)
    tail = f"\n\n— [[{c.paper}]]" + (f" ({paper_ref})" if paper_ref else "")
    return _fm(d, f"{c.statement}\n\n> {c.supporting_passage}{tail}")


def claim_from_md(text: str) -> Claim:
    fm, _ = _split(text)
    return Claim(**{k: fm.get(k) for k in
                    ("id", "statement", "paper", "supporting_passage", "claim_type", "confidence")},
                 corroborated_by=list(fm.get("corroborated_by") or []))


def problem_to_md(op: OpenProblem, *, refs: dict | None = None) -> str:
    refs = refs or {}
    d = asdict(op)
    if refs:
        d["flagged_by_ids"] = [refs[k] for k in op.flagged_by if refs.get(k)]
    links = ", ".join(f"[[{k}]]" + (f" ({refs[k]})" if refs.get(k) else "") for k in op.flagged_by)
    body = f"{op.statement}\n\n**Why it matters:** {op.why_it_matters}\n\n**Flagged by:** {links}"
    return _fm(d, body)


def benchmark_to_md(b: "Benchmark") -> str:
    body = (f"**{b.name}** — {b.method or '?'} achieves **{b.value}** {b.metric}"
            f"{f' on {b.dataset}' if b.dataset else ''}.\n\n— [[{b.paper}]]")
    return _fm(asdict(b), body)


def benchmark_from_md(text: str) -> "Benchmark":
    fm, _ = _split(text)
    return Benchmark(id=fm["id"], name=fm.get("name", ""), dataset=fm.get("dataset", ""),
                     metric=fm.get("metric", ""), value=str(fm.get("value", "")),
                     method=fm.get("method", ""), paper=fm.get("paper", ""))


def problem_from_md(text: str) -> OpenProblem:
    fm, _ = _split(text)
    return OpenProblem(id=fm["id"], statement=fm.get("statement", ""),
                       flagged_by=list(fm.get("flagged_by") or []),
                       status=fm.get("status", "open"), why_it_matters=fm.get("why_it_matters", ""))


def debate_to_md(d: Debate) -> str:
    body_lines = [d.question, ""]
    for pos in d.positions:
        links = ", ".join(f"[[{k}]]" for k in pos.papers)
        body_lines.append(f"### {pos.stance}\n{pos.summary}\n\n*Held by:* {links}\n")
    return _fm(asdict(d), "\n".join(body_lines))


def debate_from_md(text: str) -> Debate:
    fm, _ = _split(text)
    positions = [Position(stance=p.get("stance", ""), papers=list(p.get("papers") or []),
                          summary=p.get("summary", "")) for p in (fm.get("positions") or [])]
    return Debate(id=fm["id"], question=fm.get("question", ""), positions=positions,
                  resolved=bool(fm.get("resolved", False)))
