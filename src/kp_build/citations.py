"""Citation verification — the hard gate against hallucinated papers.

A paper is verified by checking it against a REAL index:
1. ``arxiv_id`` → arXiv Atom API (an entry must come back, and its title must match).
2. ``doi``      → Crossref ``/works/{doi}`` (must resolve, title must match).
3. else ``title`` → Crossref bibliographic search (top hit's title must match closely).

"Match" means the claimed title and the index's canonical title are close (token Jaccard ≥ 0.6
or one contains the other), so a real-but-different paper can't masquerade as the cited one. A
paper that fails all three is ``exists=False`` and may not anchor a shipped claim.

HTTP is injected (``get``) so the logic is unit-testable without the network.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from typing import Callable, Optional

from .schema import Paper, Verification

_UA = "kp-build/0.1 (research knowledge package builder)"
_TOK = re.compile(r"[a-z0-9]+")


def _http_get(url: str, *, timeout: float = 20.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # follows redirects by default
        return r.read().decode("utf-8", "replace")


def _norm_tokens(s: str) -> set:
    return set(_TOK.findall(s.lower()))


def titles_match(a: str, b: str, *, threshold: float = 0.6) -> bool:
    """True if two titles plausibly name the same paper."""
    ta, tb = _norm_tokens(a), _norm_tokens(b)
    if not ta or not tb:
        return False
    # A short claimed title that is a token-subset of the canonical (or vice-versa) is the same
    # paper cited by an abbreviated title — accept when the smaller set is meaningful (>=2 words).
    small, big = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if len(small) >= 2 and small <= big:
        return True
    jacc = len(ta & tb) / len(ta | tb)
    return jacc >= threshold


# ── individual index checks ─────────────────────────────────────────────────────


def _arxiv_title(arxiv_id: str, get: Callable[[str], str]) -> Optional[str]:
    aid = arxiv_id.strip().replace("arXiv:", "").strip()
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(aid)}&max_results=1"
    try:
        xml = get(url)
    except Exception:
        return None
    if "<entry>" not in xml:
        return None
    # An id_list miss still returns a feed but with no <entry>. Pull the entry title.
    m = re.search(r"<entry>.*?<title>(.*?)</title>", xml, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def _crossref_doi_title(doi: str, get: Callable[[str], str]) -> Optional[str]:
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi.strip())}"
    try:
        data = json.loads(get(url))
    except Exception:
        return None
    titles = data.get("message", {}).get("title") or []
    return titles[0] if titles else None


def _crossref_search(title: str, get: Callable[[str], str]) -> Optional[tuple[str, str]]:
    """Return (doi, canonical_title) of the best bibliographic match, else None."""
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 3})
    try:
        items = json.loads(get(url)).get("message", {}).get("items") or []
    except Exception:
        return None
    for it in items:
        cand = (it.get("title") or [""])[0]
        if cand and titles_match(title, cand):
            return it.get("DOI", ""), cand
    return None


# ── public API ──────────────────────────────────────────────────────────────────


def verify_paper(p: Paper, *, get: Callable[[str], str] = _http_get, today: str = "") -> Paper:
    """Verify *p* against arXiv/Crossref; set ``p.verified`` (returns the same object).

    Order: arxiv_id, then doi, then a Crossref title search (which can also *backfill* a doi).
    The title must match in every path, so a wrong/fake citation cannot pass.
    """
    p.verified.checked = today

    if p.arxiv_id:
        ct = _arxiv_title(p.arxiv_id, get)
        if ct and titles_match(p.title or ct, ct):
            p.verified = Verification(True, "arxiv", ct, today)
            if not p.url:
                p.url = f"https://arxiv.org/abs/{p.arxiv_id.replace('arXiv:', '').strip()}"
            return p

    if p.doi:
        ct = _crossref_doi_title(p.doi, get)
        if ct and titles_match(p.title or ct, ct):
            p.verified = Verification(True, "crossref", ct, today)
            return p

    if p.title:
        hit = _crossref_search(p.title, get)
        if hit:
            doi, ct = hit
            p.doi = p.doi or doi
            p.verified = Verification(True, "crossref", ct, today)
            return p

    p.verified = Verification(False, "unverified", "", today)
    return p


def verify_all(papers: list[Paper], *, get: Callable[[str], str] = _http_get, today: str = "") -> dict:
    """Verify a list in place; return a summary ``{verified, unverified, ids}``."""
    unv = []
    for p in papers:
        verify_paper(p, get=get, today=today)
        if not p.verified.exists:
            unv.append(p.cite_key)
    return {"total": len(papers), "verified": len(papers) - len(unv), "unverified": unv}
