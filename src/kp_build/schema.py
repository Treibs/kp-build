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
DIRECTIONS = ("lower", "higher")                       # GoalMetric: which way is better
ORACLE_KINDS = ("execution", "grounding", "none")      # GoalMetric: how a KPI is measured by falsify
RELATION_TYPES = ("tradeoff", "explains", "contradicts", "refines", "enables",
                  "addresses", "supports", "derives-from")

_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(text: str, *, max_words: int = 8) -> str:
    """Deterministic id slug: lowercase, hyphenated, first ``max_words`` words."""
    cleaned = _SLUG.sub("-", text.lower()).strip("-")
    words = [w for w in cleaned.split("-") if w]
    return "-".join(words[:max_words]) or "node"


# ── nodes ───────────────────────────────────────────────────────────────────────


@dataclass
class Verification:
    """Result of checking a node against SOME oracle — verifier-agnostic (V2-a §4.0).

    ``exists`` is the UNIVERSAL ship gate across every ``kind``: True only for a STRONG verdict.
    For citation (``kind='existence'``, the default) that means an explicit identifier (arXiv id /
    DOI) that resolves AND whose canonical title strictly matches — a title-only hit is
    ``status='unconfirmed'``/``exists=False`` so a fabricated title can't launder against an
    unrelated real work. Other kinds carry their own evidence in ``evidence`` and source tag in
    ``via`` (e.g. ``hyperframes-cli@0.6.91``, ``astm-d570``).

    ``kind``    : existence | execution | grounding | unverifiable-aesthetic | ungrounded-unreachable
                  (grounding = declared; the DocGroundingVerifier is a library block, not yet build-enforced)
    ``status``  : verified | unconfirmed | id-title-mismatch | not-found | error | unverified
                  | output-mismatch        (execution: ran clean but produced the wrong output)
    ``canonical_title`` / ``match_score`` are citation-specific (empty/0.0 for other kinds).
    Legacy packages have no ``kind`` in frontmatter → it reads back as ``existence`` (the migration).
    """

    exists: bool = False
    status: str = "unverified"
    kind: str = "existence"           # verifier kind (default keeps academic packs unchanged)
    via: str = "unverified"           # source tag: "arxiv" | "crossref" | "hyperframes-cli@…" | "astm-…" | "unverified"
    canonical_title: str = ""         # citation-only
    match_score: float = 0.0          # citation-only
    evidence: str = ""                # non-citation evidence (gate codes / quoted passage / …)
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
    #: did the claim survive a refuter pass (tried to break it with the beat's OTHER sources)?
    #: True if no refuter ran (v1 default) or it survived; False = a refuter broke it (shown capped/flagged)
    survived_refuter: bool = True
    #: passage-presence grounding: was the supporting_passage machine-confirmed in the cited paper?
    #: unchecked (default) | grounded (found) | unconfirmed (not in abstract; maybe body) | ungrounded
    #: (checked fulltext, not there — capped/flagged)
    grounded: str = "unchecked"
    #: V2-a per-claim verifier verdict — for execution/grounding claims that carry their OWN verdict
    #: instead of inheriting from an anchoring Paper. Default (exists=False) = academic claim, which ships
    #: via its Paper unchanged. A claim ships iff (its Paper is verified) OR (this verdict exists).
    verified: Verification = field(default_factory=Verification)
    #: V2-a execution directive (optional) — {tool, gate_code, artifact, aesthetic?}. When present, the build
    #: runs the ExecutionVerifier on it and sets ``verified``. Empty for citation/academic claims.
    execution: dict = field(default_factory=dict)
    #: V2-b grounding directive (optional) — {source, supporting_passage}. When present and the build runs
    #: with ``--ground-verify``, the DocGroundingVerifier checks the passage against the pinned source's
    #: corpus and sets ``verified``. Empty for citation/academic/execution claims.
    grounding: dict = field(default_factory=dict)


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
class GoalMetric:
    """A measurable KPI the package is scoped around (V2-a §4.1) — the goal/KPI-anchored scope.

    ``oracle_kind`` tells falsify how the KPI is graded: ``execution`` = a mechanical run measures it
    directly; ``grounding``/``none`` = no run-oracle, so the does-it-help signal degrades to
    cited-property recall (a grounding delta, NOT independent field performance — see the design review).
    """

    name: str
    description: str = ""
    baseline: str = ""
    target: str = ""
    direction: str = "higher"         # lower | higher (which way is better)
    unit: str = ""
    acceptance_threshold: str = ""
    measurement_method: str = ""
    oracle_kind: str = "none"         # execution | grounding | none


def goal_metric_from_dict(d: dict) -> "GoalMetric":
    return GoalMetric(
        name=d.get("name", ""), description=d.get("description", ""),
        baseline=str(d.get("baseline", "")), target=str(d.get("target", "")),
        direction=d.get("direction") or "higher", unit=d.get("unit", ""),
        acceptance_threshold=str(d.get("acceptance_threshold", "")),
        measurement_method=d.get("measurement_method", ""),
        oracle_kind=d.get("oracle_kind") or "none")


