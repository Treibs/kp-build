"""Citation-graph expansion — find what a keyword survey missed.

One keyword search per beat is breadth-limited: it can't see a seminal paper that uses different
terminology, or the latest work that cites the seeds. After wave 1 verifies a set of SEED papers, this
module pulls their references (what they cite) and citations (what cites them) from the Semantic
Scholar Graph API (keyless, like arXiv/Crossref), so the orchestration can verify the on-topic
neighbors and fold them in. It returns RAW candidates only — relevance is a judgment call left to the
orchestration, and existence is still re-checked by the citation gate. Mechanical discovery, nothing
laundered: a candidate becomes a spine paper only after the gate verifies it.
"""

from __future__ import annotations

import json
import time
from typing import Callable
from urllib.parse import quote

from .citations import _http_get, _safe, _resolve, strip_arxiv_prefix

_S2 = "https://api.semanticscholar.org/graph/v1/paper/"
_FIELDS = "title,year,externalIds"
DIRECTIONS = ("references", "citations")


def _paper_path(handle: str) -> str:
    """Map an arXiv id or DOI to a Semantic Scholar paper path."""
    h = strip_arxiv_prefix(handle).strip()
    if h.lower().startswith("10.") and "/" in h:
        return "DOI:" + h
    return "arXiv:" + h


def _parse(text: str, field: str) -> list[dict]:
    """Pull candidate papers out of an S2 references/citations payload. Tolerant of malformed JSON
    and missing fields (returns [] rather than raising)."""
    try:
        data = json.loads(text).get("data", [])
    except (ValueError, TypeError, AttributeError):
        return []
    out = []
    for row in data or []:
        p = (row or {}).get(field) or {}
        ext = p.get("externalIds") or {}
        out.append({"title": p.get("title") or "", "year": p.get("year"),
                    "arxiv_id": ext.get("ArXiv") or "", "doi": (ext.get("DOI") or "").lower()})
    return out


def neighbors(handle: str, *, get: Callable[[str], str] = _http_get, direction: str = "references",
              limit: int = 50, sleep=time.sleep, max_retries: int = 2) -> tuple[list[dict], str]:
    """References (what `handle` cites) or citations (what cites `handle`). Returns (candidates, err);
    err='transient' when the index was unreachable after retries so the caller can proceed degraded."""
    field = "citedPaper" if direction == "references" else "citingPaper"
    # encode the handle before it hits the URL (DOIs carry #, <, >, spaces); keep the prefix colon + slashes
    path = quote(_paper_path(handle), safe=":/")
    url = f"{_S2}{path}/{direction}?fields={_FIELDS}&limit={int(limit)}"
    text, err = _resolve(lambda u, g: _safe(u, g), url, get=get, sleep=sleep, max_retries=max_retries)
    if err == "transient":
        return [], "transient"
    cands = _parse(text or "", field)
    for c in cands:
        c["via"] = direction
    return cands, ""


def expand(seed_handles, *, get: Callable[[str], str] = _http_get, per_seed: int = 40,
           directions=DIRECTIONS, skip=(), sleep=time.sleep) -> list[dict]:
    """Aggregate de-duplicated neighbor candidates across all seeds, excluding any handle already in
    the package (*skip* = its arXiv ids / DOIs). One candidate per distinct paper, preferring an
    identifier (arxiv/doi) as the dedup key and falling back to the title. A seed whose expansion
    fails (transient or otherwise) is skipped — the other seeds still aggregate."""
    skip_norm = {strip_arxiv_prefix(s).strip().lower() for s in skip if s}
    seen: set = set()
    out: list[dict] = []
    for h in seed_handles:
        if not h:
            continue
        for d in directions:
            cands, _ = neighbors(h, get=get, direction=d, limit=per_seed, sleep=sleep)
            for c in cands:
                ident = (c.get("arxiv_id") or c.get("doi") or "").lower()
                key = ident or (c.get("title") or "").strip().lower()
                if not key or key in seen or (ident and ident in skip_norm):
                    continue
                seen.add(key)
                out.append(c)
    return out
