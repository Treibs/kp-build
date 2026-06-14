"""Falsification harness — does the package actually help, or is it ceremony?

It compares a BASE agent (no package) against a KP-LOADED agent on a held-out task and scores each
answer on TWO axes, not one:

- **precision / citation integrity** — what fraction of the cited papers actually EXIST. A resolvable
  arXiv id or DOI counts as real regardless of the human-supplied title (the id IS the identity);
  a title-only cite must strictly match a real work. This is the anti-hallucination metric.
- **recall / coverage** — what fraction of the package's verified spine the answer actually used. A
  base agent that knows the field may cite real papers (high precision) but miss the spine (low
  recall); a KP-loaded agent should do both.

f1 of the two is the headline. The objective core is still that a base agent's *fabricated* papers
show up as precision < 1, while a KP-loaded agent that stays on the verified spine scores precision 1.
"""

from __future__ import annotations

import re
from pathlib import Path

from .citations import (
    _http_get, _arxiv_title, _crossref_doi_title, _crossref_search_strict,
)

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

_ARXIV_RE = re.compile(r"\b(\d{4}\.\d{4,5})(v\d+)?\b")
_DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s|)\]]+)", re.I)


def make_prompts(pkg_dir: str | Path, question: str) -> dict:
    ctx = (Path(pkg_dir) / "CONTEXT.md").read_text(encoding="utf-8")
    task = _TASK.format(question=question)
    return {"base": task, "kp": _INSTR_KP.format(context=ctx) + task}


def parse_citations(answer: str) -> list[tuple[str, str]]:
    """Pull (handle, title) pairs. Reads the '## Citations' pipe block AND any arXiv ids / DOIs that
    appear inline in the prose (so a non-pipe or numbered list still counts), deduped by handle."""
    out: list[tuple[str, str]] = []
    seen: set = set()

    m = re.search(r"##\s*Citations\s*(.+)$", answer, re.S | re.I)
    block = m.group(1) if m else ""
    for line in block.splitlines():
        if "|" not in line:
            continue
        handle, title = line.split("|", 1)
        handle = re.sub(r"^[-*•·\s]+", "", handle)
        handle = re.sub(r"^\d+[.)]\s+(?=\D)", "", handle).strip()  # ordered marker, not an arxiv id
        key = handle.lower() or title.strip().lower()
        if key not in seen:
            seen.add(key)
            out.append((handle, title.strip()))

    # inline ids/DOIs anywhere (catch cites not in a clean block)
    for mobj in _ARXIV_RE.finditer(answer):
        h = mobj.group(1)
        if h.lower() not in seen:
            seen.add(h.lower()); out.append((h, ""))
    for mobj in _DOI_RE.finditer(answer):
        h = mobj.group(1).rstrip(".,);")
        if h.lower() not in seen:
            seen.add(h.lower()); out.append((h, ""))
    return out


def _handle_kind(handle: str) -> str:
    if re.match(r"^\s*(arxiv:)?\d{4}\.\d{4,5}", handle, re.I):
        return "arxiv"
    if re.search(r"10\.\d{4,9}/", handle):
        return "doi"
    return "title"


def _is_real(handle: str, title: str, get=_http_get) -> bool:
    """A cited paper is REAL if its id/DOI resolves (regardless of the human title), or — title-only —
    it strictly matches a real work."""
    kind = _handle_kind(handle)
    if kind == "arxiv":
        ct, err = _arxiv_title(handle.replace("arxiv:", "").replace("arXiv:", "").strip(), get)
        return bool(ct) if err == "" else False
    if kind == "doi":
        ct, err = _crossref_doi_title(handle.strip(), get)
        return bool(ct) if err == "" else False
    hit, err = _crossref_search_strict(title or handle, get)
    return bool(hit) if err == "" else False


def score_citations(answer: str, *, get=_http_get) -> dict:
    """Precision / integrity: how many cited papers actually exist."""
    cites = parse_citations(answer)
    fake = [f"{h} | {t}" for h, t in cites if not _is_real(h, t, get)]
    n = len(cites)
    return {"cited": n, "real": n - len(fake), "fake": len(fake), "fake_list": fake,
            "precision": (n - len(fake)) / n if n else 0.0,
            "hallucination_rate": (len(fake) / n) if n else 0.0}


def _spine_handles(spine: list[dict]) -> list[set]:
    """For each spine paper, the set of recognizable handles (arxiv id / doi, lowercased)."""
    out = []
    for p in spine:
        hs = set()
        if p.get("arxiv_id"):
            hs.add(re.sub(r"v\d+$", "", p["arxiv_id"].lower().strip()))
        if p.get("doi"):
            hs.add(p["doi"].lower().strip())
        out.append(hs)
    return out


def score_answer(answer: str, *, spine: list[dict] | None = None, get=_http_get) -> dict:
    """Full score: precision (integrity) + recall (coverage of the verified spine) + f1.

    *spine* is a list of the package's VERIFIED papers as {arxiv_id, doi, cite_key}. recall = fraction
    of spine papers the answer cited. f1 balances not-hallucinating with actually-using-the-field.
    """
    base = score_citations(answer, get=get)
    cited_handles = {h.lower().strip() for h, _ in parse_citations(answer)}
    cited_handles |= {re.sub(r"v\d+$", "", h) for h in cited_handles}
    recall, covered = None, None
    if spine:
        sh = _spine_handles(spine)
        covered = sum(1 for hs in sh if hs & cited_handles)
        recall = covered / len(spine) if spine else 0.0
    p = base["precision"]
    f1 = (2 * p * recall / (p + recall)) if (recall is not None and (p + recall) > 0) else None
    return {**base, "recall": recall, "spine_covered": covered, "spine_size": len(spine) if spine else 0,
            "f1": round(f1, 3) if f1 is not None else None}


def verdict(base_report: dict, kp_report: dict) -> str:
    """One-line comparison. Prefers f1 (precision+recall) when available, else precision."""
    if kp_report.get("cited", 0) == 0:
        return "INCONCLUSIVE — the KP answer cited nothing; check the task ran."
    if base_report.get("f1") is not None and kp_report.get("f1") is not None:
        b, k = base_report["f1"], kp_report["f1"]
        verb = "HELPS" if k > b else ("TIES" if k == b else "DID NOT HELP")
        return (f"KP {verb} — f1 {b:.2f} (base) → {k:.2f} (KP). "
                f"precision {base_report['precision']:.2f}→{kp_report['precision']:.2f}, "
                f"recall {base_report.get('recall',0):.2f}→{kp_report.get('recall',0):.2f}, "
                f"{base_report['fake']} fake cites in base vs {kp_report['fake']} in KP.")
    b, k = base_report["hallucination_rate"], kp_report["hallucination_rate"]
    if k < b:
        return f"KP HELPS on integrity — hallucination {b:.0%} (base) → {k:.0%} (KP); {base_report['fake']} fakes avoided."
    if k == b == 0:
        return "TIE on citation integrity (both clean) — compare recall/coverage and open-problem quality."
    return f"KP DID NOT HELP on integrity ({b:.0%} → {k:.0%}) — deepen the survey or rethink."
