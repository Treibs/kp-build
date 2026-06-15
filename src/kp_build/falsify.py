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
import time
from pathlib import Path

from .citations import (
    _http_get, _arxiv_title, _crossref_doi_title, _crossref_search_strict,
    titles_match_strict, _meaningful, _resolve, strip_arxiv_prefix,
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


def probe_prompt(question: str) -> str:
    """The unaided base-answer task for a topic PRE-SCREEN — no package (that's the point). Dispatch
    one agent with this; its answer reveals whether the model already knows the field or fabricates."""
    return _TASK.format(question=question)


def _norm_handle(h: str) -> str:
    """Dedup/identity key for a citation or spine handle: strip a leading 'arxiv:' (any case),
    lowercase, and strip a trailing arXiv version (vN) — but NEVER on a DOI (a DOI contains '/' and a
    trailing 'vN' there is part of the identifier, not a version). ONE normalization, applied
    identically to the cited side AND the spine side so their handle sets actually intersect."""
    s = strip_arxiv_prefix(h).lower()
    return s if "/" in s else re.sub(r"v\d+$", "", s)


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
        handle = strip_arxiv_prefix(handle)
        key = _norm_handle(handle) or title.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append((handle, title.strip()))

    m = re.search(r"##\s*Citations\s*(.+)$", answer, re.S | re.I)
    for line in (m.group(1) if m else "").splitlines():
        line = re.sub(r"^[-*•·\s]+", "", line).strip()
        line = re.sub(r"^\d+[.)]\s+", "", line)                      # ordered-list marker (also before an id)
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


def _is_real(handle: str, title: str, get=_http_get, *, sleep=time.sleep, max_retries: int = 2):
    """Tri-state. REAL (True) iff the id/DOI resolves AND — when a title is supplied — the canonical
    title strictly matches it (a 'real id, wrong paper' mislabel is False, mirroring the build gate).
    Returns None when the index can't be reached (transient error after retries) so the caller can
    EXCLUDE it — a rate-limit burst must not be scored as a fabrication. Transient errors are retried
    with backoff exactly like the build gate (it shares _resolve)."""
    kind = _handle_kind(handle)
    if kind == "arxiv":
        ct, err = _resolve(_arxiv_title, strip_arxiv_prefix(handle), get=get, sleep=sleep, max_retries=max_retries)
    elif kind == "doi":
        ct, err = _resolve(_crossref_doi_title, handle.strip(), get=get, sleep=sleep, max_retries=max_retries)
    else:
        hit, err = _resolve(_crossref_search_strict, title or handle, get=get, sleep=sleep, max_retries=max_retries)
        return None if err == "transient" else bool(hit)
    if err == "transient":
        return None
    return _title_ok(title, ct) if ct else False


def score_citations(answer: str, *, get=_http_get) -> dict:
    """Precision / integrity: of the cited papers we could CHECK, how many actually exist and are the
    paper named. Citations the index couldn't resolve (transient) are excluded from the denominator so
    a rate-limited run neither inflates nor deflates precision."""
    cites = parse_citations(answer)
    verdicts = [(h, t, _is_real(h, t, get)) for h, t in cites]
    checkable = [(h, t, v) for h, t, v in verdicts if v is not None]
    fake = [f"{h} | {t}" for h, t, v in checkable if not v]
    n = len(checkable)
    return {"cited": len(cites), "checked": n, "unresolved": len(cites) - n,
            "real": n - len(fake), "fake": len(fake), "fake_list": fake,
            "precision": (n - len(fake)) / n if n else 0.0,
            "hallucination_rate": (len(fake) / n) if n else 0.0}


def _spine_handles(spine: list[dict]) -> list[set]:
    """For each spine paper, the set of recognizable handles (arxiv id / doi, lowercased)."""
    out = []
    for p in spine:
        hs = set()
        if p.get("arxiv_id"):
            hs.add(_norm_handle(p["arxiv_id"]))        # same normalization as the cited side
        if p.get("doi"):
            hs.add(_norm_handle(p["doi"]))             # identical normalization to the cited side
        out.append(hs)
    return out


def score_answer(answer: str, *, spine: list[dict] | None = None, get=_http_get) -> dict:
    """Full score: precision (integrity) + recall (coverage of the verified spine) + f1.

    *spine* is a list of the package's VERIFIED papers as {arxiv_id, doi, cite_key}. recall = fraction
    of spine papers the answer cited. f1 balances not-hallucinating with actually-using-the-field.
    """
    base = score_citations(answer, get=get)
    cited_handles = {_norm_handle(h) for h, _ in parse_citations(answer)}
    recall, covered = None, None
    if spine:
        sh = _spine_handles(spine)
        covered = sum(1 for hs in sh if hs & cited_handles)
        recall = covered / len(spine) if spine else 0.0
    p = base["precision"]
    f1 = (2 * p * recall / (p + recall)) if (recall is not None and (p + recall) > 0) else None
    return {**base, "recall": recall, "spine_covered": covered, "spine_size": len(spine) if spine else 0,
            "f1": round(f1, 3) if f1 is not None else None}


def probe_verdict(base_answer: str, *, get=_http_get, threshold: float = 0.25, min_real: int = 3) -> dict:
    """PRE-FLIGHT: should we even build a package for this topic? Score an UNAIDED agent's answer.

    The value of a package appears only where the model is WEAK — and weakness shows up as the base
    agent FABRICATING or MISLABELING citations, or being unable to ground at all. So:
      - cited nothing, or grounded < min_real real papers  -> BUILD (the model lacks the field)
      - hallucination rate >= threshold                    -> BUILD (the model invents/mislabels here)
      - cites >= min_real real papers cleanly, low fabrication -> SKIP (it already knows this; a package
        adds ~0 value — the same topics that TIED in falsification)
      - the index was unreachable                          -> INCONCLUSIVE (re-run)
    Returns the citation report plus {decision, reason}. Decision in {build, skip, inconclusive}."""
    rep = score_citations(base_answer, get=get)
    cited, checked, real, fake = rep["cited"], rep["checked"], rep["real"], rep["fake"]
    hall = rep["hallucination_rate"]
    if cited == 0:
        decision, reason = "build", "the unaided model cited no real papers at all — it lacks this field; a package will help"
    elif checked == 0:
        decision, reason = "inconclusive", "could not reach the citation index to check the base answer — re-run"
    elif hall >= threshold:
        decision, reason = "build", (f"the unaided model fabricates/mislabels {fake}/{checked} citations "
                                     f"({hall:.0%}) — it is weak on this topic; a verified package will help")
    elif real < min_real:
        decision, reason = "build", (f"the unaided model grounded only {real} real citation(s) — too thin; "
                                     f"a package will help")
    else:
        decision, reason = "skip", (f"the unaided model already cites {real} real papers cleanly "
                                    f"({hall:.0%} fabrication) — it knows this field; a package adds little value")
    return {**rep, "decision": decision, "reason": reason, "threshold": threshold, "min_real": min_real}


def verdict(base_report: dict, kp_report: dict) -> str:
    """One-line comparison. Prefers f1 (precision+recall) when available, else precision."""
    if kp_report.get("cited", 0) == 0:
        return "INCONCLUSIVE — the KP answer cited nothing; check the task ran."
    if base_report.get("checked") == 0 or kp_report.get("checked") == 0:
        # every cited id was unreachable (index outage) — precision/f1 here is 0-by-default, not earned
        return "INCONCLUSIVE — citations could not be verified (citation index unreachable); re-run."
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
