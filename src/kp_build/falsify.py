"""Falsification harness — does the package actually help, or is it ceremony?

The gate compares a BASE agent (no package) against a KP-LOADED agent (CONTEXT.md in context) on a
held-out task, and scores each answer's citations against the REAL index. The objective,
automatable metric is the **citation hallucination rate**: base agents invent plausible-but-fake
papers; a KP-loaded agent should cite only real ones from the verified spine. That single number is
the clearest evidence the package adds value.

Usage (the orchestrator dispatches the two answer-generating subagents, then scores):
    from kp_build.falsify import make_prompts, score_citations
    prompts = make_prompts(pkg_dir, question)          # -> {"base":..., "kp":...}
    # dispatch a subagent with prompts["base"] and another with prompts["kp"];
    # each must end with a "## Citations" block of "arxiv_id | title" lines.
    report = score_citations(base_answer)              # -> hallucination metrics
"""

from __future__ import annotations

import re
from pathlib import Path

from .citations import _http_get, _arxiv_title, _crossref_search, titles_match

_TASK = (
    "Write a tight related-work paragraph for the research area below, then list the 3 most "
    "important OPEN PROBLEMS in it. Cite specific real papers. "
    "End your answer with a section exactly like:\n\n## Citations\n"
    "<arxiv_id or DOI> | <paper title>\n(one per line, only papers you actually cited)\n\n"
    "Research area: {question}\n"
)

_INSTR_KP = (
    "You have been given a verified knowledge package (a field briefing) below. Use ONLY the papers "
    "it lists — every one has been verified to exist. Do not invent citations beyond this list.\n\n"
    "=== FIELD BRIEFING (CONTEXT.md) ===\n{context}\n=== END BRIEFING ===\n\n"
)


def make_prompts(pkg_dir: str | Path, question: str) -> dict:
    """Return {'base': prompt, 'kp': prompt}. The KP prompt injects the package's CONTEXT.md."""
    ctx = (Path(pkg_dir) / "CONTEXT.md").read_text(encoding="utf-8")
    task = _TASK.format(question=question)
    return {"base": task, "kp": _INSTR_KP.format(context=ctx) + task}


def parse_citations(answer: str) -> list[tuple[str, str]]:
    """Pull (handle, title) pairs from the answer's '## Citations' block."""
    m = re.search(r"##\s*Citations\s*(.+)$", answer, re.S | re.I)
    block = m.group(1) if m else answer
    out = []
    for line in block.splitlines():
        if "|" not in line:
            continue
        handle, title = line.split("|", 1)
        # strip only leading bullet/list markers (never the digits of an arxiv id)
        handle = handle.strip().lstrip("-*•· ").strip()
        handle = re.sub(r"^\d+\.\s+(?=\D)", "", handle)  # ordered-list "1. " but not "1706.03762"
        if handle or title.strip():
            out.append((handle, title.strip()))
    return out


def _is_real(handle: str, title: str, get=_http_get) -> bool:
    h = handle.strip()
    if re.match(r"^\d{4}\.\d{4,5}", h) or h.lower().startswith("arxiv"):
        ct = _arxiv_title(h, get)
        return bool(ct and titles_match(title or ct, ct))
    # treat as title search (covers DOIs loosely + bare titles)
    return _crossref_search(title or h, get) is not None


def score_citations(answer: str, *, get=_http_get) -> dict:
    """Check every cited paper in *answer* against the real index.

    Returns {cited, real, fake, fake_list, hallucination_rate}. This is the objective metric:
    a base agent's fakes show up here; a KP-loaded agent that stayed on the verified spine scores 0.
    """
    cites = parse_citations(answer)
    fake = []
    for handle, title in cites:
        if not _is_real(handle, title, get):
            fake.append(f"{handle} | {title}")
    n = len(cites)
    return {"cited": n, "real": n - len(fake), "fake": len(fake), "fake_list": fake,
            "hallucination_rate": (len(fake) / n) if n else 0.0}


def verdict(base_report: dict, kp_report: dict) -> str:
    """A one-line human verdict comparing the two answers' citation integrity."""
    b, k = base_report["hallucination_rate"], kp_report["hallucination_rate"]
    if kp_report["cited"] == 0:
        return "INCONCLUSIVE — the KP answer cited nothing; check the task ran."
    if k < b:
        return (f"KP HELPS — hallucination rate {b:.0%} (base) → {k:.0%} (KP-loaded); "
                f"{base_report['fake']} fake cites avoided.")
    if k == b == 0:
        return "TIE on citations (both clean) — judge on coverage/usefulness of the open problems."
    return f"KP DID NOT HELP on citations ({b:.0%} → {k:.0%}) — deepen the survey or rethink."
