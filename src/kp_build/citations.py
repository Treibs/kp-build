"""Citation verification — the SOUND hard gate against hallucinated papers.

The previous version laundered fakes: its title-search fallback marked a fabricated paper
``verified`` against an unrelated real work and backfilled a wrong DOI. This version is built so a
fabricated citation can never earn ``exists=True``:

1. **An identifier's verdict is FINAL.** If an ``arxiv_id`` or ``doi`` is supplied, we resolve it and
   either accept (it resolves AND the canonical title strictly matches the claimed title) or reject —
   we NEVER fall through to a title search that could rescue a wrong id to a third paper.
2. **Title-only papers are never ``verified``.** With no identifier the best we can do is a strict
   Crossref search; a hit is recorded as ``status='unconfirmed'`` with ``exists=False`` — it cannot
   anchor a shipped claim. (The drafter must supply an arXiv id / DOI for a shippable citation.)
3. **Strict title match** (no ≥2-word subset shortcut): near-equality OR high coverage with a
   ≥4 meaningful-token floor, so "Language Models" no longer matches "Large Language Models".
4. **Transient errors (429 / timeout / 5xx) are distinguished from a real negative** and retried, so a
   rate limit never silently turns a real paper into ``not-found`` (or a fake into a pass).

HTTP is injected (``get``) so all of this is unit-testable without the network.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable, Optional

from .schema import Paper, Verification

_UA = "kp-build/0.2 (research knowledge package builder)"
_TOK = re.compile(r"[a-z0-9]+")
_STOP = frozenset("a an the of for and or via with in on to is are using based from at as".split())
_RETRYABLE = frozenset({429, 500, 502, 503, 504})


def _http_get(url: str, *, timeout: float = 20.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # follows redirects by default
        return r.read().decode("utf-8", "replace")


# ── title matching ───────────────────────────────────────────────────────────────


def _toks(s: str) -> set:
    return set(_TOK.findall(s.lower()))


def _meaningful(s: str) -> set:
    return {t for t in _toks(s) if t not in _STOP}


def titles_match(a: str, b: str, *, threshold: float = 0.6) -> bool:
    """Loose match (token Jaccard) — used only for ranking search candidates, never to ACCEPT."""
    ta, tb = _toks(a), _toks(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= threshold


def titles_match_strict(claimed: str, canonical: str) -> tuple[bool, float]:
    """STRICT match used to ACCEPT a citation. Returns (ok, score).

    Accept iff the meaningful tokens are near-equal (Jaccard >= 0.85) OR the claimed title is almost
    entirely contained in the canonical one (coverage >= 0.85) AND has >= 4 meaningful tokens — which
    allows a legitimately truncated subtitle but rejects short/generic titles ("Language Models",
    "Deep Learning") and unrelated papers.
    """
    c, k = _meaningful(claimed), _meaningful(canonical)
    if not c or not k:
        return False, 0.0
    inter = len(c & k)
    jacc = inter / len(c | k)
    cover = inter / len(c)
    if c == k or jacc >= 0.85:
        return True, max(jacc, 1.0 if c == k else jacc)
    if cover >= 0.85 and len(c) >= 4:
        return True, cover
    return False, max(jacc, 0.0)


# ── index fetchers: return (value, err) where err in {'', 'transient'} ───────────


def _safe(url: str, get: Callable[[str], str]) -> tuple[Optional[str], str]:
    try:
        return get(url), ""
    except urllib.error.HTTPError as e:
        return None, ("transient" if e.code in _RETRYABLE else "")
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        return None, "transient"
    except Exception:
        return None, ""


def strip_arxiv_prefix(s: str) -> str:
    """Drop a leading 'arXiv:'/'arxiv:' (any case) and surrounding space — so a prefixed id never
    reaches an API URL malformed. Shared by the build gate and the falsify harness."""
    return re.sub(r"(?i)^\s*arxiv:\s*", "", s.strip())


def _arxiv_title(arxiv_id: str, get: Callable[[str], str]) -> tuple[Optional[str], str]:
    aid = strip_arxiv_prefix(arxiv_id)
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(aid, safe='')}&max_results=1"
    raw, err = _safe(url, get)
    if err:
        return None, err
    if not raw or "<entry>" not in raw:
        return None, ""  # definitive: arXiv returned a feed with no entry → id does not exist
    m = re.search(r"<entry>.*?<title>(.*?)</title>", raw, re.S)
    return (re.sub(r"\s+", " ", m.group(1)).strip() if m else None), ""


def _crossref_doi_title(doi: str, get: Callable[[str], str]) -> tuple[Optional[str], str]:
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi.strip(), safe='')}"
    raw, err = _safe(url, get)
    if err:
        return None, err
    try:
        titles = json.loads(raw).get("message", {}).get("title") or []
    except Exception:
        return None, ""
    return (titles[0] if titles else None), ""


# Crossref record types that are real works (exclude components/supplementary/datasets/etc.)
_ARTICLE_TYPES = frozenset({
    "journal-article", "proceedings-article", "posted-content", "book-chapter",
    "report", "book", "monograph", "reference-entry", "dissertation",
})


def _crossref_search_strict(title: str, get: Callable[[str], str]) -> tuple[Optional[tuple[str, str, float]], str]:
    """Best STRICT title match among article-type Crossref hits → (doi, canonical, score) or None."""
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 5})
    raw, err = _safe(url, get)
    if err:
        return None, err
    try:
        items = json.loads(raw).get("message", {}).get("items") or []
    except Exception:
        return None, ""
    best = None
    for it in items:
        if it.get("type") and it["type"] not in _ARTICLE_TYPES:
            continue
        cand = (it.get("title") or [""])[0]
        ok, score = titles_match_strict(title, cand)
        if ok and (best is None or score > best[2]):
            best = (it.get("DOI", ""), cand, score)
    return best, ""


def _resolve(fn, *args, get, sleep, max_retries) -> tuple[Optional[object], str]:
    """Call an index fetcher, retrying transient errors with backoff."""
    for attempt in range(max_retries + 1):
        val, err = fn(*args, get)
        if err != "transient":
            return val, err
        if attempt < max_retries:
            sleep(0.5 * (2 ** attempt))
    return None, "transient"


# ── public API ──────────────────────────────────────────────────────────────────


def verify_paper(p: Paper, *, get: Callable[[str], str] = _http_get, today: str = "",
                 sleep: Callable[[float], None] = time.sleep, max_retries: int = 2) -> Paper:
    """Verify *p*; set ``p.verified`` (returns the same object).

    Outcomes (``status`` / ``exists``):
      verified           — id/doi resolved AND canonical title strictly matched   (exists=True)
      id-title-mismatch  — id/doi resolved but the title disagrees → REJECT        (exists=False)
      not-found          — an id/doi was supplied but the index has no such record (exists=False)
      unconfirmed        — title-only; a strict Crossref hint exists but is unverified (exists=False)
      error              — the index could not be reached (transient) — unknown, do NOT trust (exists=False)
      unverified         — nothing to check / no hit                               (exists=False)
    """
    def done(status, via="unverified", canon="", score=0.0):
        p.verified = Verification(exists=(status == "verified"), status=status, via=via,
                                  canonical_title=canon, match_score=round(score, 3), checked=today)
        return p

    # 1. Identifier path — its verdict is FINAL (never rescued by a title search).
    if p.arxiv_id:
        ct, err = _resolve(_arxiv_title, p.arxiv_id, get=get, sleep=sleep, max_retries=max_retries)
        if err == "transient":
            return done("error", "arxiv")
        if ct is None:
            return done("not-found", "arxiv")
        if not p.title:
            if not p.url:
                p.url = f"https://arxiv.org/abs/{strip_arxiv_prefix(p.arxiv_id)}"
            return done("verified", "arxiv", ct, 1.0)
        ok, score = titles_match_strict(p.title, ct)
        if ok:
            if not p.url:
                p.url = f"https://arxiv.org/abs/{strip_arxiv_prefix(p.arxiv_id)}"
            return done("verified", "arxiv", ct, score)
        return done("id-title-mismatch", "arxiv", ct, score)

    if p.doi:
        ct, err = _resolve(_crossref_doi_title, p.doi, get=get, sleep=sleep, max_retries=max_retries)
        if err == "transient":
            return done("error", "crossref")
        if ct is None:
            return done("not-found", "crossref")
        if not p.title:
            return done("verified", "crossref", ct, 1.0)
        ok, score = titles_match_strict(p.title, ct)
        return done("verified" if ok else "id-title-mismatch", "crossref", ct, score)

    # 2. Title-only path — NEVER 'verified'. A strict hit is a candidate hint, exists=False.
    if p.title:
        hit, err = _resolve(_crossref_search_strict, p.title, get=get, sleep=sleep, max_retries=max_retries)
        if err == "transient":
            return done("error", "crossref")
        if hit:
            doi, canon, score = hit
            p.doi = p.doi or doi          # a candidate, not a confirmation
            return done("unconfirmed", "crossref", canon, score)
        return done("not-found", "crossref")

    return done("unverified")


def verify_all(papers: list[Paper], *, get: Callable[[str], str] = _http_get, today: str = "",
               sleep: Callable[[float], None] = time.sleep, throttle: float = 0.0) -> dict:
    """Verify a list in place; return a status breakdown. *throttle* sleeps that many seconds BETWEEN
    papers so a large (deepened) package doesn't burst past the arXiv/Crossref rate limit and get a
    wave of false `error` statuses — the per-paper retry/backoff can't recover from a sustained 429."""
    from collections import Counter
    statuses = Counter()
    unconfirmed, rejected, errored = [], [], []
    for i, p in enumerate(papers):
        verify_paper(p, get=get, today=today, sleep=sleep)
        if throttle and i < len(papers) - 1:
            sleep(throttle)
        statuses[p.verified.status] += 1
        if p.verified.status == "unconfirmed":
            unconfirmed.append(p.cite_key)
        elif p.verified.status in ("id-title-mismatch", "not-found"):
            rejected.append(p.cite_key)
        elif p.verified.status == "error":
            errored.append(p.cite_key)
    return {
        "total": len(papers),
        "verified": statuses.get("verified", 0),
        "by_status": dict(statuses),
        "unconfirmed": unconfirmed,   # title-only hints — need an id/doi to ship
        "rejected": rejected,         # not-found or id/title mismatch — likely fabricated/wrong
        "errored": errored,           # index unreachable — unknown
    }
