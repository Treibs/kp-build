"""Falsification harness — does the package actually help, or is it ceremony?

It compares a BASE agent (no package) against a KP-LOADED agent on a held-out task and scores each
answer on TWO axes, not one:

- **precision / citation integrity** — what fraction of the cited papers actually exist AND are the
  paper the answer names. A resolvable arXiv id / DOI is real ONLY if its canonical title strictly
  matches the claimed title (so a real id bearing the WRONG paper's title — a mislabel — counts as a
  hallucination, mirroring the build-time citation gate). An id cited with no title falls back to
  existence (nothing to match); a title-only cite must strictly match a real work. This is the
  anti-hallucination metric.
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
    titles_match_strict, _meaningful,
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


def _norm_handle(h: str) -> str:
    """Dedup key for a citation handle: strip a leading 'arxiv:' and any version suffix, lowercase."""
    h = re.sub(r"(?i)^\s*arxiv:\s*", "", h.strip())
    return re.sub(r"v\d+$", "", h.lower())


_SEP_RE = re.compile(r"\s*(?:\||—|–|\s-\s)\s*")                       # block handle↔title separators
_LEAD_ID_RE = re.compile(r"(?i)\s*((?:arxiv:)?\d{4}\.\d{4,5}(?:v\d+)?|10\.\d{4,9}/\S+)\s+(.*)")


def parse_citations(answer: str) -> list[tuple[str, str]]:
    """Pull (handle, title) pairs. Reads the '## Citations' block — handle and title separated by
    '|', '—', '–', or ' - ' (or just whitespace after a leading id) — AND any arXiv ids / DOIs inline
    in the prose, deduped by normalized handle. A *titled* block entry is recorded before the bare
    inline scan, so the title survives to be strict-checked rather than lost to an untitled duplicate."""
    out: list[tuple[str, str]] = []
    seen: set = set()

    def add(handle: str, title: str):
        handle = re.sub(r"(?i)^\s*arxiv:\s*", "", handle.strip())
        key = _norm_handle(handle) or title.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append((handle, title.strip()))

    m = re.search(r"##\s*Citations\s*(.+)$", answer, re.S | re.I)
    for line in (m.group(1) if m else "").splitlines():
        line = re.sub(r"^[-*•·\s]+", "", line).strip()
        line = re.sub(r"^\d+[.)]\s+(?=\D)", "", line)                # ordered marker, not an id
        if not line:
            continue
        sep = _SEP_RE.search(line)
        if sep:
            add(line[:sep.start()], line[sep.end():])
        else:
            mid = _LEAD_ID_RE.match(line)
            add(*(mid.groups() if mid else (line, "")))

    # inline ids/DOIs anywhere (catch cites not in a clean block); untitled, so existence-only
    for mobj in _ARXIV_RE.finditer(answer):
        add(mobj.group(1), "")
    for mobj in _DOI_RE.finditer(answer):
        add(mobj.group(1).rstrip(".,);"), "")
    return out


def _handle_kind(handle: str) -> str:
    if re.match(r"^\s*(arxiv:)?\d{4}\.\d{4,5}", handle, re.I):
        return "arxiv"
    if re.search(r"10\.\d{4,9}/", handle):
        return "doi"
    return "title"


def _title_ok(claimed: str, canonical: str) -> bool:
    """Gate a resolved id's claimed title against its canonical one. An uninformative claimed title
    (no meaningful tokens) falls back to existence. Otherwise accept iff the titles strictly match in
    EITHER direction: claimed⊇canonical tolerates a legitimate annotation ('(LLaDA)', '(SEDD)') on a
    short title, canonical⊇claimed tolerates a truncated subtitle — but a DIFFERENT paper's title
    (low overlap both ways) is rejected as a mislabel. Mirrors the build gate's title strictness while
    not punishing the annotations agents naturally add in a citations list."""
    if not _meaningful(claimed):
        return True
    return titles_match_strict(claimed, canonical)[0] or titles_match_strict(canonical, claimed)[0]


def _is_real(handle: str, title: str, get=_http_get) -> bool:
    """REAL iff the id/DOI resolves AND — when a title is supplied — the canonical title strictly
    matches it. A 'real id, wrong paper' mislabel is therefore NOT real (mirrors the build gate). A
    title-only cite must strictly match a real work."""
    kind = _handle_kind(handle)
    if kind == "arxiv":
        ct, err = _arxiv_title(re.sub(r"(?i)^arxiv:", "", handle).strip(), get)
        return _title_ok(title, ct) if (err == "" and ct) else False
    if kind == "doi":
        ct, err = _crossref_doi_title(handle.strip(), get)
        return _title_ok(title, ct) if (err == "" and ct) else False
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