@dataclass
class Relation:
    """A first-class, KPI-anchored, verifiable edge BETWEEN nodes (V2-a §4.2).

    The doctrine's value is the connections, not the star: a ``Relation`` is a directed tradeoff/causal
    edge that must span **≥2 KPIs** (the spine those KPIs explain) and carry its OWN verification verdict
    (execution-confirmed for a mechanical edge, doc-grounded for a doctrinal one). ``source``/``target``
    are node ids (claim id or cite_key).
    """

    id: str
    source: str
    target: str
    type: str = "related"             # see RELATION_TYPES
    description: str = ""
    confidence: str = "medium"
    kpis: List[str] = field(default_factory=list)            # ≥2 KPI names this edge connects
    verification: Verification = field(default_factory=Verification)


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
    #: V2-a KP-model spine (optional — academic packs leave these empty and stay valid):
    goals: dict = field(default_factory=dict)                       # {goal_id: description}
    goal_metrics: List[GoalMetric] = field(default_factory=list)    # the KPIs scope is measured against
    relations: List[Relation] = field(default_factory=list)         # first-class KPI-anchored edges


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
                                 ("exists", "status", "kind", "via", "canonical_title",
                                  "match_score", "evidence", "checked")
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
    if c.paper:                              # citation/academic claim: link to its Paper
        tail = f"\n\n— [[papers/{c.paper}]]" + (f" ({paper_ref})" if paper_ref else "")
    elif c.verified.exists:                  # execution/grounding claim: cite its own verdict
        tail = f"\n\n— *{c.verified.kind} verified* via {c.verified.via}: {c.verified.evidence}"
    else:
        tail = ""
    return _fm(d, f"{c.statement}\n\n> {c.supporting_passage}{tail}")


def claim_from_md(text: str) -> Claim:
    fm, _ = _split(text)
    v = fm.get("verified") or {}
    # use dataclass defaults for absent keys — never override with None (F3, symmetric round-trip)
    return Claim(
        id=fm.get("id", ""), statement=fm.get("statement", ""), paper=fm.get("paper", ""),
        supporting_passage=fm.get("supporting_passage", ""),
        claim_type=fm.get("claim_type") or "finding", confidence=fm.get("confidence") or "medium",
        corroborated_by=list(fm.get("corroborated_by") or []),
        survived_refuter=bool(fm.get("survived_refuter", True)),
        grounded=fm.get("grounded") or "unchecked",
        verified=Verification(**{k: v.get(k) for k in
                                 ("exists", "status", "kind", "via", "canonical_title",
                                  "match_score", "evidence", "checked") if k in v}),
        execution=dict(fm.get("execution") or {}),
        grounding=dict(fm.get("grounding") or {}))


def claim_ships(c: "Claim", verified_keys) -> bool:
    """The SINGLE ship rule for a claim (V2-a) — shared by assemble + digest so they can't drift.
    A claim's OWN verdict is authoritative: a verifier that ran and FAILED vetoes; else it ships iff its
    Paper is in the verified citation spine. (``verified_keys`` may be a set or a dict keyed by cite_key.)"""
    v = c.verified
    if v.exists:
        return True
    if v.status not in ("unverified", ""):
        return False
    return c.paper in verified_keys


def problem_to_md(op: OpenProblem, *, refs: dict | None = None) -> str:
    refs = refs or {}
    d = asdict(op)
    if refs:
        d["flagged_by_ids"] = [refs[k] for k in op.flagged_by if refs.get(k)]
    links = ", ".join(f"[[papers/{k}]]" + (f" ({refs[k]})" if refs.get(k) else "") for k in op.flagged_by)
    body = f"{op.statement}\n\n**Why it matters:** {op.why_it_matters}\n\n**Flagged by:** {links}"
    return _fm(d, body)


def benchmark_to_md(b: "Benchmark") -> str:
    body = (f"**{b.name}** — {b.method or '?'} achieves **{b.value}** {b.metric}"
            f"{f' on {b.dataset}' if b.dataset else ''}.\n\n— [[papers/{b.paper}]]")
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
        links = ", ".join(f"[[papers/{k}]]" for k in pos.papers)
        body_lines.append(f"### {pos.stance}\n{pos.summary}\n\n*Held by:* {links}\n")
    return _fm(asdict(d), "\n".join(body_lines))


def debate_from_md(text: str) -> Debate:
    fm, _ = _split(text)
    positions = [Position(stance=p.get("stance", ""), papers=list(p.get("papers") or []),
                          summary=p.get("summary", "")) for p in (fm.get("positions") or [])]
    return Debate(id=fm["id"], question=fm.get("question", ""), positions=positions,
                  resolved=bool(fm.get("resolved", False)))


def relation_to_md(r: "Relation") -> str:
    d = asdict(r)
    body = (f"{r.description}\n\n[[{r.source}]] —{r.type}→ [[{r.target}]]"
            f"  ·  KPIs: {', '.join(r.kpis)}")
    return _fm(d, body)


def relation_from_md(text: str) -> "Relation":
    fm, _ = _split(text)
    v = fm.get("verification") or {}
    return Relation(
        id=fm.get("id", ""), source=fm.get("source", ""), target=fm.get("target", ""),
        type=fm.get("type") or "related", description=fm.get("description", ""),
        confidence=fm.get("confidence") or "medium", kpis=list(fm.get("kpis") or []),
        verification=Verification(**{k: v.get(k) for k in
                                     ("exists", "status", "kind", "via", "canonical_title",
                                      "match_score", "evidence", "checked") if k in v}))
